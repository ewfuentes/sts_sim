"""Tier 7: Interesting card effects — self-replication, scaling, doubling,
multi-debuff.

Tests verify more complex card mechanics match between live game and simulator.
"""

import sts_sim

from tests.live.conftest import (
    CARD_TO_BG,
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
)


# ── Anger: damage + self into draw pile ──────────────────────────────────

def test_anger_damage_and_draw_pile(game):
    """Anger deals damage and puts itself (or a copy) somewhere.

    Setup: Anger in hand, empty draw/discard, monster at 30 HP.
    After play: monster takes damage. Verify where Anger ends up
    (draw pile, discard, or both) matches between game and sim.
    """
    hand = [sts_sim.Card.Anger]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


# ── PerfectedStrike: bonus damage per Strike in hand ─────────────────────

def test_perfected_strike_hand_scaling(game):
    """PerfectedStrike gets bonus damage per Strike card in hand.

    Setup: PerfectedStrike + 2 Strikes in hand, monster at 30 HP.
    Bonus should be +magic per Strike (excluding PerfectedStrike itself).
    """
    hand = [
        sts_sim.Card.PerfectedStrike,
        sts_sim.Card.StrikeRed,
        sts_sim.Card.StrikeRed,
    ]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.PerfectedStrike,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Uppercut: damage + Vulnerable + Weak ─────────────────────────────────

def test_uppercut_damage_and_debuffs(game):
    """Uppercut deals damage and applies both Vulnerable and Weak.

    Setup: Uppercut in hand, monster at 30 HP.
    After play: monster takes damage, has both Vulnerable and Weak.
    """
    hand = [sts_sim.Card.Uppercut]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)

    # Verify both debuffs applied
    live_monster = state.combat_state.monsters[0]
    sim_monster = sim.get_monsters()[0]

    live_vuln = None
    live_weak = None
    for p in live_monster.powers:
        if "ulnerable" in p.power_id:
            live_vuln = p.amount
        if "eak" in p.power_id:
            live_weak = p.amount

    sim_vuln = sim_monster.get_power(sts_sim.PowerType.Vulnerable)
    sim_weak = sim_monster.get_power(sts_sim.PowerType.Weak)

    assert live_vuln is not None, "Vulnerable not found on live monster"
    assert live_weak is not None, "Weak not found on live monster"
    assert live_vuln == sim_vuln, (
        f"Vulnerable mismatch: live={live_vuln}, sim={sim_vuln}"
    )
    assert live_weak == sim_weak, (
        f"Weak mismatch: live={live_weak}, sim={sim_weak}"
    )


# ── Entrench: doubles current block ──────────────────────────────────────

def test_entrench_doubles_block(game):
    """Entrench doubles the player's current block.

    Setup: Entrench in hand, player has 3 block.
    After play: player should have 6 block.
    """
    hand = [sts_sim.Card.Entrench]

    set_scenario(game, hand=hand, energy=3, player_block=3, monster_hp=8)
    sim = make_sim(hand=hand, energy=3, player_block=3, monster_hp=8)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)

    # Sanity: block should have doubled
    assert state.combat_state.player.block == 6, (
        f"Expected 6 block (3 doubled), got {state.combat_state.player.block}"
    )
