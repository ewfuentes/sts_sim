use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

/// Angry Gremlin: 4 HP, always attacks for 1 damage
/// Has Angry power (gains +1 Str when damaged, handled in damage.rs)
pub fn create_angry() -> Monster {
    let mut m = Monster::new(
        "Mad Gremlin".to_string(),
        4,
        "gremlin_angry".to_string(),
        String::new(),
        false,
    );
    m.apply_power(PowerType::Anger, 1);
    m
}

/// Sneaky Gremlin: 2 HP, always attacks for 2 damage
pub fn create_sneaky() -> Monster {
    Monster::new(
        "Sneaky Gremlin".to_string(),
        2,
        "gremlin_sneaky".to_string(),
        String::new(),
        false,
    )
}

/// Fat Gremlin: 3 HP, always attacks for 1 damage
pub fn create_fat() -> Monster {
    Monster::new(
        "Fat Gremlin".to_string(),
        3,
        "gremlin_fat".to_string(),
        String::new(),
        false,
    )
}

/// Gremlin Wizard: 4 HP, charges for 2 turns then attacks for 3 damage
pub fn create_wizard() -> Monster {
    let mut m = Monster::new(
        "Gremlin Wizard".to_string(),
        4,
        "gremlin_wizard".to_string(),
        String::new(),
        false,
    );
    // turn_count starts at 0, charges on turns 0 and 1, attacks from turn 2+
    m
}

pub fn select_move_angry(monster: &mut Monster) {
    monster.current_move = 'a';
    monster.intent = Intent::Attack;
}

pub fn select_move_sneaky(monster: &mut Monster) {
    monster.current_move = 'a';
    monster.intent = Intent::Attack;
}

pub fn select_move_fat(monster: &mut Monster) {
    monster.current_move = 'a';
    monster.intent = Intent::Attack;
}

pub fn select_move_wizard(monster: &mut Monster) {
    // Charges for first 2 turns (turn_count 0, 1), attacks from turn 2+
    if monster.turn_count < 2 {
        monster.current_move = 'c'; // Charge
        monster.intent = Intent::Unknown; // Charging intent
    } else {
        monster.current_move = 'a'; // Attack
        monster.intent = Intent::Attack;
    }
}

pub fn execute_move_angry(monster: &mut Monster, player: &mut Player) -> MoveResult {
    let damage = calculate_monster_damage(monster, player, 1);
    apply_damage_to_player(player, damage);
    MoveResult::default()
}

pub fn execute_move_sneaky(monster: &mut Monster, player: &mut Player) -> MoveResult {
    let damage = calculate_monster_damage(monster, player, 2);
    apply_damage_to_player(player, damage);
    MoveResult::default()
}

pub fn execute_move_fat(monster: &mut Monster, player: &mut Player) -> MoveResult {
    let damage = calculate_monster_damage(monster, player, 1);
    apply_damage_to_player(player, damage);
    MoveResult::default()
}

pub fn execute_move_wizard(monster: &mut Monster, player: &mut Player) -> MoveResult {
    match monster.current_move {
        'c' => {
            // Charging — does nothing
        }
        'a' => {
            // Attack for 3 damage
            let damage = calculate_monster_damage(monster, player, 3);
            apply_damage_to_player(player, damage);
        }
        _ => {}
    }
    MoveResult::default()
}
