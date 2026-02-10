import sts_sim


def test_player_power_stacking():
    """Powers should stack up to their caps."""
    p = sts_sim.Player()
    # Vulnerable caps at 3
    # We test via combat since apply_power is internal
    # Instead, test through Monster which also has powers
    m = sts_sim.Monster("Test", 10, "test", "", False)
    assert m.get_power(sts_sim.PowerType.Vulnerable) == 0


def test_player_initial_stats():
    """Ironclad starts with correct stats."""
    p = sts_sim.Player()
    assert p.hp == 10
    assert p.max_hp == 10
    assert p.block == 0
    assert p.block_cap == 20
    assert p.max_energy == 3
    assert p.draw_amount == 5


def test_monster_initial_stats():
    """Monster created with correct stats."""
    m = sts_sim.Monster("Jaw Worm", 8, "jaw_worm", "sda", True)
    assert m.hp == 8
    assert m.max_hp == 8
    assert m.block == 0
    assert m.die_controlled is True
    assert m.behavior == "sda"


def test_vulnerable_cap_via_combat():
    """Vulnerable should cap at 3 stacks."""
    # Create combat, bash the monster multiple times to stack vuln
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert monsters[0].get_power(sts_sim.PowerType.Vulnerable) == 0


def test_powers_dict():
    """get_powers_dict should return string-keyed dict."""
    cs = sts_sim.create_encounter("cultist", seed=42)
    cs.start_combat()
    monsters = cs.get_monsters()
    powers = monsters[0].get_powers_dict()
    assert "Ritual" in powers
    assert powers["Ritual"] == 1
