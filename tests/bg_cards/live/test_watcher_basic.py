"""Live tests for Watcher Basic cards.

Tests verify that the live BG mod game and Rust simulator agree on card
effects for Watcher starter cards: Strike, Defend, Eruption, and Vigilance.

For stance-dependent tests, stance-changing cards (Crescendo/Tranquility)
are placed in hand alongside the card under test and played first.
"""
import pytest
import sts_sim
from tests.live.conftest import (
    set_scenario, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    CARD_TO_BG,
    _card_spec_card, _card_spec_upgraded,
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
        card = _card_spec_card(card_spec)
        if _card_spec_upgraded(card_spec):
            sim.add_upgraded_card_to_draw(card)
        else:
            sim.add_card_to_draw(card)

    for card_spec in discard_pile:
        card = _card_spec_card(card_spec)
        if _card_spec_upgraded(card_spec):
            sim.add_upgraded_card_to_discard(card)
        else:
            sim.add_card_to_discard(card)

    for card_spec in hand:
        card = _card_spec_card(card_spec)
        if _card_spec_upgraded(card_spec):
            sim.add_upgraded_card_to_hand(card)
        else:
            sim.add_card_to_hand(card)

    sim.set_die_value(1)
    return sim


# =========================================================================
# Watcher Basic Card Tests
# =========================================================================

@pytest.mark.usefixtures("single_monster_fight")
class TestCards:

    # =====================================================================
    # Strike (Purple)
    # =====================================================================

    def test_strike_base_damage(self, game):
        """Basic Strike deals 1 damage."""
        hand = [sts_sim.Card.StrikePurple]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_strike_in_wrath(self, game):
        """Strike in Wrath deals double damage. Play Crescendo first to enter Wrath."""
        hand = [sts_sim.Card.Crescendo, sts_sim.Card.StrikePurple]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
        # Enter Wrath
        state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
        # Play Strike in Wrath
        state = play_named_card(game, sim, state, sts_sim.Card.StrikePurple,
                                target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_strike_upgraded(self, game):
        """Upgraded Strike deals 2 damage."""
        hand = [(sts_sim.Card.StrikePurple, True)]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_strike_with_strength(self, game):
        """Strike with 2 Strength deals 3 damage (1 base + 2 Strength)."""
        hand = [sts_sim.Card.StrikePurple]
        powers = {"Strength": 2}
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=20,
                             player_powers=powers)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20,
                               player_powers=powers)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =====================================================================
    # Defend (Purple)
    # =====================================================================

    def test_defend_base_block(self, game):
        """Basic Defend grants 1 block."""
        hand = [sts_sim.Card.DefendPurple]
        setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)

    def test_defend_upgraded(self, game):
        """Upgraded Defend grants 2 block."""
        hand = [(sts_sim.Card.DefendPurple, True)]
        setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)

    def test_defend_in_wrath(self, game):
        """Defend in Wrath still grants normal block (Wrath does not affect block)."""
        hand = [sts_sim.Card.Crescendo, sts_sim.Card.DefendPurple]
        setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
        # Enter Wrath
        state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
        # Play Defend in Wrath
        state = play_named_card(game, sim, state, sts_sim.Card.DefendPurple)
        assert_player_matches(state, sim)

    # =====================================================================
    # Eruption
    # =====================================================================

    def test_eruption_base(self, game):
        """Basic Eruption deals 2 damage and enters Wrath."""
        hand = [sts_sim.Card.Eruption]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_eruption_from_calm(self, game):
        """Eruption from Calm grants 2 energy on exit then enters Wrath."""
        hand = [sts_sim.Card.Vigilance, sts_sim.Card.Eruption]
        setup = set_scenario(game, hand=hand, energy=5, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=5, monster_hp=20)
        # Enter Calm via Vigilance
        state = play_named_card(game, sim, setup, sts_sim.Card.Vigilance)
        # Play Eruption (exits Calm -> +2 energy, enters Wrath)
        state = play_named_card(game, sim, state, sts_sim.Card.Eruption,
                                target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_eruption_upgraded(self, game):
        """Upgraded Eruption costs 1 energy instead of 2."""
        hand = [(sts_sim.Card.Eruption, True)]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_eruption_in_wrath(self, game):
        """Eruption while already in Wrath deals doubled damage."""
        hand = [sts_sim.Card.Crescendo, sts_sim.Card.Eruption]
        setup = set_scenario(game, hand=hand, energy=5, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=5, monster_hp=20)
        # Enter Wrath
        state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
        # Play Eruption in Wrath
        state = play_named_card(game, sim, state, sts_sim.Card.Eruption,
                                target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # =====================================================================
    # Vigilance
    # =====================================================================

    def test_vigilance_base(self, game):
        """Basic Vigilance grants 2 block and enters Calm."""
        hand = [sts_sim.Card.Vigilance]
        setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)

    def test_vigilance_upgraded(self, game):
        """Upgraded Vigilance grants 3 block."""
        hand = [(sts_sim.Card.Vigilance, True)]
        setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
        state = play_card_both(game, sim, hand_index=0)
        assert_player_matches(state, sim)

    def test_vigilance_from_wrath(self, game):
        """Vigilance from Wrath exits Wrath and enters Calm."""
        hand = [sts_sim.Card.Crescendo, sts_sim.Card.Vigilance]
        setup = set_scenario(game, hand=hand, energy=5, player_block=0, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=5, player_block=0, monster_hp=20)
        # Enter Wrath
        state = play_named_card(game, sim, setup, sts_sim.Card.Crescendo)
        # Play Vigilance (exits Wrath, enters Calm)
        state = play_named_card(game, sim, state, sts_sim.Card.Vigilance)
        assert_player_matches(state, sim)

    def test_vigilance_already_in_calm(self, game):
        """Vigilance while already in Calm stays in Calm (no energy from exit)."""
        hand = [sts_sim.Card.Tranquility, sts_sim.Card.Vigilance]
        setup = set_scenario(game, hand=hand, energy=5, player_block=0, monster_hp=20)
        sim = make_watcher_sim(hand=hand, energy=5, player_block=0, monster_hp=20)
        # Enter Calm via Tranquility
        state = play_named_card(game, sim, setup, sts_sim.Card.Tranquility)
        # Play Vigilance (already in Calm, should stay, no energy gain)
        state = play_named_card(game, sim, state, sts_sim.Card.Vigilance)
        assert_player_matches(state, sim)
