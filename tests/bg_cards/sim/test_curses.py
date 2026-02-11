"""Simulator tests for Curse cards.

Implemented curses: AscendersBane [Y], Decay [Y], Injury [Y], Pain [Y]
Not implemented: Clumsy [N], Doubt [N], Parasite [N], Regret [N], Shame [N], Writhe [N]
"""
import pytest
import sts_sim
from tests.live.conftest import make_sim


# ── Ascender's Bane [Y] ─────────────────────────────────────────────────


def test_ascenders_bane_unplayable():
    """Ascender's Bane cannot be played (cost -2, Unplayable)."""
    sim = make_sim(hand=[sts_sim.Card.AscendersBane], energy=3, monster_hp=20)
    result = sim.play_card(0)
    assert result is False, "AscendersBane should not be playable"


def test_ascenders_bane_stays_in_hand():
    """Ascender's Bane remains in hand after attempting to play."""
    sim = make_sim(hand=[sts_sim.Card.AscendersBane, sts_sim.Card.StrikeRed],
                   energy=3, monster_hp=20)
    # Try to play AscendersBane — should fail
    sim.play_card(0)
    hand = sim.get_hand()
    has_bane = any(c.card == sts_sim.Card.AscendersBane for c in hand)
    assert has_bane, "AscendersBane should remain in hand after failed play"


def test_ascenders_bane_in_hand_with_strike():
    """Strike is still playable when AscendersBane is in hand."""
    sim = make_sim(hand=[sts_sim.Card.StrikeRed, sts_sim.Card.AscendersBane],
                   energy=3, monster_hp=20)
    result = sim.play_card(0, 0)  # Play Strike targeting monster 0
    assert result is True, "Strike should be playable alongside AscendersBane"
    monsters = sim.get_monsters()
    assert monsters[0].hp < 20, "Strike should deal damage"


# ── Decay [Y] ────────────────────────────────────────────────────────────


def test_decay_unplayable():
    """Decay cannot be played (Unplayable)."""
    sim = make_sim(hand=[sts_sim.Card.Decay], energy=3, monster_hp=20)
    result = sim.play_card(0)
    assert result is False, "Decay should not be playable"


def test_decay_in_hand_with_strike():
    """Strike is playable when Decay is in hand."""
    sim = make_sim(hand=[sts_sim.Card.StrikeRed, sts_sim.Card.Decay],
                   energy=3, monster_hp=20)
    result = sim.play_card(0, 0)
    assert result is True, "Strike should be playable alongside Decay"


# ── Injury [Y] ───────────────────────────────────────────────────────────


def test_injury_unplayable():
    """Injury cannot be played (Unplayable)."""
    sim = make_sim(hand=[sts_sim.Card.Injury], energy=3, monster_hp=20)
    result = sim.play_card(0)
    assert result is False, "Injury should not be playable"


def test_injury_in_hand_with_strike():
    """Strike is playable when Injury is in hand."""
    sim = make_sim(hand=[sts_sim.Card.StrikeRed, sts_sim.Card.Injury],
                   energy=3, monster_hp=20)
    result = sim.play_card(0, 0)
    assert result is True, "Strike should be playable alongside Injury"


def test_injury_stays_in_hand():
    """Injury remains in hand after attempting to play it."""
    sim = make_sim(hand=[sts_sim.Card.Injury], energy=3, monster_hp=20)
    sim.play_card(0)
    hand = sim.get_hand()
    has_injury = any(c.card == sts_sim.Card.Injury for c in hand)
    assert has_injury, "Injury should remain in hand after failed play"


# ── Pain [Y] ─────────────────────────────────────────────────────────────


def test_pain_unplayable():
    """Pain cannot be played (Unplayable)."""
    sim = make_sim(hand=[sts_sim.Card.Pain], energy=3, monster_hp=20)
    result = sim.play_card(0)
    assert result is False, "Pain should not be playable"


def test_pain_in_hand_with_strike():
    """Strike is playable when Pain is in hand."""
    sim = make_sim(hand=[sts_sim.Card.StrikeRed, sts_sim.Card.Pain],
                   energy=3, monster_hp=20)
    result = sim.play_card(0, 0)
    assert result is True, "Strike should be playable alongside Pain"


# ── Clumsy [N] ───────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Clumsy not implemented in simulator")
def test_clumsy_unplayable():
    """Clumsy cannot be played."""
    pass


@pytest.mark.skip(reason="Clumsy not implemented in simulator")
def test_clumsy_ethereal():
    """Clumsy exhausts at end of turn (Ethereal)."""
    pass


@pytest.mark.skip(reason="Clumsy not implemented in simulator")
def test_clumsy_clogs_hand():
    """Clumsy takes up a hand slot when drawn."""
    pass


# ── Doubt [N] ────────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Doubt not implemented in simulator")
def test_doubt_unplayable():
    """Doubt cannot be played."""
    pass


@pytest.mark.skip(reason="Doubt not implemented in simulator")
def test_doubt_end_of_turn_weak():
    """Doubt applies WEAK at end of turn."""
    pass


@pytest.mark.skip(reason="Doubt not implemented in simulator")
def test_doubt_stacking_weak():
    """Doubt stacks WEAK with existing WEAK tokens."""
    pass


# ── Parasite [N] ─────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Parasite not implemented in simulator")
def test_parasite_unplayable():
    """Parasite cannot be played."""
    pass


@pytest.mark.skip(reason="Parasite not implemented in simulator")
def test_parasite_removal_hp_loss():
    """Removing Parasite from deck causes 2 HP loss."""
    pass


@pytest.mark.skip(reason="Parasite not implemented in simulator")
def test_parasite_no_passive_effect():
    """Parasite has no passive effect during combat."""
    pass


# ── Regret [N] ───────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Regret not implemented in simulator")
def test_regret_unplayable():
    """Regret cannot be played."""
    pass


@pytest.mark.skip(reason="Regret not implemented in simulator")
def test_regret_retain():
    """Regret retains in hand every turn."""
    pass


@pytest.mark.skip(reason="Regret not implemented in simulator")
def test_regret_permanent_clog():
    """Regret permanently clogs one hand slot."""
    pass


# ── Shame [N] ────────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Shame not implemented in simulator")
def test_shame_unplayable():
    """Shame cannot be played."""
    pass


@pytest.mark.skip(reason="Shame not implemented in simulator")
def test_shame_end_of_turn_block_loss():
    """Shame causes 1 block loss at end of turn."""
    pass


@pytest.mark.skip(reason="Shame not implemented in simulator")
def test_shame_no_negative_block():
    """Shame does not cause block to go negative."""
    pass


# ── Writhe [N] ───────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Writhe not implemented in simulator")
def test_writhe_play_exhaust():
    """Writhe exhausts when played for 1 energy."""
    pass


@pytest.mark.skip(reason="Writhe not implemented in simulator")
def test_writhe_not_enough_energy():
    """Writhe cannot be played without enough energy."""
    pass


@pytest.mark.skip(reason="Writhe not implemented in simulator")
def test_writhe_discarded_if_not_played():
    """Writhe is discarded if not played, returns to draw pile."""
    pass
