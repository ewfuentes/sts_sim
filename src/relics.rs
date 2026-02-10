use crate::creature::{Monster, Player};
use crate::damage::apply_damage_to_monster;
use crate::enums::{CardType, PowerType, Relic};

/// Called at start of combat (after pre-battle, before first draw).
pub fn on_combat_start(player: &mut Player) {
    if player.has_relic(Relic::Anchor) {
        player.add_block(2);
    }

    if player.has_relic(Relic::BloodVial) {
        player.heal(1);
    }

    if player.has_relic(Relic::FrozenCore) {
        player.apply_power(PowerType::Metallicize, 1);
    }

    if player.has_relic(Relic::MutagenicStrength) {
        player.apply_power(PowerType::Strength, 1);
        player.apply_power(PowerType::LoseStrength, 1);
    }
}

/// Called at start of player turn.
/// Returns extra cards to draw and extra energy.
pub fn on_turn_start(player: &mut Player, turn_number: i32) -> (i32, i32) {
    let mut extra_draw = 0;
    let mut extra_energy = 0;

    // Lantern: +1 energy first turn
    if turn_number == 1 && player.has_relic(Relic::Lantern) {
        extra_energy += 1;
    }

    // Bag of Preparation: draw 2 extra at battle start
    if turn_number == 1 && player.has_relic(Relic::BagOfPreparation) {
        extra_draw += 2;
    }

    (extra_draw, extra_energy)
}

/// Called at end of player turn.
pub fn on_turn_end(player: &mut Player) {
    // Orichalcum: +1 block if player has 0 block
    if player.has_relic(Relic::Orichalcum) && player.block == 0 {
        player.add_block(1);
    }

    // LoseStrength: reduce Strength at end of turn, then remove
    let lose_str = player.get_power(PowerType::LoseStrength);
    if lose_str > 0 {
        player.apply_power(PowerType::Strength, -lose_str);
        player.powers.remove(&PowerType::LoseStrength);
    }
}

/// Called when the die is rolled for monsters. Triggers die-controlled relics.
/// Returns (extra_draw, extra_energy) from relics.
pub fn on_die_roll(player: &mut Player, monsters: &mut [Monster], roll: u8) -> (i32, i32) {
    let mut extra_draw = 0;
    let mut extra_energy = 0;

    // Vajra: die roll 2 → +1 temporary Str
    if player.has_relic(Relic::Vajra) && roll == 2 {
        player.apply_power(PowerType::Strength, 1);
    }

    // Oddly Smooth Stone: die roll 4 → +2 block
    if player.has_relic(Relic::OddlySmoothStone) && roll == 4 {
        player.add_block(2);
    }

    // Pen Nib: die roll 5 → apply 1 Vulnerable to first alive monster
    if player.has_relic(Relic::PenNib) && roll == 5 {
        for m in monsters.iter_mut() {
            if !m.is_dead() {
                m.apply_power(PowerType::Vulnerable, 1);
                break;
            }
        }
    }

    // Horn Cleat: die roll 1 or 2 → +1 block
    if player.has_relic(Relic::HornCleat) && (roll == 1 || roll == 2) {
        player.add_block(1);
    }

    // Happy Flower: die roll 3 or 4 → +1 energy
    if player.has_relic(Relic::HappyFlower) && (roll == 3 || roll == 4) {
        extra_energy += 1;
    }

    // Captain's Wheel: die roll 3 → +3 block
    if player.has_relic(Relic::CaptainsWheel) && roll == 3 {
        player.add_block(3);
    }

    // Sundial: die roll 2 → +2 energy
    if player.has_relic(Relic::Sundial) && roll == 2 {
        extra_energy += 2;
    }

    // Tungsten Rod: die roll 5 → +3 block
    if player.has_relic(Relic::TungstenRod) && roll == 5 {
        player.add_block(3);
    }

    // Red Mask: die roll 5-6 → 1 Weak to first alive monster
    if player.has_relic(Relic::RedMask) && (roll == 5 || roll == 6) {
        for m in monsters.iter_mut() {
            if !m.is_dead() {
                m.apply_power(PowerType::Weak, 1);
                break;
            }
        }
    }

    // Necronomicon: die roll 1 → DoubleTap(1)
    if player.has_relic(Relic::Necronomicon) && roll == 1 {
        player.apply_power(PowerType::DoubleTap, 1);
    }

    // Ink Bottle: die roll 5-6 → draw 1
    if player.has_relic(Relic::InkBottle) && (roll == 5 || roll == 6) {
        extra_draw += 1;
    }

    // Pocketwatch: die roll 3 → draw 3
    if player.has_relic(Relic::Pocketwatch) && roll == 3 {
        extra_draw += 3;
    }

    // Gremlin Horn: die roll 4 → draw 1; die roll 5 → +1 energy
    if player.has_relic(Relic::GremlinHorn) {
        if roll == 4 {
            extra_draw += 1;
        }
        if roll == 5 {
            extra_energy += 1;
        }
    }

    // Stone Calendar: die roll 4 → 4 damage to first alive monster
    if player.has_relic(Relic::StoneCalendar) && roll == 4 {
        for m in monsters.iter_mut() {
            if !m.is_dead() {
                apply_damage_to_monster(m, 4);
                break;
            }
        }
    }

    // The Boot: die roll 4-6 → 1 damage to first alive monster
    if player.has_relic(Relic::TheBoot) && roll >= 4 {
        for m in monsters.iter_mut() {
            if !m.is_dead() {
                apply_damage_to_monster(m, 1);
                break;
            }
        }
    }

    // Duality: die roll 2 → +2 block; die roll 4 → 2 damage to first alive monster
    if player.has_relic(Relic::Duality) {
        if roll == 2 {
            player.add_block(2);
        }
        if roll == 4 {
            for m in monsters.iter_mut() {
                if !m.is_dead() {
                    apply_damage_to_monster(m, 2);
                    break;
                }
            }
        }
    }

    // Incense Burner: die roll 6 → Buffer(1)
    if player.has_relic(Relic::IncenseBurner) && roll == 6 {
        player.apply_power(PowerType::BufferPower, 1);
    }

    // Snecko Eye: die roll 1-2 → draw 2; 3-4 → +1 energy; 5-6 → Dazed (handled in combat.rs)
    if player.has_relic(Relic::SneckoEye) {
        if roll <= 2 {
            extra_draw += 2;
        } else if roll <= 4 {
            extra_energy += 1;
        }
        // roll 5-6: add Dazed to draw pile handled in combat.rs (needs draw pile access)
    }

    (extra_draw, extra_energy)
}

/// Called when a card is played. Triggers on-card-play relics.
pub fn on_card_play(player: &mut Player, card_type: CardType) {
    // Bird-Faced Urn: +1 block when playing a Power card
    if player.has_relic(Relic::BirdFacedUrn) && card_type == CardType::Power {
        player.add_block(1);
    }
}

/// Called when draw pile is reshuffled (discard→draw).
pub fn on_shuffle(player: &mut Player) {
    // Red Skull: +1 Str when deck is shuffled
    if player.has_relic(Relic::RedSkull) {
        player.apply_power(PowerType::Strength, 1);
    }
}

/// Called on combat victory.
pub fn on_victory(player: &mut Player) {
    // Burning Blood: heal 1 HP on victory
    if player.has_relic(Relic::BurningBlood) {
        player.heal(1);
    }

    // Black Blood: heal 2 HP on victory (replaces Burning Blood)
    if player.has_relic(Relic::BlackBlood) {
        player.heal(2);
    }

    // Meat on the Bone: heal to 4 HP if HP 1-3
    if player.has_relic(Relic::MeatOnTheBone) && player.hp >= 1 && player.hp <= 3 {
        let heal_amount = 4 - player.hp;
        player.heal(heal_amount);
    }
}

/// Called at start of each monster turn (for MercuryHourglass).
pub fn on_monster_turn_start(player: &Player, monsters: &mut [Monster]) {
    // Mercury Hourglass: deal 1 damage to all enemies at start of turn
    if player.has_relic(Relic::MercuryHourglass) {
        for m in monsters.iter_mut() {
            if !m.is_dead() {
                apply_damage_to_monster(m, 1);
            }
        }
    }
}
