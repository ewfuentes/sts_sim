use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

/// Create a Lagavulin (A0): 22 HP, sequential.
/// Pattern: Sleep → Attack, Attack, Siphon Soul, Attack, Attack, Siphon Soul, ...
pub fn create() -> Monster {
    Monster::new(
        "Lagavulin".to_string(),
        22,
        "lagavulin".to_string(),
        "ZAAS".to_string(),
        false, // sequential, not die-controlled
    )
}

/// Select move for Lagavulin.
/// turn_count 0 (first_turn): Sleep (Z) — wakes up
/// Then cycles (turn_count - 1) % 3: 0→Attack, 1→Attack, 2→Siphon Soul
pub fn select_move(monster: &mut Monster) {
    if monster.first_turn {
        monster.current_move = 'Z';
        monster.intent = Intent::Sleep;
    } else {
        // turn_count is 1 on second turn (after first_turn=false, turn_count was incremented to 1)
        let cycle = (monster.turn_count - 1) % 3;
        match cycle {
            0 | 1 => {
                monster.current_move = 'A';
                monster.intent = Intent::Attack;
            }
            2 => {
                monster.current_move = 'S';
                monster.intent = Intent::StrongDebuff;
            }
            _ => unreachable!(),
        }
    }
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    match monster.current_move {
        'Z' => {
            // Sleep: wake up (no action)
        }
        'A' => {
            // Attack: 4 base damage
            let damage = calculate_monster_damage(monster, player, 4);
            apply_damage_to_player(player, damage);
        }
        'S' => {
            // Siphon Soul: apply 2 Weak to player, gain 1 Str
            player.apply_power(PowerType::Weak, 2);
            monster.apply_power(PowerType::Strength, 1);
        }
        _ => {}
    }
    MoveResult::default()
}
