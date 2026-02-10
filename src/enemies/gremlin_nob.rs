use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

/// Create a Gremlin Nob (A0): 14 HP, sequential.
/// Turn 1: Bellow (apply Anger 1), then Skull Bash (3 dmg) forever.
pub fn create() -> Monster {
    Monster::new(
        "Gremlin Nob".to_string(),
        14,
        "gremlin_nob".to_string(),
        "BS".to_string(),
        false, // sequential, not die-controlled
    )
}

/// Select move for Gremlin Nob.
pub fn select_move(monster: &mut Monster) {
    if monster.first_turn {
        // First turn: Bellow
        monster.current_move = 'B';
        monster.intent = Intent::Buff;
    } else {
        // All subsequent turns: Skull Bash
        monster.current_move = 'S';
        monster.intent = Intent::Attack;
    }
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    match monster.current_move {
        'B' => {
            // Bellow: apply Anger power (1 stack)
            monster.apply_power(PowerType::Anger, 1);
        }
        'S' => {
            // Skull Bash: 3 base damage
            let damage = calculate_monster_damage(monster, player, 3);
            apply_damage_to_player(player, damage);
        }
        _ => {}
    }
    MoveResult::default()
}
