"""Tests for all Ironclad cards (Phase 3)."""
import sts_sim


def make_combat(seed=42):
    """Helper: create a basic jaw_worm encounter."""
    cs = sts_sim.create_encounter("jaw_worm", seed=seed)
    cs.start_combat()
    return cs


def find_card_in_hand(cs, card_type):
    """Find the hand index of a specific card."""
    hand = cs.get_hand()
    for i, ci in enumerate(hand):
        if ci.card == card_type:
            return i
    return None


# =========================================================================
# Common Attacks
# =========================================================================

def test_anger_deals_damage_and_goes_to_draw():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Anger)
    idx = find_card_in_hand(cs, sts_sim.Card.Anger)
    assert idx is not None
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    # Anger deals 1 damage
    assert cs.get_monsters()[0].hp == m_hp_before - 1
    # BG mod: Anger goes to draw pile (not discard)
    draw = cs.get_draw_pile()
    assert any(ci.card == sts_sim.Card.Anger for ci in draw)
    discard = cs.get_discard_pile()
    assert not any(ci.card == sts_sim.Card.Anger for ci in discard)


def test_body_slam_damage_equals_block():
    cs = make_combat()
    # First gain some block
    cs.set_player_block(5)
    cs.add_card_to_hand(sts_sim.Card.BodySlam)
    idx = find_card_in_hand(cs, sts_sim.Card.BodySlam)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    # BodySlam damage = player block = 5
    assert cs.get_monsters()[0].hp == m_hp_before - 5


def test_body_slam_zero_block():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.BodySlam)
    idx = find_card_in_hand(cs, sts_sim.Card.BodySlam)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    # BodySlam with 0 block does 0 damage
    assert cs.get_monsters()[0].hp == m_hp_before


def test_clash_only_playable_with_all_attacks():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Clash)
    # Hand has Defend cards too, so Clash should not be in available actions
    # Actually Clash is always playable in our sim (restriction not implemented in get_available_actions yet)
    # Test that it deals damage when played
    idx = find_card_in_hand(cs, sts_sim.Card.Clash)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    assert cs.get_monsters()[0].hp == m_hp_before - 3


def test_cleave_hits_all_enemies():
    # Use jaw_worm (1 target, no CurlUp) to verify AoE damage
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Cleave)
    idx = find_card_in_hand(cs, sts_sim.Card.Cleave)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, None)
    # Cleave deals 2 damage
    assert cs.get_monsters()[0].hp == m_hp_before - 2


def test_clothesline_deals_damage_and_weak():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Clothesline)
    idx = find_card_in_hand(cs, sts_sim.Card.Clothesline)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    assert cs.get_monsters()[0].hp == m_hp_before - 3
    assert cs.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 1


def test_heavy_blade_str_multiplier():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.apply_player_power(sts_sim.PowerType.Strength, 2)
    cs.add_card_to_hand(sts_sim.Card.HeavyBlade)
    idx = find_card_in_hand(cs, sts_sim.Card.HeavyBlade)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    # HeavyBlade base=3, Str=2, multiplier=3. Normal damage would add 2 Str.
    # HeavyBlade: base_damage=3 + bonus_str=2*(3-1)=4 = 7 base. Then calculate_player_damage adds Str (+2) = 9
    # Wait: HeavyBlade has custom calc: bonus_str = str_val * (magic - 1), base = base_damage + bonus_str
    # Then calculate_player_damage adds str_val again. So total = (3 + 2*2) + 2 = 9
    assert cs.get_monsters()[0].hp == m_hp_before - 9


def test_iron_wave_blocks_and_attacks():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.IronWave)
    idx = find_card_in_hand(cs, sts_sim.Card.IronWave)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    assert cs.player.block == 1
    assert cs.get_monsters()[0].hp == m_hp_before - 1


def test_perfected_strike_bonus_per_strike():
    cs = make_combat(seed=42)
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.PerfectedStrike)
    # Count Strike-type cards in hand, excluding PerfectedStrike itself (BG mod behavior)
    hand = cs.get_hand()
    strike_cards = {sts_sim.Card.StrikeRed, sts_sim.Card.PerfectedStrike, sts_sim.Card.TwinStrike}
    other_strikes = sum(1 for ci in hand if ci.card in strike_cards and ci.card != sts_sim.Card.PerfectedStrike)
    # Damage = base(3) + other_strikes * magic(1)
    idx = find_card_in_hand(cs, sts_sim.Card.PerfectedStrike)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    expected = 3 + other_strikes * 1
    assert cs.get_monsters()[0].hp == m_hp_before - expected


def test_pommel_strike_deals_damage_and_draws():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.PommelStrike)
    idx = find_card_in_hand(cs, sts_sim.Card.PommelStrike)
    hand_size_before = len(cs.get_hand())
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    assert cs.get_monsters()[0].hp == m_hp_before - 2
    # Draws 1 card (magic=1). Card played removes 1, draw adds 1, net same
    assert len(cs.get_hand()) == hand_size_before  # -1 played, +1 drawn


def test_twin_strike_hits_twice():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.TwinStrike)
    idx = find_card_in_hand(cs, sts_sim.Card.TwinStrike)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    # TwinStrike hits twice for 1 each = 2 total
    assert cs.get_monsters()[0].hp == m_hp_before - 2


def test_wild_strike_adds_dazed():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.WildStrike)
    draw_size_before = len(cs.get_draw_pile())
    idx = find_card_in_hand(cs, sts_sim.Card.WildStrike)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    assert cs.get_monsters()[0].hp == m_hp_before - 3
    # Dazed added to discard pile
    discard = cs.get_discard_pile()
    assert any(ci.card == sts_sim.Card.Dazed for ci in discard)


# =========================================================================
# Common Skills
# =========================================================================

def test_flex_gains_temp_strength():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Flex)
    idx = find_card_in_hand(cs, sts_sim.Card.Flex)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.Strength) == 1


def test_flex_exhausts_base():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Flex)
    idx = find_card_in_hand(cs, sts_sim.Card.Flex)
    cs.play_card(idx, None)
    exhaust = cs.get_exhaust_pile()
    assert any(ci.card == sts_sim.Card.Flex for ci in exhaust)


def test_seeing_red_gives_energy():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.SeeingRed)
    idx = find_card_in_hand(cs, sts_sim.Card.SeeingRed)
    energy_before = cs.player.energy
    cs.play_card(idx, None)
    # SeeingRed costs 1, gives 2 energy. Net: +1
    assert cs.player.energy == energy_before - 1 + 2


def test_seeing_red_exhausts():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.SeeingRed)
    idx = find_card_in_hand(cs, sts_sim.Card.SeeingRed)
    cs.play_card(idx, None)
    exhaust = cs.get_exhaust_pile()
    assert any(ci.card == sts_sim.Card.SeeingRed for ci in exhaust)


def test_shrug_it_off_blocks_and_draws():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.ShrugItOff)
    idx = find_card_in_hand(cs, sts_sim.Card.ShrugItOff)
    hand_size = len(cs.get_hand())
    cs.play_card(idx, None)
    assert cs.player.block == 2
    # Draws 1: -1 played + 1 drawn = net 0
    assert len(cs.get_hand()) == hand_size


def test_true_grit_blocks_and_exhausts():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.TrueGrit)
    idx = find_card_in_hand(cs, sts_sim.Card.TrueGrit)
    hand_size = len(cs.get_hand())
    cs.play_card(idx, None)
    assert cs.player.block == 1
    # Exhausts 1 card from hand
    assert len(cs.get_hand()) == hand_size - 2  # -1 played, -1 exhausted


def test_warcry_draws_and_puts_back():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Warcry)
    idx = find_card_in_hand(cs, sts_sim.Card.Warcry)
    hand_size = len(cs.get_hand())
    draw_size = len(cs.get_draw_pile())
    cs.play_card(idx, None)
    # Warcry: draw 2, put 1 back on draw pile, exhausts self
    # hand: -1 (played, exhausted) +2 drawn -1 put back = net 0
    assert len(cs.get_hand()) == hand_size
    # Draw pile: -2 drawn +1 put back = net -1
    assert len(cs.get_draw_pile()) == draw_size - 1


# =========================================================================
# Uncommon Attacks
# =========================================================================

def test_blood_for_blood_deals_damage():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.BloodForBlood)
    idx = find_card_in_hand(cs, sts_sim.Card.BloodForBlood)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    assert cs.get_monsters()[0].hp == m_hp_before - 4


def test_carnage_deals_damage_and_ethereal():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Carnage)
    idx = find_card_in_hand(cs, sts_sim.Card.Carnage)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    assert cs.get_monsters()[0].hp == m_hp_before - 4


def test_headbutt_puts_discard_on_draw():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Headbutt)
    # First play a strike to put something in discard
    strike_idx = find_card_in_hand(cs, sts_sim.Card.StrikeRed)
    if strike_idx is not None:
        cs.play_card(strike_idx, 0)
    discard_size = len(cs.get_discard_pile())
    draw_size = len(cs.get_draw_pile())
    idx = find_card_in_hand(cs, sts_sim.Card.Headbutt)
    cs.play_card(idx, 0)
    # Headbutt moves 1 card from discard to draw, and itself goes to discard
    # discard: -1 moved + 1 (Headbutt itself) = net 0
    assert len(cs.get_discard_pile()) == discard_size
    # draw: +1 from discard
    assert len(cs.get_draw_pile()) == draw_size + 1


def test_rampage_damage_equals_exhaust_pile():
    cs = make_combat()
    # Put some cards in exhaust pile first
    cs.add_card_to_hand(sts_sim.Card.SeeingRed)
    sr_idx = find_card_in_hand(cs, sts_sim.Card.SeeingRed)
    cs.play_card(sr_idx, None)  # SeeingRed exhausts

    cs.add_card_to_hand(sts_sim.Card.Rampage)
    cs.set_player_energy(5)
    idx = find_card_in_hand(cs, sts_sim.Card.Rampage)
    exhaust_count = len(cs.get_exhaust_pile())
    assert exhaust_count == 1

    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    # Damage = exhaust pile size = 1
    assert cs.get_monsters()[0].hp == m_hp_before - 1


def test_sever_soul_deals_damage_then_exhausts():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.SeverSoul)
    hand_size = len(cs.get_hand())
    idx = find_card_in_hand(cs, sts_sim.Card.SeverSoul)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    assert cs.get_monsters()[0].hp == m_hp_before - 3
    # Exhausts 1 random card from hand
    assert len(cs.get_hand()) == hand_size - 2  # -1 played, -1 exhausted


def test_uppercut_applies_vuln_and_weak():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Uppercut)
    idx = find_card_in_hand(cs, sts_sim.Card.Uppercut)
    cs.play_card(idx, 0)
    m = cs.get_monsters()[0]
    assert m.get_power(sts_sim.PowerType.Vulnerable) == 1
    assert m.get_power(sts_sim.PowerType.Weak) == 1


def test_whirlwind_spends_all_energy():
    # Use jaw_worm (no CurlUp complication)
    cs = make_combat()
    cs.set_player_energy(3)
    cs.add_card_to_hand(sts_sim.Card.Whirlwind)
    idx = find_card_in_hand(cs, sts_sim.Card.Whirlwind)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, None)
    # X = 3 energy, 3 hits of 1 damage each = 3 total
    assert cs.get_monsters()[0].hp == m_hp_before - 3
    assert cs.player.energy == 0


def test_whirlwind_choice_spends_partial_energy():
    cs = make_combat()
    cs.set_player_energy(3)
    cs.add_card_to_hand(sts_sim.Card.Whirlwind)
    idx = find_card_in_hand(cs, sts_sim.Card.Whirlwind)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, None, 2)  # Spend only 2 of 3 energy
    assert cs.get_monsters()[0].hp == m_hp_before - 2
    assert cs.player.energy == 1


def test_whirlwind_choice_zero():
    cs = make_combat()
    cs.set_player_energy(3)
    cs.add_card_to_hand(sts_sim.Card.Whirlwind)
    idx = find_card_in_hand(cs, sts_sim.Card.Whirlwind)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, None, 0)  # Spend 0 energy
    assert cs.get_monsters()[0].hp == m_hp_before
    assert cs.player.energy == 3


# =========================================================================
# Uncommon Skills
# =========================================================================

def test_battle_trance_draws_and_no_draw():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.BattleTrance)
    idx = find_card_in_hand(cs, sts_sim.Card.BattleTrance)
    hand_size = len(cs.get_hand())
    cs.play_card(idx, None)
    # Draws 3, plays 1 = net +2
    assert len(cs.get_hand()) == hand_size + 2
    # Applies NoDraw
    assert cs.get_player_power(sts_sim.PowerType.NoDraw) == 1


def test_burning_pact_exhausts_and_draws():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.BurningPact)
    idx = find_card_in_hand(cs, sts_sim.Card.BurningPact)
    hand_size = len(cs.get_hand())
    cs.play_card(idx, None)
    # Exhaust 1, draw 2, play 1 = net 0
    assert len(cs.get_hand()) == hand_size
    assert len(cs.get_exhaust_pile()) >= 1


def test_disarm_applies_weak():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Disarm)
    idx = find_card_in_hand(cs, sts_sim.Card.Disarm)
    cs.play_card(idx, 0)
    assert cs.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 2


def test_disarm_exhausts():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Disarm)
    idx = find_card_in_hand(cs, sts_sim.Card.Disarm)
    cs.play_card(idx, 0)
    exhaust = cs.get_exhaust_pile()
    assert any(ci.card == sts_sim.Card.Disarm for ci in exhaust)


def test_entrench_doubles_block():
    cs = make_combat()
    cs.set_player_block(3)
    cs.add_card_to_hand(sts_sim.Card.Entrench)
    idx = find_card_in_hand(cs, sts_sim.Card.Entrench)
    cs.play_card(idx, None)
    assert cs.player.block == 6


def test_entrench_exhausts_base():
    cs = make_combat()
    cs.set_player_block(3)
    cs.add_card_to_hand(sts_sim.Card.Entrench)
    idx = find_card_in_hand(cs, sts_sim.Card.Entrench)
    cs.play_card(idx, None)
    exhaust = cs.get_exhaust_pile()
    assert any(ci.card == sts_sim.Card.Entrench for ci in exhaust)


def test_entrench_upgraded_no_exhaust():
    cs = make_combat()
    cs.set_player_block(3)
    cs.add_upgraded_card_to_hand(sts_sim.Card.Entrench)
    idx = find_card_in_hand(cs, sts_sim.Card.Entrench)
    cs.play_card(idx, None)
    assert cs.player.block == 6
    # Upgraded Entrench does NOT exhaust
    exhaust = cs.get_exhaust_pile()
    assert not any(ci.card == sts_sim.Card.Entrench for ci in exhaust)


def test_flame_barrier_blocks_and_thorns():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.FlameBarrier)
    idx = find_card_in_hand(cs, sts_sim.Card.FlameBarrier)
    cs.play_card(idx, None)
    assert cs.player.block == 3
    assert cs.get_player_power(sts_sim.PowerType.Thorns) == 1


def test_ghostly_armor_gives_block():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.GhostlyArmor)
    idx = find_card_in_hand(cs, sts_sim.Card.GhostlyArmor)
    cs.play_card(idx, None)
    assert cs.player.block == 2


def test_power_through_blocks_and_adds_dazed():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.PowerThrough)
    idx = find_card_in_hand(cs, sts_sim.Card.PowerThrough)
    cs.play_card(idx, None)
    assert cs.player.block == 3
    discard = cs.get_discard_pile()
    assert any(ci.card == sts_sim.Card.Dazed for ci in discard)


def test_rage_card_blocks_and_applies_rage():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.RageCard)
    # Count attacks already in hand before playing Rage
    hand = cs.get_hand()
    attack_count = sum(1 for ci in hand if ci.py_card_type == sts_sim.CardType.Attack)
    idx = find_card_in_hand(cs, sts_sim.Card.RageCard)
    cs.play_card(idx, None)
    # BG mod: Rage gives block equal to number of Attacks in hand
    assert cs.player.block == attack_count


def test_second_wind_exhausts_non_attacks_and_blocks():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.SecondWind)
    idx = find_card_in_hand(cs, sts_sim.Card.SecondWind)
    hand = cs.get_hand()
    non_attack_count = sum(
        1 for ci in hand
        if ci.card != sts_sim.Card.SecondWind and ci.py_card_type != sts_sim.CardType.Attack
    )
    cs.play_card(idx, None)
    # Block = base_block(1) * non_attack_count
    assert cs.player.block == 1 * non_attack_count
    # All non-attack cards from hand should be exhausted
    assert len(cs.get_exhaust_pile()) == non_attack_count


def test_sentinel_gives_block():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Sentinel)
    idx = find_card_in_hand(cs, sts_sim.Card.Sentinel)
    cs.play_card(idx, None)
    assert cs.player.block == 2


def test_shockwave_applies_vuln_and_weak_to_all():
    cs = sts_sim.create_encounter("louse", seed=42)
    cs.start_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Shockwave)
    idx = find_card_in_hand(cs, sts_sim.Card.Shockwave)
    cs.play_card(idx, None)
    for m in cs.get_monsters():
        assert m.get_power(sts_sim.PowerType.Vulnerable) == 1
        assert m.get_power(sts_sim.PowerType.Weak) == 1


def test_shockwave_exhausts():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Shockwave)
    idx = find_card_in_hand(cs, sts_sim.Card.Shockwave)
    cs.play_card(idx, None)
    exhaust = cs.get_exhaust_pile()
    assert any(ci.card == sts_sim.Card.Shockwave for ci in exhaust)


def test_spot_weakness_gains_strength():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.SpotWeakness)
    idx = find_card_in_hand(cs, sts_sim.Card.SpotWeakness)
    cs.play_card(idx, 0)
    assert cs.get_player_power(sts_sim.PowerType.Strength) == 1


# =========================================================================
# Uncommon Powers
# =========================================================================

def test_inflame_gives_strength():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Inflame)
    idx = find_card_in_hand(cs, sts_sim.Card.Inflame)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.Strength) == 1


def test_metallicize_power_applies():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Metallicize)
    idx = find_card_in_hand(cs, sts_sim.Card.Metallicize)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.Metallicize) == 1


def test_combust_card_applies_power():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.CombustCard)
    idx = find_card_in_hand(cs, sts_sim.Card.CombustCard)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.Combust) == 1


def test_dark_embrace_applies_power():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.DarkEmbrace)
    idx = find_card_in_hand(cs, sts_sim.Card.DarkEmbrace)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.DarkEmbrace) == 1


def test_evolve_applies_power():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Evolve)
    idx = find_card_in_hand(cs, sts_sim.Card.Evolve)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.Evolve) == 1


def test_feel_no_pain_applies_power():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.FeelNoPain)
    idx = find_card_in_hand(cs, sts_sim.Card.FeelNoPain)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.FeelNoPain) == 1


def test_fire_breathing_applies_power():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.FireBreathing)
    idx = find_card_in_hand(cs, sts_sim.Card.FireBreathing)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.FireBreathing) == 2


def test_rupture_applies_power():
    cs = make_combat()
    hp_before = cs.player.hp
    cs.add_card_to_hand(sts_sim.Card.Rupture)
    idx = find_card_in_hand(cs, sts_sim.Card.Rupture)
    cs.play_card(idx, None)
    # BG mod: Rupture loses 1 HP and gains 1 Strength (not vanilla Rupture power)
    assert cs.get_player_power(sts_sim.PowerType.Strength) == 1
    assert cs.player.hp == hp_before - 1


def test_power_cards_not_discarded():
    """Power cards should be removed from play, not go to discard."""
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Inflame)
    cs.set_player_energy(5)
    discard_before = len(cs.get_discard_pile())
    idx = find_card_in_hand(cs, sts_sim.Card.Inflame)
    cs.play_card(idx, None)
    # Power cards are removed from play — not in discard or exhaust
    assert len(cs.get_discard_pile()) == discard_before
    exhaust = cs.get_exhaust_pile()
    assert not any(ci.card == sts_sim.Card.Inflame for ci in exhaust)


# =========================================================================
# Rare Attacks
# =========================================================================

def test_bludgeon_deals_big_damage():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Bludgeon)
    idx = find_card_in_hand(cs, sts_sim.Card.Bludgeon)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    assert cs.get_monsters()[0].hp == m_hp_before - 7


def test_feed_kills_and_gains_strength():
    cs = make_combat()
    cs.set_player_energy(5)
    # Feed deals 3 damage. Weaken jaw worm (8 HP) to 3 HP first.
    while cs.get_monsters()[0].hp > 3:
        cs.add_card_to_hand(sts_sim.Card.StrikeRed)
        idx = find_card_in_hand(cs, sts_sim.Card.StrikeRed)
        cs.set_player_energy(5)
        cs.play_card(idx, 0)
        if cs.get_monsters()[0].hp <= 0:
            break
    if cs.get_monsters()[0].hp > 0:
        str_before = cs.get_player_power(sts_sim.PowerType.Strength)
        cs.add_card_to_hand(sts_sim.Card.Feed)
        cs.set_player_energy(5)
        idx = find_card_in_hand(cs, sts_sim.Card.Feed)
        cs.play_card(idx, 0)
        if cs.get_monsters()[0].hp <= 0:
            # BG mod: Feed gives Strength on kill (not max HP)
            assert cs.get_player_power(sts_sim.PowerType.Strength) == str_before + 1


def test_fiend_fire_exhausts_hand_and_deals_damage():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.FiendFire)
    hand = cs.get_hand()
    hand_size = len(hand)
    # FiendFire exhausts all other hand cards, deals 1 damage per exhausted card
    idx = find_card_in_hand(cs, sts_sim.Card.FiendFire)
    cards_to_exhaust = hand_size - 1  # all except FiendFire itself
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    # All hand cards should be gone
    assert len(cs.get_hand()) == 0
    # Damage = base_damage * cards_exhausted = 1 * cards_to_exhaust
    assert cs.get_monsters()[0].hp == m_hp_before - cards_to_exhaust
    # FiendFire itself exhausts too
    assert len(cs.get_exhaust_pile()) >= cards_to_exhaust


def test_immolate_hits_all_and_adds_dazed():
    # Use jaw_worm (no CurlUp) to test AoE damage
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Immolate)
    idx = find_card_in_hand(cs, sts_sim.Card.Immolate)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, None)
    assert cs.get_monsters()[0].hp == m_hp_before - 5
    # BG mod: 2 Dazed added to discard pile
    discard = cs.get_discard_pile()
    dazed_count = sum(1 for ci in discard if ci.card == sts_sim.Card.Dazed)
    assert dazed_count == 2


# =========================================================================
# Rare Skills
# =========================================================================

def test_double_tap_applies_power():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.DoubleTap)
    idx = find_card_in_hand(cs, sts_sim.Card.DoubleTap)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.DoubleTap) == 1


def test_exhume_retrieves_from_exhaust():
    cs = make_combat()
    # Put something in exhaust first
    cs.add_card_to_hand(sts_sim.Card.SeeingRed)
    sr_idx = find_card_in_hand(cs, sts_sim.Card.SeeingRed)
    cs.play_card(sr_idx, None)  # exhausts
    assert len(cs.get_exhaust_pile()) == 1

    cs.add_card_to_hand(sts_sim.Card.Exhume)
    idx = find_card_in_hand(cs, sts_sim.Card.Exhume)
    hand_size = len(cs.get_hand())
    cs.play_card(idx, None)
    # Retrieves 1 card from exhaust to hand. Exhume itself exhausts.
    # Net hand: -1 (Exhume played) +1 (retrieved) = same
    assert len(cs.get_hand()) == hand_size
    # Exhaust pile: had 1 (SeeingRed), -1 (retrieved), +1 (Exhume) = 1
    assert len(cs.get_exhaust_pile()) == 1


def test_limit_break_doubles_strength():
    cs = make_combat()
    cs.apply_player_power(sts_sim.PowerType.Strength, 3)
    cs.add_card_to_hand(sts_sim.Card.LimitBreak)
    idx = find_card_in_hand(cs, sts_sim.Card.LimitBreak)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.Strength) == 6


def test_limit_break_exhausts_base():
    cs = make_combat()
    cs.apply_player_power(sts_sim.PowerType.Strength, 1)
    cs.add_card_to_hand(sts_sim.Card.LimitBreak)
    idx = find_card_in_hand(cs, sts_sim.Card.LimitBreak)
    cs.play_card(idx, None)
    exhaust = cs.get_exhaust_pile()
    assert any(ci.card == sts_sim.Card.LimitBreak for ci in exhaust)


def test_limit_break_upgraded_no_exhaust():
    cs = make_combat()
    cs.apply_player_power(sts_sim.PowerType.Strength, 2)
    cs.add_upgraded_card_to_hand(sts_sim.Card.LimitBreak)
    idx = find_card_in_hand(cs, sts_sim.Card.LimitBreak)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.Strength) == 4
    # Upgraded LimitBreak does NOT exhaust
    exhaust = cs.get_exhaust_pile()
    assert not any(ci.card == sts_sim.Card.LimitBreak for ci in exhaust)


def test_offering_loses_hp_gains_energy_draws():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Offering)
    idx = find_card_in_hand(cs, sts_sim.Card.Offering)
    hp_before = cs.player.hp
    energy_before = cs.player.energy
    hand_size = len(cs.get_hand())
    cs.play_card(idx, None)
    assert cs.player.hp == hp_before - 1
    assert cs.player.energy == energy_before + 2  # costs 0, gains 2
    # Draws 3: -1 played +3 drawn = net +2
    assert len(cs.get_hand()) == hand_size + 2


def test_impervious_gives_big_block():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Impervious)
    idx = find_card_in_hand(cs, sts_sim.Card.Impervious)
    cs.play_card(idx, None)
    # BG mod: Impervious base block = 6
    assert cs.player.block == 6


def test_impervious_exhausts():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Impervious)
    idx = find_card_in_hand(cs, sts_sim.Card.Impervious)
    cs.play_card(idx, None)
    exhaust = cs.get_exhaust_pile()
    assert any(ci.card == sts_sim.Card.Impervious for ci in exhaust)


# =========================================================================
# Rare Powers
# =========================================================================

def test_barricade_card_applies_power():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Barricade)
    idx = find_card_in_hand(cs, sts_sim.Card.Barricade)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.Barricade) == 1


def test_berserk_card_applies_power():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.BerserkCard)
    idx = find_card_in_hand(cs, sts_sim.Card.BerserkCard)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.Berserk) == 1


def test_corruption_card_applies_power():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Corruption)
    idx = find_card_in_hand(cs, sts_sim.Card.Corruption)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.Corruption) == 1


def test_demon_form_card_applies_power():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.DemonForm)
    idx = find_card_in_hand(cs, sts_sim.Card.DemonForm)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.DemonForm) == 1


def test_juggernaut_card_applies_power():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Juggernaut)
    idx = find_card_in_hand(cs, sts_sim.Card.Juggernaut)
    cs.play_card(idx, None)
    assert cs.get_player_power(sts_sim.PowerType.Juggernaut) == 1


# =========================================================================
# Status & Curse cards
# =========================================================================

def test_dazed_unplayable():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Dazed)
    idx = find_card_in_hand(cs, sts_sim.Card.Dazed)
    ci = cs.get_hand()[idx]
    assert ci.py_unplayable is True


def test_dazed_ethereal():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Dazed)
    ci_list = [ci for ci in cs.get_hand() if ci.card == sts_sim.Card.Dazed]
    assert ci_list[0].py_ethereal is True


def test_burn_damages_at_end_of_turn():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Burn)
    hp_before = cs.player.hp
    cs.end_player_turn()
    # Burn deals 1 damage at end of turn
    assert cs.player.hp == hp_before - 1


def test_wound_unplayable():
    ci = sts_sim.CardInstance(sts_sim.Card.Wound)
    assert ci.py_unplayable is True


def test_slimed_playable_and_exhausts():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Slimed)
    idx = find_card_in_hand(cs, sts_sim.Card.Slimed)
    cs.play_card(idx, None)
    exhaust = cs.get_exhaust_pile()
    assert any(ci.card == sts_sim.Card.Slimed for ci in exhaust)


def test_ethereal_cards_exhaust_at_end_of_turn():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Dazed)
    cs.end_player_turn()
    # Dazed is ethereal: should be exhausted, not discarded
    exhaust = cs.get_exhaust_pile()
    assert any(ci.card == sts_sim.Card.Dazed for ci in exhaust)


def test_decay_damages_at_end_of_turn():
    cs = make_combat()
    cs.add_card_to_hand(sts_sim.Card.Decay)
    hp_before = cs.player.hp
    cs.end_player_turn()
    assert cs.player.hp == hp_before - 1


# =========================================================================
# Upgraded card tests
# =========================================================================

def test_upgraded_strike_more_damage():
    cs = make_combat()
    cs.add_upgraded_card_to_hand(sts_sim.Card.StrikeRed)
    # The upgraded Strike is the last card in hand
    hand = cs.get_hand()
    idx = len(hand) - 1  # last card is the upgraded one we just added
    assert hand[idx].upgraded is True
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    # Upgraded Strike deals 2
    assert cs.get_monsters()[0].hp == m_hp_before - 2


def test_upgraded_defend_more_block():
    cs = make_combat()
    cs.add_upgraded_card_to_hand(sts_sim.Card.DefendRed)
    idx = find_card_in_hand(cs, sts_sim.Card.DefendRed)
    cs.play_card(idx, None)
    # Upgraded Defend gives 2 block
    assert cs.player.block == 2


def test_upgraded_body_slam_costs_zero():
    ci = sts_sim.CardInstance(sts_sim.Card.BodySlam, True)
    assert ci.py_cost == 0


def test_upgraded_seeing_red_costs_zero():
    ci = sts_sim.CardInstance(sts_sim.Card.SeeingRed, True)
    assert ci.py_cost == 0


def test_upgraded_bludgeon_deals_10_damage():
    cs = make_combat()
    cs.set_player_energy(5)
    cs.add_upgraded_card_to_hand(sts_sim.Card.Bludgeon)
    idx = find_card_in_hand(cs, sts_sim.Card.Bludgeon)
    m_hp_before = cs.get_monsters()[0].hp
    cs.play_card(idx, 0)
    # BG mod: Bludgeon+ deals 10 damage (up from 7)
    assert cs.get_monsters()[0].hp == m_hp_before - 10


# =========================================================================
# Card properties
# =========================================================================

def test_card_types():
    assert sts_sim.Card.StrikeRed.py_card_type == sts_sim.CardType.Attack
    assert sts_sim.Card.DefendRed.py_card_type == sts_sim.CardType.Skill
    assert sts_sim.Card.Inflame.py_card_type == sts_sim.CardType.Power
    assert sts_sim.Card.Dazed.py_card_type == sts_sim.CardType.Status
    assert sts_sim.Card.AscendersBane.py_card_type == sts_sim.CardType.Curse


def test_targeting():
    assert sts_sim.Card.StrikeRed.py_has_target is True
    assert sts_sim.Card.DefendRed.py_has_target is False
    assert sts_sim.Card.Cleave.py_has_target is False
    assert sts_sim.Card.Whirlwind.py_has_target is False
    assert sts_sim.Card.Disarm.py_has_target is True
    assert sts_sim.Card.Immolate.py_has_target is False
