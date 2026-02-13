"""Live tests for Curse cards.

Implemented curses: AscendersBane [Y], Decay [Y], Injury [Y], Pain [Y]
Not implemented: Clumsy [N], Doubt [N], Parasite [N], Regret [N], Shame [N], Writhe [N]
"""
import pytest
import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches,
)


@pytest.mark.usefixtures("single_monster_fight")
class TestCards:

    # ── Ascender's Bane [Y] ─────────────────────────────────────────────────

    def test_ascenders_bane_in_hand(self, game):
        """AscendersBane is unplayable — verify it stays in hand while other cards play.

        Setup: AscendersBane + Strike in hand, monster at 30 HP.
        Play Strike, verify AscendersBane remains.
        """
        hand = [sts_sim.Card.StrikeRed, sts_sim.Card.AscendersBane]

        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_sim(hand=hand, energy=3, monster_hp=30)

        state = play_named_card(game, sim, setup, sts_sim.Card.StrikeRed,
                                target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    # ── Decay [Y] ────────────────────────────────────────────────────────────

    def test_decay_in_hand(self, game):
        """Decay is unplayable — verify it stays in hand while other cards play.

        Setup: Decay + Strike in hand, monster at 30 HP.
        Play Strike, verify Decay remains.
        """
        hand = [sts_sim.Card.StrikeRed, sts_sim.Card.Decay]

        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_sim(hand=hand, energy=3, monster_hp=30)

        state = play_named_card(game, sim, setup, sts_sim.Card.StrikeRed,
                                target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    # ── Injury [Y] ───────────────────────────────────────────────────────────

    def test_injury_in_hand(self, game):
        """Injury is unplayable — verify it stays in hand while other cards play.

        Setup: Injury + Strike in hand, monster at 30 HP.
        Play Strike, verify Injury remains.
        """
        hand = [sts_sim.Card.StrikeRed, sts_sim.Card.Injury]

        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_sim(hand=hand, energy=3, monster_hp=30)

        state = play_named_card(game, sim, setup, sts_sim.Card.StrikeRed,
                                target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    # ── Pain [Y] ─────────────────────────────────────────────────────────────

    def test_pain_in_hand(self, game):
        """Pain is unplayable — verify it stays in hand while other cards play.

        Setup: Pain + Strike in hand, monster at 30 HP.
        Play Strike, verify Pain remains.
        """
        hand = [sts_sim.Card.StrikeRed, sts_sim.Card.Pain]

        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_sim(hand=hand, energy=3, monster_hp=30)

        state = play_named_card(game, sim, setup, sts_sim.Card.StrikeRed,
                                target_index=0)

        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)
        assert_hand_matches(state, sim)

    # ── Clumsy [N] ───────────────────────────────────────────────────────────

    @pytest.mark.skip(reason="Clumsy not implemented in simulator")
    def test_clumsy_unplayable(self, game):
        """Clumsy cannot be played."""
        pass

    @pytest.mark.skip(reason="Clumsy not implemented in simulator")
    def test_clumsy_ethereal(self, game):
        """Clumsy exhausts at end of turn (Ethereal)."""
        pass

    @pytest.mark.skip(reason="Clumsy not implemented in simulator")
    def test_clumsy_clogs_hand(self, game):
        """Clumsy takes up a hand slot when drawn."""
        pass

    # ── Doubt [N] ────────────────────────────────────────────────────────────

    @pytest.mark.skip(reason="Doubt not implemented in simulator")
    def test_doubt_unplayable(self, game):
        """Doubt cannot be played."""
        pass

    @pytest.mark.skip(reason="Doubt not implemented in simulator")
    def test_doubt_end_of_turn_weak(self, game):
        """Doubt applies WEAK at end of turn."""
        pass

    @pytest.mark.skip(reason="Doubt not implemented in simulator")
    def test_doubt_stacking_weak(self, game):
        """Doubt stacks WEAK with existing WEAK tokens."""
        pass

    # ── Parasite [N] ─────────────────────────────────────────────────────────

    @pytest.mark.skip(reason="Parasite not implemented in simulator")
    def test_parasite_unplayable(self, game):
        """Parasite cannot be played."""
        pass

    @pytest.mark.skip(reason="Parasite not implemented in simulator")
    def test_parasite_removal_hp_loss(self, game):
        """Removing Parasite from deck causes 2 HP loss."""
        pass

    @pytest.mark.skip(reason="Parasite not implemented in simulator")
    def test_parasite_no_passive_effect(self, game):
        """Parasite has no passive effect during combat."""
        pass

    # ── Regret [N] ───────────────────────────────────────────────────────────

    @pytest.mark.skip(reason="Regret not implemented in simulator")
    def test_regret_unplayable(self, game):
        """Regret cannot be played."""
        pass

    @pytest.mark.skip(reason="Regret not implemented in simulator")
    def test_regret_retain(self, game):
        """Regret retains in hand every turn."""
        pass

    @pytest.mark.skip(reason="Regret not implemented in simulator")
    def test_regret_permanent_clog(self, game):
        """Regret permanently clogs one hand slot."""
        pass

    # ── Shame [N] ────────────────────────────────────────────────────────────

    @pytest.mark.skip(reason="Shame not implemented in simulator")
    def test_shame_unplayable(self, game):
        """Shame cannot be played."""
        pass

    @pytest.mark.skip(reason="Shame not implemented in simulator")
    def test_shame_end_of_turn_block_loss(self, game):
        """Shame causes 1 block loss at end of turn."""
        pass

    @pytest.mark.skip(reason="Shame not implemented in simulator")
    def test_shame_no_negative_block(self, game):
        """Shame does not cause block to go negative."""
        pass

    # ── Writhe [N] ───────────────────────────────────────────────────────────

    @pytest.mark.skip(reason="Writhe not implemented in simulator")
    def test_writhe_play_exhaust(self, game):
        """Writhe exhausts when played for 1 energy."""
        pass

    @pytest.mark.skip(reason="Writhe not implemented in simulator")
    def test_writhe_not_enough_energy(self, game):
        """Writhe cannot be played without enough energy."""
        pass

    @pytest.mark.skip(reason="Writhe not implemented in simulator")
    def test_writhe_discarded_if_not_played(self, game):
        """Writhe is discarded if not played, returns to draw pile."""
        pass
