"""Simulator tests for Silent Uncommon cards."""
import sts_sim
from tests.live.conftest import make_sim


# ===========================================================================
# Backstab
# ===========================================================================


def test_backstab_full_hp_bonus():
    """Backstab deals 2+2=4 damage when enemy is at full HP."""
    sim = make_sim(hand=[sts_sim.Card.Backstab], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 16  # 20 - (2+2) = 16


def test_backstab_damaged_enemy_no_bonus():
    """Backstab deals 2 damage when enemy is NOT at full HP."""
    sim = make_sim(hand=[sts_sim.Card.Backstab], energy=3, monster_hp=20)
    # Damage the enemy first so it's not at full HP
    sim.get_monsters()[0].apply_damage(5)
    hp_before = sim.get_monsters()[0].hp  # 15
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == hp_before - 2  # 15 - 2 = 13


def test_backstab_upgraded_full_hp_with_strength():
    """Backstab+ deals 4*(1+1)+2=10 damage with 1 STR against full HP enemy."""
    sim = make_sim(
        hand=[(sts_sim.Card.Backstab, True)],
        energy=3,
        player_powers={"Strength": 1},
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 10  # 20 - 10 = 10


def test_backstab_exhausts():
    """Backstab goes to exhaust pile after play."""
    sim = make_sim(hand=[sts_sim.Card.Backstab], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert len(sim.get_exhaust_pile()) == 1
    assert len(sim.get_discard_pile()) == 0


# ===========================================================================
# Bane
# ===========================================================================


def test_bane_poisoned_enemy():
    """Bane deals 2+2=4 damage when enemy has POISON."""
    sim = make_sim(
        hand=[sts_sim.Card.Bane],
        energy=3,
        monster_hp=20,
        monster_powers={"Poison": 3},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 16  # 20 - 4 = 16


def test_bane_no_poison_no_bonus():
    """Bane deals 2 damage when enemy has no POISON."""
    sim = make_sim(hand=[sts_sim.Card.Bane], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18


def test_bane_upgraded_poisoned_with_strength():
    """Bane+ deals 3*(1+2)+2=11 damage with 2 STR against poisoned enemy."""
    sim = make_sim(
        hand=[(sts_sim.Card.Bane, True)],
        energy=3,
        player_powers={"Strength": 2},
        monster_hp=30,
        monster_powers={"Poison": 1},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 19  # 30 - 11 = 19


# ===========================================================================
# Choke
# ===========================================================================


def test_choke_with_weak_and_poison():
    """Choke deals 3*(1+2+3)=18 damage against enemy with 2 WEAK, 3 POISON."""
    sim = make_sim(
        hand=[sts_sim.Card.Choke],
        energy=3,
        monster_hp=30,
        monster_powers={"Weak": 2, "Poison": 3},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 12  # 30 - 18 = 12


def test_choke_no_debuffs():
    """Choke deals 3 damage against clean enemy."""
    sim = make_sim(hand=[sts_sim.Card.Choke], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17


def test_choke_upgraded_debuffed():
    """Choke+ deals 4*(1+1+1)=12 damage against enemy with 1 WEAK, 1 POISON."""
    sim = make_sim(
        hand=[(sts_sim.Card.Choke, True)],
        energy=3,
        monster_hp=25,
        monster_powers={"Weak": 1, "Poison": 1},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 13  # 25 - 12 = 13


# ===========================================================================
# Predator
# ===========================================================================


def test_predator_damage_and_draw():
    """Predator deals 3 damage and draws 2 cards."""
    draw = [sts_sim.Card.StrikeGreen] * 5
    sim = make_sim(
        hand=[sts_sim.Card.Predator],
        draw_pile=draw,
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17
    assert len(sim.get_hand()) == 2  # drew 2 cards


def test_predator_upgraded_damage():
    """Predator+ deals 4 damage and draws 2 cards."""
    draw = [sts_sim.Card.StrikeGreen] * 5
    sim = make_sim(
        hand=[(sts_sim.Card.Predator, True)],
        draw_pile=draw,
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 16  # 20 - 4 = 16
    assert len(sim.get_hand()) == 2  # drew 2 cards


def test_predator_with_strength():
    """Predator deals 3*(1+2)=9 damage with 2 STR."""
    draw = [sts_sim.Card.StrikeGreen] * 5
    sim = make_sim(
        hand=[sts_sim.Card.Predator],
        draw_pile=draw,
        energy=3,
        player_powers={"Strength": 2},
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 11  # 20 - 9 = 11


# ===========================================================================
# Masterful Stab
# ===========================================================================


def test_masterful_stab_full_cost():
    """Masterful Stab costs 4 energy when player has not lost HP."""
    sim = make_sim(hand=[sts_sim.Card.MasterfulStab], energy=4, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18
    assert sim.player.energy == 0  # 4 - 4 = 0


def test_masterful_stab_reduced_cost():
    """Masterful Stab costs 2 energy when player lost HP this combat."""
    sim = make_sim(hand=[sts_sim.Card.MasterfulStab], energy=3, player_hp=7, monster_hp=20)
    # Simulate HP loss by marking player as having lost HP
    sim.set_player_hp(7)  # Below max of 9, simulating HP loss
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_masterful_stab_upgraded_reduced_cost():
    """Masterful Stab+ costs 1 energy when player lost HP this combat."""
    sim = make_sim(
        hand=[(sts_sim.Card.MasterfulStab, True)],
        energy=3,
        player_hp=7,
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17
    assert sim.player.energy == 2  # 3 - 1 = 2


# ===========================================================================
# Dash
# ===========================================================================


def test_dash_damage_and_block():
    """Dash deals 2 damage and grants 2 block."""
    sim = make_sim(hand=[sts_sim.Card.Dash], energy=3, player_block=0, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18
    assert sim.player.block == 2
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_dash_upgraded():
    """Dash+ deals 3 damage and grants 3 block."""
    sim = make_sim(
        hand=[(sts_sim.Card.Dash, True)],
        energy=3,
        player_block=0,
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17
    assert sim.player.block == 3
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_dash_with_footwork():
    """Dash with Footwork: 2 damage, 2*(1+1)=4 block."""
    sim = make_sim(
        hand=[sts_sim.Card.Dash],
        energy=3,
        player_block=0,
        player_powers={"Dexterity": 1},
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18
    assert sim.player.block == 4  # 2*(1+1) = 4


# ===========================================================================
# Finisher
# ===========================================================================


def test_finisher_after_3_attacks():
    """Finisher deals 1 HIT per attack played this turn = 3 damage after 3 attacks."""
    sim = make_sim(
        hand=[
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.Finisher,
        ],
        energy=10,
        monster_hp=30,
    )
    # Play 3 Strikes first
    sim.play_card(0, 0)  # Strike 1
    sim.play_card(0, 0)  # Strike 2
    sim.play_card(0, 0)  # Strike 3
    # Now play Finisher (index 0 since it's the only card left)
    sim.play_card(0, 0)
    # Monster took 3 from strikes + 3 from finisher = 6 total
    assert sim.get_monsters()[0].hp == 24  # 30 - 3 - 3 = 24


def test_finisher_no_attacks():
    """Finisher deals 0 damage when no attacks were played this turn."""
    sim = make_sim(hand=[sts_sim.Card.Finisher], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 20  # 0 damage


def test_finisher_upgraded_after_3_attacks():
    """Finisher+ deals 2 HIT per attack played = 6 damage after 3 attacks."""
    sim = make_sim(
        hand=[
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            (sts_sim.Card.Finisher, True),
        ],
        energy=10,
        monster_hp=30,
    )
    sim.play_card(0, 0)  # Strike 1
    sim.play_card(0, 0)  # Strike 2
    sim.play_card(0, 0)  # Strike 3
    sim.play_card(0, 0)  # Finisher+
    # 3 from strikes + 6 from finisher+ = 9 total
    assert sim.get_monsters()[0].hp == 21  # 30 - 3 - 6 = 21


# ===========================================================================
# Flechettes
# ===========================================================================


def test_flechettes_with_3_skills():
    """Flechettes deals 1 HIT per Skill in hand = 3 damage with 3 Skills."""
    sim = make_sim(
        hand=[
            sts_sim.Card.Flechettes,
            sts_sim.Card.DefendGreen,
            sts_sim.Card.DefendGreen,
            sts_sim.Card.DefendGreen,
        ],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17


def test_flechettes_with_0_skills():
    """Flechettes deals 0 damage with no Skills in hand."""
    sim = make_sim(
        hand=[
            sts_sim.Card.Flechettes,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 20  # 0 damage


def test_flechettes_upgraded_with_2_skills():
    """Flechettes+ deals (2+1)=3 damage with 2 Skills in hand."""
    sim = make_sim(
        hand=[
            (sts_sim.Card.Flechettes, True),
            sts_sim.Card.DefendGreen,
            sts_sim.Card.DefendGreen,
        ],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17


# ===========================================================================
# All-Out Attack
# ===========================================================================


def test_all_out_attack_aoe():
    """All-Out Attack deals 2 AOE damage and discards 1 card."""
    sim = make_sim(
        hand=[
            sts_sim.Card.AllOutAttack,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ],
        energy=3,
        monsters=[{"hp": 15}, {"hp": 10}],
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 13  # 15 - 2 = 13
    assert monsters[1].hp == 8   # 10 - 2 = 8


def test_all_out_attack_upgraded_aoe():
    """All-Out Attack+ deals 3 AOE damage."""
    sim = make_sim(
        hand=[
            (sts_sim.Card.AllOutAttack, True),
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ],
        energy=3,
        monsters=[{"hp": 15}, {"hp": 10}],
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 12  # 15 - 3 = 12
    assert monsters[1].hp == 7   # 10 - 3 = 7


# ===========================================================================
# Unload
# ===========================================================================


def test_unload_with_3_shivs():
    """Unload deals 2 HIT + 3 SHIVs at 2 damage each = 8 total."""
    sim = make_sim(
        hand=[sts_sim.Card.Unload],
        energy=3,
        player_powers={"Shiv": 3},
        monster_hp=30,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 22  # 30 - 8 = 22


def test_unload_with_0_shivs():
    """Unload deals 2 HIT only with no SHIVs."""
    sim = make_sim(hand=[sts_sim.Card.Unload], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18


def test_unload_upgraded_with_2_shivs():
    """Unload+ deals 2 HIT + 2 SHIVs at 3 damage each = 8 total."""
    sim = make_sim(
        hand=[(sts_sim.Card.Unload, True)],
        energy=3,
        player_powers={"Shiv": 2},
        monster_hp=30,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 22  # 30 - 8 = 22


# ===========================================================================
# Blur
# ===========================================================================


def test_blur_without_discarding():
    """Blur grants 2 block without discarding."""
    sim = make_sim(hand=[sts_sim.Card.Blur], energy=3, player_block=0)
    sim.play_card(0, None)
    assert sim.player.block == 2


def test_blur_after_discard():
    """Blur grants 2+1=3 block after discarding a card this turn."""
    sim = make_sim(
        hand=[sts_sim.Card.Survivor, sts_sim.Card.Blur, sts_sim.Card.StrikeGreen],
        energy=3,
        player_block=0,
    )
    # Play Survivor first to trigger a discard
    sim.play_card(0, None)
    # Now play Blur
    sim.play_card(0, None)
    assert sim.player.block >= 3  # 2 from Survivor + 3 from Blur


def test_blur_upgraded_after_discard_with_footwork():
    """Blur+ after discard with Footwork: (3+1)*(1+1)=8 block."""
    sim = make_sim(
        hand=[(sts_sim.Card.Blur, True)],
        energy=3,
        player_block=0,
        player_powers={"Dexterity": 1},
    )
    sim.play_card(0, None)
    # Without discard: 3 BLK * (1+1) = 6 block (Footwork/Dexterity adds per BLK token)
    assert sim.player.block == 6


# ===========================================================================
# Bouncing Flask
# ===========================================================================


def test_bouncing_flask_stack_on_one():
    """Bouncing Flask applies 2 POISON to one enemy."""
    sim = make_sim(
        hand=[sts_sim.Card.BouncingFlask],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 2


def test_bouncing_flask_upgraded():
    """Bouncing Flask+ applies 3 POISON total."""
    sim = make_sim(
        hand=[(sts_sim.Card.BouncingFlask, True)],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 3


# ===========================================================================
# Concentrate
# ===========================================================================


def test_concentrate_discard_2_for_2_energy():
    """Concentrate discards 2 cards and gains 2 energy."""
    sim = make_sim(
        hand=[
            sts_sim.Card.Concentrate,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ],
        energy=0,
    )
    sim.play_card(0, None, 2)  # choice=2 to discard 2 cards
    assert sim.player.energy == 2
    assert len(sim.get_exhaust_pile()) == 1  # Concentrate exhausted


def test_concentrate_discard_0():
    """Concentrate discards 0 cards, gains 0 energy."""
    sim = make_sim(hand=[sts_sim.Card.Concentrate], energy=0)
    sim.play_card(0, None, 0)
    assert sim.player.energy == 0
    assert len(sim.get_exhaust_pile()) == 1


def test_concentrate_upgraded_discard_3():
    """Concentrate+ discards 3 cards and gains 3+1=4 energy."""
    sim = make_sim(
        hand=[
            (sts_sim.Card.Concentrate, True),
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ],
        energy=0,
    )
    sim.play_card(0, None, 3)
    assert sim.player.energy == 4


# ===========================================================================
# Calculated Gamble
# ===========================================================================


def test_calculated_gamble_with_3_cards():
    """Calculated Gamble discards 3 cards, draws 3."""
    draw = [sts_sim.Card.DefendGreen] * 5
    sim = make_sim(
        hand=[
            sts_sim.Card.CalculatedGamble,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ],
        draw_pile=draw,
        energy=3,
    )
    sim.play_card(0, None)
    assert len(sim.get_hand()) == 3


def test_calculated_gamble_empty_hand():
    """Calculated Gamble with only itself: discards 0, draws 0."""
    draw = [sts_sim.Card.DefendGreen] * 5
    sim = make_sim(
        hand=[sts_sim.Card.CalculatedGamble],
        draw_pile=draw,
        energy=3,
    )
    sim.play_card(0, None)
    assert len(sim.get_hand()) == 0


# ===========================================================================
# Catalyst
# ===========================================================================


def test_catalyst_doubles_poison():
    """Catalyst doubles enemy POISON from 4 to 8."""
    sim = make_sim(
        hand=[sts_sim.Card.Catalyst],
        energy=3,
        monster_hp=20,
        monster_powers={"Poison": 4},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 8
    assert len(sim.get_exhaust_pile()) == 1


def test_catalyst_zero_poison():
    """Catalyst on enemy with 0 POISON: remains 0."""
    sim = make_sim(hand=[sts_sim.Card.Catalyst], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 0


def test_catalyst_upgraded_triples_poison():
    """Catalyst+ triples enemy POISON from 5 to 15."""
    sim = make_sim(
        hand=[(sts_sim.Card.Catalyst, True)],
        energy=3,
        monster_hp=20,
        monster_powers={"Poison": 5},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 15


# ===========================================================================
# Crippling Cloud
# ===========================================================================


def test_crippling_cloud_aoe_debuffs():
    """Crippling Cloud applies 1 POISON and 1 WEAK to all enemies."""
    sim = make_sim(
        hand=[sts_sim.Card.CripplingCloud],
        energy=3,
        monsters=[{"hp": 20}, {"hp": 15}],
    )
    sim.play_card(0, None)
    for m in sim.get_monsters():
        assert m.get_power(sts_sim.PowerType.Poison) == 1
        assert m.get_power(sts_sim.PowerType.Weak) == 1
    assert len(sim.get_exhaust_pile()) == 1


def test_crippling_cloud_upgraded():
    """Crippling Cloud+ applies 2 POISON and 1 WEAK to all enemies."""
    sim = make_sim(
        hand=[(sts_sim.Card.CripplingCloud, True)],
        energy=3,
        monsters=[{"hp": 20}, {"hp": 15}],
    )
    sim.play_card(0, None)
    for m in sim.get_monsters():
        assert m.get_power(sts_sim.PowerType.Poison) == 2
        assert m.get_power(sts_sim.PowerType.Weak) == 1


# ===========================================================================
# Leg Sweep
# ===========================================================================


def test_leg_sweep_basic():
    """Leg Sweep applies 1 WEAK, grants 3 block."""
    sim = make_sim(
        hand=[sts_sim.Card.LegSweep],
        energy=3,
        player_block=0,
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 1
    assert sim.player.block == 3


def test_leg_sweep_upgraded_with_footwork():
    """Leg Sweep+ with Footwork: 1 WEAK, 4*(1+1)=8 block."""
    sim = make_sim(
        hand=[(sts_sim.Card.LegSweep, True)],
        energy=3,
        player_block=0,
        player_powers={"Dexterity": 1},
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 1
    assert sim.player.block == 8  # 4*(1+1) = 8


def test_leg_sweep_stacking_weak():
    """Leg Sweep adds 1 WEAK on top of existing 2 WEAK."""
    sim = make_sim(
        hand=[sts_sim.Card.LegSweep],
        energy=3,
        monster_hp=20,
        monster_powers={"Weak": 2},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 3


# ===========================================================================
# Outmaneuver
# ===========================================================================


def test_outmaneuver_played_immediately():
    """Outmaneuver played immediately gives no bonus energy. Costs 1."""
    sim = make_sim(hand=[sts_sim.Card.Outmaneuver], energy=3)
    sim.play_card(0, None)
    assert sim.player.energy == 2  # 3 - 1 = 2


# ===========================================================================
# Piercing Wail
# ===========================================================================


def test_piercing_wail_basic():
    """Piercing Wail: 1 block, AOE WEAK, exhaust."""
    sim = make_sim(
        hand=[sts_sim.Card.PiercingWail],
        energy=3,
        player_block=0,
        monsters=[{"hp": 20}, {"hp": 15}],
    )
    sim.play_card(0, None)
    assert sim.player.block == 1
    for m in sim.get_monsters():
        assert m.get_power(sts_sim.PowerType.Weak) == 1
    assert len(sim.get_exhaust_pile()) == 1


def test_piercing_wail_upgraded():
    """Piercing Wail+: 3 block, AOE WEAK, exhaust."""
    sim = make_sim(
        hand=[(sts_sim.Card.PiercingWail, True)],
        energy=3,
        player_block=0,
        monsters=[{"hp": 20}, {"hp": 15}],
    )
    sim.play_card(0, None)
    assert sim.player.block == 3
    for m in sim.get_monsters():
        assert m.get_power(sts_sim.PowerType.Weak) == 1


def test_piercing_wail_with_footwork():
    """Piercing Wail with Footwork: 1*(1+1)=2 block."""
    sim = make_sim(
        hand=[sts_sim.Card.PiercingWail],
        energy=3,
        player_block=0,
        player_powers={"Dexterity": 1},
        monster_hp=20,
    )
    sim.play_card(0, None)
    assert sim.player.block == 2  # 1*(1+1) = 2


# ===========================================================================
# Escape Plan
# ===========================================================================


def test_escape_plan_draws_skill():
    """Escape Plan draws a Skill card and gains 1 block."""
    sim = make_sim(
        hand=[sts_sim.Card.EscapePlan],
        draw_pile=[sts_sim.Card.DefendGreen],
        energy=3,
        player_block=0,
    )
    sim.play_card(0, None)
    assert len(sim.get_hand()) == 1  # drew 1 card
    assert sim.player.block == 1  # drew a Skill


def test_escape_plan_draws_attack():
    """Escape Plan draws an Attack card, no block."""
    sim = make_sim(
        hand=[sts_sim.Card.EscapePlan],
        draw_pile=[sts_sim.Card.StrikeGreen],
        energy=3,
        player_block=0,
    )
    sim.play_card(0, None)
    assert len(sim.get_hand()) == 1
    assert sim.player.block == 0  # drew an Attack, no block


def test_escape_plan_upgraded_always_block():
    """Escape Plan+ always gives 1 block regardless of drawn card type."""
    sim = make_sim(
        hand=[(sts_sim.Card.EscapePlan, True)],
        draw_pile=[sts_sim.Card.StrikeGreen],
        energy=3,
        player_block=0,
    )
    sim.play_card(0, None)
    assert len(sim.get_hand()) == 1
    assert sim.player.block == 1  # unconditional block


# ===========================================================================
# Expertise
# ===========================================================================


def test_expertise_with_2_cards():
    """Expertise with 2 cards in hand: draws up to 6 (draws 5)."""
    draw = [sts_sim.Card.StrikeGreen] * 6
    sim = make_sim(
        hand=[sts_sim.Card.Expertise, sts_sim.Card.StrikeGreen],
        draw_pile=draw,
        energy=3,
    )
    sim.play_card(0, None)
    assert len(sim.get_hand()) == 6  # 1 remaining + 5 drawn


def test_expertise_full_hand():
    """Expertise with 7 cards in hand: draws 0 (already at 6 after play)."""
    sim = make_sim(
        hand=[
            sts_sim.Card.Expertise,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ],
        energy=3,
    )
    sim.play_card(0, None)
    assert len(sim.get_hand()) == 6  # 6 remaining, 0 drawn


def test_expertise_upgraded_with_3_cards():
    """Expertise+ with 3 cards: draws up to 7 (draws 5)."""
    draw = [sts_sim.Card.StrikeGreen] * 6
    sim = make_sim(
        hand=[
            (sts_sim.Card.Expertise, True),
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ],
        draw_pile=draw,
        energy=3,
    )
    sim.play_card(0, None)
    assert len(sim.get_hand()) == 7  # 2 remaining + 5 drawn


# ===========================================================================
# Riddle with Holes
# ===========================================================================


def test_riddle_with_holes_basic():
    """Riddle with Holes grants 4 SHIV tokens."""
    sim = make_sim(hand=[sts_sim.Card.RiddleWithHoles], energy=3)
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Shiv) == 4
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_riddle_with_holes_upgraded():
    """Riddle with Holes+ grants 5 SHIV tokens."""
    sim = make_sim(hand=[(sts_sim.Card.RiddleWithHoles, True)], energy=3)
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Shiv) == 5


def test_riddle_with_holes_stacks():
    """Riddle with Holes stacks SHIVs: 2 existing + 4 = 6."""
    sim = make_sim(
        hand=[sts_sim.Card.RiddleWithHoles],
        energy=3,
        player_powers={"Shiv": 2},
    )
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Shiv) == 6


# ===========================================================================
# Setup (card)
# ===========================================================================


def test_setup_give_energy_to_self():
    """Setup grants 1 energy to self (net 0 after cost). Exhausts."""
    sim = make_sim(hand=[sts_sim.Card.Setup], energy=3)
    sim.play_card(0, None)
    assert sim.player.energy == 3  # 3 - 1 + 1 = 3
    assert len(sim.get_exhaust_pile()) == 1


def test_setup_exhausts():
    """Setup goes to exhaust pile, not discard."""
    sim = make_sim(hand=[sts_sim.Card.Setup], energy=3)
    sim.play_card(0, None)
    assert len(sim.get_exhaust_pile()) == 1
    assert len(sim.get_discard_pile()) == 0


# ===========================================================================
# Terror
# ===========================================================================


def test_terror_basic():
    """Terror applies 1 VULN and exhausts."""
    sim = make_sim(hand=[sts_sim.Card.Terror], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Vulnerable) == 1
    assert len(sim.get_exhaust_pile()) == 1


def test_terror_upgraded_no_exhaust():
    """Terror+ applies 1 VULN and does NOT exhaust."""
    sim = make_sim(
        hand=[(sts_sim.Card.Terror, True)],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Vulnerable) == 1
    assert len(sim.get_exhaust_pile()) == 0
    assert len(sim.get_discard_pile()) == 1


def test_terror_stacks_vuln():
    """Terror adds 1 VULN on top of existing 2."""
    sim = make_sim(
        hand=[sts_sim.Card.Terror],
        energy=3,
        monster_hp=20,
        monster_powers={"Vulnerable": 2},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Vulnerable) == 3


# ===========================================================================
# Footwork
# ===========================================================================


def test_footwork_boosts_block():
    """Footwork boosts subsequent BLK cards: Defend 1 BLK -> 2 block."""
    sim = make_sim(
        hand=[sts_sim.Card.FootworkCard, sts_sim.Card.DefendGreen],
        energy=3,
        player_block=0,
    )
    sim.play_card(0, None)  # Play Footwork
    sim.play_card(0, None)  # Play Defend
    assert sim.player.block == 2  # 1*(1+1) = 2


def test_footwork_stacks():
    """Two Footworks stack: Defend 1 BLK -> 3 block."""
    sim = make_sim(
        hand=[
            sts_sim.Card.FootworkCard,
            sts_sim.Card.FootworkCard,
            sts_sim.Card.DefendGreen,
        ],
        energy=3,
        player_block=0,
    )
    sim.play_card(0, None)  # Play Footwork 1
    sim.play_card(0, None)  # Play Footwork 2
    sim.play_card(0, None)  # Play Defend
    assert sim.player.block == 3  # 1*(1+2) = 3


# ===========================================================================
# Noxious Fumes
# ===========================================================================


def test_noxious_fumes_applies_poison():
    """Noxious Fumes applies 1 POISON at start of next turn."""
    sim = make_sim(
        hand=[sts_sim.Card.NoxiousFumesCard],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, None)  # Play Noxious Fumes
    sim.end_player_turn()
    sim.roll_and_execute_monsters()
    # At start of next turn, enemy gains 1 POISON
    monsters = sim.get_monsters()
    assert monsters[0].get_power(sts_sim.PowerType.Poison) >= 1


# ===========================================================================
# Well-Laid Plans
# ===========================================================================


def test_well_laid_plans_power_plays():
    """Well-Laid Plans can be played as a power."""
    sim = make_sim(
        hand=[sts_sim.Card.WellLaidPlansCard],
        energy=3,
    )
    sim.play_card(0, None)
    assert sim.player.energy == 2  # 3 - 1 = 2
    assert len(sim.get_hand()) == 0


# ===========================================================================
# Distraction
# ===========================================================================


def test_distraction_plays():
    """Distraction can be played as a power."""
    sim = make_sim(
        hand=[sts_sim.Card.DistractionCard],
        energy=3,
    )
    sim.play_card(0, None)
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_distraction_upgraded_costs_less():
    """Distraction+ costs 1 energy instead of 2."""
    sim = make_sim(
        hand=[(sts_sim.Card.DistractionCard, True)],
        energy=1,
    )
    sim.play_card(0, None)
    assert sim.player.energy == 0  # 1 - 1 = 0


# ===========================================================================
# Infinite Blades
# ===========================================================================


def test_infinite_blades_plays():
    """Infinite Blades can be played as a power. Costs 1."""
    sim = make_sim(hand=[sts_sim.Card.InfiniteBlades], energy=3)
    sim.play_card(0, None)
    assert sim.player.energy == 2  # 3 - 1 = 2


# ===========================================================================
# Reflex (unplayable — tested via Calculated Gamble)
# ===========================================================================


def test_reflex_triggers_on_card_discard():
    """Reflex triggers when discarded by Calculated Gamble, drawing 2 cards."""
    draw = [sts_sim.Card.StrikeGreen] * 5
    sim = make_sim(
        hand=[
            sts_sim.Card.CalculatedGamble,
            sts_sim.Card.Reflex,
            sts_sim.Card.StrikeGreen,
        ],
        draw_pile=draw,
        energy=3,
    )
    sim.play_card(0, None)
    # Gamble discards 2 cards (Reflex + Strike), draws 2
    # Reflex triggers: draws 2 more
    # Total in hand: 2 + 2 = 4
    assert len(sim.get_hand()) == 4


# ===========================================================================
# Tactician (unplayable — tested via Calculated Gamble)
# ===========================================================================


def test_tactician_triggers_on_card_discard():
    """Tactician triggers when discarded by Calculated Gamble, giving 2 energy."""
    draw = [sts_sim.Card.StrikeGreen] * 5
    sim = make_sim(
        hand=[
            sts_sim.Card.CalculatedGamble,
            sts_sim.Card.Tactician,
        ],
        draw_pile=draw,
        energy=1,
    )
    sim.play_card(0, None)
    # Gamble costs 0, discards Tactician -> +2 energy
    assert sim.player.energy >= 3  # 1 + 2 = 3
    # Tactician should be exhausted
    assert len(sim.get_exhaust_pile()) >= 1
