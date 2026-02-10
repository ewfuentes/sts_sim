"""Tier 9: Uncommon cards — debuffs, exhaust, block, pile manipulation.

Tests verify uncommon card mechanics match between live game and simulator.
"""

import sts_sim

from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_draw_pile_matches,
    assert_discard_matches, assert_exhaust_matches,
)


# ── Disarm: apply Weak to enemy, exhaust ─────────────────────────────────

def test_disarm_weak_and_exhaust(game):
    """Disarm applies Weak to target enemy and exhausts.

    Setup: Disarm in hand, monster at 30 HP.
    After play: monster has Weak=2, Disarm exhausted, energy=2.
    """
    hand = [sts_sim.Card.Disarm]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)

    # Verify Weak on monster
    live_monster = state.combat_state.monsters[0]
    sim_monster = sim.get_monsters()[0]

    live_weak = None
    for p in live_monster.powers:
        if "eak" in p.power_id:
            live_weak = p.amount
    sim_weak = sim_monster.get_power(sts_sim.PowerType.Weak)

    assert live_weak is not None, "Weak not found on live monster"
    assert live_weak == sim_weak, f"Weak mismatch: live={live_weak}, sim={sim_weak}"


# ── SeverSoul: damage + exhaust from hand ─────────────────────────────────

def test_sever_soul_damage_and_exhaust(game):
    """SeverSoul deals damage and exhausts 1 card from hand.

    Setup: SeverSoul + Strike in hand, monster at 30 HP.
    After play: monster takes damage, Strike exhausted (only card in hand).
    """
    hand = [sts_sim.Card.SeverSoul, sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # SeverSoul's ExhaustAction uses anyNumber=true which shows a hand
    # select screen: choose(0) selects the card, then "confirm" finalizes.
    state = play_named_card(game, sim, setup, sts_sim.Card.SeverSoul,
                            target_index=0, choices=[0])
    # After card selection, BG mod requires a "confirm" to finalize the exhaust
    cmds = game.last_raw.get("available_commands", [])
    if "confirm" in cmds:
        game.send_command("confirm")
        state = game.wait_for_state(timeout=10.0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Warcry: draw cards, return 1 to top of draw pile ──────────────────────

def test_warcry_draw_and_return(game):
    """Warcry draws 2 cards and puts 1 back on top of draw pile.

    Setup: Warcry in hand, 1 Strike in draw pile.
    After play: drawn card returned to draw pile deterministically.
    """
    hand = [sts_sim.Card.Warcry]
    draw = [sts_sim.Card.StrikeRed]

    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Carnage: heavy attack, ethereal ──────────────────────────────────────

def test_carnage_damage(game):
    """Carnage deals 4 damage. Ethereal but played so normal discard.

    Setup: Carnage in hand, monster at 30 HP.
    After play: monster at 26 HP, Carnage in discard, energy=1.
    """
    hand = [sts_sim.Card.Carnage]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── BloodForBlood: expensive attack ──────────────────────────────────────

def test_blood_for_blood_damage(game):
    """BloodForBlood deals 4 damage, costs 3 energy.

    Setup: BloodForBlood in hand, 3 energy, monster at 30 HP.
    After play: monster at 26, energy=0.
    """
    hand = [sts_sim.Card.BloodForBlood]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0, target_index=0)

    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── SpotWeakness: gain Strength ──────────────────────────────────────────

def test_spot_weakness_strength(game):
    """SpotWeakness grants +1 Strength, then Strike benefits.

    Setup: SpotWeakness + Strike in hand, monster at 30 HP.
    Play SpotWeakness (targets enemy), then Strike.
    """
    hand = [sts_sim.Card.SpotWeakness, sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    # Play SpotWeakness (targets enemy)
    state = play_named_card(game, sim, setup, sts_sim.Card.SpotWeakness,
                            target_index=0)
    assert_player_matches(state, sim)

    # Play Strike — should benefit from +1 Strength
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── PowerThrough: block + Dazed to draw pile ─────────────────────────────

def test_power_through_block_and_dazed(game):
    """PowerThrough gives 3 block and adds a Dazed to draw pile.

    Setup: PowerThrough in hand, empty draw pile, monster at 30 HP.
    After play: player has 3 block, Dazed in draw pile.
    """
    hand = [sts_sim.Card.PowerThrough]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_draw_pile_matches(state, sim)
    assert_discard_matches(state, sim)


# ── SecondWind: exhaust non-attacks, gain block per card ──────────────────

def test_second_wind_exhaust_non_attacks(game):
    """SecondWind exhausts non-attack cards from hand and gains block.

    Setup: SecondWind + Defend + Strike in hand.
    After play: Defend exhausted, Strike remains in hand,
    player gains 1 block per non-attack exhausted.
    """
    hand = [sts_sim.Card.SecondWind, sts_sim.Card.DefendRed,
            sts_sim.Card.StrikeRed]

    setup = set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_named_card(game, sim, setup, sts_sim.Card.SecondWind)

    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Sentinel: block gain ─────────────────────────────────────────────────

def test_sentinel_block(game):
    """Sentinel gives 2 block, costs 1 energy.

    Setup: Sentinel in hand, 3 energy.
    After play: block=2, energy=2, Sentinel in discard.
    """
    hand = [sts_sim.Card.Sentinel]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── GhostlyArmor: block, ethereal ────────────────────────────────────────

def test_ghostly_armor_block(game):
    """GhostlyArmor gives 2 block. Ethereal but played so normal discard.

    Setup: GhostlyArmor in hand, 3 energy.
    After play: block=2, energy=2, GhostlyArmor in discard.
    """
    hand = [sts_sim.Card.GhostlyArmor]

    set_scenario(game, hand=hand, energy=3, monster_hp=30)
    sim = make_sim(hand=hand, energy=3, monster_hp=30)

    state = play_card_both(game, sim, hand_index=0)

    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)
