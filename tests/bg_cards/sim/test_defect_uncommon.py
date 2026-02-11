"""Simulator tests for Defect Uncommon cards."""
import sts_sim
from tests.live.conftest import make_sim


# ===================================================================
# BLIZZARD
# ===================================================================

def test_blizzard_base():
    """Blizzard deals AOE 2 per Frost orb."""
    sim = make_sim(hand=[sts_sim.Card.Blizzard], energy=3,
                   orbs=["Frost", "Frost"], monsters=[{"hp": 20}, {"hp": 20}])
    sim.play_card(0, 0)
    for m in sim.get_monsters():
        assert m.hp == 16  # 20 - 2*2 = 16


def test_blizzard_no_frost():
    """Blizzard with no Frost orbs deals no damage."""
    sim = make_sim(hand=[sts_sim.Card.Blizzard], energy=3,
                   orbs=["Lightning"], monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 20


def test_blizzard_upgraded():
    """Upgraded Blizzard deals AOE 3 per Frost orb."""
    sim = make_sim(hand=[(sts_sim.Card.Blizzard, True)], energy=3,
                   orbs=["Frost", "Frost", "Frost"],
                   monsters=[{"hp": 30}, {"hp": 30}])
    sim.play_card(0, 0)
    for m in sim.get_monsters():
        assert m.hp == 21  # 30 - 3*3 = 21


def test_blizzard_with_strength():
    """Blizzard with Strength adds per-HIT bonus."""
    sim = make_sim(hand=[sts_sim.Card.Blizzard], energy=3,
                   orbs=["Frost", "Frost"],
                   player_powers={"Strength": 2},
                   monsters=[{"hp": 30}])
    sim.play_card(0, 0)
    # 2 Frost orbs x 2 HIT = 4 HIT tokens, each deals 1+2 = 3 damage => 12 total
    assert sim.get_monsters()[0].hp == 18  # 30 - 12 = 18


# ===================================================================
# COLD SNAP
# ===================================================================

def test_cold_snap_base():
    """Cold Snap deals 2 damage and channels 1 Frost."""
    sim = make_sim(hand=[sts_sim.Card.ColdSnap], energy=3,
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18
    orbs = sim.player.get_orbs()
    assert any(o == sts_sim.OrbType.Frost for o in orbs)
    assert sim.player.energy == 2


def test_cold_snap_upgraded():
    """Upgraded Cold Snap deals 3 damage and channels 1 Frost."""
    sim = make_sim(hand=[(sts_sim.Card.ColdSnap, True)], energy=3,
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17
    assert sim.player.energy == 2


def test_cold_snap_full_orbs():
    """Cold Snap with full orb slots evokes oldest orb."""
    sim = make_sim(hand=[sts_sim.Card.ColdSnap], energy=3,
                   orbs=["Lightning", "Lightning", "Frost"],
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    # Oldest Lightning evoked, then Frost channeled
    assert sim.get_monsters()[0].hp < 20  # damage from Cold Snap + Lightning evoke


# ===================================================================
# DOOM AND GLOOM
# ===================================================================

def test_doom_and_gloom_base():
    """Doom and Gloom deals AOE 2 damage and channels 1 Dark."""
    sim = make_sim(hand=[sts_sim.Card.DoomAndGloom], energy=3,
                   monsters=[{"hp": 20}, {"hp": 20}])
    sim.play_card(0, 0)
    for m in sim.get_monsters():
        assert m.hp == 18  # 20 - 2 = 18
    orbs = sim.player.get_orbs()
    assert any(o == sts_sim.OrbType.Dark for o in orbs)
    assert sim.player.energy == 1


def test_doom_and_gloom_upgraded():
    """Upgraded Doom and Gloom deals AOE 3 damage."""
    sim = make_sim(hand=[(sts_sim.Card.DoomAndGloom, True)], energy=3,
                   monsters=[{"hp": 15}, {"hp": 15}])
    sim.play_card(0, 0)
    for m in sim.get_monsters():
        assert m.hp == 12  # 15 - 3 = 12
    assert sim.player.energy == 1


def test_doom_and_gloom_full_orbs():
    """Doom and Gloom with full slots evokes oldest orb."""
    sim = make_sim(hand=[sts_sim.Card.DoomAndGloom], energy=3,
                   orbs=["Frost", "Frost", "Lightning"],
                   monsters=[{"hp": 20}, {"hp": 20}])
    sim.play_card(0, 0)
    for m in sim.get_monsters():
        assert m.hp <= 18  # At least 2 AOE damage


# ===================================================================
# FTL
# ===================================================================

def test_ftl_first_card():
    """FTL as first card draws 1 card."""
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    sim = make_sim(hand=[sts_sim.Card.FTL], draw_pile=draw, energy=3,
                   monsters=[{"hp": 20}])
    hand_before = len(sim.get_hand())
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 19  # 20 - 1 = 19
    # FTL played (hand -1) + draw 1 => net same as before
    assert len(sim.get_hand()) == hand_before  # -1 played + 1 drawn = same
    assert sim.player.energy == 3  # cost 0


def test_ftl_not_first_card():
    """FTL not as first card does not draw."""
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    sim = make_sim(hand=[sts_sim.Card.StrikeBlue, sts_sim.Card.FTL],
                   draw_pile=draw, energy=3, monsters=[{"hp": 20}])
    sim.play_card(0, 0)  # Play Strike first
    hand_after_strike = len(sim.get_hand())
    sim.play_card(0, 0)  # Play FTL second
    assert sim.get_monsters()[0].hp < 20
    assert len(sim.get_hand()) == hand_after_strike - 1  # no draw


def test_ftl_upgraded():
    """Upgraded FTL deals 2 damage and draws if first card."""
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    sim = make_sim(hand=[(sts_sim.Card.FTL, True)], draw_pile=draw, energy=3,
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18
    assert sim.player.energy == 3


# ===================================================================
# MELTER
# ===================================================================

def test_melter_removes_block():
    """Melter removes all block first, then deals damage."""
    sim = make_sim(hand=[sts_sim.Card.MelterCard], energy=3,
                   monsters=[{"hp": 20, "block": 10}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].block == 0
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18


def test_melter_no_block():
    """Melter on enemy with no block just deals damage."""
    sim = make_sim(hand=[sts_sim.Card.MelterCard], energy=3,
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18


def test_melter_upgraded():
    """Upgraded Melter removes block and deals 3 damage."""
    sim = make_sim(hand=[(sts_sim.Card.MelterCard, True)], energy=3,
                   monsters=[{"hp": 20, "block": 15}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].block == 0
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17


# ===================================================================
# SCRAPE
# ===================================================================

def test_scrape_zero_cost_top():
    """Scrape returns 0-cost card from top of discard."""
    sim = make_sim(hand=[sts_sim.Card.Scrape], energy=3,
                   discard_pile=[sts_sim.Card.Zap],
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18
    # Zap should be returned to hand
    hand_cards = [c.card for c in sim.get_hand()]
    assert sts_sim.Card.Zap in hand_cards


def test_scrape_nonzero_cost_top():
    """Scrape does not return non-zero cost card."""
    sim = make_sim(hand=[sts_sim.Card.Scrape], energy=3,
                   discard_pile=[sts_sim.Card.StrikeBlue],
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18
    hand_cards = [c.card for c in sim.get_hand()]
    assert sts_sim.Card.StrikeBlue not in hand_cards


def test_scrape_empty_discard():
    """Scrape with empty discard just deals damage."""
    sim = make_sim(hand=[sts_sim.Card.Scrape], energy=3,
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18


def test_scrape_upgraded():
    """Upgraded Scrape deals 3 damage and returns 0-cost card."""
    sim = make_sim(hand=[(sts_sim.Card.Scrape, True)], energy=3,
                   discard_pile=[sts_sim.Card.TURBO],
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17
    hand_cards = [c.card for c in sim.get_hand()]
    assert sts_sim.Card.TURBO in hand_cards


# ===================================================================
# STREAMLINE
# ===================================================================

def test_streamline_no_powers():
    """Streamline costs 2 with no powers."""
    sim = make_sim(hand=[sts_sim.Card.Streamline], energy=3,
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_streamline_with_powers():
    """Streamline costs 0 with 2 powers in play."""
    sim = make_sim(hand=[sts_sim.Card.LoopCard, sts_sim.Card.StormCard,
                         sts_sim.Card.Streamline], energy=6,
                   monsters=[{"hp": 20}])
    sim.play_card(0)  # Play Loop (cost 1)
    sim.play_card(0)  # Play Storm (cost 1)
    sim.play_card(0, 0)  # Play Streamline (cost 2-2 = 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17
    assert sim.player.energy == 4  # 6 - 1 - 1 - 0 = 4


def test_streamline_upgraded():
    """Upgraded Streamline deals 4 damage."""
    sim = make_sim(hand=[(sts_sim.Card.Streamline, True)], energy=3,
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 16  # 20 - 4 = 16
    assert sim.player.energy == 1  # 3 - 2 = 1


# ===================================================================
# SUNDER
# ===================================================================

def test_sunder_kills_refund():
    """Sunder kills enemy and refunds 3 energy."""
    sim = make_sim(hand=[sts_sim.Card.Sunder], energy=3,
                   monsters=[{"hp": 4}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].is_gone
    assert sim.player.energy == 3  # spent 3, gained 3


def test_sunder_no_kill():
    """Sunder does not refund energy if enemy survives."""
    sim = make_sim(hand=[sts_sim.Card.Sunder], energy=3,
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 15  # 20 - 5 = 15
    assert sim.player.energy == 0  # spent 3, no refund


def test_sunder_upgraded_kills():
    """Upgraded Sunder deals 7, kills, and refunds."""
    sim = make_sim(hand=[(sts_sim.Card.Sunder, True)], energy=3,
                   monsters=[{"hp": 6}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].is_gone
    assert sim.player.energy == 3


# ===================================================================
# DARKNESS
# ===================================================================

def test_darkness_base():
    """Darkness channels 1 Dark orb, costs 1."""
    sim = make_sim(hand=[sts_sim.Card.DarknessCard], energy=3)
    sim.play_card(0)
    orbs = sim.player.get_orbs()
    assert any(o == sts_sim.OrbType.Dark for o in orbs)
    assert sim.player.energy == 2


def test_darkness_upgraded():
    """Upgraded Darkness costs 0."""
    sim = make_sim(hand=[(sts_sim.Card.DarknessCard, True)], energy=3)
    sim.play_card(0)
    orbs = sim.player.get_orbs()
    assert any(o == sts_sim.OrbType.Dark for o in orbs)
    assert sim.player.energy == 3


def test_darkness_full_orbs():
    """Darkness with full orb slots evokes oldest orb."""
    sim = make_sim(hand=[sts_sim.Card.DarknessCard], energy=3,
                   orbs=["Lightning", "Frost", "Frost"],
                   monsters=[{"hp": 20}])
    sim.play_card(0)
    orbs = sim.player.get_orbs()
    assert any(o == sts_sim.OrbType.Dark for o in orbs)


# ===================================================================
# DOUBLE ENERGY
# ===================================================================

def test_double_energy_base():
    """Double Energy doubles energy and exhausts."""
    sim = make_sim(hand=[sts_sim.Card.DoubleEnergy], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 4  # (3-1)*2 = 4
    assert len(sim.get_exhaust_pile()) == 1


def test_double_energy_capped():
    """Double Energy caps at 6."""
    sim = make_sim(hand=[sts_sim.Card.DoubleEnergy], energy=5)
    sim.play_card(0)
    assert sim.player.energy == 6  # (5-1)*2 = 8 capped at 6
    assert len(sim.get_exhaust_pile()) == 1


def test_double_energy_upgraded():
    """Upgraded Double Energy costs 0."""
    sim = make_sim(hand=[(sts_sim.Card.DoubleEnergy, True)], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 6  # (3-0)*2 = 6
    assert len(sim.get_exhaust_pile()) == 1


# ===================================================================
# EQUILIBRIUM
# ===================================================================

def test_equilibrium_block():
    """Equilibrium grants 3 block."""
    sim = make_sim(hand=[sts_sim.Card.Equilibrium], energy=3)
    sim.play_card(0)
    assert sim.player.block == 3
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_equilibrium_upgraded_block():
    """Upgraded Equilibrium grants 4 block."""
    sim = make_sim(hand=[(sts_sim.Card.Equilibrium, True)], energy=3)
    sim.play_card(0)
    assert sim.player.block == 4
    assert sim.player.energy == 1


def test_equilibrium_block_stacks():
    """Equilibrium block stacks with existing block."""
    sim = make_sim(hand=[sts_sim.Card.Equilibrium], energy=3,
                   player_block=5)
    sim.play_card(0)
    assert sim.player.block == 8  # 5 + 3 = 8


# ===================================================================
# FORCE FIELD
# ===================================================================

def test_force_field_with_2_powers():
    """Force Field with 2 powers costs 2."""
    sim = make_sim(hand=[sts_sim.Card.LoopCard, sts_sim.Card.DefragmentCard,
                         sts_sim.Card.ForceField], energy=6)
    sim.play_card(0)  # Loop (cost 1)
    sim.play_card(0)  # Defragment (cost 1)
    sim.play_card(0)  # Force Field (cost 4-2 = 2)
    assert sim.player.block == 3
    assert sim.player.energy == 2  # 6 - 1 - 1 - 2 = 2


def test_force_field_upgraded_with_3_powers():
    """Upgraded Force Field with 3 powers costs 1, gives 4 block."""
    sim = make_sim(hand=[sts_sim.Card.LoopCard, sts_sim.Card.DefragmentCard,
                         sts_sim.Card.StormCard,
                         (sts_sim.Card.ForceField, True)], energy=6)
    sim.play_card(0)  # Loop (cost 1)
    sim.play_card(0)  # Defragment (cost 1)
    sim.play_card(0)  # Storm (cost 1)
    sim.play_card(0)  # Force Field+ (cost 4-3 = 1)
    assert sim.player.block == 4
    assert sim.player.energy == 2  # 6 - 1 - 1 - 1 - 1 = 2


# ===================================================================
# GLACIER
# ===================================================================

def test_glacier_base():
    """Glacier grants 2 block and channels 1 Frost."""
    sim = make_sim(hand=[sts_sim.Card.Glacier], energy=3)
    sim.play_card(0)
    assert sim.player.block == 2
    orbs = sim.player.get_orbs()
    assert any(o == sts_sim.OrbType.Frost for o in orbs)
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_glacier_full_orbs():
    """Glacier with full orb slots evokes oldest orb."""
    sim = make_sim(hand=[sts_sim.Card.Glacier], energy=3,
                   orbs=["Dark", "Dark", "Lightning"],
                   monsters=[{"hp": 20}])
    sim.play_card(0)
    assert sim.player.block >= 2
    orbs = sim.player.get_orbs()
    assert any(o == sts_sim.OrbType.Frost for o in orbs)


# ===================================================================
# HOLOGRAM
# ===================================================================

def test_hologram_retrieves_and_exhausts():
    """Hologram retrieves card from discard and exhausts."""
    sim = make_sim(hand=[sts_sim.Card.Hologram], energy=3,
                   discard_pile=[sts_sim.Card.BallLightning, sts_sim.Card.Zap])
    sim.play_card(0, None, 0)  # choose first card from discard
    assert sim.player.block == 1
    hand_cards = [c.card for c in sim.get_hand()]
    assert sts_sim.Card.BallLightning in hand_cards
    assert len(sim.get_exhaust_pile()) == 1  # Hologram exhausted


def test_hologram_upgraded_no_exhaust():
    """Upgraded Hologram does not exhaust."""
    sim = make_sim(hand=[(sts_sim.Card.Hologram, True)], energy=3,
                   discard_pile=[sts_sim.Card.BallLightning])
    sim.play_card(0, None, 0)
    assert sim.player.block == 1
    hand_cards = [c.card for c in sim.get_hand()]
    assert sts_sim.Card.BallLightning in hand_cards
    assert len(sim.get_exhaust_pile()) == 0  # Not exhausted


def test_hologram_empty_discard():
    """Hologram with empty discard still gives block and exhausts."""
    sim = make_sim(hand=[sts_sim.Card.Hologram], energy=3)
    sim.play_card(0)
    assert sim.player.block == 1
    assert len(sim.get_exhaust_pile()) == 1


# ===================================================================
# OVERCLOCK
# ===================================================================

def test_overclock_base():
    """Overclock draws 2 cards and adds Dazed to discard."""
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    sim = make_sim(hand=[sts_sim.Card.Overclock], draw_pile=draw, energy=3)
    sim.play_card(0)
    assert len(sim.get_hand()) == 2  # drew 2 cards
    discard_cards = [c.card for c in sim.get_discard_pile()]
    assert sts_sim.Card.Dazed in discard_cards
    assert sts_sim.Card.Overclock in discard_cards
    assert sim.player.energy == 2  # 3 - 1 = 2


def test_overclock_upgraded():
    """Upgraded Overclock draws 3 cards."""
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    sim = make_sim(hand=[(sts_sim.Card.Overclock, True)], draw_pile=draw,
                   energy=3)
    sim.play_card(0)
    assert len(sim.get_hand()) == 3  # drew 3 cards
    discard_cards = [c.card for c in sim.get_discard_pile()]
    assert sts_sim.Card.Dazed in discard_cards


# ===================================================================
# RECYCLE
# ===================================================================

def test_recycle_2_cost():
    """Recycle exhausts a 2-cost card and gains 2 energy."""
    sim = make_sim(hand=[sts_sim.Card.RecycleCard, sts_sim.Card.Glacier],
                   energy=3)
    sim.play_card(0, None, 0)  # choose Glacier to exhaust
    exhaust_cards = [c.card for c in sim.get_exhaust_pile()]
    assert sts_sim.Card.Glacier in exhaust_cards
    assert sim.player.energy == 4  # 3 - 1 + 2 = 4


def test_recycle_0_cost():
    """Recycle exhausts a 0-cost card and gains 0 energy."""
    sim = make_sim(hand=[sts_sim.Card.RecycleCard, sts_sim.Card.Zap],
                   energy=3)
    sim.play_card(0, None, 0)  # choose Zap to exhaust
    exhaust_cards = [c.card for c in sim.get_exhaust_pile()]
    assert sts_sim.Card.Zap in exhaust_cards
    assert sim.player.energy == 2  # 3 - 1 + 0 = 2


def test_recycle_x_cost_doubles():
    """Recycle an X-cost card doubles energy."""
    sim = make_sim(hand=[sts_sim.Card.RecycleCard, sts_sim.Card.MultiCast],
                   energy=3)
    sim.play_card(0, None, 0)  # choose Multi-Cast to exhaust
    exhaust_cards = [c.card for c in sim.get_exhaust_pile()]
    assert sts_sim.Card.MultiCast in exhaust_cards
    assert sim.player.energy == 4  # (3 - 1) * 2 = 4


def test_recycle_upgraded():
    """Upgraded Recycle costs 0."""
    sim = make_sim(hand=[(sts_sim.Card.RecycleCard, True),
                         sts_sim.Card.DoomAndGloom], energy=3)
    sim.play_card(0, None, 0)  # choose Doom and Gloom to exhaust
    exhaust_cards = [c.card for c in sim.get_exhaust_pile()]
    assert sts_sim.Card.DoomAndGloom in exhaust_cards
    assert sim.player.energy == 5  # 3 - 0 + 2 = 5


# ===================================================================
# REPROGRAM
# ===================================================================

def test_reprogram_with_orbs():
    """Reprogram gains Strength and removes all orbs."""
    sim = make_sim(hand=[sts_sim.Card.Reprogram], energy=3,
                   orbs=["Lightning", "Frost"])
    sim.play_card(0)
    assert sim.player.get_power(sts_sim.PowerType.Strength) == 1
    assert len(sim.player.get_orbs()) == 0
    assert sim.player.energy == 2  # 3 - 1 = 2


def test_reprogram_no_orbs():
    """Reprogram with no orbs still gains Strength."""
    sim = make_sim(hand=[sts_sim.Card.Reprogram], energy=3)
    sim.play_card(0)
    assert sim.player.get_power(sts_sim.PowerType.Strength) == 1
    assert sim.player.energy == 2


def test_reprogram_upgraded():
    """Upgraded Reprogram costs 0."""
    sim = make_sim(hand=[(sts_sim.Card.Reprogram, True)], energy=3,
                   orbs=["Frost", "Frost", "Dark"])
    sim.play_card(0)
    assert sim.player.get_power(sts_sim.PowerType.Strength) == 1
    assert len(sim.player.get_orbs()) == 0
    assert sim.player.energy == 3  # cost 0


# ===================================================================
# STACK
# ===================================================================

def test_stack_with_orbs():
    """Stack gains block equal to number of orbs."""
    sim = make_sim(hand=[sts_sim.Card.StackCard], energy=3,
                   orbs=["Lightning", "Frost", "Dark"])
    sim.play_card(0)
    assert sim.player.block == 3  # 3 orbs
    assert sim.player.energy == 2  # 3 - 1 = 2


def test_stack_no_orbs():
    """Stack with 0 orbs gains 0 block."""
    sim = make_sim(hand=[sts_sim.Card.StackCard], energy=3)
    sim.play_card(0)
    assert sim.player.block == 0
    assert sim.player.energy == 2


def test_stack_upgraded():
    """Upgraded Stack gains X+1 block."""
    sim = make_sim(hand=[(sts_sim.Card.StackCard, True)], energy=3,
                   orbs=["Frost", "Frost"])
    sim.play_card(0)
    assert sim.player.block == 3  # 2 + 1 = 3
    assert sim.player.energy == 2


# ===================================================================
# TURBO
# ===================================================================

def test_turbo_base():
    """TURBO gains 2 energy, adds Dazed, exhausts."""
    sim = make_sim(hand=[sts_sim.Card.TURBO], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 5  # 3 + 2 = 5
    discard_cards = [c.card for c in sim.get_discard_pile()]
    assert sts_sim.Card.Dazed in discard_cards
    assert len(sim.get_exhaust_pile()) == 1


def test_turbo_upgraded():
    """Upgraded TURBO gains 3 energy."""
    sim = make_sim(hand=[(sts_sim.Card.TURBO, True)], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 6  # 3 + 3 = 6
    discard_cards = [c.card for c in sim.get_discard_pile()]
    assert sts_sim.Card.Dazed in discard_cards
    assert len(sim.get_exhaust_pile()) == 1


# ===================================================================
# REINFORCED BODY
# ===================================================================

def test_reinforced_body_x1():
    """Reinforced Body with X=1 gains 2 block."""
    sim = make_sim(hand=[sts_sim.Card.ReinforcedBody], energy=3)
    sim.play_card(0, None, 1)  # X=1
    assert sim.player.block == 2  # X+1 = 1+1 = 2
    assert sim.player.energy == 2  # 3 - 1 = 2


def test_reinforced_body_x3():
    """Reinforced Body with X=3 gains 4 block."""
    sim = make_sim(hand=[sts_sim.Card.ReinforcedBody], energy=3)
    sim.play_card(0, None, 3)  # X=3
    assert sim.player.block == 4  # X+1 = 3+1 = 4
    assert sim.player.energy == 0  # 3 - 3 = 0


def test_reinforced_body_upgraded():
    """Upgraded Reinforced Body applies block twice."""
    sim = make_sim(hand=[(sts_sim.Card.ReinforcedBody, True)], energy=3)
    sim.play_card(0, None, 2)  # X=2
    assert sim.player.block == 4  # X*2 = 2+2 = 4
    assert sim.player.energy == 1  # 3 - 2 = 1


# ===================================================================
# CAPACITOR
# ===================================================================

def test_capacitor_base():
    """Capacitor gains 2 orb slots."""
    sim = make_sim(hand=[sts_sim.Card.CapacitorCard], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 2  # 3 - 1 = 2


def test_capacitor_upgraded():
    """Upgraded Capacitor gains 3 orb slots."""
    sim = make_sim(hand=[(sts_sim.Card.CapacitorCard, True)], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 2  # 3 - 1 = 2


# ===================================================================
# CONSUME
# ===================================================================

def test_consume_base():
    """Consume enters play as power, costs 2."""
    sim = make_sim(hand=[sts_sim.Card.ConsumeCard], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_consume_upgraded():
    """Upgraded Consume costs 1."""
    sim = make_sim(hand=[(sts_sim.Card.ConsumeCard, True)], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 2  # 3 - 1 = 2


# ===================================================================
# FUSION
# ===================================================================

def test_fusion_base():
    """Fusion enters play as power, costs 2."""
    sim = make_sim(hand=[sts_sim.Card.FusionCard], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_fusion_upgraded():
    """Upgraded Fusion costs 1."""
    sim = make_sim(hand=[(sts_sim.Card.FusionCard, True)], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 2  # 3 - 1 = 2


# ===================================================================
# HEATSINKS
# ===================================================================

def test_heatsinks_triggers_on_power():
    """Heatsinks draws 2 when a power is played."""
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    sim = make_sim(hand=[sts_sim.Card.HeatsinkCard, sts_sim.Card.StormCard],
                   draw_pile=draw, energy=3)
    sim.play_card(0)  # Play Heatsinks
    hand_before = len(sim.get_hand())
    sim.play_card(0)  # Play Storm (triggers Heatsinks)
    assert len(sim.get_hand()) == hand_before - 1 + 2  # -1 played + 2 drawn


def test_heatsinks_no_trigger_on_attack():
    """Heatsinks does not trigger on non-power cards."""
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    sim = make_sim(hand=[sts_sim.Card.HeatsinkCard, sts_sim.Card.BallLightning],
                   draw_pile=draw, energy=3, monsters=[{"hp": 20}])
    sim.play_card(0)  # Play Heatsinks
    hand_before = len(sim.get_hand())
    sim.play_card(0, 0)  # Play Ball Lightning (attack, no trigger)
    assert len(sim.get_hand()) == hand_before - 1  # -1 played, no draw


# ===================================================================
# LOOP
# ===================================================================

def test_loop_base():
    """Loop enters play as power, costs 1."""
    sim = make_sim(hand=[sts_sim.Card.LoopCard], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 2  # 3 - 1 = 2


# ===================================================================
# MACHINE LEARNING
# ===================================================================

def test_machine_learning_base():
    """Machine Learning enters play as power, costs 1."""
    sim = make_sim(hand=[sts_sim.Card.MachineLearningCard], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 2  # 3 - 1 = 2


def test_machine_learning_upgraded():
    """Upgraded Machine Learning costs 0."""
    sim = make_sim(hand=[(sts_sim.Card.MachineLearningCard, True)], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 3  # cost 0


# ===================================================================
# STORM
# ===================================================================

def test_storm_base():
    """Storm enters play as power, costs 1."""
    sim = make_sim(hand=[sts_sim.Card.StormCard], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 2  # 3 - 1 = 2
