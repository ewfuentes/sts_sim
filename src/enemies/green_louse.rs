use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

/// Create a Green Louse with a specific behavior string.
pub fn create(behavior: &str) -> Monster {
    Monster::new(
        "Green Louse".to_string(),
        3,
        "green_louse".to_string(),
        behavior.to_string(),
        true,
    )
}

/// Pre-battle: apply 2 Curl Up
pub fn pre_battle(monster: &mut Monster) {
    monster.apply_power(PowerType::CurlUp, 2);
}

/// Set move based on behavior character.
/// W = Weaken (apply 1 Weak to player)
/// 1 = Bite (1 dmg)
/// 2 = Bite (2 dmg)
pub fn set_move(monster: &mut Monster, ch: char) {
    monster.current_move = ch;
    monster.intent = match ch {
        'W' => Intent::Debuff,
        '1' | '2' => Intent::Attack,
        _ => Intent::Unknown,
    };
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    match monster.current_move {
        'W' => {
            // Weaken: apply 1 Weak to player
            player.apply_power(PowerType::Weak, 1);
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
