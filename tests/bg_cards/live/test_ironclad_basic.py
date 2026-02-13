"""Live tests for Ironclad Basic cards."""
import pytest
import sts_sim
from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    end_turn_both, assert_monsters_match, assert_player_matches,
    assert_powers_match,
    assert_hand_matches, assert_discard_matches, assert_exhaust_matches,
)


@pytest.mark.usefixtures("single_monster_fight")
class TestSingleTarget:

    # =========================================================================
    # Strike
    # =========================================================================

    def test_strike_base_damage(self, game):
        """Base Strike deals 1 damage."""
        hand = [sts_sim.Card.StrikeRed]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_strike_with_strength(self, game):
        """Strike with 2 STR deals 3 damage."""
        hand = [sts_sim.Card.StrikeRed]
        set_scenario(game, hand=hand, energy=3, monster_hp=20,
                     player_powers={"Strength": 2})
        sim = make_sim(hand=hand, energy=3, monster_hp=20,
                       player_powers={"Strength": 2})
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_strike_upgraded(self, game):
        """Upgraded Strike deals 2 damage."""
        hand = [(sts_sim.Card.StrikeRed, True)]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =========================================================================
    # Defend
    # =========================================================================

    def test_defend_base_block(self, game):
        """Base Defend grants 1 block."""
        hand = [sts_sim.Card.DefendRed]
        set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)

    def test_defend_upgraded_block(self, game):
        """Upgraded Defend grants 2 block to any player."""
        hand = [(sts_sim.Card.DefendRed, True)]
        set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)

    # =========================================================================
    # Bash
    # =========================================================================

    def test_bash_base_damage_and_vulnerable(self, game):
        """Base Bash deals 2 damage and applies Vulnerable."""
        hand = [sts_sim.Card.Bash]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_bash_upgraded_damage_and_vulnerable(self, game):
        """Upgraded Bash deals 4 damage and applies Vulnerable."""
        hand = [(sts_sim.Card.Bash, True)]
        set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_bash_with_strength(self, game):
        """Bash with 1 STR scales per HIT: 4 damage total."""
        hand = [sts_sim.Card.Bash]
        set_scenario(game, hand=hand, energy=3, monster_hp=20,
                     player_powers={"Strength": 1})
        sim = make_sim(hand=hand, energy=3, monster_hp=20,
                       player_powers={"Strength": 1})
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)


@pytest.mark.usefixtures("fresh_combat")
class TestMultiTurn:

    # =========================================================================
    # Defend (multi-turn)
    # =========================================================================

    def test_defend_block_removed_next_turn(self, game):
        """Block from Defend is removed at start of next turn."""
        hand = [sts_sim.Card.DefendRed]
        draw = [sts_sim.Card.StrikeRed] * 5
        # Use Gremlin Nob: turn 1 is Bellow (no damage), so HP stays consistent
        set_scenario(game, encounter="BoardGame:Gremlin Nob",
                     hand=hand, draw_pile=draw, energy=3,
                     player_hp=9, monster_hp=30)
        sim = make_sim(hand=hand, draw_pile=draw, energy=3,
                       player_hp=9, monster_hp=30, monster_id="gremlin_nob")
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)  # Verify block gained
        state = end_turn_both(game, sim)
        assert_player_matches(state, sim)  # Block should be 0 after turn
