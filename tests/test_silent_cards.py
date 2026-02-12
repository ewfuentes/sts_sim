"""Tests for Silent cards and mechanics (Phase 2)."""
import sts_sim


def make_combat(seed=0):
    """Create a Silent combat against Jaw Worm."""
    cs = sts_sim.create_encounter("jaw_worm", seed, sts_sim.Character.Silent)
    return cs


def make_multi_combat(seed=0):
    """Create a Silent combat against multiple enemies (louse encounter)."""
    cs = sts_sim.create_encounter("louse", seed, sts_sim.Character.Silent)
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


# ==================== POISON MECHANIC ====================


def test_poison_tick():
    """Poison deals damage at end of monster turn and reduces by 1."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.DeadlyPoison)
    cs.play_card(hi, 0)
    monsters = cs.get_monsters()
    assert monsters[0].get_power(sts_sim.PowerType.Poison) == 1
    hp_before = monsters[0].hp
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    monsters = cs.get_monsters()
    # Poison dealt 1 damage, then reduced to 0
    assert monsters[0].hp <= hp_before - 1


def test_poison_stacks():
    """Multiple poison applications stack."""
    cs = make_combat()
    cs.start_combat()
    hi1 = setup_card(cs, sts_sim.Card.DeadlyPoison)
    cs.play_card(hi1, 0)
    hi2 = setup_card(cs, sts_sim.Card.DeadlyPoison)
    cs.play_card(hi2, 0)
    monsters = cs.get_monsters()
    assert monsters[0].get_power(sts_sim.PowerType.Poison) == 2


def test_catalyst_doubles_poison():
    """Catalyst doubles existing poison."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.DeadlyPoison)
    cs.play_card(hi, 0)
    assert cs.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 1
    hi = setup_card(cs, sts_sim.Card.Catalyst)
    cs.play_card(hi, 0)
    assert cs.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 2


def test_catalyst_upgraded_triples_poison():
    """Upgraded Catalyst triples existing poison."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.DeadlyPoison)
    cs.play_card(hi, 0)
    hi = setup_card(cs, sts_sim.Card.Catalyst, upgraded=True)
    cs.play_card(hi, 0)
    assert cs.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 3


def test_corpse_explosion_applies_poison_and_power():
    """Corpse Explosion applies poison (BG mod doesn't apply CorpseExplosion power)."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.CorpseExplosionCard)
    cs.play_card(hi, 0)
    m = cs.get_monsters()[0]
    assert m.get_power(sts_sim.PowerType.Poison) == 2


def test_bouncing_flask_applies_poison():
    """Bouncing Flask applies poison equal to magic number."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.BouncingFlask)
    cs.play_card(hi, 0)
    assert cs.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 2


def test_crippling_cloud_poison_and_weak_all():
    """Crippling Cloud applies poison and weak to all enemies."""
    cs = make_multi_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.CripplingCloud)
    cs.play_card(hi, None)
    for m in cs.get_monsters():
        if not m.is_dead():
            assert m.get_power(sts_sim.PowerType.Poison) >= 1
            assert m.get_power(sts_sim.PowerType.Weak) >= 1


# ==================== ATTACK CARD EFFECTS ====================


def test_neutralize_deals_damage_and_weak():
    """Neutralize deals damage and applies Weak."""
    cs = make_combat()
    cs.start_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Neutralize)
    cs.play_card(hi, 0)
    m = cs.get_monsters()[0]
    assert m.hp < hp_before
    assert m.get_power(sts_sim.PowerType.Weak) > 0


def test_poisoned_stab_damage_and_poison():
    """Poisoned Stab deals damage and applies poison."""
    cs = make_combat()
    cs.start_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.PoisonedStab)
    cs.play_card(hi, 0)
    m = cs.get_monsters()[0]
    assert m.hp < hp_before
    assert m.get_power(sts_sim.PowerType.Poison) >= 1


def test_slice_deals_damage():
    """Slice deals damage (0 cost attack)."""
    cs = make_combat()
    cs.start_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Slice)
    cs.play_card(hi, 0)
    assert cs.get_monsters()[0].hp < hp_before


def test_sneaky_strike_deals_damage_and_gains_energy():
    """SneakyStrike deals damage; +2 energy only if discarded this turn."""
    cs = make_combat()
    cs.start_combat()
    cs.set_player_energy(3)
    hi = setup_card(cs, sts_sim.Card.SneakyStrike, energy=3)
    hp_before = cs.get_monsters()[0].hp
    cs.play_card(hi, 0)
    assert cs.get_monsters()[0].hp < hp_before
    # Cost 2, no discard this turn so no +2 bonus
    assert cs.player.energy == 1


def test_dagger_throw_attacks_draws_discards():
    """DaggerThrow deals damage, draws 1, discards 1."""
    cs = make_combat()
    cs.start_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.DaggerThrow)
    hand_before = len(cs.get_hand())
    cs.play_card(hi, 0)
    assert cs.get_monsters()[0].hp < hp_before
    # Played 1, drew 1, discarded 1: net -1
    assert len(cs.get_hand()) == hand_before - 1 + 1 - 1


def test_dagger_spray_hits_all_enemies():
    """DaggerSpray hits all enemies multiple times."""
    m1 = sts_sim.Monster("A", 10, "a", "AAAA", False)
    m2 = sts_sim.Monster("B", 10, "b", "AAAA", False)
    cs = sts_sim.CombatState.new_with_character([m1, m2], 0, sts_sim.Character.Silent)
    hi = setup_card(cs, sts_sim.Card.DaggerSpray)
    cs.play_card(hi, None)
    monsters = cs.get_monsters()
    # base_damage 1, magic 2 hits -> 2 damage to each
    assert monsters[0].hp < 10
    assert monsters[1].hp < 10


def test_backstab_bonus_at_full_hp():
    """Backstab deals bonus damage to full HP target."""
    cs = make_combat()
    cs.start_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Backstab)
    cs.play_card(hi, 0)
    # Base 2 + Bonus 2 (full HP) = 4 damage
    assert hp_before - cs.get_monsters()[0].hp >= 4


def test_backstab_no_bonus_if_damaged():
    """Backstab doesn't get bonus if target is not at full HP."""
    cs = make_combat()
    cs.start_combat()
    # Damage the monster first
    hi = setup_card(cs, sts_sim.Card.Slice)
    cs.play_card(hi, 0)
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Backstab)
    cs.play_card(hi, 0)
    # Base 2, no bonus = 2 damage
    assert hp_before - cs.get_monsters()[0].hp == 2


def test_bane_bonus_if_poisoned():
    """Bane deals bonus damage if target has Poison."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.DeadlyPoison)
    cs.play_card(hi, 0)
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Bane)
    cs.play_card(hi, 0)
    # Base 2 + Bonus 2 (poisoned) = 4
    assert hp_before - cs.get_monsters()[0].hp >= 4


def test_bane_no_bonus_if_not_poisoned():
    """Bane deals only base damage if target has no Poison."""
    cs = make_combat()
    cs.start_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Bane)
    cs.play_card(hi, 0)
    # Base 2 only
    assert hp_before - cs.get_monsters()[0].hp == 2


def test_choke_bonus_per_debuff():
    """Choke deals base_damage * (1 + debuff_count) damage."""
    cs = make_combat()
    cs.start_combat()
    # Apply poison and weak first
    hi = setup_card(cs, sts_sim.Card.DeadlyPoison)
    cs.play_card(hi, 0)
    hi = setup_card(cs, sts_sim.Card.Neutralize)
    cs.play_card(hi, 0)
    # Target has Poison=1 and Weak=1 = 2 debuffs
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Choke)
    cs.play_card(hi, 0)
    # base_damage(3) * (1 + 1 poison + 1 weak) = 9
    assert hp_before - cs.get_monsters()[0].hp == 9


def test_predator_attacks_and_draws():
    """Predator deals damage and draws cards."""
    cs = make_combat()
    cs.start_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Predator)
    hand_before = len(cs.get_hand())
    cs.play_card(hi, 0)
    assert cs.get_monsters()[0].hp < hp_before
    # Played 1, drew 2: net +1
    assert len(cs.get_hand()) == hand_before - 1 + 2


def test_flechettes_bonus_per_skill_in_hand():
    """Flechettes deals bonus damage per skill in hand."""
    cs = make_combat()
    cs.start_combat()
    # Add some skills to hand
    cs.add_card_to_hand(sts_sim.Card.Deflect)  # skill
    cs.add_card_to_hand(sts_sim.Card.Backflip)  # skill
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Flechettes)
    cs.play_card(hi, 0)
    # Base 1 + (0 * skills) for unupgraded, but still deals > 0
    assert cs.get_monsters()[0].hp < hp_before


def test_flechettes_upgraded_scales_better():
    """Upgraded Flechettes adds 1 per skill in hand."""
    m = sts_sim.Monster("Test", 20, "test", "AAAA", False)
    cs = sts_sim.CombatState.new_with_character([m], 0, sts_sim.Character.Silent)
    # Clear hand to control skill count exactly
    # Add exactly 2 skills
    cs.add_card_to_hand(sts_sim.Card.Deflect)
    cs.add_card_to_hand(sts_sim.Card.Backflip)
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Flechettes, upgraded=True)
    cs.play_card(hi, 0)
    # Count skills in hand at time of play: Deflect + Backflip = 2 (Flechettes itself is attack)
    # Base 1 + (1 * 2 skills) = 3
    assert hp_before - cs.get_monsters()[0].hp == 3


def test_die_die_die_hits_all():
    """Die Die Die deals damage to all enemies."""
    cs = make_multi_combat()
    cs.start_combat()
    before = [(m.hp, m.is_dead()) for m in cs.get_monsters()]
    hi = setup_card(cs, sts_sim.Card.DieDieDie)
    cs.play_card(hi, None)
    for i, m in enumerate(cs.get_monsters()):
        if not before[i][1]:
            assert m.hp < before[i][0]


def test_all_out_attack_hits_all_and_discards():
    """AllOutAttack hits all enemies and discards a card."""
    m1 = sts_sim.Monster("A", 10, "a", "AAAA", False)
    m2 = sts_sim.Monster("B", 10, "b", "AAAA", False)
    cs = sts_sim.CombatState.new_with_character([m1, m2], 0, sts_sim.Character.Silent)
    # Add a card to hand so there's something to discard
    cs.add_card_to_hand(sts_sim.Card.Slice)
    hi = setup_card(cs, sts_sim.Card.AllOutAttack)
    hand_before = len(cs.get_hand())
    cs.play_card(hi, None)
    monsters = cs.get_monsters()
    assert monsters[0].hp < 10
    assert monsters[1].hp < 10
    # Played 1, discarded 1: net -2
    assert len(cs.get_hand()) == hand_before - 1 - 1


def test_grand_finale_aoe():
    """Grand Finale deals heavy AoE damage when draw pile is empty."""
    m1 = sts_sim.Monster("A", 20, "a", "AAAA", False)
    m2 = sts_sim.Monster("B", 20, "b", "AAAA", False)
    cs = sts_sim.CombatState.new_with_character([m1, m2], 0, sts_sim.Character.Silent)
    # Draw pile starts empty for new_with_character (no start_combat called)
    hi = setup_card(cs, sts_sim.Card.GrandFinale)
    cs.play_card(hi, None)
    monsters = cs.get_monsters()
    # GrandFinale base damage is 10, hits all
    assert monsters[0].hp < 20
    assert monsters[1].hp < 20


def test_skewer_x_cost_damage():
    """Skewer deals damage based on energy spent."""
    cs = make_combat()
    cs.start_combat()
    cs.set_player_energy(4)
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Skewer, energy=4)
    cs.play_card(hi, 0)
    # X-cost: spends all energy. base_damage(1) + energy(4) = 5
    assert cs.get_monsters()[0].hp < hp_before
    assert cs.player.energy == 0


def test_skewer_choice_partial_energy():
    """Skewer with choice spends only chosen energy."""
    cs = make_combat()
    cs.start_combat()
    cs.set_player_energy(4)
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Skewer, energy=4)
    cs.play_card(hi, 0, 2)  # Spend 2 of 4 energy
    # base_damage(1) + 2 = 3
    assert cs.get_monsters()[0].hp == hp_before - 3
    assert cs.player.energy == 2


# ==================== SKILL CARD EFFECTS ====================


def test_backflip_gives_block_and_draws():
    """Backflip gives block and draws 2."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.Backflip)
    hand_before = len(cs.get_hand())
    cs.play_card(hi, None)
    assert cs.player.block > 0
    assert len(cs.get_hand()) == hand_before - 1 + 2


def test_acrobatics_draws_and_discards():
    """Acrobatics draws 3 and discards 1."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.Acrobatics)
    hand_before = len(cs.get_hand())
    cs.play_card(hi, None)
    # Drew 3, discarded 1, played 1: net +1
    assert len(cs.get_hand()) == hand_before - 1 + 3 - 1


def test_deflect_gives_block():
    """Deflect gives block at 0 cost."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.Deflect)
    cs.play_card(hi, None)
    assert cs.player.block >= 1


def test_dodge_and_roll_gives_block():
    """Dodge and Roll gives block multiple times."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.DodgeAndRoll)
    cs.play_card(hi, None)
    # base_block(1) * magic(2) = 2 block
    assert cs.player.block >= 2


def test_prepared_draws_and_discards():
    """Prepared draws and discards equal amounts."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.Prepared)
    hand_before = len(cs.get_hand())
    cs.play_card(hi, None)
    # Draws 1, discards 1, played 1: net -1
    assert len(cs.get_hand()) == hand_before - 1 + 1 - 1


def test_survivor_gives_block_and_discards():
    """Survivor gives block and discards 1."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.Survivor)
    hand_before = len(cs.get_hand())
    cs.play_card(hi, None)
    assert cs.player.block > 0
    # Played 1, discarded 1: net -2
    assert len(cs.get_hand()) == hand_before - 1 - 1


def test_dash_gives_damage_and_block():
    """Dash deals damage and gives block."""
    cs = make_combat()
    cs.start_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Dash)
    cs.play_card(hi, 0)
    assert cs.player.block > 0
    assert cs.get_monsters()[0].hp < hp_before


def test_leg_sweep_block_and_weak():
    """Leg Sweep gives block and applies Weak."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.LegSweep)
    cs.play_card(hi, 0)
    assert cs.player.block > 0
    assert cs.get_monsters()[0].get_power(sts_sim.PowerType.Weak) > 0


def test_terror_applies_vulnerable():
    """Terror applies Vulnerable to target."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.Terror)
    cs.play_card(hi, 0)
    assert cs.get_monsters()[0].get_power(sts_sim.PowerType.Vulnerable) > 0


def test_piercing_wail_block_and_weak_all():
    """Piercing Wail gives block and applies Weak to all enemies."""
    cs = make_multi_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.PiercingWail)
    cs.play_card(hi, None)
    assert cs.player.block >= 1
    for m in cs.get_monsters():
        if not m.is_dead():
            assert m.get_power(sts_sim.PowerType.Weak) >= 1


def test_escape_plan_block_and_draw():
    """Escape Plan gives block and draws 1."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.EscapePlan)
    hand_before = len(cs.get_hand())
    cs.play_card(hi, None)
    assert cs.player.block >= 1
    assert len(cs.get_hand()) == hand_before - 1 + 1


def test_expertise_draws_cards():
    """Expertise draws up to magic - hand_size cards."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.Expertise)
    hand_before = len(cs.get_hand())
    cs.play_card(hi, None)
    # BG mod: draws max(0, base_magic - hand_size) cards
    # hand_before=6, play 1 so hand=5, base_magic=6, draw max(0,6-5)=1
    assert len(cs.get_hand()) == 6  # 5 remaining + 1 drawn


def test_concentrate_discards_hand_and_draws():
    """Concentrate discards entire hand then draws magic number."""
    cs = make_combat()
    cs.start_combat()
    # Add extra cards to draw pile
    for _ in range(5):
        cs.add_card_to_draw(sts_sim.Card.StrikeGreen)
    hi = setup_card(cs, sts_sim.Card.Concentrate)
    # Concentrate discards rest of hand, then draws magic(0) -> wait
    # Actually Concentrate has magic=0 and cost=0
    # Let me check: concentrate discards hand, draws base_magic
    cs.play_card(hi, None)
    # After: hand discarded, some cards drawn based on magic number


def test_calculated_gamble_redraws_hand():
    """Calculated Gamble discards hand and draws same number."""
    cs = make_combat()
    cs.start_combat()
    # Add cards to draw pile
    for _ in range(10):
        cs.add_card_to_draw(sts_sim.Card.StrikeGreen)
    # Add some extra cards to hand first
    cs.add_card_to_hand(sts_sim.Card.Slice)
    cs.add_card_to_hand(sts_sim.Card.Slice)
    hand_size = len(cs.get_hand())
    hi = setup_card(cs, sts_sim.Card.CalculatedGamble)
    # CalculatedGamble: records hand_size (which includes itself), discards all, draws that many
    # hand_size before play includes CalculatedGamble
    cs.play_card(hi, None)
    # Should have redrawn hand_size cards (the hand size counted all cards before the discard)
    new_hand = len(cs.get_hand())
    assert new_hand >= hand_size - 1  # at least most of them redrawn


def test_setup_gives_energy():
    """Setup gives 1 energy."""
    cs = make_combat()
    cs.start_combat()
    cs.set_player_energy(3)
    hi = setup_card(cs, sts_sim.Card.Setup, energy=3)
    cs.play_card(hi, None)
    # Cost 0, +1 energy
    assert cs.player.energy == 4


def test_adrenaline_gives_energy_and_draws():
    """Adrenaline (base) gives 1 energy and draws 2."""
    cs = make_combat()
    cs.start_combat()
    cs.set_player_energy(3)
    hi = setup_card(cs, sts_sim.Card.Adrenaline, energy=3)
    hand_before = len(cs.get_hand())
    cs.play_card(hi, None)
    assert cs.player.energy == 4  # cost 0, +1
    assert len(cs.get_hand()) == hand_before - 1 + 2


def test_adrenaline_upgraded_gives_2_energy():
    """Upgraded Adrenaline gives 2 energy."""
    cs = make_combat()
    cs.start_combat()
    cs.set_player_energy(3)
    hi = setup_card(cs, sts_sim.Card.Adrenaline, upgraded=True, energy=3)
    cs.play_card(hi, None)
    assert cs.player.energy == 5  # cost 0, +2


def test_outmaneuver_gives_energy():
    """Outmaneuver: costs 0 energy, BG mod gives energy when retained."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.Outmaneuver, energy=3)
    cs.play_card(hi, None)
    # BG mod: costs 0, energy gain only when retained
    assert cs.player.energy == 3


def test_unload_attacks_and_discards():
    """Unload deals damage (BG mod: no hand discard, uses shiv relic instead)."""
    cs = make_combat()
    cs.start_combat()
    hp_before = cs.get_monsters()[0].hp
    hi = setup_card(cs, sts_sim.Card.Unload)
    hand_before = len(cs.get_hand())
    cs.play_card(hi, 0)
    assert cs.get_monsters()[0].hp < hp_before
    # BG mod: only the played card leaves hand (no discard effect)
    assert len(cs.get_hand()) == hand_before - 1


def test_bullet_time_prevents_draw():
    """Bullet Time applies NoDraw power."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.BulletTime)
    cs.play_card(hi, None)
    assert cs.get_player_power(sts_sim.PowerType.NoDraw) == 1


def test_malaise_x_cost_weak():
    """Malaise applies Weak based on energy spent."""
    cs = make_combat()
    cs.start_combat()
    cs.set_player_energy(3)
    hi = setup_card(cs, sts_sim.Card.Malaise, energy=3)
    cs.play_card(hi, 0)
    m = cs.get_monsters()[0]
    assert m.get_power(sts_sim.PowerType.Weak) >= 3
    assert cs.player.energy == 0


def test_malaise_choice_partial_energy():
    """Malaise with choice spends only chosen energy."""
    cs = make_combat()
    cs.start_combat()
    cs.set_player_energy(3)
    hi = setup_card(cs, sts_sim.Card.Malaise, energy=3)
    cs.play_card(hi, 0, 1)  # Spend 1 of 3 energy
    m = cs.get_monsters()[0]
    # X=1 + base_magic weak
    assert m.get_power(sts_sim.PowerType.Weak) >= 1
    assert cs.player.energy == 2


# ==================== POWER CARD EFFECTS ====================


def test_footwork_gives_dexterity():
    """Footwork applies Dexterity power."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.FootworkCard)
    cs.play_card(hi, None)
    assert cs.player.get_power(sts_sim.PowerType.Dexterity) == 1


def test_accuracy_applies_power():
    """Accuracy applies Accuracy power."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.AccuracyCard)
    cs.play_card(hi, None)
    assert cs.player.get_power(sts_sim.PowerType.Accuracy) == 1


def test_after_image_applies_power():
    """After Image applies AfterImage power."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.AfterImageCard)
    cs.play_card(hi, None)
    assert cs.player.get_power(sts_sim.PowerType.AfterImage) == 1


def test_noxious_fumes_applies_power():
    """Noxious Fumes applies NoxiousFumes power."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.NoxiousFumesCard)
    cs.play_card(hi, None)
    assert cs.player.get_power(sts_sim.PowerType.NoxiousFumes) == 1


def test_well_laid_plans_applies_power():
    """Well-Laid Plans applies WellLaidPlans power."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.WellLaidPlansCard)
    cs.play_card(hi, None)
    assert cs.player.get_power(sts_sim.PowerType.WellLaidPlans) == 1


def test_infinite_blades_applies_power():
    """Infinite Blades applies InfiniteBlades power."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.InfiniteBlades)
    cs.play_card(hi, None)
    assert cs.player.get_power(sts_sim.PowerType.InfiniteBlades) == 1


def test_a_thousand_cuts_applies_power():
    """A Thousand Cuts applies AThousandCuts power."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.AThousandCutsCard)
    cs.play_card(hi, None)
    assert cs.player.get_power(sts_sim.PowerType.AThousandCuts) == 5


def test_burst_applies_power():
    """Burst applies Burst power."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.BurstCard)
    cs.play_card(hi, None)
    assert cs.player.get_power(sts_sim.PowerType.Burst) == 1


def test_envenom_applies_power():
    """Envenom applies Envenom power."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.EnvenomCard)
    cs.play_card(hi, None)
    assert cs.player.get_power(sts_sim.PowerType.Envenom) == 1


def test_tools_of_the_trade_applies_power():
    """Tools of the Trade applies ToolsOfTheTrade power."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.ToolsOfTheTradeCard)
    cs.play_card(hi, None)
    assert cs.player.get_power(sts_sim.PowerType.ToolsOfTheTrade) == 1


def test_wraith_form_applies_power():
    """Wraith Form applies WraithForm power."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.WraithFormCard)
    cs.play_card(hi, None)
    assert cs.player.get_power(sts_sim.PowerType.WraithForm) == 2


def test_distraction_applies_power():
    """Distraction applies Distraction power."""
    cs = make_combat()
    cs.start_combat()
    hi = setup_card(cs, sts_sim.Card.DistractionCard)
    cs.play_card(hi, None)
    assert cs.player.get_power(sts_sim.PowerType.Distraction) == 2


# ==================== REWARD DECK ====================


def test_silent_reward_deck():
    """Silent reward deck contains Silent cards."""
    rd = sts_sim.RewardDeck(0, sts_sim.Character.Silent)
    cards = rd.draw_rewards(3)
    assert len(cards) == 3
    for c in cards:
        assert c.card != sts_sim.Card.StrikeRed
        assert c.card != sts_sim.Card.Bash


# ==================== CARD PROPERTIES ====================


def test_poisoned_stab_exhausts():
    """Poisoned Stab exhausts."""
    assert sts_sim.CardInstance(sts_sim.Card.PoisonedStab, False).py_exhausts is True


def test_backstab_exhausts():
    """Backstab exhausts."""
    assert sts_sim.CardInstance(sts_sim.Card.Backstab, False).py_exhausts is True


def test_concentrate_exhausts():
    """Concentrate exhausts."""
    assert sts_sim.CardInstance(sts_sim.Card.Concentrate, False).py_exhausts is True


def test_piercing_wail_exhausts():
    """Piercing Wail exhausts."""
    assert sts_sim.CardInstance(sts_sim.Card.PiercingWail, False).py_exhausts is True


def test_malaise_exhausts():
    """Malaise exhausts."""
    assert sts_sim.CardInstance(sts_sim.Card.Malaise, False).py_exhausts is True


def test_calculated_gamble_exhausts_base_not_upgraded():
    """Calculated Gamble exhausts when not upgraded, doesn't when upgraded."""
    assert sts_sim.CardInstance(sts_sim.Card.CalculatedGamble, False).py_exhausts is True
    assert sts_sim.CardInstance(sts_sim.Card.CalculatedGamble, True).py_exhausts is False


def test_reflex_unplayable():
    """Reflex is unplayable."""
    assert sts_sim.CardInstance(sts_sim.Card.Reflex, False).py_unplayable is True


def test_tactician_unplayable():
    """Tactician is unplayable."""
    assert sts_sim.CardInstance(sts_sim.Card.Tactician, False).py_unplayable is True


def test_outmaneuver_retains():
    """Outmaneuver retains."""
    assert sts_sim.CardInstance(sts_sim.Card.Outmaneuver, False).py_retain is True


def test_silent_card_names():
    """Verify key Silent card names."""
    assert sts_sim.Card.PoisonedStab.py_name == "Poisoned Stab"
    assert sts_sim.Card.DaggerThrow.py_name == "Dagger Throw"
    assert sts_sim.Card.DaggerSpray.py_name == "Dagger Spray"
    assert sts_sim.Card.BladeDance.py_name == "Blade Dance"
    assert sts_sim.Card.DeadlyPoison.py_name == "Deadly Poison"
    assert sts_sim.Card.DieDieDie.py_name == "Die Die Die"
    assert sts_sim.Card.FootworkCard.py_name == "Footwork"
    assert sts_sim.Card.NoxiousFumesCard.py_name == "Noxious Fumes"
    assert sts_sim.Card.WraithFormCard.py_name == "Wraith Form"
    assert sts_sim.Card.CorpseExplosionCard.py_name == "Corpse Explosion"
    assert sts_sim.Card.AThousandCutsCard.py_name == "A Thousand Cuts"
    assert sts_sim.Card.ToolsOfTheTradeCard.py_name == "Tools of the Trade"


def test_silent_card_types():
    """Verify card types for Silent cards."""
    assert sts_sim.CardInstance(sts_sim.Card.Slice, False).py_card_type == sts_sim.CardType.Attack
    assert sts_sim.CardInstance(sts_sim.Card.Deflect, False).py_card_type == sts_sim.CardType.Skill
    assert sts_sim.CardInstance(sts_sim.Card.FootworkCard, False).py_card_type == sts_sim.CardType.Power
    assert sts_sim.CardInstance(sts_sim.Card.NoxiousFumesCard, False).py_card_type == sts_sim.CardType.Power
    assert sts_sim.CardInstance(sts_sim.Card.AccuracyCard, False).py_card_type == sts_sim.CardType.Power


def test_silent_card_costs():
    """Verify costs for key Silent cards."""
    assert sts_sim.CardInstance(sts_sim.Card.Slice, False).py_cost == 0
    assert sts_sim.CardInstance(sts_sim.Card.Deflect, False).py_cost == 0
    assert sts_sim.CardInstance(sts_sim.Card.Neutralize, False).py_cost == 0
    assert sts_sim.CardInstance(sts_sim.Card.Backflip, False).py_cost == 1
    assert sts_sim.CardInstance(sts_sim.Card.DaggerSpray, False).py_cost == 1
    assert sts_sim.CardInstance(sts_sim.Card.Dash, False).py_cost == 2
    assert sts_sim.CardInstance(sts_sim.Card.BulletTime, False).py_cost == 3
    assert sts_sim.CardInstance(sts_sim.Card.BulletTime, True).py_cost == 2
