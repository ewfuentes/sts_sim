"""Live tests for Defect Uncommon cards.

Tests verify that Defect uncommon cards produce matching state between
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
# BLIZZARD
# ===================================================================

def test_blizzard_base(game):
    """Blizzard deals AOE 2 per Frost orb (2 Frost = 4 damage each)."""
    hand = [sts_sim.Card.Blizzard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         orbs=["Frost", "Frost"])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   orbs=["Frost", "Frost"])
    state = play_named_card(game, sim, setup, sts_sim.Card.Blizzard)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_blizzard_no_frost(game):
    """Blizzard with no Frost orbs deals 0 damage."""
    hand = [sts_sim.Card.Blizzard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         orbs=["Lightning"])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   orbs=["Lightning"])
    state = play_named_card(game, sim, setup, sts_sim.Card.Blizzard)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_blizzard_upgraded(game):
    """Upgraded Blizzard deals AOE 3 per Frost orb."""
    hand = [(sts_sim.Card.Blizzard, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         orbs=["Frost", "Frost", "Frost"])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   orbs=["Frost", "Frost", "Frost"])
    state = play_named_card(game, sim, setup, sts_sim.Card.Blizzard,
                            upgraded=True)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# COLD SNAP
# ===================================================================

def test_cold_snap_base(game):
    """Cold Snap deals 2 damage and channels Frost."""
    hand = [sts_sim.Card.ColdSnap]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.ColdSnap,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_cold_snap_upgraded(game):
    """Upgraded Cold Snap deals 3 damage."""
    hand = [(sts_sim.Card.ColdSnap, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.ColdSnap,
                            target_index=0, upgraded=True)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# DOOM AND GLOOM
# ===================================================================

def test_doom_and_gloom_base(game):
    """Doom and Gloom deals AOE 2 and channels Dark."""
    hand = [sts_sim.Card.DoomAndGloom]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.DoomAndGloom)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_doom_and_gloom_upgraded(game):
    """Upgraded Doom and Gloom deals AOE 3."""
    hand = [(sts_sim.Card.DoomAndGloom, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.DoomAndGloom,
                            upgraded=True)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# FTL
# ===================================================================

def test_ftl_first_card(game):
    """FTL as first card deals 1 damage and draws 1."""
    hand = [sts_sim.Card.FTL]
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.FTL,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


def test_ftl_upgraded(game):
    """Upgraded FTL deals 2 damage."""
    hand = [(sts_sim.Card.FTL, True)]
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.FTL,
                            target_index=0, upgraded=True)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# MELTER
# ===================================================================

def test_melter_removes_block(game):
    """Melter removes block then deals 2 damage."""
    hand = [sts_sim.Card.MelterCard]
    setup = set_scenario(game, hand=hand, energy=3,
                         monster_hp=30, monster_block=10)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, monster_block=10)
    state = play_named_card(game, sim, setup, sts_sim.Card.MelterCard,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_melter_no_block(game):
    """Melter on enemy with no block just deals damage."""
    hand = [sts_sim.Card.MelterCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.MelterCard,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_melter_upgraded(game):
    """Upgraded Melter removes block and deals 3 damage."""
    hand = [(sts_sim.Card.MelterCard, True)]
    setup = set_scenario(game, hand=hand, energy=3,
                         monster_hp=30, monster_block=15)
    sim = make_sim(hand=hand, energy=3, monster_hp=30, monster_block=15)
    state = play_named_card(game, sim, setup, sts_sim.Card.MelterCard,
                            target_index=0, upgraded=True)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# SCRAPE
# ===================================================================

def test_scrape_zero_cost_top(game):
    """Scrape returns 0-cost card from top of discard."""
    hand = [sts_sim.Card.Scrape]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         discard_pile=[sts_sim.Card.Zap])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   discard_pile=[sts_sim.Card.Zap])
    state = play_named_card(game, sim, setup, sts_sim.Card.Scrape,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


def test_scrape_empty_discard(game):
    """Scrape with empty discard just deals damage."""
    hand = [sts_sim.Card.Scrape]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.Scrape,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# STREAMLINE
# ===================================================================

def test_streamline_no_powers(game):
    """Streamline costs 2 with no powers, deals 3 damage."""
    hand = [sts_sim.Card.Streamline]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.Streamline,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_streamline_upgraded(game):
    """Upgraded Streamline deals 4 damage."""
    hand = [(sts_sim.Card.Streamline, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.Streamline,
                            target_index=0, upgraded=True)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# SUNDER
# ===================================================================

def test_sunder_no_kill(game):
    """Sunder on high-HP enemy does not refund energy."""
    hand = [sts_sim.Card.Sunder]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.Sunder,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# DARKNESS
# ===================================================================

def test_darkness_base(game):
    """Darkness channels Dark orb, costs 1."""
    hand = [sts_sim.Card.DarknessCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.DarknessCard)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_darkness_upgraded(game):
    """Upgraded Darkness costs 0."""
    hand = [(sts_sim.Card.DarknessCard, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.DarknessCard,
                            upgraded=True)
    assert_player_matches(state, sim)


# ===================================================================
# DOUBLE ENERGY
# ===================================================================

def test_double_energy_base(game):
    """Double Energy doubles energy and exhausts."""
    hand = [sts_sim.Card.DoubleEnergy]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.DoubleEnergy)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_double_energy_upgraded(game):
    """Upgraded Double Energy costs 0."""
    hand = [(sts_sim.Card.DoubleEnergy, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.DoubleEnergy,
                            upgraded=True)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ===================================================================
# EQUILIBRIUM
# ===================================================================

def test_equilibrium_block(game):
    """Equilibrium grants 3 block."""
    hand = [sts_sim.Card.Equilibrium]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.Equilibrium)
    assert_player_matches(state, sim)


def test_equilibrium_upgraded_block(game):
    """Upgraded Equilibrium grants 4 block."""
    hand = [(sts_sim.Card.Equilibrium, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.Equilibrium,
                            upgraded=True)
    assert_player_matches(state, sim)


# ===================================================================
# GLACIER
# ===================================================================

def test_glacier_base(game):
    """Glacier grants 2 block and channels Frost."""
    hand = [sts_sim.Card.Glacier]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.Glacier)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===================================================================
# HOLOGRAM
# ===================================================================

def test_hologram_retrieves_and_exhausts(game):
    """Hologram retrieves card from discard and exhausts."""
    hand = [sts_sim.Card.Hologram]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         discard_pile=[sts_sim.Card.BallLightning])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   discard_pile=[sts_sim.Card.BallLightning])
    state = play_named_card(game, sim, setup, sts_sim.Card.Hologram,
                            choices=[0])
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_hologram_upgraded_no_exhaust(game):
    """Upgraded Hologram does not exhaust."""
    hand = [(sts_sim.Card.Hologram, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         discard_pile=[sts_sim.Card.BallLightning])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   discard_pile=[sts_sim.Card.BallLightning])
    state = play_named_card(game, sim, setup, sts_sim.Card.Hologram,
                            choices=[0], upgraded=True)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ===================================================================
# OVERCLOCK
# ===================================================================

def test_overclock_base(game):
    """Overclock draws 2 and adds Dazed to discard."""
    hand = [sts_sim.Card.Overclock]
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.Overclock)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)


def test_overclock_upgraded(game):
    """Upgraded Overclock draws 3."""
    hand = [(sts_sim.Card.Overclock, True)]
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.Overclock,
                            upgraded=True)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


# ===================================================================
# REPROGRAM
# ===================================================================

def test_reprogram_base(game):
    """Reprogram gains Strength and removes orbs."""
    hand = [sts_sim.Card.Reprogram]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         orbs=["Lightning", "Frost"])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   orbs=["Lightning", "Frost"])
    state = play_named_card(game, sim, setup, sts_sim.Card.Reprogram)
    assert_player_matches(state, sim)


def test_reprogram_upgraded(game):
    """Upgraded Reprogram costs 0."""
    hand = [(sts_sim.Card.Reprogram, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         orbs=["Frost", "Frost", "Dark"])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   orbs=["Frost", "Frost", "Dark"])
    state = play_named_card(game, sim, setup, sts_sim.Card.Reprogram,
                            upgraded=True)
    assert_player_matches(state, sim)


# ===================================================================
# STACK
# ===================================================================

def test_stack_with_orbs(game):
    """Stack gains block equal to orb count."""
    hand = [sts_sim.Card.StackCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         orbs=["Lightning", "Frost", "Dark"])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   orbs=["Lightning", "Frost", "Dark"])
    state = play_named_card(game, sim, setup, sts_sim.Card.StackCard)
    assert_player_matches(state, sim)


def test_stack_upgraded(game):
    """Upgraded Stack gains X+1 block."""
    hand = [(sts_sim.Card.StackCard, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         orbs=["Frost", "Frost"])
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   orbs=["Frost", "Frost"])
    state = play_named_card(game, sim, setup, sts_sim.Card.StackCard,
                            upgraded=True)
    assert_player_matches(state, sim)


# ===================================================================
# TURBO
# ===================================================================

def test_turbo_base(game):
    """TURBO gains 2 energy, adds Dazed, exhausts."""
    hand = [sts_sim.Card.TURBO]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.TURBO)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_turbo_upgraded(game):
    """Upgraded TURBO gains 3 energy."""
    hand = [(sts_sim.Card.TURBO, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.TURBO,
                            upgraded=True)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ===================================================================
# REINFORCED BODY
# ===================================================================

def test_reinforced_body_x1(game):
    """Reinforced Body with X=1 gains 2 block."""
    hand = [sts_sim.Card.ReinforcedBody]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.ReinforcedBody,
                            choices=[0])  # X=1 (first choice)
    assert_player_matches(state, sim)


# ===================================================================
# CAPACITOR
# ===================================================================

def test_capacitor_base(game):
    """Capacitor gains orb slots."""
    hand = [sts_sim.Card.CapacitorCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.CapacitorCard)
    assert_player_matches(state, sim)


def test_capacitor_upgraded(game):
    """Upgraded Capacitor gains 3 orb slots."""
    hand = [(sts_sim.Card.CapacitorCard, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.CapacitorCard,
                            upgraded=True)
    assert_player_matches(state, sim)


# ===================================================================
# CONSUME
# ===================================================================

def test_consume_base(game):
    """Consume enters play, costs 2."""
    hand = [sts_sim.Card.ConsumeCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.ConsumeCard)
    assert_player_matches(state, sim)


def test_consume_upgraded(game):
    """Upgraded Consume costs 1."""
    hand = [(sts_sim.Card.ConsumeCard, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.ConsumeCard,
                            upgraded=True)
    assert_player_matches(state, sim)


# ===================================================================
# FUSION
# ===================================================================

def test_fusion_base(game):
    """Fusion enters play, costs 2."""
    hand = [sts_sim.Card.FusionCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.FusionCard)
    assert_player_matches(state, sim)


def test_fusion_upgraded(game):
    """Upgraded Fusion costs 1."""
    hand = [(sts_sim.Card.FusionCard, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.FusionCard,
                            upgraded=True)
    assert_player_matches(state, sim)


# ===================================================================
# HEATSINKS
# ===================================================================

def test_heatsinks_base(game):
    """Heatsinks enters play, costs 1."""
    hand = [sts_sim.Card.HeatsinkCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.HeatsinkCard)
    assert_player_matches(state, sim)


# ===================================================================
# LOOP
# ===================================================================

def test_loop_base(game):
    """Loop enters play, costs 1."""
    hand = [sts_sim.Card.LoopCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.LoopCard)
    assert_player_matches(state, sim)


# ===================================================================
# MACHINE LEARNING
# ===================================================================

def test_machine_learning_base(game):
    """Machine Learning enters play, costs 1."""
    hand = [sts_sim.Card.MachineLearningCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup,
                            sts_sim.Card.MachineLearningCard)
    assert_player_matches(state, sim)


def test_machine_learning_upgraded(game):
    """Upgraded Machine Learning costs 0."""
    hand = [(sts_sim.Card.MachineLearningCard, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup,
                            sts_sim.Card.MachineLearningCard, upgraded=True)
    assert_player_matches(state, sim)


# ===================================================================
# STORM
# ===================================================================

def test_storm_base(game):
    """Storm enters play, costs 1."""
    hand = [sts_sim.Card.StormCard]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)
    state = play_named_card(game, sim, setup, sts_sim.Card.StormCard)
    assert_player_matches(state, sim)
