use crate::cards::Card;
use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

pub fn create(behavior: &str) -> Monster {
    Monster::new(
        "Blue Slaver".to_string(),
        10,
        "blue_slaver".to_string(),
        behavior.to_string(),
        true,
    )
}

/// Behavior chars (case-sensitive):
/// 'd' = Stab small (byte 1): 2 dmg + add Dazed
/// 'D' = Stab large (byte 2): 3 dmg + add Dazed
/// 'W' = Rake (byte 3): 2 dmg + apply 1 Weak
/// '2' = Sweep small (byte 4): 2 dmg
/// '3' = Sweep large (byte 5): 3 dmg
pub fn set_move(monster: &mut Monster, ch: char) {
    monster.current_move = ch;
    monster.intent = match ch {
        'd' | 'D' | 'W' => Intent::AttackDebuff,
        '2' | '3' => Intent::Attack,
        _ => Intent::Unknown,
    };
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    let mut result = MoveResult::default();
    match monster.current_move {
        'd' => {
            // Stab small: 2 dmg + Dazed
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
            result.cards_to_draw_pile.push(Card::Dazed);
        }
        'D' => {
            // Stab large: 3 dmg + Dazed
            let damage = calculate_monster_damage(monster, player, 3);
            apply_damage_to_player(player, damage);
            result.cards_to_draw_pile.push(Card::Dazed);
        }
        'W' => {
            // Rake: 2 dmg + apply 1 Weak
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
            player.apply_power(PowerType::Weak, 1);
        }
        '2' => {
            // Sweep small: 2 dmg
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
        }
        '3' => {
            // Sweep large: 3 dmg
            let damage = calculate_monster_damage(monster, player, 3);
            apply_damage_to_player(player, damage);
        }
        _ => {}
    }
    result
}
