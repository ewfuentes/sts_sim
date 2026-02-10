"""Tier 6: Multi-target attacks, status application, energy generation.

Tests verify AoE damage (Cleave), Weak application (Clothesline),
and energy generation (Seeing Red already covered in tier 3).
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_discard_matches,
)


# ── Cleave: AoE damage ──────────────────────────────────────────────────

def test_cleave_damage(game):
    """Cleave hits all enemies. Verify damage with single monster.

    Setup: Cleave in hand, monster at 8 HP.
    After play: monster takes Cleave base damage.
    """
    hand = [sts_sim.Card.Cleave]

    set_scenario(game, hand=hand, energy=3, monster_hp=8)
    sim = make_sim(hand=hand, energy=3, monster_hp=8)

    # Cleave has no target (AoE)
    state = play_card_both(game, sim, hand_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Clothesline: damage + apply Weak ─────────────────────────────────────

def test_clothesline_damage_and_weak(game):
    """Clothesline deals damage and applies Weak to the target.

    Setup: Clothesline in hand, monster at 30 HP, no existing debuffs.
    After play: monster takes damage AND gains Weak stacks.
    """
    hand = [sts_sim.Card.Clothesline]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)

    # Verify Weak was applied
    live_monster = state.combat_state.monsters[0]
    sim_monster = sim.get_monsters()[0]

    live_weak = None
    for p in live_monster.powers:
        if "eak" in p.power_id:  # Match "Weak" or "BGWeakened"
            live_weak = p.amount
            break

    sim_weak = sim_monster.get_power(sts_sim.PowerType.Weak)

    assert live_weak is not None, "Weak not found on live monster"
    assert live_weak == sim_weak, (
        f"Weak mismatch: live={live_weak}, sim={sim_weak}"
    )


# ── Flex + Vulnerable combined: strength boosts doubled damage ───────────

def test_flex_and_vulnerable_combined(game):
    """Flex + Vulnerable: Strength bonus is also doubled by Vulnerable.

    Setup: Flex + Strike, monster Vulnerable=1, HP=30.
    Play Flex (gain Str), then Strike on Vulnerable monster.
    The (base + Str) damage should be doubled by Vulnerable.
    """
    hand = [sts_sim.Card.Flex, sts_sim.Card.StrikeRed]

    setup = set_scenario(
        game, hand=hand, energy=3, monster_hp=30,
        monster_powers={"Vulnerable": 1},
    )
    sim = make_sim(
        hand=hand, energy=3, monster_hp=30,
        monster_powers={"Vulnerable": 1},
    )

    from tests.live.conftest import play_named_card

    # Play Flex (no target)
    state = play_named_card(game, sim, setup, sts_sim.Card.Flex)

    # Play Strike on Vulnerable monster
    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
