"""Live tests for Defect Basic cards.

Each test uses set_scenario to configure exact game state, then plays a card
in both the live game and simulator, asserting that state matches afterward.
"""
import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both,
    assert_monsters_match, assert_player_matches,
    assert_discard_matches,
)


# ===================================================================
# Strike (Blue) — Attack, Cost 1, 1 HIT. Upgrade: Cost 0.
# ===================================================================


def test_strike_blue_base_damage(game):
    """Basic Strike deals 1 damage."""
    hand = [sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_strike_blue_with_strength(game):
    """Strike benefits from Strength."""
    hand = [sts_sim.Card.StrikeBlue]
    powers = {"Strength": 2}

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         player_powers=powers)
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   player_powers=powers)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_strike_blue_upgraded_costs_0(game):
    """Upgraded Strike costs 0."""
    hand = [(sts_sim.Card.StrikeBlue, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)

    state = play_card_both(game, sim, 0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# Defend (Blue) — Skill, Cost 1, 1 BLK. Upgrade: 2 BLK to any player.
# ===================================================================


def test_defend_blue_base_block(game):
    """Basic Defend grants 1 block."""
    hand = [sts_sim.Card.DefendBlue]

    setup = set_scenario(game, hand=hand, energy=3, player_block=0)
    sim = make_sim(hand=hand, energy=3, player_block=0)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_defend_blue_stacks_with_existing_block(game):
    """Defend block stacks with existing block."""
    hand = [sts_sim.Card.DefendBlue]

    setup = set_scenario(game, hand=hand, energy=3, player_block=3)
    sim = make_sim(hand=hand, energy=3, player_block=3)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)


# ===================================================================
# Zap — Skill, Cost 1, Channel 1 Lightning. Upgrade: Cost 0.
# ===================================================================


def test_zap_channels_lightning(game):
    """Zap channels a Lightning orb."""
    hand = [sts_sim.Card.Zap]

    setup = set_scenario(game, hand=hand, energy=3)
    sim = make_sim(hand=hand, energy=3)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_zap_evokes_oldest_when_full(game):
    """Zap evokes oldest orb when orb slots are full."""
    hand = [sts_sim.Card.Zap]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         orbs=["Frost", "Frost", "Frost"])
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   orbs=["Frost", "Frost", "Frost"])

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)


def test_zap_upgraded_costs_0(game):
    """Upgraded Zap costs 0."""
    hand = [(sts_sim.Card.Zap, True)]

    setup = set_scenario(game, hand=hand, energy=3)
    sim = make_sim(hand=hand, energy=3)

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)


# ===================================================================
# Dualcast — Skill, Cost 1, Evoke an Orb twice. Upgrade: Cost 0.
# ===================================================================


def test_dualcast_evokes_lightning_twice(game):
    """Dualcast evokes Lightning orb twice for double damage."""
    hand = [sts_sim.Card.Dualcast]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         orbs=["Lightning"])
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   orbs=["Lightning"])

    state = play_card_both(game, sim, 0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_dualcast_evokes_frost_twice(game):
    """Dualcast evokes Frost orb twice for double block."""
    hand = [sts_sim.Card.Dualcast]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         player_block=0, orbs=["Frost"])
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   player_block=0, orbs=["Frost"])

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)


def test_dualcast_upgraded_costs_0(game):
    """Upgraded Dualcast costs 0."""
    hand = [(sts_sim.Card.Dualcast, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         orbs=["Dark"])
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   orbs=["Dark"])

    state = play_card_both(game, sim, 0)

    assert_player_matches(state, sim)


def test_dualcast_no_orbs(game):
    """Dualcast with no orbs does nothing."""
    hand = [sts_sim.Card.Dualcast]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)

    state = play_card_both(game, sim, 0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
