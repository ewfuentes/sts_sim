"""Simulator tests for Ironclad Uncommon cards."""
import sts_sim
from tests.live.conftest import make_sim


# ── Uppercut ─────────────────────────────────────────────────────────────

def test_uppercut_base():
    """Uppercut deals 3 damage and applies VULN and WEAK."""
    sim = make_sim(hand=[sts_sim.Card.Uppercut], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Vulnerable) == 1
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 1
    assert sim.player.energy == 1


def test_uppercut_with_strength():
    """Uppercut with 2 STR deals 5 damage (3 base + 2 STR)."""
    sim = make_sim(
        hand=[sts_sim.Card.Uppercut], energy=3, monster_hp=20,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 15  # 20 - 5
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Vulnerable) == 1
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 1


def test_uppercut_upgraded():
    """Upgraded Uppercut applies 2 VULN and 1 WEAK."""
    sim = make_sim(hand=[(sts_sim.Card.Uppercut, True)], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Vulnerable) == 2
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 1


# ── Entrench ─────────────────────────────────────────────────────────────

def test_entrench_doubles_block():
    """Entrench doubles existing block and exhausts."""
    sim = make_sim(hand=[sts_sim.Card.Entrench], energy=3, player_block=4, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 8
    assert len(sim.get_exhaust_pile()) == 1


def test_entrench_block_cap():
    """Entrench respects 20 BLK cap."""
    sim = make_sim(hand=[sts_sim.Card.Entrench], energy=3, player_block=12, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 20
    assert len(sim.get_exhaust_pile()) == 1


def test_entrench_zero_block():
    """Entrench with zero block does nothing."""
    sim = make_sim(hand=[sts_sim.Card.Entrench], energy=3, player_block=0, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 0
    assert len(sim.get_exhaust_pile()) == 1


def test_entrench_upgraded_no_exhaust():
    """Upgraded Entrench does not exhaust."""
    sim = make_sim(hand=[(sts_sim.Card.Entrench, True)], energy=3, player_block=5, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 10
    assert len(sim.get_exhaust_pile()) == 0
    assert len(sim.get_discard_pile()) == 1


# ── Shockwave ────────────────────────────────────────────────────────────

def test_shockwave_base():
    """Shockwave applies 1 VULN and 1 WEAK to all enemies and exhausts."""
    sim = make_sim(
        hand=[sts_sim.Card.Shockwave], energy=3,
        monsters=[{"hp": 20}, {"hp": 20}],
    )
    sim.play_card(0, None)
    for m in sim.get_monsters():
        assert m.get_power(sts_sim.PowerType.Vulnerable) == 1
        assert m.get_power(sts_sim.PowerType.Weak) == 1
    assert len(sim.get_exhaust_pile()) == 1


def test_shockwave_upgraded():
    """Upgraded Shockwave applies 1 VULN and 2 WEAK to all enemies."""
    sim = make_sim(
        hand=[(sts_sim.Card.Shockwave, True)], energy=3,
        monsters=[{"hp": 20}, {"hp": 20}],
    )
    sim.play_card(0, None)
    for m in sim.get_monsters():
        assert m.get_power(sts_sim.PowerType.Vulnerable) == 1
        assert m.get_power(sts_sim.PowerType.Weak) == 2
    assert len(sim.get_exhaust_pile()) == 1


def test_shockwave_stacks_with_existing():
    """Shockwave stacks with existing debuffs."""
    sim = make_sim(
        hand=[sts_sim.Card.Shockwave], energy=3,
        monsters=[{"hp": 20, "powers": {"Vulnerable": 1}}, {"hp": 20}],
    )
    sim.play_card(0, None)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Vulnerable) == 2
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 1
    assert sim.get_monsters()[1].get_power(sts_sim.PowerType.Vulnerable) == 1
    assert sim.get_monsters()[1].get_power(sts_sim.PowerType.Weak) == 1


# ── Whirlwind ────────────────────────────────────────────────────────────

def test_whirlwind_spends_all_energy():
    """Whirlwind spends all energy and hits all enemies."""
    sim = make_sim(
        hand=[sts_sim.Card.Whirlwind], energy=3,
        monsters=[{"hp": 10}, {"hp": 10}],
    )
    sim.play_card(0, 0, 3)
    for m in sim.get_monsters():
        assert m.hp == 7  # 3 hits of 1 damage each
    assert sim.player.energy == 0


def test_whirlwind_zero_energy():
    """Whirlwind with 0 energy does nothing."""
    sim = make_sim(hand=[sts_sim.Card.Whirlwind], energy=0, monster_hp=10)
    sim.play_card(0, 0, 0)
    assert sim.get_monsters()[0].hp == 10
    assert sim.player.energy == 0


def test_whirlwind_upgraded():
    """Upgraded Whirlwind hits X+1 times."""
    sim = make_sim(hand=[(sts_sim.Card.Whirlwind, True)], energy=2, monster_hp=10)
    sim.play_card(0, 0, 2)
    assert sim.get_monsters()[0].hp == 7  # (2+1) hits of 1 damage
    assert sim.player.energy == 0


def test_whirlwind_with_strength():
    """Whirlwind with Strength scales per HIT."""
    sim = make_sim(
        hand=[sts_sim.Card.Whirlwind], energy=2, monster_hp=10,
        player_powers={"Strength": 1},
    )
    sim.play_card(0, 0, 2)
    assert sim.get_monsters()[0].hp == 6  # 2 hits x (1+1) = 4 damage
    assert sim.player.energy == 0


# ── Battle Trance ────────────────────────────────────────────────────────

def test_battle_trance_base():
    """Battle Trance draws 3 cards for free."""
    draw = [sts_sim.Card.StrikeRed] * 5
    sim = make_sim(hand=[sts_sim.Card.BattleTrance], draw_pile=draw, energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert len(sim.get_hand()) == 3
    assert len(sim.get_draw_pile()) == 2
    assert sim.player.energy == 3


def test_battle_trance_upgraded():
    """Upgraded Battle Trance draws 4 cards."""
    draw = [sts_sim.Card.StrikeRed] * 5
    sim = make_sim(hand=[(sts_sim.Card.BattleTrance, True)], draw_pile=draw, energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert len(sim.get_hand()) == 4
    assert len(sim.get_draw_pile()) == 1
    assert sim.player.energy == 3


def test_battle_trance_reshuffle():
    """Battle Trance reshuffles discard into draw when draw pile runs out."""
    draw = [sts_sim.Card.StrikeRed]
    discard = [sts_sim.Card.DefendRed] * 5
    sim = make_sim(
        hand=[sts_sim.Card.BattleTrance], draw_pile=draw, discard_pile=discard,
        energy=3, monster_hp=20,
    )
    sim.play_card(0, None)
    assert len(sim.get_hand()) == 3


# ── Burning Pact ─────────────────────────────────────────────────────────

def test_burning_pact_base():
    """Burning Pact exhausts a card and draws 2."""
    draw = [sts_sim.Card.DefendRed] * 5
    sim = make_sim(
        hand=[sts_sim.Card.BurningPact, sts_sim.Card.StrikeRed],
        draw_pile=draw, energy=3, monster_hp=20,
    )
    sim.play_card(0, None, 0)  # choose index 0 in remaining hand (Strike)
    assert len(sim.get_exhaust_pile()) == 1
    assert len(sim.get_hand()) == 2  # drew 2 cards
    assert sim.player.energy == 2


def test_burning_pact_upgraded():
    """Upgraded Burning Pact draws 3 cards."""
    draw = [sts_sim.Card.DefendRed] * 5
    sim = make_sim(
        hand=[(sts_sim.Card.BurningPact, True), sts_sim.Card.DefendRed],
        draw_pile=draw, energy=3, monster_hp=20,
    )
    sim.play_card(0, None, 0)  # choose Defend to exhaust
    assert len(sim.get_exhaust_pile()) == 1
    assert len(sim.get_hand()) == 3  # drew 3 cards
    assert sim.player.energy == 2


def test_burning_pact_with_dark_embrace():
    """Burning Pact + Dark Embrace draws an extra card on exhaust."""
    draw = [sts_sim.Card.DefendRed] * 5
    sim = make_sim(
        hand=[sts_sim.Card.BurningPact, sts_sim.Card.StrikeRed],
        draw_pile=draw, energy=3, monster_hp=20,
        player_powers={"DarkEmbrace": 1},
    )
    sim.play_card(0, None, 0)  # exhaust Strike
    assert len(sim.get_exhaust_pile()) == 1
    # Dark Embrace draws 1 + Burning Pact draws 2 = 3 cards
    assert len(sim.get_hand()) == 3


# ── Carnage ──────────────────────────────────────────────────────────────

def test_carnage_base():
    """Carnage deals 4 damage."""
    sim = make_sim(hand=[sts_sim.Card.Carnage], energy=3, monster_hp=10)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 6
    assert sim.player.energy == 1


def test_carnage_ethereal():
    """Carnage is exhausted if not played (Ethereal) at end of turn."""
    sim = make_sim(hand=[sts_sim.Card.Carnage], energy=3, monster_hp=20)
    sim.end_player_turn()
    assert len(sim.get_exhaust_pile()) == 1


def test_carnage_upgraded():
    """Upgraded Carnage deals 6 damage."""
    sim = make_sim(hand=[(sts_sim.Card.Carnage, True)], energy=3, monster_hp=10)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 4


# ── Blood for Blood ──────────────────────────────────────────────────────

def test_blood_for_blood_full_cost():
    """Blood for Blood at full cost (4 energy) when no HP lost."""
    sim = make_sim(hand=[sts_sim.Card.BloodForBlood], energy=4, monster_hp=10)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 6
    assert sim.player.energy == 0


def test_blood_for_blood_reduced_cost():
    """Blood for Blood costs 1 after losing HP."""
    sim = make_sim(hand=[sts_sim.Card.BloodForBlood], energy=3, monster_hp=10, player_hp=8)
    # Simulate having lost HP this combat by dealing damage to player
    sim.deal_damage_to_player(1)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 6
    assert sim.player.energy == 2


def test_blood_for_blood_upgraded_free():
    """Upgraded Blood for Blood costs 0 after losing HP."""
    sim = make_sim(hand=[(sts_sim.Card.BloodForBlood, True)], energy=3, monster_hp=10, player_hp=8)
    sim.deal_damage_to_player(1)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 6
    assert sim.player.energy == 3


# ── Disarm ───────────────────────────────────────────────────────────────

def test_disarm_base():
    """Disarm applies 2 WEAK and exhausts."""
    sim = make_sim(hand=[sts_sim.Card.Disarm], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 2
    assert len(sim.get_exhaust_pile()) == 1
    assert sim.player.energy == 2


def test_disarm_upgraded():
    """Upgraded Disarm applies 3 WEAK."""
    sim = make_sim(hand=[(sts_sim.Card.Disarm, True)], energy=3, monster_hp=20)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 3
    assert len(sim.get_exhaust_pile()) == 1


def test_disarm_stacks():
    """Disarm stacks WEAK on already-weakened enemy."""
    sim = make_sim(
        hand=[sts_sim.Card.Disarm], energy=3, monster_hp=20,
        monster_powers={"Weak": 1},
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 3


# ── Flame Barrier ────────────────────────────────────────────────────────
# Note: Flame Barrier retaliation requires end_player_turn + enemy attack,
# so the retaliation part is tested as multi-turn. Block grant is testable.

def test_flame_barrier_grants_block():
    """Flame Barrier grants 3 BLK when played."""
    sim = make_sim(hand=[sts_sim.Card.FlameBarrier], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 3
    assert sim.player.energy == 1


def test_flame_barrier_upgraded_block():
    """Upgraded Flame Barrier grants 4 BLK."""
    sim = make_sim(hand=[(sts_sim.Card.FlameBarrier, True)], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 4


# ── Ghostly Armor ────────────────────────────────────────────────────────

def test_ghostly_armor_base():
    """Ghostly Armor grants 2 block."""
    sim = make_sim(hand=[sts_sim.Card.GhostlyArmor], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 2
    assert sim.player.energy == 2


def test_ghostly_armor_ethereal():
    """Ghostly Armor is exhausted if not played (Ethereal)."""
    sim = make_sim(hand=[sts_sim.Card.GhostlyArmor], energy=3, monster_hp=20)
    sim.end_player_turn()
    assert len(sim.get_exhaust_pile()) == 1


def test_ghostly_armor_upgraded():
    """Upgraded Ghostly Armor grants 3 block."""
    sim = make_sim(hand=[(sts_sim.Card.GhostlyArmor, True)], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 3
    assert sim.player.energy == 2


# ── Inflame ──────────────────────────────────────────────────────────────

def test_inflame_base():
    """Inflame grants 1 STR."""
    sim = make_sim(hand=[sts_sim.Card.Inflame], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 1
    assert sim.player.energy == 1


def test_inflame_stacks():
    """Inflame stacks with existing STR."""
    sim = make_sim(
        hand=[sts_sim.Card.Inflame], energy=3, monster_hp=20,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 3


def test_inflame_upgraded():
    """Upgraded Inflame costs 1 energy."""
    sim = make_sim(hand=[(sts_sim.Card.Inflame, True)], energy=1, monster_hp=20)
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 1
    assert sim.player.energy == 0


# ── Metallicize ──────────────────────────────────────────────────────────

def test_metallicize_end_of_turn():
    """Metallicize grants 1 BLK at end of turn."""
    sim = make_sim(hand=[sts_sim.Card.Metallicize], energy=3, monster_hp=20)
    sim.play_card(0, None)
    sim.end_player_turn()
    assert sim.player.block >= 1


def test_metallicize_upgraded_cost():
    """Upgraded Metallicize costs 0 energy."""
    sim = make_sim(hand=[(sts_sim.Card.Metallicize, True)], energy=0, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.energy == 0


# ── Power Through ────────────────────────────────────────────────────────

def test_power_through_base():
    """Power Through grants 3 BLK and adds DAZED to discard pile."""
    sim = make_sim(hand=[sts_sim.Card.PowerThrough], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 3
    assert sim.player.energy == 2
    # Check DAZED in discard pile
    discard = sim.get_discard_pile()
    dazed_count = sum(1 for c in discard if c.card == sts_sim.Card.Dazed)
    assert dazed_count == 1


def test_power_through_upgraded():
    """Upgraded Power Through grants 4 BLK."""
    sim = make_sim(hand=[(sts_sim.Card.PowerThrough, True)], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 4
    discard = sim.get_discard_pile()
    dazed_count = sum(1 for c in discard if c.card == sts_sim.Card.Dazed)
    assert dazed_count == 1


# ── Rampage ──────────────────────────────────────────────────────────────

def test_rampage_base():
    """Rampage deals damage equal to exhaust pile size."""
    sim = make_sim(hand=[sts_sim.Card.Rampage], energy=3, monster_hp=10)
    # Add 3 cards to exhaust pile by exhausting them via the sim
    sim.add_card_to_exhaust(sts_sim.Card.StrikeRed)
    sim.add_card_to_exhaust(sts_sim.Card.StrikeRed)
    sim.add_card_to_exhaust(sts_sim.Card.StrikeRed)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 7  # 10 - 3


def test_rampage_empty_exhaust():
    """Rampage with empty exhaust pile deals 0 damage."""
    sim = make_sim(hand=[sts_sim.Card.Rampage], energy=3, monster_hp=10)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 10


def test_rampage_upgraded():
    """Upgraded Rampage exhausts a card first, then counts."""
    sim = make_sim(
        hand=[(sts_sim.Card.Rampage, True), sts_sim.Card.StrikeRed],
        energy=3, monster_hp=10,
    )
    # Exhaust pile has 2 cards already
    sim.add_card_to_exhaust(sts_sim.Card.DefendRed)
    sim.add_card_to_exhaust(sts_sim.Card.DefendRed)
    sim.play_card(0, 0, 0)  # choose Strike to exhaust
    assert sim.get_monsters()[0].hp == 7  # 3 in exhaust pile -> 3 HIT


def test_rampage_with_strength():
    """Rampage scales with Strength."""
    sim = make_sim(
        hand=[sts_sim.Card.Rampage], energy=3, monster_hp=10,
        player_powers={"Strength": 2},
    )
    sim.add_card_to_exhaust(sts_sim.Card.StrikeRed)
    sim.add_card_to_exhaust(sts_sim.Card.StrikeRed)
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 6  # 2 (exhaust count) + 2 STR = 4 damage


# ── Second Wind ──────────────────────────────────────────────────────────

def test_second_wind_base():
    """Second Wind exhausts non-Attacks and gains 1 BLK per card."""
    sim = make_sim(
        hand=[
            sts_sim.Card.SecondWind,
            sts_sim.Card.DefendRed,
            sts_sim.Card.DefendRed,
            sts_sim.Card.StrikeRed,
        ],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, None)
    assert sim.player.block == 2  # 2 Defends exhausted x 1 BLK each
    assert len(sim.get_exhaust_pile()) == 2
    # Strike should remain in hand
    hand = sim.get_hand()
    assert len(hand) == 1
    assert hand[0].card == sts_sim.Card.StrikeRed


def test_second_wind_only_attacks():
    """Second Wind with only Attacks in hand exhausts nothing."""
    sim = make_sim(
        hand=[
            sts_sim.Card.SecondWind,
            sts_sim.Card.StrikeRed,
            sts_sim.Card.StrikeRed,
            sts_sim.Card.StrikeRed,
        ],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, None)
    assert sim.player.block == 0
    assert len(sim.get_exhaust_pile()) == 0


def test_second_wind_upgraded():
    """Upgraded Second Wind gains 2 BLK per card exhausted."""
    sim = make_sim(
        hand=[
            (sts_sim.Card.SecondWind, True),
            sts_sim.Card.DefendRed,
            sts_sim.Card.DefendRed,
            sts_sim.Card.DefendRed,
            sts_sim.Card.StrikeRed,
        ],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, None)
    assert sim.player.block == 6  # 3 Defends x 2 BLK each
    assert len(sim.get_exhaust_pile()) == 3


# ── Sentinel ─────────────────────────────────────────────────────────────

def test_sentinel_base():
    """Sentinel grants 2 block when played normally."""
    sim = make_sim(hand=[sts_sim.Card.Sentinel], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.block == 2
    assert sim.player.energy == 2
    assert len(sim.get_discard_pile()) == 1
    assert len(sim.get_exhaust_pile()) == 0


def test_sentinel_energy_on_exhaust():
    """Sentinel grants 2 energy when exhausted by Second Wind."""
    sim = make_sim(
        hand=[sts_sim.Card.SecondWind, sts_sim.Card.Sentinel],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, None)
    # Sentinel exhausted -> +2 energy, Second Wind costs 1
    # 3 - 1 (Second Wind) + 2 (Sentinel exhaust) = 4
    assert sim.player.energy == 4
    assert len(sim.get_exhaust_pile()) == 1


def test_sentinel_upgraded():
    """Upgraded Sentinel grants 3 BLK and 3 energy on exhaust."""
    draw = [sts_sim.Card.StrikeRed] * 5
    sim = make_sim(
        hand=[sts_sim.Card.BurningPact, (sts_sim.Card.Sentinel, True)],
        draw_pile=draw, energy=3, monster_hp=20,
    )
    sim.play_card(0, None, 0)  # Burning Pact, choose Sentinel+ to exhaust
    # Sentinel+ exhausted -> +3 energy, Burning Pact costs 1
    # 3 - 1 + 3 = 5
    assert sim.player.energy == 5


# ── Sever Soul ───────────────────────────────────────────────────────────

def test_sever_soul_base():
    """Sever Soul deals 3 damage and exhausts a card."""
    sim = make_sim(
        hand=[sts_sim.Card.SeverSoul, sts_sim.Card.DefendRed],
        energy=3, monster_hp=10,
    )
    sim.play_card(0, 0, 0)  # target enemy 0, choose Defend to exhaust
    assert sim.get_monsters()[0].hp == 7
    assert len(sim.get_exhaust_pile()) == 1


def test_sever_soul_upgraded():
    """Upgraded Sever Soul deals 4 damage and can exhaust 2 cards."""
    sim = make_sim(
        hand=[(sts_sim.Card.SeverSoul, True), sts_sim.Card.DefendRed, sts_sim.Card.DefendRed],
        energy=3, monster_hp=10,
    )
    sim.play_card(0, 0, 0)  # exhaust first available
    assert sim.get_monsters()[0].hp == 6


def test_sever_soul_with_strength():
    """Sever Soul with 2 STR deals 5 damage (3 base + 2 STR)."""
    sim = make_sim(
        hand=[sts_sim.Card.SeverSoul, sts_sim.Card.StrikeRed],
        energy=3, monster_hp=15,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, 0, 0)  # target enemy, exhaust Strike
    assert sim.get_monsters()[0].hp == 10  # 15 - 5


# ── Spot Weakness ────────────────────────────────────────────────────────

def test_spot_weakness_valid_die():
    """Spot Weakness grants STR when die is on valid face (1-3)."""
    sim = make_sim(hand=[sts_sim.Card.SpotWeakness], energy=3, monster_hp=20)
    sim.set_die_value(2)
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 1
    assert sim.player.energy == 2


def test_spot_weakness_invalid_die():
    """Spot Weakness fails when die is on invalid face (5)."""
    sim = make_sim(hand=[sts_sim.Card.SpotWeakness], energy=3, monster_hp=20)
    sim.set_die_value(5)
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 0
    assert sim.player.energy == 2


def test_spot_weakness_upgraded():
    """Upgraded Spot Weakness succeeds on die face [4]."""
    sim = make_sim(hand=[(sts_sim.Card.SpotWeakness, True)], energy=3, monster_hp=20)
    sim.set_die_value(4)
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 1


# ── Rage ─────────────────────────────────────────────────────────────────

def test_rage_base():
    """Rage grants block equal to number of Attacks in hand."""
    sim = make_sim(
        hand=[
            sts_sim.Card.RageCard,
            sts_sim.Card.StrikeRed,
            sts_sim.Card.StrikeRed,
            sts_sim.Card.DefendRed,
        ],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, None)
    assert sim.player.block == 2  # 2 Strikes in hand
    assert sim.player.energy == 2


def test_rage_no_attacks():
    """Rage with no Attacks in hand grants 0 BLK."""
    sim = make_sim(
        hand=[
            sts_sim.Card.RageCard,
            sts_sim.Card.DefendRed,
            sts_sim.Card.DefendRed,
            sts_sim.Card.DefendRed,
        ],
        energy=3, monster_hp=20,
    )
    sim.play_card(0, None)
    assert sim.player.block == 0


def test_rage_upgraded():
    """Upgraded Rage costs 0 energy."""
    sim = make_sim(
        hand=[
            (sts_sim.Card.RageCard, True),
            sts_sim.Card.StrikeRed,
            sts_sim.Card.StrikeRed,
            sts_sim.Card.StrikeRed,
        ],
        energy=0, monster_hp=20,
    )
    sim.play_card(0, None)
    assert sim.player.block == 3  # 3 Strikes
    assert sim.player.energy == 0


# ── Combust ──────────────────────────────────────────────────────────────

def test_combust_base():
    """Combust deals 1 damage once per turn (power card)."""
    sim = make_sim(hand=[sts_sim.Card.CombustCard], energy=3, monster_hp=10)
    sim.play_card(0, None)
    assert sim.player.energy == 2


def test_combust_upgraded():
    """Upgraded Combust deals 2 damage (power card)."""
    sim = make_sim(hand=[(sts_sim.Card.CombustCard, True)], energy=3, monster_hp=10)
    sim.play_card(0, None)
    assert sim.player.energy == 2


# ── Dark Embrace ─────────────────────────────────────────────────────────

def test_dark_embrace_on_exhaust():
    """Dark Embrace draws a card when a card is exhausted."""
    draw = [sts_sim.Card.StrikeRed] * 5
    sim = make_sim(
        hand=[sts_sim.Card.BurningPact, sts_sim.Card.DefendRed],
        draw_pile=draw, energy=3, monster_hp=20,
        player_powers={"DarkEmbrace": 1},
    )
    sim.play_card(0, None, 0)  # Burning Pact, exhaust Defend
    # Dark Embrace draws 1 + Burning Pact draws 2 = 3 cards
    assert len(sim.get_hand()) == 3


def test_dark_embrace_multiple():
    """Dark Embrace triggers for each card exhausted."""
    draw = [sts_sim.Card.StrikeRed] * 5
    sim = make_sim(
        hand=[sts_sim.Card.SecondWind, sts_sim.Card.DefendRed, sts_sim.Card.DefendRed],
        draw_pile=draw, energy=3, monster_hp=20,
        player_powers={"DarkEmbrace": 1},
    )
    sim.play_card(0, None)
    # 2 Defends exhausted -> 2 Dark Embrace draws
    assert len(sim.get_hand()) == 2


def test_dark_embrace_upgraded_cost():
    """Upgraded Dark Embrace costs 1 energy."""
    sim = make_sim(hand=[(sts_sim.Card.DarkEmbrace, True)], energy=1, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.energy == 0


# ── Evolve ───────────────────────────────────────────────────────────────

def test_evolve_upgraded_cost():
    """Upgraded Evolve costs 0 energy."""
    sim = make_sim(hand=[(sts_sim.Card.Evolve, True)], energy=0, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.energy == 0


# ── Feel No Pain ─────────────────────────────────────────────────────────

def test_feel_no_pain_on_exhaust():
    """Feel No Pain grants 1 BLK when a card is exhausted."""
    sim = make_sim(
        hand=[sts_sim.Card.BurningPact, sts_sim.Card.StrikeRed],
        draw_pile=[sts_sim.Card.DefendRed] * 5,
        energy=3, monster_hp=20,
        player_powers={"FeelNoPain": 1},
    )
    sim.play_card(0, None, 0)  # Burning Pact, exhaust Strike
    assert sim.player.block >= 1


def test_feel_no_pain_multiple():
    """Feel No Pain triggers for each card exhausted."""
    sim = make_sim(
        hand=[
            sts_sim.Card.SecondWind,
            sts_sim.Card.DefendRed,
            sts_sim.Card.DefendRed,
            sts_sim.Card.DefendRed,
        ],
        energy=3, monster_hp=20,
        player_powers={"FeelNoPain": 1},
    )
    sim.play_card(0, None)
    # 3 Defends exhausted: 3 BLK from Feel No Pain + 3 BLK from Second Wind = 6
    assert sim.player.block == 6


def test_feel_no_pain_upgraded_cost():
    """Upgraded Feel No Pain costs 0 energy."""
    sim = make_sim(hand=[(sts_sim.Card.FeelNoPain, True)], energy=0, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.energy == 0


# ── Fire Breathing ───────────────────────────────────────────────────────
# Fire Breathing triggers on draw — hard to test without end_player_turn
# cycle. Cost test is straightforward.

def test_fire_breathing_base_cost():
    """Fire Breathing costs 1 energy to play."""
    sim = make_sim(hand=[sts_sim.Card.FireBreathing], energy=3, monster_hp=20)
    sim.play_card(0, None)
    assert sim.player.energy == 2


# ── Rupture ──────────────────────────────────────────────────────────────

def test_rupture_base():
    """Rupture grants 1 STR and costs 1 HP."""
    sim = make_sim(hand=[sts_sim.Card.Rupture], energy=3, player_hp=9, monster_hp=20)
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 1
    assert sim.player.hp == 8
    assert sim.player.energy == 2


def test_rupture_stacks():
    """Rupture stacks with existing STR."""
    sim = make_sim(
        hand=[sts_sim.Card.Rupture], energy=3, player_hp=9, monster_hp=20,
        player_powers={"Strength": 2},
    )
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 3
    assert sim.player.hp == 8


def test_rupture_upgraded():
    """Upgraded Rupture costs 0 energy."""
    sim = make_sim(hand=[(sts_sim.Card.Rupture, True)], energy=0, player_hp=9, monster_hp=20)
    sim.play_card(0, None)
    assert sim.get_player_power(sts_sim.PowerType.Strength) == 1
    assert sim.player.hp == 8
    assert sim.player.energy == 0
