"""Live tests for Silent Basic cards."""
import pytest
import sts_sim
from tests.live.conftest import (
    set_scenario, make_sim, play_card_both,
    assert_monsters_match, assert_player_matches,
    assert_discard_matches,
)


@pytest.mark.usefixtures("single_monster_fight")
class TestCards:

    # ---------------------------------------------------------------------------
    # Strike (Green)
    # ---------------------------------------------------------------------------

    def test_strike_green_base(self, game):
        """Basic Strike deals 1 damage."""
        hand = [sts_sim.Card.StrikeGreen]
        set_scenario(game, hand=hand, energy=3, monster_hp=10)
        sim = make_sim(hand=hand, energy=3, monster_hp=10)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_strike_green_with_strength(self, game):
        """Strike with 2 STR adds bonus damage per HIT."""
        hand = [sts_sim.Card.StrikeGreen]
        powers = {"Strength": 2}
        set_scenario(game, hand=hand, energy=3, monster_hp=10, player_powers=powers)
        sim = make_sim(hand=hand, energy=3, monster_hp=10, player_powers=powers)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_strike_green_upgraded(self, game):
        """Upgraded Strike deals 2 HIT (each boosted by STR)."""
        hand = [(sts_sim.Card.StrikeGreen, True)]
        powers = {"Strength": 1}
        set_scenario(game, hand=hand, energy=3, monster_hp=10, player_powers=powers)
        sim = make_sim(hand=hand, energy=3, monster_hp=10, player_powers=powers)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ---------------------------------------------------------------------------
    # Defend (Green)
    # ---------------------------------------------------------------------------

    def test_defend_green_base(self, game):
        """Basic Defend grants 1 block to self."""
        hand = [sts_sim.Card.DefendGreen]
        set_scenario(game, hand=hand, energy=3, player_block=0)
        sim = make_sim(hand=hand, energy=3, player_block=0)
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)

    def test_defend_green_upgraded_stack_on_self(self, game):
        """Upgraded Defend can stack both BLK on self."""
        hand = [(sts_sim.Card.DefendGreen, True)]
        set_scenario(game, hand=hand, energy=3, player_block=0)
        sim = make_sim(hand=hand, energy=3, player_block=0)
        # Choice 0 = assign to self for each BLK
        state = play_card_both(game, sim, hand_index=0, choices=[0])
        assert_player_matches(state, sim)

    # ---------------------------------------------------------------------------
    # Neutralize
    # ---------------------------------------------------------------------------

    def test_neutralize_base(self, game):
        """Neutralize deals 1 damage and applies 1 Weak at zero cost."""
        hand = [sts_sim.Card.Neutralize]
        set_scenario(game, hand=hand, energy=3, monster_hp=10)
        sim = make_sim(hand=hand, energy=3, monster_hp=10)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_neutralize_with_strength(self, game):
        """Neutralize with 1 STR deals 2 damage."""
        hand = [sts_sim.Card.Neutralize]
        powers = {"Strength": 1}
        set_scenario(game, hand=hand, energy=3, monster_hp=10, player_powers=powers)
        sim = make_sim(hand=hand, energy=3, monster_hp=10, player_powers=powers)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_neutralize_upgraded(self, game):
        """Upgraded Neutralize deals 2 HIT and applies 1 Weak."""
        hand = [(sts_sim.Card.Neutralize, True)]
        powers = {"Strength": 1}
        set_scenario(game, hand=hand, energy=3, monster_hp=10, player_powers=powers)
        sim = make_sim(hand=hand, energy=3, monster_hp=10, player_powers=powers)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ---------------------------------------------------------------------------
    # Survivor
    # ---------------------------------------------------------------------------

    def test_survivor_base(self, game):
        """Survivor grants 2 block and forces a discard."""
        hand = [sts_sim.Card.Survivor, sts_sim.Card.StrikeGreen]
        set_scenario(game, hand=hand, energy=3, player_block=0)
        sim = make_sim(hand=hand, energy=3, player_block=0)
        # Play Survivor, choose to discard card at index 0
        state = play_card_both(game, sim, hand_index=0, choices=[0])
        assert_player_matches(state, sim)
        assert_discard_matches(state, sim)

    def test_survivor_upgraded(self, game):
        """Upgraded Survivor grants 3 block and forces a discard."""
        hand = [(sts_sim.Card.Survivor, True), sts_sim.Card.DefendGreen]
        set_scenario(game, hand=hand, energy=3, player_block=0)
        sim = make_sim(hand=hand, energy=3, player_block=0)
        state = play_card_both(game, sim, hand_index=0, choices=[0])
        assert_player_matches(state, sim)
        assert_discard_matches(state, sim)
