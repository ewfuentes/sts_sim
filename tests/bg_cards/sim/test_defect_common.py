"""Simulator tests for Defect Common cards."""
import sts_sim
from tests.live.conftest import make_sim


# ===================================================================
# Ball Lightning — Attack, Cost 1, 1 HIT + Channel 1 Lightning.
# Upgrade: 2 HIT + Channel 1 Lightning.
# ===================================================================


def test_ball_lightning_damage_and_channel():
    """Ball Lightning deals 1 damage and channels Lightning."""
    sim = make_sim(
        hand=[sts_sim.Card.BallLightning], energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 19
    orbs = sim.get_orbs()
    assert len(orbs) == 1
    assert orbs[0].orb_type == sts_sim.OrbType.Lightning
    assert sim.player.energy == 2


def test_ball_lightning_upgraded_deals_2():
    """Upgraded Ball Lightning deals 2 damage."""
    sim = make_sim(
        hand=[(sts_sim.Card.BallLightning, True)], energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 18
    orbs = sim.get_orbs()
    assert len(orbs) == 1
    assert orbs[0].orb_type == sts_sim.OrbType.Lightning


def test_ball_lightning_full_orb_slots():
    """Ball Lightning with full orb slots evokes oldest orb."""
    sim = make_sim(
        hand=[sts_sim.Card.BallLightning], energy=3, monster_hp=20,
        orbs=["Frost", "Frost", "Frost"],
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 19
    orbs = sim.get_orbs()
    assert len(orbs) == 3
    assert orbs[-1].orb_type == sts_sim.OrbType.Lightning


# ===================================================================
# Barrage — Attack, Cost 1, 1 HIT per Orb.
# Upgrade: 1 HIT per Orb +1.
# ===================================================================


def test_barrage_hits_per_orb():
    """Barrage deals hits equal to number of orbs."""
    sim = make_sim(
        hand=[sts_sim.Card.Barrage], energy=3, monster_hp=20,
        orbs=["Lightning", "Frost", "Dark"],
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 17  # 3 hits of 1 damage


def test_barrage_no_orbs():
    """Barrage with no orbs deals no damage."""
    sim = make_sim(
        hand=[sts_sim.Card.Barrage], energy=3, monster_hp=20,
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 20


def test_barrage_upgraded_extra_hit():
    """Upgraded Barrage deals one extra hit."""
    sim = make_sim(
        hand=[(sts_sim.Card.Barrage, True)], energy=3, monster_hp=20,
        orbs=["Lightning", "Frost"],
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 17  # 2 orbs + 1 = 3 hits of 1 damage


def test_barrage_with_strength():
    """Barrage benefits from Strength on each hit."""
    sim = make_sim(
        hand=[sts_sim.Card.Barrage], energy=3, monster_hp=20,
        orbs=["Lightning", "Frost"],
        player_powers={"Strength": 2},
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 14  # 2 hits of (1+2) = 6 total damage


# ===================================================================
# Beam Cell — Attack, Cost 0, die-dependent VULN.
# [1][2][3] 1 HIT VULN. [4][5][6] 1 HIT.
# Upgrade: Always applies VULN.
# ===================================================================


def test_beam_cell_vuln_on_low_roll():
    """Beam Cell applies Vulnerable on low die roll."""
    sim = make_sim(
        hand=[sts_sim.Card.BeamCell], energy=3, monster_hp=20,
    )
    sim.set_die_value(2)
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 19
    assert monsters[0].get_power(sts_sim.PowerType.Vulnerable) > 0
    assert sim.player.energy == 3  # cost 0


def test_beam_cell_no_vuln_on_high_roll():
    """Beam Cell does not apply Vulnerable on high die roll."""
    sim = make_sim(
        hand=[sts_sim.Card.BeamCell], energy=3, monster_hp=20,
    )
    sim.set_die_value(5)
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 19
    assert monsters[0].get_power(sts_sim.PowerType.Vulnerable) == 0


def test_beam_cell_upgraded_always_vuln():
    """Upgraded Beam Cell always applies Vulnerable."""
    sim = make_sim(
        hand=[(sts_sim.Card.BeamCell, True)], energy=3, monster_hp=20,
    )
    sim.set_die_value(6)
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 19
    assert monsters[0].get_power(sts_sim.PowerType.Vulnerable) > 0


# ===================================================================
# Claw — Attack, Cost 0, 1 HIT.
# +1 damage if topmost discard pile card costs 0.
# Upgrade: +3 damage if topmost discard costs 0.
# ===================================================================


def test_claw_base_no_bonus():
    """Claw deals base 1 damage when discard top is not cost 0."""
    sim = make_sim(
        hand=[sts_sim.Card.Claw], energy=3, monster_hp=20,
        discard_pile=[sts_sim.Card.DefendBlue],  # cost 1
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 19


def test_claw_bonus_from_cost_0_discard():
    """Claw deals 2 damage when discard top is cost 0."""
    sim = make_sim(
        hand=[sts_sim.Card.Claw], energy=3, monster_hp=20,
        discard_pile=[sts_sim.Card.Claw],  # cost 0
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 18  # 1 base + 1 bonus


def test_claw_upgraded_bonus():
    """Upgraded Claw deals 4 damage when discard top is cost 0."""
    sim = make_sim(
        hand=[(sts_sim.Card.Claw, True)], energy=3, monster_hp=20,
        discard_pile=[sts_sim.Card.BeamCell],  # cost 0
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 16  # 1 base + 3 bonus


def test_claw_bonus_stacks_with_strength():
    """Claw bonus stacks with Strength."""
    sim = make_sim(
        hand=[sts_sim.Card.Claw], energy=3, monster_hp=20,
        discard_pile=[sts_sim.Card.Claw],  # cost 0
        player_powers={"Strength": 2},
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 16  # 1 base + 1 bonus + 2 STR = 4


# ===================================================================
# Compile Driver — Attack, Cost 1, 1 HIT + draw per unique orb type.
# Upgrade: 2 HIT + draw per unique orb type.
# ===================================================================


def test_compile_driver_draws_per_unique_orb():
    """Compile Driver draws cards for each unique orb type."""
    sim = make_sim(
        hand=[sts_sim.Card.CompileDriver], energy=3, monster_hp=20,
        orbs=["Lightning", "Frost", "Lightning"],
        draw_pile=[
            sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.StrikeBlue,
        ],
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 19
    # 2 unique orb types (Lightning, Frost) -> draw 2 cards
    hand = sim.get_hand()
    assert len(hand) == 2


def test_compile_driver_no_orbs():
    """Compile Driver with no orbs draws nothing."""
    sim = make_sim(
        hand=[sts_sim.Card.CompileDriver], energy=3, monster_hp=20,
        draw_pile=[
            sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.StrikeBlue,
        ],
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 19
    hand = sim.get_hand()
    assert len(hand) == 0  # no orbs, no draws


def test_compile_driver_upgraded():
    """Upgraded Compile Driver deals 2 damage."""
    sim = make_sim(
        hand=[(sts_sim.Card.CompileDriver, True)], energy=3, monster_hp=20,
        orbs=["Dark"],
        draw_pile=[
            sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.StrikeBlue,
        ],
    )
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 18  # 2 HIT
    hand = sim.get_hand()
    assert len(hand) == 1  # 1 unique orb type


# ===================================================================
# Go for the Eyes — Attack, Cost 0, die-dependent WEAK.
# [1][2][3] 1 HIT. [4][5][6] 1 HIT WEAK.
# Upgrade: Always applies WEAK.
# ===================================================================


def test_go_for_the_eyes_weak_on_high_roll():
    """Go for the Eyes applies Weak on high die roll."""
    sim = make_sim(
        hand=[sts_sim.Card.GoForTheEyes], energy=3, monster_hp=20,
    )
    sim.set_die_value(4)
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 19
    assert monsters[0].get_power(sts_sim.PowerType.Weak) > 0
    assert sim.player.energy == 3  # cost 0


def test_go_for_the_eyes_no_weak_on_low_roll():
    """Go for the Eyes does not apply Weak on low die roll."""
    sim = make_sim(
        hand=[sts_sim.Card.GoForTheEyes], energy=3, monster_hp=20,
    )
    # Die is already 1 from make_sim
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 19
    assert monsters[0].get_power(sts_sim.PowerType.Weak) == 0


def test_go_for_the_eyes_upgraded_always_weak():
    """Upgraded Go for the Eyes always applies Weak."""
    sim = make_sim(
        hand=[(sts_sim.Card.GoForTheEyes, True)], energy=3, monster_hp=20,
    )
    sim.set_die_value(2)
    sim.play_card(0, 0)
    monsters = sim.get_monsters()
    assert monsters[0].hp == 19
    assert monsters[0].get_power(sts_sim.PowerType.Weak) > 0


# ===================================================================
# Sweeping Beam — Attack, Cost 1, AOE 1 HIT + Draw 1.
# Upgrade: AOE 2 HIT + Draw 1.
# ===================================================================


def test_sweeping_beam_aoe_and_draw():
    """Sweeping Beam hits all enemies and draws a card."""
    sim = make_sim(
        hand=[sts_sim.Card.SweepingBeam], energy=3,
        monsters=[{"hp": 10}, {"hp": 10}, {"hp": 10}],
        draw_pile=[
            sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.StrikeBlue,
        ],
    )
    sim.play_card(0)  # AOE, no target
    monsters = sim.get_monsters()
    for m in monsters:
        assert m.hp == 9  # 1 damage each
    hand = sim.get_hand()
    assert len(hand) == 1  # drew 1 card
    assert sim.player.energy == 2


def test_sweeping_beam_upgraded():
    """Upgraded Sweeping Beam deals 2 damage to all enemies."""
    sim = make_sim(
        hand=[(sts_sim.Card.SweepingBeam, True)], energy=3,
        monsters=[{"hp": 10}, {"hp": 10}],
        draw_pile=[
            sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.StrikeBlue,
        ],
    )
    sim.play_card(0)
    monsters = sim.get_monsters()
    for m in monsters:
        assert m.hp == 8  # 2 damage each


def test_sweeping_beam_with_strength():
    """Sweeping Beam with Strength hits all enemies for boosted damage."""
    sim = make_sim(
        hand=[sts_sim.Card.SweepingBeam], energy=3,
        monsters=[{"hp": 20}, {"hp": 20}],
        player_powers={"Strength": 3},
        draw_pile=[sts_sim.Card.StrikeBlue],
    )
    sim.play_card(0)
    monsters = sim.get_monsters()
    for m in monsters:
        assert m.hp == 16  # 1 base + 3 STR = 4 per enemy


# ===================================================================
# Charge Battery — Skill, Cost 1, 2 BLK. Energy if >= 3 orbs.
# Upgrade: 3 BLK.
# ===================================================================


def test_charge_battery_block_no_energy():
    """Charge Battery grants 2 block without enough orbs."""
    sim = make_sim(
        hand=[sts_sim.Card.ChargeBattery], energy=3, player_block=0,
        orbs=["Lightning", "Frost"],
    )
    sim.play_card(0)
    assert sim.player.block == 2
    assert sim.player.energy == 2  # no bonus energy


def test_charge_battery_block_and_energy():
    """Charge Battery grants block and energy with 3 orbs."""
    sim = make_sim(
        hand=[sts_sim.Card.ChargeBattery], energy=3, player_block=0,
        orbs=["Lightning", "Frost", "Dark"],
    )
    sim.play_card(0)
    assert sim.player.block == 2
    assert sim.player.energy == 3  # spent 1, gained 1 back


def test_charge_battery_upgraded():
    """Upgraded Charge Battery grants 3 block."""
    sim = make_sim(
        hand=[(sts_sim.Card.ChargeBattery, True)], energy=3, player_block=0,
        orbs=["Lightning"],
    )
    sim.play_card(0)
    assert sim.player.block == 3
    assert sim.player.energy == 2  # fewer than 3 orbs, no bonus


# ===================================================================
# Chaos — Skill, Cost 1, Channel orb based on die.
# [1][2] Lightning, [3][4] Frost, [5][6] Dark.
# Upgrade: Cost 0.
# ===================================================================


def test_chaos_lightning_on_low_roll():
    """Chaos channels Lightning on die roll 1 or 2."""
    sim = make_sim(hand=[sts_sim.Card.Chaos], energy=3, monster_hp=20)
    sim.set_die_value(2)
    sim.play_card(0)
    orbs = sim.get_orbs()
    assert len(orbs) == 1
    assert orbs[0].orb_type == sts_sim.OrbType.Lightning
    assert sim.player.energy == 2


def test_chaos_frost_on_mid_roll():
    """Chaos channels Frost on die roll 3 or 4."""
    sim = make_sim(hand=[sts_sim.Card.Chaos], energy=3, monster_hp=20)
    sim.set_die_value(3)
    sim.play_card(0)
    orbs = sim.get_orbs()
    assert len(orbs) == 1
    assert orbs[0].orb_type == sts_sim.OrbType.Frost


def test_chaos_dark_on_high_roll():
    """Chaos channels Dark on die roll 5 or 6."""
    sim = make_sim(hand=[sts_sim.Card.Chaos], energy=3, monster_hp=20)
    sim.set_die_value(6)
    sim.play_card(0)
    orbs = sim.get_orbs()
    assert len(orbs) == 1
    assert orbs[0].orb_type == sts_sim.OrbType.Dark


def test_chaos_upgraded_costs_0():
    """Upgraded Chaos costs 0."""
    sim = make_sim(hand=[(sts_sim.Card.Chaos, True)], energy=3, monster_hp=20)
    sim.set_die_value(4)
    sim.play_card(0)
    orbs = sim.get_orbs()
    assert len(orbs) == 1
    assert orbs[0].orb_type == sts_sim.OrbType.Frost
    assert sim.player.energy == 3


# ===================================================================
# Coolheaded — Skill, Cost 1, Channel 1 Frost.
# Upgrade: Channel 1 Frost + Draw 1.
# ===================================================================


def test_coolheaded_channels_frost():
    """Coolheaded channels a Frost orb."""
    sim = make_sim(hand=[sts_sim.Card.Coolheaded], energy=3, monster_hp=20)
    sim.play_card(0)
    orbs = sim.get_orbs()
    assert len(orbs) == 1
    assert orbs[0].orb_type == sts_sim.OrbType.Frost
    assert sim.player.energy == 2


def test_coolheaded_upgraded_draws():
    """Upgraded Coolheaded channels Frost and draws a card."""
    sim = make_sim(
        hand=[(sts_sim.Card.Coolheaded, True)], energy=3, monster_hp=20,
        draw_pile=[
            sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.StrikeBlue, sts_sim.Card.DefendBlue,
            sts_sim.Card.StrikeBlue,
        ],
    )
    sim.play_card(0)
    orbs = sim.get_orbs()
    assert len(orbs) == 1
    assert orbs[0].orb_type == sts_sim.OrbType.Frost
    hand = sim.get_hand()
    assert len(hand) == 1  # drew 1 card
    assert sim.player.energy == 2


def test_coolheaded_full_orb_slots():
    """Coolheaded with full orb slots evokes oldest orb."""
    sim = make_sim(
        hand=[sts_sim.Card.Coolheaded], energy=3, monster_hp=20,
        orbs=["Lightning", "Lightning", "Lightning"],
    )
    sim.play_card(0)
    orbs = sim.get_orbs()
    assert len(orbs) == 3
    assert orbs[-1].orb_type == sts_sim.OrbType.Frost
    # Leftmost Lightning was evoked; remaining two are Lightning
    assert orbs[0].orb_type == sts_sim.OrbType.Lightning
    assert orbs[1].orb_type == sts_sim.OrbType.Lightning


# ===================================================================
# Leap — Skill, Cost 1, 2 BLK to any player.
# Upgrade: 3 BLK to any player.
# ===================================================================


def test_leap_block_to_self():
    """Leap grants 2 block to self."""
    sim = make_sim(hand=[sts_sim.Card.Leap], energy=3, player_block=0)
    sim.play_card(0)
    assert sim.player.block == 2
    assert sim.player.energy == 2


def test_leap_upgraded_block():
    """Upgraded Leap grants 3 block."""
    sim = make_sim(
        hand=[(sts_sim.Card.Leap, True)], energy=3, player_block=0,
    )
    sim.play_card(0)
    assert sim.player.block == 3
    assert sim.player.energy == 2


# ===================================================================
# Recursion — Skill, Cost 1, Evoke 1 Orb + Channel same type.
# Upgrade: Cost 0.
# ===================================================================


def test_recursion_evokes_and_rechannels_lightning():
    """Recursion evokes and re-channels a Lightning orb."""
    sim = make_sim(
        hand=[sts_sim.Card.Recursion], energy=3, monster_hp=20,
        orbs=["Lightning"],
    )
    sim.play_card(0)
    orbs = sim.get_orbs()
    assert len(orbs) == 1
    assert orbs[0].orb_type == sts_sim.OrbType.Lightning
    assert sim.player.energy == 2
    # Lightning was evoked -> damage dealt
    monsters = sim.get_monsters()
    assert monsters[0].hp < 20


def test_recursion_evokes_frost():
    """Recursion evokes Frost and re-channels it."""
    sim = make_sim(
        hand=[sts_sim.Card.Recursion], energy=3, monster_hp=20,
        player_block=0, orbs=["Frost"],
    )
    sim.play_card(0)
    orbs = sim.get_orbs()
    assert len(orbs) == 1
    assert orbs[0].orb_type == sts_sim.OrbType.Frost
    # Frost evoked -> player gained block
    assert sim.player.block > 0


def test_recursion_upgraded_costs_0():
    """Upgraded Recursion costs 0."""
    sim = make_sim(
        hand=[(sts_sim.Card.Recursion, True)], energy=3, monster_hp=20,
        orbs=["Dark"],
    )
    sim.play_card(0)
    assert sim.player.energy == 3
    orbs = sim.get_orbs()
    assert len(orbs) == 1
    assert orbs[0].orb_type == sts_sim.OrbType.Dark


def test_recursion_no_orbs():
    """Recursion with no orbs does nothing."""
    sim = make_sim(
        hand=[sts_sim.Card.Recursion], energy=3, monster_hp=20,
    )
    sim.play_card(0)
    assert sim.player.energy == 2
    orbs = sim.get_orbs()
    assert len(orbs) == 0
    monsters = sim.get_monsters()
    assert monsters[0].hp == 20


# ===================================================================
# Steam Barrier — Skill, Cost 0, 1 BLK.
# +1 BLK if topmost discard costs 0.
# Upgrade: 2 BLK + conditional +1.
# ===================================================================


def test_steam_barrier_base_no_bonus():
    """Steam Barrier grants 1 block when discard top is not cost 0."""
    sim = make_sim(
        hand=[sts_sim.Card.SteamBarrier], energy=3, player_block=0,
        discard_pile=[sts_sim.Card.DefendBlue],  # cost 1
    )
    sim.play_card(0)
    assert sim.player.block == 1
    assert sim.player.energy == 3  # cost 0


def test_steam_barrier_bonus_from_cost_0():
    """Steam Barrier grants 2 block when discard top is cost 0."""
    sim = make_sim(
        hand=[sts_sim.Card.SteamBarrier], energy=3, player_block=0,
        discard_pile=[sts_sim.Card.Claw],  # cost 0
    )
    sim.play_card(0)
    assert sim.player.block == 2  # 1 base + 1 bonus


def test_steam_barrier_upgraded_bonus():
    """Upgraded Steam Barrier grants 3 block when discard top is cost 0."""
    sim = make_sim(
        hand=[(sts_sim.Card.SteamBarrier, True)], energy=3, player_block=0,
        discard_pile=[sts_sim.Card.BeamCell],  # cost 0
    )
    sim.play_card(0)
    assert sim.player.block == 3  # 2 base + 1 bonus


def test_steam_barrier_empty_discard():
    """Steam Barrier with empty discard pile grants only base block."""
    sim = make_sim(
        hand=[sts_sim.Card.SteamBarrier], energy=3, player_block=0,
    )
    sim.play_card(0)
    assert sim.player.block == 1  # base only, no bonus
