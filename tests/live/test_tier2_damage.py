"""Tier 2: Damage pipeline — Vulnerable, Weak, Strength, Block absorption.

Tests verify that damage modifiers in the live game match the simulator.
Each test uses the set command to pre-configure powers, then plays a card
and compares results.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both,
    assert_monsters_match, assert_player_matches,
)


# ── Test 5: Vulnerable increases damage taken ─────────────────────────────

def test_vulnerable_increases_damage(game):
    """Strike a Vulnerable monster. Verify damage is boosted.

    In the board game mod, Vulnerable adds +50% damage (rounded down)
    for the die-based system. The simulator should match whatever the
    game produces.
    """
    hand = [sts_sim.Card.StrikeRed]

    # Set up: monster already has Vulnerable
    set_scenario(
        game, hand=hand, energy=3, monster_hp=8,
        monster_powers={"Vulnerable": 1},
    )
    sim = make_sim(
        hand=hand, energy=3, monster_hp=8,
        monster_powers={"Vulnerable": 1},
    )

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Test 6: Weak reduces outgoing damage ──────────────────────────────────

def test_weak_reduces_damage(game):
    """Strike while Weak. Verify damage is reduced."""
    hand = [sts_sim.Card.StrikeRed]

    set_scenario(
        game, hand=hand, energy=3, monster_hp=8,
        player_powers={"Weak": 1},
    )
    sim = make_sim(
        hand=hand, energy=3, monster_hp=8,
        player_powers={"Weak": 1},
    )

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Test 7: Strength adds damage ──────────────────────────────────────────

def test_strength_adds_damage(game):
    """Strike with 2 Strength. Verify extra damage."""
    hand = [sts_sim.Card.StrikeRed]

    set_scenario(
        game, hand=hand, energy=3, monster_hp=8,
        player_powers={"Strength": 2},
    )
    sim = make_sim(
        hand=hand, energy=3, monster_hp=8,
        player_powers={"Strength": 2},
    )

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Test 8: Block absorbs damage before HP ────────────────────────────────

def test_block_absorbs_damage(game):
    """Strike a monster that has block. Verify block absorbs damage first."""
    hand = [sts_sim.Card.StrikeRed]

    set_scenario(
        game, hand=hand, energy=3,
        monster_hp=8, monster_block=5,
    )
    sim = make_sim(
        hand=hand, energy=3,
        monster_hp=8, monster_block=5,
    )

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)

    # Sanity: block should have absorbed the damage, HP unchanged
    live_monster = state.combat_state.monsters[0]
    assert live_monster.current_hp == 8, (
        f"Monster HP should be 8 (block absorbed), got {live_monster.current_hp}"
    )


# ── Test: Iron Wave — both damage and block ───────────────────────────────

def test_iron_wave_damage_and_block(game):
    """Iron Wave deals damage AND gains block. Verify both."""
    hand = [sts_sim.Card.IronWave]

    set_scenario(
        game, hand=hand, energy=3,
        player_block=0, monster_hp=8,
    )
    sim = make_sim(
        hand=hand, energy=3,
        player_block=0, monster_hp=8,
    )

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)

    # Sanity: player should have gained block
    assert state.combat_state.player.block > 0, "Player should have gained block from Iron Wave"


# ── Test: Twin Strike — two hits ──────────────────────────────────────────

def test_twin_strike_two_hits(game):
    """Twin Strike hits twice. Verify total damage matches simulator."""
    hand = [sts_sim.Card.TwinStrike]

    set_scenario(
        game, hand=hand, energy=3, monster_hp=8,
    )
    sim = make_sim(
        hand=hand, energy=3, monster_hp=8,
    )

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Test: Heavy Blade with Strength ───────────────────────────────────────

def test_heavy_blade_strength_scaling(game):
    """Heavy Blade multiplies Strength bonus. Verify with 2 Strength."""
    hand = [sts_sim.Card.HeavyBlade]

    # Use high HP so the monster survives Heavy Blade's big hit
    set_scenario(
        game, hand=hand, energy=3, monster_hp=30,
        player_powers={"Strength": 2},
    )
    sim = make_sim(
        hand=hand, energy=3, monster_hp=30,
        player_powers={"Strength": 2},
    )

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Test: Strength + Vulnerable combined ──────────────────────────────────

def test_strength_and_vulnerable_combined(game):
    """Strike with Strength on a Vulnerable monster. Verify combined bonus."""
    hand = [sts_sim.Card.StrikeRed]

    set_scenario(
        game, hand=hand, energy=3, monster_hp=8,
        player_powers={"Strength": 2},
        monster_powers={"Vulnerable": 1},
    )
    sim = make_sim(
        hand=hand, energy=3, monster_hp=8,
        player_powers={"Strength": 2},
        monster_powers={"Vulnerable": 1},
    )

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
