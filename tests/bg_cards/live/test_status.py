"""Live tests for Status cards.

Implemented statuses: Burn [Y], Dazed [Y], Slimed [Y], VoidCard [Y]
Not implemented: Desync [N]
"""
import pytest
import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches,
)


# ── Slimed [Y] ───────────────────────────────────────────────────────────


def test_slimed_plays_and_costs_energy(game):
    """Slimed costs 1 energy, does nothing, and exhausts.

    Setup: Slimed in hand, energy=3.
    After play: energy=2. Slimed disappears from exhaust
    (BG mod: CardDisappearsOnExhaust), so exhaust pile is empty.
    """
    hand = [sts_sim.Card.Slimed]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 2, (
        f"Expected 2 energy after Slimed (cost 1), got {state.combat_state.player.energy}"
    )


# ── Dazed [Y] ────────────────────────────────────────────────────────────


def test_dazed_in_hand_with_playable(game):
    """Dazed is unplayable and ethereal — verify it stays while playing other cards.

    Setup: Dazed + Strike in hand, monster at 30 HP.
    Play Strike, verify Dazed remains in hand.
    """
    hand = [sts_sim.Card.StrikeRed, sts_sim.Card.Dazed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StrikeRed,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


# ── Burn [Y] ─────────────────────────────────────────────────────────────


def test_burn_in_hand_with_playable(game):
    """Burn is unplayable — verify it stays in hand while other cards play.

    Setup: Burn + Strike in hand, monster at 30 HP.
    Play Strike, verify Burn remains in hand.
    """
    hand = [sts_sim.Card.StrikeRed, sts_sim.Card.Burn]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StrikeRed,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


# ── VoidCard [Y] ─────────────────────────────────────────────────────────


def test_void_card_draw_energy_loss(game):
    """VoidCard auto-plays when drawn, costing 1 energy, then exhausts and vanishes.

    Setup: PommelStrike in hand, VoidCard in draw pile, energy=3, monster=30.
    Play PommelStrike (cost 1, draws 1). Void drawn -> auto-plays (cost 1) -> exhausts -> vanishes.
    Expected energy: 3 - 1 (PommelStrike cost) - 1 (Void auto-play) = 1.
    """
    hand = [sts_sim.Card.PommelStrike]
    draw = [sts_sim.Card.VoidCard]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Desync [N] ───────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Desync not implemented in simulator")
def test_desync_unplayable(game):
    """Desync cannot be played (error indicator card)."""
    pass


@pytest.mark.skip(reason="Desync not implemented in simulator")
def test_desync_clogs_hand(game):
    """Desync takes up a hand slot when drawn."""
    pass
