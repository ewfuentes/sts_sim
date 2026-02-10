use pyo3::prelude::*;

use crate::combat::CombatState;
use crate::enums::Character;
use crate::creature::Monster;
use crate::enemies::{
    cultist, jaw_worm, red_louse, green_louse,
    acid_slime_m, spike_slime_m, spike_slime_s,
    fungi_beast, blue_slaver, red_slaver, looter, gremlin,
    gremlin_nob, lagavulin, sentry,
    the_guardian, hexaghost, slime_boss,
};

/// Create an encounter by name. Returns a CombatState ready to play.
#[pyfunction]
#[pyo3(signature = (name, seed=None, character=None))]
pub fn create_encounter(name: &str, seed: Option<u64>, character: Option<Character>) -> PyResult<CombatState> {
    let s = seed.unwrap_or(0);
    let monsters = match name {
        // --- Easy / first-fight pool ---
        "jaw_worm" => vec![jaw_worm::create()],
        "cultist" => vec![cultist::create()],
        "louse" => create_louse_encounter(s),

        // --- Strong pool ---
        "cultist_and_spike_slime" => {
            let behaviors = ["2DV", "V2D", "DV2", "VD2"];
            let b = behaviors[(s % behaviors.len() as u64) as usize];
            vec![cultist::create(), spike_slime_m::create(b)]
        }
        "cultist_and_louse" => {
            let green_b = if s % 2 == 0 { "1W2" } else { "21W" };
            vec![cultist::create(), green_louse::create(green_b)]
        }
        "fungi_beasts" => {
            vec![fungi_beast::create("21S"), fungi_beast::create("2S1")]
        }
        "slime_trio" => {
            let acid_behaviors = ["CAL", "LCA", "ALC", "LAC"];
            let spike_behaviors = ["2DV", "V2D", "DV2", "VD2"];
            let ab = acid_behaviors[(s % acid_behaviors.len() as u64) as usize];
            let sb = spike_behaviors[((s / 4) % spike_behaviors.len() as u64) as usize];
            vec![spike_slime_s::create(), acid_slime_m::create(ab), spike_slime_m::create(sb)]
        }
        "3_louse_hard" => {
            vec![
                red_louse::create_with_behavior("S22"),
                green_louse::create(if s % 2 == 0 { "1W2" } else { "21W" }),
                red_louse::create_with_behavior("21S"),
            ]
        }
        "large_slime" => {
            let behaviors = ["CAL", "LCA", "ALC", "LAC"];
            let b = behaviors[(s % behaviors.len() as u64) as usize];
            // Large slime is just an acid slime M with 8 HP for now
            let mut m = acid_slime_m::create(b);
            m.hp = 8;
            m.max_hp = 8;
            m.name = "Acid Slime (L)".to_string();
            m.monster_id = "acid_slime_l".to_string();
            vec![m]
        }
        "blue_slaver" => {
            vec![blue_slaver::create("W2d")]
        }
        "red_slaver" => {
            vec![red_slaver::create("DV3")]
        }
        "looter" => {
            vec![looter::create()]
        }
        "sneaky_gremlin_team" => create_gremlin_team(s, "sneaky"),
        "angry_gremlin_team" => create_gremlin_team(s, "angry"),

        // --- Elites ---
        "gremlin_nob" => vec![gremlin_nob::create()],
        "lagavulin" => vec![lagavulin::create()],
        "sentries" => {
            vec![
                sentry::create("D3", 7),
                sentry::create("3D", 8),
                sentry::create("2D", 7),
            ]
        }

        // --- Bosses ---
        "the_guardian" => vec![the_guardian::create()],
        "hexaghost" => vec![hexaghost::create()],
        "slime_boss" => vec![slime_boss::create()],

        _ => {
            return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                format!("Unknown encounter: {}", name),
            ))
        }
    };

    Ok(CombatState::new_with_character(monsters, seed, character))
}

/// Create a 2-Louse encounter: 1 Red + 1 Green (behavior from pool based on seed).
fn create_louse_encounter(seed: u64) -> Vec<Monster> {
    let green_behavior = if seed % 2 == 0 { "1W2" } else { "21W" };
    vec![
        red_louse::create(),
        green_louse::create(green_behavior),
    ]
}

/// Create a gremlin team: 1 leader + 2 random gremlins.
fn create_gremlin_team(seed: u64, leader_type: &str) -> Vec<Monster> {
    let leader = match leader_type {
        "sneaky" => gremlin::create_sneaky(),
        "angry" => gremlin::create_angry(),
        _ => gremlin::create_angry(),
    };

    // Pick 2 random gremlins from pool
    let pool = ["angry", "sneaky", "fat", "wizard"];
    let g1 = pool[(seed % pool.len() as u64) as usize];
    let g2 = pool[((seed / 4) % pool.len() as u64) as usize];

    let create_gremlin = |name: &str| -> Monster {
        match name {
            "angry" => gremlin::create_angry(),
            "sneaky" => gremlin::create_sneaky(),
            "fat" => gremlin::create_fat(),
            "wizard" => gremlin::create_wizard(),
            _ => gremlin::create_angry(),
        }
    };

    vec![leader, create_gremlin(g1), create_gremlin(g2)]
}
