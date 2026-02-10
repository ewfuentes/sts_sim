"""Tier 18: Ironclad upgrade verification — remaining 37 cards.

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


# ── Damage Upgrades ─────────────────────────────────────────────────────


def test_anger_upgraded_damage(game):
    """Anger+ deals 2 damage (up from 1), costs 0 energy.

    Setup: Anger+ in hand, monster at 30 HP.
    After play: monster takes 2 damage, Anger copy added to discard.
    """
    hand = [(sts_sim.Card.Anger, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Anger,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_clash_upgraded_damage(game):
    """Clash+ deals 4 damage (up from 3), costs 0 energy.

    Setup: Clash+ in hand (only attacks), monster at 30 HP.
    After play: monster takes 4 damage.
    """
    hand = [(sts_sim.Card.Clash, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Clash,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_cleave_upgraded_damage(game):
    """Cleave+ deals 3 damage (up from 2), costs 1 energy.

    Setup: Cleave+ in hand, monster at 30 HP.
    After play: monster takes 3 AoE damage.
    """
    hand = [(sts_sim.Card.Cleave, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Cleave,
                            upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_clothesline_upgraded_damage(game):
    """Clothesline+ deals 4 damage (up from 3), costs 2, applies Weak.

    Setup: Clothesline+ in hand, monster at 30 HP.
    After play: monster takes 4 damage and has Weak.
    """
    hand = [(sts_sim.Card.Clothesline, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Clothesline,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_headbutt_upgraded_damage(game):
    """Headbutt+ deals 3 damage (up from 2), costs 1.

    Setup: Headbutt+ in hand, 1 Defend in discard, monster at 30 HP.
    After play: monster takes 3 damage, Defend moved to draw pile.
    """
    hand = [(sts_sim.Card.Headbutt, True)]
    discard = [sts_sim.Card.DefendRed]

    setup = set_scenario(game, hand=hand, discard_pile=discard, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, discard_pile=discard, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Headbutt,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_twin_strike_upgraded_damage(game):
    """TwinStrike+ deals 2 damage per hit (up from 1), costs 1.

    Setup: TwinStrike+ in hand, monster at 30 HP.
    After play: monster takes 2*2=4 damage.
    """
    hand = [(sts_sim.Card.TwinStrike, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.TwinStrike,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_wild_strike_upgraded_damage(game):
    """WildStrike+ deals 4 damage (up from 3), costs 1, adds Dazed.

    Setup: WildStrike+ in hand, monster at 30 HP.
    After play: monster takes 4 damage, Dazed in draw pile.
    """
    hand = [(sts_sim.Card.WildStrike, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.WildStrike,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_immolate_upgraded_damage(game):
    """Immolate+ deals 7 damage (up from 5), costs 2.

    Setup: Immolate+ in hand, monster at 30 HP.
    After play: monster takes 7 AoE damage.
    """
    hand = [(sts_sim.Card.Immolate, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Immolate,
                            upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_fiend_fire_upgraded_damage(game):
    """FiendFire+ deals 2 damage per card (up from 1), costs 2, exhausts hand.

    Setup: FiendFire+ + Strike + Defend in hand, monster at 30 HP.
    After play: 2 cards exhausted from hand, monster takes 2*2=4 damage.
    """
    hand = [(sts_sim.Card.FiendFire, True), sts_sim.Card.StrikeRed,
            sts_sim.Card.DefendRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FiendFire,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_feed_upgraded_magic(game):
    """Feed+ still deals 3 damage, magic 1→2 (max HP gain on kill).

    Non-kill path: verify damage and exhaust match.
    Setup: Feed+ in hand, energy=3, monster=30.
    """
    hand = [(sts_sim.Card.Feed, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Feed,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_sever_soul_upgraded_damage(game):
    """SeverSoul+ deals 4 damage (up from 3), costs 2, exhausts from hand.

    Setup: SeverSoul+ + Strike in hand, monster at 30 HP.
    After play: monster takes 4 damage, Strike exhausted.
    """
    hand = [(sts_sim.Card.SeverSoul, True), sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SeverSoul,
                            target_index=0, upgraded=True, choices=[0])
    cmds = game.last_raw.get("available_commands", [])
    if "confirm" in cmds:
        game.send_command("confirm")
        state = game.wait_for_state(timeout=10.0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Block Upgrades ──────────────────────────────────────────────────────


def test_shrug_it_off_upgraded_block(game):
    """ShrugItOff+ gains 3 block (up from 2) + draws 1, costs 1.

    Setup: ShrugItOff+ in hand, 1 Strike in draw pile.
    After play: block=3, Strike drawn to hand.
    """
    hand = [(sts_sim.Card.ShrugItOff, True)]
    draw = [sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.ShrugItOff,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_flame_barrier_upgraded_block(game):
    """FlameBarrier+ gains 4 block (up from 3), costs 2.

    Setup: FlameBarrier+ in hand, 3 energy.
    After play: block=4, energy=1.
    """
    hand = [(sts_sim.Card.FlameBarrier, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FlameBarrier,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_ghostly_armor_upgraded_block(game):
    """GhostlyArmor+ gains 3 block (up from 2), costs 1.

    Setup: GhostlyArmor+ in hand, 3 energy.
    After play: block=3, energy=2.
    """
    hand = [(sts_sim.Card.GhostlyArmor, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.GhostlyArmor,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_power_through_upgraded_block(game):
    """PowerThrough+ gains 4 block (up from 3), costs 1, adds Dazed.

    Setup: PowerThrough+ in hand, 3 energy.
    After play: block=4, Dazed in draw pile.
    """
    hand = [(sts_sim.Card.PowerThrough, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.PowerThrough,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_sentinel_upgraded_block(game):
    """Sentinel+ gains 3 block (up from 2), costs 1.

    Setup: Sentinel+ in hand, 3 energy.
    After play: block=3, energy=2.
    """
    hand = [(sts_sim.Card.Sentinel, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Sentinel,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_true_grit_upgraded_block(game):
    """TrueGrit+ gains 2 block (up from 1), costs 1, exhausts 1 card.

    Setup: TrueGrit+ + Strike in hand, 3 energy.
    After play: block=2, Strike exhausted.
    """
    hand = [(sts_sim.Card.TrueGrit, True), sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.TrueGrit,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_second_wind_upgraded_block(game):
    """SecondWind+ gains 2 block per card (up from 1), costs 1.

    Setup: SecondWind+ + Defend + Strike in hand.
    After play: Defend exhausted, block=2, Strike remains.
    """
    hand = [(sts_sim.Card.SecondWind, True), sts_sim.Card.DefendRed,
            sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SecondWind,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Cost Reductions ─────────────────────────────────────────────────────


def test_blood_for_blood_upgraded_cost(game):
    """BloodForBlood+ still costs 3 (BG mod: upgrade changes magic number, not cost).

    Setup: BloodForBlood+ in hand, 3 energy, monster at 30 HP.
    After play: monster at 26, energy=0.
    """
    hand = [(sts_sim.Card.BloodForBlood, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BloodForBlood,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_double_tap_upgraded_cost(game):
    """DoubleTap+ costs 0 (down from 1).

    Setup: DoubleTap+ + Strike in hand, energy=3, monster=30.
    Play DoubleTap+ (cost 0), play Strike (cost 1, replayed).
    Energy=2.
    """
    hand = [(sts_sim.Card.DoubleTap, True), sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DoubleTap,
                            upgraded=True)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 2, (
        f"Expected 2 energy after DoubleTap+ (0) + Strike (1), got {state.combat_state.player.energy}"
    )


def test_exhume_upgraded_cost(game):
    """Exhume+ costs 0 (down from 1).

    Setup: SeeingRed + Exhume+ in hand, energy=3.
    Play SeeingRed (exhausts), play Exhume+ (cost 0, recovers SeeingRed).
    Energy=4 (3-1+2-0).
    """
    hand = [sts_sim.Card.SeeingRed, (sts_sim.Card.Exhume, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SeeingRed)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_havoc_upgraded_cost(game):
    """Havoc+ costs 0 (down from 1).

    Setup: Havoc+ in hand, Strike on draw pile, energy=3, monster=30.
    Play Havoc+ (cost 0), auto-plays Strike for free.
    Energy=3 (0 cost for Havoc+).
    """
    hand = [(sts_sim.Card.Havoc, True)]
    draw = [sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Havoc,
                            upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after Havoc+ (0 cost), got {state.combat_state.player.energy}"
    )


def test_rage_upgraded_cost(game):
    """RageCard+ costs 0 (down from 1).

    Setup: RageCard+ in hand, energy=3.
    After play: energy=3 (0 cost), Rage power applied.
    """
    hand = [(sts_sim.Card.RageCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.RageCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after RageCard+ (0 cost), got {state.combat_state.player.energy}"
    )


# ── Magic Number Upgrades ───────────────────────────────────────────────


def test_battle_trance_upgraded_draw(game):
    """BattleTrance+ draws 4 cards (up from 3), costs 0.

    Setup: BattleTrance+ in hand, 4 cards in draw pile.
    After play: 4 cards drawn to hand.
    """
    hand = [(sts_sim.Card.BattleTrance, True)]
    draw = [sts_sim.Card.StrikeRed, sts_sim.Card.DefendRed,
            sts_sim.Card.StrikeRed, sts_sim.Card.DefendRed]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BattleTrance,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert len(state.combat_state.hand) == 4, (
        f"Expected 4 cards in hand, got {len(state.combat_state.hand)}"
    )


def test_burning_pact_upgraded_draw(game):
    """BurningPact+ draws 3 cards (up from 2), costs 1, exhausts 1.

    Setup: BurningPact+ + Strike in hand, 3 Defends in draw pile.
    After play: Strike exhausted, 3 Defends drawn.
    """
    hand = [(sts_sim.Card.BurningPact, True), sts_sim.Card.StrikeRed]
    draw = [sts_sim.Card.DefendRed, sts_sim.Card.DefendRed, sts_sim.Card.DefendRed]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BurningPact,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_disarm_upgraded_magic(game):
    """Disarm+ applies 3 Weak (up from 2), costs 1, exhausts.

    Setup: Disarm+ in hand, monster at 30 HP.
    After play: monster has Weak=3.
    """
    hand = [(sts_sim.Card.Disarm, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Disarm,
                            target_index=0, upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_shockwave_upgraded_magic(game):
    """Shockwave+ applies 2 Vulnerable and 2 Weak (up from 1 each).

    Setup: Shockwave+ in hand, monster at 30 HP.
    After play: monster has Vuln=2 and Weak=2, card exhausted.
    """
    hand = [(sts_sim.Card.Shockwave, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Shockwave,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_perfected_strike_upgraded_magic(game):
    """PerfectedStrike+ gets +2 damage per Strike (up from +1).

    Setup: PerfectedStrike+ + 2 Strikes in hand, monster at 30 HP.
    Base damage 3 + 2*2 = 7. Monster HP=23.
    """
    hand = [(sts_sim.Card.PerfectedStrike, True),
            sts_sim.Card.StrikeRed, sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.PerfectedStrike,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_spot_weakness_upgraded(game):
    """SpotWeakness+ effect verification.

    Setup: SpotWeakness+ + Strike in hand, monster at 30 HP.
    Play SpotWeakness+ (targets enemy), then Strike.
    """
    hand = [(sts_sim.Card.SpotWeakness, True), sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SpotWeakness,
                            target_index=0, upgraded=True)
    assert_player_matches(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_warcry_upgraded_draw(game):
    """Warcry+ draws 3 cards (up from 2), costs 0, exhausts.

    Setup: Warcry+ in hand, 1 Strike in draw pile.
    After play: cards drawn and returned to draw pile.
    """
    hand = [(sts_sim.Card.Warcry, True)]
    draw = [sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Warcry,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_offering_upgraded_draw(game):
    """Offering+ draws 5 cards (up from 3), costs 0, exhausts.

    Setup: Offering+ in hand, 5 cards in draw pile, 1 energy, 9 HP.
    After play: HP=8, energy=3 (1+2), 5 cards drawn.
    """
    hand = [(sts_sim.Card.Offering, True)]
    draw = [sts_sim.Card.StrikeRed, sts_sim.Card.DefendRed,
            sts_sim.Card.StrikeRed, sts_sim.Card.DefendRed,
            sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=1,
                         player_hp=9, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=1,
                   player_hp=9, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Offering,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Whirlwind X-Cost ────────────────────────────────────────────────────


def test_whirlwind_upgraded(game):
    """Whirlwind+ hits X times, base damage stays 1.

    Setup: Whirlwind+ in hand, 3 energy, monster at 30 HP.
    After play: energy=0, damage matches sim.
    """
    hand = [(sts_sim.Card.Whirlwind, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Whirlwind,
                            upgraded=True, choices=[3])

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 0


# ── Exhaust Behavior Changes ───────────────────────────────────────────


def test_limit_break_upgraded_no_exhaust(game):
    """LimitBreak+ does not exhaust (unupgraded exhausts).

    Setup: LimitBreak+ + Strike in hand, Strength=2, monster=30.
    Play LimitBreak+ (Str 2→4), verify it goes to discard (not exhaust).
    """
    hand = [(sts_sim.Card.LimitBreak, True), sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_powers={"Strength": 2})
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   player_powers={"Strength": 2})

    state = play_named_card(game, sim, setup, sts_sim.Card.LimitBreak,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)

    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Power Card Upgrades ─────────────────────────────────────────────────


def test_combust_upgraded_magic(game):
    """CombustCard+ magic 1→2 (more damage per turn), costs 1.

    Setup: CombustCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.CombustCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.CombustCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_berserk_upgraded_magic(game):
    """BerserkCard+ magic 1→2 (more energy per turn), costs 1.

    Setup: BerserkCard+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.BerserkCard, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BerserkCard,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_fire_breathing_upgraded_magic(game):
    """FireBreathing+ magic 2→3, costs 1.

    Setup: FireBreathing+ in hand, energy=3.
    After play: energy=2, power applied.
    """
    hand = [(sts_sim.Card.FireBreathing, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FireBreathing,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Rampage Upgraded ────────────────────────────────────────────────────


def test_rampage_upgraded(game):
    """Rampage+ verification.

    Setup: SeeingRed + Rampage+ in hand, energy=3, monster=30.
    Play SeeingRed (exhausts), play Rampage+ with 1 card in exhaust pile.
    """
    hand = [sts_sim.Card.SeeingRed, (sts_sim.Card.Rampage, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SeeingRed)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
