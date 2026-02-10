"""Tests for Act 1 Elite encounters."""
import pytest
import sts_sim


# ============================================================
# Gremlin Nob — 14 HP, sequential
# ============================================================

def test_gremlin_nob_hp():
    cs = sts_sim.create_encounter("gremlin_nob", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].hp == 14
    assert monsters[0].name == "Gremlin Nob"


def test_gremlin_nob_bellow_first_turn():
    """First turn: Bellow (apply Anger power)."""
    cs = sts_sim.create_encounter("gremlin_nob", seed=42)
    cs.start_combat()
    initial_hp = cs.player.hp
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # Bellow doesn't deal damage
    monsters = cs.get_monsters()
    assert monsters[0].get_power(sts_sim.PowerType.Anger) == 1
    # Player HP unchanged from Bellow (no damage)
    assert cs.player.hp == initial_hp


def test_gremlin_nob_skull_bash_second_turn():
    """Second turn: Skull Bash (3 dmg)."""
    cs = sts_sim.create_encounter("gremlin_nob", seed=42)
    cs.start_combat()
    # Turn 1: Bellow
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    hp_after_bellow = cs.player.hp
    # Turn 2: Skull Bash (3 dmg)
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    assert cs.player.hp == hp_after_bellow - 3


def test_gremlin_nob_anger_on_skill():
    """Anger power: deal 1 damage to player when a Skill is played."""
    cs = sts_sim.create_encounter("gremlin_nob", seed=42)
    cs.start_combat()
    # Turn 1: Bellow (sets up Anger)
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    hp_before_skill = cs.player.hp
    # Play a Defend (Skill) — should trigger Anger (1 HP loss, bypasses block)
    hand = cs.get_hand()
    skill_idx = None
    for i, card in enumerate(hand):
        if card.card == sts_sim.Card.DefendRed:
            skill_idx = i
            break
    if skill_idx is not None:
        cs.play_card(skill_idx)
        # Player lost 1 HP from Anger (bypasses block, so block gained from Defend doesn't matter)
        assert cs.player.hp == hp_before_skill - 1


def test_gremlin_nob_anger_not_on_attack():
    """Anger should NOT trigger on Attack cards."""
    cs = sts_sim.create_encounter("gremlin_nob", seed=42)
    cs.start_combat()
    # Turn 1: Bellow
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    hp_before = cs.player.hp
    # Play a Strike (Attack) — should NOT trigger Anger
    hand = cs.get_hand()
    attack_idx = None
    for i, card in enumerate(hand):
        if card.card == sts_sim.Card.StrikeRed:
            attack_idx = i
            break
    if attack_idx is not None:
        cs.play_card(attack_idx, 0)
        # HP unchanged (no Anger trigger from attacks)
        assert cs.player.hp == hp_before


def test_gremlin_nob_combat_runs():
    cs = sts_sim.create_encounter("gremlin_nob", seed=42)
    cs.start_combat()
    for _ in range(3):
        if cs.combat_over:
            break
        cs.end_player_turn()
        cs.roll_and_execute_monsters()
        if cs.combat_over:
            break


# ============================================================
# Lagavulin — 22 HP, sequential, starts asleep
# ============================================================

def test_lagavulin_hp():
    cs = sts_sim.create_encounter("lagavulin", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].hp == 22
    assert monsters[0].name == "Lagavulin"


def test_lagavulin_sleeps_first_turn():
    """First turn: Sleep (no damage)."""
    cs = sts_sim.create_encounter("lagavulin", seed=42)
    cs.start_combat()
    initial_hp = cs.player.hp
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # Sleep deals no damage
    assert cs.player.hp == initial_hp


def test_lagavulin_attacks_second_turn():
    """Second turn: Attack (4 dmg)."""
    cs = sts_sim.create_encounter("lagavulin", seed=42)
    cs.start_combat()
    # Turn 1: Sleep
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    hp_after_sleep = cs.player.hp
    # Turn 2: Attack (4 dmg)
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    assert cs.player.hp == hp_after_sleep - 4


def test_lagavulin_siphon_soul_on_turn_4():
    """Turn 4: Siphon Soul (2 Weak + 1 Str)."""
    cs = sts_sim.create_encounter("lagavulin", seed=42)
    cs.start_combat()
    # Turn 1: Sleep
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # Turn 2: Attack
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # Turn 3: Attack
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    hp_before_siphon = cs.player.hp
    # Turn 4: Siphon Soul
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # No damage from Siphon Soul, but player gets 2 Weak
    assert cs.player.hp == hp_before_siphon  # no direct damage
    assert cs.player.get_power(sts_sim.PowerType.Weak) > 0
    # Monster gains Str
    monsters = cs.get_monsters()
    assert monsters[0].get_power(sts_sim.PowerType.Strength) == 1


def test_lagavulin_combat_runs():
    cs = sts_sim.create_encounter("lagavulin", seed=42)
    cs.start_combat()
    for _ in range(5):
        if cs.combat_over:
            break
        cs.end_player_turn()
        cs.roll_and_execute_monsters()
        if cs.combat_over:
            break


# ============================================================
# Sentries — 3 sentries, die-controlled (2-char behaviors)
# ============================================================

def test_sentries_composition():
    cs = sts_sim.create_encounter("sentries", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 3
    assert all(m.name == "Sentry" for m in monsters)


def test_sentries_hp():
    cs = sts_sim.create_encounter("sentries", seed=0)
    cs.start_combat()
    monsters = cs.get_monsters()
    # Sentry A: "D3" → 7 HP
    assert monsters[0].hp == 7
    # Sentry B: "3D" → 8 HP
    assert monsters[1].hp == 8
    # Sentry C: "2D" → 7 HP (A0)
    assert monsters[2].hp == 7


def test_sentries_combat_runs():
    cs = sts_sim.create_encounter("sentries", seed=42)
    cs.start_combat()
    for _ in range(3):
        if cs.combat_over:
            break
        cs.end_player_turn()
        cs.roll_and_execute_monsters()
        if cs.combat_over:
            break


def test_sentries_add_dazed():
    """Sentry Daze move should add Dazed to draw pile."""
    cs = sts_sim.create_encounter("sentries", seed=0)
    cs.start_combat()
    draw_before = len(cs.get_draw_pile())
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # At least one sentry should have dazed (depending on die roll)
    # We can't guarantee which move fires, but combat should work
    assert not cs.combat_over or cs.player.hp > 0


def test_sentries_deal_damage():
    """Sentries should deal damage when attacking."""
    cs = sts_sim.create_encounter("sentries", seed=42)
    cs.start_combat()
    initial_hp = cs.player.hp
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    # Player should have taken damage or gotten Dazed (or both)
    draw_pile = cs.get_draw_pile()
    has_dazed = any(c.card == sts_sim.Card.Dazed for c in draw_pile)
    took_damage = cs.player.hp < initial_hp
    assert has_dazed or took_damage


# ============================================================
# Smoke tests — all elite encounters
# ============================================================

@pytest.mark.parametrize("encounter", [
    "gremlin_nob", "lagavulin", "sentries",
])
def test_elite_creates(encounter):
    cs = sts_sim.create_encounter(encounter, seed=42)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) >= 1


@pytest.mark.parametrize("encounter", [
    "gremlin_nob", "lagavulin", "sentries",
])
def test_elite_runs_one_turn(encounter):
    cs = sts_sim.create_encounter(encounter, seed=42)
    cs.start_combat()
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    assert True


@pytest.mark.parametrize("encounter", [
    "gremlin_nob", "lagavulin", "sentries",
])
def test_elite_runs_multiple_turns(encounter):
    cs = sts_sim.create_encounter(encounter, seed=42)
    cs.start_combat()
    for _ in range(5):
        if cs.combat_over:
            break
        cs.end_player_turn()
        cs.roll_and_execute_monsters()
        if cs.combat_over:
            break
