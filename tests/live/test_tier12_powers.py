"""Tier 12: Power cards — uncommon and rare Ironclad powers.

Power cards apply a persistent effect and are removed from play (not discarded).
Each test verifies the card costs the correct energy and is properly removed.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both,
    assert_player_matches, assert_discard_matches,
)


# ── Uncommon Powers ──────────────────────────────────────────────────────

def test_combust_power(game):
    """CombustCard is a power card that costs 1 energy.

    After play: energy=2, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.CombustCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_dark_embrace_power(game):
    """DarkEmbrace is a power card that costs 2 energy.

    After play: energy=1, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.DarkEmbrace]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_evolve_power(game):
    """Evolve is a power card that costs 1 energy.

    After play: energy=2, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.Evolve]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_feel_no_pain_power(game):
    """FeelNoPain is a power card that costs 1 energy.

    After play: energy=2, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.FeelNoPain]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_fire_breathing_power(game):
    """FireBreathing is a power card that costs 1 energy.

    After play: energy=2, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.FireBreathing]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_rupture_power(game):
    """Rupture is a power card that costs 1 energy.

    After play: energy=2, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.Rupture]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Rare Powers ──────────────────────────────────────────────────────────

def test_barricade_power(game):
    """Barricade is a power card that costs 2 energy.

    After play: energy=1, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.Barricade]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_berserk_power(game):
    """BerserkCard is a power card that costs 1 energy.

    After play: energy=2, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.BerserkCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_corruption_power(game):
    """Corruption is a power card that costs 3 energy.

    After play: energy=0, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.Corruption]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_demon_form_power(game):
    """DemonForm is a power card that costs 3 energy.

    After play: energy=0, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.DemonForm]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_juggernaut_power(game):
    """Juggernaut is a power card that costs 2 energy.

    After play: energy=1, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.Juggernaut]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
