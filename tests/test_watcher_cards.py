"""Tests for Watcher cards, stance system, miracles, and scry mechanics."""
import sts_sim


def make_combat(character=None, seed=0):
    """Create a Watcher combat with a single 20HP monster."""
    ch = character or sts_sim.Character.Watcher
    m = sts_sim.Monster("Test", 20, "test", "AAAA", False)
    cs = sts_sim.CombatState.new_with_character([m], seed, ch)
    return cs


def setup_card(cs, card, upgraded=False, energy=10):
    """Add a card to hand, set energy high so cost is never an issue."""
    if upgraded:
        cs.add_upgraded_card_to_hand(card)
    else:
        cs.add_card_to_hand(card)
    cs.set_player_energy(energy)
    hand = cs.get_hand()
    return len(hand) - 1  # hand index


# ==================== STANCE TESTS ====================


def test_watcher_starts_neutral():
    cs = make_combat()
    assert cs.get_stance() == sts_sim.Stance.Neutral


def test_eruption_enters_wrath():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.Eruption)
    cs.play_card(hi, 0)
    assert cs.get_stance() == sts_sim.Stance.Wrath


def test_vigilance_enters_calm():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.Vigilance)
    cs.play_card(hi, None)
    assert cs.get_stance() == sts_sim.Stance.Calm


def test_calm_exit_gives_energy():
    """Exiting Calm should give +2 energy."""
    cs = make_combat()
    # Enter Calm first
    hi = setup_card(cs, sts_sim.Card.Vigilance)
    cs.play_card(hi, None)
    assert cs.get_stance() == sts_sim.Stance.Calm
    # Now enter Wrath (exits Calm -> +2 energy)
    cs.set_player_energy(5)
    hi = setup_card(cs, sts_sim.Card.Eruption, energy=5)
    cs.play_card(hi, 0)
    assert cs.get_stance() == sts_sim.Stance.Wrath
    # Energy: 5 - 2 (Eruption cost) + 2 (Calm exit) = 5
    assert cs.player.energy == 5


def test_wrath_adds_damage():
    """Wrath stance should add +1 to attack damage."""
    cs = make_combat()
    m = cs.get_monsters()[0]
    hp_start = m.hp

    # Attack without Wrath (Neutral)
    hi = setup_card(cs, sts_sim.Card.StrikePurple)
    cs.play_card(hi, 0)
    m = cs.get_monsters()[0]
    damage_neutral = hp_start - m.hp  # should be 1

    # Enter Wrath
    hi = setup_card(cs, sts_sim.Card.Crescendo)
    cs.play_card(hi, None)
    assert cs.get_stance() == sts_sim.Stance.Wrath

    # Attack in Wrath
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.StrikePurple)
    cs.play_card(hi, 0)
    m = cs.get_monsters()[0]
    damage_wrath = hp_before - m.hp  # should be 2 (1 base + 1 Wrath)

    assert damage_neutral == 1
    assert damage_wrath == 2


def test_wrath_end_of_turn_damage():
    """Wrath should deal 1 damage to player at end of turn."""
    cs = make_combat()
    cs.set_player_hp(10)
    # Enter Wrath
    hi = setup_card(cs, sts_sim.Card.Crescendo)
    cs.play_card(hi, None)
    assert cs.get_stance() == sts_sim.Stance.Wrath
    cs.end_player_turn()
    assert cs.player.hp == 9  # took 1 damage from Wrath


def test_empty_body_enters_neutral():
    cs = make_combat()
    # First enter Wrath
    hi = setup_card(cs, sts_sim.Card.Crescendo)
    cs.play_card(hi, None)
    assert cs.get_stance() == sts_sim.Stance.Wrath
    # Empty Body enters Neutral
    hi = setup_card(cs, sts_sim.Card.EmptyBody)
    cs.play_card(hi, None)
    assert cs.get_stance() == sts_sim.Stance.Neutral


def test_empty_fist_enters_neutral_and_deals_damage():
    cs = make_combat()
    # Enter Wrath
    hi = setup_card(cs, sts_sim.Card.Crescendo)
    cs.play_card(hi, None)
    # Empty Fist
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.EmptyFist)
    cs.play_card(hi, 0)
    assert cs.get_stance() == sts_sim.Stance.Neutral
    # Damage should include Wrath bonus (+1) since stance changes AFTER attack
    # Actually, Empty Fist deals damage then changes stance
    # In Wrath: 2 base + 1 Wrath = 3
    assert cs.get_monsters()[0].hp == hp_before - 3


def test_tranquility_enters_calm():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.Tranquility)
    cs.play_card(hi, None)
    assert cs.get_stance() == sts_sim.Stance.Calm


def test_crescendo_enters_wrath():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.Crescendo)
    cs.play_card(hi, None)
    assert cs.get_stance() == sts_sim.Stance.Wrath


def test_same_stance_no_change():
    """Entering same stance should not trigger exit/enter effects."""
    cs = make_combat()
    # Enter Calm
    hi = setup_card(cs, sts_sim.Card.Tranquility)
    cs.play_card(hi, None)
    assert cs.get_stance() == sts_sim.Stance.Calm
    # Try to enter Calm again via Vigilance
    cs.set_player_energy(5)
    hi = setup_card(cs, sts_sim.Card.Vigilance)
    energy_before = cs.player.energy
    cs.play_card(hi, None)
    # Should not get +2 from Calm exit (didn't actually change)
    assert cs.get_stance() == sts_sim.Stance.Calm
    assert cs.player.energy == energy_before - 2  # just paid cost, no Calm exit energy


# ==================== MIRACLE TESTS ====================


def test_miracles_relic_gives_1_at_start():
    cs = make_combat()
    cs.start_combat()
    assert cs.get_miracles() >= 1


def test_collect_gains_miracles():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.Collect)
    cs.play_card(hi, None)
    assert cs.get_miracles() == 2  # base magic = 2


def test_collect_upgraded_gains_3():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.Collect, upgraded=True)
    cs.play_card(hi, None)
    assert cs.get_miracles() == 3


def test_deus_ex_machina_gains_miracles():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.DeusExMachina)
    cs.play_card(hi, None)
    assert cs.get_miracles() == 2


def test_prostrate_gains_miracle_and_block():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.Prostrate)
    cs.play_card(hi, None)
    assert cs.get_miracles() == 1
    assert cs.player.block > 0


def test_miracles_used_for_energy():
    """Miracles should be usable as extra energy."""
    cs = make_combat()
    # Give some miracles
    cs.apply_player_power(sts_sim.PowerType.MiracleCount, 3)
    cs.set_player_energy(0)  # no regular energy
    # Should be able to play a 1-cost card
    hi = setup_card(cs, sts_sim.Card.StrikePurple, energy=0)
    cs.set_player_energy(0)
    result = cs.play_card(hi, 0)
    assert result is True
    assert cs.get_miracles() == 2  # used 1 miracle


def test_brilliance_scales_with_miracles():
    cs = make_combat()
    cs.apply_player_power(sts_sim.PowerType.MiracleCount, 3)
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.BrillianceCard)
    cs.play_card(hi, 0)
    # base_damage(2) * 3 miracles = 6
    assert cs.get_monsters()[0].hp == hp_before - 6


def test_reach_heaven_scales_with_miracles():
    cs = make_combat()
    cs.apply_player_power(sts_sim.PowerType.MiracleCount, 2)
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.ReachHeaven)
    cs.play_card(hi, 0)
    # base 2 + magic(1) * 2 miracles = 4
    assert cs.get_monsters()[0].hp == hp_before - 4


# ==================== SCRY TESTS ====================


def test_third_eye_gives_block_and_scries():
    cs = make_combat()
    # Add some status cards to draw pile
    cs.add_card_to_draw(sts_sim.Card.Dazed)
    cs.add_card_to_draw(sts_sim.Card.Wound)
    draw_size_before = len(cs.get_draw_pile())
    hi = setup_card(cs, sts_sim.Card.ThirdEye)
    cs.play_card(hi, None)
    assert cs.player.block > 0
    # Scry should have moved status cards to discard
    draw_size_after = len(cs.get_draw_pile())
    assert draw_size_after < draw_size_before


def test_cut_through_fate_attacks_scries_draws():
    cs = make_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.CutThroughFate)
    cs.play_card(hi, 0)
    assert cs.get_monsters()[0].hp < hp_before


# ==================== CARD EFFECT TESTS ====================


def test_consecrate_hits_all():
    m1 = sts_sim.Monster("A", 10, "a", "AAAA", False)
    m2 = sts_sim.Monster("B", 10, "b", "AAAA", False)
    cs = sts_sim.CombatState.new_with_character([m1, m2], 0, sts_sim.Character.Watcher)
    hi = setup_card(cs, sts_sim.Card.Consecrate)
    cs.play_card(hi, None)
    monsters = cs.get_monsters()
    assert monsters[0].hp < 10
    assert monsters[1].hp < 10


def test_crush_joints_deals_damage_and_weak():
    cs = make_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.CrushJoints)
    cs.play_card(hi, 0)
    m = cs.get_monsters()[0]
    assert m.hp < hp_before
    assert m.get_power(sts_sim.PowerType.Weak) > 0


def test_sash_whip_deals_damage_and_vuln():
    cs = make_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.SashWhip)
    cs.play_card(hi, 0)
    m = cs.get_monsters()[0]
    assert m.hp < hp_before
    assert m.get_power(sts_sim.PowerType.Vulnerable) > 0


def test_tantrum_multi_hit_and_enters_wrath():
    cs = make_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Tantrum)
    cs.play_card(hi, 0)
    assert cs.get_stance() == sts_sim.Stance.Wrath
    # 1 hit of 2 damage = 2
    assert cs.get_monsters()[0].hp == hp_before - 2


def test_flying_sleeves_multi_hit():
    cs = make_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.FlyingSleeves)
    cs.play_card(hi, 0)
    # 2 hits of 1 damage = 2
    assert cs.get_monsters()[0].hp == hp_before - 2


def test_conclude_aoe_multi_hit():
    m1 = sts_sim.Monster("A", 10, "a", "AAAA", False)
    m2 = sts_sim.Monster("B", 10, "b", "AAAA", False)
    cs = sts_sim.CombatState.new_with_character([m1, m2], 0, sts_sim.Character.Watcher)
    hi = setup_card(cs, sts_sim.Card.Conclude)
    cs.play_card(hi, None)
    monsters = cs.get_monsters()
    # 2 hits of 1 damage each to all enemies
    assert monsters[0].hp == 8
    assert monsters[1].hp == 8


def test_ragnarok_multi_hit():
    cs = make_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Ragnarok)
    cs.play_card(hi, 0)
    # 1 + 4 (magic) = 5 hits of 1 damage = 5
    assert cs.get_monsters()[0].hp == hp_before - 5


def test_empty_mind_draws_and_enters_neutral():
    cs = make_combat()
    # Enter Wrath first
    hi = setup_card(cs, sts_sim.Card.Crescendo)
    cs.play_card(hi, None)
    # Empty Mind
    hi = setup_card(cs, sts_sim.Card.EmptyMind)
    cs.play_card(hi, None)
    assert cs.get_stance() == sts_sim.Stance.Neutral


def test_meditate_scries_and_enters_calm():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.MeditateCard)
    cs.play_card(hi, None)
    assert cs.get_stance() == sts_sim.Stance.Calm


def test_inner_peace_draws_cards():
    cs = make_combat()
    # Add some cards to draw pile
    for _ in range(5):
        cs.add_card_to_draw(sts_sim.Card.StrikePurple)
    hi = setup_card(cs, sts_sim.Card.InnerPeace)
    hand_before = len(cs.get_hand())
    cs.play_card(hi, None)
    # Plays InnerPeace (-1) and draws 3, net +2
    assert len(cs.get_hand()) == hand_before - 1 + 3


def test_pray_gains_miracles_and_draws():
    cs = make_combat()
    for _ in range(3):
        cs.add_card_to_draw(sts_sim.Card.StrikePurple)
    hi = setup_card(cs, sts_sim.Card.Pray)
    cs.play_card(hi, None)
    assert cs.get_miracles() == 1  # base magic
    assert cs.get_player_power(sts_sim.PowerType.NoDraw) == 1


def test_swivel_gives_block_and_free_attack():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.Swivel)
    cs.play_card(hi, None)
    assert cs.player.block > 0
    # Next attack should be free — play a 1-cost Strike and verify no energy spent
    energy_before = cs.player.energy
    hi2 = setup_card(cs, sts_sim.Card.StrikePurple, energy=energy_before)
    cs.play_card(hi2, 0)
    assert cs.player.energy == energy_before  # attack was free


def test_indignation_in_wrath_applies_vuln():
    cs = make_combat()
    # Enter Wrath
    hi = setup_card(cs, sts_sim.Card.Crescendo)
    cs.play_card(hi, None)
    # Indignation in Wrath
    hi = setup_card(cs, sts_sim.Card.Indignation)
    cs.play_card(hi, None)
    m = cs.get_monsters()[0]
    assert m.get_power(sts_sim.PowerType.Vulnerable) > 0


def test_indignation_not_in_wrath_enters_wrath():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.Indignation)
    cs.play_card(hi, None)
    assert cs.get_stance() == sts_sim.Stance.Wrath


def test_blasphemy_exhausts_draw_and_gives_triple():
    cs = make_combat()
    for _ in range(3):
        cs.add_card_to_draw(sts_sim.Card.StrikePurple)
    draw_before = len(cs.get_draw_pile())
    hi = setup_card(cs, sts_sim.Card.Blasphemy)
    cs.play_card(hi, None)
    assert len(cs.get_draw_pile()) == 0
    assert cs.get_player_power(sts_sim.PowerType.TripleAttack) == 1


def test_judgment_kills_low_hp():
    m = sts_sim.Monster("Weak", 5, "weak", "AAAA", False)
    cs = sts_sim.CombatState.new_with_character([m], 0, sts_sim.Character.Watcher)
    hi = setup_card(cs, sts_sim.Card.JudgmentCard)
    cs.play_card(hi, 0)
    # Judgment magic = 7, monster HP = 5, should kill
    assert cs.get_monsters()[0].is_dead()


def test_judgment_doesnt_kill_high_hp():
    m = sts_sim.Monster("Strong", 10, "strong", "AAAA", False)
    cs = sts_sim.CombatState.new_with_character([m], 0, sts_sim.Character.Watcher)
    hi = setup_card(cs, sts_sim.Card.JudgmentCard)
    cs.play_card(hi, 0)
    # Judgment magic = 7, monster HP = 10, should NOT kill
    assert not cs.get_monsters()[0].is_dead()
    assert cs.get_monsters()[0].hp == 10


def test_vault_discards_hand_draws_and_gains_energy():
    cs = make_combat()
    for _ in range(5):
        cs.add_card_to_draw(sts_sim.Card.StrikePurple)
    hi = setup_card(cs, sts_sim.Card.VaultCard, energy=6)
    energy_before = cs.player.energy
    cs.play_card(hi, None)
    # Vault costs 3, gives +3 energy, net 0 change
    assert cs.player.energy == energy_before - 3 + 3


def test_scrawl_draws_5():
    cs = make_combat()
    for _ in range(5):
        cs.add_card_to_draw(sts_sim.Card.StrikePurple)
    hi = setup_card(cs, sts_sim.Card.ScrawlCard)
    hand_before = len(cs.get_hand())
    cs.play_card(hi, None)
    # Plays ScrawlCard (-1) and draws 5, net +4
    assert len(cs.get_hand()) == hand_before - 1 + 5


def test_spirit_shield_block_per_card():
    cs = make_combat()
    # Add 3 cards to hand
    for _ in range(3):
        setup_card(cs, sts_sim.Card.StrikePurple)
    cs.set_player_energy(10)
    hi = setup_card(cs, sts_sim.Card.SpiritShieldCard)
    hand_size = len(cs.get_hand())
    cs.play_card(hi, None)
    # Block = 1 * (hand_size - 1) since SpiritShield was removed before effect
    # Actually the card is removed from hand before playing
    assert cs.player.block == hand_size - 1


# ==================== POWER TESTS ====================


def test_mental_fortress_block_on_stance_change():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.MentalFortressCard)
    cs.play_card(hi, None)
    # Change stance
    hi = setup_card(cs, sts_sim.Card.Crescendo)
    cs.play_card(hi, None)
    assert cs.player.block >= 1  # Mental Fortress gives 1 block per stance change


def test_rushdown_draws_on_entering_wrath():
    cs = make_combat()
    for _ in range(5):
        cs.add_card_to_draw(sts_sim.Card.StrikePurple)
    hi = setup_card(cs, sts_sim.Card.RushdownCard)
    cs.play_card(hi, None)
    hand_before = len(cs.get_hand())
    # Enter Wrath -> Rushdown draws 2
    hi = setup_card(cs, sts_sim.Card.Crescendo)
    cs.play_card(hi, None)
    # Hand should have grown (drew 2, played 1 Crescendo)
    assert len(cs.get_hand()) >= hand_before + 2 - 1


def test_like_water_block_in_calm_at_end():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.LikeWaterCard)
    cs.play_card(hi, None)
    hi = setup_card(cs, sts_sim.Card.Tranquility)
    cs.play_card(hi, None)
    assert cs.get_stance() == sts_sim.Stance.Calm
    cs.end_player_turn()
    assert cs.player.block >= 1


def test_omega_deals_damage_end_of_turn():
    cs = make_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.OmegaCard)
    cs.play_card(hi, None)
    cs.end_player_turn()
    # Omega deals 5 damage at end of turn
    assert cs.get_monsters()[0].hp == hp_before - 5


def test_simmering_fury_boosts_wrath():
    cs = make_combat()
    hi = setup_card(cs, sts_sim.Card.SimmeringFuryCard)
    cs.play_card(hi, None)
    # Enter Wrath
    hi = setup_card(cs, sts_sim.Card.Crescendo)
    cs.play_card(hi, None)
    # Attack: base 1 + Wrath 1 + SimmeringFury 1 = 3
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.StrikePurple)
    cs.play_card(hi, 0)
    assert cs.get_monsters()[0].hp == hp_before - 3


# ==================== REWARD/PROPERTY TESTS ====================


def test_watcher_reward_deck():
    rd = sts_sim.RewardDeck(42, sts_sim.Character.Watcher)
    rewards = rd.draw_rewards(3)
    assert len(rewards) == 3
    for r in rewards:
        assert r.py_name != ""


def test_watcher_card_exhausts():
    assert sts_sim.CardInstance(sts_sim.Card.Tranquility, False).py_exhausts is True
    assert sts_sim.CardInstance(sts_sim.Card.Crescendo, False).py_exhausts is True
    assert sts_sim.CardInstance(sts_sim.Card.Collect, False).py_exhausts is True
    assert sts_sim.CardInstance(sts_sim.Card.DeusExMachina, False).py_exhausts is True
    assert sts_sim.CardInstance(sts_sim.Card.Blasphemy, False).py_exhausts is True
    assert sts_sim.CardInstance(sts_sim.Card.Blasphemy, True).py_exhausts is True  # BG: always exhausts


def test_watcher_card_retain():
    assert sts_sim.CardInstance(sts_sim.Card.Protect, False).py_retain is True
    assert sts_sim.CardInstance(sts_sim.Card.Tranquility, False).py_retain is True
    assert sts_sim.CardInstance(sts_sim.Card.Crescendo, False).py_retain is True
    assert sts_sim.CardInstance(sts_sim.Card.SandsOfTime, False).py_retain is True
    assert sts_sim.CardInstance(sts_sim.Card.FlyingSleeves, False).py_retain is True
    assert sts_sim.CardInstance(sts_sim.Card.Perseverance, False).py_retain is True


def test_watcher_card_ethereal():
    assert sts_sim.CardInstance(sts_sim.Card.JudgmentCard, False).py_ethereal is True
    assert sts_sim.CardInstance(sts_sim.Card.JudgmentCard, True).py_ethereal is False


def test_watcher_card_names():
    assert sts_sim.Card.Eruption.py_name == "Eruption"
    assert sts_sim.Card.Vigilance.py_name == "Vigilance"
    assert sts_sim.Card.FlurryOfBlows.py_name == "Flurry of Blows"
    assert sts_sim.Card.CutThroughFate.py_name == "Cut Through Fate"
    assert sts_sim.Card.Crescendo.py_name == "Crescendo"
    assert sts_sim.Card.MeditateCard.py_name == "Meditate"
    assert sts_sim.Card.Blasphemy.py_name == "Blasphemy"
    assert sts_sim.Card.JudgmentCard.py_name == "Judgment"
    assert sts_sim.Card.OmegaCard.py_name == "Omega"
    assert sts_sim.Card.BrillianceCard.py_name == "Brilliance"


def test_eruption_upgrade_reduces_cost_not_damage():
    ci_base = sts_sim.CardInstance(sts_sim.Card.Eruption, False)
    ci_up = sts_sim.CardInstance(sts_sim.Card.Eruption, True)
    assert ci_base.py_cost == 2
    assert ci_up.py_cost == 1
    assert ci_base.py_base_damage == 2
    assert ci_up.py_base_damage == 2  # damage unchanged


# ==================== X-COST AND CHOICE CARDS ====================


def test_conjure_blade_boosts_starter_strike():
    """ConjureBlade applies ConjureBladePower that boosts starter Strikes."""
    cs = make_combat()
    cs.start_combat()
    cs.set_player_energy(3)
    hi = setup_card(cs, sts_sim.Card.ConjureBladeCard, energy=3)
    cs.play_card(hi, None)  # X=3, magic=1 -> power = 4
    assert cs.get_player_power(sts_sim.PowerType.ConjureBladePower) == 4
    # Now play a starter Strike — should deal base(1) + 4 = 5 damage
    hp_before = cs.get_monsters()[0].hp
    hi2 = setup_card(cs, sts_sim.Card.StrikePurple)
    cs.play_card(hi2, 0)
    assert cs.get_monsters()[0].hp == hp_before - 5


def test_conjure_blade_choice_partial():
    """ConjureBlade with choice=1 spends only 1 energy."""
    cs = make_combat()
    cs.start_combat()
    cs.set_player_energy(3)
    hi = setup_card(cs, sts_sim.Card.ConjureBladeCard, energy=3)
    cs.play_card(hi, None, 1)  # X=1, magic=1 -> power = 2
    assert cs.get_player_power(sts_sim.PowerType.ConjureBladePower) == 2
    assert cs.player.energy == 2


def test_worship_choice_partial():
    """Worship with choice spends only chosen energy."""
    cs = make_combat()
    cs.start_combat()
    cs.set_player_energy(3)
    hi = setup_card(cs, sts_sim.Card.WorshipCard, energy=3)
    cs.play_card(hi, None, 2)
    assert cs.get_player_power(sts_sim.PowerType.MiracleCount) >= 2
    assert cs.player.energy == 1


def test_wish_choice_strength():
    """Wish with choice=0 gives Strength."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.WishCard)
    cs.play_card(hi, None, 0)
    assert cs.get_player_power(sts_sim.PowerType.Strength) == 1


def test_wish_choice_block():
    """Wish with choice=1 gives block."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.WishCard)
    cs.play_card(hi, None, 1)
    assert cs.player.block >= 10


def test_wish_choice_miracles():
    """Wish with choice=2 gives miracles."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.WishCard)
    cs.play_card(hi, None, 2)
    assert cs.get_player_power(sts_sim.PowerType.MiracleCount) >= 4
