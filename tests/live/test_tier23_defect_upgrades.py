"""Tier 23: Defect upgrade verification — all ~56 Defect cards.

Tests verify that upgraded card stats (damage, block, cost, magic,
exhaust behavior) match between the live game and the simulator.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
)


# ===========================================================================
# Starters
# ===========================================================================


def test_strike_blue_upgraded_cost_and_damage(game):
    """StrikeBlue+ costs 0 (down from 1), damage 2 (up from 1).

    Setup: StrikeBlue+ in hand, monster at 30 HP, energy=3.
    After play: monster HP=28, energy=3 (0 cost).
    """
    hand = [(sts_sim.Card.StrikeBlue, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StrikeBlue,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after StrikeBlue+ (0 cost), got {state.combat_state.player.energy}"
    )


def test_defend_blue_upgraded_block(game):
    """DefendBlue+ gains 2 block (up from 1), costs 1.

    Setup: DefendBlue+ in hand, energy=3.
    After play: block=2, energy=2.
    """
    hand = [(sts_sim.Card.DefendBlue, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DefendBlue,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_zap_upgraded_cost(game):
    """Zap+ costs 0 (down from 1), channels Lightning.

    Setup: Zap+ in hand, energy=3.
    After play: energy=3 (0 cost), Lightning orb channeled.
    """
    hand = [(sts_sim.Card.Zap, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Zap,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after Zap+ (0 cost), got {state.combat_state.player.energy}"
    )


def test_dualcast_upgraded_cost(game):
    """Dualcast+ costs 0 (down from 1), evokes orb twice.

    Setup: Dualcast+ in hand, energy=3.
    After play: energy=3 (0 cost).
    """
    hand = [(sts_sim.Card.Dualcast, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Dualcast,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after Dualcast+ (0 cost), got {state.combat_state.player.energy}"
    )


# ===========================================================================
# Common Attacks
# ===========================================================================


def test_ball_lightning_upgraded_damage(game):
    """BallLightning+ deals 2 damage (up from 1), costs 1.

    Setup: BallLightning+ in hand, monster at 30 HP.
    After play: monster takes 2 damage.
    """
    hand = [(sts_sim.Card.BallLightning, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BallLightning,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_barrage_upgraded_magic(game):
    """Barrage+ gains 1 bonus hit (magic 0->1), cost 1, damage 1.

    Setup: Barrage+ in hand, monster at 30 HP.
    After play: monster takes damage.
    """
    hand = [(sts_sim.Card.Barrage, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Barrage,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_beam_cell_upgraded_damage(game):
    """BeamCell+ deals 2 damage (up from 1), costs 1, applies Vuln.

    Setup: BeamCell+ in hand, monster at 30 HP.
    After play: monster takes 2 damage, has Vulnerable.
    """
    hand = [(sts_sim.Card.BeamCell, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BeamCell,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_claw_upgraded_damage(game):
    """Claw+ deals 2 damage (up from 1), costs 0.

    Setup: Claw+ in hand, monster at 30 HP.
    After play: monster takes 2 damage, energy=3.
    """
    hand = [(sts_sim.Card.Claw, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Claw,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_compile_driver_upgraded_damage(game):
    """CompileDriver+ deals 2 damage (up from 1), costs 1, draws cards.

    Setup: CompileDriver+ in hand, 1 Strike in draw pile, monster at 30 HP.
    After play: monster takes 2 damage, cards drawn.
    """
    hand = [(sts_sim.Card.CompileDriver, True)]
    draw = [sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CompileDriver,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


def test_go_for_the_eyes_upgraded_damage(game):
    """GoForTheEyes+ deals 2 damage (up from 1), costs 0, applies Weak.

    Setup: GoForTheEyes+ in hand, monster at 30 HP.
    After play: monster takes 2 damage, has Weak.
    """
    hand = [(sts_sim.Card.GoForTheEyes, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.GoForTheEyes,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_sweeping_beam_upgraded_damage(game):
    """SweepingBeam+ deals 2 damage (up from 1), costs 1, AoE, draws.

    Setup: SweepingBeam+ in hand, 1 Strike in draw pile, monster at 30 HP.
    After play: monster takes 2 AoE damage, card drawn.
    """
    hand = [(sts_sim.Card.SweepingBeam, True)]
    draw = [sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SweepingBeam,
                            upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


# ===========================================================================
# Common Skills
# ===========================================================================


def test_charge_battery_upgraded_block(game):
    """ChargeBattery+ gains 3 block (up from 2), costs 1.

    Setup: ChargeBattery+ in hand, energy=3.
    After play: block=3, energy=2.
    """
    hand = [(sts_sim.Card.ChargeBattery, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ChargeBattery,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_chaos_upgraded_cost(game):
    """Chaos+ costs 0 (down from 1), channels random orb.

    Setup: Chaos+ in hand, energy=3.
    After play: energy=3 (0 cost).
    """
    hand = [(sts_sim.Card.Chaos, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Chaos,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after Chaos+ (0 cost), got {state.combat_state.player.energy}"
    )


def test_coolheaded_upgraded(game):
    """Coolheaded+ channels Frost, draws cards. Cost 1.

    Setup: Coolheaded+ in hand, 1 Strike in draw pile.
    After play: Frost channeled, card drawn.
    """
    hand = [(sts_sim.Card.Coolheaded, True)]
    draw = [sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Coolheaded,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_leap_upgraded_block(game):
    """Leap+ gains 3 block (up from 2), costs 1.

    Setup: Leap+ in hand, energy=3.
    After play: block=3, energy=2.
    """
    hand = [(sts_sim.Card.Leap, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Leap,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_recursion_upgraded_cost(game):
    """Recursion+ costs 0 (down from 1), evokes orb, channels copy.

    Setup: Recursion+ in hand, energy=3.
    After play: energy=3 (0 cost).
    """
    hand = [(sts_sim.Card.Recursion, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Recursion,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after Recursion+ (0 cost), got {state.combat_state.player.energy}"
    )


def test_steam_barrier_upgraded_block(game):
    """SteamBarrier+ gains 2 block (up from 1), costs 0.

    Setup: SteamBarrier+ in hand, energy=3.
    After play: block=2, energy=3.
    """
    hand = [(sts_sim.Card.SteamBarrier, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SteamBarrier,
                            upgraded=True)

    assert_player_matches(state, sim)


# ===========================================================================
# Uncommon Attacks
# ===========================================================================


def test_blizzard_upgraded_damage(game):
    """Blizzard+ deals 3 damage (up from 2), costs 1, AoE.

    Setup: Blizzard+ in hand, monster at 30 HP.
    After play: monster takes AoE damage.
    """
    hand = [(sts_sim.Card.Blizzard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Blizzard,
                            upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_cold_snap_upgraded_damage(game):
    """ColdSnap+ deals 3 damage (up from 2), costs 2.

    Setup: ColdSnap+ in hand, monster at 30 HP.
    After play: monster takes 3 damage.
    """
    hand = [(sts_sim.Card.ColdSnap, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ColdSnap,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_doom_and_gloom_upgraded_damage(game):
    """DoomAndGloom+ deals 3 damage (up from 2), costs 2, AoE.

    Setup: DoomAndGloom+ in hand, monster at 30 HP.
    After play: monster takes 3 AoE damage.
    """
    hand = [(sts_sim.Card.DoomAndGloom, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DoomAndGloom,
                            upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_ftl_upgraded_damage(game):
    """FTL+ deals 2 damage (up from 1), costs 0.

    Setup: FTL+ in hand, monster at 30 HP.
    After play: monster takes 2 damage, energy=3.
    """
    hand = [(sts_sim.Card.FTL, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FTL,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_melter_card_upgraded_damage(game):
    """MelterCard+ deals 3 damage (up from 2), costs 1.

    Setup: MelterCard+ in hand, monster at 30 HP.
    After play: monster takes 3 damage.
    """
    hand = [(sts_sim.Card.MelterCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.MelterCard,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_scrape_upgraded_damage(game):
    """Scrape+ deals 3 damage (up from 2), costs 1.

    Setup: Scrape+ in hand, monster at 30 HP.
    After play: monster takes 3 damage.
    """
    hand = [(sts_sim.Card.Scrape, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Scrape,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_streamline_upgraded_damage(game):
    """Streamline+ deals 4 damage (up from 3), costs 2.

    Setup: Streamline+ in hand, monster at 30 HP.
    After play: monster takes 4 damage.
    """
    hand = [(sts_sim.Card.Streamline, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Streamline,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_sunder_upgraded_damage(game):
    """Sunder+ deals 7 damage (up from 5), costs 3.

    Setup: Sunder+ in hand, monster at 30 HP, energy=3.
    After play: monster takes 7 damage, energy=0.
    """
    hand = [(sts_sim.Card.Sunder, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Sunder,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===========================================================================
# Uncommon Skills
# ===========================================================================


def test_darkness_card_upgraded_cost(game):
    """DarknessCard+ costs 0 (down from 1), channels Dark orb.

    Setup: DarknessCard+ in hand, energy=3.
    After play: energy=3 (0 cost).
    """
    hand = [(sts_sim.Card.DarknessCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DarknessCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after DarknessCard+ (0 cost), got {state.combat_state.player.energy}"
    )


def test_double_energy_upgraded_cost(game):
    """DoubleEnergy+ costs 0 (down from 1), exhausts, doubles energy.

    Setup: DoubleEnergy+ in hand, energy=3.
    After play: energy=6 (3*2, 0 cost), card exhausted.
    """
    hand = [(sts_sim.Card.DoubleEnergy, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DoubleEnergy,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert state.combat_state.player.energy == 6, (
        f"Expected 6 energy after DoubleEnergy+ (0 cost, 3*2), got {state.combat_state.player.energy}"
    )


def test_equilibrium_upgraded_block_and_magic(game):
    """Equilibrium+ gains 4 block (up from 3), magic 2 (up from 1). Cost 2.

    Setup: Equilibrium+ in hand, energy=3.
    After play: block=4, energy=1.
    """
    hand = [(sts_sim.Card.Equilibrium, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Equilibrium,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_force_field_upgraded_block(game):
    """ForceField+ gains 4 block (up from 3), costs 3.

    Setup: ForceField+ in hand, energy=3.
    After play: block=4, energy=0.
    """
    hand = [(sts_sim.Card.ForceField, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ForceField,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_glacier_upgraded_block(game):
    """Glacier+ gains 3 block (up from 2), costs 2.

    Setup: Glacier+ in hand, energy=3.
    After play: block=3, energy=1.
    """
    hand = [(sts_sim.Card.Glacier, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Glacier,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_hologram_upgraded_block_no_exhaust(game):
    """Hologram+ gains 2 block (up from 1), no longer exhausts. Cost 1.

    Setup: Hologram+ in hand, 1 Defend in discard pile.
    After play: block=2, Hologram+ goes to discard (not exhaust).
    """
    hand = [(sts_sim.Card.Hologram, True)]
    discard = [sts_sim.Card.DefendBlue]

    setup = set_scenario(game, hand=hand, discard_pile=discard, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, discard_pile=discard, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Hologram,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert_hand_matches(state, sim)


def test_overclock_upgraded_draw(game):
    """Overclock+ draws 3 cards (up from 2), costs 0, adds Burn.

    Setup: Overclock+ in hand, 3 Strikes in draw pile.
    After play: 3 cards drawn, Burn added.
    """
    hand = [(sts_sim.Card.Overclock, True)]
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.StrikeBlue,
            sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Overclock,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_recycle_card_upgraded_cost(game):
    """RecycleCard+ costs 0 (down from 1).

    Setup: RecycleCard+ + Strike in hand, energy=3.
    After play: energy=3 (0 cost).
    """
    hand = [(sts_sim.Card.RecycleCard, True), sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.RecycleCard,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_reprogram_upgraded_cost(game):
    """Reprogram+ costs 0 (down from 1).

    Setup: Reprogram+ in hand, energy=3.
    After play: energy=3 (0 cost).
    """
    hand = [(sts_sim.Card.Reprogram, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Reprogram,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after Reprogram+ (0 cost), got {state.combat_state.player.energy}"
    )


def test_stack_card_upgraded(game):
    """StackCard+ verification (stays same cost 1).

    Setup: StackCard+ in hand, energy=3.
    After play: block gained, energy=2.
    """
    hand = [(sts_sim.Card.StackCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StackCard,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_turbo_upgraded_magic(game):
    """TURBO+ gains 3 energy (up from 2), costs 0, exhausts.

    Setup: TURBO+ in hand, energy=3.
    After play: energy=6 (3+3), card exhausted.
    """
    hand = [(sts_sim.Card.TURBO, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.TURBO,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_reinforced_body_upgraded_magic(game):
    """ReinforcedBody+ gains 1 bonus (magic 0->1). Cost X.

    Setup: ReinforcedBody+ in hand, energy=3.
    After play with X=3: block gained, energy=0.
    """
    hand = [(sts_sim.Card.ReinforcedBody, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ReinforcedBody,
                            upgraded=True, choices=[3])

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 0


# ===========================================================================
# Uncommon Powers
# ===========================================================================


def test_capacitor_card_upgraded_magic(game):
    """CapacitorCard+ magic 3 (up from 2), costs 1.

    Setup: CapacitorCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.CapacitorCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CapacitorCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_consume_card_upgraded_cost(game):
    """ConsumeCard+ costs 1 (down from 2).

    Setup: ConsumeCard+ in hand, energy=3.
    After play: energy=2 (1 cost), power applied.
    """
    hand = [(sts_sim.Card.ConsumeCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ConsumeCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert state.combat_state.player.energy == 2, (
        f"Expected 2 energy after ConsumeCard+ (1 cost), got {state.combat_state.player.energy}"
    )


def test_fusion_card_upgraded_cost(game):
    """FusionCard+ costs 1 (down from 2).

    Setup: FusionCard+ in hand, energy=3.
    After play: energy=2 (1 cost), power applied.
    """
    hand = [(sts_sim.Card.FusionCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FusionCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert state.combat_state.player.energy == 2, (
        f"Expected 2 energy after FusionCard+ (1 cost), got {state.combat_state.player.energy}"
    )


def test_heatsink_card_upgraded_magic(game):
    """HeatsinkCard+ magic 3 (up from 2), costs 1.

    Setup: HeatsinkCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.HeatsinkCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.HeatsinkCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_loop_card_upgraded_magic(game):
    """LoopCard+ magic 2 (up from 1), costs 1.

    Setup: LoopCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.LoopCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.LoopCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_machine_learning_card_upgraded_cost(game):
    """MachineLearningCard+ costs 0 (down from 1).

    Setup: MachineLearningCard+ in hand, energy=3.
    After play: energy=3 (0 cost), power applied.
    """
    hand = [(sts_sim.Card.MachineLearningCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.MachineLearningCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after MachineLearningCard+ (0 cost), got {state.combat_state.player.energy}"
    )


def test_storm_card_upgraded_magic(game):
    """StormCard+ magic 2 (up from 1), costs 1.

    Setup: StormCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.StormCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StormCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===========================================================================
# Rare Attacks
# ===========================================================================


def test_all_for_one_upgraded_damage(game):
    """AllForOne+ deals 3 damage (up from 2), costs 2.

    Setup: AllForOne+ in hand, monster at 30 HP.
    After play: monster takes 3 damage.
    """
    hand = [(sts_sim.Card.AllForOne, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.AllForOne,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_core_surge_upgraded_damage(game):
    """CoreSurge+ deals 4 damage (up from 3), costs 1.

    Setup: CoreSurge+ in hand, monster at 30 HP.
    After play: monster takes 4 damage.
    """
    hand = [(sts_sim.Card.CoreSurge, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CoreSurge,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_hyperbeam_upgraded_damage(game):
    """Hyperbeam+ deals 7 damage (up from 5), costs 2, AoE.

    Setup: Hyperbeam+ in hand, monster at 30 HP.
    After play: monster takes 7 AoE damage.
    """
    hand = [(sts_sim.Card.Hyperbeam, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Hyperbeam,
                            upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_meteor_strike_upgraded_damage(game):
    """MeteorStrike+ deals 15 damage (up from 10), costs 5.

    Setup: MeteorStrike+ in hand, monster at 30 HP, energy=5.
    After play: monster takes 15 damage, energy=0.
    """
    hand = [(sts_sim.Card.MeteorStrike, True)]

    setup = set_scenario(game, hand=hand, energy=5, monster_hp=30)
    sim = make_sim(hand=hand, energy=5, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.MeteorStrike,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_thunder_strike_upgraded_damage(game):
    """ThunderStrike+ deals 6 damage (up from 4), costs 3, AoE.

    Setup: ThunderStrike+ in hand, monster at 30 HP, energy=3.
    After play: monster takes AoE damage, energy=0.
    """
    hand = [(sts_sim.Card.ThunderStrike, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ThunderStrike,
                            upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===========================================================================
# Rare Skills
# ===========================================================================


def test_amplify_card_upgraded_magic(game):
    """AmplifyCard+ magic 5 (up from 3), costs 1, exhausts.

    Setup: AmplifyCard+ in hand, energy=3.
    After play: energy=2, power applied, card exhausted.
    """
    hand = [(sts_sim.Card.AmplifyCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.AmplifyCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_fission_upgraded(game):
    """Fission+ stays same (cost 0, exhausts).

    Setup: Fission+ in hand, energy=3.
    After play: card exhausted.
    """
    hand = [(sts_sim.Card.Fission, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Fission,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_multi_cast_upgraded_magic(game):
    """MultiCast+ gains 1 bonus (magic 0->1). Cost X.

    Setup: MultiCast+ in hand, energy=3.
    After play with X=3: energy=0.
    """
    hand = [(sts_sim.Card.MultiCast, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.MultiCast,
                            upgraded=True, choices=[3])

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 0


def test_rainbow_card_upgraded_no_exhaust(game):
    """RainbowCard+ no longer exhausts (unupgraded exhausts). Cost 2.

    Setup: RainbowCard+ in hand, energy=3.
    After play: card goes to discard (not exhaust), energy=1.
    """
    hand = [(sts_sim.Card.RainbowCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.RainbowCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_seek_card_upgraded_magic(game):
    """SeekCard+ magic 2 (up from 1), costs 0, exhausts.

    Setup: SeekCard+ in hand, 2 Strikes in draw pile, energy=3.
    After play: 2 cards sought, card exhausted.
    """
    hand = [(sts_sim.Card.SeekCard, True)]
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SeekCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_skim_card_upgraded_draw(game):
    """SkimCard+ draws 4 cards (up from 3), costs 1.

    Setup: SkimCard+ in hand, 4 Strikes in draw pile.
    After play: 4 cards drawn.
    """
    hand = [(sts_sim.Card.SkimCard, True)]
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.StrikeBlue,
            sts_sim.Card.StrikeBlue, sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SkimCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_tempest_card_upgraded_magic(game):
    """TempestCard+ gains 1 bonus (magic 0->1). Cost X, exhausts.

    Setup: TempestCard+ in hand, energy=3.
    After play with X=3: energy=0, card exhausted.
    """
    hand = [(sts_sim.Card.TempestCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.TempestCard,
                            upgraded=True, choices=[3])

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert state.combat_state.player.energy == 0


# ===========================================================================
# Rare Powers
# ===========================================================================


def test_buffer_card_upgraded_magic(game):
    """BufferCard+ magic 2 (up from 1), costs 2.

    Setup: BufferCard+ in hand, energy=3.
    After play: energy=1, power applied.
    """
    hand = [(sts_sim.Card.BufferCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BufferCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_defragment_card_upgraded_no_ethereal(game):
    """DefragmentCard+ stays cost 3, loses ethereal when upgraded.

    Setup: DefragmentCard+ in hand, energy=3.
    After play: energy=0, power applied.
    """
    hand = [(sts_sim.Card.DefragmentCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DefragmentCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_echo_form_card_upgraded_no_ethereal(game):
    """EchoFormCard+ stays cost 3, loses ethereal when upgraded.

    Setup: EchoFormCard+ in hand, energy=3.
    After play: energy=0, power applied.
    """
    hand = [(sts_sim.Card.EchoFormCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.EchoFormCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_electrodynamics_card_upgraded_magic(game):
    """ElectrodynamicsCard+ magic 3 (up from 2), costs 2.

    Setup: ElectrodynamicsCard+ in hand, energy=3.
    After play: energy=1, power applied.
    """
    hand = [(sts_sim.Card.ElectrodynamicsCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ElectrodynamicsCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_static_discharge_card_upgraded_magic(game):
    """StaticDischargeCard+ magic 2 (up from 1), costs 2.

    Setup: StaticDischargeCard+ in hand, energy=3.
    After play: energy=1, power applied.
    """
    hand = [(sts_sim.Card.StaticDischargeCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StaticDischargeCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
