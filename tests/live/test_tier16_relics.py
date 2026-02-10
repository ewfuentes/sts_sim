"""Tier 16: New relic infrastructure — die-roll, combat-start, and on-card-play relics.

Tests verify:
(a) new relics are correctly set on both game and sim
(b) card play still works correctly with new relic configs
(c) the sim's relic state matches the game
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both,
    assert_monsters_match, assert_player_matches, assert_relics_match,
)


# ── Die-Roll Relics ──────────────────────────────────────────────────────

def test_card_play_with_captains_wheel(game):
    """Card play works with CaptainsWheel present."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.CaptainsWheel]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_card_play_with_sundial(game):
    """Card play works with Sundial present."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.Sundial]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_card_play_with_tungsten_rod(game):
    """Card play works with TungstenRod present."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.TungstenRod]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_card_play_with_red_mask(game):
    """Card play works with RedMask present."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.RedMask]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_card_play_with_necronomicon(game):
    """Card play works with Necronomicon present."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.Necronomicon]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_card_play_with_ink_bottle(game):
    """Card play works with InkBottle present."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.InkBottle]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_card_play_with_stone_calendar(game):
    """Card play works with StoneCalendar present."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.StoneCalendar]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Combat-Start Relics ──────────────────────────────────────────────────

def test_card_play_with_blood_vial(game):
    """Card play works with BloodVial present."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.BloodVial]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_card_play_with_frozen_core(game):
    """Card play works with FrozenCore present."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.FrozenCore]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── All New Relics Together ──────────────────────────────────────────────

def test_card_play_with_all_new(game):
    """All 17 new relics at once — card play still works."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [
        sts_sim.Relic.CaptainsWheel,
        sts_sim.Relic.Sundial,
        sts_sim.Relic.TungstenRod,
        sts_sim.Relic.RedMask,
        sts_sim.Relic.Necronomicon,
        sts_sim.Relic.InkBottle,
        sts_sim.Relic.Pocketwatch,
        sts_sim.Relic.GremlinHorn,
        sts_sim.Relic.StoneCalendar,
        sts_sim.Relic.TheBoot,
        sts_sim.Relic.Duality,
        sts_sim.Relic.BloodVial,
        sts_sim.Relic.FrozenCore,
        sts_sim.Relic.MutagenicStrength,
        sts_sim.Relic.IncenseBurner,
        sts_sim.Relic.SneckoEye,
        sts_sim.Relic.BirdFacedUrn,
    ]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
