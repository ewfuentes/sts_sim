use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

pub fn create() -> Monster {
    Monster::new(
        "Jaw Worm".to_string(),
        8,
        "jaw_worm".to_string(),
        "sda".to_string(),
        true,
    )
}

/// Set the monster's move based on behavior character.
/// s = Bellow (+1 Str, +2 block)
/// d = Thrash (2 dmg, +1 block)
/// a = Chomp (3 dmg)
pub fn set_move(monster: &mut Monster, ch: char) {
    monster.current_move = ch;
    monster.intent = match ch {
        's' => Intent::DefendBuff,
        'd' => Intent::AttackDefend,
        'a' => Intent::Attack,
        _ => Intent::Unknown,
    };
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    match monster.current_move {
        's' => {
            // Bellow: +1 Strength, +2 block
            monster.apply_power(PowerType::Strength, 1);
            monster.add_block(2);
        }
        'd' => {
            // Thrash: 2 damage, +1 block
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
            monster.add_block(1);
        }
        'a' => {
            // Chomp: 3 damage
            let damage = calculate_monster_damage(monster, player, 3);
            apply_damage_to_player(player, damage);
        }
        _ => {}
    }
    MoveResult::default()
}
