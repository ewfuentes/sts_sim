"""Live tests for Ironclad Rare cards."""
import sts_sim
from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_discard_matches, assert_exhaust_matches,
)


# ── Bludgeon ─────────────────────────────────────────────────────────────

def test_bludgeon_base(game):
    """Bludgeon deals 7 damage."""
    hand = [sts_sim.Card.Bludgeon]
    set_scenario(game, hand=hand, energy=3, monster_hp=15)
    sim = make_sim(hand=hand, energy=3, monster_hp=15)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_bludgeon_upgraded(game):
    """Upgraded Bludgeon deals 10 damage."""
    hand = [(sts_sim.Card.Bludgeon, True)]
    set_scenario(game, hand=hand, energy=3, monster_hp=15)
    sim = make_sim(hand=hand, energy=3, monster_hp=15)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_bludgeon_with_strength(game):
    """Bludgeon with 2 STR deals 21 damage."""
    hand = [sts_sim.Card.Bludgeon]
    set_scenario(game, hand=hand, energy=3, monster_hp=30,
                 player_powers={"Strength": 2})
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   player_powers={"Strength": 2})
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Impervious ───────────────────────────────────────────────────────────

def test_impervious_base(game):
    """Impervious grants 6 block and exhausts."""
    hand = [sts_sim.Card.Impervious]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_impervious_upgraded(game):
    """Upgraded Impervious grants 8 block."""
    hand = [(sts_sim.Card.Impervious, True)]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_impervious_stacks(game):
    """Impervious block stacks with existing block."""
    hand = [sts_sim.Card.Impervious]
    set_scenario(game, hand=hand, energy=3, player_block=4, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, player_block=4, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Offering ─────────────────────────────────────────────────────────────

def test_offering_base(game):
    """Offering costs HP, gains energy, draws cards, and exhausts."""
    hand = [sts_sim.Card.Offering]
    draw = [sts_sim.Card.StrikeRed] * 5
    set_scenario(game, hand=hand, draw_pile=draw, energy=0, player_hp=9, monster_hp=20)
    sim = make_sim(hand=hand, draw_pile=draw, energy=0, player_hp=9, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert_hand_matches(state, sim)


def test_offering_upgraded(game):
    """Upgraded Offering draws 5 cards."""
    hand = [(sts_sim.Card.Offering, True)]
    draw = [sts_sim.Card.StrikeRed] * 6
    set_scenario(game, hand=hand, draw_pile=draw, energy=0, player_hp=9, monster_hp=20)
    sim = make_sim(hand=hand, draw_pile=draw, energy=0, player_hp=9, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert_hand_matches(state, sim)


# ── Barricade ────────────────────────────────────────────────────────────

def test_barricade_base(game):
    """Barricade costs 2 energy to play."""
    hand = [sts_sim.Card.Barricade]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_barricade_upgraded(game):
    """Upgraded Barricade costs 1 energy."""
    hand = [(sts_sim.Card.Barricade, True)]
    set_scenario(game, hand=hand, energy=1, monster_hp=20)
    sim = make_sim(hand=hand, energy=1, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ── Berserk ──────────────────────────────────────────────────────────────

def test_berserk_base(game):
    """Berserk costs 1 energy to play."""
    hand = [sts_sim.Card.BerserkCard]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ── Corruption ───────────────────────────────────────────────────────────

def test_corruption_base(game):
    """Corruption costs 3 energy to play."""
    hand = [sts_sim.Card.Corruption]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_corruption_upgraded(game):
    """Upgraded Corruption costs 2 energy."""
    hand = [(sts_sim.Card.Corruption, True)]
    set_scenario(game, hand=hand, energy=2, monster_hp=20)
    sim = make_sim(hand=hand, energy=2, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ── Demon Form ───────────────────────────────────────────────────────────

def test_demon_form_base(game):
    """Demon Form costs 3 energy to play."""
    hand = [sts_sim.Card.DemonForm]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_demon_form_upgraded(game):
    """Upgraded Demon Form costs 2 energy."""
    hand = [(sts_sim.Card.DemonForm, True)]
    set_scenario(game, hand=hand, energy=2, monster_hp=20)
    sim = make_sim(hand=hand, energy=2, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ── Double Tap ───────────────────────────────────────────────────────────

def test_double_tap_base(game):
    """Double Tap causes next Attack to play twice."""
    hand = [sts_sim.Card.DoubleTap, sts_sim.Card.StrikeRed]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, energy=3, monster_hp=10)
    # Play Double Tap first
    play_named_card(game, sim, setup, sts_sim.Card.DoubleTap)
    # Need fresh state for second card
    import time
    time.sleep(0.5)
    game.request_state()
    state2 = game.wait_for_state(timeout=10.0)
    # Play Strike
    state = play_named_card(game, sim, state2, sts_sim.Card.StrikeRed,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_double_tap_upgraded(game):
    """Upgraded Double Tap costs 0 energy."""
    hand = [(sts_sim.Card.DoubleTap, True), sts_sim.Card.StrikeRed]
    setup = set_scenario(game, hand=hand, energy=2, monster_hp=10)
    sim = make_sim(hand=hand, energy=2, monster_hp=10)
    play_named_card(game, sim, setup, sts_sim.Card.DoubleTap, upgraded=True)
    import time
    time.sleep(0.5)
    game.request_state()
    state2 = game.wait_for_state(timeout=10.0)
    state = play_named_card(game, sim, state2, sts_sim.Card.StrikeRed,
                            target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Exhume ───────────────────────────────────────────────────────────────
# Exhume requires exhaust pile setup which is complex for live tests.
# See to_implement notes.


# ── Feed ─────────────────────────────────────────────────────────────────

def test_feed_no_kill(game):
    """Feed does not grant STR if enemy survives."""
    hand = [sts_sim.Card.Feed]
    set_scenario(game, hand=hand, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, energy=3, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Fiend Fire ───────────────────────────────────────────────────────────

def test_fiend_fire_base(game):
    """Fiend Fire exhausts hand and deals damage per card."""
    hand = [
        sts_sim.Card.FiendFire,
        sts_sim.Card.StrikeRed,
        sts_sim.Card.DefendRed,
        sts_sim.Card.Bash,
    ]
    set_scenario(game, hand=hand, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, energy=3, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_fiend_fire_empty_hand(game):
    """Fiend Fire with empty hand deals 0 damage."""
    hand = [sts_sim.Card.FiendFire]
    set_scenario(game, hand=hand, energy=2, monster_hp=10)
    sim = make_sim(hand=hand, energy=2, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_exhaust_matches(state, sim)


def test_fiend_fire_upgraded(game):
    """Upgraded Fiend Fire deals 2 HIT per card exhausted."""
    hand = [
        (sts_sim.Card.FiendFire, True),
        sts_sim.Card.StrikeRed,
        sts_sim.Card.DefendRed,
    ]
    set_scenario(game, hand=hand, energy=3, monster_hp=15)
    sim = make_sim(hand=hand, energy=3, monster_hp=15)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_exhaust_matches(state, sim)


def test_fiend_fire_with_strength(game):
    """Fiend Fire with Strength scales per HIT."""
    hand = [
        sts_sim.Card.FiendFire,
        sts_sim.Card.StrikeRed,
        sts_sim.Card.DefendRed,
        sts_sim.Card.Bash,
    ]
    set_scenario(game, hand=hand, energy=3, monster_hp=20,
                 player_powers={"Strength": 2})
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   player_powers={"Strength": 2})
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Immolate ─────────────────────────────────────────────────────────────

def test_immolate_base(game):
    """Immolate deals 5 AOE damage and adds 2 DAZED."""
    hand = [sts_sim.Card.Immolate]
    set_scenario(game, hand=hand, energy=3,
                 monsters=[{"hp": 10}, {"hp": 10}])
    sim = make_sim(hand=hand, energy=3,
                   monsters=[{"hp": 10}, {"hp": 10}])
    state = play_card_both(game, sim, hand_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_immolate_upgraded(game):
    """Upgraded Immolate deals 7 AOE damage."""
    hand = [(sts_sim.Card.Immolate, True)]
    set_scenario(game, hand=hand, energy=3,
                 monsters=[{"hp": 10}, {"hp": 10}])
    sim = make_sim(hand=hand, energy=3,
                   monsters=[{"hp": 10}, {"hp": 10}])
    state = play_card_both(game, sim, hand_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_immolate_with_strength(game):
    """Immolate with 1 STR deals 10 damage."""
    hand = [sts_sim.Card.Immolate]
    set_scenario(game, hand=hand, energy=3, monster_hp=15,
                 player_powers={"Strength": 1})
    sim = make_sim(hand=hand, energy=3, monster_hp=15,
                   player_powers={"Strength": 1})
    state = play_card_both(game, sim, hand_index=0)
    assert_monsters_match(state, sim)
    assert_discard_matches(state, sim)


# ── Juggernaut ───────────────────────────────────────────────────────────

def test_juggernaut_on_block_gain(game):
    """Juggernaut deals 1 damage when gaining block."""
    hand = [sts_sim.Card.DefendRed]
    set_scenario(game, hand=hand, energy=3, monster_hp=10,
                 player_powers={"Juggernaut": 1})
    sim = make_sim(hand=hand, energy=3, monster_hp=10,
                   player_powers={"Juggernaut": 1})
    state = play_card_both(game, sim, hand_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Limit Break ──────────────────────────────────────────────────────────

def test_limit_break_base(game):
    """Limit Break doubles STR and exhausts."""
    hand = [sts_sim.Card.LimitBreak]
    set_scenario(game, hand=hand, energy=3, monster_hp=20,
                 player_powers={"Strength": 2})
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   player_powers={"Strength": 2})
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_limit_break_cap(game):
    """Limit Break respects 8 STR cap."""
    hand = [sts_sim.Card.LimitBreak]
    set_scenario(game, hand=hand, energy=3, monster_hp=20,
                 player_powers={"Strength": 5})
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   player_powers={"Strength": 5})
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_limit_break_zero_str(game):
    """Limit Break with 0 STR does nothing."""
    hand = [sts_sim.Card.LimitBreak]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_limit_break_upgraded(game):
    """Upgraded Limit Break does not exhaust."""
    hand = [(sts_sim.Card.LimitBreak, True)]
    set_scenario(game, hand=hand, energy=3, monster_hp=20,
                 player_powers={"Strength": 3})
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   player_powers={"Strength": 3})
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
