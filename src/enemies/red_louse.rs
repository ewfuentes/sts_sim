use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

pub fn create() -> Monster {
    Monster::new(
        "Red Louse".to_string(),
        3,
        "red_louse".to_string(),
        "S21".to_string(),
        true,
    )
}

pub fn create_with_behavior(behavior: &str) -> Monster {
    Monster::new(
        "Red Louse".to_string(),
        3,
        "red_louse".to_string(),
        behavior.to_string(),
        true,
    )
}

/// Pre-battle: apply 2 Curl Up
pub fn pre_battle(monster: &mut Monster) {
    monster.apply_power(PowerType::CurlUp, 2);
}

/// Set move based on behavior character.
/// S = Strengthen (+1 Str)
/// 1 = Bite (1 dmg)
/// 2 = Bite (2 dmg)
pub fn set_move(monster: &mut Monster, ch: char) {
    monster.current_move = ch;
    monster.intent = match ch {
        'S' => Intent::Buff,
        '1' | '2' => Intent::Attack,
        _ => Intent::Unknown,
    };
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    match monster.current_move {
        'S' => {
            // Strengthen: +1 Strength
            monster.apply_power(PowerType::Strength, 1);
        }
        '1' => {
            // Bite: 1 base damage
            let damage = calculate_monster_damage(monster, player, 1);
            apply_damage_to_player(player, damage);
        }
        '2' => {
            // Bite: 2 base damage
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
        }
        _ => {}
    }
    MoveResult::default()
}
