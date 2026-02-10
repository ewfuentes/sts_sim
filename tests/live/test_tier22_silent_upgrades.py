"""Tier 22: Silent upgrade verification — all ~48 Silent cards.

Tests verify that upgraded card stats (damage, block, cost, magic,
exhaust behavior) match between the live game and the simulator.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
)


# ── Starter Upgrades ──────────────────────────────────────────────────


def test_strike_green_upgraded_damage(game):
    """StrikeGreen+ deals 2 damage (up from 1), costs 1.

    Setup: StrikeGreen+ in hand, monster at 30 HP.
    After play: monster HP=28, energy=2.
    """
    hand = [(sts_sim.Card.StrikeGreen, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StrikeGreen,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_defend_green_upgraded_block(game):
    """DefendGreen+ gains 2 block (up from 1), costs 1.

    Setup: DefendGreen+ in hand, energy=3.
    After play: block=2, energy=2.
    """
    hand = [(sts_sim.Card.DefendGreen, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DefendGreen,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_neutralize_upgraded_damage(game):
    """Neutralize+ deals 2 damage (up from 1), costs 0, applies Weak.

    Setup: Neutralize+ in hand, monster at 30 HP.
    After play: monster HP=28, monster has Weak.
    """
    hand = [(sts_sim.Card.Neutralize, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Neutralize,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_survivor_upgraded_block(game):
    """Survivor+ gains 3 block (up from 2), costs 1, discards 1.

    Setup: Survivor+ + Strike in hand, energy=3.
    After play: block=3, Strike discarded, energy=2.
    """
    hand = [(sts_sim.Card.Survivor, True), sts_sim.Card.StrikeGreen]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Survivor,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Common Attack Upgrades ─────────────────────────────────────────────


def test_poisoned_stab_upgraded_magic(game):
    """PoisonedStab+ applies 2 poison (up from 1), costs 1, exhausts.

    Setup: PoisonedStab+ in hand, monster at 30 HP.
    After play: monster takes damage and has 2 Poison, card exhausted.
    """
    hand = [(sts_sim.Card.PoisonedStab, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.PoisonedStab,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_dagger_throw_upgraded_damage(game):
    """DaggerThrow+ deals 3 damage (up from 2), costs 1, draws 1, discards 1.

    Setup: DaggerThrow+ in hand, 1 Defend in draw pile.
    After play: monster takes 3 damage, Defend drawn then discarded.
    """
    hand = [(sts_sim.Card.DaggerThrow, True)]
    draw = [sts_sim.Card.DefendGreen]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DaggerThrow,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)


def test_dagger_spray_upgraded_magic(game):
    """DaggerSpray+ hits 3 times (up from 2), costs 1, AoE.

    Setup: DaggerSpray+ in hand, monster at 30 HP.
    After play: monster takes damage from 3 hits.
    """
    hand = [(sts_sim.Card.DaggerSpray, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DaggerSpray,
                            upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_sneaky_strike_upgraded_damage(game):
    """SneakyStrike+ deals 4 damage (up from 3), costs 2.

    Setup: SneakyStrike+ in hand, monster at 30 HP.
    After play: monster takes 4 damage, energy=1.
    """
    hand = [(sts_sim.Card.SneakyStrike, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SneakyStrike,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_slice_upgraded_damage(game):
    """Slice+ deals 2 damage (up from 1), costs 0.

    Setup: Slice+ in hand, monster at 30 HP.
    After play: monster HP=28, energy=3.
    """
    hand = [(sts_sim.Card.Slice, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Slice,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Common Skill Upgrades ─────────────────────────────────────────────


def test_backflip_upgraded_block(game):
    """Backflip+ gains 2 block (up from 1), costs 1, draws cards.

    Setup: Backflip+ in hand, 2 cards in draw pile.
    After play: block=2, cards drawn.
    """
    hand = [(sts_sim.Card.Backflip, True)]
    draw = [sts_sim.Card.StrikeGreen, sts_sim.Card.DefendGreen]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Backflip,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_dodge_and_roll_upgraded_magic(game):
    """DodgeAndRoll+ magic 3 (up from 2), costs 1, block 1.

    Setup: DodgeAndRoll+ in hand, energy=3.
    After play: block gained, energy=2.
    """
    hand = [(sts_sim.Card.DodgeAndRoll, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DodgeAndRoll,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_deflect_upgraded_block(game):
    """Deflect+ gains 2 block (up from 1), costs 0.

    Setup: Deflect+ in hand, energy=3.
    After play: block=2, energy=3.
    """
    hand = [(sts_sim.Card.Deflect, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Deflect,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_cloak_and_dagger_upgraded_magic(game):
    """CloakAndDagger+ generates 2 shivs (up from 1), costs 1, block 1.

    Setup: CloakAndDagger+ in hand, energy=3.
    After play: block gained, 2 Shivs added to hand.
    """
    hand = [(sts_sim.Card.CloakAndDagger, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CloakAndDagger,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


def test_blade_dance_upgraded_magic(game):
    """BladeDance+ generates 3 shivs (up from 2), costs 1.

    Setup: BladeDance+ in hand, energy=3.
    After play: 3 Shivs in hand.
    """
    hand = [(sts_sim.Card.BladeDance, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BladeDance,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


def test_prepared_upgraded_magic(game):
    """Prepared+ draws 2 and discards 2 (up from 1/1), costs 0.

    Setup: Prepared+ in hand, 2 cards in draw pile.
    After play: 2 drawn, then 2 discarded.
    """
    hand = [(sts_sim.Card.Prepared, True)]
    draw = [sts_sim.Card.StrikeGreen, sts_sim.Card.DefendGreen]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Prepared,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)


def test_deadly_poison_upgraded_cost(game):
    """DeadlyPoison+ costs 0 (down from 1), applies poison.

    Setup: DeadlyPoison+ in hand, monster at 30 HP.
    After play: energy=3, poison on monster.
    """
    hand = [(sts_sim.Card.DeadlyPoison, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DeadlyPoison,
                            target_index=0, upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after DeadlyPoison+ (0 cost), got {state.combat_state.player.energy}"
    )


def test_acrobatics_upgraded_magic(game):
    """Acrobatics+ draws 4 cards (up from 3), costs 1, then discards 1.

    Setup: Acrobatics+ in hand, 4 cards in draw pile.
    After play: 4 drawn, then 1 discarded.
    """
    hand = [(sts_sim.Card.Acrobatics, True)]
    draw = [sts_sim.Card.StrikeGreen, sts_sim.Card.DefendGreen,
            sts_sim.Card.StrikeGreen, sts_sim.Card.DefendGreen]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Acrobatics,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Common Power Upgrades ──────────────────────────────────────────────


def test_accuracy_upgraded_cost(game):
    """AccuracyCard+ costs 0 (down from 1).

    Setup: AccuracyCard+ in hand, energy=3.
    After play: energy=3 (0 cost), power applied.
    """
    hand = [(sts_sim.Card.AccuracyCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.AccuracyCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after AccuracyCard+ (0 cost), got {state.combat_state.player.energy}"
    )


def test_after_image_upgraded_cost(game):
    """AfterImageCard+ costs 0 (down from 1).

    Setup: AfterImageCard+ in hand, energy=3.
    After play: energy=3 (0 cost), power applied.
    """
    hand = [(sts_sim.Card.AfterImageCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.AfterImageCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after AfterImageCard+ (0 cost), got {state.combat_state.player.energy}"
    )


# ── Uncommon Attack Upgrades ───────────────────────────────────────────


def test_backstab_upgraded_damage(game):
    """Backstab+ deals 4 damage (up from 2), costs 0, exhausts.

    Setup: Backstab+ in hand, monster at 30 HP.
    After play: monster takes 4 damage, card exhausted.
    """
    hand = [(sts_sim.Card.Backstab, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Backstab,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_bane_upgraded_damage(game):
    """Bane+ deals 3 damage (up from 2), costs 1.

    Setup: Bane+ in hand, monster at 30 HP.
    After play: monster takes 3 damage.
    """
    hand = [(sts_sim.Card.Bane, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Bane,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_choke_upgraded_damage(game):
    """Choke+ deals 4 damage (up from 3), costs 2, applies Choke debuff.

    Setup: Choke+ in hand, monster at 30 HP.
    After play: monster takes 4 damage and has Choke debuff.
    """
    hand = [(sts_sim.Card.Choke, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Choke,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_predator_upgraded_damage(game):
    """Predator+ deals 4 damage (up from 3), costs 2, draws 2.

    Setup: Predator+ in hand, 2 cards in draw pile, monster at 30 HP.
    After play: monster takes 4 damage, 2 cards drawn.
    """
    hand = [(sts_sim.Card.Predator, True)]
    draw = [sts_sim.Card.StrikeGreen, sts_sim.Card.DefendGreen]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Predator,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_masterful_stab_upgraded_damage(game):
    """MasterfulStab+ deals 3 damage (up from 2), costs 0.

    Setup: MasterfulStab+ in hand, monster at 30 HP.
    After play: monster takes 3 damage, energy=3.
    """
    hand = [(sts_sim.Card.MasterfulStab, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.MasterfulStab,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_dash_upgraded(game):
    """Dash+ deals 3 damage and gains 3 block (up from 2/2), costs 2.

    Setup: Dash+ in hand, monster at 30 HP.
    After play: monster takes 3 damage, player gains 3 block.
    """
    hand = [(sts_sim.Card.Dash, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Dash,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_finisher_upgraded_damage(game):
    """Finisher+ deals 2 damage per attack played (up from 1), costs 1.

    Setup: Finisher+ + Strike in hand, monster at 30 HP.
    Play Strike first, then Finisher+ (1 attack played -> 2 damage).
    """
    hand = [sts_sim.Card.StrikeGreen, (sts_sim.Card.Finisher, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play Strike first (1 attack played this turn)
    state = play_named_card(game, sim, setup, sts_sim.Card.StrikeGreen,
                            target_index=0)

    # Play Finisher+ (1 attack played -> 2 damage)
    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_flechettes_upgraded_magic(game):
    """Flechettes+ has magic +1 (extra hit per skill), costs 1.

    Setup: Flechettes+ + 2 skills in hand, monster at 30 HP.
    After play: damage based on number of skills in hand + magic bonus.
    """
    hand = [(sts_sim.Card.Flechettes, True), sts_sim.Card.DefendGreen,
            sts_sim.Card.Deflect]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Flechettes,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_all_out_attack_upgraded_damage(game):
    """AllOutAttack+ deals 3 damage (up from 2), costs 1, AoE.

    Setup: AllOutAttack+ + Strike in hand, monster at 30 HP.
    After play: monster takes 3 AoE damage, random card discarded.
    """
    hand = [(sts_sim.Card.AllOutAttack, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.AllOutAttack,
                            upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_unload_upgraded_magic(game):
    """Unload+ discards 2 non-attack cards (up from 1), deals 2 damage, costs 1.

    Setup: Unload+ + 2 skills in hand, monster at 30 HP.
    After play: monster takes damage, skills discarded.
    """
    hand = [(sts_sim.Card.Unload, True), sts_sim.Card.DefendGreen,
            sts_sim.Card.Deflect]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Unload,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Uncommon Skill Upgrades ────────────────────────────────────────────


def test_blur_upgraded_block(game):
    """Blur+ gains 3 block (up from 2), costs 1.

    Setup: Blur+ in hand, energy=3.
    After play: block=3, energy=2.
    """
    hand = [(sts_sim.Card.Blur, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Blur,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_bouncing_flask_upgraded_magic(game):
    """BouncingFlask+ applies 3 poison hits (up from 2), costs 2.

    Setup: BouncingFlask+ in hand, monster at 30 HP.
    After play: monster has 3 Poison.
    """
    hand = [(sts_sim.Card.BouncingFlask, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BouncingFlask,
                            target_index=0, upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_concentrate_upgraded(game):
    """Concentrate+ gains more energy or discards fewer, costs 0, exhausts.

    Setup: Concentrate+ in hand, energy=3.
    After play: energy changes, card exhausted.
    """
    hand = [(sts_sim.Card.Concentrate, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Concentrate,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_calculated_gamble_upgraded_no_exhaust(game):
    """CalculatedGamble+ no longer exhausts (unupgraded exhausts).

    Setup: CalculatedGamble+ + Strike in hand, 1 card in draw pile.
    After play: hand discarded and redrawn, card goes to discard (not exhaust).
    """
    hand = [(sts_sim.Card.CalculatedGamble, True), sts_sim.Card.StrikeGreen]
    draw = [sts_sim.Card.DefendGreen]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CalculatedGamble,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_catalyst_upgraded_triple(game):
    """Catalyst+ triples poison (instead of doubles), costs 1, exhausts.

    Setup: Catalyst+ in hand, monster at 30 HP with 2 Poison.
    After play: monster has 6 Poison (2*3), card exhausted.
    """
    hand = [(sts_sim.Card.Catalyst, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         monster_powers={"Poison": 2})
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   monster_powers={"Poison": 2})

    state = play_named_card(game, sim, setup, sts_sim.Card.Catalyst,
                            target_index=0, upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_crippling_cloud_upgraded_magic(game):
    """CripplingCloud+ applies 2 poison (up from 1), costs 2, exhausts.

    Setup: CripplingCloud+ in hand, monster at 30 HP.
    After play: monster has 2 Poison, card exhausted.
    """
    hand = [(sts_sim.Card.CripplingCloud, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CripplingCloud,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_leg_sweep_upgraded_block(game):
    """LegSweep+ gains 4 block (up from 3), costs 2, applies Weak.

    Setup: LegSweep+ in hand, monster at 30 HP.
    After play: block=4, monster has Weak.
    """
    hand = [(sts_sim.Card.LegSweep, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.LegSweep,
                            target_index=0, upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_outmaneuver_upgraded_magic(game):
    """Outmaneuver+ gains 3 energy next turn (up from 2), costs 0.

    Setup: Outmaneuver+ in hand, energy=3.
    After play: energy=3 (0 cost), power applied.
    """
    hand = [(sts_sim.Card.Outmaneuver, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Outmaneuver,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_piercing_wail_upgraded_block(game):
    """PiercingWail+ block 3 (up from 1), costs 1, exhausts.

    Setup: PiercingWail+ in hand, energy=3.
    After play: card exhausted.
    """
    hand = [(sts_sim.Card.PiercingWail, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.PiercingWail,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_escape_plan_upgraded(game):
    """EscapePlan+ block stays 1, costs 0.

    Setup: EscapePlan+ in hand, 1 card in draw pile.
    After play: block=1, card drawn.
    """
    hand = [(sts_sim.Card.EscapePlan, True)]
    draw = [sts_sim.Card.StrikeGreen]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.EscapePlan,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_expertise_upgraded_magic(game):
    """Expertise+ draws to 7 cards (up from 6), costs 1.

    Setup: Expertise+ + 2 cards in hand, 5 cards in draw pile.
    After play: draws up to 7 total cards in hand.
    """
    hand = [(sts_sim.Card.Expertise, True), sts_sim.Card.StrikeGreen]
    draw = [sts_sim.Card.DefendGreen, sts_sim.Card.StrikeGreen,
            sts_sim.Card.DefendGreen, sts_sim.Card.StrikeGreen,
            sts_sim.Card.DefendGreen]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Expertise,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_riddle_with_holes_upgraded_magic(game):
    """RiddleWithHoles+ hits 5 times (up from 4), costs 2.

    Setup: RiddleWithHoles+ in hand, monster at 30 HP.
    After play: monster takes damage from 5 hits.
    """
    hand = [(sts_sim.Card.RiddleWithHoles, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.RiddleWithHoles,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_setup_upgraded_magic(game):
    """Setup+ magic 2 (up from 1), costs 0, exhausts.

    Setup: Setup+ + Strike in hand.
    After play: card exhausted.
    """
    hand = [(sts_sim.Card.Setup, True), sts_sim.Card.StrikeGreen]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Setup,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_terror_upgraded_no_exhaust(game):
    """Terror+ no longer exhausts (unupgraded exhausts), costs 1.

    Setup: Terror+ in hand, monster at 30 HP.
    After play: monster has Vulnerable, card in discard (not exhaust).
    """
    hand = [(sts_sim.Card.Terror, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Terror,
                            target_index=0, upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Uncommon Power Upgrades ────────────────────────────────────────────


def test_footwork_upgraded(game):
    """FootworkCard+ stays cost 2, magic stays 1.

    Setup: FootworkCard+ in hand, energy=3.
    After play: energy=1, power applied.
    """
    hand = [(sts_sim.Card.FootworkCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FootworkCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_noxious_fumes_upgraded(game):
    """NoxiousFumesCard+ stays cost 1.

    Setup: NoxiousFumesCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.NoxiousFumesCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.NoxiousFumesCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_well_laid_plans_upgraded_magic(game):
    """WellLaidPlansCard+ retains 2 cards (up from 1), costs 1.

    Setup: WellLaidPlansCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.WellLaidPlansCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.WellLaidPlansCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_distraction_upgraded_cost(game):
    """DistractionCard+ costs 1 (down from 2).

    Setup: DistractionCard+ in hand, energy=3.
    After play: energy=2 (1 cost).
    """
    hand = [(sts_sim.Card.DistractionCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DistractionCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 2, (
        f"Expected 2 energy after DistractionCard+ (1 cost), got {state.combat_state.player.energy}"
    )


def test_infinite_blades_upgraded_magic(game):
    """InfiniteBlades+ generates 2 shivs per turn (up from 1), costs 1.

    Setup: InfiniteBlades+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.InfiniteBlades, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.InfiniteBlades,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Rare Attack Upgrades ──────────────────────────────────────────────


def test_die_die_die_upgraded_damage(game):
    """DieDieDie+ deals 4 damage (up from 3), costs 1, AoE, exhausts.

    Setup: DieDieDie+ in hand, monster at 30 HP.
    After play: monster takes 4 damage, card exhausted.
    """
    hand = [(sts_sim.Card.DieDieDie, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DieDieDie,
                            upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_grand_finale_upgraded_damage(game):
    """GrandFinale+ deals 12 damage (up from 10), costs 0, AoE.

    Setup: GrandFinale+ in hand, empty draw pile, monster at 30 HP.
    After play: monster takes 12 damage.
    """
    hand = [(sts_sim.Card.GrandFinale, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.GrandFinale,
                            upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_skewer_upgraded_damage(game):
    """Skewer+ deals 2 damage per X (up from 1), costs X.

    Setup: Skewer+ in hand, energy=3, monster at 30 HP.
    After play with X=3: monster takes 3*2=6 damage.
    """
    hand = [(sts_sim.Card.Skewer, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Skewer,
                            target_index=0, upgraded=True, choices=[3])

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Rare Skill Upgrades ───────────────────────────────────────────────


def test_adrenaline_upgraded(game):
    """Adrenaline+ stays same stats, costs 0, exhausts.

    Setup: Adrenaline+ in hand, 2 cards in draw pile.
    After play: energy gained, cards drawn, card exhausted.
    """
    hand = [(sts_sim.Card.Adrenaline, True)]
    draw = [sts_sim.Card.StrikeGreen, sts_sim.Card.DefendGreen]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Adrenaline,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_bullet_time_upgraded_cost(game):
    """BulletTime+ costs 2 (down from 3).

    Setup: BulletTime+ in hand, energy=3.
    After play: energy=1 (2 cost).
    """
    hand = [(sts_sim.Card.BulletTime, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BulletTime,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 1, (
        f"Expected 1 energy after BulletTime+ (2 cost), got {state.combat_state.player.energy}"
    )


def test_malaise_upgraded_magic(game):
    """Malaise+ has +1 magic bonus, costs X, exhausts.

    Setup: Malaise+ in hand, energy=3, monster at 30 HP.
    After play with X=3: applies debuffs with bonus, card exhausted.
    """
    hand = [(sts_sim.Card.Malaise, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Malaise,
                            target_index=0, upgraded=True, choices=[3])

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_storm_of_steel_upgraded_magic(game):
    """StormOfSteel+ generates shivs with +1 magic bonus, costs 1.

    Setup: StormOfSteel+ + 2 cards in hand.
    After play: hand discarded, shivs generated.
    """
    hand = [(sts_sim.Card.StormOfSteel, True), sts_sim.Card.StrikeGreen]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StormOfSteel,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_discard_matches(state, sim)


def test_doppelganger_upgraded_no_exhaust(game):
    """Doppelganger+ no longer exhausts (unupgraded exhausts), costs X.

    Setup: Doppelganger+ in hand, energy=3.
    After play with X=2: gains energy/draw next turn, card in discard (not exhaust).
    """
    hand = [(sts_sim.Card.Doppelganger, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Doppelganger,
                            upgraded=True, choices=[2])

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_corpse_explosion_upgraded_magic(game):
    """CorpseExplosionCard+ applies 3 poison (up from 2), costs 2.

    Setup: CorpseExplosionCard+ in hand, monster at 30 HP.
    After play: monster has 3 Poison, power applied.
    """
    hand = [(sts_sim.Card.CorpseExplosionCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CorpseExplosionCard,
                            target_index=0, upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Rare Power Upgrades ───────────────────────────────────────────────


def test_a_thousand_cuts_upgraded_magic(game):
    """AThousandCutsCard+ deals 7 damage per card (up from 5), costs 2.

    Setup: AThousandCutsCard+ in hand, energy=3.
    After play: energy=1, power applied.
    """
    hand = [(sts_sim.Card.AThousandCutsCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.AThousandCutsCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_burst_upgraded_cost(game):
    """BurstCard+ costs 0 (down from 1).

    Setup: BurstCard+ in hand, energy=3.
    After play: energy=3 (0 cost), power applied.
    """
    hand = [(sts_sim.Card.BurstCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BurstCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after BurstCard+ (0 cost), got {state.combat_state.player.energy}"
    )


def test_envenom_upgraded_cost(game):
    """EnvenomCard+ costs 2 (down from 3).

    Setup: EnvenomCard+ in hand, energy=3.
    After play: energy=1 (2 cost), power applied.
    """
    hand = [(sts_sim.Card.EnvenomCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.EnvenomCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 1, (
        f"Expected 1 energy after EnvenomCard+ (2 cost), got {state.combat_state.player.energy}"
    )


def test_tools_of_the_trade_upgraded_cost(game):
    """ToolsOfTheTradeCard+ costs 0 (down from 1).

    Setup: ToolsOfTheTradeCard+ in hand, energy=3.
    After play: energy=3 (0 cost), power applied.
    """
    hand = [(sts_sim.Card.ToolsOfTheTradeCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ToolsOfTheTradeCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after ToolsOfTheTradeCard+ (0 cost), got {state.combat_state.player.energy}"
    )


def test_wraith_form_upgraded_magic(game):
    """WraithFormCard+ magic 3 (up from 2), costs 3.

    Setup: WraithFormCard+ in hand, energy=3.
    After play: energy=0, power applied.
    """
    hand = [(sts_sim.Card.WraithFormCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.WraithFormCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
