"""Tier 19: Defect base card tests.

Tests verify that all Defect base (unupgraded) cards produce matching
state between the live BG mod game and the Rust simulator.  Orb state
is not compared directly — only HP, block, energy, and card piles.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
    CARD_TO_BG, _card_spec_card, _card_spec_upgraded,
)


# ---------------------------------------------------------------------------
# Helper: make_sim variant that uses Character.Defect so orb slots exist.
# Mirrors conftest.make_sim but passes Character.Defect to the constructor.
# ---------------------------------------------------------------------------

def _make_defect_sim(*, hand=None, draw_pile=None, discard_pile=None,
                     energy=3, player_hp=9, player_block=0,
                     player_powers=None, player_relics=None, monster_hp=8,
                     monster_block=0, monster_powers=None, monsters=None):
    hand = hand or []
    draw_pile = draw_pile or []
    discard_pile = discard_pile or []

    if monsters is not None:
        monster_list = []
        for i, m in enumerate(monsters):
            mon = sts_sim.Monster(f"Monster_{i}", m.get("hp", 30),
                                  "jaw_worm", "A", False)
            blk = m.get("block", 0)
            if blk > 0:
                mon.add_block(blk)
            if m.get("powers"):
                for power_name, amount in m["powers"].items():
                    pt = getattr(sts_sim.PowerType, power_name)
                    mon.apply_power(pt, amount)
            monster_list.append(mon)
    else:
        monster = sts_sim.Monster("Jaw Worm", monster_hp, "jaw_worm",
                                   "A", False)
        if monster_block > 0:
            monster.add_block(monster_block)
        if monster_powers:
            for power_name, amount in monster_powers.items():
                pt = getattr(sts_sim.PowerType, power_name)
                monster.apply_power(pt, amount)
        monster_list = [monster]

    sim = sts_sim.CombatState.new_with_character(
        monster_list, seed=0, character=sts_sim.Character.Defect,
    )
    sim.set_player_energy(energy)
    sim.set_player_hp(player_hp)
    sim.set_player_block(player_block)

    if player_relics is not None:
        sim.clear_relics()
        for relic in player_relics:
            sim.add_relic(relic)

    if player_powers:
        for power_name, amount in player_powers.items():
            pt = getattr(sts_sim.PowerType, power_name)
            sim.apply_player_power(pt, amount)

    for card_spec in draw_pile:
        card = _card_spec_card(card_spec)
        if _card_spec_upgraded(card_spec):
            sim.add_upgraded_card_to_draw(card)
        else:
            sim.add_card_to_draw(card)

    for card_spec in discard_pile:
        card = _card_spec_card(card_spec)
        if _card_spec_upgraded(card_spec):
            sim.add_upgraded_card_to_discard(card)
        else:
            sim.add_card_to_discard(card)

    for card_spec in hand:
        card = _card_spec_card(card_spec)
        if _card_spec_upgraded(card_spec):
            sim.add_upgraded_card_to_hand(card)
        else:
            sim.add_card_to_hand(card)

    return sim


# ===================================================================
# STARTERS
# ===================================================================


# -- StrikeBlue: cost 1, damage 1, attack, targeted --

def test_strike_blue(game):
    """StrikeBlue deals base damage to a single target."""
    hand = [sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StrikeBlue,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- DefendBlue: cost 1, block 1, skill --

def test_defend_blue(game):
    """DefendBlue grants block."""
    hand = [sts_sim.Card.DefendBlue]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DefendBlue)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- Zap: cost 1, skill (channels Lightning orb) --

def test_zap(game):
    """Zap channels a Lightning orb. Verify energy and piles."""
    hand = [sts_sim.Card.Zap]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Zap)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- Dualcast: cost 1, skill (evokes orb twice) --

def test_dualcast(game):
    """Dualcast evokes the first orb twice. Verify energy and piles.

    Setup: Zap first to have an orb, then Dualcast.
    """
    hand = [sts_sim.Card.Zap, sts_sim.Card.Dualcast]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    # Channel an orb first
    state = play_named_card(game, sim, setup, sts_sim.Card.Zap)
    # Then evoke it twice
    state = play_card_both(game, sim, hand_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# COMMON ATTACKS
# ===================================================================


# -- BallLightning: cost 1, damage 1, magic 1 (channel Lightning), targeted --

def test_ball_lightning(game):
    """BallLightning deals damage and channels Lightning."""
    hand = [sts_sim.Card.BallLightning]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BallLightning,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- Barrage: cost 1, damage 1, targeted (hits per orb) --

def test_barrage(game):
    """Barrage hits once per channeled orb. With no orbs, deals 0 hits.

    Setup: Zap first to have 1 orb, then Barrage for 1 hit.
    """
    hand = [sts_sim.Card.Zap, sts_sim.Card.Barrage]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Zap)
    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- BeamCell: cost 1, damage 1, targeted (applies Vulnerable) --

def test_beam_cell(game):
    """BeamCell deals damage and applies Vulnerable."""
    hand = [sts_sim.Card.BeamCell]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BeamCell,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- Claw: cost 0, damage 1, targeted (increases damage globally) --

def test_claw(game):
    """Claw deals damage at cost 0."""
    hand = [sts_sim.Card.Claw]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Claw,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- CompileDriver: cost 1, damage 1, magic 1 (draw), targeted --

def test_compile_driver(game):
    """CompileDriver deals damage and draws 1 card."""
    hand = [sts_sim.Card.CompileDriver]
    draw = [sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, draw_pile=draw,
                           energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CompileDriver,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


# -- GoForTheEyes: cost 0, damage 1, targeted (applies Weak) --

def test_go_for_the_eyes(game):
    """GoForTheEyes deals damage and applies Weak."""
    hand = [sts_sim.Card.GoForTheEyes]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.GoForTheEyes,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- SweepingBeam: cost 1, damage 1, magic 1 (draw), AoE (no target) --

def test_sweeping_beam(game):
    """SweepingBeam deals AoE damage and draws 1 card."""
    hand = [sts_sim.Card.SweepingBeam]
    draw = [sts_sim.Card.DefendBlue]

    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, draw_pile=draw,
                           energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SweepingBeam)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


# ===================================================================
# COMMON SKILLS
# ===================================================================


# -- ChargeBattery: cost 1, block 2, magic 1, skill --

def test_charge_battery(game):
    """ChargeBattery grants block."""
    hand = [sts_sim.Card.ChargeBattery]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ChargeBattery)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- Chaos: cost 1, skill (channels random orb) --

def test_chaos(game):
    """Chaos channels a random orb. Verify energy and piles."""
    hand = [sts_sim.Card.Chaos]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Chaos)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- Coolheaded: cost 1, skill (channels Frost, draws 1) --

def test_coolheaded(game):
    """Coolheaded channels Frost and draws 1 card."""
    hand = [sts_sim.Card.Coolheaded]
    draw = [sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, draw_pile=draw,
                           energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Coolheaded)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


# -- Leap: cost 1, block 2, skill --

def test_leap(game):
    """Leap grants block."""
    hand = [sts_sim.Card.Leap]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Leap)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- Recursion: cost 1, skill (evokes orb, channels copy) --

def test_recursion(game):
    """Recursion evokes first orb and channels a copy.

    Setup: Zap first to have a Lightning orb, then Recursion.
    """
    hand = [sts_sim.Card.Zap, sts_sim.Card.Recursion]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Zap)
    state = play_card_both(game, sim, hand_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- SteamBarrier: cost 0, block 1, skill --

def test_steam_barrier(game):
    """SteamBarrier grants block at cost 0."""
    hand = [sts_sim.Card.SteamBarrier]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SteamBarrier)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===================================================================
# UNCOMMON ATTACKS
# ===================================================================


# -- Blizzard: cost 1, damage 2, AoE (no target, damage per channel) --

def test_blizzard(game):
    """Blizzard deals AoE damage based on Frost orbs channeled."""
    hand = [sts_sim.Card.Blizzard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Blizzard)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- ColdSnap: cost 2, damage 2, targeted (channels Frost) --

def test_cold_snap(game):
    """ColdSnap deals damage and channels Frost."""
    hand = [sts_sim.Card.ColdSnap]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ColdSnap,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- DoomAndGloom: cost 2, damage 2, AoE (no target, channels Dark) --

def test_doom_and_gloom(game):
    """DoomAndGloom deals AoE damage and channels Dark orb."""
    hand = [sts_sim.Card.DoomAndGloom]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DoomAndGloom)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- FTL: cost 0, damage 1, targeted (draws if <4 cards played) --

def test_ftl(game):
    """FTL deals damage and draws cards if fewer than 4 cards played this turn."""
    hand = [sts_sim.Card.FTL]
    draw = [sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, draw_pile=draw,
                           energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FTL,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


# -- MelterCard: cost 1, damage 2, targeted (removes block) --

def test_melter(game):
    """MelterCard deals damage and removes enemy block."""
    hand = [sts_sim.Card.MelterCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         monster_block=5)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30,
                           monster_block=5)

    state = play_named_card(game, sim, setup, sts_sim.Card.MelterCard,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- Scrape: cost 1, damage 2, targeted (draws, discards non-0-cost) --

def test_scrape(game):
    """Scrape deals damage, draws cards, discards non-0-cost drawn cards."""
    hand = [sts_sim.Card.Scrape]
    draw = [sts_sim.Card.Claw]  # 0-cost, should stay in hand

    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, draw_pile=draw,
                           energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Scrape,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


# -- Streamline: cost 2, damage 3, targeted (cost decreases) --

def test_streamline(game):
    """Streamline deals damage. Cost decreases each play."""
    hand = [sts_sim.Card.Streamline]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Streamline,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- Sunder: cost 3, damage 5, targeted (gain energy if kills) --

def test_sunder(game):
    """Sunder deals heavy damage. If it kills, gain energy."""
    hand = [sts_sim.Card.Sunder]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Sunder,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# UNCOMMON SKILLS
# ===================================================================


# -- DarknessCard: cost 1, skill (channels Dark orb) --

def test_darkness(game):
    """DarknessCard channels a Dark orb."""
    hand = [sts_sim.Card.DarknessCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DarknessCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- DoubleEnergy: cost 1, skill, exhausts (doubles energy) --

def test_double_energy(game):
    """DoubleEnergy doubles current energy and exhausts."""
    hand = [sts_sim.Card.DoubleEnergy]

    setup = set_scenario(game, hand=hand, energy=2, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=2, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DoubleEnergy)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# -- Equilibrium: cost 2, block 3, magic 1, skill (retain hand) --

def test_equilibrium(game):
    """Equilibrium grants block and retains hand."""
    hand = [sts_sim.Card.Equilibrium]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Equilibrium)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- ForceField: cost 3, block 3, skill (cost decreases per power played) --

def test_force_field(game):
    """ForceField grants block. Cost decreases per power played."""
    hand = [sts_sim.Card.ForceField]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ForceField)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- Glacier: cost 2, block 2, skill (channels 2 Frost) --

def test_glacier(game):
    """Glacier grants block and channels 2 Frost orbs."""
    hand = [sts_sim.Card.Glacier]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Glacier)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- Hologram: cost 1, block 1, skill, exhausts(base) (retrieve from discard) --

def test_hologram(game):
    """Hologram grants block, retrieves a card from discard, exhausts (base).

    Setup: Hologram in hand, 1 StrikeBlue in discard.
    After play: StrikeBlue moved to hand, Hologram exhausted.
    """
    hand = [sts_sim.Card.Hologram]
    discard = [sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, discard_pile=discard,
                         energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, discard_pile=discard,
                           energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Hologram)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)


# -- Overclock: cost 0, magic 2 (draw), skill (adds Burn) --

def test_overclock(game):
    """Overclock draws 2 cards and adds a Burn to the discard pile."""
    hand = [sts_sim.Card.Overclock]
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]

    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, draw_pile=draw,
                           energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Overclock)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


# -- RecycleCard: cost 1, skill (exhaust card from hand, gain energy) --

def test_recycle(game):
    """RecycleCard exhausts a card from hand and gains energy.

    Setup: RecycleCard + StrikeBlue in hand.
    After play: StrikeBlue exhausted (only remaining card), energy gained.
    """
    hand = [sts_sim.Card.RecycleCard, sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.RecycleCard)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


# -- Reprogram: cost 1, magic 1, skill (lose Focus, gain Str/Dex) --

def test_reprogram(game):
    """Reprogram loses Focus and gains Strength and Dexterity."""
    hand = [sts_sim.Card.Reprogram]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Reprogram)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- StackCard: cost 1, skill (block = discard pile size) --

def test_stack(game):
    """StackCard gains block equal to discard pile size.

    Setup: 3 cards in discard pile so block = 3.
    """
    hand = [sts_sim.Card.StackCard]
    discard = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
               sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, discard_pile=discard,
                         energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, discard_pile=discard,
                           energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StackCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- TURBO: cost 0, magic 2 (energy), skill, exhausts (gain energy, add Void) --

def test_turbo(game):
    """TURBO gains 2 energy and adds a Void to the discard pile."""
    hand = [sts_sim.Card.TURBO]

    setup = set_scenario(game, hand=hand, energy=1, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=1, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.TURBO)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- ReinforcedBody: X-cost (-1), skill (gain block per X) --

def test_reinforced_body(game):
    """ReinforcedBody gains block X times where X = energy spent.

    Setup: 3 energy. choices=[3] to spend all energy.
    """
    hand = [sts_sim.Card.ReinforcedBody]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ReinforcedBody,
                            choices=[3])

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===================================================================
# UNCOMMON POWERS
# ===================================================================


# -- CapacitorCard: cost 1, magic 2 (orb slots), power --

def test_capacitor(game):
    """CapacitorCard is a power that costs 1 energy."""
    hand = [sts_sim.Card.CapacitorCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CapacitorCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- ConsumeCard: cost 2, magic 1, power --

def test_consume(game):
    """ConsumeCard is a power that costs 2 energy."""
    hand = [sts_sim.Card.ConsumeCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ConsumeCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- FusionCard: cost 2, magic 1, power --

def test_fusion(game):
    """FusionCard is a power that costs 2 energy."""
    hand = [sts_sim.Card.FusionCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FusionCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- HeatsinkCard: cost 1, magic 2 (draw on power), power --

def test_heatsink(game):
    """HeatsinkCard is a power that costs 1 energy."""
    hand = [sts_sim.Card.HeatsinkCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.HeatsinkCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- LoopCard: cost 1, magic 1, power --

def test_loop(game):
    """LoopCard is a power that costs 1 energy."""
    hand = [sts_sim.Card.LoopCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.LoopCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- MachineLearningCard: cost 1, magic 1, power --

def test_machine_learning(game):
    """MachineLearningCard is a power that costs 1 energy."""
    hand = [sts_sim.Card.MachineLearningCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.MachineLearningCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- StormCard: cost 1, magic 1, power --

def test_storm(game):
    """StormCard is a power that costs 1 energy."""
    hand = [sts_sim.Card.StormCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StormCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===================================================================
# RARE ATTACKS
# ===================================================================


# -- AllForOne: cost 2, damage 2, targeted (play all 0-cost from discard) --

def test_all_for_one(game):
    """AllForOne deals damage and plays all 0-cost cards from discard.

    Setup: AllForOne in hand, Claw in discard (0-cost).
    After play: Claw moved from discard to hand.
    """
    hand = [sts_sim.Card.AllForOne]
    discard = [sts_sim.Card.Claw]

    setup = set_scenario(game, hand=hand, discard_pile=discard,
                         energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, discard_pile=discard,
                           energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.AllForOne,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


# -- CoreSurge: cost 1, damage 3, targeted (gain Artifact) --

def test_core_surge(game):
    """CoreSurge deals damage and grants Artifact."""
    hand = [sts_sim.Card.CoreSurge]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CoreSurge,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- Hyperbeam: cost 2, damage 5, AoE (no target, lose Focus) --

def test_hyperbeam(game):
    """Hyperbeam deals AoE damage and player loses Focus."""
    hand = [sts_sim.Card.Hyperbeam]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Hyperbeam)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- MeteorStrike: cost 5, damage 10, targeted (channel 3 Plasma) --

def test_meteor_strike(game):
    """MeteorStrike deals heavy damage and channels 3 Plasma orbs."""
    hand = [sts_sim.Card.MeteorStrike]

    setup = set_scenario(game, hand=hand, energy=5, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=5, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.MeteorStrike,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- ThunderStrike: cost 3, damage 4, AoE (no target, hits per Lightning) --

def test_thunder_strike(game):
    """ThunderStrike deals AoE damage, hitting once per Lightning channeled."""
    hand = [sts_sim.Card.ThunderStrike]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ThunderStrike)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# RARE SKILLS
# ===================================================================


# -- AmplifyCard: cost 1, magic 3, skill, exhausts --

def test_amplify(game):
    """AmplifyCard exhausts after play."""
    hand = [sts_sim.Card.AmplifyCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.AmplifyCard)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# -- Fission: cost 0, skill, exhausts (remove orbs, gain energy+draw) --

def test_fission(game):
    """Fission removes orbs, gains energy and draws. Exhausts.

    Setup: No orbs channeled, so 0 energy/draw gained.
    """
    hand = [sts_sim.Card.Fission]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Fission)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# -- MultiCast: X-cost (-1), skill (evoke orb X times) --

def test_multi_cast(game):
    """MultiCast evokes first orb X times.

    Setup: Zap + MultiCast in hand, 3 energy. Zap first to have orb.
    Then MultiCast with choices=[2] (spend 2 remaining energy).
    """
    hand = [sts_sim.Card.Zap, sts_sim.Card.MultiCast]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Zap)
    state = play_card_both(game, sim, hand_index=0, choices=[2])

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# -- RainbowCard: cost 2, skill, exhausts(base) (channel all 3 orb types) --

def test_rainbow(game):
    """RainbowCard channels Lightning, Frost, and Dark. Exhausts (base)."""
    hand = [sts_sim.Card.RainbowCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.RainbowCard)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# -- SeekCard: cost 0, magic 1, skill, exhausts (draw from deck) --

def test_seek(game):
    """SeekCard draws a card from draw pile and exhausts.

    Setup: 1 StrikeBlue in draw pile.
    """
    hand = [sts_sim.Card.SeekCard]
    draw = [sts_sim.Card.StrikeBlue]

    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, draw_pile=draw,
                           energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SeekCard)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_exhaust_matches(state, sim)


# -- SkimCard: cost 1, magic 3 (draw), skill --

def test_skim(game):
    """SkimCard draws 3 cards."""
    hand = [sts_sim.Card.SkimCard]
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Claw]

    setup = set_scenario(game, hand=hand, draw_pile=draw,
                         energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, draw_pile=draw,
                           energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SkimCard)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


# -- TempestCard: X-cost (-1), skill, exhausts (channel X Lightning) --

def test_tempest(game):
    """TempestCard channels X Lightning orbs and exhausts.

    Setup: 3 energy. choices=[3] to spend all energy.
    """
    hand = [sts_sim.Card.TempestCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.TempestCard,
                            choices=[3])

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ===================================================================
# RARE POWERS
# ===================================================================


# -- BufferCard: cost 2, magic 1, power --

def test_buffer(game):
    """BufferCard is a power that costs 2 energy."""
    hand = [sts_sim.Card.BufferCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BufferCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- DefragmentCard: cost 3, magic 1, power --

def test_defragment(game):
    """DefragmentCard is a power that costs 3 energy (BG base)."""
    hand = [sts_sim.Card.DefragmentCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DefragmentCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- EchoFormCard: cost 3, power (ethereal base) --

def test_echo_form(game):
    """EchoFormCard is a power that costs 3 energy. Ethereal at base."""
    hand = [sts_sim.Card.EchoFormCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.EchoFormCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- ElectrodynamicsCard: cost 2, magic 2, power --

def test_electrodynamics(game):
    """ElectrodynamicsCard is a power that costs 2 energy."""
    hand = [sts_sim.Card.ElectrodynamicsCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup,
                            sts_sim.Card.ElectrodynamicsCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# -- StaticDischargeCard: cost 2, magic 1, power --

def test_static_discharge(game):
    """StaticDischargeCard is a power that costs 2 energy."""
    hand = [sts_sim.Card.StaticDischargeCard]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = _make_defect_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup,
                            sts_sim.Card.StaticDischargeCard)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
