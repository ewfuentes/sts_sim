"""Tier 13: Power effect verification + remaining deferred cards.

Tests verify that power effects actually trigger (not just cost/removal),
covers Havoc, DoubleTap, Feed, and DoubleTap interaction edge cases.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_discard_matches, assert_exhaust_matches,
)


# ── Power Effect Tests ──────────────────────────────────────────────────


def test_feel_no_pain_block_on_exhaust(game):
    """FeelNoPain triggers block gain when a card is exhausted.

    Setup: FeelNoPain + TrueGrit + StrikeRed, energy=3, monster=30.
    Play FeelNoPain (cost 1), play TrueGrit (cost 1, block=1, exhausts Strike).
    FeelNoPain triggers: +1 block. Total block = 1 (TrueGrit) + 1 (FnP) = 2.
    """
    hand = [sts_sim.Card.FeelNoPain, sts_sim.Card.TrueGrit, sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play FeelNoPain (power, cost 1)
    state = play_named_card(game, sim, setup, sts_sim.Card.FeelNoPain)

    # Play TrueGrit by name (hand has 2 cards, ordering may differ between game/sim)
    state = play_named_card(game, sim, state, sts_sim.Card.TrueGrit)

    assert_player_matches(state, sim)
    assert state.combat_state.player.block == 2, (
        f"Expected 2 block (1 TrueGrit + 1 FnP), got {state.combat_state.player.block}"
    )


def test_dark_embrace_draw_on_exhaust(game):
    """DarkEmbrace triggers a card draw when a card is exhausted.

    Setup: DarkEmbrace + SeeingRed, draw=[StrikeRed], energy=3, monster=30.
    Play DarkEmbrace (cost 2), play SeeingRed (cost 1, exhausts, +2 energy).
    DarkEmbrace triggers: draw 1 -> StrikeRed. Hand=[StrikeRed].
    """
    hand = [sts_sim.Card.DarkEmbrace, sts_sim.Card.SeeingRed]
    draw = [sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    # Play DarkEmbrace (power, cost 2)
    state = play_named_card(game, sim, setup, sts_sim.Card.DarkEmbrace)

    # Play SeeingRed (cost 1, exhausts, +2 energy, triggers DarkEmbrace draw)
    state = play_card_both(game, sim, hand_index=0, target_index=None)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


def test_corruption_free_exhaust_skills(game):
    """Corruption makes skills cost 0 and exhaust on play.

    Setup: Corruption + DefendRed, energy=3, monster=30.
    Play Corruption (cost 3, energy->0). Play DefendRed (cost 0 due to Corruption,
    block=1, exhausts). Verify energy=0, block=1, DefendRed in exhaust.
    """
    hand = [sts_sim.Card.Corruption, sts_sim.Card.DefendRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play Corruption (power, cost 3)
    state = play_named_card(game, sim, setup, sts_sim.Card.Corruption)

    # Play DefendRed (free due to Corruption, exhausts)
    state = play_card_both(game, sim, hand_index=0, target_index=None)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert state.combat_state.player.energy == 0, (
        f"Expected 0 energy, got {state.combat_state.player.energy}"
    )
    assert state.combat_state.player.block == 1, (
        f"Expected 1 block, got {state.combat_state.player.block}"
    )


def test_juggernaut_damage_on_block(game):
    """Juggernaut deals damage to a random enemy when player gains block.

    Setup: Juggernaut + DefendRed, energy=3, monster=30.
    Play Juggernaut (cost 2), play DefendRed (cost 1, block=1).
    Juggernaut triggers: 1 damage to monster[0]. Monster HP=29, block=1.
    """
    hand = [sts_sim.Card.Juggernaut, sts_sim.Card.DefendRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play Juggernaut (power, cost 2)
    state = play_named_card(game, sim, setup, sts_sim.Card.Juggernaut)

    # Play DefendRed (cost 1, block=1, triggers Juggernaut)
    state = play_card_both(game, sim, hand_index=0, target_index=None)

    assert_player_matches(state, sim)
    assert_monsters_match(state, sim)
    assert state.combat_state.player.block == 1, (
        f"Expected 1 block, got {state.combat_state.player.block}"
    )


# ── Remaining Card Tests ────────────────────────────────────────────────


def test_havoc_plays_top_card(game):
    """Havoc plays the top card of draw pile for free and exhausts it.

    Setup: Havoc in hand, StrikeRed on top of draw pile, energy=3, monster=30.
    Havoc (cost 1) auto-plays Strike for free. Monster takes 1 damage -> 29.
    Energy=2 (only Havoc's cost). Strike is exhausted.
    """
    hand = [sts_sim.Card.Havoc]
    draw = [sts_sim.Card.StrikeRed]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=None)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert state.combat_state.player.energy == 2, (
        f"Expected 2 energy (only Havoc cost), got {state.combat_state.player.energy}"
    )


def test_double_tap_replays_attack(game):
    """DoubleTap causes the next attack to be played twice.

    Setup: DoubleTap + StrikeRed, energy=3, monster=30.
    Play DoubleTap (cost 1), play Strike (cost 1, target=0).
    Strike hits twice: monster takes 1+1=2 damage -> 28. Energy=1.
    """
    hand = [sts_sim.Card.DoubleTap, sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play DoubleTap (skill, cost 1)
    state = play_named_card(game, sim, setup, sts_sim.Card.DoubleTap)

    # Play Strike (cost 1, target=0, replayed by DoubleTap)
    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 1, (
        f"Expected 1 energy, got {state.combat_state.player.energy}"
    )


def test_feed_damage_and_exhaust(game):
    """Feed deals damage and exhausts (non-kill path).

    Setup: Feed in hand, energy=3, monster=30, target=0.
    Feed deals 3 damage (30->27), exhausts. Monster survives.
    """
    hand = [sts_sim.Card.Feed]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── DoubleTap Interaction Tests ─────────────────────────────────────────


def test_double_tap_vulnerable_interaction(game):
    """DoubleTap + Strike on a Vulnerable monster: Vuln consumed on first hit.

    Setup: DoubleTap + StrikeRed, energy=3, monster=30, monster Vulnerable=1.
    Play DoubleTap, play Strike. Hit 1: 1*2=2 dmg (Vuln), Vuln consumed (1->0).
    Hit 2: 1 dmg (no Vuln). Monster=27, Vuln=0.
    """
    hand = [sts_sim.Card.DoubleTap, sts_sim.Card.StrikeRed]

    setup = set_scenario(
        game, hand=hand, energy=3, monster_hp=30,
        monster_powers={"Vulnerable": 1},
    )
    sim = make_sim(
        hand=hand, energy=3, monster_hp=30,
        monster_powers={"Vulnerable": 1},
    )

    # Play DoubleTap
    state = play_named_card(game, sim, setup, sts_sim.Card.DoubleTap)

    # Play Strike on Vulnerable monster
    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_double_tap_bash_secondary_effects(game):
    """DoubleTap + Bash: both hits apply Vuln, second hit benefits from first's Vuln.

    Setup: DoubleTap + Bash, energy=3, monster=30.
    Play DoubleTap (cost 1), play Bash (cost 2, target=0).
    Hit 1: 2 dmg, apply Vuln=1. Hit 2: 2*2=4 dmg (Vuln bonus), apply Vuln=1
    (total=2), consume Vuln (2->1). Monster=24, Vuln=1.
    """
    hand = [sts_sim.Card.DoubleTap, sts_sim.Card.Bash]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play DoubleTap (cost 1)
    state = play_named_card(game, sim, setup, sts_sim.Card.DoubleTap)

    # Play Bash (cost 2, target=0, replayed by DoubleTap)
    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_double_tap_feed_double_damage(game):
    """DoubleTap + Feed deals damage twice (non-kill path).

    Setup: DoubleTap + Feed, energy=3, monster=30.
    Play DoubleTap (cost 1), play Feed (cost 1, target=0).
    Hit 1: 3 dmg. Hit 2: 3 dmg (replay). Monster=24. Energy=1.
    Feed exhausts.
    """
    hand = [sts_sim.Card.DoubleTap, sts_sim.Card.Feed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play DoubleTap (cost 1)
    state = play_named_card(game, sim, setup, sts_sim.Card.DoubleTap)

    # Play Feed (cost 1, target=0, replayed by DoubleTap)
    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
