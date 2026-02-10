use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::Intent;
use crate::enemies::MoveResult;

pub fn create() -> Monster {
    Monster::new(
        "Looter".to_string(),
        9,
        "looter".to_string(),
        String::new(),
        false,
    )
}

/// Sequential pattern: Mug → Lunge+Block → Escape
pub fn select_move(monster: &mut Monster) {
    if monster.first_turn {
        monster.current_move = 'm'; // Mug
        monster.intent = Intent::Attack;
    } else if monster.turn_count == 1 {
        monster.current_move = 'l'; // Lunge
        monster.intent = Intent::AttackDefend;
    } else {
        monster.current_move = 'e'; // Escape
        monster.intent = Intent::Escape;
    }
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    let mut result = MoveResult::default();
    match monster.current_move {
        'm' => {
            // Mug: 2 dmg
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
        }
        'l' => {
            // Lunge: 3 dmg + gain 1 block
            let damage = calculate_monster_damage(monster, player, 3);
            apply_damage_to_player(player, damage);
            monster.add_block(1);
        }
        'e' => {
            // Escape: steal 2 gold and flee
            result.player_gold_change = -2;
            result.escaped = true;
        }
        _ => {}
    }
    result
}
