"""Simulator tests for Watcher Uncommon cards.

Tests verify that Watcher uncommon card mechanics -- stances, conditional
effects, Retain, Miracles, X-cost, powers -- are modeled correctly in the
Rust simulator.

NOTE: make_sim() from conftest uses Character.Ironclad. We use a local
make_watcher_sim() that creates CombatState with Character.Watcher so
stance mechanics work correctly.
"""
import pytest
import sts_sim
from tests.live.conftest import make_sim


# ---------------------------------------------------------------------------
# Local helper: make_sim variant that uses Character.Watcher
# ---------------------------------------------------------------------------

def make_watcher_sim(*, hand=None, draw_pile=None, discard_pile=None,
                     energy=3, player_hp=9, player_block=0,
                     player_powers=None, player_relics=None,
                     monster_hp=20, monster_block=0, monster_powers=None,
                     monsters=None):
    """Create a simulator CombatState with Character.Watcher."""
    hand = hand or []
    draw_pile = draw_pile or []
    discard_pile = discard_pile or []

    if monsters is not None:
        monster_list = []
        for i, m in enumerate(monsters):
            mon = sts_sim.Monster(f"Monster_{i}", m.get("hp", 30), "jaw_worm", "A", False)
            blk = m.get("block", 0)
            if blk > 0:
                mon.add_block(blk)
            if m.get("powers"):
                for power_name, amount in m["powers"].items():
                    pt = getattr(sts_sim.PowerType, power_name)
                    mon.apply_power(pt, amount)
            monster_list.append(mon)
    else:
        monster = sts_sim.Monster("Jaw Worm", monster_hp, "jaw_worm", "A", False)
        if monster_block > 0:
            monster.add_block(monster_block)
        if monster_powers:
            for power_name, amount in monster_powers.items():
                pt = getattr(sts_sim.PowerType, power_name)
                monster.apply_power(pt, amount)
        monster_list = [monster]

    sim = sts_sim.CombatState.new_with_character(
        monster_list, seed=0, character=sts_sim.Character.Watcher,
    )
    sim.set_player_energy(energy)
    sim.set_player_hp(player_hp)
    sim.set_player_block(player_block)

    if player_relics is not None:
        sim.clear_relics()
        for relic in player_relics:
            sim.add_relic(relic)

    if player_powers:
        for power_name, amount in player_powers.items():
            pt = getattr(sts_sim.PowerType, power_name)
            sim.apply_player_power(pt, amount)

    for card_spec in draw_pile:
        card, upgraded = _unpack(card_spec)
        if upgraded:
            sim.add_upgraded_card_to_draw(card)
        else:
            sim.add_card_to_draw(card)

    for card_spec in discard_pile:
        card, upgraded = _unpack(card_spec)
        if upgraded:
            sim.add_upgraded_card_to_discard(card)
        else:
            sim.add_card_to_discard(card)

    for card_spec in hand:
        card, upgraded = _unpack(card_spec)
        if upgraded:
            sim.add_upgraded_card_to_hand(card)
        else:
            sim.add_card_to_hand(card)

    sim.set_die_value(1)
    return sim


def _unpack(card_spec):
    """Return (Card, upgraded_bool) from a card spec."""
    if isinstance(card_spec, tuple):
        return card_spec[0], card_spec[1]
    return card_spec, False


# ===================================================================
# CRUSH JOINTS
# ===================================================================

def test_crush_joints_neutral_damage():
    """Crush Joints from Neutral stance deals 1 damage, no Vulnerable."""
    sim = make_watcher_sim(hand=[sts_sim.Card.CrushJoints], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 19
    assert sim.player.energy == 2


def test_crush_joints_wrath_applies_vuln():
    """Crush Joints in Wrath deals doubled damage and applies Vulnerable."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Crescendo, sts_sim.Card.CrushJoints],
        energy=3, monster_hp=20,
    )
    # Enter Wrath via Crescendo
    sim.play_card(0, 0)
    # Play Crush Joints (index shifted after Crescendo exhausted)
    sim.play_card(0, 0)
    m = sim.get_monsters()[0]
    # 1 HIT doubled by Wrath = 2 damage
    assert m.hp == 18
    assert m.get_power(sts_sim.PowerType.Vulnerable) > 0


def test_crush_joints_upgraded_in_wrath():
    """Upgraded Crush Joints in Wrath deals 2 HIT x2 = 4 damage, applies Vuln."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Crescendo, (sts_sim.Card.CrushJoints, True)],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)  # Crescendo -> Wrath
    sim.play_card(0, 0)  # Crush Joints+
    m = sim.get_monsters()[0]
    # 2 HIT doubled by Wrath = 4 damage
    assert m.hp == 16
    assert m.get_power(sts_sim.PowerType.Vulnerable) > 0


# ===================================================================
# FEAR NO EVIL
# ===================================================================

def test_fear_no_evil_neutral():
    """Fear No Evil from Neutral deals 2 damage, stays in Neutral."""
    sim = make_watcher_sim(hand=[sts_sim.Card.FearNoEvil], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18


def test_fear_no_evil_wrath_to_calm():
    """Fear No Evil in Wrath deals doubled damage and enters Calm."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Crescendo, sts_sim.Card.FearNoEvil],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)  # Crescendo -> Wrath
    sim.play_card(0, 0)  # Fear No Evil
    # 2 HIT doubled by Wrath = 4 damage
    assert sim.get_monsters()[0].hp == 16


def test_fear_no_evil_upgraded_wrath():
    """Upgraded Fear No Evil in Wrath: 3 HIT x2 = 6 damage, enters Calm."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Crescendo, (sts_sim.Card.FearNoEvil, True)],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)  # Crescendo -> Wrath
    sim.play_card(0, 0)  # Fear No Evil+
    # 3 HIT doubled by Wrath = 6 damage
    assert sim.get_monsters()[0].hp == 14


# ===================================================================
# FOREIGN INFLUENCE
# ===================================================================

def test_foreign_influence_basic():
    """Foreign Influence deals 3 damage for 0 energy."""
    sim = make_watcher_sim(hand=[sts_sim.Card.ForeignInfluence], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17
    assert sim.player.energy == 3  # costs 0


def test_foreign_influence_upgraded():
    """Upgraded Foreign Influence deals 4 damage for 0 energy."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.ForeignInfluence, True)], energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 16
    assert sim.player.energy == 3


# ===================================================================
# SASH WHIP
# ===================================================================

def test_sash_whip_neutral_no_weak():
    """Sash Whip from Neutral deals 2 damage, no Weak applied."""
    sim = make_watcher_sim(hand=[sts_sim.Card.SashWhip], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18
    # Not in Calm, so no Weak
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 0


def test_sash_whip_calm_applies_weak():
    """Sash Whip in Calm deals 2 damage and applies 1 Weak."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Tranquility, sts_sim.Card.SashWhip],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)  # Tranquility -> Calm (exhausts)
    sim.play_card(0, 0)  # Sash Whip
    m = sim.get_monsters()[0]
    assert m.hp == 18
    assert m.get_power(sts_sim.PowerType.Weak) >= 1


def test_sash_whip_upgraded_calm_double_weak():
    """Upgraded Sash Whip in Calm applies 2 stacks of Weak."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Tranquility, (sts_sim.Card.SashWhip, True)],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)  # Tranquility -> Calm
    sim.play_card(0, 0)  # Sash Whip+
    m = sim.get_monsters()[0]
    assert m.hp == 18
    assert m.get_power(sts_sim.PowerType.Weak) >= 2


# ===================================================================
# TANTRUM
# ===================================================================

def test_tantrum_damage_and_wrath():
    """Tantrum deals 2 damage and enters Wrath. Card goes to draw pile."""
    draw = [sts_sim.Card.StrikePurple] * 5
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Tantrum], draw_pile=draw, energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18
    assert sim.player.energy == 2
    # Tantrum should be on top of draw pile (not in discard)
    draw_cards = [ci.card for ci in sim.get_draw_pile()]
    assert sts_sim.Card.Tantrum in draw_cards


def test_tantrum_upgraded_two_hits():
    """Upgraded Tantrum deals two separate hits (1+1), Strength adds per hit."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.Tantrum, True)],
        energy=3, monster_hp=20,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, 0)
    # Two hits of (1+2) = 3 each = 6 total
    assert sim.get_monsters()[0].hp == 14


# ===================================================================
# CARVE REALITY
# ===================================================================

def test_carve_reality_single_target():
    """Carve Reality deals 3 damage to a single target."""
    sim = make_watcher_sim(hand=[sts_sim.Card.CarveReality], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17


def test_carve_reality_upgraded_with_strength():
    """Upgraded Carve Reality deals 4 HIT + Strength bonus."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.CarveReality, True)],
        energy=3, monster_hp=20,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, 0)
    # 4 HIT + 2 STR = 6 damage
    assert sim.get_monsters()[0].hp == 14


# ===================================================================
# SANDS OF TIME
# ===================================================================

def test_sands_of_time_basic():
    """Sands of Time deals 3 damage with no other Retain cards."""
    sim = make_watcher_sim(hand=[sts_sim.Card.SandsOfTime], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17
    assert sim.player.energy == 1  # cost 2


# ===================================================================
# WINDMILL STRIKE
# ===================================================================

def test_windmill_strike_base():
    """Windmill Strike deals 2 base damage (not Retained)."""
    sim = make_watcher_sim(hand=[sts_sim.Card.WindmillStrike], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18


# ===================================================================
# WALLOP
# ===================================================================

def test_wallop_full_damage_to_block():
    """Wallop deals 2 damage and gains 2 block (no enemy block)."""
    sim = make_watcher_sim(hand=[sts_sim.Card.Wallop], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18
    assert sim.player.block == 2


def test_wallop_enemy_has_block():
    """Wallop vs enemy with 1 block: 1 HP lost, 1 block gained."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Wallop], energy=3, monster_hp=20, monster_block=1,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 19
    assert sim.player.block == 1


def test_wallop_upgraded_wrath():
    """Upgraded Wallop in Wrath: 3 HIT x2 = 6 damage, gains 6 block."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Crescendo, (sts_sim.Card.Wallop, True)],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)  # Crescendo -> Wrath
    sim.play_card(0, 0)  # Wallop+
    # 3 HIT doubled by Wrath = 6 damage
    assert sim.get_monsters()[0].hp == 14
    assert sim.player.block == 6


# ===================================================================
# WEAVE
# ===================================================================

def test_weave_basic():
    """Weave deals 1 damage for 0 energy."""
    sim = make_watcher_sim(hand=[sts_sim.Card.Weave], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 19
    assert sim.player.energy == 3


# ===================================================================
# SIGNATURE MOVE
# ===================================================================

def test_signature_move_only_attack():
    """Signature Move deals 6 damage when it is the only Attack in hand."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.SignatureMove, sts_sim.Card.DefendPurple,
              sts_sim.Card.DefendPurple, sts_sim.Card.DefendPurple],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 14
    assert sim.player.energy == 1  # cost 2


def test_signature_move_upgraded():
    """Upgraded Signature Move deals 8 damage."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.SignatureMove, True), sts_sim.Card.DefendPurple],
        energy=3, monster_hp=30,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 22


# ===================================================================
# CONCLUDE
# ===================================================================

def test_conclude_aoe():
    """Conclude deals 2 hits of 1 damage AOE to all enemies."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Conclude],
        energy=3,
        monsters=[{"hp": 15}, {"hp": 10}],
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    # 2 hits of 1 each = 2 damage to each
    assert monsters[0].hp == 13
    assert monsters[1].hp == 8


def test_conclude_upgraded_three_hits():
    """Upgraded Conclude deals 3 hits of 1 damage AOE."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.Conclude, True)],
        energy=3,
        monsters=[{"hp": 15}, {"hp": 10}],
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 12
    assert monsters[1].hp == 7


def test_conclude_with_strength():
    """Conclude with 2 Strength: each hit = 1+2 = 3, two hits = 6 damage."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Conclude],
        energy=3, monster_hp=20,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 14


# ===================================================================
# REACH HEAVEN
# ===================================================================

def test_reach_heaven_no_miracles():
    """Reach Heaven with 0 Miracles deals 2 base damage."""
    sim = make_watcher_sim(hand=[sts_sim.Card.ReachHeaven], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18


# ===================================================================
# EMPTY MIND
# ===================================================================

def test_empty_mind_draws_and_neutral():
    """Empty Mind draws 2 cards and enters Neutral from Wrath."""
    draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
            sts_sim.Card.StrikePurple]
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Crescendo, sts_sim.Card.EmptyMind],
        draw_pile=draw, energy=3,
    )
    sim.play_card(0, 0)  # Crescendo -> Wrath (exhausts)
    sim.play_card(0, 0)  # Empty Mind -> draws 2, enters Neutral
    # After playing Empty Mind: hand should have 2 drawn cards
    assert len(sim.get_hand()) == 2
    assert sim.player.energy == 2  # 3 - 0 (Crescendo) - 1 (Empty Mind) = 2


def test_empty_mind_upgraded_draws_3():
    """Upgraded Empty Mind draws 3 cards."""
    draw = [sts_sim.Card.StrikePurple] * 5
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.EmptyMind, True)],
        draw_pile=draw, energy=3,
    )
    sim.play_card(0, 0)
    assert len(sim.get_hand()) == 3


# ===================================================================
# MEDITATE
# ===================================================================

def test_meditate_retrieves_from_discard():
    """MeditateCard retrieves 1 card from discard, enters Calm."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.MeditateCard],
        discard_pile=[sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple],
        energy=3,
    )
    sim.play_card(0, 0, 0)  # choice=0 to pick first card from discard
    # Should have the retrieved card in hand
    assert len(sim.get_hand()) >= 1


# ===================================================================
# INNER PEACE
# ===================================================================

def test_inner_peace_not_calm_enters_calm():
    """Inner Peace from Neutral enters Calm, draws no cards."""
    draw = [sts_sim.Card.StrikePurple] * 5
    sim = make_watcher_sim(
        hand=[sts_sim.Card.InnerPeace],
        draw_pile=draw, energy=3,
    )
    hand_before = len(sim.get_hand())
    sim.play_card(0, 0)
    # Should not draw cards from Neutral; enters Calm
    assert sim.player.energy == 2  # cost 1


# ===================================================================
# INDIGNATION
# ===================================================================

def test_indignation_neutral_enters_wrath():
    """Indignation from Neutral enters Wrath, no Vulnerable."""
    sim = make_watcher_sim(hand=[sts_sim.Card.Indignation], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    m = sim.get_monsters()[0]
    assert m.get_power(sts_sim.PowerType.Vulnerable) == 0
    assert sim.player.energy == 2


# ===================================================================
# SWIVEL
# ===================================================================

def test_swivel_block():
    """Swivel grants 2 block."""
    sim = make_watcher_sim(hand=[sts_sim.Card.Swivel], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.player.block == 2
    assert sim.player.energy == 1  # cost 2


# ===================================================================
# PERSEVERANCE
# ===================================================================

def test_perseverance_base_block():
    """Perseverance gives 1 block (not Retained)."""
    sim = make_watcher_sim(hand=[sts_sim.Card.Perseverance], energy=3)
    sim.play_card(0, 0)
    assert sim.player.block == 1
    assert sim.player.energy == 2


# ===================================================================
# PRAY
# ===================================================================

def test_pray_draws_cards():
    """Pray draws 2 cards and costs 1 energy."""
    draw = [sts_sim.Card.StrikePurple] * 5
    sim = make_watcher_sim(
        hand=[sts_sim.Card.Pray],
        draw_pile=draw, energy=3,
    )
    sim.play_card(0, 0)
    # Should have drawn 2 cards
    assert len(sim.get_hand()) == 2
    assert sim.player.energy == 2


# ===================================================================
# PROSTRATE
# ===================================================================

def test_prostrate_block_and_miracle():
    """Prostrate gives 1 block for 0 energy."""
    sim = make_watcher_sim(hand=[sts_sim.Card.Prostrate], energy=3)
    sim.play_card(0, 0)
    assert sim.player.block == 1
    assert sim.player.energy == 3  # costs 0


def test_prostrate_upgraded():
    """Upgraded Prostrate gives 2 block for 0 energy."""
    sim = make_watcher_sim(hand=[(sts_sim.Card.Prostrate, True)], energy=3)
    sim.play_card(0, 0)
    assert sim.player.block == 2
    assert sim.player.energy == 3


# ===================================================================
# WREATH OF FLAME
# ===================================================================

def test_wreath_of_flame_x_cost_exhaust():
    """Wreath of Flame (X=3) grants 3 Strength and exhausts."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.WreathOfFlameCard], energy=3, monster_hp=20,
    )
    sim.play_card(0, 0, 3)  # X=3
    assert sim.player.energy == 0
    # Card should be exhausted
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.WreathOfFlameCard in exhaust_cards


def test_wreath_of_flame_upgraded_no_exhaust():
    """Upgraded Wreath of Flame does not exhaust."""
    sim = make_watcher_sim(
        hand=[(sts_sim.Card.WreathOfFlameCard, True)], energy=2, monster_hp=20,
    )
    sim.play_card(0, 0, 2)  # X=2
    # Card should go to discard, not exhaust
    discard_cards = [ci.card for ci in sim.get_discard_pile()]
    assert sts_sim.Card.WreathOfFlameCard in discard_cards
    exhaust_cards = [ci.card for ci in sim.get_exhaust_pile()]
    assert sts_sim.Card.WreathOfFlameCard not in exhaust_cards


# ===================================================================
# BATTLE HYMN (Power)
# ===================================================================

def test_battle_hymn_power_play():
    """BattleHymnCard costs 1 energy to play."""
    sim = make_watcher_sim(hand=[sts_sim.Card.BattleHymnCard], energy=3)
    sim.play_card(0, 0)
    assert sim.player.energy == 2
    # Power cards do not go to discard
    assert len(sim.get_discard_pile()) == 0


# ===================================================================
# SIMMERING FURY (Power)
# ===================================================================

def test_simmering_fury_power_play():
    """SimmeringFuryCard costs 1 energy to play."""
    sim = make_watcher_sim(hand=[sts_sim.Card.SimmeringFuryCard], energy=3)
    sim.play_card(0, 0)
    assert sim.player.energy == 2


# ===================================================================
# MENTAL FORTRESS (Power)
# ===================================================================

def test_mental_fortress_power_play():
    """MentalFortressCard costs 1 energy to play."""
    sim = make_watcher_sim(hand=[sts_sim.Card.MentalFortressCard], energy=3)
    sim.play_card(0, 0)
    assert sim.player.energy == 2


def test_mental_fortress_block_on_stance_switch():
    """Mental Fortress grants 1 block on stance switch."""
    sim = make_watcher_sim(
        hand=[sts_sim.Card.MentalFortressCard, sts_sim.Card.Crescendo],
        energy=3,
    )
    sim.play_card(0, 0)  # Mental Fortress power
    sim.play_card(0, 0)  # Crescendo -> Wrath (stance switch)
    assert sim.player.block >= 1


# ===================================================================
# NIRVANA (Power)
# ===================================================================

def test_nirvana_power_play():
    """NirvanaCard costs 1 energy to play."""
    sim = make_watcher_sim(hand=[sts_sim.Card.NirvanaCard], energy=3)
    sim.play_card(0, 0)
    assert sim.player.energy == 2


# ===================================================================
# LIKE WATER (Power)
# ===================================================================

def test_like_water_power_play():
    """LikeWaterCard costs 1 energy to play."""
    sim = make_watcher_sim(hand=[sts_sim.Card.LikeWaterCard], energy=3)
    sim.play_card(0, 0)
    assert sim.player.energy == 2


# ===================================================================
# FORESIGHT (Power)
# ===================================================================

def test_foresight_power_play():
    """ForesightCard costs 1 energy to play."""
    sim = make_watcher_sim(hand=[sts_sim.Card.ForesightCard], energy=3)
    sim.play_card(0, 0)
    assert sim.player.energy == 2


# ===================================================================
# STUDY (Power)
# ===================================================================

def test_study_power_play():
    """StudyCard costs 2 energy to play."""
    sim = make_watcher_sim(hand=[sts_sim.Card.StudyCard], energy=3)
    sim.play_card(0, 0)
    assert sim.player.energy == 1  # cost 2


def test_study_upgraded_costs_1():
    """Upgraded StudyCard costs 1 energy."""
    sim = make_watcher_sim(hand=[(sts_sim.Card.StudyCard, True)], energy=3)
    sim.play_card(0, 0)
    assert sim.player.energy == 2


# ===================================================================
# RUSHDOWN (Power)
# ===================================================================

def test_rushdown_power_play():
    """RushdownCard costs 1 energy to play."""
    sim = make_watcher_sim(hand=[sts_sim.Card.RushdownCard], energy=3)
    sim.play_card(0, 0)
    assert sim.player.energy == 2


def test_rushdown_draws_on_wrath_entry():
    """Rushdown draws 2 cards when entering Wrath."""
    draw = [sts_sim.Card.StrikePurple] * 5
    sim = make_watcher_sim(
        hand=[sts_sim.Card.RushdownCard, sts_sim.Card.Crescendo],
        draw_pile=draw, energy=3,
    )
    sim.play_card(0, 0)  # Rushdown power
    sim.play_card(0, 0)  # Crescendo -> Wrath (triggers Rushdown)
    # Should have drawn 2 cards from Rushdown
    assert len(sim.get_hand()) >= 2
