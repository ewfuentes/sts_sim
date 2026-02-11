"""Simulator tests for Silent Basic cards."""
import sts_sim
from tests.live.conftest import make_sim


# ---------------------------------------------------------------------------
# Strike (Green)
# ---------------------------------------------------------------------------

def test_strike_green_base():
    """Basic Strike deals 1 damage."""
    sim = make_sim(hand=[sts_sim.Card.StrikeGreen], energy=3, monster_hp=10)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 9
    assert sim.player.energy == 2


def test_strike_green_with_strength():
    """Strike with 2 STR adds bonus damage per HIT."""
    sim = make_sim(
        hand=[sts_sim.Card.StrikeGreen], energy=3, monster_hp=10,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 7  # 1 HIT + 2 STR = 3 damage


def test_strike_green_upgraded():
    """Upgraded Strike deals 2 HIT (each boosted by STR)."""
    sim = make_sim(
        hand=[(sts_sim.Card.StrikeGreen, True)], energy=3, monster_hp=10,
        player_powers={"Strength": 1},
    )
    sim.play_card(0, 0)
    # 2 HIT, each dealing 1+1 STR = 2 damage each = 4 total
    assert sim.get_monsters()[0].hp == 6


# ---------------------------------------------------------------------------
# Defend (Green)
# ---------------------------------------------------------------------------

def test_defend_green_base():
    """Basic Defend grants 1 block to self."""
    sim = make_sim(hand=[sts_sim.Card.DefendGreen], energy=3, player_block=0)
    sim.play_card(0, None)
    assert sim.player.block == 1
    assert sim.player.energy == 2


def test_defend_green_upgraded_stack_on_self():
    """Upgraded Defend can stack both BLK on self."""
    sim = make_sim(
        hand=[(sts_sim.Card.DefendGreen, True)], energy=3, player_block=0,
    )
    # Assign both BLK to self (choice 0 = self for each BLK)
    sim.play_card(0, None, 0)
    assert sim.player.block == 2


# ---------------------------------------------------------------------------
# Neutralize
# ---------------------------------------------------------------------------

def test_neutralize_base():
    """Neutralize deals 1 damage and applies 1 WEAK at zero cost."""
    sim = make_sim(hand=[sts_sim.Card.Neutralize], energy=3, monster_hp=10)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 9
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 1
    assert sim.player.energy == 3  # costs 0


def test_neutralize_with_strength():
    """Neutralize with 1 STR deals 2 damage."""
    sim = make_sim(
        hand=[sts_sim.Card.Neutralize], energy=3, monster_hp=10,
        player_powers={"Strength": 1},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 8  # 1 HIT + 1 STR = 2 damage
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 1


def test_neutralize_upgraded():
    """Upgraded Neutralize deals 2 HIT and applies 1 Weak."""
    sim = make_sim(
        hand=[(sts_sim.Card.Neutralize, True)], energy=3, monster_hp=10,
        player_powers={"Strength": 1},
    )
    sim.play_card(0, 0)
    # 2 HIT, each dealing 1+1 STR = 2 damage each = 4 total
    assert sim.get_monsters()[0].hp == 6
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 1


# ---------------------------------------------------------------------------
# Survivor
# ---------------------------------------------------------------------------

def test_survivor_base():
    """Survivor grants 2 block and forces a discard."""
    sim = make_sim(
        hand=[sts_sim.Card.Survivor, sts_sim.Card.StrikeGreen],
        energy=3, player_block=0,
    )
    # Play Survivor (index 0), choose to discard card at index 0 in remaining hand (Strike)
    sim.play_card(0, None, 0)
    assert sim.player.block == 2
    assert sim.player.energy == 2
    # Strike should be in discard pile
    discard = sim.get_discard_pile()
    discard_cards = [c.card for c in discard]
    assert sts_sim.Card.StrikeGreen in discard_cards


def test_survivor_upgraded():
    """Upgraded Survivor grants 3 block and forces a discard."""
    sim = make_sim(
        hand=[(sts_sim.Card.Survivor, True), sts_sim.Card.DefendGreen],
        energy=3, player_block=0,
    )
    sim.play_card(0, None, 0)
    assert sim.player.block == 3
    assert sim.player.energy == 2
    discard = sim.get_discard_pile()
    discard_cards = [c.card for c in discard]
    assert sts_sim.Card.DefendGreen in discard_cards


def test_survivor_discard_triggers_after_image():
    """Survivor discard triggers After Image for extra block."""
    sim = make_sim(
        hand=[sts_sim.Card.Survivor, sts_sim.Card.StrikeGreen],
        energy=3, player_block=0,
        player_powers={"AfterImage": 1},
    )
    sim.play_card(0, None, 0)
    # 2 block from Survivor + 1 block from After Image = 3
    assert sim.player.block == 3
