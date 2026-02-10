"""Tier 3: Card draw & pile manipulation.

Tests verify that drawing cards, moving cards between piles, and exhaust
in the live game match the simulator.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
)


# ── Pommel Strike: damage + draw 1 ──────────────────────────────────────

def test_pommel_strike_damage_and_draw(game):
    """Pommel Strike deals damage and draws 1 card.

    Setup: Pommel Strike in hand, 1 Defend in draw pile.
    After play: monster takes damage, Defend drawn to hand,
    Pommel Strike in discard, draw pile empty.
    """
    hand = [sts_sim.Card.PommelStrike]
    draw = [sts_sim.Card.DefendRed]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=8)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=8)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Shrug It Off: block + draw 1 ────────────────────────────────────────

def test_shrug_it_off_block_and_draw(game):
    """Shrug It Off gains block and draws 1 card.

    Setup: Shrug It Off in hand, 1 Strike in draw pile.
    After play: player gains block, Strike drawn to hand,
    Shrug It Off in discard, draw pile empty.
    """
    hand = [sts_sim.Card.ShrugItOff]
    draw = [sts_sim.Card.StrikeRed]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3,
                 player_block=0, monster_hp=8)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3,
                   player_block=0, monster_hp=8)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)

    # Sanity: player should have gained block
    assert state.combat_state.player.block > 0, (
        "Player should have block from Shrug It Off"
    )


# ── Headbutt: damage + move discard to top of draw ──────────────────────

def test_headbutt_move_discard_to_draw(game):
    """Headbutt deals damage and puts a card from discard on draw pile.

    Setup: Headbutt in hand, 1 Defend in discard, empty draw pile.
    After play: monster takes damage, Defend moved from discard to draw pile,
    Headbutt in discard.
    """
    hand = [sts_sim.Card.Headbutt]
    discard = [sts_sim.Card.DefendRed]

    set_scenario(game, hand=hand, discard_pile=discard, energy=3, monster_hp=8)
    sim = make_sim(hand=hand, discard_pile=discard, energy=3, monster_hp=8)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Draw from empty draw pile reshuffles discard ─────────────────────────

def test_draw_reshuffles_discard(game):
    """When draw pile is empty, drawing reshuffles discard into draw pile.

    Setup: Pommel Strike in hand, empty draw pile, 1 Strike in discard.
    Pommel Strike draws 1 → triggers reshuffle → Strike drawn from
    reshuffled pile.
    """
    hand = [sts_sim.Card.PommelStrike]
    discard = [sts_sim.Card.StrikeRed]

    set_scenario(game, hand=hand, discard_pile=discard, energy=3, monster_hp=8)
    sim = make_sim(hand=hand, discard_pile=discard, energy=3, monster_hp=8)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    # After reshuffle: the Strike was drawn to hand, Pommel Strike went to discard
    assert_discard_matches(state, sim)


# ── Seeing Red: exhaust + gain energy ────────────────────────────────────

def test_seeing_red_exhaust_and_energy(game):
    """Seeing Red exhausts itself and gains 2 energy.

    Setup: Seeing Red in hand with 1 energy (cost 1).
    After play: 0+2=2 energy remaining, card exhausted (not in discard).
    """
    hand = [sts_sim.Card.SeeingRed]

    set_scenario(game, hand=hand, energy=1, monster_hp=8)
    sim = make_sim(hand=hand, energy=1, monster_hp=8)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)

    # Sanity: should have gained energy (1 - 1 cost + 2 = 2)
    assert state.combat_state.player.energy == 2, (
        f"Expected 2 energy after Seeing Red, got {state.combat_state.player.energy}"
    )
