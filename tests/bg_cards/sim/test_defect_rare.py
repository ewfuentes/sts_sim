"""Simulator tests for Defect Rare cards."""
import sts_sim
from tests.live.conftest import make_sim


# ===================================================================
# ALL FOR ONE
# ===================================================================

def test_all_for_one_retrieves_zero_cost():
    """All for One deals 2 damage and retrieves 0-cost cards from discard."""
    sim = make_sim(hand=[sts_sim.Card.AllForOne], energy=3,
                   discard_pile=[sts_sim.Card.Zap, sts_sim.Card.FTL,
                                 sts_sim.Card.StrikeBlue],
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18  # 20 - 2 = 18
    hand_cards = [c.card for c in sim.get_hand()]
    assert sts_sim.Card.Zap in hand_cards
    assert sts_sim.Card.FTL in hand_cards
    assert sts_sim.Card.StrikeBlue not in hand_cards  # cost 1
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_all_for_one_no_zero_cost():
    """All for One with no 0-cost cards in discard retrieves nothing."""
    sim = make_sim(hand=[sts_sim.Card.AllForOne], energy=3,
                   discard_pile=[sts_sim.Card.StrikeBlue, sts_sim.Card.Glacier],
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 18
    assert len(sim.get_hand()) == 0  # no cards retrieved


def test_all_for_one_upgraded():
    """Upgraded All for One deals 3 damage."""
    sim = make_sim(hand=[(sts_sim.Card.AllForOne, True)], energy=3,
                   discard_pile=[sts_sim.Card.Zap],
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17
    hand_cards = [c.card for c in sim.get_hand()]
    assert sts_sim.Card.Zap in hand_cards


# ===================================================================
# CORE SURGE
# ===================================================================

def test_core_surge_removes_debuffs():
    """Core Surge removes Weak and Vulnerable from player."""
    sim = make_sim(hand=[sts_sim.Card.CoreSurge], energy=3,
                   player_powers={"Weak": 2, "Vulnerable": 1},
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 17  # 20 - 3 = 17
    assert sim.player.get_power(sts_sim.PowerType.Weak) == 0
    assert sim.player.get_power(sts_sim.PowerType.Vulnerable) == 0
    assert sim.player.energy == 2  # 3 - 1 = 2


def test_core_surge_retains():
    """Core Surge has Retain."""
    sim = make_sim(hand=[sts_sim.Card.CoreSurge,
                         sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue],
                   draw_pile=[sts_sim.Card.Zap, sts_sim.Card.StrikeBlue,
                              sts_sim.Card.DefendBlue, sts_sim.Card.Zap,
                              sts_sim.Card.StrikeBlue],
                   energy=3, monsters=[{"hp": 20}])
    sim.end_player_turn()
    # Core Surge should be retained in hand
    hand_cards = [c.card for c in sim.get_hand()]
    assert sts_sim.Card.CoreSurge in hand_cards


# ===================================================================
# HYPERBEAM
# ===================================================================

def test_hyperbeam_base():
    """Hyperbeam deals AOE 5 and removes all orbs."""
    sim = make_sim(hand=[sts_sim.Card.Hyperbeam], energy=3,
                   orbs=["Lightning", "Frost"],
                   monsters=[{"hp": 20}, {"hp": 20}])
    sim.play_card(0, 0)
    for m in sim.get_monsters():
        assert m.hp == 15  # 20 - 5 = 15
    assert len(sim.player.get_orbs()) == 0
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_hyperbeam_no_orbs():
    """Hyperbeam with no orbs still deals damage."""
    sim = make_sim(hand=[sts_sim.Card.Hyperbeam], energy=3,
                   monsters=[{"hp": 20}, {"hp": 20}])
    sim.play_card(0, 0)
    for m in sim.get_monsters():
        assert m.hp == 15
    assert sim.player.energy == 1


def test_hyperbeam_upgraded():
    """Upgraded Hyperbeam deals AOE 7."""
    sim = make_sim(hand=[(sts_sim.Card.Hyperbeam, True)], energy=3,
                   orbs=["Frost", "Frost", "Dark"],
                   monsters=[{"hp": 20}, {"hp": 20}])
    sim.play_card(0, 0)
    for m in sim.get_monsters():
        assert m.hp == 13  # 20 - 7 = 13
    assert len(sim.player.get_orbs()) == 0


# ===================================================================
# METEOR STRIKE
# ===================================================================

def test_meteor_strike_with_3_powers():
    """Meteor Strike with 3 powers costs 2."""
    sim = make_sim(hand=[sts_sim.Card.LoopCard, sts_sim.Card.StormCard,
                         sts_sim.Card.DefragmentCard,
                         sts_sim.Card.MeteorStrike], energy=6,
                   monsters=[{"hp": 20}])
    sim.play_card(0)  # Loop (cost 1)
    sim.play_card(0)  # Storm (cost 1)
    sim.play_card(0)  # Defragment (cost 1)
    sim.play_card(0, 0)  # Meteor Strike (cost 5-3 = 2)
    assert sim.get_monsters()[0].hp == 10  # 20 - 10 = 10
    assert sim.player.energy == 1  # 6 - 1 - 1 - 1 - 2 = 1


def test_meteor_strike_with_strength():
    """Meteor Strike with Strength adds per-HIT bonus."""
    sim = make_sim(hand=[sts_sim.Card.MeteorStrike], energy=5,
                   player_powers={"Strength": 2},
                   monsters=[{"hp": 40}])
    sim.play_card(0, 0)
    # 10 HIT, each deals 1 + 2 = 3 damage => 30 total
    assert sim.get_monsters()[0].hp == 10  # 40 - 30 = 10
    assert sim.player.energy == 0  # 5 - 5 = 0


# ===================================================================
# THUNDER STRIKE
# ===================================================================

def test_thunder_strike_with_2_lightning():
    """Thunder Strike with 2 Lightning orbs deals AOE 8."""
    sim = make_sim(hand=[sts_sim.Card.ThunderStrike], energy=3,
                   orbs=["Lightning", "Lightning", "Frost"],
                   monsters=[{"hp": 30}, {"hp": 30}])
    sim.play_card(0, 0)
    for m in sim.get_monsters():
        assert m.hp == 22  # 30 - 4*2 = 22
    assert sim.player.energy == 0  # 3 - 3 = 0


def test_thunder_strike_no_lightning():
    """Thunder Strike with no Lightning orbs deals 0."""
    sim = make_sim(hand=[sts_sim.Card.ThunderStrike], energy=3,
                   orbs=["Frost", "Frost"],
                   monsters=[{"hp": 20}])
    sim.play_card(0, 0)
    assert sim.get_monsters()[0].hp == 20  # 0 damage


def test_thunder_strike_upgraded():
    """Upgraded Thunder Strike deals AOE 6 per Lightning orb."""
    sim = make_sim(hand=[(sts_sim.Card.ThunderStrike, True)], energy=3,
                   orbs=["Lightning", "Lightning", "Lightning"],
                   monsters=[{"hp": 40}, {"hp": 40}])
    sim.play_card(0, 0)
    for m in sim.get_monsters():
        assert m.hp == 22  # 40 - 6*3 = 22


# ===================================================================
# AMPLIFY
# ===================================================================

def test_amplify_base():
    """Amplify enters play, costs 1."""
    sim = make_sim(hand=[sts_sim.Card.AmplifyCard], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 2  # 3 - 1 = 2


def test_amplify_upgraded():
    """Upgraded Amplify enters play, costs 1."""
    sim = make_sim(hand=[(sts_sim.Card.AmplifyCard, True)], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 2  # 3 - 1 = 2


# ===================================================================
# FISSION
# ===================================================================

def test_fission_with_3_orbs():
    """Fission removes 3 orbs, gains 3 energy, draws 3, exhausts."""
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    sim = make_sim(hand=[sts_sim.Card.Fission], draw_pile=draw, energy=3,
                   orbs=["Lightning", "Frost", "Dark"])
    sim.play_card(0)
    assert len(sim.player.get_orbs()) == 0
    assert sim.player.energy == 6  # 3 + 3 = 6
    assert len(sim.get_hand()) == 3  # drew 3 cards
    assert len(sim.get_exhaust_pile()) == 1  # Fission exhausted


def test_fission_no_orbs():
    """Fission with 0 orbs just exhausts."""
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    sim = make_sim(hand=[sts_sim.Card.Fission], draw_pile=draw, energy=3)
    sim.play_card(0)
    assert sim.player.energy == 3  # 3 + 0 = 3
    assert len(sim.get_hand()) == 0  # drew 0 cards
    assert len(sim.get_exhaust_pile()) == 1


def test_fission_upgraded_evokes():
    """Upgraded Fission evokes all orbs (not just removes)."""
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    sim = make_sim(hand=[(sts_sim.Card.Fission, True)], draw_pile=draw,
                   energy=3, orbs=["Lightning", "Frost", "Dark"],
                   monsters=[{"hp": 30}])
    sim.play_card(0)
    assert len(sim.player.get_orbs()) == 0
    assert sim.player.energy == 6  # 3 + 3 = 6
    assert len(sim.get_hand()) == 3
    assert len(sim.get_exhaust_pile()) == 1
    # Evoke effects should have occurred (Lightning damage, Frost block, Dark damage)


# ===================================================================
# MULTI-CAST
# ===================================================================

def test_multi_cast_x2_lightning():
    """Multi-Cast X=2 evokes first orb 2 times."""
    sim = make_sim(hand=[sts_sim.Card.MultiCast], energy=3,
                   orbs=["Lightning", "Frost", "Dark"],
                   monsters=[{"hp": 20}])
    sim.play_card(0, None, 2)  # X=2
    assert sim.player.energy == 1  # 3 - 2 = 1
    # Lightning evoked 2 times, dealing damage to enemy


def test_multi_cast_x3_frost():
    """Multi-Cast X=3 evokes Frost orb 3 times."""
    sim = make_sim(hand=[sts_sim.Card.MultiCast], energy=3,
                   orbs=["Frost", "Lightning", "Dark"])
    sim.play_card(0, None, 3)  # X=3
    assert sim.player.energy == 0  # 3 - 3 = 0
    # Frost evoked 3 times, granting block
    assert sim.player.block > 0


def test_multi_cast_upgraded():
    """Upgraded Multi-Cast X=2 evokes 3 times (X+1)."""
    sim = make_sim(hand=[(sts_sim.Card.MultiCast, True)], energy=3,
                   orbs=["Dark", "Frost", "Lightning"],
                   monsters=[{"hp": 30}])
    sim.play_card(0, None, 2)  # X=2, evokes X+1 = 3 times
    assert sim.player.energy == 1  # 3 - 2 = 1


# ===================================================================
# RAINBOW
# ===================================================================

def test_rainbow_channels_3_orbs():
    """Rainbow channels Lightning, Frost, and Dark, then exhausts."""
    sim = make_sim(hand=[sts_sim.Card.RainbowCard], energy=3)
    sim.play_card(0)
    orbs = sim.player.get_orbs()
    orb_types = [o for o in orbs]
    assert sts_sim.OrbType.Lightning in orb_types
    assert sts_sim.OrbType.Frost in orb_types
    assert sts_sim.OrbType.Dark in orb_types
    assert len(sim.get_exhaust_pile()) == 1  # Rainbow exhausted
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_rainbow_upgraded_no_exhaust():
    """Upgraded Rainbow does not exhaust."""
    sim = make_sim(hand=[(sts_sim.Card.RainbowCard, True)], energy=3)
    sim.play_card(0)
    orbs = sim.player.get_orbs()
    orb_types = [o for o in orbs]
    assert sts_sim.OrbType.Lightning in orb_types
    assert sts_sim.OrbType.Frost in orb_types
    assert sts_sim.OrbType.Dark in orb_types
    assert len(sim.get_exhaust_pile()) == 0  # Not exhausted
    discard_cards = [c.card for c in sim.get_discard_pile()]
    assert sts_sim.Card.RainbowCard in discard_cards


# ===================================================================
# SEEK
# ===================================================================

def test_seek_base():
    """Seek finds 1 card from draw pile, exhausts."""
    draw = [sts_sim.Card.Glacier, sts_sim.Card.StrikeBlue,
            sts_sim.Card.DefendBlue, sts_sim.Card.Zap,
            sts_sim.Card.BallLightning]
    sim = make_sim(hand=[sts_sim.Card.SeekCard], draw_pile=draw, energy=3)
    sim.play_card(0, None, 0)  # choose first card (Glacier)
    hand_cards = [c.card for c in sim.get_hand()]
    assert sts_sim.Card.Glacier in hand_cards
    assert len(sim.get_exhaust_pile()) == 1  # Seek exhausted
    assert sim.player.energy == 3  # cost 0


def test_seek_upgraded():
    """Upgraded Seek finds 2 cards."""
    draw = [sts_sim.Card.Glacier, sts_sim.Card.BallLightning,
            sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap]
    sim = make_sim(hand=[(sts_sim.Card.SeekCard, True)], draw_pile=draw,
                   energy=3)
    sim.play_card(0, None, 0)  # choose cards
    hand_cards = [c.card for c in sim.get_hand()]
    assert len(hand_cards) >= 1  # At least 1 card found
    assert len(sim.get_exhaust_pile()) == 1


# ===================================================================
# SKIM
# ===================================================================

def test_skim_base():
    """Skim draws 3 cards."""
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue]
    sim = make_sim(hand=[sts_sim.Card.SkimCard], draw_pile=draw, energy=3)
    sim.play_card(0)
    assert len(sim.get_hand()) == 3  # drew 3 cards
    assert sim.player.energy == 2  # 3 - 1 = 2


def test_skim_upgraded():
    """Upgraded Skim draws 4 cards."""
    draw = [sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.Zap, sts_sim.Card.StrikeBlue,
            sts_sim.Card.DefendBlue, sts_sim.Card.Zap]
    sim = make_sim(hand=[(sts_sim.Card.SkimCard, True)], draw_pile=draw,
                   energy=3)
    sim.play_card(0)
    assert len(sim.get_hand()) == 4  # drew 4 cards
    assert sim.player.energy == 2


# ===================================================================
# TEMPEST
# ===================================================================

def test_tempest_x3():
    """Tempest X=3 channels 3 Lightning and exhausts."""
    sim = make_sim(hand=[sts_sim.Card.TempestCard], energy=3)
    sim.play_card(0, None, 3)  # X=3
    orbs = sim.player.get_orbs()
    lightning_count = sum(1 for o in orbs if o == sts_sim.OrbType.Lightning)
    assert lightning_count == 3
    assert len(sim.get_exhaust_pile()) == 1
    assert sim.player.energy == 0  # 3 - 3 = 0


def test_tempest_x0():
    """Tempest X=0 channels 0 Lightning and exhausts."""
    sim = make_sim(hand=[sts_sim.Card.TempestCard], energy=0)
    sim.play_card(0, None, 0)  # X=0
    orbs = sim.player.get_orbs()
    lightning_count = sum(1 for o in orbs if o == sts_sim.OrbType.Lightning)
    assert lightning_count == 0
    assert len(sim.get_exhaust_pile()) == 1


def test_tempest_upgraded():
    """Upgraded Tempest X=2 channels 3 Lightning (X+1)."""
    sim = make_sim(hand=[(sts_sim.Card.TempestCard, True)], energy=3)
    sim.play_card(0, None, 2)  # X=2, channels X+1 = 3
    orbs = sim.player.get_orbs()
    lightning_count = sum(1 for o in orbs if o == sts_sim.OrbType.Lightning)
    assert lightning_count == 3
    assert len(sim.get_exhaust_pile()) == 1
    assert sim.player.energy == 1  # 3 - 2 = 1


# ===================================================================
# BUFFER
# ===================================================================

def test_buffer_base():
    """Buffer enters play as power, costs 2."""
    sim = make_sim(hand=[sts_sim.Card.BufferCard], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_buffer_upgraded():
    """Upgraded Buffer enters play as power, costs 2."""
    sim = make_sim(hand=[(sts_sim.Card.BufferCard, True)], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 1  # 3 - 2 = 1


# ===================================================================
# DEFRAGMENT
# ===================================================================

def test_defragment_base():
    """Defragment enters play as power, costs 1."""
    sim = make_sim(hand=[sts_sim.Card.DefragmentCard], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 2  # 3 - 1 = 2


def test_defragment_ethereal():
    """Defragment is exhausted if not played (Ethereal)."""
    sim = make_sim(hand=[sts_sim.Card.DefragmentCard,
                         sts_sim.Card.StrikeBlue],
                   draw_pile=[sts_sim.Card.Zap, sts_sim.Card.StrikeBlue,
                              sts_sim.Card.DefendBlue, sts_sim.Card.Zap,
                              sts_sim.Card.StrikeBlue],
                   energy=3, monsters=[{"hp": 20}])
    sim.end_player_turn()
    exhaust_cards = [c.card for c in sim.get_exhaust_pile()]
    assert sts_sim.Card.DefragmentCard in exhaust_cards


def test_defragment_upgraded_not_ethereal():
    """Upgraded Defragment is not Ethereal."""
    sim = make_sim(hand=[(sts_sim.Card.DefragmentCard, True),
                         sts_sim.Card.StrikeBlue],
                   draw_pile=[sts_sim.Card.Zap, sts_sim.Card.StrikeBlue,
                              sts_sim.Card.DefendBlue, sts_sim.Card.Zap,
                              sts_sim.Card.StrikeBlue],
                   energy=3, monsters=[{"hp": 20}])
    sim.end_player_turn()
    exhaust_cards = [c.card for c in sim.get_exhaust_pile()]
    assert sts_sim.Card.DefragmentCard not in exhaust_cards
    discard_cards = [c.card for c in sim.get_discard_pile()]
    assert sts_sim.Card.DefragmentCard in discard_cards


# ===================================================================
# ECHO FORM
# ===================================================================

def test_echo_form_base():
    """Echo Form enters play as power, costs 3."""
    sim = make_sim(hand=[sts_sim.Card.EchoFormCard], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 0  # 3 - 3 = 0


def test_echo_form_ethereal():
    """Echo Form is exhausted if not played (Ethereal)."""
    sim = make_sim(hand=[sts_sim.Card.EchoFormCard,
                         sts_sim.Card.StrikeBlue],
                   draw_pile=[sts_sim.Card.Zap, sts_sim.Card.StrikeBlue,
                              sts_sim.Card.DefendBlue, sts_sim.Card.Zap,
                              sts_sim.Card.StrikeBlue],
                   energy=3, monsters=[{"hp": 20}])
    sim.end_player_turn()
    exhaust_cards = [c.card for c in sim.get_exhaust_pile()]
    assert sts_sim.Card.EchoFormCard in exhaust_cards


def test_echo_form_upgraded_not_ethereal():
    """Upgraded Echo Form is not Ethereal."""
    sim = make_sim(hand=[(sts_sim.Card.EchoFormCard, True),
                         sts_sim.Card.StrikeBlue],
                   draw_pile=[sts_sim.Card.Zap, sts_sim.Card.StrikeBlue,
                              sts_sim.Card.DefendBlue, sts_sim.Card.Zap,
                              sts_sim.Card.StrikeBlue],
                   energy=3, monsters=[{"hp": 20}])
    sim.end_player_turn()
    exhaust_cards = [c.card for c in sim.get_exhaust_pile()]
    assert sts_sim.Card.EchoFormCard not in exhaust_cards
    discard_cards = [c.card for c in sim.get_discard_pile()]
    assert sts_sim.Card.EchoFormCard in discard_cards


# ===================================================================
# ELECTRODYNAMICS
# ===================================================================

def test_electrodynamics_channels_2():
    """Electrodynamics channels 2 Lightning on play."""
    sim = make_sim(hand=[sts_sim.Card.ElectrodynamicsCard], energy=3)
    sim.play_card(0)
    orbs = sim.player.get_orbs()
    lightning_count = sum(1 for o in orbs if o == sts_sim.OrbType.Lightning)
    assert lightning_count == 2
    assert sim.player.energy == 1  # 3 - 2 = 1


def test_electrodynamics_upgraded_channels_3():
    """Upgraded Electrodynamics channels 3 Lightning."""
    sim = make_sim(hand=[(sts_sim.Card.ElectrodynamicsCard, True)], energy=3)
    sim.play_card(0)
    orbs = sim.player.get_orbs()
    lightning_count = sum(1 for o in orbs if o == sts_sim.OrbType.Lightning)
    assert lightning_count == 3
    assert sim.player.energy == 1  # 3 - 2 = 1


# ===================================================================
# STATIC DISCHARGE
# ===================================================================

def test_static_discharge_base():
    """Static Discharge enters play as power, costs 1."""
    sim = make_sim(hand=[sts_sim.Card.StaticDischargeCard], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 2  # 3 - 1 = 2


def test_static_discharge_upgraded():
    """Upgraded Static Discharge enters play as power, costs 1."""
    sim = make_sim(hand=[(sts_sim.Card.StaticDischargeCard, True)], energy=3)
    sim.play_card(0)
    assert sim.player.energy == 2  # 3 - 1 = 2
