"""Tier 14: Upgraded card verification.

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


def test_strike_upgraded_damage(game):
    """Strike+ deals 2 damage (up from 1).

    Setup: Strike+ in hand, monster at 30 HP.
    After play: monster HP=28, energy=2.
    """
    hand = [(sts_sim.Card.StrikeRed, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.StrikeRed,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_bludgeon_upgraded_damage(game):
    """Bludgeon+ deals 10 damage (up from 7).

    Setup: Bludgeon+ in hand, monster at 30 HP, energy=3.
    After play: monster HP=20, energy=0.
    """
    hand = [(sts_sim.Card.Bludgeon, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Bludgeon,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_carnage_upgraded_damage(game):
    """Carnage+ deals 6 damage (up from 4).

    Setup: Carnage+ in hand, monster at 30 HP, energy=3.
    After play: monster HP=24, energy=1.
    """
    hand = [(sts_sim.Card.Carnage, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Carnage,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Block Upgrades ──────────────────────────────────────────────────────


def test_defend_upgraded_block(game):
    """Defend+ gains 2 block (up from 1).

    Setup: Defend+ in hand, energy=3.
    After play: player block=2, energy=2.
    """
    hand = [(sts_sim.Card.DefendRed, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DefendRed,
                            upgraded=True)

    assert_player_matches(state, sim)


def test_impervious_upgraded_block(game):
    """Impervious+ gains 8 block (up from 6).

    Setup: Impervious+ in hand, energy=3.
    After play: player block=8, energy=1.
    """
    hand = [(sts_sim.Card.Impervious, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Impervious,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Magic Upgrades ──────────────────────────────────────────────────────


def test_heavy_blade_upgraded_magic(game):
    """Heavy Blade+ uses 5x Strength multiplier (up from 3x).

    Setup: Heavy Blade+ in hand, player Str=1, monster at 30 HP.
    Damage = base 3 + 5*1 = 8. Monster HP=22.
    """
    hand = [(sts_sim.Card.HeavyBlade, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30,
                         player_powers={"Strength": 1})
    sim = make_sim(hand=hand, energy=3, monster_hp=30,
                   player_powers={"Strength": 1})

    state = play_named_card(game, sim, setup, sts_sim.Card.HeavyBlade,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_pommel_strike_upgraded_draw(game):
    """Pommel Strike+ draws 2 cards (up from 1).

    Setup: Pommel Strike+ in hand, 2 cards in draw pile, monster at 30 HP.
    After play: 2 damage to monster, 2 cards drawn to hand.
    """
    hand = [(sts_sim.Card.PommelStrike, True)]
    draw = [sts_sim.Card.StrikeRed, sts_sim.Card.DefendRed]

    setup = set_scenario(game, hand=hand, draw_pile=draw, energy=3,
                         monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.PommelStrike,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)


def test_uppercut_upgraded_debuffs(game):
    """Uppercut+ applies 2 Vulnerable and 2 Weak (up from 1 each).

    Setup: Uppercut+ in hand, monster at 30 HP.
    After play: 3 damage, 2 Vuln + 2 Weak on monster.
    """
    hand = [(sts_sim.Card.Uppercut, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Uppercut,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Cost Reduction ──────────────────────────────────────────────────────


def test_body_slam_upgraded_cost(game):
    """Body Slam+ costs 0 energy (down from 1).

    Setup: Body Slam+ in hand, player block=3, monster at 30 HP, energy=3.
    After play: 3 damage (= block), energy=3 (0 cost).
    """
    hand = [(sts_sim.Card.BodySlam, True)]

    setup = set_scenario(game, hand=hand, energy=3, player_block=3,
                         monster_hp=30)
    sim = make_sim(hand=hand, energy=3, player_block=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.BodySlam,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_corruption_upgraded_cost(game):
    """Corruption+ costs 2 energy (down from 3).

    Setup: Corruption+ + DefendRed, energy=3, monster=30.
    Play Corruption+ (cost 2, energy->1). Play DefendRed (free, exhausts).
    """
    hand = [(sts_sim.Card.Corruption, True), sts_sim.Card.DefendRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play Corruption+ (cost 2)
    state = play_named_card(game, sim, setup, sts_sim.Card.Corruption,
                            upgraded=True)

    # Play DefendRed (free due to Corruption, exhausts)
    state = play_card_both(game, sim, hand_index=0, target_index=None)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert state.combat_state.player.energy == 1, (
        f"Expected 1 energy, got {state.combat_state.player.energy}"
    )


def test_seeing_red_upgraded_cost(game):
    """Seeing Red+ costs 0 energy (down from 1).

    Setup: Seeing Red+ in hand, energy=3.
    After play: 3 - 0 + 2 = 5 energy, card exhausted.
    """
    hand = [(sts_sim.Card.SeeingRed, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SeeingRed,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert state.combat_state.player.energy == 5, (
        f"Expected 5 energy after Seeing Red+, got {state.combat_state.player.energy}"
    )


# ── Exhaust Removal ─────────────────────────────────────────────────────


def test_flex_upgraded_no_exhaust(game):
    """Flex+ does not exhaust (unupgraded exhausts).

    Setup: Flex+ in hand, energy=3, monster=30.
    After play: Flex+ in discard (not exhaust), +1 Str.
    """
    hand = [(sts_sim.Card.Flex, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Flex,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_entrench_upgraded_no_exhaust(game):
    """Entrench+ does not exhaust (unupgraded exhausts).

    Setup: Entrench+ in hand, player block=2, energy=3, monster=30.
    After play: block doubles to 4, Entrench+ in discard (not exhaust).
    """
    hand = [(sts_sim.Card.Entrench, True)]

    setup = set_scenario(game, hand=hand, energy=3, player_block=2,
                         monster_hp=30)
    sim = make_sim(hand=hand, energy=3, player_block=2, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Entrench,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert state.combat_state.player.block == 4, (
        f"Expected 4 block after Entrench+, got {state.combat_state.player.block}"
    )


# ── Combined Upgrades ───────────────────────────────────────────────────


def test_iron_wave_upgraded_spear(game):
    """Iron Wave+ Spear choice: 2 damage, 1 block.

    BG mod Iron Wave+ presents a choice: Spear (2dmg/1blk) or Shield (1dmg/2blk).
    This test picks choice 0 (Spear).
    Sim models the Spear side, so sim and game should match.
    """
    hand = [(sts_sim.Card.IronWave, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.IronWave,
                            target_index=0, upgraded=True, choices=[0])

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    # Verify concrete values: Spear = 2 damage, 1 block
    assert state.combat_state.player.block == 1
    lm = [m for m in state.combat_state.monsters if not m.is_gone][0]
    assert lm.current_hp == 28  # 30 - 2


def test_iron_wave_upgraded_shield(game):
    """Iron Wave+ Shield choice: 1 damage, 2 block.

    BG mod Iron Wave+ presents a choice: Spear (2dmg/1blk) or Shield (1dmg/2blk).
    This test picks choice 1 (Shield) and verifies sim matches game.
    """
    from tests.live.conftest import _wait_for_play_resolution

    hand = [(sts_sim.Card.IronWave, True)]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play card in game, picking Shield (choice 1)
    game.play_card(0, target_index=0)
    state = _wait_for_play_resolution(game, choices=[1])

    # Play card in sim with choice=1 (Shield)
    sim.play_card(0, 0, 1)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_bash_upgraded_damage(game):
    """Bash+ deals 4 damage (up from 2) and applies 1 Vulnerable.

    Setup: Bash+ in hand, monster at 30 HP, energy=3.
    After play: monster HP=26, 1 Vuln on monster.
    """
    hand = [(sts_sim.Card.Bash, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Bash,
                            target_index=0, upgraded=True)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Power Card Upgrades — Cost Reductions ────────────────────────────────


def test_inflame_upgraded_cost(game):
    """Inflame+ costs 1 energy (down from 2), still grants 1 Strength.

    Setup: Inflame+ + Strike in hand, energy=3, monster=30.
    Play Inflame+ (cost 1, energy->2). Play Strike (1+1 Str = 2 damage).
    """
    hand = [(sts_sim.Card.Inflame, True), sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play Inflame+ (cost 1)
    state = play_named_card(game, sim, setup, sts_sim.Card.Inflame,
                            upgraded=True)
    assert_player_matches(state, sim)

    # Play Strike — should benefit from +1 Strength
    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_metallicize_upgraded_cost(game):
    """Metallicize+ costs 0 energy (down from 1).

    Setup: Metallicize+ in hand, energy=3, monster=30.
    After play: energy=3 (0 cost).
    """
    hand = [(sts_sim.Card.Metallicize, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Metallicize,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after Metallicize+, got {state.combat_state.player.energy}"
    )


def test_feel_no_pain_upgraded_cost(game):
    """FeelNoPain+ costs 0 energy (down from 1).

    Setup: FeelNoPain+ in hand, energy=3, monster=30.
    After play: energy=3 (0 cost).
    """
    hand = [(sts_sim.Card.FeelNoPain, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.FeelNoPain,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after FeelNoPain+, got {state.combat_state.player.energy}"
    )


def test_dark_embrace_upgraded_cost(game):
    """DarkEmbrace+ costs 1 energy (down from 2).

    Setup: DarkEmbrace+ in hand, energy=3, monster=30.
    After play: energy=2 (1 cost).
    """
    hand = [(sts_sim.Card.DarkEmbrace, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DarkEmbrace,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 2, (
        f"Expected 2 energy after DarkEmbrace+, got {state.combat_state.player.energy}"
    )


def test_evolve_upgraded_cost(game):
    """Evolve+ costs 0 energy (down from 1).

    Setup: Evolve+ in hand, energy=3, monster=30.
    After play: energy=3 (0 cost).
    """
    hand = [(sts_sim.Card.Evolve, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Evolve,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after Evolve+, got {state.combat_state.player.energy}"
    )


def test_rupture_upgraded_cost(game):
    """Rupture+ costs 0 energy (down from 1).

    Setup: Rupture+ in hand, energy=3, monster=30.
    After play: energy=3 (0 cost).
    """
    hand = [(sts_sim.Card.Rupture, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Rupture,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 3, (
        f"Expected 3 energy after Rupture+, got {state.combat_state.player.energy}"
    )


def test_barricade_upgraded_cost(game):
    """Barricade+ costs 1 energy (down from 2).

    Setup: Barricade+ in hand, energy=3, monster=30.
    After play: energy=2 (1 cost).
    """
    hand = [(sts_sim.Card.Barricade, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.Barricade,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 2, (
        f"Expected 2 energy after Barricade+, got {state.combat_state.player.energy}"
    )


def test_demon_form_upgraded_cost(game):
    """DemonForm+ costs 2 energy (down from 3).

    Setup: DemonForm+ in hand, energy=3, monster=30.
    After play: energy=1 (2 cost).
    """
    hand = [(sts_sim.Card.DemonForm, True)]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.DemonForm,
                            upgraded=True)

    assert_player_matches(state, sim)
    assert state.combat_state.player.energy == 1, (
        f"Expected 1 energy after DemonForm+, got {state.combat_state.player.energy}"
    )


# ── Power Card Upgrades — Magic Number Increases ─────────────────────────


def test_juggernaut_upgraded_magic(game):
    """Juggernaut+ deals 2 damage per block gain (up from 1).

    Setup: Juggernaut+ + DefendRed, energy=3, monster=30.
    Play Juggernaut+ (cost 2), play DefendRed (cost 1, block=1).
    Juggernaut triggers: 2 damage to monster. Monster HP=28.
    """
    hand = [(sts_sim.Card.Juggernaut, True), sts_sim.Card.DefendRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play Juggernaut+ (power, cost 2)
    state = play_named_card(game, sim, setup, sts_sim.Card.Juggernaut,
                            upgraded=True)

    # Play DefendRed (cost 1, block=1, triggers Juggernaut for 2 damage)
    state = play_card_both(game, sim, hand_index=0, target_index=None)

    assert_player_matches(state, sim)
    assert_monsters_match(state, sim)
