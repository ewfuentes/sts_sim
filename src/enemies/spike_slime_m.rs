use crate::cards::Card;
use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

pub fn create(behavior: &str) -> Monster {
    Monster::new(
        "Spike Slime (M)".to_string(),
        5,
        "spike_slime_m".to_string(),
        behavior.to_string(),
        true,
    )
}

/// Behavior chars (case-sensitive):
/// 'V' = Lick: 1 dmg + apply 1 Vulnerable
/// 'D' = Corrosive Spit: 1 dmg + add Dazed to draw
/// '2' = Attack: 2 dmg
pub fn set_move(monster: &mut Monster, ch: char) {
    monster.current_move = ch;
    monster.intent = match ch {
        'V' => Intent::AttackDebuff,
        'D' => Intent::AttackDebuff,
        '2' => Intent::Attack,
        _ => Intent::Unknown,
    };
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    let mut result = MoveResult::default();
    match monster.current_move {
        'V' => {
            // Lick: 1 dmg + apply 1 Vulnerable
            let damage = calculate_monster_damage(monster, player, 1);
            apply_damage_to_player(player, damage);
            player.apply_power(PowerType::Vulnerable, 1);
        }
        'D' => {
            // Corrosive Spit: 1 dmg + add Dazed
            let damage = calculate_monster_damage(monster, player, 1);
            apply_damage_to_player(player, damage);
            result.cards_to_draw_pile.push(Card::Dazed);
        }
        '2' => {
            // Attack: 2 dmg
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
        }
        _ => {}
    }
    result
}
