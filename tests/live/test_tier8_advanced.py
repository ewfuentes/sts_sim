"""Tier 8: Advanced card mechanics — AoE debuffs, X-cost, power cards,
draw limits, exhaust-for-draw, dynamic damage.

Tests verify more complex card interactions match between live game and sim.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
)


# ── Shockwave: AoE Vulnerable + Weak, exhaust ───────────────────────────

def test_shockwave_aoe_debuffs(game):
    """Shockwave applies Vulnerable and Weak to all enemies and exhausts.

    Setup: Shockwave in hand, monster at 30 HP.
    After play: monster has Vulnerable and Weak, card exhausted.
    """
    hand = [sts_sim.Card.Shockwave]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)

    # Verify both debuffs on monster
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
    assert live_vuln == sim_vuln, f"Vulnerable mismatch: live={live_vuln}, sim={sim_vuln}"
    assert live_weak == sim_weak, f"Weak mismatch: live={live_weak}, sim={sim_weak}"


# ── Whirlwind: X-cost AoE, spend all energy ──────────────────────────────

def test_whirlwind_spends_all_energy(game):
    """Whirlwind hits all enemies X times where X = current energy.

    Setup: Whirlwind in hand, 3 energy, monster at 30 HP.
    After play: monster takes X * base_damage, energy = 0.
    """
    hand = [sts_sim.Card.Whirlwind]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, choices=[3])

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)

    # Sanity: energy should be 0
    assert state.combat_state.player.energy == 0, (
        f"Expected 0 energy after Whirlwind, got {state.combat_state.player.energy}"
    )


# ── Inflame: power card, permanent +1 Strength ──────────────────────────

def test_inflame_permanent_strength(game):
    """Inflame is a power card that grants permanent Strength.

    Setup: Inflame + Strike in hand, monster at 30 HP.
    Play Inflame, then Strike. Strike should deal base + 1 damage.
    Inflame should not appear in discard (power cards are removed).
    """
    hand = [sts_sim.Card.Inflame, sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play Inflame
    state = play_named_card(game, sim, setup, sts_sim.Card.Inflame)
    assert_player_matches(state, sim)

    # Inflame should not be in discard (power cards are removed from play)
    assert_discard_matches(state, sim)

    # Play Strike — should benefit from +1 Strength
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── BattleTrance: draw 3, can't draw more this turn ─────────────────────

def test_battle_trance_draw_and_no_draw(game):
    """BattleTrance draws 3 cards and prevents further draws.

    Setup: BattleTrance in hand, 3 Strikes in draw pile.
    After play: 3 Strikes drawn to hand, BattleTrance in discard.
    """
    hand = [sts_sim.Card.BattleTrance]
    draw = [sts_sim.Card.StrikeRed, sts_sim.Card.DefendRed, sts_sim.Card.StrikeRed]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)

    # Sanity: should have drawn 3 cards
    assert len(state.combat_state.hand) == 3, (
        f"Expected 3 cards in hand, got {len(state.combat_state.hand)}"
    )


# ── BurningPact: exhaust 1 from hand, draw cards ────────────────────────

def test_burning_pact_exhaust_and_draw(game):
    """BurningPact exhausts 1 card from hand, then draws 2.

    Setup: BurningPact + Strike in hand, 2 Defends in draw pile.
    After play: Strike exhausted, 2 Defends drawn, BurningPact in discard.
    With only 1 card in hand when exhaust triggers, choice is deterministic.
    """
    hand = [sts_sim.Card.BurningPact, sts_sim.Card.StrikeRed]
    draw = [sts_sim.Card.DefendRed, sts_sim.Card.DefendRed]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BurningPact)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── WildStrike: damage + add Dazed to draw pile ─────────────────────────

def test_wild_strike_adds_dazed(game):
    """WildStrike deals damage and adds a Dazed to draw pile.

    Setup: WildStrike in hand, empty draw pile, monster at 30 HP.
    After play: monster takes damage, Dazed in draw pile.
    """
    hand = [sts_sim.Card.WildStrike]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_draw_pile_matches(state, sim)


# ── Rampage: damage = exhaust pile size ──────────────────────────────────

def test_rampage_scales_with_exhaust(game):
    """Rampage deals damage equal to exhaust pile size.

    Setup: Rampage in hand, 1 card already exhausted (via SeeingRed first).
    Use SeeingRed to get a card into exhaust pile, then play Rampage.
    """
    hand = [sts_sim.Card.SeeingRed, sts_sim.Card.Rampage]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play SeeingRed first (exhausts itself, gains 2 energy)
    state = play_named_card(game, sim, setup, sts_sim.Card.SeeingRed)

    # Now Rampage is alone in hand at index 0, exhaust pile has SeeingRed
    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
