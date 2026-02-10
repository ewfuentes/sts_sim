"""Tier 4: Exhaust & conditional cards.

Tests verify exhaust mechanics, dynamic damage (Body Slam), and
card playability conditions (Clash) match between live game and simulator.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_discard_matches, assert_exhaust_matches,
)


# ── Body Slam: damage equals player block ────────────────────────────────

def test_body_slam_damage_equals_block(game):
    """Body Slam deals damage equal to current block.

    Setup: Body Slam in hand, player has 5 block, monster at 8 HP.
    After play: monster takes 5 damage (= player block).
    """
    hand = [sts_sim.Card.BodySlam]

    set_scenario(game, hand=hand, energy=3, player_block=5, monster_hp=8)
    sim = make_sim(hand=hand, energy=3, player_block=5, monster_hp=8)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── True Grit: block + exhaust a card from hand ─────────────────────────

def test_true_grit_block_and_exhaust(game):
    """True Grit gains block and exhausts 1 random card from hand.

    Setup: True Grit + Strike in hand (2 cards). Play True Grit.
    After play: block gained, Strike exhausted, True Grit in discard.
    With only 1 card remaining in hand when exhaust triggers, the
    choice is deterministic.
    """
    hand = [sts_sim.Card.TrueGrit, sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=8)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=8)

    state = play_named_card(game, sim, setup, sts_sim.Card.TrueGrit)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)

    # Sanity: player should have gained block
    assert state.combat_state.player.block > 0, (
        "Player should have block from True Grit"
    )


# ── Clash: only playable when hand is all attacks ────────────────────────

def test_clash_all_attacks(game):
    """Clash deals damage when hand is all attacks.

    Setup: Clash + Strike in hand (both attacks). Play Clash.
    After play: monster takes damage.
    """
    hand = [sts_sim.Card.Clash, sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=8)
    sim = make_sim(hand=hand, energy=3, monster_hp=8)

    state = play_named_card(game, sim, setup, sts_sim.Card.Clash, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)
