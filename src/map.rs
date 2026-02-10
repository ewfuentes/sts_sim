use pyo3::prelude::*;
use rand::rngs::StdRng;
use rand::seq::SliceRandom;
use rand::{Rng, SeedableRng};

use crate::enums::RoomType;

/// A single node on the Act 1 map.
#[pyclass]
#[derive(Clone, Debug)]
pub struct MapNode {
    #[pyo3(get)]
    pub row: i32,
    #[pyo3(get)]
    pub col: i32,
    #[pyo3(get)]
    pub room_type: RoomType,
    #[pyo3(get)]
    pub connections: Vec<(i32, i32)>,  // (row, col) of connected nodes
}

/// The full Act 1 map.
#[pyclass]
#[derive(Clone, Debug)]
pub struct ActMap {
    #[pyo3(get)]
    pub nodes: Vec<MapNode>,
    #[pyo3(get)]
    pub layout_id: i32,
}

#[pymethods]
impl ActMap {
    /// Get the node at a given (row, col), if it exists.
    pub fn get_node(&self, row: i32, col: i32) -> Option<MapNode> {
        self.nodes.iter().find(|n| n.row == row && n.col == col).cloned()
    }

    /// Get all nodes at a given row.
    pub fn get_row(&self, row: i32) -> Vec<MapNode> {
        self.nodes.iter().filter(|n| n.row == row).cloned().collect()
    }

    /// Get the starting nodes (row 12).
    pub fn get_start_nodes(&self) -> Vec<MapNode> {
        self.get_row(12)
    }

    /// Get connections from a node.
    pub fn get_connections(&self, row: i32, col: i32) -> Vec<MapNode> {
        if let Some(node) = self.get_node(row, col) {
            node.connections.iter()
                .filter_map(|&(r, c)| self.get_node(r, c))
                .collect()
        } else {
            vec![]
        }
    }
}

// Layout templates: each row is a 7-char string, chars = room type
// '.' = empty, 'B' = boss, 'R' = rest, '$' = shop, '?' = event,
// 'M' = monster, 'T' = treasure, 'E' = elite, 'D' = dark token, 'L' = light token

const LAYOUT_1: [&str; 13] = [
    "...B...",  // row 0 (boss)
    ".RR.RR.",  // row 1
    "D.$.D.?",  // row 2
    "L.M.?.L",  // row 3
    ".D..L.D",  // row 4
    "M.?.D.M",  // row 5
    "T..T.T.",  // row 6
    ".L..L.D",  // row 7
    "D.M.D.L",  // row 8
    "M.L.?.?",  // row 9
    "?..M..M",  // row 10
    ".?.?.?.",  // row 11
    "...M...",  // row 12 (start)
];

const LAYOUT_2: [&str; 13] = [
    "...B...",  // row 0 (boss)
    ".RR.RR.",  // row 1
    "?.D.D.?",  // row 2
    "E.L.?.D",  // row 3
    "L.?.L.L",  // row 4
    ".M.D.D.",  // row 5
    ".T.TT.T",  // row 6
    "?.D.M.D",  // row 7
    "D.M.L.L",  // row 8
    "$.L.?.M",  // row 9
    "M..M..?",  // row 10
    ".?.?.?.",  // row 11
    "...M...",  // row 12 (start)
];

fn resolve_token(ch: char, dark_tokens: &mut Vec<RoomType>, light_tokens: &mut Vec<RoomType>) -> RoomType {
    match ch {
        'B' => RoomType::Boss,
        'R' => RoomType::Rest,
        '$' => RoomType::Shop,
        '?' => RoomType::Event,
        'M' => RoomType::Monster,
        'T' => RoomType::Treasure,
        'E' => RoomType::Elite,
        'D' => dark_tokens.pop().unwrap_or(RoomType::Monster),
        'L' => light_tokens.pop().unwrap_or(RoomType::Event),
        _ => RoomType::Empty,
    }
}

fn make_token_pools(rng: &mut StdRng) -> (Vec<RoomType>, Vec<RoomType>) {
    // Dark tokens: 3 Elite, 3 Monster, 2 Event
    let mut dark = vec![
        RoomType::Elite, RoomType::Elite, RoomType::Elite,
        RoomType::Monster, RoomType::Monster, RoomType::Monster,
        RoomType::Event, RoomType::Event,
    ];
    // Light tokens: 1 Monster, 1 Event, 2 Shop, 3 Rest
    let mut light = vec![
        RoomType::Monster,
        RoomType::Event,
        RoomType::Shop, RoomType::Shop,
        RoomType::Rest, RoomType::Rest, RoomType::Rest,
    ];
    dark.shuffle(rng);
    light.shuffle(rng);
    (dark, light)
}

/// Build adjacency: each non-empty node connects to nearby nodes in the row above (row - 1).
/// Connections go "upward" (toward boss). From row r, col c, can connect to row r-1 cols c-1, c, c+1
/// if those positions have a room.
fn build_connections(nodes: &mut Vec<MapNode>) {
    let positions: Vec<(i32, i32, RoomType)> = nodes.iter()
        .map(|n| (n.row, n.col, n.room_type))
        .collect();

    for node in nodes.iter_mut() {
        if node.row == 0 {
            continue; // boss has no outgoing connections
        }
        let target_row = node.row - 1;
        for dc in -1..=1 {
            let target_col = node.col + dc;
            if target_col < 0 || target_col >= 7 {
                continue;
            }
            if positions.iter().any(|&(r, c, rt)| r == target_row && c == target_col && rt != RoomType::Empty) {
                node.connections.push((target_row, target_col));
            }
        }
    }
}

/// Generate the Act 1 map.
#[pyfunction]
#[pyo3(signature = (seed=None))]
pub fn generate_map(seed: Option<u64>) -> ActMap {
    let s = seed.unwrap_or(0);
    let mut rng = StdRng::seed_from_u64(s);

    // Choose layout
    let layout_id = if rng.gen::<bool>() { 1 } else { 2 };
    let layout = if layout_id == 1 { &LAYOUT_1 } else { &LAYOUT_2 };

    // Create token pools
    let (mut dark_tokens, mut light_tokens) = make_token_pools(&mut rng);

    // Build nodes
    let mut nodes = Vec::new();
    for (row, row_str) in layout.iter().enumerate() {
        for (col, ch) in row_str.chars().enumerate() {
            if ch == '.' {
                continue; // skip empty
            }
            let room_type = resolve_token(ch, &mut dark_tokens, &mut light_tokens);
            nodes.push(MapNode {
                row: row as i32,
                col: col as i32,
                room_type,
                connections: Vec::new(),
            });
        }
    }

    // Build connections
    build_connections(&mut nodes);

    ActMap {
        nodes,
        layout_id,
    }
}
