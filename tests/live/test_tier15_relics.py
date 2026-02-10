"""Tier 15: Relic infrastructure and card play with various relic configs.

Tests verify:
(a) relics are correctly set on both game and sim
(b) card play still works correctly with various relic configs
(c) the sim's relic state matches the game
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both,
    assert_monsters_match, assert_player_matches, assert_relics_match,
)


# ── Relic Infrastructure Tests ─────────────────────────────────────────────

def test_set_burning_blood_only(game):
    """Default relic (BurningBlood) appears in both game and sim."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.BurningBlood]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)


def test_set_empty_relics(game):
    """Clearing all relics works, card play still functions."""
    hand = [sts_sim.Card.StrikeRed]
    relics = []

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_set_multiple_relics(game):
    """Multiple relics appear in both game and sim."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.BurningBlood, sts_sim.Relic.Anchor,
              sts_sim.Relic.Lantern]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)


# ── Card Play With Relics ──────────────────────────────────────────────────

def test_card_play_with_anchor(game):
    """Card play works with Anchor present."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.Anchor]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_relics_match(state, sim)


def test_card_play_with_orichalcum(game):
    """Card play works with Orichalcum present."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.Orichalcum]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_relics_match(state, sim)


def test_card_play_with_lantern(game):
    """Card play works with Lantern present."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.Lantern]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_relics_match(state, sim)


def test_card_play_with_vajra(game):
    """Die-roll relic present (die=1, safe)."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.Vajra]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_relics_match(state, sim)


def test_card_play_with_all_common(game):
    """All common relics at once."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [
        sts_sim.Relic.BurningBlood,
        sts_sim.Relic.Anchor,
        sts_sim.Relic.Lantern,
        sts_sim.Relic.Orichalcum,
        sts_sim.Relic.Vajra,
        sts_sim.Relic.OddlySmoothStone,
        sts_sim.Relic.PenNib,
        sts_sim.Relic.HornCleat,
        sts_sim.Relic.HappyFlower,
        sts_sim.Relic.RedSkull,
        sts_sim.Relic.MeatOnTheBone,
    ]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_relics_match(state, sim)


# ── Relic Replacement ──────────────────────────────────────────────────────

def test_replace_relics_between_scenarios(game):
    """Relic list fully replaced between scenarios."""
    hand = [sts_sim.Card.StrikeRed]

    # First scenario: Anchor only
    state1 = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                          player_relics=[sts_sim.Relic.Anchor])
    sim1 = make_sim(hand=hand, energy=3, monster_hp=30,
                    player_relics=[sts_sim.Relic.Anchor])
    assert_relics_match(state1, sim1)

    # Second scenario: Lantern only (Anchor should be gone)
    state2 = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                          player_relics=[sts_sim.Relic.Lantern])
    sim2 = make_sim(hand=hand, energy=3, monster_hp=30,
                    player_relics=[sts_sim.Relic.Lantern])
    assert_relics_match(state2, sim2)


def test_black_blood_replaces_burning_blood(game):
    """Boss relic swap works — BlackBlood without BurningBlood."""
    hand = [sts_sim.Card.StrikeRed]
    relics = [sts_sim.Relic.BlackBlood]

    state = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_relics=relics)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, player_relics=relics)

    assert_relics_match(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_relics_match(state, sim)
