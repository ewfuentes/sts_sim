"""Live tests for Colorless Uncommon cards.

All Colorless Uncommon cards are marked [N] (not in simulator).
Tests are skipped until these cards are implemented.
"""
import pytest


# ── Dark Shackles ────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Dark Shackles not implemented in simulator")
def test_dark_shackles_base(game):
    """Dark Shackles gains 2 block per attacking enemy and exhausts."""
    pass


@pytest.mark.skip(reason="Dark Shackles not implemented in simulator")
def test_dark_shackles_no_attackers(game):
    """Dark Shackles gains 0 block when no enemies intend to attack."""
    pass


@pytest.mark.skip(reason="Dark Shackles not implemented in simulator")
def test_dark_shackles_upgraded(game):
    """Dark Shackles+ gains 3 block per attacking enemy."""
    pass


# ── Dramatic Entrance ────────────────────────────────────────────────────


@pytest.mark.skip(reason="Dramatic Entrance not implemented in simulator")
def test_dramatic_entrance_first_turn(game):
    """Dramatic Entrance deals AOE 2 + 1 bonus on first turn and exhausts."""
    pass


@pytest.mark.skip(reason="Dramatic Entrance not implemented in simulator")
def test_dramatic_entrance_after_first_turn(game):
    """Dramatic Entrance deals AOE 2 with no bonus after first turn."""
    pass


@pytest.mark.skip(reason="Dramatic Entrance not implemented in simulator")
def test_dramatic_entrance_upgraded(game):
    """Dramatic Entrance+ deals AOE 2 + 3 bonus on first turn."""
    pass


# ── Hand of Greed ────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Hand of Greed not implemented in simulator")
def test_hand_of_greed_no_gold_bonus(game):
    """Hand of Greed deals 4 damage without gold bonus."""
    pass


@pytest.mark.skip(reason="Hand of Greed not implemented in simulator")
def test_hand_of_greed_gold_bonus(game):
    """Hand of Greed deals 4 + 3 bonus with 10+ gold."""
    pass


@pytest.mark.skip(reason="Hand of Greed not implemented in simulator")
def test_hand_of_greed_upgraded(game):
    """Hand of Greed+ deals 4 + 5 bonus with 10+ gold."""
    pass


@pytest.mark.skip(reason="Hand of Greed not implemented in simulator")
def test_hand_of_greed_exact_threshold(game):
    """Hand of Greed bonus applies at exactly 10 gold."""
    pass


# ── Mayhem ───────────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Mayhem not implemented in simulator")
def test_mayhem_base(game):
    """Mayhem auto-plays a drawn card each turn."""
    pass


@pytest.mark.skip(reason="Mayhem not implemented in simulator")
def test_mayhem_upgraded(game):
    """Mayhem+ costs 1 energy instead of 2."""
    pass


@pytest.mark.skip(reason="Mayhem not implemented in simulator")
def test_mayhem_once_per_turn(game):
    """Mayhem only auto-plays one card per turn."""
    pass


# ── Mind Blast ───────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Mind Blast not implemented in simulator")
def test_mind_blast_base(game):
    """Mind Blast deals damage equal to other cards in hand."""
    pass


@pytest.mark.skip(reason="Mind Blast not implemented in simulator")
def test_mind_blast_only_card(game):
    """Mind Blast deals 0 damage when it's the only card."""
    pass


@pytest.mark.skip(reason="Mind Blast not implemented in simulator")
def test_mind_blast_upgraded(game):
    """Mind Blast+ deals X+1 damage."""
    pass


# ── Panacea ──────────────────────────────────────────────────────────────


@pytest.mark.skip(reason="Panacea not implemented in simulator")
def test_panacea_base(game):
    """Panacea removes all WEAK and VULN from a single player."""
    pass


@pytest.mark.skip(reason="Panacea not implemented in simulator")
def test_panacea_retain(game):
    """Panacea retains in hand if not played."""
    pass


@pytest.mark.skip(reason="Panacea not implemented in simulator")
def test_panacea_upgraded(game):
    """Panacea+ removes debuffs from all players."""
    pass


# ── Sadistic Nature ──────────────────────────────────────────────────────


@pytest.mark.skip(reason="Sadistic Nature not implemented in simulator")
def test_sadistic_nature_base(game):
    """Sadistic Nature deals 1 damage when debuff is applied."""
    pass


@pytest.mark.skip(reason="Sadistic Nature not implemented in simulator")
def test_sadistic_nature_multiple_tokens(game):
    """Sadistic Nature triggers per token applied."""
    pass


@pytest.mark.skip(reason="Sadistic Nature not implemented in simulator")
def test_sadistic_nature_upgraded(game):
    """Sadistic Nature+ deals 2 damage per token."""
    pass
