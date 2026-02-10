use crate::cards::Card;
use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

/// Create a Sentry with given behavior and HP.
/// Behaviors: "D3" (7 HP), "3D" (8 HP), "2D" (7 HP at A0)
pub fn create(behavior: &str, hp: i32) -> Monster {
    Monster::new(
        "Sentry".to_string(),
        hp,
        "sentry".to_string(),
        behavior.to_string(),
        true, // die-controlled
    )
}

/// Sentry die move: 2-char behavior, 1-3→char 0, 4-6→char 1.
pub fn select_die_move(monster: &mut Monster, roll: u8) {
    let idx = if roll <= 3 { 0 } else { 1 };
    let ch = monster.behavior.chars().nth(idx).unwrap_or(' ');
    set_move(monster, ch);
}

pub fn set_move(monster: &mut Monster, ch: char) {
    monster.current_move = ch;
    monster.intent = match ch {
        'D' => Intent::Debuff,
        '2' | '3' => Intent::Attack,
        _ => Intent::Unknown,
    };
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    let mut result = MoveResult::default();
    match monster.current_move {
        'D' => {
            // Bolt: add 1 Dazed to draw pile
            result.cards_to_draw_pile.push(Card::Dazed);
        }
        '2' => {
            // Beam: 2 base damage
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
        }
        '3' => {
            // Beam: 3 base damage
            let damage = calculate_monster_damage(monster, player, 3);
            apply_damage_to_player(player, damage);
        }
        _ => {}
    }
    result
}
