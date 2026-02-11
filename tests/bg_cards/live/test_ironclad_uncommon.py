"""Live tests for Ironclad Uncommon cards."""
import sts_sim
from tests.live.conftest import (
    set_scenario, make_sim, play_card_both, play_named_card,
    assert_monsters_match, assert_player_matches,
    assert_hand_matches, assert_discard_matches, assert_exhaust_matches,
)


# ── Uppercut ─────────────────────────────────────────────────────────────

def test_uppercut_base(game):
    """Uppercut deals 3 damage and applies VULN and WEAK."""
    hand = [sts_sim.Card.Uppercut]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_uppercut_with_strength(game):
    """Uppercut with 2 STR deals 9 damage."""
    hand = [sts_sim.Card.Uppercut]
    set_scenario(game, hand=hand, energy=3, monster_hp=20,
                 player_powers={"Strength": 2})
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   player_powers={"Strength": 2})
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_uppercut_upgraded(game):
    """Upgraded Uppercut applies 2 VULN and 1 WEAK."""
    hand = [(sts_sim.Card.Uppercut, True)]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Entrench ─────────────────────────────────────────────────────────────

def test_entrench_doubles_block(game):
    """Entrench doubles existing block and exhausts."""
    hand = [sts_sim.Card.Entrench]
    set_scenario(game, hand=hand, energy=3, player_block=4, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, player_block=4, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_entrench_block_cap(game):
    """Entrench respects 20 BLK cap."""
    hand = [sts_sim.Card.Entrench]
    set_scenario(game, hand=hand, energy=3, player_block=12, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, player_block=12, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_entrench_zero_block(game):
    """Entrench with zero block does nothing."""
    hand = [sts_sim.Card.Entrench]
    set_scenario(game, hand=hand, energy=3, player_block=0, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, player_block=0, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_entrench_upgraded_no_exhaust(game):
    """Upgraded Entrench does not exhaust."""
    hand = [(sts_sim.Card.Entrench, True)]
    set_scenario(game, hand=hand, energy=3, player_block=5, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, player_block=5, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Shockwave ────────────────────────────────────────────────────────────

def test_shockwave_base(game):
    """Shockwave applies VULN and WEAK to all enemies and exhausts."""
    hand = [sts_sim.Card.Shockwave]
    set_scenario(game, hand=hand, energy=3,
                 monsters=[{"hp": 20}, {"hp": 20}])
    sim = make_sim(hand=hand, energy=3,
                   monsters=[{"hp": 20}, {"hp": 20}])
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_shockwave_upgraded(game):
    """Upgraded Shockwave applies extra WEAK."""
    hand = [(sts_sim.Card.Shockwave, True)]
    set_scenario(game, hand=hand, energy=3,
                 monsters=[{"hp": 20}, {"hp": 20}])
    sim = make_sim(hand=hand, energy=3,
                   monsters=[{"hp": 20}, {"hp": 20}])
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Whirlwind ────────────────────────────────────────────────────────────

def test_whirlwind_spends_all_energy(game):
    """Whirlwind spends all energy and hits all enemies."""
    hand = [sts_sim.Card.Whirlwind]
    set_scenario(game, hand=hand, energy=3,
                 monsters=[{"hp": 10}, {"hp": 10}])
    sim = make_sim(hand=hand, energy=3,
                   monsters=[{"hp": 10}, {"hp": 10}])
    state = play_card_both(game, sim, hand_index=0, target_index=0,
                           choices=[3])
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_whirlwind_zero_energy(game):
    """Whirlwind with 0 energy does nothing."""
    hand = [sts_sim.Card.Whirlwind]
    set_scenario(game, hand=hand, energy=0, monster_hp=10)
    sim = make_sim(hand=hand, energy=0, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0,
                           choices=[0])
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_whirlwind_upgraded(game):
    """Upgraded Whirlwind hits X+1 times."""
    hand = [(sts_sim.Card.Whirlwind, True)]
    set_scenario(game, hand=hand, energy=2, monster_hp=10)
    sim = make_sim(hand=hand, energy=2, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0,
                           choices=[2])
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_whirlwind_with_strength(game):
    """Whirlwind with Strength scales per HIT."""
    hand = [sts_sim.Card.Whirlwind]
    set_scenario(game, hand=hand, energy=2, monster_hp=10,
                 player_powers={"Strength": 1})
    sim = make_sim(hand=hand, energy=2, monster_hp=10,
                   player_powers={"Strength": 1})
    state = play_card_both(game, sim, hand_index=0, target_index=0,
                           choices=[2])
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Battle Trance ────────────────────────────────────────────────────────

def test_battle_trance_base(game):
    """Battle Trance draws 3 cards for free."""
    hand = [sts_sim.Card.BattleTrance]
    draw = [sts_sim.Card.StrikeRed] * 5
    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


def test_battle_trance_upgraded(game):
    """Upgraded Battle Trance draws 4 cards."""
    hand = [(sts_sim.Card.BattleTrance, True)]
    draw = [sts_sim.Card.StrikeRed] * 5
    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


# ── Burning Pact ─────────────────────────────────────────────────────────

def test_burning_pact_base(game):
    """Burning Pact exhausts a card and draws 2."""
    hand = [sts_sim.Card.BurningPact, sts_sim.Card.StrikeRed]
    draw = [sts_sim.Card.DefendRed] * 5
    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, choices=[0])
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_burning_pact_upgraded(game):
    """Upgraded Burning Pact draws 3 cards."""
    hand = [(sts_sim.Card.BurningPact, True), sts_sim.Card.DefendRed]
    draw = [sts_sim.Card.StrikeRed] * 5
    set_scenario(game, hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, draw_pile=draw, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, choices=[0])
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Carnage ──────────────────────────────────────────────────────────────

def test_carnage_base(game):
    """Carnage deals 4 damage."""
    hand = [sts_sim.Card.Carnage]
    set_scenario(game, hand=hand, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, energy=3, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


def test_carnage_upgraded(game):
    """Upgraded Carnage deals 6 damage."""
    hand = [(sts_sim.Card.Carnage, True)]
    set_scenario(game, hand=hand, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, energy=3, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Blood for Blood ──────────────────────────────────────────────────────

def test_blood_for_blood_full_cost(game):
    """Blood for Blood at full cost when no HP lost."""
    hand = [sts_sim.Card.BloodForBlood]
    set_scenario(game, hand=hand, energy=4, monster_hp=10)
    sim = make_sim(hand=hand, energy=4, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Disarm ───────────────────────────────────────────────────────────────

def test_disarm_base(game):
    """Disarm applies 2 WEAK and exhausts."""
    hand = [sts_sim.Card.Disarm]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_disarm_upgraded(game):
    """Upgraded Disarm applies 3 WEAK."""
    hand = [(sts_sim.Card.Disarm, True)]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_disarm_stacks(game):
    """Disarm stacks WEAK on already-weakened enemy."""
    hand = [sts_sim.Card.Disarm]
    set_scenario(game, hand=hand, energy=3, monster_hp=20,
                 monster_powers={"Weak": 1})
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   monster_powers={"Weak": 1})
    state = play_card_both(game, sim, hand_index=0, target_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Ghostly Armor ────────────────────────────────────────────────────────

def test_ghostly_armor_base(game):
    """Ghostly Armor grants 2 block."""
    hand = [sts_sim.Card.GhostlyArmor]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_ghostly_armor_upgraded(game):
    """Upgraded Ghostly Armor grants 3 block."""
    hand = [(sts_sim.Card.GhostlyArmor, True)]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ── Inflame ──────────────────────────────────────────────────────────────

def test_inflame_base(game):
    """Inflame grants 1 STR."""
    hand = [sts_sim.Card.Inflame]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_inflame_stacks(game):
    """Inflame stacks with existing STR."""
    hand = [sts_sim.Card.Inflame]
    set_scenario(game, hand=hand, energy=3, monster_hp=20,
                 player_powers={"Strength": 2})
    sim = make_sim(hand=hand, energy=3, monster_hp=20,
                   player_powers={"Strength": 2})
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_inflame_upgraded(game):
    """Upgraded Inflame costs 1 energy."""
    hand = [(sts_sim.Card.Inflame, True)]
    set_scenario(game, hand=hand, energy=1, monster_hp=20)
    sim = make_sim(hand=hand, energy=1, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ── Power Through ────────────────────────────────────────────────────────

def test_power_through_base(game):
    """Power Through grants 3 BLK and adds DAZED to discard."""
    hand = [sts_sim.Card.PowerThrough]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_power_through_upgraded(game):
    """Upgraded Power Through grants 4 BLK."""
    hand = [(sts_sim.Card.PowerThrough, True)]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


# ── Second Wind ──────────────────────────────────────────────────────────

def test_second_wind_base(game):
    """Second Wind exhausts non-Attacks and gains block."""
    hand = [
        sts_sim.Card.SecondWind,
        sts_sim.Card.DefendRed,
        sts_sim.Card.DefendRed,
        sts_sim.Card.StrikeRed,
    ]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_second_wind_only_attacks(game):
    """Second Wind with only Attacks in hand exhausts nothing."""
    hand = [
        sts_sim.Card.SecondWind,
        sts_sim.Card.StrikeRed,
        sts_sim.Card.StrikeRed,
        sts_sim.Card.StrikeRed,
    ]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_hand_matches(state, sim)


def test_second_wind_upgraded(game):
    """Upgraded Second Wind gains 2 BLK per card exhausted."""
    hand = [
        (sts_sim.Card.SecondWind, True),
        sts_sim.Card.DefendRed,
        sts_sim.Card.DefendRed,
        sts_sim.Card.DefendRed,
        sts_sim.Card.StrikeRed,
    ]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Sentinel ─────────────────────────────────────────────────────────────

def test_sentinel_base(game):
    """Sentinel grants 2 block when played normally."""
    hand = [sts_sim.Card.Sentinel]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_discard_matches(state, sim)


def test_sentinel_energy_on_exhaust(game):
    """Sentinel grants 2 energy when exhausted by Second Wind."""
    hand = [sts_sim.Card.SecondWind, sts_sim.Card.Sentinel]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


# ── Sever Soul ───────────────────────────────────────────────────────────

def test_sever_soul_base(game):
    """Sever Soul deals 3 damage and exhausts a card."""
    hand = [sts_sim.Card.SeverSoul, sts_sim.Card.DefendRed]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, energy=3, monster_hp=10)
    state = play_named_card(game, sim, setup, sts_sim.Card.SeverSoul,
                            target_index=0, choices=[0])
    # Handle confirm for HAND_SELECT
    cmds = game.last_raw.get("available_commands", [])
    if "confirm" in cmds:
        game.send_command("confirm")
        state = game.wait_for_state(timeout=10.0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)
    assert_exhaust_matches(state, sim)


def test_sever_soul_with_strength(game):
    """Sever Soul with Strength scales per HIT."""
    hand = [sts_sim.Card.SeverSoul, sts_sim.Card.StrikeRed]
    setup = set_scenario(game, hand=hand, energy=3, monster_hp=15,
                         player_powers={"Strength": 2})
    sim = make_sim(hand=hand, energy=3, monster_hp=15,
                   player_powers={"Strength": 2})
    state = play_named_card(game, sim, setup, sts_sim.Card.SeverSoul,
                            target_index=0, choices=[0])
    cmds = game.last_raw.get("available_commands", [])
    if "confirm" in cmds:
        game.send_command("confirm")
        state = game.wait_for_state(timeout=10.0)
    assert_monsters_match(state, sim)
    assert_player_matches(state, sim)


# ── Spot Weakness ────────────────────────────────────────────────────────

def test_spot_weakness_valid(game):
    """Spot Weakness grants STR when die is on valid face (die=1 by default)."""
    hand = [sts_sim.Card.SpotWeakness]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ── Rage ─────────────────────────────────────────────────────────────────

def test_rage_base(game):
    """Rage grants block equal to number of Attacks in hand."""
    hand = [
        sts_sim.Card.RageCard,
        sts_sim.Card.StrikeRed,
        sts_sim.Card.StrikeRed,
        sts_sim.Card.DefendRed,
    ]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_rage_no_attacks(game):
    """Rage with no Attacks in hand grants 0 BLK."""
    hand = [
        sts_sim.Card.RageCard,
        sts_sim.Card.DefendRed,
        sts_sim.Card.DefendRed,
        sts_sim.Card.DefendRed,
    ]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_rage_upgraded(game):
    """Upgraded Rage costs 0 energy."""
    hand = [
        (sts_sim.Card.RageCard, True),
        sts_sim.Card.StrikeRed,
        sts_sim.Card.StrikeRed,
        sts_sim.Card.StrikeRed,
    ]
    set_scenario(game, hand=hand, energy=0, monster_hp=20)
    sim = make_sim(hand=hand, energy=0, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ── Combust ──────────────────────────────────────────────────────────────

def test_combust_base(game):
    """Combust power card is played for 1 energy."""
    hand = [sts_sim.Card.CombustCard]
    set_scenario(game, hand=hand, energy=3, monster_hp=10)
    sim = make_sim(hand=hand, energy=3, monster_hp=10)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ── Dark Embrace ─────────────────────────────────────────────────────────

def test_dark_embrace_upgraded(game):
    """Upgraded Dark Embrace costs 1 energy."""
    hand = [(sts_sim.Card.DarkEmbrace, True)]
    set_scenario(game, hand=hand, energy=1, monster_hp=20)
    sim = make_sim(hand=hand, energy=1, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ── Evolve ───────────────────────────────────────────────────────────────

def test_evolve_upgraded(game):
    """Upgraded Evolve costs 0 energy."""
    hand = [(sts_sim.Card.Evolve, True)]
    set_scenario(game, hand=hand, energy=0, monster_hp=20)
    sim = make_sim(hand=hand, energy=0, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ── Feel No Pain ─────────────────────────────────────────────────────────

def test_feel_no_pain_upgraded(game):
    """Upgraded Feel No Pain costs 0 energy."""
    hand = [(sts_sim.Card.FeelNoPain, True)]
    set_scenario(game, hand=hand, energy=0, monster_hp=20)
    sim = make_sim(hand=hand, energy=0, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ── Fire Breathing ───────────────────────────────────────────────────────

def test_fire_breathing_base(game):
    """Fire Breathing costs 1 energy to play."""
    hand = [sts_sim.Card.FireBreathing]
    set_scenario(game, hand=hand, energy=3, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


# ── Rupture ──────────────────────────────────────────────────────────────

def test_rupture_base(game):
    """Rupture grants 1 STR and costs 1 HP."""
    hand = [sts_sim.Card.Rupture]
    set_scenario(game, hand=hand, energy=3, player_hp=9, monster_hp=20)
    sim = make_sim(hand=hand, energy=3, player_hp=9, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_rupture_stacks(game):
    """Rupture stacks with existing STR."""
    hand = [sts_sim.Card.Rupture]
    set_scenario(game, hand=hand, energy=3, player_hp=9, monster_hp=20,
                 player_powers={"Strength": 2})
    sim = make_sim(hand=hand, energy=3, player_hp=9, monster_hp=20,
                   player_powers={"Strength": 2})
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)


def test_rupture_upgraded(game):
    """Upgraded Rupture costs 0 energy."""
    hand = [(sts_sim.Card.Rupture, True)]
    set_scenario(game, hand=hand, energy=0, player_hp=9, monster_hp=20)
    sim = make_sim(hand=hand, energy=0, player_hp=9, monster_hp=20)
    state = play_card_both(game, sim, hand_index=0)
    assert_player_matches(state, sim)
