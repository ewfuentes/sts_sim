use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::Intent;
use crate::enemies::MoveResult;

pub fn create() -> Monster {
    Monster::new(
        "Spike Slime (S)".to_string(),
        3,
        "spike_slime_s".to_string(),
        String::new(),
        false,
    )
}

pub fn select_move(monster: &mut Monster) {
    monster.current_move = 'a';
    monster.intent = Intent::Attack;
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    // Always attacks for 1 damage
    let damage = calculate_monster_damage(monster, player, 1);
    apply_damage_to_player(player, damage);
    MoveResult::default()
}
