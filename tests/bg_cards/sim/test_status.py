"""Simulator tests for Status cards.

Implemented statuses: Burn [Y], Dazed [Y], Slimed [Y], VoidCard [Y]
Not implemented: Desync [N]
"""
import pytest
import sts_sim
from tests.live.conftest import make_sim


# ── Burn [Y] ─────────────────────────────────────────────────────────────


def test_burn_unplayable():
    """Burn cannot be played (Unplayable, cost -2)."""
    sim = make_sim(hand=[sts_sim.Card.Burn], energy=3, monster_hp=20)
    result = sim.play_card(0)
    assert result is False, "Burn should not be playable"


def test_burn_in_hand_with_strike():
    """Strike is playable when Burn is in hand."""
    sim = make_sim(hand=[sts_sim.Card.StrikeRed, sts_sim.Card.Burn],
                   energy=3, monster_hp=20)
    result = sim.play_card(0, 0)
    assert result is True, "Strike should be playable alongside Burn"
    monsters = sim.get_monsters()
    assert monsters[0].hp < 20, "Strike should deal damage"


def test_burn_stays_in_hand():
    """Burn remains in hand after failed play attempt."""
    sim = make_sim(hand=[sts_sim.Card.Burn], energy=3, monster_hp=20)
    sim.play_card(0)
    hand = sim.get_hand()
    has_burn = any(c.card == sts_sim.Card.Burn for c in hand)
    assert has_burn, "Burn should remain in hand after failed play"


# ── Dazed [Y] ────────────────────────────────────────────────────────────


def test_dazed_unplayable():
    """Dazed cannot be played (Unplayable)."""
    sim = make_sim(hand=[sts_sim.Card.Dazed], energy=3, monster_hp=20)
    result = sim.play_card(0)
    assert result is False, "Dazed should not be playable"


def test_dazed_in_hand_with_strike():
    """Strike is playable when Dazed is in hand."""
    sim = make_sim(hand=[sts_sim.Card.StrikeRed, sts_sim.Card.Dazed],
                   energy=3, monster_hp=20)
    result = sim.play_card(0, 0)
    assert result is True, "Strike should be playable alongside Dazed"


def test_dazed_stays_in_hand():
    """Dazed remains in hand after failed play attempt."""
    sim = make_sim(hand=[sts_sim.Card.Dazed], energy=3, monster_hp=20)
    sim.play_card(0)
    hand = sim.get_hand()
    has_dazed = any(c.card == sts_sim.Card.Dazed for c in hand)
    assert has_dazed, "Dazed should remain in hand after failed play"


# ── Slimed [Y] ───────────────────────────────────────────────────────────


def test_slimed_plays_and_exhausts():
    """Slimed costs 1 energy and exhausts when played."""
    sim = make_sim(hand=[sts_sim.Card.Slimed], energy=3, monster_hp=20)
    result = sim.play_card(0)
    assert result is True, "Slimed should be playable"
    assert sim.player.energy == 2, "Slimed should cost 1 energy"
    hand = sim.get_hand()
    assert len(hand) == 0, "Slimed should be removed from hand"


def test_slimed_not_enough_energy():
    """Slimed cannot be played with 0 energy."""
    sim = make_sim(hand=[sts_sim.Card.Slimed], energy=0, monster_hp=20)
    result = sim.play_card(0)
    assert result is False, "Slimed should not be playable with 0 energy"
    hand = sim.get_hand()
    has_slimed = any(c.card == sts_sim.Card.Slimed for c in hand)
    assert has_slimed, "Slimed should remain in hand"


def test_slimed_in_hand_with_strike():
    """Strike is playable alongside Slimed."""
    sim = make_sim(hand=[sts_sim.Card.StrikeRed, sts_sim.Card.Slimed],
                   energy=3, monster_hp=20)
    result = sim.play_card(0, 0)
    assert result is True, "Strike should be playable alongside Slimed"


# ── Void [Y] ─────────────────────────────────────────────────────────────


def test_void_unplayable():
    """VoidCard cannot be played from hand (cost -2, Unplayable in sim).

    Note: In the BG mod, VoidCard auto-plays when drawn. The simulator
    models it as unplayable (cost -2) — the auto-exhaust-on-draw behavior
    is handled by the BG mod layer, not the sim.
    """
    sim = make_sim(hand=[sts_sim.Card.VoidCard], energy=3, monster_hp=20)
    result = sim.play_card(0)
    assert result is False, "VoidCard should not be playable (cost -2)"


def test_void_draw_costs_energy():
    """VoidCard drawn via PommelStrike costs 1 energy on draw.

    The sim deducts 1 energy when VoidCard is drawn, matching the BG mod
    behavior. VoidCard remains in hand (sim does not auto-exhaust it).
    PommelStrike costs 1 + Void draw costs 1 = 2 energy spent total.
    """
    sim = make_sim(
        hand=[sts_sim.Card.PommelStrike],
        draw_pile=[sts_sim.Card.VoidCard],
        energy=3,
        monster_hp=20,
    )
    result = sim.play_card(0, 0)  # PommelStrike draws 1 card (VoidCard)
    assert result is True
    # PommelStrike costs 1, Void draw costs 1 = 1 energy remaining
    assert sim.player.energy == 1, (
        f"Expected 1 energy (3 - 1 PommelStrike - 1 Void), got {sim.player.energy}"
    )
    # Void remains in hand in the sim (not auto-exhausted)
    hand = sim.get_hand()
    has_void = any(c.card == sts_sim.Card.VoidCard for c in hand)
    assert has_void, "VoidCard should be in hand after draw in sim"


# ── Desync [N] ───────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Desync not implemented in simulator")
def test_desync_unplayable():
    """Desync cannot be played (error indicator card)."""
    pass


@pytest.mark.skip(reason="Desync not implemented in simulator")
def test_desync_clogs_hand():
    """Desync takes up a hand slot when drawn."""
    pass
