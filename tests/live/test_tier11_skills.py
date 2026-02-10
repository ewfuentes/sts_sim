"""Tier 11: Remaining immediate-effect skills and attacks — block+power,
Strength doubling, exhaust recovery, multi-exhaust damage, AoE.

Tests verify card mechanics match between live game and simulator.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
)


# ── FlameBarrier: block + Thorns power ───────────────────────────────────

def test_flame_barrier_block_and_thorns(game):
    """FlameBarrier gives 3 block and applies Thorns, costs 2 energy.

    Setup: FlameBarrier in hand, 3 energy, monster at 30 HP.
    After play: block=3, energy=1, FlameBarrier in discard.
    """
    hand = [sts_sim.Card.FlameBarrier]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── RageCard: block + Rage power ─────────────────────────────────────────

def test_rage_block_and_power(game):
    """RageCard applies Rage power, costs 1 energy.

    Setup: RageCard in hand, 3 energy, monster at 30 HP.
    After play: block=0, energy=2, RageCard in discard.
    Rage power grants block when attacks are played (not on play).
    """
    hand = [sts_sim.Card.RageCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── LimitBreak: double current Strength ──────────────────────────────────

def test_limit_break_double_strength(game):
    """LimitBreak doubles current Strength, costs 1 energy, exhausts.

    Setup: LimitBreak + Strike in hand, Strength=2, monster at 30 HP.
    Play LimitBreak (Strength 2→4), then Strike (deals 2+4=6 damage).
    """
    hand = [sts_sim.Card.LimitBreak, sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_powers={"Strength": 2})
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   player_powers={"Strength": 2})

    # Play LimitBreak
    state = play_named_card(game, sim, setup, sts_sim.Card.LimitBreak)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)

    # Play Strike — should benefit from doubled Strength (4)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Exhume: recover card from exhaust pile ────────────────────────────────

def test_exhume_recover_card(game):
    """Exhume recovers a card from exhaust pile to hand, then exhausts itself.

    Setup: SeeingRed + Exhume in hand, 3 energy.
    Step 1: Play SeeingRed (exhausts itself, +2 energy).
    Step 2: Play Exhume (recovers SeeingRed from exhaust to hand).
    After: hand=[SeeingRed], exhaust=[Exhume].
    """
    hand = [sts_sim.Card.SeeingRed, sts_sim.Card.Exhume]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play SeeingRed (exhausts itself, gains 2 energy)
    state = play_named_card(game, sim, setup, sts_sim.Card.SeeingRed)

    # Play Exhume (now alone in hand at index 0)
    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── FiendFire: exhaust entire hand, damage per card ──────────────────────

def test_fiend_fire_exhaust_and_damage(game):
    """FiendFire exhausts all cards in hand and deals damage per card exhausted.

    Setup: FiendFire + Strike + Defend in hand, 3 energy, monster at 30 HP.
    After play: Strike and Defend exhausted, FiendFire exhausted,
    monster takes base_damage * 2 damage.
    """
    hand = [sts_sim.Card.FiendFire, sts_sim.Card.StrikeRed,
            sts_sim.Card.DefendRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FiendFire,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Immolate: AoE damage + Dazed to discard ──────────────────────────────

def test_immolate_aoe_and_dazed(game):
    """Immolate deals 5 AoE damage and adds 2 Dazed status cards.

    Setup: Immolate in hand, 3 energy, monster at 30 HP.
    After play: monster at 25, energy=1, Dazed cards added.
    """
    hand = [sts_sim.Card.Immolate]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
