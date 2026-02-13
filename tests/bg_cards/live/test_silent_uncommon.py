"""Live verification tests for Silent Uncommon cards.

Each test:
1. Uses the set command to configure a precise game state
2. Plays a card in both the live game and the simulator
3. Asserts that results match between live game and simulator
"""

import pytest
import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    end_turn_both, assert_monsters_match, assert_player_matches,
    assert_powers_match,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
)


@pytest.mark.usefixtures("single_monster_fight")
class TestSingleTarget:

    # ===========================================================================
    # Backstab
    # ===========================================================================

    def test_backstab_full_hp_bonus(self, game):
        """Backstab deals 2+2=4 damage when enemy is at full HP. Exhausts."""
        hand = [sts_sim.Card.Backstab]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_backstab_upgraded_full_hp_with_strength(self, game):
        """Backstab+ deals 4*(1+1)+2=10 damage with 1 STR against full HP."""
        hand = [(sts_sim.Card.Backstab, True)]

        set_scenario(game, hand=hand, energy=3, monster_hp=20,
                     player_powers={"Strength": 1})
        sim = make_sim(hand=hand, energy=3, monster_hp=20,
                       player_powers={"Strength": 1})

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    # ===========================================================================
    # Bane
    # ===========================================================================

    def test_bane_poisoned_enemy(self, game):
        """Bane deals 2+2=4 damage when enemy has POISON."""
        hand = [sts_sim.Card.Bane]

        set_scenario(game, hand=hand, energy=3, monster_hp=20,
                     monster_powers={"Poison": 3})
        sim = make_sim(hand=hand, energy=3, monster_hp=20,
                       monster_powers={"Poison": 3})

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_bane_no_poison(self, game):
        """Bane deals 2 damage when enemy has no POISON."""
        hand = [sts_sim.Card.Bane]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_bane_upgraded_poisoned_with_strength(self, game):
        """Bane+ deals 3*(1+2)+2=11 damage with 2 STR against poisoned enemy."""
        hand = [(sts_sim.Card.Bane, True)]

        set_scenario(game, hand=hand, energy=3, monster_hp=30,
                     player_powers={"Strength": 2},
                     monster_powers={"Poison": 1})
        sim = make_sim(hand=hand, energy=3, monster_hp=30,
                       player_powers={"Strength": 2},
                       monster_powers={"Poison": 1})

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Choke
    # ===========================================================================

    def test_choke_with_debuffs(self, game):
        """Choke deals 3*(1+2+3)=18 against enemy with 2 WEAK, 3 POISON."""
        hand = [sts_sim.Card.Choke]

        set_scenario(game, hand=hand, energy=3, monster_hp=30,
                     monster_powers={"Weak": 2, "Poison": 3})
        sim = make_sim(hand=hand, energy=3, monster_hp=30,
                       monster_powers={"Weak": 2, "Poison": 3})

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_choke_no_debuffs(self, game):
        """Choke deals 3 damage against clean enemy."""
        hand = [sts_sim.Card.Choke]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_choke_upgraded_debuffed(self, game):
        """Choke+ deals 4*(1+1+1)=12 against enemy with 1 WEAK, 1 POISON."""
        hand = [(sts_sim.Card.Choke, True)]

        set_scenario(game, hand=hand, energy=3, monster_hp=25,
                     monster_powers={"Weak": 1, "Poison": 1})
        sim = make_sim(hand=hand, energy=3, monster_hp=25,
                       monster_powers={"Weak": 1, "Poison": 1})

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Predator
    # ===========================================================================

    def test_predator_damage_and_draw(self, game):
        """Predator deals 3 damage and draws 2 cards."""
        hand = [sts_sim.Card.Predator]
        draw = [sts_sim.Card.StrikeGreen] * 5

        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    def test_predator_upgraded(self, game):
        """Predator+ deals 4 damage and draws 2 cards."""
        hand = [(sts_sim.Card.Predator, True)]
        draw = [sts_sim.Card.StrikeGreen] * 5

        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    def test_predator_with_strength(self, game):
        """Predator with 2 STR: 3*(1+2)=9 damage."""
        hand = [sts_sim.Card.Predator]
        draw = [sts_sim.Card.StrikeGreen] * 5

        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20,
                     player_powers={"Strength": 2})
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20,
                       player_powers={"Strength": 2})

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Masterful Stab
    # ===========================================================================

    def test_masterful_stab_full_cost(self, game):
        """Masterful Stab costs 4 energy, deals 2 damage (no HP lost)."""
        hand = [sts_sim.Card.MasterfulStab]

        set_scenario(game, hand=hand, energy=4, monster_hp=20)
        sim = make_sim(hand=hand, energy=4, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Dash
    # ===========================================================================

    def test_dash_damage_and_block(self, game):
        """Dash deals 2 damage and grants 2 block."""
        hand = [sts_sim.Card.Dash]

        set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_dash_upgraded(self, game):
        """Dash+ deals 3 damage and grants 3 block."""
        hand = [(sts_sim.Card.Dash, True)]

        set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_dash_with_footwork(self, game):
        """Dash with Footwork: 2 damage, 2*(1+1)=4 block."""
        hand = [sts_sim.Card.Dash]

        set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20,
                     player_powers={"Dexterity": 1})
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20,
                       player_powers={"Dexterity": 1})

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Finisher
    # ===========================================================================

    def test_finisher_after_3_attacks(self, game):
        """Finisher deals 3 damage after 3 attacks played this turn."""
        hand = [
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.Finisher,
        ]

        setup = set_scenario(game, hand=hand, energy=10, monster_hp=30)
        sim = make_sim(hand=hand, energy=10, monster_hp=30)

        # Play 3 strikes first
        state = play_named_card(game, sim, setup, sts_sim.Card.StrikeGreen,
                                target_index=0)
        state = play_named_card(game, sim, state, sts_sim.Card.StrikeGreen,
                                target_index=0)
        state = play_named_card(game, sim, state, sts_sim.Card.StrikeGreen,
                                target_index=0)
        # Play finisher
        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_finisher_no_attacks(self, game):
        """Finisher deals 0 damage with no attacks played this turn."""
        hand = [sts_sim.Card.Finisher]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Flechettes
    # ===========================================================================

    def test_flechettes_with_3_skills(self, game):
        """Flechettes deals 3 damage with 3 Skills in hand."""
        hand = [
            sts_sim.Card.Flechettes,
            sts_sim.Card.DefendGreen,
            sts_sim.Card.DefendGreen,
            sts_sim.Card.DefendGreen,
        ]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_flechettes_with_0_skills(self, game):
        """Flechettes deals 0 damage with no Skills in hand."""
        hand = [
            sts_sim.Card.Flechettes,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_flechettes_upgraded_with_2_skills(self, game):
        """Flechettes+ deals 3 damage with 2 Skills in hand (+1 bonus)."""
        hand = [
            (sts_sim.Card.Flechettes, True),
            sts_sim.Card.DefendGreen,
            sts_sim.Card.DefendGreen,
        ]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Unload
    # ===========================================================================

    def test_unload_with_0_shivs(self, game):
        """Unload deals 2 damage with no SHIVs."""
        hand = [sts_sim.Card.Unload]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Blur
    # ===========================================================================

    def test_blur_without_discarding(self, game):
        """Blur grants 2 block without discarding."""
        hand = [sts_sim.Card.Blur]

        set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_discard_matches(state, sim)

    # ===========================================================================
    # Bouncing Flask
    # ===========================================================================

    def test_bouncing_flask_stack_on_one(self, game):
        """Bouncing Flask applies 2 POISON to one enemy."""
        hand = [sts_sim.Card.BouncingFlask]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0,
                               choices=[0, 0])

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Catalyst
    # ===========================================================================

    def test_catalyst_doubles_poison(self, game):
        """Catalyst doubles POISON from 4 to 8. Exhausts."""
        hand = [sts_sim.Card.Catalyst]

        set_scenario(game, hand=hand, energy=3, monster_hp=20,
                     monster_powers={"Poison": 4})
        sim = make_sim(hand=hand, energy=3, monster_hp=20,
                       monster_powers={"Poison": 4})

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_catalyst_zero_poison(self, game):
        """Catalyst on enemy with 0 POISON: remains 0."""
        hand = [sts_sim.Card.Catalyst]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_exhaust_matches(state, sim)

    def test_catalyst_upgraded_triples(self, game):
        """Catalyst+ triples POISON from 5 to 15."""
        hand = [(sts_sim.Card.Catalyst, True)]

        set_scenario(game, hand=hand, energy=3, monster_hp=20,
                     monster_powers={"Poison": 5})
        sim = make_sim(hand=hand, energy=3, monster_hp=20,
                       monster_powers={"Poison": 5})

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_exhaust_matches(state, sim)

    # ===========================================================================
    # Leg Sweep
    # ===========================================================================

    def test_leg_sweep_basic(self, game):
        """Leg Sweep: 1 WEAK, 3 block."""
        hand = [sts_sim.Card.LegSweep]

        set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_leg_sweep_upgraded_with_footwork(self, game):
        """Leg Sweep+ with Footwork: 1 WEAK, 4*(1+1)=8 block."""
        hand = [(sts_sim.Card.LegSweep, True)]

        set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20,
                     player_powers={"Dexterity": 1})
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20,
                       player_powers={"Dexterity": 1})

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_leg_sweep_stacking_weak(self, game):
        """Leg Sweep adds 1 WEAK on top of existing 2 WEAK."""
        hand = [sts_sim.Card.LegSweep]

        set_scenario(game, hand=hand, energy=3, monster_hp=20,
                     monster_powers={"Weak": 2})
        sim = make_sim(hand=hand, energy=3, monster_hp=20,
                       monster_powers={"Weak": 2})

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Outmaneuver
    # ===========================================================================

    def test_outmaneuver_played_immediately(self, game):
        """Outmaneuver played immediately: no bonus, costs 1."""
        hand = [sts_sim.Card.Outmaneuver]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)

    # ===========================================================================
    # Escape Plan
    # ===========================================================================

    def test_escape_plan_draws_skill(self, game):
        """Escape Plan draws a Skill and gains 1 block."""
        hand = [sts_sim.Card.EscapePlan]
        draw = [sts_sim.Card.DefendGreen]

        set_scenario(game, hand=hand, draw_pile=draw, energy=3, player_block=0,
                     monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, player_block=0,
                       monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    def test_escape_plan_draws_attack(self, game):
        """Escape Plan draws an Attack, no block."""
        hand = [sts_sim.Card.EscapePlan]
        draw = [sts_sim.Card.StrikeGreen]

        set_scenario(game, hand=hand, draw_pile=draw, energy=3, player_block=0,
                     monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, player_block=0,
                       monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    def test_escape_plan_upgraded_always_block(self, game):
        """Escape Plan+ always gives 1 block regardless of drawn card type."""
        hand = [(sts_sim.Card.EscapePlan, True)]
        draw = [sts_sim.Card.StrikeGreen]

        set_scenario(game, hand=hand, draw_pile=draw, energy=3, player_block=0,
                     monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, player_block=0,
                       monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    # ===========================================================================
    # Expertise
    # ===========================================================================

    def test_expertise_with_2_cards(self, game):
        """Expertise with 2 cards in hand: draws up to 6."""
        hand = [sts_sim.Card.Expertise, sts_sim.Card.StrikeGreen]
        draw = [sts_sim.Card.StrikeGreen] * 6

        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    def test_expertise_full_hand(self, game):
        """Expertise with 7 cards: draws 0 after playing."""
        hand = [
            sts_sim.Card.Expertise,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    def test_expertise_upgraded_with_3_cards(self, game):
        """Expertise+ with 3 cards: draws up to 7."""
        hand = [
            (sts_sim.Card.Expertise, True),
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ]
        draw = [sts_sim.Card.StrikeGreen] * 6

        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    # ===========================================================================
    # Riddle with Holes
    # ===========================================================================

    def test_riddle_with_holes_basic(self, game):
        """Riddle with Holes grants 4 SHIV tokens."""
        hand = [sts_sim.Card.RiddleWithHoles]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)

    def test_riddle_with_holes_upgraded(self, game):
        """Riddle with Holes+ grants 5 SHIV tokens."""
        hand = [(sts_sim.Card.RiddleWithHoles, True)]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)

    # ===========================================================================
    # Setup (card)
    # ===========================================================================

    def test_setup_give_energy_to_self(self, game):
        """Setup grants 1 energy to self (net 0). Exhausts."""
        hand = [sts_sim.Card.Setup]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    # ===========================================================================
    # Terror
    # ===========================================================================

    def test_terror_basic(self, game):
        """Terror applies 1 VULN and exhausts."""
        hand = [sts_sim.Card.Terror]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_terror_upgraded_no_exhaust(self, game):
        """Terror+ applies 1 VULN, goes to discard (not exhaust)."""
        hand = [(sts_sim.Card.Terror, True)]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_discard_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_terror_stacks_vuln(self, game):
        """Terror adds 1 VULN on top of existing 2."""
        hand = [sts_sim.Card.Terror]

        set_scenario(game, hand=hand, energy=3, monster_hp=20,
                     monster_powers={"Vulnerable": 2})
        sim = make_sim(hand=hand, energy=3, monster_hp=20,
                       monster_powers={"Vulnerable": 2})

        state = play_card_both(game, sim, hand_index=0, target_index=0)

        assert_monsters_match(state, sim)
        assert_exhaust_matches(state, sim)

    # ===========================================================================
    # Footwork
    # ===========================================================================

    def test_footwork_boosts_block(self, game):
        """Footwork boosts subsequent BLK: Defend 1 BLK -> 2 block."""
        hand = [sts_sim.Card.FootworkCard, sts_sim.Card.DefendGreen]

        setup = set_scenario(game, hand=hand, energy=3, player_block=0,
                             monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)

        state = play_named_card(game, sim, setup, sts_sim.Card.FootworkCard)
        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)

    def test_footwork_stacks(self, game):
        """Two Footworks stack: Defend 1 BLK -> 3 block."""
        hand = [
            sts_sim.Card.FootworkCard,
            sts_sim.Card.FootworkCard,
            sts_sim.Card.DefendGreen,
        ]

        setup = set_scenario(game, hand=hand, energy=3, player_block=0,
                             monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)

        state = play_named_card(game, sim, setup, sts_sim.Card.FootworkCard)
        state = play_named_card(game, sim, state, sts_sim.Card.FootworkCard)
        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)

    # ===========================================================================
    # Distraction
    # ===========================================================================

    def test_distraction_upgraded_cost(self, game):
        """Distraction+ costs 1 energy."""
        hand = [(sts_sim.Card.DistractionCard, True)]

        set_scenario(game, hand=hand, energy=1, monster_hp=20)
        sim = make_sim(hand=hand, energy=1, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)

    # ===========================================================================
    # Infinite Blades
    # ===========================================================================

    def test_infinite_blades_plays(self, game):
        """Infinite Blades can be played as a power. Costs 1."""
        hand = [sts_sim.Card.InfiniteBlades]

        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)

    # ===========================================================================
    # Calculated Gamble
    # ===========================================================================

    def test_calculated_gamble_with_3_cards(self, game):
        """Calculated Gamble discards 3, draws 3."""
        hand = [
            sts_sim.Card.CalculatedGamble,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ]
        draw = [sts_sim.Card.DefendGreen] * 5

        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    def test_calculated_gamble_empty_hand(self, game):
        """Calculated Gamble with only itself: discards 0, draws 0."""
        hand = [sts_sim.Card.CalculatedGamble]
        draw = [sts_sim.Card.DefendGreen] * 5

        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)


@pytest.mark.usefixtures("two_monster_fight")
class TestAOE:

    # ===========================================================================
    # All-Out Attack
    # ===========================================================================

    def test_all_out_attack_aoe(self, game):
        """All-Out Attack deals 2 AOE damage, discards 1 card."""
        hand = [
            sts_sim.Card.AllOutAttack,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ]

        set_scenario(game, hand=hand, energy=3,
                     monsters=[{"hp": 15}, {"hp": 10}])
        sim = make_sim(hand=hand, energy=3,
                       monsters=[{"hp": 15}, {"hp": 10}])

        state = play_card_both(game, sim, hand_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_all_out_attack_upgraded(self, game):
        """All-Out Attack+ deals 3 AOE damage."""
        hand = [
            (sts_sim.Card.AllOutAttack, True),
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ]

        set_scenario(game, hand=hand, energy=3,
                     monsters=[{"hp": 15}, {"hp": 10}])
        sim = make_sim(hand=hand, energy=3,
                       monsters=[{"hp": 15}, {"hp": 10}])

        state = play_card_both(game, sim, hand_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===========================================================================
    # Crippling Cloud
    # ===========================================================================

    def test_crippling_cloud_aoe(self, game):
        """Crippling Cloud applies 1 POISON, 1 WEAK to all enemies. Exhausts."""
        hand = [sts_sim.Card.CripplingCloud]

        set_scenario(game, hand=hand, energy=3,
                     monsters=[{"hp": 20}, {"hp": 15}])
        sim = make_sim(hand=hand, energy=3,
                       monsters=[{"hp": 20}, {"hp": 15}])

        state = play_card_both(game, sim, hand_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_crippling_cloud_upgraded(self, game):
        """Crippling Cloud+ applies 2 POISON, 1 WEAK to all enemies."""
        hand = [(sts_sim.Card.CripplingCloud, True)]

        set_scenario(game, hand=hand, energy=3,
                     monsters=[{"hp": 20}, {"hp": 15}])
        sim = make_sim(hand=hand, energy=3,
                       monsters=[{"hp": 20}, {"hp": 15}])

        state = play_card_both(game, sim, hand_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    # ===========================================================================
    # Piercing Wail
    # ===========================================================================

    def test_piercing_wail_basic(self, game):
        """Piercing Wail: 1 block, AOE WEAK, exhaust."""
        hand = [sts_sim.Card.PiercingWail]

        set_scenario(game, hand=hand, energy=3, player_block=0,
                     monsters=[{"hp": 20}, {"hp": 15}])
        sim = make_sim(hand=hand, energy=3, player_block=0,
                       monsters=[{"hp": 20}, {"hp": 15}])

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_piercing_wail_upgraded(self, game):
        """Piercing Wail+: 3 block, AOE WEAK, exhaust."""
        hand = [(sts_sim.Card.PiercingWail, True)]

        set_scenario(game, hand=hand, energy=3, player_block=0,
                     monsters=[{"hp": 20}, {"hp": 15}])
        sim = make_sim(hand=hand, energy=3, player_block=0,
                       monsters=[{"hp": 20}, {"hp": 15}])

        state = play_card_both(game, sim, hand_index=0)

        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)


@pytest.mark.usefixtures("fresh_combat")
class TestMultiTurn:

    # ===========================================================================
    # Noxious Fumes (multi-turn)
    # ===========================================================================

    def test_noxious_fumes_applies_poison(self, game):
        """Noxious Fumes applies 1 POISON to enemies at start of next turn."""
        hand = [sts_sim.Card.StrikeGreen] * 5
        draw = [sts_sim.Card.StrikeGreen] * 5

        # Use Gremlin Nob: turn 1 is Bellow (no damage), so HP stays consistent
        set_scenario(game, encounter="BoardGame:Gremlin Nob",
                     hand=hand, draw_pile=draw, energy=3, player_hp=9,
                     player_powers={"NoxiousFumes": 1}, monster_hp=30)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, player_hp=9,
                       player_powers={"NoxiousFumes": 1}, monster_hp=30,
                       monster_id="gremlin_nob")

        state = end_turn_both(game, sim)

        assert_player_matches(state, sim)
        # Check Poison specifically (monster native powers differ between sim/live)
        live_monster = [m for m in state.combat_state.monsters if not m.is_gone][0]
        sim_monster = sim.get_monsters()[0]
        # BG mod uses "BGPoison" as the power ID
        live_poison = live_monster.get_power("BGPoison") or live_monster.get_power("Poison")
        assert live_poison is not None, (
            f"Live monster has no Poison. Powers: {[(p.power_id, p.amount) for p in live_monster.powers]}"
        )
        assert live_poison.amount >= 1, f"Live Poison={live_poison.amount}, expected >= 1"
        sim_poison = sim_monster.get_power(sts_sim.PowerType.Poison)
        assert sim_poison >= 1, f"Sim Poison={sim_poison}, expected >= 1"
