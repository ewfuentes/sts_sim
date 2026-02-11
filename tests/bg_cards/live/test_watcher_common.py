"""Live tests for Watcher Common cards.

Tests verify that the live BG mod game and Rust simulator agree on card
effects for Watcher common cards: Flurry of Blows, Empty Fist, Consecrate,
Cut Through Fate, Just Lucky, Flying Sleeves, Empty Body, Protect, Halt,
Third Eye, Tranquility, Crescendo, and Collect.

For stance-dependent tests, stance-changing cards are placed in hand and
played sequentially before the card under test.
"""
import sts_sim
from tests.live.conftest import (
    set_scenario, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_discard_matches, assert_exhaust_matches,
    CARD_TO_BG,
    _card_spec_card, _card_spec_upgraded,
)


# ---------------------------------------------------------------------------
# Local helper: make_sim variant that uses Character.Watcher
# ---------------------------------------------------------------------------

def make_watcher_sim(*, hand=None, draw_pile=None, discard_pile=None,
                     energy=3, player_hp=9, player_block=0,
                     player_powers=None, player_relics=None,
                     monster_hp=30, monster_block=0, monster_powers=None,
                     monsters=None):
    """Create a simulator CombatState with Character.Watcher."""
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

    sim.set_die_value(1)
    return sim


# =========================================================================
# Flurry of Blows
# =========================================================================

def test_flurry_of_blows_no_stance_switch(game):
    """Flurry of Blows without stance switch deals 1 damage."""
    hand = [sts_sim.Card.FlurryOfBlows]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_flurry_of_blows_with_stance_switch(game):
    """Flurry of Blows after Crescendo stance switch (in Wrath)."""
    hand = [sts_sim.Card.Crescendo, sts_sim.Card.FlurryOfBlows]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    # Enter Wrath
    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
    # Play Flurry of Blows (with stance switch bonus + Wrath)
    state = play_named_card(game, sim, state, sts_sim.Card.FlurryOfBlows,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_flurry_of_blows_upgraded_with_stance_switch(game):
    """Upgraded Flurry of Blows after stance switch in Wrath."""
    hand = [sts_sim.Card.Crescendo, (sts_sim.Card.FlurryOfBlows, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
    state = play_named_card(game, sim, state, sts_sim.Card.FlurryOfBlows,
                            target_index=0, upgraded=True)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# =========================================================================
# Empty Fist
# =========================================================================

def test_empty_fist_from_wrath(game):
    """Empty Fist from Wrath deals doubled damage and exits to Neutral."""
    hand = [sts_sim.Card.Crescendo, sts_sim.Card.EmptyFist]
    setup = set_scenario(game, hand=hand, energy=5, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=5, monster_hp=20)
    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
    state = play_named_card(game, sim, state, sts_sim.Card.EmptyFist,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_empty_fist_from_calm(game):
    """Empty Fist from Calm grants 2 energy and enters Neutral."""
    hand = [sts_sim.Card.Vigilance, sts_sim.Card.EmptyFist]
    setup = set_scenario(game, hand=hand, energy=5, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=5, monster_hp=20)
    state = play_named_card(game, sim, setup, sts_sim.Card.Vigilance)
    state = play_named_card(game, sim, state, sts_sim.Card.EmptyFist,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_empty_fist_upgraded(game):
    """Upgraded Empty Fist deals 3 HIT."""
    hand = [(sts_sim.Card.EmptyFist, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_empty_fist_from_neutral(game):
    """Empty Fist from Neutral stays in Neutral."""
    hand = [sts_sim.Card.EmptyFist]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# =========================================================================
# Consecrate
# =========================================================================

def test_consecrate_aoe(game):
    """Consecrate hits all enemies for 1 damage."""
    hand = [sts_sim.Card.Consecrate]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_consecrate_in_wrath(game):
    """Consecrate in Wrath deals doubled AOE damage."""
    hand = [sts_sim.Card.Crescendo, sts_sim.Card.Consecrate]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
    state = play_named_card(game, sim, state, sts_sim.Card.Consecrate)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_consecrate_upgraded(game):
    """Upgraded Consecrate deals 2 HIT AOE."""
    hand = [(sts_sim.Card.Consecrate, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# =========================================================================
# Cut Through Fate
# =========================================================================

def test_cut_through_fate_base(game):
    """Cut Through Fate deals 1 damage, scries, and draws."""
    draw = [sts_sim.Card.StrikePurple] * 5
    hand = [sts_sim.Card.CutThroughFate]
    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_cut_through_fate_upgraded(game):
    """Upgraded Cut Through Fate deals 2 damage and scries 3."""
    draw = [sts_sim.Card.StrikePurple] * 5
    hand = [(sts_sim.Card.CutThroughFate, True)]
    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_cut_through_fate_in_wrath(game):
    """Cut Through Fate in Wrath doubles damage."""
    draw = [sts_sim.Card.StrikePurple] * 5
    hand = [sts_sim.Card.Crescendo, sts_sim.Card.CutThroughFate]
    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
    state = play_named_card(game, sim, state, sts_sim.Card.CutThroughFate,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# =========================================================================
# Just Lucky
# =========================================================================

def test_just_lucky_base(game):
    """Just Lucky deals damage (die=1: low roll -> scry path)."""
    draw = [sts_sim.Card.StrikePurple] * 5
    hand = [sts_sim.Card.JustLucky]
    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    # Die is set to 1 by default (low roll)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# NOTE: Testing specific die rolls (high vs low) in live requires the
# set_scenario die parameter. The default die=1 gives a low roll.
# High roll tests would need die=4+ which requires set_scenario modification.
# See to_implement notes.


# =========================================================================
# Flying Sleeves
# =========================================================================

def test_flying_sleeves_base(game):
    """Flying Sleeves deals 2 damage in two hits."""
    hand = [sts_sim.Card.FlyingSleeves]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_flying_sleeves_upgraded(game):
    """Upgraded Flying Sleeves deals 3 damage in three hits."""
    hand = [(sts_sim.Card.FlyingSleeves, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_flying_sleeves_with_strength(game):
    """Flying Sleeves with 2 Strength: each HIT gets +2."""
    hand = [sts_sim.Card.FlyingSleeves]
    powers = {"Strength": 2}
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                         player_powers=powers)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20,
                           player_powers=powers)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# NOTE: Flying Sleeves retain test requires end-of-turn verification which
# is complex in live testing. See to_implement notes.


# =========================================================================
# Empty Body
# =========================================================================

def test_empty_body_from_wrath(game):
    """Empty Body from Wrath grants 2 block and enters Neutral."""
    hand = [sts_sim.Card.Crescendo, sts_sim.Card.EmptyBody]
    setup = set_scenario(game, hand=hand, energy=5, player_block=0, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=5, player_block=0, monster_hp=20)
    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
    state = play_named_card(game, sim, state, sts_sim.Card.EmptyBody)
    assert_player_matches(state, sim)


def test_empty_body_from_calm(game):
    """Empty Body from Calm grants energy and enters Neutral."""
    hand = [sts_sim.Card.Vigilance, sts_sim.Card.EmptyBody]
    setup = set_scenario(game, hand=hand, energy=5, player_block=0, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=5, player_block=0, monster_hp=20)
    state = play_named_card(game, sim, setup, sts_sim.Card.Vigilance)
    state = play_named_card(game, sim, state, sts_sim.Card.EmptyBody)
    assert_player_matches(state, sim)


def test_empty_body_upgraded(game):
    """Upgraded Empty Body grants 3 block."""
    hand = [sts_sim.Card.Crescendo, (sts_sim.Card.EmptyBody, True)]
    setup = set_scenario(game, hand=hand, energy=5, player_block=0, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=5, player_block=0, monster_hp=20)
    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
    state = play_named_card(game, sim, state, sts_sim.Card.EmptyBody,
                            upgraded=True)
    assert_player_matches(state, sim)


# =========================================================================
# Protect
# =========================================================================

def test_protect_base(game):
    """Protect grants 3 block."""
    hand = [sts_sim.Card.Protect]
    setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_protect_upgraded(game):
    """Upgraded Protect grants 4 block."""
    hand = [(sts_sim.Card.Protect, True)]
    setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# NOTE: Protect retain test requires end-of-turn verification.
# See to_implement notes.


# =========================================================================
# Halt
# =========================================================================

def test_halt_neutral(game):
    """Halt in Neutral grants 1 block."""
    hand = [sts_sim.Card.Halt]
    setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_halt_in_wrath(game):
    """Halt in Wrath grants 2 block (1 base + 1 Wrath bonus)."""
    hand = [sts_sim.Card.Crescendo, sts_sim.Card.Halt]
    setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
    state = play_named_card(game, sim, state, sts_sim.Card.Halt)
    assert_player_matches(state, sim)


def test_halt_upgraded_in_wrath(game):
    """Upgraded Halt in Wrath grants 3 block (1 base + 2 Wrath bonus)."""
    hand = [sts_sim.Card.Crescendo, (sts_sim.Card.Halt, True)]
    setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
    state = play_named_card(game, sim, state, sts_sim.Card.Halt, upgraded=True)
    assert_player_matches(state, sim)


def test_halt_in_calm(game):
    """Halt in Calm grants only 1 block (no Wrath bonus)."""
    hand = [sts_sim.Card.Tranquility, sts_sim.Card.Halt]
    setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
    state = play_named_card(game, sim, setup, sts_sim.Card.Tranquility)
    state = play_named_card(game, sim, state, sts_sim.Card.Halt)
    assert_player_matches(state, sim)


# =========================================================================
# Third Eye
# =========================================================================

def test_third_eye_base(game):
    """Third Eye grants 2 block and scries 3."""
    draw = [sts_sim.Card.StrikePurple] * 5
    hand = [sts_sim.Card.ThirdEye]
    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3,
                         player_block=0, monster_hp=20)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3,
                           player_block=0, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_third_eye_upgraded(game):
    """Upgraded Third Eye grants 3 block and scries 5."""
    draw = [sts_sim.Card.StrikePurple] * 6
    hand = [(sts_sim.Card.ThirdEye, True)]
    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3,
                         player_block=0, monster_hp=20)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3,
                           player_block=0, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# NOTE: Third Eye scry discard test requires specific scry choice handling
# in the live game. See to_implement notes.


# =========================================================================
# Tranquility
# =========================================================================

def test_tranquility_base(game):
    """Tranquility enters Calm and exhausts."""
    hand = [sts_sim.Card.Tranquility]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_tranquility_upgraded(game):
    """Upgraded Tranquility costs 0 energy."""
    hand = [(sts_sim.Card.Tranquility, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_tranquility_from_wrath(game):
    """Tranquility from Wrath exits Wrath and enters Calm."""
    hand = [sts_sim.Card.Crescendo, sts_sim.Card.Tranquility]
    setup = set_scenario(game, hand=hand, energy=5, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=5, monster_hp=20)
    state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
    state = play_named_card(game, sim, state, sts_sim.Card.Tranquility)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# NOTE: Tranquility retain test requires end-of-turn verification.
# See to_implement notes.


# =========================================================================
# Crescendo
# =========================================================================

def test_crescendo_base(game):
    """Crescendo enters Wrath and exhausts."""
    hand = [sts_sim.Card.Crescendo]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_crescendo_from_calm(game):
    """Crescendo from Calm grants 2 energy on exit and enters Wrath."""
    hand = [sts_sim.Card.Tranquility, sts_sim.Card.Crescendo]
    setup = set_scenario(game, hand=hand, energy=5, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=5, monster_hp=20)
    state = play_named_card(game, sim, setup, sts_sim.Card.Tranquility)
    state = play_named_card(game, sim, state, sts_sim.Card.Crescendo)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_crescendo_upgraded_draws(game):
    """Upgraded Crescendo draws 1 card after entering Wrath."""
    draw = [sts_sim.Card.StrikePurple] * 5
    hand = [(sts_sim.Card.Crescendo, True)]
    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert_hand_matches(state, sim)


# NOTE: Crescendo retain test requires end-of-turn verification.
# See to_implement notes.


# =========================================================================
# Collect
# =========================================================================

def test_collect_base(game):
    """Collect generates 2 miracles and exhausts."""
    hand = [sts_sim.Card.Collect]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_collect_upgraded(game):
    """Upgraded Collect generates 3 miracles."""
    hand = [(sts_sim.Card.Collect, True)]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# NOTE: Miracle spending tests and Collect->Miracle->Eruption chain tests
# require multi-step card play with generated Miracle cards. The live game
# handles Miracles differently (as actual cards in hand) from the sim
# (MiracleCount power). See to_implement notes.
