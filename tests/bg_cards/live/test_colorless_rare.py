"""Live tests for Colorless Rare cards.

All Colorless Rare cards are marked [N] (not in simulator).
Tests are skipped until these cards are implemented.
"""
import pytest


# ── Apotheosis ───────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Apotheosis not implemented in simulator")
def test_apotheosis_base(game):
    """Apotheosis buffs starter Strikes and Defends."""
    pass


@pytest.mark.skip(reason="Apotheosis not implemented in simulator")
def test_apotheosis_upgraded(game):
    """Apotheosis+ costs 1 energy instead of 2."""
    pass


@pytest.mark.skip(reason="Apotheosis not implemented in simulator")
def test_apotheosis_only_starters(game):
    """Apotheosis only affects starter cards, not non-starter attacks."""
    pass


# ── Apparition ───────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Apparition not implemented in simulator")
def test_apparition_base(game):
    """Apparition caps damage taken at 1 HP this turn."""
    pass


@pytest.mark.skip(reason="Apparition not implemented in simulator")
def test_apparition_ethereal(game):
    """Apparition exhausts at end of turn if not played (Ethereal)."""
    pass


@pytest.mark.skip(reason="Apparition not implemented in simulator")
def test_apparition_upgraded(game):
    """Apparition+ is no longer Ethereal."""
    pass


@pytest.mark.skip(reason="Apparition not implemented in simulator")
def test_apparition_multiple_hits(game):
    """Apparition caps total damage from multiple hits at 1 HP."""
    pass


# ── Master of Strategy ──────────────────────────────────────────────────


@pytest.mark.skip(reason="Master of Strategy not implemented in simulator")
def test_master_of_strategy_base(game):
    """Master of Strategy draws 3 cards for free."""
    pass


@pytest.mark.skip(reason="Master of Strategy not implemented in simulator")
def test_master_of_strategy_upgraded(game):
    """Master of Strategy+ draws 4 cards."""
    pass


@pytest.mark.skip(reason="Master of Strategy not implemented in simulator")
def test_master_of_strategy_reshuffle(game):
    """Master of Strategy triggers reshuffle when draw pile is smaller."""
    pass


# ── Panache ──────────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Panache not implemented in simulator")
def test_panache_base(game):
    """Panache deals 3 damage to a row when hand is empty at end of turn."""
    pass


@pytest.mark.skip(reason="Panache not implemented in simulator")
def test_panache_hand_not_empty(game):
    """Panache does not trigger when hand is not empty."""
    pass


@pytest.mark.skip(reason="Panache not implemented in simulator")
def test_panache_upgraded(game):
    """Panache+ deals 5 damage."""
    pass


# ── The Bomb ─────────────────────────────────────────────────────────────


@pytest.mark.skip(reason="The Bomb not implemented in simulator")
def test_the_bomb_base(game):
    """The Bomb detonates after 3 turns for 10 AOE damage."""
    pass


@pytest.mark.skip(reason="The Bomb not implemented in simulator")
def test_the_bomb_upgraded(game):
    """The Bomb+ deals 12 damage."""
    pass


@pytest.mark.skip(reason="The Bomb not implemented in simulator")
def test_the_bomb_not_before_3_turns(game):
    """The Bomb does not trigger before 3 turns have passed."""
    pass
