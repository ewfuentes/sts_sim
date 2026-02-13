"""Live verification tests for Silent Rare cards.

Each test:
1. Uses the set command to configure a precise game state
2. Plays a card in both the live game and the simulator
3. Asserts that results match between live game and simulator
"""

import pytest
import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
)


@pytest.mark.usefixtures("two_monster_fight")
class TestAOE:

    # ===========================================================================
    # Die Die Die
    # ===========================================================================

    def test_die_die_die_aoe(self, game):
        """Die Die Die deals 3 AOE damage, exhausts."""
        hand = [sts_sim.Card.DieDieDie]

        set_scenario(game, hand=hand, energy=3,
                     monsters=[{"hp": 20}, {"hp": 15}])
        sim = make_sim(hand=hand, energy=3,
                       monsters=[{"hp": 20}, {"hp": 15}])

        state = play_card_both(game, sim, hand_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_die_die_die_upgraded(self, game):
        """Die Die Die+ deals 4 AOE damage, exhausts."""
        hand = [(sts_sim.Card.DieDieDie, True)]

        set_scenario(game, hand=hand, energy=3,
                     monsters=[{"hp": 20}, {"hp": 15}])
        sim = make_sim(hand=hand, energy=3,
                       monsters=[{"hp": 20}, {"hp": 15}])

        state = play_card_both(game, sim, hand_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_die_die_die_with_strength(self, game):
        """Die Die Die with 2 STR: 3*(1+2)=9 AOE damage."""
        hand = [sts_sim.Card.DieDieDie]

        set_scenario(game, hand=hand, energy=3,
                     player_powers={"Strength": 2},
                     monsters=[{"hp": 20}, {"hp": 15}])
        sim = make_sim(hand=hand, energy=3,
                       player_powers={"Strength": 2},
                       monsters=[{"hp": 20}, {"hp": 15}])

        state = play_card_both(game, sim, hand_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Grand Finale
    # ===========================================================================

    def test_grand_finale_empty_draw(self, game):
        """Grand Finale deals 10 AOE damage with empty draw pile."""
        hand = [sts_sim.Card.GrandFinale]

        set_scenario(game, hand=hand, energy=3,
                     monsters=[{"hp": 20}, {"hp": 15}])
        sim = make_sim(hand=hand, energy=3,
                       monsters=[{"hp": 20}, {"hp": 15}])

        state = play_card_both(game, sim, hand_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_grand_finale_upgraded(self, game):
        """Grand Finale+ deals 12 AOE damage with empty draw pile."""
        hand = [(sts_sim.Card.GrandFinale, True)]

        set_scenario(game, hand=hand, energy=3,
                     monsters=[{"hp": 20}, {"hp": 20}])
        sim = make_sim(hand=hand, energy=3,
                       monsters=[{"hp": 20}, {"hp": 20}])

        state = play_card_both(game, sim, hand_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)


@pytest.mark.usefixtures("single_monster_fight")
class TestSingleTarget:

    # ===========================================================================
    # Grand Finale
    # ===========================================================================

    def test_grand_finale_with_strength(self, game):
        """Grand Finale with 1 STR: 10*(1+1)=20 damage."""
        hand = [sts_sim.Card.GrandFinale]

        set_scenario(game, hand=hand, energy=3, monster_hp=30,
                     player_powers={"Strength": 1})
        sim = make_sim(hand=hand, energy=3, monster_hp=30,
                       player_powers={"Strength": 1})

        state = play_card_both(game, sim, hand_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Skewer
    # ===========================================================================

    def test_skewer_with_3_energy(self, game):
        """Skewer with X=3: 1*(3+1)=4 damage."""
        hand = [sts_sim.Card.Skewer]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0,
                               choices=[3])

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_skewer_with_0_energy(self, game):
        """Skewer with X=0: 1 damage."""
        hand = [sts_sim.Card.Skewer]

        set_scenario(game, hand=hand, energy=0, monster_hp=20)
        sim = make_sim(hand=hand, energy=0, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0,
                               choices=[0])

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_skewer_upgraded_with_3_energy(self, game):
        """Skewer+ with X=3: 2*3=6 damage."""
        hand = [(sts_sim.Card.Skewer, True)]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0,
                               choices=[3])

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_skewer_with_strength(self, game):
        """Skewer with 2 STR, X=2: (1+2)*(2+1)=9 damage."""
        hand = [sts_sim.Card.Skewer]

        set_scenario(game, hand=hand, energy=2, monster_hp=20,
                     player_powers={"Strength": 2})
        sim = make_sim(hand=hand, energy=2, monster_hp=20,
                       player_powers={"Strength": 2})

        state = play_card_both(game, sim, hand_index=0, target_index=0,
                               choices=[2])

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Adrenaline
    # ===========================================================================

    def test_adrenaline_basic(self, game):
        """Adrenaline: +2 energy, draw 2, exhaust."""
        hand = [sts_sim.Card.Adrenaline]
        draw = [sts_sim.Card.StrikeGreen] * 5

        set_scenario(game, hand=hand, draw_pile=draw, energy=0, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=0, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_adrenaline_as_turn_starter(self, game):
        """Adrenaline with 3 energy: 5 energy, draw 2, exhaust."""
        hand = [
            sts_sim.Card.Adrenaline,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ]
        draw = [sts_sim.Card.StrikeGreen] * 5

        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)
        assert_exhaust_matches(state, sim)

    # ===========================================================================
    # Bullet Time
    # ===========================================================================

    def test_bullet_time_basic(self, game):
        """Bullet Time costs 3. Cards cost 0 this turn."""
        hand = [
            sts_sim.Card.BulletTime,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)

    def test_bullet_time_upgraded(self, game):
        """Bullet Time+ costs 2."""
        hand = [
            (sts_sim.Card.BulletTime, True),
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)

    # ===========================================================================
    # Malaise
    # ===========================================================================

    def test_malaise_with_3_energy(self, game):
        """Malaise with X=3: 3 WEAK, 3 POISON. Exhausts."""
        hand = [sts_sim.Card.Malaise]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0,
                               choices=[3])

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_malaise_with_1_energy(self, game):
        """Malaise with X=1: 1 WEAK, 1 POISON."""
        hand = [sts_sim.Card.Malaise]

        set_scenario(game, hand=hand, energy=1, monster_hp=20)
        sim = make_sim(hand=hand, energy=1, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0,
                               choices=[1])

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_malaise_upgraded_with_2_energy(self, game):
        """Malaise+ with X=2: applies X+1=3 WEAK and 3 POISON."""
        hand = [(sts_sim.Card.Malaise, True)]

        set_scenario(game, hand=hand, energy=2, monster_hp=20)
        sim = make_sim(hand=hand, energy=2, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0,
                               choices=[2])

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    # ===========================================================================
    # Corpse Explosion
    # ===========================================================================

    def test_corpse_explosion_applies_poison(self, game):
        """Corpse Explosion applies 2 POISON."""
        hand = [sts_sim.Card.CorpseExplosionCard]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_corpse_explosion_upgraded(self, game):
        """Corpse Explosion+ applies 3 POISON."""
        hand = [(sts_sim.Card.CorpseExplosionCard, True)]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # A Thousand Cuts
    # ===========================================================================

    def test_a_thousand_cuts_plays(self, game):
        """A Thousand Cuts can be played as a power. Costs 2."""
        hand = [sts_sim.Card.AThousandCutsCard]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)

    # ===========================================================================
    # Burst
    # ===========================================================================

    def test_burst_doubles_next_skill(self, game):
        """Burst doubles the next Skill: Leg Sweep x2 = 2 WEAK, 6 block."""
        hand = [sts_sim.Card.BurstCard, sts_sim.Card.LegSweep]

        setup = set_scenario(game, hand=hand, energy=3, player_block=0,
                             monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)

        state = play_named_card(game, sim, setup, sts_sim.Card.BurstCard)
        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_burst_upgraded_costs_0(self, game):
        """Burst+ costs 0 energy. Doubles next Skill."""
        hand = [(sts_sim.Card.BurstCard, True), sts_sim.Card.DeadlyPoison]

        setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_named_card(game, sim, setup, sts_sim.Card.BurstCard,
                                upgraded=True)
        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_burst_does_not_double_attacks(self, game):
        """Burst does NOT double Attacks."""
        hand = [sts_sim.Card.BurstCard, sts_sim.Card.StrikeGreen]

        setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_named_card(game, sim, setup, sts_sim.Card.BurstCard)
        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Envenom
    # ===========================================================================

    def test_envenom_adds_poison(self, game):
        """Envenom adds POISON to HIT attacks."""
        hand = [sts_sim.Card.EnvenomCard, sts_sim.Card.StrikeGreen]

        setup = set_scenario(game, hand=hand, energy=4, monster_hp=20)
        sim = make_sim(hand=hand, energy=4, monster_hp=20)

        state = play_named_card(game, sim, setup, sts_sim.Card.EnvenomCard)
        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_envenom_upgraded_costs_2(self, game):
        """Envenom+ costs 2 energy."""
        hand = [(sts_sim.Card.EnvenomCard, True)]

        set_scenario(game, hand=hand, energy=2, monster_hp=20)
        sim = make_sim(hand=hand, energy=2, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)

    # ===========================================================================
    # Tools of the Trade
    # ===========================================================================

    def test_tools_of_the_trade_plays(self, game):
        """Tools of the Trade can be played as a power. Costs 1."""
        hand = [sts_sim.Card.ToolsOfTheTradeCard]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)

    def test_tools_of_the_trade_upgraded(self, game):
        """Tools of the Trade+ costs 0."""
        hand = [(sts_sim.Card.ToolsOfTheTradeCard, True)]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)

    # ===========================================================================
    # Wraith Form
    # ===========================================================================

    def test_wraith_form_plays(self, game):
        """Wraith Form can be played as a power. Costs 3."""
        hand = [sts_sim.Card.WraithFormCard]

        set_scenario(game, hand=hand, energy=3, player_hp=20, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_hp=20, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
