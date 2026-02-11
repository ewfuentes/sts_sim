"""Simulator tests for Colorless Common cards.

All Colorless Common cards are marked [N] (not in simulator).
Tests are skipped until these cards are implemented.
"""
import pytest


# ── Blind ────────────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Blind not implemented in simulator")
def test_blind_base():
    """Blind applies 1 WEAK and exhausts."""
    pass


@pytest.mark.skip(reason="Blind not implemented in simulator")
def test_blind_upgraded():
    """Blind+ applies 2 WEAK and exhausts."""
    pass


@pytest.mark.skip(reason="Blind not implemented in simulator")
def test_blind_exhaust_interaction():
    """Blind is removed from combat after play (exhaust pile)."""
    pass


# ── Finesse ──────────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Finesse not implemented in simulator")
def test_finesse_base():
    """Finesse gains 1 block, draws 1 card, and exhausts."""
    pass


@pytest.mark.skip(reason="Finesse not implemented in simulator")
def test_finesse_upgraded():
    """Finesse+ gains 1 block, draws 1, no longer exhausts."""
    pass


@pytest.mark.skip(reason="Finesse not implemented in simulator")
def test_finesse_empty_draw_pile():
    """Finesse with empty draw pile triggers shuffle before draw."""
    pass


# ── Flash of Steel ───────────────────────────────────────────────────────


@pytest.mark.skip(reason="Flash of Steel not implemented in simulator")
def test_flash_of_steel_base():
    """Flash of Steel deals 1 damage, draws 1 card, and exhausts."""
    pass


@pytest.mark.skip(reason="Flash of Steel not implemented in simulator")
def test_flash_of_steel_upgraded():
    """Flash of Steel+ deals 1 damage, draws 1, no longer exhausts."""
    pass


@pytest.mark.skip(reason="Flash of Steel not implemented in simulator")
def test_flash_of_steel_vs_block():
    """Flash of Steel damage against enemy with 1 block."""
    pass


# ── Good Instincts ───────────────────────────────────────────────────────


@pytest.mark.skip(reason="Good Instincts not implemented in simulator")
def test_good_instincts_base():
    """Good Instincts gains 1 block on self."""
    pass


@pytest.mark.skip(reason="Good Instincts not implemented in simulator")
def test_good_instincts_target_ally():
    """Good Instincts targets another player for 1 block."""
    pass


@pytest.mark.skip(reason="Good Instincts not implemented in simulator")
def test_good_instincts_upgraded():
    """Good Instincts+ gains 2 block."""
    pass


# ── Impatience ───────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Impatience not implemented in simulator")
def test_impatience_base():
    """Impatience draws 2 cards."""
    pass


@pytest.mark.skip(reason="Impatience not implemented in simulator")
def test_impatience_upgraded():
    """Impatience+ draws 3 cards."""
    pass


@pytest.mark.skip(reason="Impatience not implemented in simulator")
def test_impatience_draw_pile_smaller():
    """Impatience with fewer cards in draw pile than draw amount."""
    pass


# ── Madness ──────────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Madness not implemented in simulator")
def test_madness_base():
    """Madness makes next card cost 0 and exhausts."""
    pass


@pytest.mark.skip(reason="Madness not implemented in simulator")
def test_madness_only_next_card():
    """Madness effect only applies to the very next card played."""
    pass


@pytest.mark.skip(reason="Madness not implemented in simulator")
def test_madness_upgraded_retain():
    """Madness+ retains if not played."""
    pass


# ── Purity ───────────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Purity not implemented in simulator")
def test_purity_base():
    """Purity exhausts up to 3 cards from hand."""
    pass


@pytest.mark.skip(reason="Purity not implemented in simulator")
def test_purity_fewer_than_max():
    """Purity can exhaust fewer than 3 cards."""
    pass


@pytest.mark.skip(reason="Purity not implemented in simulator")
def test_purity_upgraded():
    """Purity+ exhausts up to 5 cards from hand."""
    pass


# ── Swift Strike ─────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Swift Strike not implemented in simulator")
def test_swift_strike_base():
    """Swift Strike deals 1 damage and optionally switches rows."""
    pass


@pytest.mark.skip(reason="Swift Strike not implemented in simulator")
def test_swift_strike_decline_switch():
    """Swift Strike deals damage without row switch."""
    pass


@pytest.mark.skip(reason="Swift Strike not implemented in simulator")
def test_swift_strike_upgraded():
    """Swift Strike+ deals 2 damage."""
    pass


# ── Thinking Ahead ───────────────────────────────────────────────────────


@pytest.mark.skip(reason="Thinking Ahead not implemented in simulator")
def test_thinking_ahead_base():
    """Thinking Ahead draws 2, puts 1 back on draw pile, exhausts."""
    pass


@pytest.mark.skip(reason="Thinking Ahead not implemented in simulator")
def test_thinking_ahead_upgraded():
    """Thinking Ahead+ draws 3 instead of 2."""
    pass


@pytest.mark.skip(reason="Thinking Ahead not implemented in simulator")
def test_thinking_ahead_card_put_back():
    """Card put back by Thinking Ahead is first drawn next turn."""
    pass


# ── Trip ─────────────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Trip not implemented in simulator")
def test_trip_base():
    """Trip applies 2 VULN and exhausts."""
    pass


@pytest.mark.skip(reason="Trip not implemented in simulator")
def test_trip_upgraded():
    """Trip+ applies 3 VULN and exhausts."""
    pass


@pytest.mark.skip(reason="Trip not implemented in simulator")
def test_trip_stacking_vuln():
    """Trip stacks VULN on already-vulnerable enemy."""
    pass
