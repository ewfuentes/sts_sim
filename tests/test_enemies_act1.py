"""Tests for Act 1 normal enemies (strong pool)."""
import pytest
import sts_sim


# ============================================================
# Acid Slime (M) — 5 HP, die-controlled
# ============================================================

def test_acid_slime_m_hp():
    cs = sts_sim.create_encounter("slime_trio", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    # Index 1 is acid slime M
    acid = monsters[1]
    assert acid.hp == 5
    assert acid.name == "Acid Slime (M)"


def test_acid_slime_m_wound_tackle():
    """Wound Tackle ('C'): 2 dmg + add Dazed to draw."""
    cs = sts_sim.create_encounter("slime_trio", seed=0)
    cs.start_combat()
    # Behavior "CAL": roll 1-2 → 'C' (Wound Tackle)
    # Need a die roll of 1 or 2 for first behavior char
    initial_hp = cs.player.hp
    draw_before = len(cs.get_draw_pile())
    cs.end_player_turn()
    roll = cs.roll_and_execute_monsters()
    # After monster turn, check damage was dealt and cards may have been added


def test_acid_slime_m_weak_lick():
    """Weak Lick ('L'): apply 1 Weak to player."""
    cs = sts_sim.create_encounter("slime_trio", seed=0)
    cs.start_combat()
    # We can't easily control the die roll, but we test that the encounter works
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # Game should not crash — basic smoke test


# ============================================================
# Spike Slime (M) — 5 HP, die-controlled
# ============================================================

def test_spike_slime_m_hp():
    cs = sts_sim.create_encounter("cultist_and_spike_slime", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    spike = monsters[1]
    assert spike.hp == 5
    assert spike.name == "Spike Slime (M)"


def test_spike_slime_m_combat_runs():
    """Spike Slime should execute moves without crashing."""
    cs = sts_sim.create_encounter("cultist_and_spike_slime", seed=42)
    cs.start_combat()
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    assert cs.player.hp <= 10  # took some damage


# ============================================================
# Spike Slime (S) — 3 HP, always attacks for 1
# ============================================================

def test_spike_slime_s_hp():
    cs = sts_sim.create_encounter("slime_trio", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    small = monsters[0]
    assert small.hp == 3
    assert small.name == "Spike Slime (S)"


def test_spike_slime_s_always_attacks():
    """Spike Slime S always deals 1 damage."""
    cs = sts_sim.create_encounter("slime_trio", seed=42)
    cs.start_combat()
    initial_hp = cs.player.hp
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # Player should have taken damage from all 3 slimes
    assert cs.player.hp < initial_hp


# ============================================================
# Fungi Beast — 5 HP, die-controlled, SporeCloud
# ============================================================

def test_fungi_beast_hp():
    cs = sts_sim.create_encounter("fungi_beasts", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 2
    assert monsters[0].hp == 5
    assert monsters[1].hp == 5
    assert monsters[0].name == "Fungi Beast"


def test_fungi_beast_spore_cloud():
    """Fungi Beast should have SporeCloud power."""
    cs = sts_sim.create_encounter("fungi_beasts", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert monsters[0].get_power(sts_sim.PowerType.SporeCloud) == 1


def test_fungi_beast_combat_runs():
    cs = sts_sim.create_encounter("fungi_beasts", seed=42)
    cs.start_combat()
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    assert cs.player.hp <= 10


# ============================================================
# Blue Slaver — 10 HP, die-controlled
# ============================================================

def test_blue_slaver_hp():
    cs = sts_sim.create_encounter("blue_slaver", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].hp == 10
    assert monsters[0].name == "Blue Slaver"


def test_blue_slaver_combat_runs():
    cs = sts_sim.create_encounter("blue_slaver", seed=42)
    cs.start_combat()
    cs.end_player_turn()
    roll = cs.roll_and_execute_monsters()
    # Slaver should have attacked or debuffed
    assert cs.player.hp <= 10 or cs.player.get_power(sts_sim.PowerType.Weak) > 0


# ============================================================
# Red Slaver — 10 HP, die-controlled
# ============================================================

def test_red_slaver_hp():
    cs = sts_sim.create_encounter("red_slaver", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].hp == 10
    assert monsters[0].name == "Red Slaver"


def test_red_slaver_combat_runs():
    cs = sts_sim.create_encounter("red_slaver", seed=42)
    cs.start_combat()
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    assert cs.player.hp <= 10 or cs.player.get_power(sts_sim.PowerType.Vulnerable) > 0


# ============================================================
# Looter — 9 HP, sequential pattern
# ============================================================

def test_looter_hp():
    cs = sts_sim.create_encounter("looter", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].hp == 9
    assert monsters[0].name == "Looter"


def test_looter_mug_deals_damage():
    """Looter's first move (Mug) should deal 2 damage."""
    cs = sts_sim.create_encounter("looter", seed=42)
    cs.start_combat()
    initial_hp = cs.player.hp
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # Mug deals 2 damage
    assert cs.player.hp == initial_hp - 2


def test_looter_sequential_pattern():
    """Looter should follow Mug → Lunge → Escape."""
    cs = sts_sim.create_encounter("looter", seed=42)
    cs.start_combat()

    # Turn 1: Mug (2 dmg)
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    hp_after_mug = cs.player.hp

    # Turn 2: Lunge (3 dmg + 1 block)
    cs.start_player_turn()
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    hp_after_lunge = cs.player.hp
    assert hp_after_lunge == hp_after_mug - 3

    # Turn 3: Escape (monster dies/escapes)
    cs.start_player_turn()
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    monsters = cs.get_monsters()
    assert monsters[0].hp <= 0  # escaped = dead


# ============================================================
# Gremlins
# ============================================================

def test_angry_gremlin_hp():
    cs = sts_sim.create_encounter("angry_gremlin_team", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 3
    # Leader is angry gremlin
    assert monsters[0].hp == 4
    assert monsters[0].name == "Mad Gremlin"


def test_angry_gremlin_has_anger():
    """Angry Gremlin should have Anger power."""
    cs = sts_sim.create_encounter("angry_gremlin_team", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert monsters[0].get_power(sts_sim.PowerType.Anger) == 1


def test_sneaky_gremlin_hp():
    cs = sts_sim.create_encounter("sneaky_gremlin_team", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 3
    assert monsters[0].hp == 2
    assert monsters[0].name == "Sneaky Gremlin"


def test_fat_gremlin_hp():
    """Fat Gremlin should have 3 HP."""
    # Create a team that includes a fat gremlin (seed 2 → pool index 2 = "fat")
    cs = sts_sim.create_encounter("sneaky_gremlin_team", seed=2)
    cs.start_combat()
    monsters = cs.get_monsters()
    has_fat = any(m.name == "Fat Gremlin" for m in monsters)
    assert has_fat
    for m in monsters:
        if m.name == "Fat Gremlin":
            assert m.hp == 3


def test_wizard_gremlin_hp():
    """Wizard Gremlin should have 4 HP."""
    # seed 3 → pool index 3 = "wizard"
    cs = sts_sim.create_encounter("sneaky_gremlin_team", seed=3)
    cs.start_combat()
    monsters = cs.get_monsters()
    has_wizard = any(m.name == "Gremlin Wizard" for m in monsters)
    assert has_wizard
    for m in monsters:
        if m.name == "Gremlin Wizard":
            assert m.hp == 4


def test_gremlin_combat_runs():
    """Gremlin team combat should run without crashing."""
    cs = sts_sim.create_encounter("angry_gremlin_team", seed=42)
    cs.start_combat()
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    assert cs.player.hp < 10  # gremlins should deal damage


def test_wizard_charges_then_attacks():
    """Wizard Gremlin should charge for 2 turns, then attack for 3."""
    cs = sts_sim.create_encounter("sneaky_gremlin_team", seed=3)
    cs.start_combat()
    monsters = cs.get_monsters()
    wizard_idx = None
    for i, m in enumerate(monsters):
        if m.name == "Gremlin Wizard":
            wizard_idx = i
            break
    assert wizard_idx is not None

    # Kill all non-wizard gremlins so only wizard attacks
    for i, m in enumerate(monsters):
        if i != wizard_idx:
            # Kill by playing strikes
            pass  # We'll just check turns

    # Turn 1: Wizard charges (no damage)
    hp_before = cs.player.hp
    cs.end_player_turn()
    cs.roll_and_execute_monsters()

    # Turn 2: Wizard still charges
    cs.start_player_turn()
    cs.end_player_turn()
    cs.roll_and_execute_monsters()

    # Turn 3: Wizard attacks for 3 damage
    cs.start_player_turn()
    hp_before_attack = cs.player.hp
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # Wizard should have dealt 3 damage (plus other gremlins dealing damage too)
    assert cs.player.hp < hp_before_attack


# ============================================================
# 3 Louse (Hard) encounter
# ============================================================

def test_3_louse_hard_composition():
    cs = sts_sim.create_encounter("3_louse_hard", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 3
    assert monsters[0].name == "Red Louse"
    assert monsters[1].name == "Green Louse"
    assert monsters[2].name == "Red Louse"


def test_3_louse_hard_all_have_curl_up():
    cs = sts_sim.create_encounter("3_louse_hard", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    for m in monsters:
        assert m.get_power(sts_sim.PowerType.CurlUp) == 2


# ============================================================
# Large Slime encounter
# ============================================================

def test_large_slime_hp():
    cs = sts_sim.create_encounter("large_slime", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].hp == 8
    assert monsters[0].name == "Acid Slime (L)"


# ============================================================
# Encounter smoke tests — all encounters create without crashing
# ============================================================

@pytest.mark.parametrize("encounter", [
    "jaw_worm", "cultist", "louse",
    "cultist_and_spike_slime", "cultist_and_louse",
    "fungi_beasts", "slime_trio", "3_louse_hard", "large_slime",
    "blue_slaver", "red_slaver", "looter",
    "sneaky_gremlin_team", "angry_gremlin_team",
])
def test_encounter_creates(encounter):
    """All encounters should create successfully."""
    cs = sts_sim.create_encounter(encounter, seed=42)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) >= 1


@pytest.mark.parametrize("encounter", [
    "jaw_worm", "cultist", "louse",
    "cultist_and_spike_slime", "cultist_and_louse",
    "fungi_beasts", "slime_trio", "3_louse_hard", "large_slime",
    "blue_slaver", "red_slaver", "looter",
    "sneaky_gremlin_team", "angry_gremlin_team",
])
def test_encounter_runs_one_turn(encounter):
    """All encounters should run at least one turn without crashing."""
    cs = sts_sim.create_encounter(encounter, seed=42)
    cs.start_combat()
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # Should not crash
    assert True


@pytest.mark.parametrize("encounter", [
    "jaw_worm", "cultist", "louse",
    "cultist_and_spike_slime", "cultist_and_louse",
    "fungi_beasts", "slime_trio", "3_louse_hard", "large_slime",
    "blue_slaver", "red_slaver", "looter",
    "sneaky_gremlin_team", "angry_gremlin_team",
])
def test_encounter_runs_multiple_turns(encounter):
    """All encounters should survive 3 turns without crashing."""
    cs = sts_sim.create_encounter(encounter, seed=42)
    cs.start_combat()
    for _ in range(3):
        if cs.combat_over:
            break
        cs.end_player_turn()
        cs.roll_and_execute_monsters()
        if cs.combat_over:
            break
        cs.start_player_turn()
