"""Tier 5: Power/buff duration and stack consumption.

Tests verify that temporary powers (Flex strength), and per-attack
Vulnerable/Weak consumption match between live game and simulator.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
)


# ── Flex: temporary strength boosts next attack ──────────────────────────

def test_flex_strength_boosts_attack(game):
    """Flex grants Strength that boosts the next attack.

    Setup: Flex + Strike in hand, monster at 30 HP.
    Play Flex (gain 1 Str), then Strike (should deal base + 1 damage).
    """
    hand = [sts_sim.Card.Flex, sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play Flex first (no target)
    state = play_named_card(game, sim, setup, sts_sim.Card.Flex)

    # Now only Strike remains — play it at index 0
    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Vulnerable consumed per attack (monster) ─────────────────────────────

def test_vulnerable_consumed_per_attack(game):
    """Vulnerable is consumed 1 stack per attack card played.

    Setup: 2 Strikes in hand, monster has 2 Vulnerable, HP=30.
    After 1st Strike: Vulnerable=1, damage boosted.
    After 2nd Strike: Vulnerable=0, damage boosted.
    Both sim and live should agree on final monster HP.
    """
    hand = [sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed]

    set_scenario(
        game, hand=hand, energy=3, monster_hp=30,
        monster_powers={"Vulnerable": 2},
    )
    sim = make_sim(
        hand=hand, energy=3, monster_hp=30,
        monster_powers={"Vulnerable": 2},
    )

    # Play first Strike (both identical, index 0 is fine)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)

    # Play second Strike
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Weak consumed per attack (player) ───────────────────────────────────

def test_weak_consumed_per_attack(game):
    """Weak is consumed 1 stack per attack card played.

    Setup: 2 Strikes in hand, player has 2 Weak, monster HP=30.
    After 1st Strike: Weak=1, damage reduced.
    After 2nd Strike: Weak=0, damage reduced.
    Both sim and live should agree on final monster HP.
    """
    hand = [sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed]

    set_scenario(
        game, hand=hand, energy=3, monster_hp=30,
        player_powers={"Weak": 2},
    )
    sim = make_sim(
        hand=hand, energy=3, monster_hp=30,
        player_powers={"Weak": 2},
    )

    # Play first Strike
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)

    # Play second Strike
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Vulnerable + Weak cancel then deplete independently ──────────────────

def test_vulnerable_and_weak_cancel_then_deplete(game):
    """With both Weak and Vulnerable, they cancel damage-wise but both
    consume a stack per attack.

    Setup: 2 Strikes, player Weak=1, monster Vulnerable=1, HP=30.
    1st Strike: Weak+Vuln cancel (normal damage), both consumed.
    2nd Strike: no modifiers (normal damage again).
    """
    hand = [sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed]

    set_scenario(
        game, hand=hand, energy=3, monster_hp=30,
        player_powers={"Weak": 1},
        monster_powers={"Vulnerable": 1},
    )
    sim = make_sim(
        hand=hand, energy=3, monster_hp=30,
        player_powers={"Weak": 1},
        monster_powers={"Vulnerable": 1},
    )

    # 1st Strike: Weak + Vuln cancel
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)

    # 2nd Strike: no modifiers
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
