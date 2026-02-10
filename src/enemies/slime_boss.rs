use crate::cards::Card;
use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_player, calculate_monster_damage};
use crate::enums::{Intent, PowerType};
use crate::enemies::MoveResult;
use crate::enemies::{acid_slime_m, spike_slime_m};

/// Create Slime Boss (A0): 22 HP, sequential.
/// Cycle: Sticky (3 Slimed) → Tackle (3 dmg + 2 Slimed) → Slam (6 dmg) → repeat.
/// Splits into 3 slimes on death.
pub fn create() -> Monster {
    Monster::new(
        "Slime Boss".to_string(),
        22,
        "slime_boss".to_string(),
        String::new(),
        false,
    )
}

pub fn select_move(monster: &mut Monster) {
    // If half_dead, force split
    if monster.half_dead {
        monster.current_move = 'X'; // Split
        monster.intent = Intent::Unknown;
        return;
    }

    let cycle = monster.turn_count % 3;
    match cycle {
        0 => {
            // Sticky: add Slimed to discard
            monster.current_move = 'S';
            monster.intent = Intent::StrongDebuff;
        }
        1 => {
            // Tackle: 3 dmg + 2 Slimed
            monster.current_move = 'T';
            monster.intent = Intent::AttackDebuff;
        }
        2 => {
            // Slam: 6 dmg
            monster.current_move = 'L';
            monster.intent = Intent::Attack;
        }
        _ => unreachable!(),
    }
}

pub fn execute_move(monster: &mut Monster, player: &mut Player) -> MoveResult {
    let mut result = MoveResult::default();
    match monster.current_move {
        'S' => {
            // Sticky: add 3 Slimed to discard
            for _ in 0..3 {
                result.cards_to_discard_pile.push(Card::Slimed);
            }
        }
        'T' => {
            // Tackle: 3 dmg + 2 Slimed to discard
            let damage = calculate_monster_damage(monster, player, 3);
            apply_damage_to_player(player, damage);
            result.cards_to_discard_pile.push(Card::Slimed);
            result.cards_to_discard_pile.push(Card::Slimed);
        }
        'L' => {
            // Slam: 6 dmg
            let damage = calculate_monster_damage(monster, player, 6);
            apply_damage_to_player(player, damage);
        }
        'X' => {
            // Split: die and spawn 3 slimes
            monster.half_dead = false; // Allow death
            monster.hp = 0;
            // Spawn Acid Slime L (8 HP), Acid Slime M, Spike Slime M
            let mut acid_l = acid_slime_m::create("CAL");
            acid_l.hp = 8;
            acid_l.max_hp = 8;
            acid_l.name = "Acid Slime (L)".to_string();
            acid_l.monster_id = "acid_slime_l".to_string();
            result.spawn_monsters.push(acid_l);
            result.spawn_monsters.push(acid_slime_m::create("LCA"));
            result.spawn_monsters.push(spike_slime_m::create("V2D"));
        }
        _ => {}
    }
    result
}

/// Called when Slime Boss would die. Returns true if death is prevented (split pending).
pub fn on_would_die(monster: &mut Monster) -> bool {
    if !monster.half_dead {
        monster.half_dead = true;
        true // Prevent death
    } else {
        false // Allow death (split already happened)
    }
}
