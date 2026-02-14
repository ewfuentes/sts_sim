pub mod jaw_worm;
pub mod cultist;
pub mod red_louse;
pub mod green_louse;
pub mod acid_slime_m;
pub mod spike_slime_m;
pub mod spike_slime_s;
pub mod fungi_beast;
pub mod blue_slaver;
pub mod red_slaver;
pub mod looter;
pub mod gremlin;
pub mod gremlin_nob;
pub mod lagavulin;
pub mod sentry;
pub mod the_guardian;
pub mod hexaghost;
pub mod slime_boss;
pub mod dummy;

use crate::cards::Card;
use crate::creature::{Monster, Player};
use crate::die::TheDie;

/// Side effects from a monster's move that need to be processed by CombatState.
#[derive(Default)]
pub struct MoveResult {
    pub cards_to_draw_pile: Vec<Card>,
    pub cards_to_discard_pile: Vec<Card>,
    pub player_gold_change: i32,
    pub escaped: bool,
    pub spawn_monsters: Vec<Monster>,
    pub monster_gain_block: i32,
}

/// Select a move for a die-controlled monster based on die roll.
pub fn select_die_move(monster: &mut Monster, roll: u8) {
    let idx = TheDie::behavior_index(roll);
    let ch = monster.behavior.chars().nth(idx).unwrap_or(' ');

    match monster.monster_id.as_str() {
        "jaw_worm" => jaw_worm::set_move(monster, ch.to_ascii_lowercase()),
        "red_louse" => red_louse::set_move(monster, ch),
        "green_louse" => green_louse::set_move(monster, ch),
        "acid_slime_m" => acid_slime_m::set_move(monster, ch),
        "spike_slime_m" => spike_slime_m::set_move(monster, ch),
        "fungi_beast" => fungi_beast::set_move(monster, ch),
        "blue_slaver" => blue_slaver::set_move(monster, ch),
        "red_slaver" => red_slaver::set_move(monster, ch),
        "sentry" => sentry::set_move(monster, ch),
        _ => {}
    }
}

/// Select a move for a die-controlled monster with a 6-char behavior string.
/// Maps die roll 1-6 directly to behavior index 0-5 (one action per face).
pub fn select_die_move_direct(monster: &mut Monster, roll: u8) {
    let idx = (roll - 1) as usize;
    let ch = monster.behavior.chars().nth(idx).unwrap_or(' ');

    match monster.monster_id.as_str() {
        "dummy" => dummy::set_move(monster, ch),
        _ => {}
    }
}

/// Select die move for 2-char behavior monsters (sentries).
/// Roll 1-3→char 0, 4-6→char 1.
pub fn select_die_move_2char(monster: &mut Monster, roll: u8) {
    match monster.monster_id.as_str() {
        "sentry" => sentry::select_die_move(monster, roll),
        _ => {}
    }
}

/// Select move for non-die-controlled monster.
pub fn select_move(monster: &mut Monster) {
    match monster.monster_id.as_str() {
        "cultist" => cultist::select_move(monster),
        "spike_slime_s" => spike_slime_s::select_move(monster),
        "looter" => looter::select_move(monster),
        "gremlin_angry" => gremlin::select_move_angry(monster),
        "gremlin_sneaky" => gremlin::select_move_sneaky(monster),
        "gremlin_fat" => gremlin::select_move_fat(monster),
        "gremlin_wizard" => gremlin::select_move_wizard(monster),
        "gremlin_nob" => gremlin_nob::select_move(monster),
        "lagavulin" => lagavulin::select_move(monster),
        "the_guardian" => the_guardian::select_move(monster),
        "hexaghost" => hexaghost::select_move(monster),
        "slime_boss" => slime_boss::select_move(monster),
        _ => {}
    }
}

/// Execute the current move for a monster against the player.
/// Returns MoveResult with side effects to be processed by CombatState.
pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    match monster.monster_id.as_str() {
        "jaw_worm" => jaw_worm::execute_move(monster, player),
        "cultist" => cultist::execute_move(monster, player),
        "red_louse" => red_louse::execute_move(monster, player),
        "green_louse" => green_louse::execute_move(monster, player),
        "acid_slime_m" => acid_slime_m::execute_move(monster, player),
        "spike_slime_m" => spike_slime_m::execute_move(monster, player),
        "spike_slime_s" => spike_slime_s::execute_move(monster, player),
        "fungi_beast" => fungi_beast::execute_move(monster, player),
        "blue_slaver" => blue_slaver::execute_move(monster, player),
        "red_slaver" => red_slaver::execute_move(monster, player),
        "looter" => looter::execute_move(monster, player),
        "gremlin_angry" => gremlin::execute_move_angry(monster, player),
        "gremlin_sneaky" => gremlin::execute_move_sneaky(monster, player),
        "gremlin_fat" => gremlin::execute_move_fat(monster, player),
        "gremlin_wizard" => gremlin::execute_move_wizard(monster, player),
        "gremlin_nob" => gremlin_nob::execute_move(monster, player),
        "lagavulin" => lagavulin::execute_move(monster, player),
        "sentry" => sentry::execute_move(monster, player),
        "the_guardian" => the_guardian::execute_move(monster, player),
        "hexaghost" => hexaghost::execute_move(monster, player),
        "slime_boss" => slime_boss::execute_move(monster, player),
        "dummy" => dummy::execute_move(monster, player),
        _ => MoveResult::default(),
    }
}

/// Apply pre-battle setup for a monster.
pub fn pre_battle(monster: &mut Monster) {
    match monster.monster_id.as_str() {
        "cultist" => cultist::pre_battle(monster),
        "red_louse" => red_louse::pre_battle(monster),
        "green_louse" => green_louse::pre_battle(monster),
        "fungi_beast" => fungi_beast::pre_battle(monster),
        _ => {}
    }
}
