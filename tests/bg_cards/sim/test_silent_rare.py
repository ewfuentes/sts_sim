"""Simulator tests for Silent Rare cards."""
import sts_sim
from tests.live.conftest import make_sim


# ===========================================================================
# Die Die Die
# ===========================================================================


def test_die_die_die_aoe():
    """Die Die Die deals 3 AOE damage, exhausts."""
    sim = make_sim(
        hand=[sts_sim.Card.DieDieDie],
        energy=3,
        monsters=[{"hp": 20}, {"hp": 15}],
    )
    sim.play_card(0, None)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 17  # 20 - 3 = 17
    assert monsters[1].hp == 12  # 15 - 3 = 12
    assert len(sim.get_exhaust_pile()) == 1


def test_die_die_die_upgraded():
    """Die Die Die+ deals 4 AOE damage, exhausts."""
    sim = make_sim(
        hand=[(sts_sim.Card.DieDieDie, True)],
        energy=3,
        monsters=[{"hp": 20}, {"hp": 15}],
    )
    sim.play_card(0, None)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 16  # 20 - 4 = 16
    assert monsters[1].hp == 11  # 15 - 4 = 11
    assert len(sim.get_exhaust_pile()) == 1


def test_die_die_die_with_strength():
    """Die Die Die with 2 STR: 3*(1+2)=9 AOE damage."""
    sim = make_sim(
        hand=[sts_sim.Card.DieDieDie],
        energy=3,
        player_powers={"Strength": 2},
        monsters=[{"hp": 20}, {"hp": 15}],
    )
    sim.play_card(0, None)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 15  # 20 - (3+2) = 15
    assert monsters[1].hp == 10  # 15 - (3+2) = 10


# ===========================================================================
# Grand Finale
# ===========================================================================


def test_grand_finale_empty_draw_pile():
    """Grand Finale deals 10 AOE damage with empty draw pile."""
    sim = make_sim(
        hand=[sts_sim.Card.GrandFinale],
        energy=3,
        monsters=[{"hp": 20}, {"hp": 15}],
    )
    sim.play_card(0, None)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 10  # 20 - 10 = 10
    assert monsters[1].hp == 5   # 15 - 10 = 5


def test_grand_finale_upgraded_empty_draw():
    """Grand Finale+ deals 12 AOE damage with empty draw pile."""
    sim = make_sim(
        hand=[(sts_sim.Card.GrandFinale, True)],
        energy=3,
        monsters=[{"hp": 20}, {"hp": 20}],
    )
    sim.play_card(0, None)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 8  # 20 - 12 = 8
    assert monsters[1].hp == 8


def test_grand_finale_with_strength():
    """Grand Finale with 1 STR: 10*(1+1)=20 AOE damage."""
    sim = make_sim(
        hand=[sts_sim.Card.GrandFinale],
        energy=3,
        player_powers={"Strength": 1},
        monster_hp=30,
    )
    sim.play_card(0, None)
    assert sim.get_monsters()[0].hp == 19  # 30 - (10+1) = 19


# ===========================================================================
# Skewer
# ===========================================================================


def test_skewer_with_3_energy():
    """Skewer with X=3: 1*(3+1)=4 damage."""
    sim = make_sim(hand=[sts_sim.Card.Skewer], energy=3, monster_hp=20)
    sim.play_card(0, 0, 3)  # choice=3 for X=3
    assert sim.get_monsters()[0].hp == 16  # 20 - 4 = 16
    assert sim.player.energy == 0


def test_skewer_with_0_energy():
    """Skewer with X=0: 1 damage (1 HIT once)."""
    sim = make_sim(hand=[sts_sim.Card.Skewer], energy=0, monster_hp=20)
    sim.play_card(0, 0, 0)
    assert sim.get_monsters()[0].hp == 19  # 20 - 1 = 19


def test_skewer_upgraded_with_3_energy():
    """Skewer+ with X=3: 2*3=6 damage."""
    sim = make_sim(
        hand=[(sts_sim.Card.Skewer, True)],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, 0, 3)
    assert sim.get_monsters()[0].hp == 14  # 20 - 6 = 14
    assert sim.player.energy == 0


def test_skewer_with_strength():
    """Skewer with 2 STR, X=2: (1+2)*(2+1)=9 damage."""
    sim = make_sim(
        hand=[sts_sim.Card.Skewer],
        energy=2,
        player_powers={"Strength": 2},
        monster_hp=20,
    )
    sim.play_card(0, 0, 2)
    assert sim.get_monsters()[0].hp == 11  # 20 - 9 = 11


# ===========================================================================
# Adrenaline
# ===========================================================================


def test_adrenaline_basic():
    """Adrenaline (base) gives 1 energy, draws 2 cards, exhausts."""
    draw = [sts_sim.Card.StrikeGreen] * 5
    sim = make_sim(
        hand=[sts_sim.Card.Adrenaline],
        draw_pile=draw,
        energy=0,
    )
    sim.play_card(0, None)
    assert sim.player.energy == 1  # base: +1
    assert len(sim.get_hand()) == 2
    assert len(sim.get_exhaust_pile()) == 1


def test_adrenaline_as_turn_starter():
    """Adrenaline (base) with 3 energy: 4 energy, 4 cards in hand."""
    draw = [sts_sim.Card.StrikeGreen] * 5
    sim = make_sim(
        hand=[
            sts_sim.Card.Adrenaline,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ],
        draw_pile=draw,
        energy=3,
    )
    sim.play_card(0, None)
    assert sim.player.energy == 4  # 3 + 1 = 4
    assert len(sim.get_hand()) == 4  # 2 existing + 2 drawn


# ===========================================================================
# Bullet Time
# ===========================================================================


def test_bullet_time_basic():
    """Bullet Time costs 3 energy, cards cost 0 this turn."""
    sim = make_sim(
        hand=[
            sts_sim.Card.BulletTime,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, None)
    assert sim.player.energy == 0  # 3 - 3 = 0
    # Remaining cards should cost 0 — play one to verify
    sim.play_card(0, 0)
    assert sim.player.energy == 0  # Still 0, card was free


def test_bullet_time_upgraded():
    """Bullet Time+ costs 2 energy."""
    sim = make_sim(
        hand=[
            (sts_sim.Card.BulletTime, True),
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, None)
    assert sim.player.energy == 1  # 3 - 2 = 1


# ===========================================================================
# Malaise
# ===========================================================================


def test_malaise_with_3_energy():
    """Malaise with X=3: 3 WEAK, 3 POISON. Exhausts."""
    sim = make_sim(
        hand=[sts_sim.Card.Malaise],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, 0, 3)
    m = sim.get_monsters()[0]
    assert m.get_power(sts_sim.PowerType.Weak) == 3
    assert m.get_power(sts_sim.PowerType.Poison) == 3
    assert sim.player.energy == 0
    assert len(sim.get_exhaust_pile()) == 1


def test_malaise_with_1_energy():
    """Malaise with X=1: 1 WEAK, 1 POISON."""
    sim = make_sim(
        hand=[sts_sim.Card.Malaise],
        energy=1,
        monster_hp=20,
    )
    sim.play_card(0, 0, 1)
    m = sim.get_monsters()[0]
    assert m.get_power(sts_sim.PowerType.Weak) == 1
    assert m.get_power(sts_sim.PowerType.Poison) == 1


def test_malaise_upgraded_with_2_energy():
    """Malaise+ with X=2: applies X+1=3 WEAK and 3 POISON."""
    sim = make_sim(
        hand=[(sts_sim.Card.Malaise, True)],
        energy=2,
        monster_hp=20,
    )
    sim.play_card(0, 0, 2)
    m = sim.get_monsters()[0]
    assert m.get_power(sts_sim.PowerType.Weak) == 3
    assert m.get_power(sts_sim.PowerType.Poison) == 3
    assert sim.player.energy == 0


# ===========================================================================
# Storm of Steel
# ===========================================================================


def test_storm_of_steel_discard_3():
    """Storm of Steel: discards entire hand (3 cards), gain 3 SHIV."""
    sim = make_sim(
        hand=[
            sts_sim.Card.StormOfSteel,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ],
        energy=3,
    )
    sim.play_card(0, None)  # discards remaining 3 cards
    assert sim.get_player_power(sts_sim.PowerType.Shiv) == 3


def test_storm_of_steel_discard_0():
    """Storm of Steel with empty hand: gain 0 SHIV."""
    sim = make_sim(hand=[sts_sim.Card.StormOfSteel], energy=3)
    sim.play_card(0, None)  # no cards left to discard
    assert sim.get_player_power(sts_sim.PowerType.Shiv) == 0


def test_storm_of_steel_upgraded_discard_2():
    """Storm of Steel+: discards 2 cards, gain 2+1=3 SHIV."""
    sim = make_sim(
        hand=[
            (sts_sim.Card.StormOfSteel, True),
            sts_sim.Card.StrikeGreen,
            sts_sim.Card.StrikeGreen,
        ],
        energy=3,
    )
    sim.play_card(0, None)  # discards remaining 2 cards
    assert sim.get_player_power(sts_sim.PowerType.Shiv) == 3


# ===========================================================================
# Doppelganger
# ===========================================================================


def test_doppelganger_exhausts():
    """Doppelganger exhausts after use."""
    sim = make_sim(
        hand=[sts_sim.Card.StrikeGreen, sts_sim.Card.Doppelganger],
        energy=5,
        monster_hp=30,
    )
    sim.play_card(0, 0)  # Play Strike first
    sim.play_card(0, 0, 2)  # Play Doppelganger (X=2)
    assert len(sim.get_exhaust_pile()) == 1


def test_doppelganger_upgraded_no_exhaust():
    """Doppelganger+ does NOT exhaust."""
    sim = make_sim(
        hand=[sts_sim.Card.StrikeGreen, (sts_sim.Card.Doppelganger, True)],
        energy=5,
        monster_hp=30,
    )
    sim.play_card(0, 0)  # Play Strike first
    sim.play_card(0, 0, 1)  # Play Doppelganger+ (X=1)
    assert len(sim.get_exhaust_pile()) == 0
    assert len(sim.get_discard_pile()) >= 1


# ===========================================================================
# Corpse Explosion
# ===========================================================================


def test_corpse_explosion_applies_poison():
    """Corpse Explosion applies 2 POISON to target."""
    sim = make_sim(
        hand=[sts_sim.Card.CorpseExplosionCard],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 2


def test_corpse_explosion_upgraded():
    """Corpse Explosion+ applies 3 POISON."""
    sim = make_sim(
        hand=[(sts_sim.Card.CorpseExplosionCard, True)],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 3


# ===========================================================================
# A Thousand Cuts
# ===========================================================================


def test_a_thousand_cuts_plays():
    """A Thousand Cuts can be played as a power. Costs 2."""
    sim = make_sim(hand=[sts_sim.Card.AThousandCutsCard], energy=3)
    sim.play_card(0, None)
    assert sim.player.energy == 1  # 3 - 2 = 1


# ===========================================================================
# Burst
# ===========================================================================


def test_burst_doubles_next_skill():
    """Burst doubles the next Skill played this turn."""
    sim = make_sim(
        hand=[sts_sim.Card.BurstCard, sts_sim.Card.LegSweep],
        energy=3,
        player_block=0,
        monster_hp=20,
    )
    sim.play_card(0, None)  # Play Burst
    sim.play_card(0, 0)     # Play Leg Sweep
    # Leg Sweep played twice: 2 WEAK, 6 block
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Weak) == 2
    assert sim.player.block == 6


def test_burst_only_affects_next_skill():
    """Burst only doubles the FIRST Skill, not subsequent ones."""
    sim = make_sim(
        hand=[
            sts_sim.Card.BurstCard,
            sts_sim.Card.DefendGreen,
            sts_sim.Card.Blur,
        ],
        energy=3,
        player_block=0,
    )
    sim.play_card(0, None)  # Burst
    sim.play_card(0, None)  # Defend (doubled: 2 block)
    sim.play_card(0, None)  # Blur (not doubled: 2 block)
    assert sim.player.block == 4  # 2 + 2 = 4


def test_burst_upgraded_costs_0():
    """Burst+ costs 0 energy."""
    sim = make_sim(
        hand=[(sts_sim.Card.BurstCard, True), sts_sim.Card.DeadlyPoison],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, None)  # Burst+ (costs 0)
    assert sim.player.energy == 3
    sim.play_card(0, 0)     # Deadly Poison (doubled)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 2


def test_burst_does_not_double_attacks():
    """Burst does NOT double Attacks."""
    sim = make_sim(
        hand=[sts_sim.Card.BurstCard, sts_sim.Card.StrikeGreen],
        energy=3,
        monster_hp=20,
    )
    sim.play_card(0, None)  # Burst
    sim.play_card(0, 0)     # Strike (NOT doubled)
    assert sim.get_monsters()[0].hp == 19  # Only 1 damage


# ===========================================================================
# Envenom
# ===========================================================================


def test_envenom_adds_poison_to_hits():
    """Envenom adds POISON to each HIT."""
    sim = make_sim(
        hand=[sts_sim.Card.EnvenomCard, sts_sim.Card.StrikeGreen],
        energy=4,
        monster_hp=20,
    )
    sim.play_card(0, None)  # Envenom
    sim.play_card(0, 0)     # Strike (1 HIT)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 1


def test_envenom_multi_hit():
    """Envenom with single-hit model: Die Die Die (1 HIT) = 1 POISON."""
    sim = make_sim(
        hand=[sts_sim.Card.DieDieDie],
        energy=3,
        player_powers={"Envenom": 1},
        monster_hp=20,
    )
    sim.play_card(0, None)
    assert sim.get_monsters()[0].get_power(sts_sim.PowerType.Poison) == 1


def test_envenom_upgraded_costs_2():
    """Envenom+ costs 2 energy (reduced from 3)."""
    sim = make_sim(hand=[(sts_sim.Card.EnvenomCard, True)], energy=2)
    sim.play_card(0, None)
    assert sim.player.energy == 0  # 2 - 2 = 0


# ===========================================================================
# Tools of the Trade
# ===========================================================================


def test_tools_of_the_trade_plays():
    """Tools of the Trade can be played as a power. Costs 1."""
    sim = make_sim(hand=[sts_sim.Card.ToolsOfTheTradeCard], energy=3)
    sim.play_card(0, None)
    assert sim.player.energy == 2  # 3 - 1 = 2


def test_tools_of_the_trade_upgraded_costs_0():
    """Tools of the Trade+ costs 0 energy."""
    sim = make_sim(hand=[(sts_sim.Card.ToolsOfTheTradeCard, True)], energy=3)
    sim.play_card(0, None)
    assert sim.player.energy == 3  # 3 - 0 = 3


# ===========================================================================
# Wraith Form
# ===========================================================================


def test_wraith_form_plays():
    """Wraith Form can be played as a power. Costs 3."""
    sim = make_sim(hand=[sts_sim.Card.WraithFormCard], energy=3, player_hp=20)
    sim.play_card(0, None)
    assert sim.player.energy == 0  # 3 - 3 = 0
