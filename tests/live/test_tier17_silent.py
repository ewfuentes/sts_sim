"""Tier 17: Silent character base card tests.

Each test:
1. Uses the set command to configure a precise game state
2. Plays a card in both the live game and the simulator
3. Asserts that results match between live game and simulator

Covers all Silent cards: starters, common attacks, common skills, common
powers, uncommon attacks, uncommon skills, uncommon powers, rare attacks,
rare skills, and rare powers.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
)


# ===========================================================================
# Starters
# ===========================================================================


def test_strike_green_damage(game):
    """StrikeGreen deals damage to a target. Cost 1, damage 1."""
    hand = [sts_sim.Card.StrikeGreen]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_defend_green_block(game):
    """DefendGreen grants block. Cost 1, block 1."""
    hand = [sts_sim.Card.DefendGreen]

    set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_neutralize_damage_and_weak(game):
    """Neutralize deals damage and applies Weak. Cost 0, damage 1, magic 1."""
    hand = [sts_sim.Card.Neutralize]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_survivor_block_and_discard(game):
    """Survivor grants block and discards 1 card from hand. Cost 1, block 2.

    Setup: Survivor + StrikeGreen in hand. After play: block gained,
    StrikeGreen discarded (only card remaining when discard triggers).
    """
    hand = [sts_sim.Card.Survivor, sts_sim.Card.StrikeGreen]

    setup = set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Survivor)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)


# ===========================================================================
# Common Attacks
# ===========================================================================


def test_poisoned_stab_damage_poison_exhaust(game):
    """PoisonedStab deals damage, applies poison, exhausts. Cost 1, damage 1, magic 1."""
    hand = [sts_sim.Card.PoisonedStab]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_dagger_throw_damage_draw_discard(game):
    """DaggerThrow deals damage, draws 1, discards 1. Cost 1, damage 2.

    Setup: DaggerThrow + DefendGreen in hand, StrikeGreen in draw pile.
    After play: monster takes damage, StrikeGreen drawn, DefendGreen discarded
    (only card in hand when discard triggers).
    """
    hand = [sts_sim.Card.DaggerThrow, sts_sim.Card.DefendGreen]
    draw = [sts_sim.Card.StrikeGreen]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DaggerThrow,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


def test_dagger_spray_aoe_damage(game):
    """DaggerSpray hits all enemies. Cost 1, damage 1, magic 2 (hits)."""
    hand = [sts_sim.Card.DaggerSpray]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_sneaky_strike_damage(game):
    """SneakyStrike deals damage. Cost 2, damage 3."""
    hand = [sts_sim.Card.SneakyStrike]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_slice_damage(game):
    """Slice deals damage at 0 cost. Cost 0, damage 1."""
    hand = [sts_sim.Card.Slice]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ===========================================================================
# Common Skills
# ===========================================================================


def test_backflip_block_and_draw(game):
    """Backflip grants block and draws 2 cards. Cost 1.

    Setup: Backflip in hand, 2 StrikeGreen in draw pile.
    After play: block gained, 2 cards drawn to hand.
    """
    hand = [sts_sim.Card.Backflip]
    draw = [sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3,
                 player_block=0, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3,
                   player_block=0, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


def test_dodge_and_roll_block(game):
    """DodgeAndRoll grants block. Cost 1, block 1, magic 2."""
    hand = [sts_sim.Card.DodgeAndRoll]

    set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_deflect_block(game):
    """Deflect grants block at 0 cost. Cost 0, block 1."""
    hand = [sts_sim.Card.Deflect]

    set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_cloak_and_dagger_block_and_shivs(game):
    """CloakAndDagger grants block and adds Shivs to hand. Cost 1, block 1, magic 1."""
    hand = [sts_sim.Card.CloakAndDagger]

    set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)


def test_blade_dance_shivs(game):
    """BladeDance adds Shivs to hand. Cost 1, magic 2."""
    hand = [sts_sim.Card.BladeDance]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)


def test_prepared_draw_and_discard(game):
    """Prepared draws 1 and discards 1. Cost 0, magic 1.

    Setup: Prepared in hand, StrikeGreen in draw pile. Empty draw pile after draw.
    After play: StrikeGreen drawn then discarded (only card in hand).
    """
    hand = [sts_sim.Card.Prepared]
    draw = [sts_sim.Card.StrikeGreen]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


def test_deadly_poison_apply_poison(game):
    """DeadlyPoison applies poison to target. Cost 1, magic 1."""
    hand = [sts_sim.Card.DeadlyPoison]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_acrobatics_draw_and_discard(game):
    """Acrobatics draws 3 cards then discards 1. Cost 1, magic 3.

    Setup: Acrobatics in hand, 3 StrikeGreen in draw pile.
    After play: 3 cards drawn, 1 discarded (deterministic with 1 card in hand
    after draw, when only the drawn cards remain, the first one is discarded).
    """
    hand = [sts_sim.Card.Acrobatics]
    draw = [sts_sim.Card.StrikeGreen, sts_sim.Card.DefendGreen,
            sts_sim.Card.StrikeGreen]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


# ===========================================================================
# Common Powers
# ===========================================================================


def test_accuracy_power(game):
    """AccuracyCard is a power card that costs 1 energy.

    After play: energy=2, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.AccuracyCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_after_image_power(game):
    """AfterImageCard is a power card that costs 1 energy.

    After play: energy=2, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.AfterImageCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===========================================================================
# Uncommon Attacks
# ===========================================================================


def test_backstab_damage_and_exhaust(game):
    """Backstab deals bonus damage to full HP target, exhausts. Cost 0, damage 2, magic 2."""
    hand = [sts_sim.Card.Backstab]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_bane_damage_with_poison(game):
    """Bane deals bonus damage if target has Poison. Cost 1, damage 2, magic 2.

    Setup: Apply poison via DeadlyPoison first, then play Bane.
    """
    hand = [sts_sim.Card.DeadlyPoison, sts_sim.Card.Bane]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Apply poison first
    state = play_named_card(game, sim, setup, sts_sim.Card.DeadlyPoison,
                            target_index=0)

    # Play Bane on poisoned target
    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_choke_damage(game):
    """Choke deals damage. Cost 2, damage 3, magic 1."""
    hand = [sts_sim.Card.Choke]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_predator_damage_and_draw(game):
    """Predator deals damage and draws cards. Cost 2, damage 3, magic 2.

    Setup: Predator in hand, 2 cards in draw pile.
    After play: monster takes damage, 2 cards drawn.
    """
    hand = [sts_sim.Card.Predator]
    draw = [sts_sim.Card.StrikeGreen, sts_sim.Card.DefendGreen]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


def test_masterful_stab_damage(game):
    """MasterfulStab deals damage. Cost 0, damage 2."""
    hand = [sts_sim.Card.MasterfulStab]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_dash_damage_and_block(game):
    """Dash deals damage and grants block. Cost 2, damage 2, block 2."""
    hand = [sts_sim.Card.Dash]

    set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_finisher_damage_per_attack(game):
    """Finisher deals damage per attack played this turn. Cost 1, damage 1 per attack.

    Setup: Slice (attack) + Finisher. Play Slice first, then Finisher.
    Finisher should deal damage based on 1 attack played this turn.
    """
    hand = [sts_sim.Card.Slice, sts_sim.Card.Finisher]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play Slice first (0-cost attack)
    state = play_named_card(game, sim, setup, sts_sim.Card.Slice,
                            target_index=0)

    # Play Finisher (1 attack played this turn)
    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_flechettes_damage_per_skill(game):
    """Flechettes deals damage per skill in hand. Cost 1, damage 1 per skill.

    Setup: Flechettes + 2 skills in hand.
    """
    hand = [sts_sim.Card.Flechettes, sts_sim.Card.Deflect, sts_sim.Card.Deflect]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Flechettes,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_all_out_attack_aoe_and_discard(game):
    """AllOutAttack hits all enemies and discards a random card. Cost 1, damage 2.

    Setup: AllOutAttack + StrikeGreen in hand. After play: monster takes damage,
    StrikeGreen discarded (only card remaining when discard triggers).
    """
    hand = [sts_sim.Card.AllOutAttack, sts_sim.Card.StrikeGreen]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.AllOutAttack)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)


def test_unload_damage_and_discard(game):
    """Unload deals damage and discards a card. Cost 1, damage 2, magic 1.

    Setup: Unload + DefendGreen in hand. After play: monster takes damage,
    DefendGreen discarded.
    """
    hand = [sts_sim.Card.Unload, sts_sim.Card.DefendGreen]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Unload,
                            target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)


# ===========================================================================
# Uncommon Skills
# ===========================================================================


def test_blur_block(game):
    """Blur grants block (block not lost next turn). Cost 1, block 2."""
    hand = [sts_sim.Card.Blur]

    set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_bouncing_flask_poison(game):
    """BouncingFlask applies poison to target. Cost 2, magic 2."""
    hand = [sts_sim.Card.BouncingFlask]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_concentrate_exhaust(game):
    """Concentrate exhausts. Cost 0.

    Setup: Concentrate alone in hand.
    After play: exhausted.
    """
    hand = [sts_sim.Card.Concentrate]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_calculated_gamble_redraw(game):
    """CalculatedGamble discards hand and draws same count. Cost 0, exhausts.

    Setup: CalculatedGamble + StrikeGreen in hand, 2 DefendGreen in draw pile.
    After play: hand discarded, 2 cards drawn (hand size was 2 before play
    including CalculatedGamble), CalculatedGamble exhausted.
    """
    hand = [sts_sim.Card.CalculatedGamble, sts_sim.Card.StrikeGreen]
    draw = [sts_sim.Card.DefendGreen, sts_sim.Card.DefendGreen]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CalculatedGamble)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_catalyst_doubles_poison(game):
    """Catalyst doubles poison on target, exhausts. Cost 1.

    Setup: Apply poison first via DeadlyPoison, then Catalyst.
    """
    hand = [sts_sim.Card.DeadlyPoison, sts_sim.Card.Catalyst]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Apply poison first
    state = play_named_card(game, sim, setup, sts_sim.Card.DeadlyPoison,
                            target_index=0)

    # Play Catalyst to double poison
    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_crippling_cloud_poison_and_exhaust(game):
    """CripplingCloud applies poison to all enemies and exhausts. Cost 2, magic 1."""
    hand = [sts_sim.Card.CripplingCloud]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_leg_sweep_block_and_weak(game):
    """LegSweep grants block and applies Weak to target. Cost 2, block 3, magic 1."""
    hand = [sts_sim.Card.LegSweep]

    set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_player_matches(state, sim)
    assert_monsters_match(state, sim)
    assert_discard_matches(state, sim)


def test_outmaneuver_energy(game):
    """Outmaneuver gives energy. Cost 0, magic 2."""
    hand = [sts_sim.Card.Outmaneuver]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_piercing_wail_block_weak_exhaust(game):
    """PiercingWail grants block and applies Weak to all enemies, exhausts. Cost 1."""
    hand = [sts_sim.Card.PiercingWail]

    set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_monsters_match(state, sim)
    assert_exhaust_matches(state, sim)


def test_escape_plan_block_and_draw(game):
    """EscapePlan grants block and draws 1 card. Cost 0, block 1.

    Setup: EscapePlan in hand, 1 StrikeGreen in draw pile.
    """
    hand = [sts_sim.Card.EscapePlan]
    draw = [sts_sim.Card.StrikeGreen]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3,
                 player_block=0, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3,
                   player_block=0, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


def test_expertise_draws(game):
    """Expertise draws cards up to magic number. Cost 1, magic 6.

    Setup: Expertise in hand, 6 cards in draw pile.
    After play: draws up to 6 cards.
    """
    hand = [sts_sim.Card.Expertise]
    draw = [sts_sim.Card.StrikeGreen, sts_sim.Card.StrikeGreen,
            sts_sim.Card.DefendGreen, sts_sim.Card.DefendGreen,
            sts_sim.Card.StrikeGreen, sts_sim.Card.DefendGreen]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


def test_terror_vulnerable_exhaust(game):
    """Terror applies Vulnerable to target and exhausts. Cost 1, magic 1."""
    hand = [sts_sim.Card.Terror]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_player_matches(state, sim)
    assert_monsters_match(state, sim)
    assert_exhaust_matches(state, sim)


# ===========================================================================
# Uncommon Powers
# ===========================================================================


def test_footwork_power(game):
    """FootworkCard is a power card that costs 2 energy.

    After play: energy=1, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.FootworkCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_noxious_fumes_power(game):
    """NoxiousFumesCard is a power card that costs 1 energy.

    After play: energy=2, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.NoxiousFumesCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_well_laid_plans_power(game):
    """WellLaidPlansCard is a power card that costs 1 energy.

    After play: energy=2, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.WellLaidPlansCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_distraction_power(game):
    """DistractionCard is a power card that costs 2 energy.

    After play: energy=1, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.DistractionCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_infinite_blades_power(game):
    """InfiniteBlades is a power card that costs 1 energy.

    After play: energy=2, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.InfiniteBlades]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===========================================================================
# Rare Attacks
# ===========================================================================


def test_die_die_die_aoe_exhaust(game):
    """DieDieDie deals AoE damage and exhausts. Cost 1, damage 3."""
    hand = [sts_sim.Card.DieDieDie]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_grand_finale_aoe_damage(game):
    """GrandFinale deals heavy AoE damage when draw pile is empty. Cost 0, damage 10.

    Setup: GrandFinale in hand, draw pile empty.
    """
    hand = [sts_sim.Card.GrandFinale]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_skewer_x_cost_damage(game):
    """Skewer deals damage based on energy spent. X-cost, damage 1.

    Setup: Skewer in hand, 3 energy. Spend all 3 energy.
    """
    hand = [sts_sim.Card.Skewer]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0, choices=[3])

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)

    assert state.combat_state.player.energy == 0, (
        f"Expected 0 energy after Skewer, got {state.combat_state.player.energy}"
    )


# ===========================================================================
# Rare Skills
# ===========================================================================


def test_adrenaline_energy_draw_exhaust(game):
    """Adrenaline gains energy, draws cards, and exhausts. Cost 0.

    Setup: Adrenaline in hand, 2 cards in draw pile.
    After play: +1 energy, 2 cards drawn, Adrenaline exhausted.
    """
    hand = [sts_sim.Card.Adrenaline]
    draw = [sts_sim.Card.StrikeGreen, sts_sim.Card.DefendGreen]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_bullet_time(game):
    """BulletTime makes cards cost 0 this turn. Cost 3."""
    hand = [sts_sim.Card.BulletTime]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_malaise_x_cost_weak_exhaust(game):
    """Malaise applies Weak based on energy spent, exhausts. X-cost.

    Setup: Malaise in hand, 3 energy. Spend all 3 energy.
    """
    hand = [sts_sim.Card.Malaise]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0, choices=[3])

    assert_player_matches(state, sim)
    assert_monsters_match(state, sim)
    assert_exhaust_matches(state, sim)

    assert state.combat_state.player.energy == 0, (
        f"Expected 0 energy after Malaise, got {state.combat_state.player.energy}"
    )


def test_storm_of_steel_discard_hand(game):
    """StormOfSteel discards entire hand and gains Shivs. Cost 1.

    Setup: StormOfSteel + 2 cards in hand.
    After play: hand discarded, Shivs added to hand.
    """
    hand = [sts_sim.Card.StormOfSteel, sts_sim.Card.StrikeGreen,
            sts_sim.Card.DefendGreen]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StormOfSteel)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)


def test_doppelganger_copies_strike(game):
    """Doppelganger copies and replays the most recently played card.

    Setup: StrikeGreen + Doppelganger, energy=3, monster_hp=30.
    Play StrikeGreen first (damage 1, energy=2).
    Play Doppelganger: auto-selects X=1, copies Strike, deals 1 damage.
    Assert: monster HP=28, energy=1, Doppelganger exhausted.
    """
    hand = [sts_sim.Card.StrikeGreen, sts_sim.Card.Doppelganger]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play StrikeGreen first
    state = play_named_card(game, sim, setup, sts_sim.Card.StrikeGreen,
                            target_index=0)

    # Play Doppelganger (auto-selects X=1, copies Strike)
    state = play_card_both(game, sim, hand_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_corpse_explosion_poison(game):
    """CorpseExplosionCard applies poison to target. Cost 2, magic 2."""
    hand = [sts_sim.Card.CorpseExplosionCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ===========================================================================
# Rare Powers
# ===========================================================================


def test_a_thousand_cuts_power(game):
    """AThousandCutsCard is a power card that costs 2 energy.

    After play: energy=1, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.AThousandCutsCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_burst_power(game):
    """BurstCard is a power card that costs 1 energy.

    After play: energy=2, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.BurstCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_envenom_power(game):
    """EnvenomCard is a power card that costs 3 energy.

    After play: energy=0, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.EnvenomCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_tools_of_the_trade_power(game):
    """ToolsOfTheTradeCard is a power card that costs 1 energy.

    After play: energy=2, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.ToolsOfTheTradeCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_wraith_form_power(game):
    """WraithFormCard is a power card that costs 3 energy.

    After play: energy=0, discard empty (power removed from play).
    """
    hand = [sts_sim.Card.WraithFormCard]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
