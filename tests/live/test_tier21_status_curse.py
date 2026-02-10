"""Tier 21: Status and Curse card verification.

Tests verify that status and curse cards behave correctly in both
the live game and the simulator: unplayable cards block hand slots,
playable status cards (Slimed) cost energy properly, and cards with
draw-time effects (Void) trigger correctly.

Note: Wound is not implemented in the BG mod (no BGWound card).
Note: BG mod status cards implement CardDisappearsOnExhaust so they
vanish from the exhaust pile after being exhausted.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
)


# ── Slimed: playable status, costs 1, exhausts (then disappears) ────────


def test_slimed_plays_and_costs_energy(game):
    """Slimed costs 1 energy, does nothing, and exhausts.

    Setup: Slimed in hand, energy=3.
    After play: energy=2. Slimed disappears from exhaust
    (BG mod: CardDisappearsOnExhaust), so exhaust pile is empty.
    """
    hand = [sts_sim.Card.Slimed]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 2, (
        f"Expected 2 energy after Slimed (cost 1), got {state.combat_state.player.energy}"
    )


# ── Dazed: unplayable, ethereal ─────────────────────────────────────────


def test_dazed_in_hand_with_playable(game):
    """Dazed is unplayable and ethereal — verify it stays while playing other cards.

    Setup: Dazed + Strike in hand, monster at 30 HP.
    Play Strike, verify Dazed remains in hand.
    (Dazed would exhaust at end of turn due to ethereal, but we don't end turn.)
    """
    hand = [sts_sim.Card.StrikeRed, sts_sim.Card.Dazed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StrikeRed,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


# ── Burn: unplayable, deals self-damage at end of turn ──────────────────


def test_burn_in_hand_with_playable(game):
    """Burn is unplayable — verify it stays in hand while other cards play.

    Setup: Burn + Strike in hand, monster at 30 HP.
    Play Strike, verify Burn remains in hand.
    (Burn would deal self-damage at end of turn, tested by end-turn flow.)
    """
    hand = [sts_sim.Card.StrikeRed, sts_sim.Card.Burn]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StrikeRed,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


# ── VoidCard: when drawn, lose 1 energy ─────────────────────────────────


def test_void_card_draw_energy_loss(game):
    """VoidCard auto-plays when drawn, costing 1 energy, then exhausts and vanishes.

    Setup: PommelStrike in hand, VoidCard in draw pile, energy=3, monster=30.
    Play PommelStrike (cost 1, draws 1). Void drawn → auto-plays (cost 1) → exhausts → vanishes.
    Expected energy: 3 - 1 (PommelStrike cost) - 1 (Void auto-play) = 1.
    VoidCard won't be in hand (auto-played) or exhaust (CardDisappearsOnExhaust).
    """
    hand = [sts_sim.Card.PommelStrike]
    draw = [sts_sim.Card.VoidCard]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── AscendersBane: unplayable, ethereal ─────────────────────────────────


def test_ascenders_bane_in_hand(game):
    """AscendersBane is unplayable and ethereal.

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


# ── Injury: unplayable curse ────────────────────────────────────────────


def test_injury_in_hand(game):
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


# ── Pain: unplayable curse ──────────────────────────────────────────────


def test_pain_in_hand(game):
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


# ── Decay: unplayable curse, deals damage at end of turn ────────────────


def test_decay_in_hand(game):
    """Decay is unplayable — verify it stays in hand while other cards play.

    Setup: Decay + Strike in hand, monster at 30 HP.
    Play Strike, verify Decay remains.
    (Decay deals 1 self-damage at end of turn, tested by end-turn flow.)
    """
    hand = [sts_sim.Card.StrikeRed, sts_sim.Card.Decay]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StrikeRed,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
