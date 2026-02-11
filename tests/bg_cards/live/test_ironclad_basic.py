"""Live tests for Ironclad Basic cards."""
import sts_sim
from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_discard_matches, assert_exhaust_matches,
)


# =========================================================================
# Strike
# =========================================================================

def test_strike_base_damage(game):
    """Base Strike deals 1 damage."""
    hand = [sts_sim.Card.StrikeRed]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_strike_with_strength(game):
    """Strike with 2 STR deals 3 damage."""
    hand = [sts_sim.Card.StrikeRed]
    set_scenario(game, hand=hand, energy=3, monster_hp=20,
                 player_powers={"Strength": 2})
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   player_powers={"Strength": 2})
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_strike_upgraded(game):
    """Upgraded Strike deals 2 damage."""
    hand = [(sts_sim.Card.StrikeRed, True)]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# =========================================================================
# Defend
# =========================================================================

def test_defend_base_block(game):
    """Base Defend grants 1 block."""
    hand = [sts_sim.Card.DefendRed]
    set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_defend_upgraded_block(game):
    """Upgraded Defend grants 2 block to any player."""
    hand = [(sts_sim.Card.DefendRed, True)]
    set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# =========================================================================
# Bash
# =========================================================================

def test_bash_base_damage_and_vulnerable(game):
    """Base Bash deals 2 damage and applies Vulnerable."""
    hand = [sts_sim.Card.Bash]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_bash_upgraded_damage_and_vulnerable(game):
    """Upgraded Bash deals 4 damage and applies Vulnerable."""
    hand = [(sts_sim.Card.Bash, True)]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_bash_with_strength(game):
    """Bash with 1 STR scales per HIT: 4 damage total."""
    hand = [sts_sim.Card.Bash]
    set_scenario(game, hand=hand, energy=3, monster_hp=20,
                 player_powers={"Strength": 1})
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   player_powers={"Strength": 1})
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
