use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

pub fn create() -> Monster {
    Monster::new(
        "Cultist".to_string(),
        9,
        "cultist".to_string(),
        String::new(),
        false,
    )
}

/// Pre-battle: apply 1 Ritual
pub fn pre_battle(monster: &mut Monster) {
    monster.apply_power(PowerType::Ritual, 1);
}

/// Select move: Turn 1 = Incantation, Turn 2+ = Dark Strike
pub fn select_move(monster: &mut Monster) {
    if monster.first_turn {
        monster.current_move = 'i'; // Incantation
        monster.intent = Intent::Attack; // It does deal damage too
    } else {
        monster.current_move = 'd'; // Dark Strike
        monster.intent = Intent::Attack;
    }
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    match monster.current_move {
        'i' => {
            // Incantation: 1 damage + manually apply +1 Strength
            let damage = calculate_monster_damage(monster, player, 1);
            apply_damage_to_player(player, damage);
            monster.apply_power(PowerType::Strength, 1);
        }
        'd' => {
            // Dark Strike: 1 base damage (Strength adds to this)
            let damage = calculate_monster_damage(monster, player, 1);
            apply_damage_to_player(player, damage);
        }
        _ => {}
    }
    MoveResult::default()
}
