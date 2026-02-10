use crate::creature::{Monster, Player};
use crate::enums::{PowerType, Stance};
use crate::powers;

/// Full damage pipeline for monster attacking player.
/// Pipeline: base + Strength → atDamageGive (Weak) → atDamageReceive (Vulnerable) → floor, min 0
pub fn calculate_monster_damage(attacker: &Monster, target: &Player, base_damage: i32) -> i32 {
    let strength = attacker.get_power(PowerType::Strength);
    let mut damage = (base_damage + strength) as f32;

    let attacker_weak = attacker.get_power(PowerType::Weak);
    let target_vuln = target.get_power(PowerType::Vulnerable);

    // atDamageGive — Weak
    damage = powers::at_damage_give(attacker_weak, target_vuln, damage);

    // atDamageReceive — Vulnerable
    damage = powers::at_damage_receive(attacker_weak, target_vuln, damage);

    // Floor and clamp
    let result = damage.floor() as i32;
    result.max(0)
}

/// Full damage pipeline for player attacking monster.
/// Pipeline: base + Strength + Wrath → atDamageGive (Weak) → atDamageReceive (Vulnerable) → floor, min 0
pub fn calculate_player_damage(attacker: &Player, target: &Monster, base_damage: i32) -> i32 {
    let strength = attacker.get_power(PowerType::Strength);
    let mut wrath_bonus = 0;
    if attacker.stance == Stance::Wrath {
        wrath_bonus = 1 + attacker.get_power(PowerType::SimmeringFury);
    }
    let mut damage = (base_damage + strength + wrath_bonus) as f32;

    let attacker_weak = attacker.get_power(PowerType::Weak);
    let target_vuln = target.get_power(PowerType::Vulnerable);

    // atDamageGive — Weak
    damage = powers::at_damage_give(attacker_weak, target_vuln, damage);

    // atDamageReceive — Vulnerable
    damage = powers::at_damage_receive(attacker_weak, target_vuln, damage);

    // Floor and clamp
    let result = damage.floor() as i32;
    result.max(0)
}

/// Apply damage to player, accounting for block. Returns actual HP lost.
pub fn apply_damage_to_player(player: &mut Player, damage: i32) -> i32 {
    if damage <= 0 {
        return 0;
    }
    let blocked = damage.min(player.block);
    player.block -= blocked;
    let hp_damage = damage - blocked;
    player.hp -= hp_damage;
    hp_damage
}

/// Apply damage to monster, accounting for block and Curl Up.
/// Returns actual HP lost.
pub fn apply_damage_to_monster(monster: &mut Monster, damage: i32) -> i32 {
    if damage <= 0 {
        return 0;
    }

    // Curl Up check: triggers on non-lethal damage before block
    let curl_up = monster.get_power(PowerType::CurlUp);
    if curl_up > 0 {
        // Check if damage after block would be non-lethal
        let blocked = damage.min(monster.block);
        let hp_damage = damage - blocked;
        if hp_damage > 0 && hp_damage < monster.hp {
            // Curl Up triggers: grant 2 block, then remove
            monster.add_block(2);
            monster.powers.remove(&PowerType::CurlUp);
        }
    }

    let blocked = damage.min(monster.block);
    monster.block -= blocked;
    let hp_damage = damage - blocked;
    monster.hp -= hp_damage;

    // Slime Boss: when HP reaches 0, enter half_dead state (split pending)
    if monster.hp <= 0 && monster.monster_id == "slime_boss" && !monster.half_dead {
        monster.half_dead = true;
    }

    hp_damage
}
