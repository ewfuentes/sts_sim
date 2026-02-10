use crate::enums::PowerType;

/// Calculate damage modifier from attacker's powers (atDamageGive step).
/// BG mod Weak: flat -1 damage per attack.
/// If both Weak and Vulnerable are present, they cancel out (no modification).
pub fn at_damage_give(
    attacker_weak: i32,
    target_vulnerable: i32,
    damage: f32,
) -> f32 {
    if attacker_weak > 0 {
        if target_vulnerable > 0 {
            // Weak + Vulnerable cancel: no damage modification
            damage
        } else {
            damage - 1.0
        }
    } else {
        damage
    }
}

/// Calculate damage modifier from target's powers (atDamageReceive step).
/// BG mod Vulnerable: double damage for the next incoming hit.
/// If both Weak and Vulnerable are present, they cancel out (no modification).
pub fn at_damage_receive(
    attacker_weak: i32,
    target_vulnerable: i32,
    damage: f32,
) -> f32 {
    if target_vulnerable > 0 {
        if attacker_weak > 0 {
            // Weak + Vulnerable cancel: no damage modification
            damage
        } else {
            damage * 2.0
        }
    } else {
        damage
    }
}

/// Get the power cap for a given power type.
pub fn power_cap(power: PowerType) -> i32 {
    match power {
        PowerType::Vulnerable => 3,
        PowerType::Weak => 3,
        _ => 999,
    }
}
