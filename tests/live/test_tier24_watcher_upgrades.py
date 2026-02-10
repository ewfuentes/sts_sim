"""Tier 24: Watcher upgrade verification — all ~60 Watcher cards.

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


# ---------------------------------------------------------------------------
# Local helper: make_sim variant that uses Character.Watcher
# ---------------------------------------------------------------------------

def make_watcher_sim(*, hand=None, draw_pile=None, discard_pile=None,
                     energy=3, player_hp=9, player_block=0,
                     player_powers=None, player_relics=None,
                     monster_hp=30, monster_block=0, monster_powers=None,
                     monsters=None):
    """Create a simulator CombatState with Character.Watcher.

    Mirrors make_sim() from conftest but uses the Watcher character so that
    stance mechanics (Wrath, Calm, Divinity) work correctly.
    """
    hand = hand or []
    draw_pile = draw_pile or []
    discard_pile = discard_pile or []

    if monsters is not None:
        monster_list = []
        for i, m in enumerate(monsters):
            mon = sts_sim.Monster(f"Monster_{i}", m.get("hp", 30), "jaw_worm", "A", False)
            blk = m.get("block", 0)
            if blk > 0:
                mon.add_block(blk)
            if m.get("powers"):
                for power_name, amount in m["powers"].items():
                    pt = getattr(sts_sim.PowerType, power_name)
                    mon.apply_power(pt, amount)
            monster_list.append(mon)
    else:
        monster = sts_sim.Monster("Jaw Worm", monster_hp, "jaw_worm", "A", False)
        if monster_block > 0:
            monster.add_block(monster_block)
        if monster_powers:
            for power_name, amount in monster_powers.items():
                pt = getattr(sts_sim.PowerType, power_name)
                monster.apply_power(pt, amount)
        monster_list = [monster]

    sim = sts_sim.CombatState.new_with_character(
        monster_list, seed=0, character=sts_sim.Character.Watcher,
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


def _card_spec_card(card_spec):
    if isinstance(card_spec, tuple):
        return card_spec[0]
    return card_spec


def _card_spec_upgraded(card_spec):
    if isinstance(card_spec, tuple):
        return card_spec[1]
    return False


# ===================================================================
# STARTERS
# ===================================================================


def test_strike_purple_upgraded_damage(game):
    """StrikePurple+ deals 2 damage (up from 1), costs 1.

    Setup: StrikePurple+ in hand, monster at 30 HP.
    After play: monster takes 2 damage.
    """
    hand = [(sts_sim.Card.StrikePurple, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StrikePurple,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_defend_purple_upgraded_block(game):
    """DefendPurple+ gains 2 block (up from 1), costs 1.

    Setup: DefendPurple+ in hand.
    After play: block=2, energy=2.
    """
    hand = [(sts_sim.Card.DefendPurple, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DefendPurple,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_eruption_upgraded_cost(game):
    """Eruption+ costs 1 (down from 2), deals 2 damage, enters Wrath.

    Setup: Eruption+ in hand, monster at 30 HP, energy=3.
    After play: monster takes 2 damage, energy=2 (cost 1).
    """
    hand = [(sts_sim.Card.Eruption, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Eruption,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_vigilance_upgraded_block(game):
    """Vigilance+ gains 3 block (up from 2), costs 2, enters Calm.

    Setup: Vigilance+ in hand, energy=3.
    After play: block=3, energy=1.
    """
    hand = [(sts_sim.Card.Vigilance, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Vigilance,
                            upgraded=True)

    assert_player_matches(state, sim)


# ===================================================================
# COMMON ATTACKS
# ===================================================================


def test_flurry_of_blows_upgraded_magic(game):
    """FlurryOfBlows+ magic 1->2 bonus, costs 0, damage 1.

    Setup: FlurryOfBlows+ in hand, monster at 30 HP.
    After play: monster takes damage matching sim.
    """
    hand = [(sts_sim.Card.FlurryOfBlows, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FlurryOfBlows,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_empty_fist_upgraded_damage(game):
    """EmptyFist+ deals 3 damage (up from 2), costs 1, exits stance.

    Setup: EmptyFist+ in hand, monster at 30 HP.
    After play: monster takes 3 damage.
    """
    hand = [(sts_sim.Card.EmptyFist, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.EmptyFist,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_consecrate_upgraded_damage(game):
    """Consecrate+ deals 2 damage (up from 1), costs 0, AoE.

    Setup: Consecrate+ in hand, monster at 30 HP.
    After play: monster takes 2 AoE damage.
    """
    hand = [(sts_sim.Card.Consecrate, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Consecrate,
                            upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_cut_through_fate_upgraded(game):
    """CutThroughFate+ deals 2 damage (up from 1), scry 3 (up from 2).

    Setup: CutThroughFate+ in hand, 3 cards in draw pile.
    After play: monster takes 2 damage, scry resolves.
    """
    hand = [(sts_sim.Card.CutThroughFate, True)]
    draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CutThroughFate,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_just_lucky_upgraded(game):
    """JustLucky+ deals 2 damage (up from 1), scry 2 (up from 1), block 1.

    Setup: JustLucky+ in hand, 2 cards in draw pile, monster at 30 HP.
    After play: monster takes 2 damage, block=1.
    """
    hand = [(sts_sim.Card.JustLucky, True)]
    draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.JustLucky,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# COMMON SKILLS
# ===================================================================


def test_empty_body_upgraded_block(game):
    """EmptyBody+ gains 3 block (up from 2), costs 1, exits stance.

    Setup: EmptyBody+ in hand, energy=3.
    After play: block=3, energy=2.
    """
    hand = [(sts_sim.Card.EmptyBody, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.EmptyBody,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_protect_upgraded_block(game):
    """Protect+ gains 4 block (up from 3), costs 2.

    Setup: Protect+ in hand, energy=3.
    After play: block=4, energy=1.
    """
    hand = [(sts_sim.Card.Protect, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Protect,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_halt_upgraded_magic(game):
    """Halt+ magic 1->2 extra block, costs 0, base block 1.

    Setup: Halt+ in hand, energy=3.
    After play: block matches sim, energy=3.
    """
    hand = [(sts_sim.Card.Halt, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Halt,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_third_eye_upgraded(game):
    """ThirdEye+ gains 3 block (up from 2), scry 5 (up from 3).

    Setup: ThirdEye+ in hand, 5 cards in draw pile.
    After play: block=3, scry resolves.
    """
    hand = [(sts_sim.Card.ThirdEye, True)]
    draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ThirdEye,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_tranquility_upgraded_cost(game):
    """Tranquility+ costs 0 (down from 1), exhausts, enters Calm.

    Setup: Tranquility+ in hand, energy=3.
    After play: energy=3 (0 cost), card exhausted.
    """
    hand = [(sts_sim.Card.Tranquility, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Tranquility,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert_hand_matches(state, sim)


def test_crescendo_upgraded(game):
    """Crescendo+ stays same (cost 0, exhaust, enters Wrath).

    Setup: Crescendo+ in hand, energy=3.
    After play: energy=3, card exhausted.
    """
    hand = [(sts_sim.Card.Crescendo, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert_hand_matches(state, sim)


def test_collect_upgraded_magic(game):
    """Collect+ generates 3 miracles (up from 2), costs 1, exhausts.

    Setup: Collect+ in hand, energy=3.
    After play: energy=2, card exhausted.
    """
    hand = [(sts_sim.Card.Collect, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Collect,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ===================================================================
# UNCOMMON ATTACKS
# ===================================================================


def test_crush_joints_upgraded_damage(game):
    """CrushJoints+ deals 2 damage (up from 1), costs 1, applies Weak.

    Setup: CrushJoints+ in hand, monster at 30 HP.
    After play: monster takes 2 damage.
    """
    hand = [(sts_sim.Card.CrushJoints, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CrushJoints,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_fear_no_evil_upgraded_damage(game):
    """FearNoEvil+ deals 3 damage (up from 2), costs 1.

    Setup: FearNoEvil+ in hand, monster at 30 HP.
    After play: monster takes 3 damage.
    """
    hand = [(sts_sim.Card.FearNoEvil, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FearNoEvil,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_foreign_influence_upgraded_damage(game):
    """ForeignInfluence+ deals 4 damage (up from 3), costs 2.

    Setup: ForeignInfluence+ in hand, monster at 30 HP.
    After play: monster takes 4 damage.
    """
    hand = [(sts_sim.Card.ForeignInfluence, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ForeignInfluence,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_sash_whip_upgraded(game):
    """SashWhip+ deals 3 damage (up from 2), vuln 2 (up from 1), costs 1.

    Setup: SashWhip+ in hand, monster at 30 HP.
    After play: monster takes 3 damage.
    """
    hand = [(sts_sim.Card.SashWhip, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SashWhip,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_tantrum_upgraded(game):
    """Tantrum+ damage 1 (down from 2) but 2 hits (up from 1), costs 1.

    Setup: Tantrum+ in hand, monster at 30 HP.
    After play: monster takes total damage matching sim.
    """
    hand = [(sts_sim.Card.Tantrum, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Tantrum,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_carve_reality_upgraded_damage(game):
    """CarveReality+ deals 4 damage (up from 3), costs 2.

    Setup: CarveReality+ in hand, monster at 30 HP.
    After play: monster takes 4 damage.
    """
    hand = [(sts_sim.Card.CarveReality, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CarveReality,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_sands_of_time_upgraded_magic(game):
    """SandsOfTime+ magic 2->3 per retain, costs 2, base damage 3.

    Setup: SandsOfTime+ in hand, monster at 30 HP.
    After play: monster takes base damage (not retained yet).
    """
    hand = [(sts_sim.Card.SandsOfTime, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SandsOfTime,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_windmill_strike_upgraded_magic(game):
    """WindmillStrike+ magic 3->5 bonus if retained, costs 2, base damage 2.

    Setup: WindmillStrike+ in hand, monster at 30 HP (first play, not retained).
    After play: monster takes base damage.
    """
    hand = [(sts_sim.Card.WindmillStrike, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.WindmillStrike,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_wallop_upgraded_damage(game):
    """Wallop+ deals 3 damage (up from 2), costs 2, block=unblocked dmg.

    Setup: Wallop+ in hand, monster at 30 HP (no block).
    After play: monster takes 3 damage, player gains 3 block.
    """
    hand = [(sts_sim.Card.Wallop, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Wallop,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_weave_upgraded(game):
    """Weave+ deals 2 damage (up from 1), magic 5->6, costs 0.

    Setup: Weave+ in hand, monster at 30 HP.
    After play: monster takes 2 damage.
    """
    hand = [(sts_sim.Card.Weave, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Weave,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_signature_move_upgraded_damage(game):
    """SignatureMove+ deals 8 damage (up from 6), costs 2.

    Setup: SignatureMove+ as only attack in hand, monster at 30 HP.
    After play: monster takes 8 damage.
    """
    hand = [(sts_sim.Card.SignatureMove, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SignatureMove,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_flying_sleeves_upgraded_magic(game):
    """FlyingSleeves+ hits 3 times (up from 2), damage 1, costs 1.

    Setup: FlyingSleeves+ in hand, monster at 30 HP.
    After play: monster takes 1*3=3 damage.
    """
    hand = [(sts_sim.Card.FlyingSleeves, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FlyingSleeves,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_conclude_upgraded_magic(game):
    """Conclude+ hits 3 times (up from 2), damage 1, block 1, AoE, ends turn.

    Setup: Conclude+ in hand, monster at 30 HP.
    After play: monster takes damage matching sim.
    """
    hand = [(sts_sim.Card.Conclude, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Conclude,
                            upgraded=True)

    assert_monsters_match(state, sim)


def test_reach_heaven_upgraded_magic(game):
    """ReachHeaven+ magic 1->2, deals 2 damage, costs 1.

    Setup: ReachHeaven+ in hand, monster at 30 HP.
    After play: monster takes 2 damage.
    """
    hand = [(sts_sim.Card.ReachHeaven, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ReachHeaven,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# UNCOMMON SKILLS
# ===================================================================


def test_empty_mind_upgraded_draw(game):
    """EmptyMind+ draws 3 cards (up from 2), costs 1, exits stance.

    Setup: EmptyMind+ in hand, 3 cards in draw pile.
    After play: 3 cards drawn.
    """
    hand = [(sts_sim.Card.EmptyMind, True)]
    draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.EmptyMind,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


def test_meditate_upgraded_magic(game):
    """MeditateCard+ magic 1->2, costs 1, ends turn, enters Calm.

    Setup: MeditateCard+ in hand.
    After play: verify player matches (ends turn).
    """
    hand = [(sts_sim.Card.MeditateCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.MeditateCard,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_inner_peace_upgraded_draw(game):
    """InnerPeace+ draws 4 cards (up from 3), costs 1.

    Setup: InnerPeace+ in hand, 4 cards in draw pile.
    After play: cards drawn or enters Calm depending on stance.
    """
    hand = [(sts_sim.Card.InnerPeace, True)]
    draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.InnerPeace,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_indignation_upgraded(game):
    """Indignation+ stays same (cost 1), enters Wrath or applies Vuln.

    Setup: Indignation+ in hand, energy=3.
    After play: verify player matches.
    """
    hand = [(sts_sim.Card.Indignation, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Indignation,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_swivel_upgraded_block(game):
    """Swivel+ gains 3 block (up from 2), costs 2.

    Setup: Swivel+ in hand, energy=3.
    After play: block=3, energy=1.
    """
    hand = [(sts_sim.Card.Swivel, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Swivel,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_perseverance_upgraded_block(game):
    """Perseverance+ gains 2 block (up from 1), magic stays 2, costs 1.

    Setup: Perseverance+ in hand, energy=3.
    After play: block=2, energy=2.
    """
    hand = [(sts_sim.Card.Perseverance, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Perseverance,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_pray_upgraded_magic(game):
    """Pray+ generates 2 miracles (up from 1), costs 1.

    Setup: Pray+ in hand, energy=3.
    After play: energy=2.
    """
    hand = [(sts_sim.Card.Pray, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Pray,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_prostrate_upgraded_block(game):
    """Prostrate+ gains 2 block (up from 1), costs 1.

    Setup: Prostrate+ in hand, energy=3.
    After play: block=2, energy=2.
    """
    hand = [(sts_sim.Card.Prostrate, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Prostrate,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_wreath_of_flame_upgraded_no_exhaust(game):
    """WreathOfFlameCard+ no longer exhausts, X-cost.

    Setup: WreathOfFlameCard+ in hand, energy=3.
    After play: energy=0, card in discard (not exhaust).
    """
    hand = [(sts_sim.Card.WreathOfFlameCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.WreathOfFlameCard,
                            upgraded=True, choices=[3])

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ===================================================================
# UNCOMMON POWERS
# ===================================================================


def test_battle_hymn_upgraded_magic(game):
    """BattleHymnCard+ magic 1->2, costs 1, power.

    Setup: BattleHymnCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.BattleHymnCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BattleHymnCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_simmering_fury_upgraded_magic(game):
    """SimmeringFuryCard+ magic 1->2, costs 2, power.

    Setup: SimmeringFuryCard+ in hand, energy=3.
    After play: energy=1, power applied.
    """
    hand = [(sts_sim.Card.SimmeringFuryCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SimmeringFuryCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_mental_fortress_upgraded_magic(game):
    """MentalFortressCard+ magic 1->2, costs 1, power.

    Setup: MentalFortressCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.MentalFortressCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.MentalFortressCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_nirvana_upgraded_magic(game):
    """NirvanaCard+ magic 1->2, costs 1, power.

    Setup: NirvanaCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.NirvanaCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.NirvanaCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_like_water_upgraded_magic(game):
    """LikeWaterCard+ magic 1->2, costs 1, power.

    Setup: LikeWaterCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.LikeWaterCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.LikeWaterCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_foresight_upgraded_magic(game):
    """ForesightCard+ magic 3->4, costs 1, power.

    Setup: ForesightCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.ForesightCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ForesightCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_study_upgraded_cost(game):
    """StudyCard+ costs 1 (down from 2), power.

    Setup: StudyCard+ in hand, energy=3.
    After play: energy=2 (cost 1).
    """
    hand = [(sts_sim.Card.StudyCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StudyCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert state.combat_state.player.energy == 2, (
        f"Expected 2 energy after StudyCard+ (cost 1), got {state.combat_state.player.energy}"
    )


def test_rushdown_upgraded_magic(game):
    """RushdownCard+ magic 2->3, costs 1, power.

    Setup: RushdownCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.RushdownCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.RushdownCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===================================================================
# RARE ATTACKS
# ===================================================================


def test_ragnarok_upgraded_magic(game):
    """Ragnarok+ hits 5 times (up from 4), damage 1, costs 3.

    Setup: Ragnarok+ in hand, monster at 30 HP, energy=3.
    After play: monster takes 1*5=5 damage.
    """
    hand = [(sts_sim.Card.Ragnarok, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Ragnarok,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_brilliance_upgraded_damage(game):
    """BrillianceCard+ deals 3 damage (up from 2), costs 1.

    Setup: BrillianceCard+ in hand, monster at 30 HP.
    After play: monster takes 3 base damage.
    """
    hand = [(sts_sim.Card.BrillianceCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BrillianceCard,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===================================================================
# RARE SKILLS
# ===================================================================


def test_blasphemy_upgraded_no_exhaust(game):
    """Blasphemy+ no longer exhausts, costs 2, enters Divinity.

    Setup: Blasphemy+ in hand, energy=3.
    After play: energy=1, card in discard (not exhaust).
    """
    hand = [(sts_sim.Card.Blasphemy, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Blasphemy,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_deus_ex_machina_upgraded_magic(game):
    """DeusExMachina+ generates 3 miracles (up from 2), costs 0, exhausts.

    Setup: DeusExMachina+ in hand, energy=3.
    After play: energy=3, card exhausted.
    """
    hand = [(sts_sim.Card.DeusExMachina, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DeusExMachina,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_omniscience_upgraded_cost(game):
    """OmniscienceCard+ costs 1 (down from 3), exhausts.

    Setup: OmniscienceCard+ + StrikePurple in hand, energy=3.
    After play: energy=2 (cost 1), card exhausted.
    """
    hand = [(sts_sim.Card.OmniscienceCard, True), sts_sim.Card.StrikePurple]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.OmniscienceCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_scrawl_upgraded_cost(game):
    """ScrawlCard+ costs 0 (down from 1), exhausts, draws.

    Setup: ScrawlCard+ in hand, 5 cards in draw pile, energy=3.
    After play: energy=3 (0 cost), cards drawn, card exhausted.
    """
    hand = [(sts_sim.Card.ScrawlCard, True)]
    draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ScrawlCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_vault_upgraded_cost(game):
    """VaultCard+ costs 1 (down from 3), exhausts.

    Setup: VaultCard+ in hand, energy=3.
    After play: energy=2 (cost 1), card exhausted.
    """
    hand = [(sts_sim.Card.VaultCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.VaultCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_wish_upgraded_block(game):
    """WishCard+ gains 15 block (up from 10), costs 3, exhausts.

    Setup: WishCard+ in hand, energy=3.
    After play: block matches sim, card exhausted.
    """
    hand = [(sts_sim.Card.WishCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    # Choose block option (choice 0)
    state = play_named_card(game, sim, setup, sts_sim.Card.WishCard,
                            upgraded=True, choices=[0])

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_spirit_shield_upgraded_no_exhaust(game):
    """SpiritShieldCard+ no longer exhausts, costs 2.

    Setup: SpiritShieldCard+ + Strike + Defend in hand, energy=3.
    After play: block matches sim, card in discard (not exhaust).
    """
    hand = [(sts_sim.Card.SpiritShieldCard, True), sts_sim.Card.StrikePurple,
            sts_sim.Card.DefendPurple]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SpiritShieldCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_judgment_upgraded_magic(game):
    """JudgmentCard+ magic 7->8 kill threshold, costs 1, targeted.

    Setup: JudgmentCard+ in hand, monster at 30 HP (above threshold).
    After play: monster survives (HP > 8).
    """
    hand = [(sts_sim.Card.JudgmentCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.JudgmentCard,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_worship_upgraded(game):
    """WorshipCard+ stays same, X-cost, exhausts.

    Setup: WorshipCard+ in hand, energy=3.
    After play: energy=0, card exhausted.
    """
    hand = [(sts_sim.Card.WorshipCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.WorshipCard,
                            upgraded=True, choices=[3])

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ===================================================================
# RARE POWERS
# ===================================================================


def test_omega_upgraded_magic(game):
    """OmegaCard+ magic 5->6, costs 3, power.

    Setup: OmegaCard+ in hand, energy=3.
    After play: energy=0, power applied.
    """
    hand = [(sts_sim.Card.OmegaCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.OmegaCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_deva_form_upgraded_magic(game):
    """DevaFormCard+ magic 1->2, costs 2, power.

    Setup: DevaFormCard+ in hand, energy=3.
    After play: energy=1, power applied.
    """
    hand = [(sts_sim.Card.DevaFormCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DevaFormCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_devotion_upgraded_magic(game):
    """DevotionCard+ magic 3->4, costs 1, power.

    Setup: DevotionCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.DevotionCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DevotionCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_establishment_upgraded_magic(game):
    """EstablishmentCard+ magic 1->2, costs 1, power.

    Setup: EstablishmentCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.EstablishmentCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.EstablishmentCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_conjure_blade_upgraded_magic(game):
    """ConjureBladeCard+ magic 1->2, X-cost, power.

    Setup: ConjureBladeCard+ in hand, energy=3.
    After play: energy=0, power applied.
    """
    hand = [(sts_sim.Card.ConjureBladeCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ConjureBladeCard,
                            upgraded=True, choices=[3])

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
