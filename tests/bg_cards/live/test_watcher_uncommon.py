"""Live verification tests for Watcher Uncommon cards.

Tests verify that Watcher uncommon card mechanics match between the live
BG mod game and the Rust simulator.

NOTE: make_sim() from conftest uses Character.Ironclad. We use a local
make_watcher_sim() that creates CombatState with Character.Watcher so
stance mechanics work correctly.
"""
import pytest
import sts_sim

from tests.live.conftest import (
    set_scenario, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
    CARD_TO_BG,
)


# ---------------------------------------------------------------------------
# Local helper: make_sim variant that uses Character.Watcher
# ---------------------------------------------------------------------------

def make_watcher_sim(*, hand=None, draw_pile=None, discard_pile=None,
                     energy=3, player_hp=9, player_block=0,
                     player_powers=None, player_relics=None,
                     monster_hp=30, monster_block=0, monster_powers=None,
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
    if isinstance(card_spec, tuple):
        return card_spec[0], card_spec[1]
    return card_spec, False


# ===================================================================
# ALL WATCHER UNCOMMON CARD TESTS
# ===================================================================

@pytest.mark.usefixtures("single_monster_fight")
class TestCards:

    # ===================================================================
    # CRUSH JOINTS
    # ===================================================================

    def test_crush_joints_neutral(self, game):
        """Crush Joints from Neutral: 1 damage, no Vulnerable."""
        hand = [sts_sim.Card.CrushJoints]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.CrushJoints, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_crush_joints_in_wrath(self, game):
        """Crush Joints in Wrath: doubled damage, applies Vulnerable."""
        hand = [sts_sim.Card.Crescendo, sts_sim.Card.CrushJoints]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
        state = play_named_card(game, sim, state, sts_sim.Card.CrushJoints, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_crush_joints_upgraded_wrath(self, game):
        """Upgraded Crush Joints in Wrath: 2 HIT x2 = 4 damage."""
        hand = [sts_sim.Card.Crescendo, (sts_sim.Card.CrushJoints, True)]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
        state = play_named_card(game, sim, state, sts_sim.Card.CrushJoints,
                                target_index=0, upgraded=True)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # FEAR NO EVIL
    # ===================================================================

    def test_fear_no_evil_neutral(self, game):
        """Fear No Evil from Neutral: 2 damage, stays Neutral."""
        hand = [sts_sim.Card.FearNoEvil]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.FearNoEvil, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_fear_no_evil_wrath(self, game):
        """Fear No Evil in Wrath: doubled damage, enters Calm."""
        hand = [sts_sim.Card.Crescendo, sts_sim.Card.FearNoEvil]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
        state = play_named_card(game, sim, state, sts_sim.Card.FearNoEvil, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # FOREIGN INFLUENCE
    # ===================================================================

    def test_foreign_influence_basic(self, game):
        """Foreign Influence: 3 damage, cost 0."""
        hand = [sts_sim.Card.ForeignInfluence]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.ForeignInfluence, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # SASH WHIP
    # ===================================================================

    def test_sash_whip_neutral(self, game):
        """Sash Whip from Neutral: 2 damage, no Weak."""
        hand = [sts_sim.Card.SashWhip]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.SashWhip, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # TANTRUM
    # ===================================================================

    def test_tantrum_basic(self, game):
        """Tantrum: 2 damage, enters Wrath, card to draw pile."""
        hand = [sts_sim.Card.Tantrum]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Tantrum, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # CARVE REALITY
    # ===================================================================

    def test_carve_reality_single(self, game):
        """Carve Reality: 3 damage to single target."""
        hand = [sts_sim.Card.CarveReality]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.CarveReality, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # SANDS OF TIME
    # ===================================================================

    def test_sands_of_time_basic(self, game):
        """Sands of Time: 3 damage, cost 2."""
        hand = [sts_sim.Card.SandsOfTime]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.SandsOfTime, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # WINDMILL STRIKE
    # ===================================================================

    def test_windmill_strike_base(self, game):
        """Windmill Strike: 2 base damage (not Retained)."""
        hand = [sts_sim.Card.WindmillStrike]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.WindmillStrike, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # WALLOP
    # ===================================================================

    def test_wallop_basic(self, game):
        """Wallop: 2 damage, gains 2 block."""
        hand = [sts_sim.Card.Wallop]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Wallop, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_wallop_enemy_block(self, game):
        """Wallop vs enemy with block: only unblocked damage becomes block."""
        hand = [sts_sim.Card.Wallop]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30, monster_block=1)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30, monster_block=1)
        state = play_named_card(game, sim, setup, sts_sim.Card.Wallop, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # WEAVE
    # ===================================================================

    def test_weave_basic(self, game):
        """Weave: 1 damage, cost 0."""
        hand = [sts_sim.Card.Weave]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Weave, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # SIGNATURE MOVE
    # ===================================================================

    def test_signature_move_only_attack(self, game):
        """Signature Move: 6 damage when only Attack in hand."""
        hand = [sts_sim.Card.SignatureMove, sts_sim.Card.DefendPurple,
                sts_sim.Card.DefendPurple]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.SignatureMove, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # CONCLUDE
    # ===================================================================

    def test_conclude_aoe(self, game):
        """Conclude: AOE 2 hits of 1 damage."""
        hand = [sts_sim.Card.Conclude]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Conclude)
        assert_monsters_match(state, sim)

    # ===================================================================
    # REACH HEAVEN
    # ===================================================================

    def test_reach_heaven_basic(self, game):
        """Reach Heaven: 2 base damage."""
        hand = [sts_sim.Card.ReachHeaven]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.ReachHeaven, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # EMPTY MIND
    # ===================================================================

    def test_empty_mind_draws(self, game):
        """Empty Mind draws 2 cards and exits stance."""
        hand = [sts_sim.Card.EmptyMind]
        draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple]
        setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.EmptyMind)
        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    # ===================================================================
    # MEDITATE
    # ===================================================================

    def test_meditate_basic(self, game):
        """MeditateCard: play and verify state matches."""
        hand = [sts_sim.Card.MeditateCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.MeditateCard)
        assert_player_matches(state, sim)

    # ===================================================================
    # INNER PEACE
    # ===================================================================

    def test_inner_peace_neutral(self, game):
        """Inner Peace from Neutral: enters Calm, no draw."""
        hand = [sts_sim.Card.InnerPeace]
        draw = [sts_sim.Card.StrikePurple] * 5
        setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.InnerPeace)
        assert_player_matches(state, sim)

    # ===================================================================
    # INDIGNATION
    # ===================================================================

    def test_indignation_neutral(self, game):
        """Indignation from Neutral: enters Wrath."""
        hand = [sts_sim.Card.Indignation]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Indignation)
        assert_player_matches(state, sim)

    # ===================================================================
    # SWIVEL
    # ===================================================================

    def test_swivel_block(self, game):
        """Swivel: 2 block, cost 2."""
        hand = [sts_sim.Card.Swivel]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Swivel)
        assert_player_matches(state, sim)

    # ===================================================================
    # PERSEVERANCE
    # ===================================================================

    def test_perseverance_base(self, game):
        """Perseverance: 1 block (not Retained)."""
        hand = [sts_sim.Card.Perseverance]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Perseverance)
        assert_player_matches(state, sim)

    # ===================================================================
    # PRAY
    # ===================================================================

    def test_pray_basic(self, game):
        """Pray: draws 2, costs 1."""
        hand = [sts_sim.Card.Pray]
        draw = [sts_sim.Card.StrikePurple] * 5
        setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Pray)
        assert_player_matches(state, sim)

    # ===================================================================
    # PROSTRATE
    # ===================================================================

    def test_prostrate_basic(self, game):
        """Prostrate: 1 block, cost 0."""
        hand = [sts_sim.Card.Prostrate]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Prostrate)
        assert_player_matches(state, sim)

    # ===================================================================
    # WREATH OF FLAME
    # ===================================================================

    def test_wreath_of_flame_x_cost(self, game):
        """Wreath of Flame (X=3): spends all energy, exhausts."""
        hand = [sts_sim.Card.WreathOfFlameCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.WreathOfFlameCard,
                                choices=[3])
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    # ===================================================================
    # UNCOMMON POWERS (play cost verification)
    # ===================================================================

    def test_battle_hymn_play(self, game):
        """BattleHymnCard: cost 1 power."""
        hand = [sts_sim.Card.BattleHymnCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.BattleHymnCard)
        assert_player_matches(state, sim)

    def test_simmering_fury_play(self, game):
        """SimmeringFuryCard: cost 1 power."""
        hand = [sts_sim.Card.SimmeringFuryCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.SimmeringFuryCard)
        assert_player_matches(state, sim)

    def test_mental_fortress_play(self, game):
        """MentalFortressCard: cost 1 power."""
        hand = [sts_sim.Card.MentalFortressCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.MentalFortressCard)
        assert_player_matches(state, sim)

    def test_nirvana_play(self, game):
        """NirvanaCard: cost 1 power."""
        hand = [sts_sim.Card.NirvanaCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.NirvanaCard)
        assert_player_matches(state, sim)

    def test_like_water_play(self, game):
        """LikeWaterCard: cost 1 power."""
        hand = [sts_sim.Card.LikeWaterCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.LikeWaterCard)
        assert_player_matches(state, sim)

    def test_foresight_play(self, game):
        """ForesightCard: cost 1 power."""
        hand = [sts_sim.Card.ForesightCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.ForesightCard)
        assert_player_matches(state, sim)

    def test_study_play(self, game):
        """StudyCard: cost 2 power."""
        hand = [sts_sim.Card.StudyCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.StudyCard)
        assert_player_matches(state, sim)

    def test_rushdown_play(self, game):
        """RushdownCard: cost 1 power."""
        hand = [sts_sim.Card.RushdownCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.RushdownCard)
        assert_player_matches(state, sim)
