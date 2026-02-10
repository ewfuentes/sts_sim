use crate::cards::Card;
use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;

/// Create Hexaghost (A0): 36 HP, sequential 6-turn cycle.
/// Turn 1: Sear (1 dmg + 1 Burn)
/// Turn 2: Flame Charge (2×2 dmg + 1 Burn)
/// Turn 3: Burn (2 Burns, no damage)
/// Turn 4: Strengthen (3 dmg + 5 block)
/// Turn 5: Sear (2 dmg + 1 Burn)
/// Turn 6: Inferno (2×3 dmg + 2 Burns + 1 Str)
pub fn create() -> Monster {
    Monster::new(
        "Hexaghost".to_string(),
        36,
        "hexaghost".to_string(),
        String::new(),
        false,
    )
}

pub fn select_move(monster: &mut Monster) {
    let cycle = monster.turn_count % 6;
    match cycle {
        0 => {
            // Turn 1: Sear
            monster.current_move = '1';
            monster.intent = Intent::AttackDebuff;
        }
        1 => {
            // Turn 2: Flame Charge
            monster.current_move = '2';
            monster.intent = Intent::AttackDebuff;
        }
        2 => {
            // Turn 3: Burn (debuff only)
            monster.current_move = '3';
            monster.intent = Intent::Debuff;
        }
        3 => {
            // Turn 4: Strengthen
            monster.current_move = '4';
            monster.intent = Intent::AttackDefend;
        }
        4 => {
            // Turn 5: Sear
            monster.current_move = '5';
            monster.intent = Intent::AttackDebuff;
        }
        5 => {
            // Turn 6: Inferno
            monster.current_move = '6';
            monster.intent = Intent::AttackDebuff;
        }
        _ => unreachable!(),
    }
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    let mut result = MoveResult::default();
    match monster.current_move {
        '1' => {
            // Sear: 1 dmg + 1 Burn to discard
            let damage = calculate_monster_damage(monster, player, 1);
            apply_damage_to_player(player, damage);
            result.cards_to_discard_pile.push(Card::Burn);
        }
        '2' => {
            // Flame Charge: 2 dmg × 2 hits + 1 Burn to discard
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
            let damage2 = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage2);
            result.cards_to_discard_pile.push(Card::Burn);
        }
        '3' => {
            // Burn: 2 Burns to discard (no damage)
            result.cards_to_discard_pile.push(Card::Burn);
            result.cards_to_discard_pile.push(Card::Burn);
        }
        '4' => {
            // Strengthen: 3 dmg + 5 block
            let damage = calculate_monster_damage(monster, player, 3);
            apply_damage_to_player(player, damage);
            result.monster_gain_block = 5;
        }
        '5' => {
            // Sear: 2 dmg + 1 Burn to discard
            let damage = calculate_monster_damage(monster, player, 2);
            apply_damage_to_player(player, damage);
            result.cards_to_discard_pile.push(Card::Burn);
        }
        '6' => {
            // Inferno: 3 dmg × 2 hits + 2 Burns + 1 Str
            let damage = calculate_monster_damage(monster, player, 3);
            apply_damage_to_player(player, damage);
            let damage2 = calculate_monster_damage(monster, player, 3);
            apply_damage_to_player(player, damage2);
            result.cards_to_discard_pile.push(Card::Burn);
            result.cards_to_discard_pile.push(Card::Burn);
            monster.apply_power(PowerType::Strength, 1);
        }
        _ => {}
    }
    result
}
