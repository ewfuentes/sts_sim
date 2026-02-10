use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

/// Create The Guardian (A0): 40 HP, sequential.
/// Offensive cycle: Whirlwind+ChargeUp → Fierce Bash → repeat
/// Whirlwind: 2 dmg + 5 block
/// Fierce Bash: 6 dmg
/// TODO: Mode Shift (defensive mode) not yet implemented.
pub fn create() -> Monster {
    Monster::new(
        "The Guardian".to_string(),
        40,
        "the_guardian".to_string(),
        String::new(),
        false,
    )
}

/// Select move for The Guardian.
/// Alternates: Whirlwind+ChargeUp (even turns) and Fierce Bash (odd turns after first).
/// turn_count 0 (first): Whirlwind+ChargeUp
/// turn_count 1: Fierce Bash
/// turn_count 2: Whirlwind+ChargeUp
/// ...
pub fn select_move(monster: &mut Monster) {
    if monster.turn_count % 2 == 0 {
        // Whirlwind + ChargeUp
        monster.current_move = 'W';
        monster.intent = Intent::AttackDefend;
    } else {
        // Fierce Bash
        monster.current_move = 'F';
        monster.intent = Intent::Attack;
    }
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    let mut result = MoveResult::default();
    match monster.current_move {
        'W' => {
            // Whirlwind: 2 dmg × 1 hit
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
            // ChargeUp: gain 5 block
            result.monster_gain_block = 5;
        }
        'F' => {
            // Fierce Bash: 6 dmg
            let damage = calculate_monster_damage(monster, player, 6);
            apply_damage_to_player(player, damage);
        }
        _ => {}
    }
    result
}
