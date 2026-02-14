use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

pub fn create() -> Monster {
    Monster::new(
        "Dummy".to_string(),
        8,
        "dummy".to_string(),
        "nbswav".to_string(),
        true,
    )
}

pub fn create_boss() -> Monster {
    Monster::new(
        "Dummy Boss".to_string(),
        16,
        "dummy".to_string(),
        "nbswav".to_string(),
        true,
    )
}

/// Set the monster's move based on behavior character.
/// n = Nothing
/// b = Block (+2 block)
/// s = Strength (+1 Str)
/// w = Weak (apply 1 Weak to player)
/// a = Attack (3 damage)
/// v = Vulnerable (apply 1 Vulnerable to player)
pub fn set_move(monster: &mut Monster, ch: char) {
    monster.current_move = ch;
    monster.intent = match ch {
        'n' => Intent::Sleep,
        'b' => Intent::Defend,
        's' => Intent::Buff,
        'w' => Intent::Debuff,
        'a' => Intent::Attack,
        'v' => Intent::StrongDebuff,
        _ => Intent::Unknown,
    };
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    match monster.current_move {
        'n' => {
            // Nothing
        }
        'b' => {
            // Block: +2 block
            monster.add_block(2);
        }
        's' => {
            // Strength: +1 Strength
            monster.apply_power(PowerType::Strength, 1);
        }
        'w' => {
            // Weak: apply 1 Weak to player
            player.apply_power(PowerType::Weak, 1);
        }
        'a' => {
            // Attack: 3 damage
            let damage = calculate_monster_damage(monster, player, 3);
            apply_damage_to_player(player, damage);
        }
        'v' => {
            // Vulnerable: apply 1 Vulnerable to player
            player.apply_power(PowerType::Vulnerable, 1);
        }
        _ => {}
    }
    MoveResult::default()
}
