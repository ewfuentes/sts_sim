use crate::cards::Card;
use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

pub fn create(behavior: &str) -> Monster {
    Monster::new(
        "Red Slaver".to_string(),
        10,
        "red_slaver".to_string(),
        behavior.to_string(),
        true,
    )
}

/// Behavior chars (case-sensitive):
/// 'D' = Entangle (byte 2): 2 dmg + add Dazed
/// 'V' = Scrape (byte 3): 2 dmg + apply 1 Vulnerable
/// '3' = Stab (byte 1): 3 dmg
pub fn set_move(monster: &mut Monster, ch: char) {
    monster.current_move = ch;
    monster.intent = match ch {
        'D' | 'V' => Intent::AttackDebuff,
        '3' => Intent::Attack,
        _ => Intent::Unknown,
    };
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    let mut result = MoveResult::default();
    match monster.current_move {
        'D' => {
            // Entangle: 2 dmg + add Dazed
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
            result.cards_to_draw_pile.push(Card::Dazed);
        }
        'V' => {
            // Scrape: 2 dmg + apply 1 Vulnerable
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
            player.apply_power(PowerType::Vulnerable, 1);
        }
        '3' => {
            // Stab: 3 dmg
            let damage = calculate_monster_damage(monster, player, 3);
            apply_damage_to_player(player, damage);
        }
        _ => {}
    }
    result
}
