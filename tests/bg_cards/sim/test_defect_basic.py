"""Simulator tests for Defect Basic cards."""
import sts_sim
from tests.live.conftest import make_sim


# ===================================================================
# Strike (Blue) — Attack, Cost 1, 1 HIT. Upgrade: Cost 0.
# ===================================================================


def test_strike_blue_base_damage():
    """Basic Strike deals 1 damage."""
    sim = make_sim(hand=[sts_sim.Card.StrikeBlue], energy=3, monster_hp=20)
    sim.play_card(0, 0)  # target monster 0
    monsters = sim.get_monsters()
    assert monsters[0].hp == 19
    assert sim.player.energy == 2


def test_strike_blue_with_strength():
    """Strike benefits from Strength."""
    sim = make_sim(
        hand=[sts_sim.Card.StrikeBlue], energy=3, monster_hp=20,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 17  # 1 base + 2 STR = 3 damage


def test_strike_blue_upgraded_costs_0():
    """Upgraded Strike costs 0."""
    sim = make_sim(
        hand=[(sts_sim.Card.StrikeBlue, True)], energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 19
    assert sim.player.energy == 3


# ===================================================================
# Defend (Blue) — Skill, Cost 1, 1 BLK. Upgrade: 2 BLK to any player.
# ===================================================================


def test_defend_blue_base_block():
    """Basic Defend grants 1 block."""
    sim = make_sim(hand=[sts_sim.Card.DefendBlue], energy=3, player_block=0)
    sim.play_card(0)  # no target for skills
    assert sim.player.block == 1
    assert sim.player.energy == 2


def test_defend_blue_stacks_with_existing_block():
    """Defend block stacks with existing block."""
    sim = make_sim(hand=[sts_sim.Card.DefendBlue], energy=3, player_block=3)
    sim.play_card(0)
    assert sim.player.block == 4


# ===================================================================
# Zap — Skill, Cost 1, Channel 1 Lightning. Upgrade: Cost 0.
# ===================================================================


def test_zap_channels_lightning():
    """Zap channels 1 Lightning orb."""
    sim = make_sim(hand=[sts_sim.Card.Zap], energy=3, monster_hp=20)
    sim.play_card(0)
    orbs = sim.get_orbs()
    assert len(orbs) == 1
    assert orbs[0].orb_type == sts_sim.OrbType.Lightning
    assert sim.player.energy == 2


def test_zap_evokes_oldest_when_full():
    """Zap evokes oldest orb when orb slots are full."""
    sim = make_sim(
        hand=[sts_sim.Card.Zap], energy=3, monster_hp=20,
        orbs=["Frost", "Frost", "Frost"],
    )
    sim.play_card(0)
    orbs = sim.get_orbs()
    assert len(orbs) == 3
    # Rightmost should be Lightning (newly channeled)
    assert orbs[-1].orb_type == sts_sim.OrbType.Lightning
    # The other two should still be Frost
    assert orbs[0].orb_type == sts_sim.OrbType.Frost
    assert orbs[1].orb_type == sts_sim.OrbType.Frost


def test_zap_upgraded_costs_0():
    """Upgraded Zap costs 0."""
    sim = make_sim(
        hand=[(sts_sim.Card.Zap, True)], energy=3, monster_hp=20,
    )
    sim.play_card(0)
    orbs = sim.get_orbs()
    assert len(orbs) == 1
    assert orbs[0].orb_type == sts_sim.OrbType.Lightning
    assert sim.player.energy == 3


# ===================================================================
# Dualcast — Skill, Cost 1, Evoke an Orb twice. Upgrade: Cost 0.
# ===================================================================


def test_dualcast_evokes_lightning_twice():
    """Dualcast evokes Lightning orb twice for double damage."""
    sim = make_sim(
        hand=[sts_sim.Card.Dualcast], energy=3, monster_hp=20,
        orbs=["Lightning"],
    )
    sim.play_card(0)
    # Lightning evoked twice; orb list should be empty
    orbs = sim.get_orbs()
    assert len(orbs) == 0
    assert sim.player.energy == 2
    # Monster should have taken damage from 2 evocations
    monsters = sim.get_monsters()
    assert monsters[0].hp < 20


def test_dualcast_evokes_frost_twice():
    """Dualcast evokes Frost orb twice for double block."""
    sim = make_sim(
        hand=[sts_sim.Card.Dualcast], energy=3, monster_hp=20,
        player_block=0, orbs=["Frost"],
    )
    sim.play_card(0)
    orbs = sim.get_orbs()
    assert len(orbs) == 0
    # Player should have gained block from 2 Frost evocations
    assert sim.player.block > 0


def test_dualcast_upgraded_costs_0():
    """Upgraded Dualcast costs 0."""
    sim = make_sim(
        hand=[(sts_sim.Card.Dualcast, True)], energy=3, monster_hp=20,
        orbs=["Dark"],
    )
    sim.play_card(0)
    assert sim.player.energy == 3


def test_dualcast_no_orbs():
    """Dualcast with no orbs does nothing."""
    sim = make_sim(hand=[sts_sim.Card.Dualcast], energy=3, monster_hp=20)
    sim.play_card(0)
    assert sim.player.energy == 2
    monsters = sim.get_monsters()
    assert monsters[0].hp == 20
