"""Tier 10: Rare cards and power cards.

Tests verify rare card mechanics match between live game and simulator.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_discard_matches, assert_exhaust_matches,
)


# ── Bludgeon: heavy damage ───────────────────────────────────────────────

def test_bludgeon_heavy_damage(game):
    """Bludgeon deals 7 damage, costs 3 energy.

    Setup: Bludgeon in hand, 3 energy, monster at 30 HP.
    After play: monster at 23, energy=0.
    """
    hand = [sts_sim.Card.Bludgeon]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Impervious: big block, exhaust ───────────────────────────────────────

def test_impervious_big_block(game):
    """Impervious gives 5 block, costs 2 energy, exhausts.

    Setup: Impervious in hand, 3 energy.
    After play: block=5, energy=1, Impervious exhausted.
    """
    hand = [sts_sim.Card.Impervious]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Metallicize: power card ──────────────────────────────────────────────

def test_metallicize_power(game):
    """Metallicize is a power card that costs 1 energy.

    Setup: Metallicize in hand, 3 energy.
    After play: energy=2, discard empty (power cards removed from play).
    """
    hand = [sts_sim.Card.Metallicize]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Offering: HP loss, energy gain, draw ─────────────────────────────────

def test_offering_hp_energy_draw(game):
    """Offering loses 1 HP, gains 2 energy, draws 3 cards, exhausts.

    Setup: Offering in hand, 3 Strikes in draw pile, 1 energy, 9 HP.
    After play: HP=8, energy=3 (1+2), 3 cards drawn, Offering exhausted.
    """
    hand = [sts_sim.Card.Offering]
    draw = [sts_sim.Card.StrikeRed, sts_sim.Card.DefendRed,
            sts_sim.Card.StrikeRed]

    set_scenario(game, hand=hand, draw_pile=draw, energy=1,
                 player_hp=9, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=1,
                   player_hp=9, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)
