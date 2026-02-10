use crate::cards::Card;
use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

pub fn create(behavior: &str) -> Monster {
    Monster::new(
        "Acid Slime (M)".to_string(),
        5,
        "acid_slime_m".to_string(),
        behavior.to_string(),
        true,
    )
}

/// Behavior chars (case-sensitive):
/// 'C' = Wound Tackle: 2 dmg + add Dazed to draw
/// 'L' = Weak Lick: apply 1 Weak
/// 'A' = Normal Tackle: 2 dmg
pub fn set_move(monster: &mut Monster, ch: char) {
    monster.current_move = ch;
    monster.intent = match ch {
        'C' => Intent::AttackDebuff,
        'L' => Intent::Debuff,
        'A' => Intent::Attack,
        _ => Intent::Unknown,
    };
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    let mut result = MoveResult::default();
    match monster.current_move {
        'C' => {
            // Wound Tackle: 2 dmg + add Dazed
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
            result.cards_to_draw_pile.push(Card::Dazed);
        }
        'L' => {
            // Weak Lick: apply 1 Weak
            player.apply_power(PowerType::Weak, 1);
        }
        'A' => {
            // Normal Tackle: 2 dmg
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
        }
        _ => {}
    }
    result
}
