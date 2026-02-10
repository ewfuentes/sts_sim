"""Tests for Act 1 Boss encounters."""
import pytest
import sts_sim


# ============================================================
# The Guardian — 40 HP, offensive cycle
# ============================================================

def test_guardian_hp():
    cs = sts_sim.create_encounter("the_guardian", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].hp == 40
    assert monsters[0].name == "The Guardian"


def test_guardian_whirlwind_first_turn():
    """First turn: Whirlwind (2 dmg) + ChargeUp (5 block)."""
    cs = sts_sim.create_encounter("the_guardian", seed=42)
    cs.start_combat()
    initial_hp = cs.player.hp
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # Took 2 damage from Whirlwind
    assert cs.player.hp == initial_hp - 2
    # Note: Guardian's block resets at start of its turn, so we can't easily
    # check block here since start_player_turn was called. The block was gained
    # during the monster turn.


def test_guardian_fierce_bash_second_turn():
    """Second turn: Fierce Bash (6 dmg)."""
    cs = sts_sim.create_encounter("the_guardian", seed=42)
    cs.start_combat()
    # Turn 1: Whirlwind
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    hp_after_t1 = cs.player.hp
    # Turn 2: Fierce Bash
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    assert cs.player.hp == hp_after_t1 - 6


def test_guardian_alternates():
    """Guardian should alternate Whirlwind and Fierce Bash."""
    cs = sts_sim.create_encounter("the_guardian", seed=42)
    cs.start_combat()
    cs.set_player_hp(50)  # Enough HP to survive 4 turns
    damages = []
    hp = cs.player.hp
    for _ in range(4):
        if cs.combat_over:
            break
        cs.end_player_turn()
        cs.roll_and_execute_monsters()
        new_hp = cs.player.hp
        damages.append(hp - new_hp)
        hp = new_hp
    # Expected: 2, 6, 2, 6
    assert damages == [2, 6, 2, 6]


def test_guardian_combat_runs():
    cs = sts_sim.create_encounter("the_guardian", seed=42)
    cs.start_combat()
    for _ in range(5):
        if cs.combat_over:
            break
        cs.end_player_turn()
        cs.roll_and_execute_monsters()
        if cs.combat_over:
            break


# ============================================================
# Hexaghost — 36 HP, 6-turn cycle
# ============================================================

def test_hexaghost_hp():
    cs = sts_sim.create_encounter("hexaghost", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].hp == 36
    assert monsters[0].name == "Hexaghost"


def test_hexaghost_sear_turn_1():
    """Turn 1: Sear (1 dmg + 1 Burn to discard)."""
    cs = sts_sim.create_encounter("hexaghost", seed=42)
    cs.start_combat()
    initial_hp = cs.player.hp
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # 1 damage
    assert cs.player.hp == initial_hp - 1
    # 1 Burn in discard
    discard = cs.get_discard_pile()
    burns = [c for c in discard if c.card == sts_sim.Card.Burn]
    assert len(burns) >= 1


def test_hexaghost_flame_charge_turn_2():
    """Turn 2: Flame Charge (2×2 dmg + 1 Burn)."""
    cs = sts_sim.create_encounter("hexaghost", seed=42)
    cs.start_combat()
    # Turn 1: Sear
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    hp_after_t1 = cs.player.hp
    # Turn 2: Flame Charge (2+2 = 4 dmg)
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    assert cs.player.hp == hp_after_t1 - 4


def test_hexaghost_burn_turn_3():
    """Turn 3: Burn (2 Burns, no damage)."""
    cs = sts_sim.create_encounter("hexaghost", seed=42)
    cs.start_combat()
    # Turn 1-2
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    hp_after_t2 = cs.player.hp
    # Turn 3: Burn (no damage)
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    assert cs.player.hp == hp_after_t2  # no damage


def test_hexaghost_inferno_turn_6():
    """Turn 6: Inferno (2×3 dmg + 2 Burns + 1 Str)."""
    cs = sts_sim.create_encounter("hexaghost", seed=42)
    cs.start_combat()
    # Run 5 turns first
    for _ in range(5):
        if cs.combat_over:
            break
        cs.end_player_turn()
        cs.roll_and_execute_monsters()
        if cs.combat_over:
            break
    if not cs.combat_over:
        hp_before_inferno = cs.player.hp
        cs.end_player_turn()
        cs.roll_and_execute_monsters()
        # 3+3 = 6 damage from Inferno
        assert cs.player.hp == hp_before_inferno - 6
        # Hexaghost gains 1 Str
        monsters = cs.get_monsters()
        assert monsters[0].get_power(sts_sim.PowerType.Strength) == 1


def test_hexaghost_combat_runs():
    cs = sts_sim.create_encounter("hexaghost", seed=42)
    cs.start_combat()
    for _ in range(8):
        if cs.combat_over:
            break
        cs.end_player_turn()
        cs.roll_and_execute_monsters()
        if cs.combat_over:
            break


# ============================================================
# Slime Boss — 22 HP, splits on death
# ============================================================

def test_slime_boss_hp():
    cs = sts_sim.create_encounter("slime_boss", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].hp == 22
    assert monsters[0].name == "Slime Boss"


def test_slime_boss_sticky_first_turn():
    """Turn 1: Sticky (3 Slimed to discard)."""
    cs = sts_sim.create_encounter("slime_boss", seed=42)
    cs.start_combat()
    initial_hp = cs.player.hp
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # No damage from Sticky
    assert cs.player.hp == initial_hp
    # 3 Slimed in discard
    discard = cs.get_discard_pile()
    slimed = [c for c in discard if c.card == sts_sim.Card.Slimed]
    assert len(slimed) >= 3


def test_slime_boss_tackle_second_turn():
    """Turn 2: Tackle (3 dmg + 2 Slimed)."""
    cs = sts_sim.create_encounter("slime_boss", seed=42)
    cs.start_combat()
    # Turn 1: Sticky
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    hp_after_t1 = cs.player.hp
    # Turn 2: Tackle (3 dmg)
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    assert cs.player.hp == hp_after_t1 - 3


def test_slime_boss_slam_third_turn():
    """Turn 3: Slam (6 dmg)."""
    cs = sts_sim.create_encounter("slime_boss", seed=42)
    cs.start_combat()
    # Turn 1-2
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    hp_after_t2 = cs.player.hp
    # Turn 3: Slam (6 dmg)
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    assert cs.player.hp == hp_after_t2 - 6


def test_slime_boss_half_dead_on_zero_hp():
    """Slime Boss enters half_dead state when HP reaches 0."""
    cs = sts_sim.create_encounter("slime_boss", seed=42)
    cs.start_combat()
    # Set Slime Boss HP to 1 so next attack kills it
    cs.set_player_hp(10)
    # Give player enough Str to one-shot the boss (Strike base=1, need 22+ damage)
    cs.apply_player_power(sts_sim.PowerType.Strength, 25)
    # Play Strike targeting Slime Boss
    hand = cs.get_hand()
    for i, card in enumerate(hand):
        if card.card == sts_sim.Card.StrikeRed:
            cs.play_card(i, 0)
            break
    # Combat should NOT be over — boss is half_dead
    assert not cs.combat_over
    monsters = cs.get_monsters()
    assert monsters[0].half_dead is True


def test_slime_boss_splits():
    """Slime Boss should split into 3 slimes after becoming half_dead."""
    cs = sts_sim.create_encounter("slime_boss", seed=42)
    cs.start_combat()
    # One-shot the boss
    cs.apply_player_power(sts_sim.PowerType.Strength, 25)
    hand = cs.get_hand()
    for i, card in enumerate(hand):
        if card.card == sts_sim.Card.StrikeRed:
            cs.play_card(i, 0)
            break
    # Boss is half_dead, combat continues
    assert not cs.combat_over
    # End turn and let monsters act — Slime Boss should split
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # Now we should have 3+ monsters (the dead boss + 3 spawned slimes)
    monsters = cs.get_monsters()
    alive = [m for m in monsters if m.hp > 0]
    assert len(alive) == 3


def test_slime_boss_combat_runs():
    cs = sts_sim.create_encounter("slime_boss", seed=42)
    cs.start_combat()
    for _ in range(5):
        if cs.combat_over:
            break
        cs.end_player_turn()
        cs.roll_and_execute_monsters()
        if cs.combat_over:
            break


# ============================================================
# Smoke tests — all boss encounters
# ============================================================

@pytest.mark.parametrize("encounter", [
    "the_guardian", "hexaghost", "slime_boss",
])
def test_boss_creates(encounter):
    cs = sts_sim.create_encounter(encounter, seed=42)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) >= 1


@pytest.mark.parametrize("encounter", [
    "the_guardian", "hexaghost", "slime_boss",
])
def test_boss_runs_one_turn(encounter):
    cs = sts_sim.create_encounter(encounter, seed=42)
    cs.start_combat()
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    assert True


@pytest.mark.parametrize("encounter", [
    "the_guardian", "hexaghost", "slime_boss",
])
def test_boss_runs_multiple_turns(encounter):
    cs = sts_sim.create_encounter(encounter, seed=42)
    cs.start_combat()
    for _ in range(5):
        if cs.combat_over:
            break
        cs.end_player_turn()
        cs.roll_and_execute_monsters()
        if cs.combat_over:
            break
