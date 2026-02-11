"""Live tests for Defect Rare cards.

Tests verify that Defect rare cards produce matching state between
the live BG mod game and the Rust simulator. Uses set_scenario to
configure exact game state before each test.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
    CARD_TO_BG,
)


# ===================================================================
# ALL FOR ONE
# ===================================================================

def test_all_for_one_retrieves_zero_cost(game):
    """All for One deals damage and retrieves 0-cost cards from discard."""
    hand = [sts_sim.Card.AllForOne]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         discard_pile=[sts_sim.Card.Zap, sts_sim.Card.FTL,
                                       sts_sim.Card.StrikeBlue])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   discard_pile=[sts_sim.Card.Zap, sts_sim.Card.FTL,
                                 sts_sim.Card.StrikeBlue])
    state = play_named_card(game, sim, setup, sts_sim.Card.AllForOne,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


def test_all_for_one_upgraded(game):
    """Upgraded All for One deals 3 damage."""
    hand = [(sts_sim.Card.AllForOne, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         discard_pile=[sts_sim.Card.Zap])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   discard_pile=[sts_sim.Card.Zap])
    state = play_named_card(game, sim, setup, sts_sim.Card.AllForOne,
                            target_index=0, upgraded=True)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


# ===================================================================
# CORE SURGE
# ===================================================================

def test_core_surge_base(game):
    """Core Surge removes debuffs and deals damage."""
    hand = [sts_sim.Card.CoreSurge]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_powers={"Weak": 2, "Vulnerable": 1})
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   player_powers={"Weak": 2, "Vulnerable": 1})
    state = play_named_card(game, sim, setup, sts_sim.Card.CoreSurge,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# HYPERBEAM
# ===================================================================

def test_hyperbeam_base(game):
    """Hyperbeam deals AOE 5 and removes orbs."""
    hand = [sts_sim.Card.Hyperbeam]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         orbs=["Lightning", "Frost"])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   orbs=["Lightning", "Frost"])
    state = play_named_card(game, sim, setup, sts_sim.Card.Hyperbeam)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_hyperbeam_no_orbs(game):
    """Hyperbeam with no orbs still deals damage."""
    hand = [sts_sim.Card.Hyperbeam]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.Hyperbeam)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_hyperbeam_upgraded(game):
    """Upgraded Hyperbeam deals AOE 7."""
    hand = [(sts_sim.Card.Hyperbeam, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         orbs=["Frost", "Frost", "Dark"])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   orbs=["Frost", "Frost", "Dark"])
    state = play_named_card(game, sim, setup, sts_sim.Card.Hyperbeam,
                            upgraded=True)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# THUNDER STRIKE
# ===================================================================

def test_thunder_strike_with_lightning(game):
    """Thunder Strike with 2 Lightning orbs deals AOE damage."""
    hand = [sts_sim.Card.ThunderStrike]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         orbs=["Lightning", "Lightning", "Frost"])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   orbs=["Lightning", "Lightning", "Frost"])
    state = play_named_card(game, sim, setup, sts_sim.Card.ThunderStrike)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_thunder_strike_no_lightning(game):
    """Thunder Strike with no Lightning orbs deals 0."""
    hand = [sts_sim.Card.ThunderStrike]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         orbs=["Frost", "Frost"])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   orbs=["Frost", "Frost"])
    state = play_named_card(game, sim, setup, sts_sim.Card.ThunderStrike)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# FISSION
# ===================================================================

def test_fission_with_orbs(game):
    """Fission removes orbs, gains energy, draws, exhausts."""
    hand = [sts_sim.Card.Fission]
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30,
                         orbs=["Lightning", "Frost", "Dark"])
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30,
                   orbs=["Lightning", "Frost", "Dark"])
    state = play_named_card(game, sim, setup, sts_sim.Card.Fission)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_fission_no_orbs(game):
    """Fission with no orbs just exhausts."""
    hand = [sts_sim.Card.Fission]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.Fission)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ===================================================================
# RAINBOW
# ===================================================================

def test_rainbow_channels_3_orbs(game):
    """Rainbow channels Lightning, Frost, Dark and exhausts."""
    hand = [sts_sim.Card.RainbowCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.RainbowCard)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_rainbow_upgraded_no_exhaust(game):
    """Upgraded Rainbow does not exhaust."""
    hand = [(sts_sim.Card.RainbowCard, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.RainbowCard,
                            upgraded=True)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===================================================================
# SKIM
# ===================================================================

def test_skim_base(game):
    """Skim draws 3 cards."""
    hand = [sts_sim.Card.SkimCard]
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.SkimCard)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_skim_upgraded(game):
    """Upgraded Skim draws 4 cards."""
    hand = [(sts_sim.Card.SkimCard, True)]
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue,
            sts_sim.Card.DefendBlue, sts_sim.Card.Zap]
    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.SkimCard,
                            upgraded=True)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


# ===================================================================
# ELECTRODYNAMICS
# ===================================================================

def test_electrodynamics_channels_2(game):
    """Electrodynamics channels 2 Lightning on play."""
    hand = [sts_sim.Card.ElectrodynamicsCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup,
                            sts_sim.Card.ElectrodynamicsCard)
    assert_player_matches(state, sim)


def test_electrodynamics_upgraded(game):
    """Upgraded Electrodynamics channels 3 Lightning."""
    hand = [(sts_sim.Card.ElectrodynamicsCard, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup,
                            sts_sim.Card.ElectrodynamicsCard, upgraded=True)
    assert_player_matches(state, sim)


# ===================================================================
# DEFRAGMENT
# ===================================================================

def test_defragment_base(game):
    """Defragment enters play, costs 1."""
    hand = [sts_sim.Card.DefragmentCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.DefragmentCard)
    assert_player_matches(state, sim)


# ===================================================================
# STATIC DISCHARGE
# ===================================================================

def test_static_discharge_base(game):
    """Static Discharge enters play, costs 1."""
    hand = [sts_sim.Card.StaticDischargeCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup,
                            sts_sim.Card.StaticDischargeCard)
    assert_player_matches(state, sim)


# ===================================================================
# BUFFER
# ===================================================================

def test_buffer_base(game):
    """Buffer enters play, costs 2."""
    hand = [sts_sim.Card.BufferCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.BufferCard)
    assert_player_matches(state, sim)


# ===================================================================
# ECHO FORM
# ===================================================================

def test_echo_form_base(game):
    """Echo Form enters play, costs 3."""
    hand = [sts_sim.Card.EchoFormCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.EchoFormCard)
    assert_player_matches(state, sim)


# ===================================================================
# AMPLIFY
# ===================================================================

def test_amplify_base(game):
    """Amplify enters play, costs 1."""
    hand = [sts_sim.Card.AmplifyCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.AmplifyCard)
    assert_player_matches(state, sim)
