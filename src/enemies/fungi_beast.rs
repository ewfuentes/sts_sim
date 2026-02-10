use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

pub fn create(behavior: &str) -> Monster {
    let mut m = Monster::new(
        "Fungi Beast".to_string(),
        5,
        "fungi_beast".to_string(),
        behavior.to_string(),
        true,
    );
    // Store strAmount as a custom power (Grow strength amount = 2 for normal)
    m.powers.insert(PowerType::SporeCloud, 1);
    m
}

pub fn pre_battle(monster: &mut Monster) {
    // SporeCloud 1 is already set in create()
    // (In the real game, SporeCloud applies Vulnerable on death)
}

/// Behavior chars:
/// '2' = Bite (byte 1): 2 dmg
/// '1'/'!' = Power Up (byte 2): 1 dmg + apply 1 Str to self
/// 'S'/'s' = Grow (byte 3): apply 2 Str to self (buff only)
pub fn set_move(monster: &mut Monster, ch: char) {
    monster.current_move = ch;
    monster.intent = match ch {
        '2' => Intent::Attack,
        '1' | '!' => Intent::AttackBuff,
        'S' | 's' => Intent::Buff,
        _ => Intent::Unknown,
    };
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    match monster.current_move {
        '2' => {
            // Bite: 2 dmg
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
        }
        '1' | '!' => {
            // Power Up: 1 dmg + apply 1 Str
            let damage = calculate_monster_damage(monster, player, 1);
            apply_damage_to_player(player, damage);
            monster.apply_power(PowerType::Strength, 1);
        }
        'S' | 's' => {
            // Grow: apply 2 Str (normal fungi beast)
            monster.apply_power(PowerType::Strength, 2);
        }
        _ => {}
    }
    MoveResult::default()
}
