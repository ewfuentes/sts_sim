"""Tier 1: Fundamental mechanics — Strike, Defend, energy, Bash.

Each test:
1. Uses the set command to configure a precise game state
2. Plays a card in both the live game and the simulator
3. Asserts that monster HP, player block, and energy match
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both,
    assert_monsters_match, assert_player_matches,
)


# ── Test 1: Strike deals expected damage ──────────────────────────────────

def test_strike_damage(game):
    """Play Strike on a Jaw Worm. Verify monster HP drops by base_damage."""
    hand = [sts_sim.Card.StrikeRed]

    set_scenario(game, hand=hand, energy=3, monster_hp=8)
    sim = make_sim(hand=hand, energy=3, monster_hp=8)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Test 2: Defend grants expected block ──────────────────────────────────

def test_defend_block(game):
    """Play Defend. Verify player gains block and energy is deducted."""
    hand = [sts_sim.Card.DefendRed]

    set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=8)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=8)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)


# ── Test 3: Energy is deducted correctly ──────────────────────────────────

def test_energy_deduction(game):
    """Play a 1-cost card with 3 energy. Verify 2 energy remains."""
    hand = [sts_sim.Card.StrikeRed]

    set_scenario(game, hand=hand, energy=3, monster_hp=8)
    sim = make_sim(hand=hand, energy=3, monster_hp=8)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    live_energy = state.combat_state.player.energy
    sim_energy = sim.player.energy
    assert live_energy == sim_energy, (
        f"Energy mismatch: live={live_energy}, sim={sim_energy}"
    )
    # Also check the actual value as sanity
    assert live_energy == 2, f"Expected 2 energy after 1-cost card, got {live_energy}"


# ── Test 4: Bash deals damage and applies Vulnerable ─────────────────────

def test_bash_damage_and_vulnerable(game):
    """Play Bash. Verify damage dealt AND Vulnerable applied to monster."""
    hand = [sts_sim.Card.Bash]

    set_scenario(game, hand=hand, energy=3, monster_hp=8)
    sim = make_sim(hand=hand, energy=3, monster_hp=8)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    # Verify damage
    assert_monsters_match(state, sim)

    # Verify energy (Bash costs 2)
    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 1, (
        f"Expected 1 energy after Bash (cost 2), got {state.combat_state.player.energy}"
    )

    # Verify Vulnerable was applied
    live_monster = state.combat_state.monsters[0]
    sim_monster = sim.get_monsters()[0]

    # Find Vulnerable power on live monster
    live_vuln = None
    for p in live_monster.powers:
        if "ulnerable" in p.power_id:  # Match "Vulnerable" or "BGVulnerable"
            live_vuln = p.amount
            break

    sim_vuln = sim_monster.get_power(sts_sim.PowerType.Vulnerable)

    assert live_vuln is not None, "Vulnerable not found on live monster"
    assert live_vuln == sim_vuln, (
        f"Vulnerable mismatch: live={live_vuln}, sim={sim_vuln}"
    )
