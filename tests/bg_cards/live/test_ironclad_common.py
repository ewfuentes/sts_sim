"""Live tests for Ironclad Common cards."""
import pytest
import sts_sim
from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_discard_matches, assert_exhaust_matches,
    assert_draw_pile_matches,
)


@pytest.mark.usefixtures("single_monster_fight")
class TestSingleTarget:

    # =========================================================================
    # Anger
    # =========================================================================

    def test_anger_base_damage_and_draw_pile(self, game):
        """Base Anger deals 1 damage and goes to draw pile."""
        draw = [sts_sim.Card.StrikeRed, sts_sim.Card.DefendRed, sts_sim.Card.DefendRed]
        hand = [sts_sim.Card.Anger]
        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_draw_pile_matches(state, sim)

    def test_anger_upgraded_damage(self, game):
        """Upgraded Anger deals 2 damage."""
        hand = [(sts_sim.Card.Anger, True)]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_anger_with_strength(self, game):
        """Anger with 1 STR deals 2 damage."""
        hand = [sts_sim.Card.Anger]
        set_scenario(game, hand=hand, energy=3, monster_hp=20,
                     player_powers={"Strength": 1})
        sim = make_sim(hand=hand, energy=3, monster_hp=20,
                       player_powers={"Strength": 1})
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =========================================================================
    # Body Slam
    # =========================================================================

    def test_body_slam_damage_equals_block(self, game):
        """Body Slam deals damage equal to current block."""
        hand = [sts_sim.Card.BodySlam]
        set_scenario(game, hand=hand, energy=3, player_block=5, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=5, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_body_slam_zero_block(self, game):
        """Body Slam with 0 block deals 0 damage."""
        hand = [sts_sim.Card.BodySlam]
        set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_body_slam_upgraded_costs_zero(self, game):
        """Upgraded Body Slam costs 0 energy."""
        hand = [(sts_sim.Card.BodySlam, True)]
        set_scenario(game, hand=hand, energy=3, player_block=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_body_slam_with_strength(self, game):
        """Body Slam with Strength: (1+2)*4 = 12 damage."""
        hand = [sts_sim.Card.BodySlam]
        set_scenario(game, hand=hand, energy=3, player_block=4, monster_hp=20,
                     player_powers={"Strength": 2})
        sim = make_sim(hand=hand, energy=3, player_block=4, monster_hp=20,
                       player_powers={"Strength": 2})
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =========================================================================
    # Clash
    # =========================================================================

    def test_clash_all_attacks_playable(self, game):
        """Clash is playable when all cards in hand are Attacks."""
        hand = [sts_sim.Card.Clash, sts_sim.Card.StrikeRed, sts_sim.Card.Anger]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_named_card(game, sim, setup, sts_sim.Card.Clash, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_clash_upgraded_damage(self, game):
        """Upgraded Clash deals 4 damage."""
        hand = [(sts_sim.Card.Clash, True), sts_sim.Card.StrikeRed]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_named_card(game, sim, setup, sts_sim.Card.Clash,
                                target_index=0, upgraded=True)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =========================================================================
    # Clothesline
    # =========================================================================

    def test_clothesline_base_damage_and_weak(self, game):
        """Base Clothesline deals 3 damage and applies Weak."""
        hand = [sts_sim.Card.Clothesline]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_clothesline_upgraded_damage_and_weak(self, game):
        """Upgraded Clothesline deals 4 damage and applies Weak."""
        hand = [(sts_sim.Card.Clothesline, True)]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_clothesline_with_strength(self, game):
        """Clothesline with 2 STR: 9 damage."""
        hand = [sts_sim.Card.Clothesline]
        set_scenario(game, hand=hand, energy=3, monster_hp=20,
                     player_powers={"Strength": 2})
        sim = make_sim(hand=hand, energy=3, monster_hp=20,
                       player_powers={"Strength": 2})
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =========================================================================
    # Heavy Blade
    # =========================================================================

    def test_heavy_blade_base_no_strength(self, game):
        """Base Heavy Blade deals 3 damage with no Strength."""
        hand = [sts_sim.Card.HeavyBlade]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_heavy_blade_with_strength_triples(self, game):
        """Heavy Blade with 2 STR: 21 damage total."""
        hand = [sts_sim.Card.HeavyBlade]
        set_scenario(game, hand=hand, energy=3, monster_hp=30,
                     player_powers={"Strength": 2})
        sim = make_sim(hand=hand, energy=3, monster_hp=30,
                       player_powers={"Strength": 2})
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_heavy_blade_upgraded_quintuples(self, game):
        """Upgraded Heavy Blade with 2 STR: 33 damage total."""
        hand = [(sts_sim.Card.HeavyBlade, True)]
        set_scenario(game, hand=hand, energy=3, monster_hp=40,
                     player_powers={"Strength": 2})
        sim = make_sim(hand=hand, energy=3, monster_hp=40,
                       player_powers={"Strength": 2})
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =========================================================================
    # Iron Wave
    # =========================================================================

    def test_iron_wave_base_damage_and_block(self, game):
        """Base Iron Wave deals 1 damage and gains 1 block."""
        hand = [sts_sim.Card.IronWave]
        set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_iron_wave_with_strength(self, game):
        """Iron Wave with 1 STR: 2 damage, 1 block."""
        hand = [sts_sim.Card.IronWave]
        set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20,
                     player_powers={"Strength": 1})
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20,
                       player_powers={"Strength": 1})
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_iron_wave_upgraded_choice(self, game):
        """Upgraded Iron Wave choosing 2 HIT 1 BLK option."""
        hand = [(sts_sim.Card.IronWave, True)]
        set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0,
                               choices=[0])  # choice 0 = 2 HIT 1 BLK
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =========================================================================
    # Perfected Strike
    # =========================================================================

    def test_perfected_strike_no_other_strikes(self, game):
        """Base Perfected Strike with no other Strikes: 3 damage."""
        hand = [sts_sim.Card.PerfectedStrike, sts_sim.Card.DefendRed, sts_sim.Card.Bash]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_named_card(game, sim, setup, sts_sim.Card.PerfectedStrike,
                                target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_perfected_strike_with_two_strikes(self, game):
        """Perfected Strike with 2 other Strikes: 5 damage."""
        hand = [sts_sim.Card.PerfectedStrike, sts_sim.Card.StrikeRed,
                sts_sim.Card.TwinStrike, sts_sim.Card.DefendRed]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_named_card(game, sim, setup, sts_sim.Card.PerfectedStrike,
                                target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_perfected_strike_upgraded_with_two_strikes(self, game):
        """Upgraded Perfected Strike with 2 other Strikes: 7 damage."""
        hand = [(sts_sim.Card.PerfectedStrike, True), sts_sim.Card.StrikeRed,
                sts_sim.Card.PommelStrike, sts_sim.Card.Bash]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_named_card(game, sim, setup, sts_sim.Card.PerfectedStrike,
                                target_index=0, upgraded=True)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =========================================================================
    # Pommel Strike
    # =========================================================================

    def test_pommel_strike_base_damage_and_draw(self, game):
        """Base Pommel Strike deals 2 damage and draws 1 card."""
        draw = [sts_sim.Card.DefendRed, sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed,
                sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed]
        hand = [sts_sim.Card.PommelStrike]
        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    def test_pommel_strike_upgraded_draws_two(self, game):
        """Upgraded Pommel Strike draws 2 cards."""
        draw = [sts_sim.Card.DefendRed, sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed,
                sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed]
        hand = [(sts_sim.Card.PommelStrike, True)]
        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    def test_pommel_strike_empty_draw_reshuffle(self, game):
        """Pommel Strike with empty draw pile triggers reshuffle."""
        discard = [sts_sim.Card.StrikeRed, sts_sim.Card.DefendRed, sts_sim.Card.DefendRed]
        hand = [sts_sim.Card.PommelStrike]
        set_scenario(game, hand=hand, discard_pile=discard, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, discard_pile=discard, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =========================================================================
    # Shrug It Off
    # =========================================================================

    def test_shrug_it_off_base_block_and_draw(self, game):
        """Base Shrug It Off grants 2 block and draws 1 card."""
        draw = [sts_sim.Card.DefendRed, sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed,
                sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed]
        hand = [sts_sim.Card.ShrugItOff]
        set_scenario(game, hand=hand, draw_pile=draw, energy=3,
                     player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3,
                       player_block=0, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    def test_shrug_it_off_upgraded_block(self, game):
        """Upgraded Shrug It Off grants 3 block."""
        draw = [sts_sim.Card.DefendRed, sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed,
                sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed]
        hand = [(sts_sim.Card.ShrugItOff, True)]
        set_scenario(game, hand=hand, draw_pile=draw, energy=3,
                     player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3,
                       player_block=0, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    def test_shrug_it_off_stacks_with_existing_block(self, game):
        """Shrug It Off block stacks with existing block."""
        draw = [sts_sim.Card.DefendRed, sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed,
                sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed]
        hand = [sts_sim.Card.ShrugItOff]
        set_scenario(game, hand=hand, draw_pile=draw, energy=3,
                     player_block=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3,
                       player_block=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)

    # =========================================================================
    # Twin Strike
    # =========================================================================

    def test_twin_strike_base_two_hits(self, game):
        """Base Twin Strike deals 2 separate hits of 1 damage each."""
        hand = [sts_sim.Card.TwinStrike]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_twin_strike_against_block(self, game):
        """Twin Strike vs 1 block: first hit removes block, second hits HP."""
        hand = [sts_sim.Card.TwinStrike]
        set_scenario(game, hand=hand, energy=3, monster_hp=20, monster_block=1)
        sim = make_sim(hand=hand, energy=3, monster_hp=20, monster_block=1)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_twin_strike_upgraded(self, game):
        """Upgraded Twin Strike deals 2 damage per hit."""
        hand = [(sts_sim.Card.TwinStrike, True)]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_twin_strike_with_strength(self, game):
        """Twin Strike with 1 STR: 4 total damage."""
        hand = [sts_sim.Card.TwinStrike]
        set_scenario(game, hand=hand, energy=3, monster_hp=20,
                     player_powers={"Strength": 1})
        sim = make_sim(hand=hand, energy=3, monster_hp=20,
                       player_powers={"Strength": 1})
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =========================================================================
    # Wild Strike
    # =========================================================================

    def test_wild_strike_base_damage_and_dazed(self, game):
        """Base Wild Strike deals 3 damage and adds Dazed to discard pile."""
        hand = [sts_sim.Card.WildStrike]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_discard_matches(state, sim)

    def test_wild_strike_upgraded_damage(self, game):
        """Upgraded Wild Strike deals 4 damage."""
        hand = [(sts_sim.Card.WildStrike, True)]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_discard_matches(state, sim)

    # =========================================================================
    # Headbutt
    # =========================================================================

    def test_headbutt_base_damage_and_moves_discard(self, game):
        """Base Headbutt deals 2 damage and moves card from discard to draw pile."""
        draw = [sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed]
        discard = [sts_sim.Card.Bash, sts_sim.Card.DefendRed]
        hand = [sts_sim.Card.Headbutt]
        set_scenario(game, hand=hand, draw_pile=draw, discard_pile=discard,
                     energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, discard_pile=discard,
                       energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0,
                               choices=[0])  # Choose first card from discard
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_headbutt_upgraded_damage(self, game):
        """Upgraded Headbutt deals 3 damage."""
        discard = [sts_sim.Card.StrikeRed]
        hand = [(sts_sim.Card.Headbutt, True)]
        set_scenario(game, hand=hand, discard_pile=discard, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, discard_pile=discard, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0,
                               choices=[0])
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_headbutt_empty_discard(self, game):
        """Headbutt with empty discard pile still deals damage."""
        hand = [sts_sim.Card.Headbutt]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =========================================================================
    # Havoc
    # =========================================================================

    def test_havoc_draws_plays_and_exhausts(self, game):
        """Havoc draws and plays a card for free, then exhausts it."""
        draw = [sts_sim.Card.StrikeRed]
        hand = [sts_sim.Card.Havoc]
        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_havoc_upgraded_costs_zero(self, game):
        """Upgraded Havoc costs 0 energy."""
        draw = [sts_sim.Card.StrikeRed]
        hand = [(sts_sim.Card.Havoc, True)]
        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =========================================================================
    # Seeing Red
    # =========================================================================

    def test_seeing_red_base_grants_energy(self, game):
        """Base Seeing Red grants 2 energy (net +1)."""
        hand = [sts_sim.Card.SeeingRed]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)

    def test_seeing_red_upgraded_costs_zero(self, game):
        """Upgraded Seeing Red costs 0, grants 2 energy."""
        hand = [(sts_sim.Card.SeeingRed, True)]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)

    # =========================================================================
    # True Grit
    # =========================================================================

    def test_true_grit_base_block_and_exhaust(self, game):
        """Base True Grit grants 1 block and exhausts a card from hand."""
        hand = [sts_sim.Card.TrueGrit, sts_sim.Card.StrikeRed]
        setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
        state = play_named_card(game, sim, setup, sts_sim.Card.TrueGrit)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_true_grit_upgraded_block(self, game):
        """Upgraded True Grit grants 2 block."""
        hand = [(sts_sim.Card.TrueGrit, True), sts_sim.Card.DefendRed]
        setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
        state = play_named_card(game, sim, setup, sts_sim.Card.TrueGrit, upgraded=True)
        assert_player_matches(state, sim)

    def test_true_grit_only_card_in_hand(self, game):
        """True Grit when only True Grit is in hand."""
        hand = [sts_sim.Card.TrueGrit]
        set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)

    # =========================================================================
    # Warcry
    # =========================================================================

    def test_warcry_base_draws_two_puts_one_back_exhausts(self, game):
        """Base Warcry draws 2, puts 1 back on draw pile, and exhausts."""
        draw = [sts_sim.Card.StrikeRed, sts_sim.Card.DefendRed,
                sts_sim.Card.StrikeRed, sts_sim.Card.DefendRed,
                sts_sim.Card.StrikeRed]
        hand = [sts_sim.Card.Warcry, sts_sim.Card.Bash, sts_sim.Card.DefendRed]
        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, choices=[0])
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_warcry_upgraded_draws_three(self, game):
        """Upgraded Warcry draws 3 cards."""
        draw = [sts_sim.Card.StrikeRed, sts_sim.Card.DefendRed,
                sts_sim.Card.StrikeRed, sts_sim.Card.DefendRed,
                sts_sim.Card.StrikeRed]
        hand = [(sts_sim.Card.Warcry, True), sts_sim.Card.Bash, sts_sim.Card.DefendRed]
        set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, choices=[0])
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)


@pytest.mark.usefixtures("two_monster_fight")
class TestAOE:

    # =========================================================================
    # Cleave
    # =========================================================================

    def test_cleave_base_hits_all_enemies(self, game):
        """Base Cleave hits all enemies for 2 damage each."""
        hand = [sts_sim.Card.Cleave]
        monsters = [{"hp": 15}, {"hp": 10}]
        set_scenario(game, hand=hand, energy=3, monsters=monsters)
        sim = make_sim(hand=hand, energy=3, monsters=monsters)
        state = play_card_both(game, sim, hand_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_cleave_upgraded_hits_all_enemies(self, game):
        """Upgraded Cleave hits all enemies for 3 damage each."""
        hand = [(sts_sim.Card.Cleave, True)]
        monsters = [{"hp": 15}, {"hp": 10}]
        set_scenario(game, hand=hand, energy=3, monsters=monsters)
        sim = make_sim(hand=hand, energy=3, monsters=monsters)
        state = play_card_both(game, sim, hand_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_cleave_with_strength(self, game):
        """Cleave with 1 STR: 4 damage to each enemy."""
        hand = [sts_sim.Card.Cleave]
        monsters = [{"hp": 15}, {"hp": 10}]
        set_scenario(game, hand=hand, energy=3, monsters=monsters,
                     player_powers={"Strength": 1})
        sim = make_sim(hand=hand, energy=3, monsters=monsters,
                       player_powers={"Strength": 1})
        state = play_card_both(game, sim, hand_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
