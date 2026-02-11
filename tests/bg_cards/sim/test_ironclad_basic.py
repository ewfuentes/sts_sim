"""Simulator tests for Ironclad Basic cards."""
import sts_sim
from tests.live.conftest import make_sim


# =========================================================================
# Strike
# =========================================================================

def test_strike_base_damage():
    """Base Strike deals 1 damage."""
    sim = make_sim(hand=[sts_sim.Card.StrikeRed], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 19  # 20 - 1 = 19
    assert sim.player.energy == 2


def test_strike_with_strength():
    """Strike with 2 STR deals 3 damage (1 base + 2 STR)."""
    sim = make_sim(hand=[sts_sim.Card.StrikeRed], energy=3, monster_hp=20,
                   player_powers={"Strength": 2})
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17


def test_strike_upgraded():
    """Upgraded Strike deals 2 damage."""
    sim = make_sim(hand=[(sts_sim.Card.StrikeRed, True)], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18


# =========================================================================
# Defend
# =========================================================================

def test_defend_base_block():
    """Base Defend grants 1 block."""
    sim = make_sim(hand=[sts_sim.Card.DefendRed], energy=3, player_block=0)
    sim.play_card(0, None)
    assert sim.player.block == 1
    assert sim.player.energy == 2


def test_defend_upgraded_block():
    """Upgraded Defend grants 2 block to any player."""
    sim = make_sim(hand=[(sts_sim.Card.DefendRed, True)], energy=3, player_block=0)
    sim.play_card(0, None)
    assert sim.player.block == 2
    assert sim.player.energy == 2


def test_defend_block_removed_next_turn():
    """Block from Defend is removed at start of next turn."""
    sim = make_sim(hand=[sts_sim.Card.DefendRed], energy=3, player_block=0)
    sim.play_card(0, None)
    assert sim.player.block == 1
    sim.end_player_turn()
    sim.roll_and_execute_monsters()
    # Block resets at start of next player turn (inside roll_and_execute_monsters)
    assert sim.player.block == 0


# =========================================================================
# Bash
# =========================================================================

def test_bash_base_damage_and_vulnerable():
    """Base Bash deals 2 damage and applies Vulnerable."""
    sim = make_sim(hand=[sts_sim.Card.Bash], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Vulnerable) == 1
    assert sim.player.energy == 1


def test_bash_upgraded_damage_and_vulnerable():
    """Upgraded Bash deals 4 damage and applies Vulnerable."""
    sim = make_sim(hand=[(sts_sim.Card.Bash, True)], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 16  # 20 - 4 = 16
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Vulnerable) == 1
    assert sim.player.energy == 1


def test_bash_with_strength():
    """Bash with 1 STR deals 3 damage (2 base + 1 STR)."""
    sim = make_sim(hand=[sts_sim.Card.Bash], energy=3, monster_hp=20,
                   player_powers={"Strength": 1})
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Vulnerable) == 1
