"""Live verification tests for Watcher Rare cards.

Tests verify that Watcher rare card mechanics match between the live
BG mod game and the Rust simulator.

NOTE: TalkToTheHand is [N] (not in simulator) -- all its tests are skipped.
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


@pytest.mark.usefixtures("single_monster_fight")
class TestCards:

    # ===================================================================
    # RAGNAROK
    # ===================================================================

    def test_ragnarok_basic(self, game):
        """Ragnarok: 5 hits of 1 damage, cost 3."""
        hand = [sts_sim.Card.Ragnarok]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Ragnarok, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_ragnarok_with_strength(self, game):
        """Ragnarok with 2 Strength: 5 hits of 3 damage each."""
        hand = [sts_sim.Card.Ragnarok]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                             player_powers={"Strength": 2})
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30,
                               player_powers={"Strength": 2})
        state = play_named_card(game, sim, setup, sts_sim.Card.Ragnarok, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    def test_ragnarok_upgraded(self, game):
        """Upgraded Ragnarok: 6 hits of 1 damage."""
        hand = [(sts_sim.Card.Ragnarok, True)]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Ragnarok,
                                target_index=0, upgraded=True)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # BRILLIANCE
    # ===================================================================

    def test_brilliance_basic(self, game):
        """BrillianceCard: base damage."""
        hand = [sts_sim.Card.BrillianceCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.BrillianceCard, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # BLASPHEMY
    # ===================================================================

    def test_blasphemy_exhaust(self, game):
        """Blasphemy: exhausts when played."""
        hand = [sts_sim.Card.Blasphemy]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.Blasphemy)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    # ===================================================================
    # DEUS EX MACHINA
    # ===================================================================

    def test_deus_ex_machina_basic(self, game):
        """Deus Ex Machina: cost 0, exhausts."""
        hand = [sts_sim.Card.DeusExMachina]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.DeusExMachina)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    # ===================================================================
    # SCRAWL
    # ===================================================================

    def test_scrawl_draw_exhaust(self, game):
        """ScrawlCard: draws cards and exhausts."""
        hand = [sts_sim.Card.ScrawlCard]
        draw = [sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
                sts_sim.Card.StrikePurple, sts_sim.Card.DefendPurple,
                sts_sim.Card.StrikePurple]
        setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.ScrawlCard)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)
        assert_hand_matches(state, sim)
        assert_draw_pile_matches(state, sim)

    # ===================================================================
    # WISH
    # ===================================================================

    def test_wish_strength(self, game):
        """WishCard: choose Strength, exhausts."""
        hand = [sts_sim.Card.WishCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.WishCard, choices=[0])
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    def test_wish_block(self, game):
        """WishCard: choose Block, exhausts."""
        hand = [sts_sim.Card.WishCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.WishCard, choices=[1])
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    # ===================================================================
    # SPIRIT SHIELD
    # ===================================================================

    def test_spirit_shield_basic(self, game):
        """SpiritShieldCard: block per card in hand, exhausts."""
        hand = [sts_sim.Card.SpiritShieldCard, sts_sim.Card.StrikePurple,
                sts_sim.Card.DefendPurple]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.SpiritShieldCard)
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    # ===================================================================
    # JUDGMENT
    # ===================================================================

    def test_judgment_above_threshold(self, game):
        """JudgmentCard: no effect on enemy above 7 HP."""
        hand = [sts_sim.Card.JudgmentCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.JudgmentCard, target_index=0)
        assert_monsters_match(state, sim)
        assert_player_matches(state, sim)

    # ===================================================================
    # WORSHIP
    # ===================================================================

    def test_worship_x_cost(self, game):
        """WorshipCard: X-cost, exhausts."""
        hand = [sts_sim.Card.WorshipCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.WorshipCard, choices=[3])
        assert_player_matches(state, sim)
        assert_exhaust_matches(state, sim)

    # ===================================================================
    # RARE POWERS (play cost verification)
    # ===================================================================

    def test_omega_play(self, game):
        """OmegaCard: cost 3 power."""
        hand = [sts_sim.Card.OmegaCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.OmegaCard)
        assert_player_matches(state, sim)

    def test_deva_form_play(self, game):
        """DevaFormCard: cost 3 power."""
        hand = [sts_sim.Card.DevaFormCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.DevaFormCard)
        assert_player_matches(state, sim)

    def test_devotion_play(self, game):
        """DevotionCard: cost 1 power."""
        hand = [sts_sim.Card.DevotionCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.DevotionCard)
        assert_player_matches(state, sim)

    def test_establishment_play(self, game):
        """EstablishmentCard: cost 1 power."""
        hand = [sts_sim.Card.EstablishmentCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.EstablishmentCard)
        assert_player_matches(state, sim)

    def test_conjure_blade_x_cost(self, game):
        """ConjureBladeCard: X-cost power."""
        hand = [sts_sim.Card.ConjureBladeCard]
        setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
        sim = make_watcher_sim(hand=hand, energy=3, monster_hp=30)
        state = play_named_card(game, sim, setup, sts_sim.Card.ConjureBladeCard, choices=[3])
        assert_player_matches(state, sim)
