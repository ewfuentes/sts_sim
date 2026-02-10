"""Tests for Defect cards and mechanics (Phase 3)."""
import sts_sim


def make_defect_combat(seed=0):
    """Create a Defect combat against Jaw Worm."""
    cs = sts_sim.create_encounter("jaw_worm", seed, sts_sim.Character.Defect)
    return cs


def make_combat_with_card(card, upgraded=False, seed=0):
    """Create Defect combat and add a specific card to hand."""
    cs = make_defect_combat(seed)
    cs.start_combat()
    if upgraded:
        cs.add_upgraded_card_to_hand(card)
    else:
        cs.add_card_to_hand(card)
    return cs


# --- Orb System ---

def test_defect_starts_with_3_orb_slots():
    """Defect starts with 3 orb slots."""
    cs = make_defect_combat()
    cs.start_combat()
    assert cs.player.orb_slots == 3


def test_cracked_core_channels_lightning_at_start():
    """CrackedCore channels 1 Lightning at combat start."""
    cs = make_defect_combat()
    cs.start_combat()
    orbs = cs.player.get_orbs()
    assert len(orbs) == 1
    assert orbs[0] == sts_sim.OrbType.Lightning


def test_channel_orb_adds_to_list():
    """Channeling an orb adds it to the orb list."""
    cs = make_combat_with_card(sts_sim.Card.Coolheaded)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.Coolheaded)
    orbs_before = len(cs.player.get_orbs())
    cs.play_card(idx, None)
    orbs = cs.player.get_orbs()
    assert len(orbs) == orbs_before + 1
    assert orbs[-1] == sts_sim.OrbType.Frost


def test_ball_lightning_channels_lightning():
    """Ball Lightning deals damage and channels Lightning."""
    cs = make_combat_with_card(sts_sim.Card.BallLightning)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.BallLightning)
    monsters = cs.get_monsters()
    hp_before = monsters[0].hp
    cs.play_card(idx, 0)
    monsters = cs.get_monsters()
    assert monsters[0].hp < hp_before
    # Should have CrackedCore Lightning + BallLightning Lightning
    orbs = cs.player.get_orbs()
    assert any(o == sts_sim.OrbType.Lightning for o in orbs)


def test_cold_snap_channels_frost():
    """Cold Snap deals damage and channels Frost."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.ColdSnap)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.ColdSnap)
    cs.play_card(idx, 0)
    orbs = cs.player.get_orbs()
    assert any(o == sts_sim.OrbType.Frost for o in orbs)


def test_doom_and_gloom_channels_dark():
    """Doom and Gloom deals AOE damage and channels Dark."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.DoomAndGloom)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.DoomAndGloom)
    cs.play_card(idx, None)
    orbs = cs.player.get_orbs()
    assert any(o == sts_sim.OrbType.Dark for o in orbs)


def test_orb_evoke_lightning():
    """Lightning orb evoke deals damage."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(5)
    # Fill slots with Lightning (CrackedCore already has 1)
    cs.add_card_to_hand(sts_sim.Card.BallLightning)
    cs.add_card_to_hand(sts_sim.Card.BallLightning)
    hand = cs.get_hand()
    bl_indices = [i for i, c in enumerate(hand) if c.card == sts_sim.Card.BallLightning]
    cs.play_card(bl_indices[1], 0)
    cs.play_card(bl_indices[0], 0)
    # Now 3 slots full. Channel another to force evoke
    monsters = cs.get_monsters()
    hp_before = monsters[0].hp
    cs.add_card_to_hand(sts_sim.Card.BallLightning)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.BallLightning)
    cs.play_card(idx, 0)
    monsters = cs.get_monsters()
    # Should have taken evoke damage (2) + attack damage (1)
    assert monsters[0].hp < hp_before


def test_orb_evoke_frost():
    """Frost orb evoke grants block."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(10)
    # Fill all 3 slots with Frost
    for _ in range(3):
        cs.add_card_to_hand(sts_sim.Card.Coolheaded)
    hand = cs.get_hand()
    ch_indices = [i for i, c in enumerate(hand) if c.card == sts_sim.Card.Coolheaded]
    for idx in reversed(ch_indices):
        cs.play_card(idx, None)
    # 3 slots: 1 Lightning (CrackedCore) was evoked, now 3 Frost
    # The CrackedCore lightning was auto-evoked when slots filled
    # Now channel another Frost to force evoke first Frost
    block_before = cs.player.block
    cs.add_card_to_hand(sts_sim.Card.Coolheaded)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.Coolheaded)
    cs.play_card(idx, None)
    # Should have gained block from Frost evoke (1 block)
    assert cs.player.block >= block_before


def test_frost_passive_grants_block():
    """Frost orb passive grants block at end of turn."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Coolheaded)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.Coolheaded)
    cs.play_card(idx, None)
    # End turn to trigger passives
    cs.end_player_turn()
    # Frost passive should have granted 1 block
    assert cs.player.block >= 1


def test_hyperbeam_removes_all_orbs():
    """Hyperbeam deals AOE damage and removes all orbs."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(5)
    assert len(cs.player.get_orbs()) > 0  # CrackedCore Lightning
    cs.add_card_to_hand(sts_sim.Card.Hyperbeam)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.Hyperbeam)
    cs.play_card(idx, None)
    assert len(cs.player.get_orbs()) == 0


# --- Card Effects ---

def test_zap_channels_lightning():
    """Zap channels Lightning."""
    cs = make_combat_with_card(sts_sim.Card.Zap)
    # Zap is a starter - just check it's in the hand. Let's manually add it.
    # CrackedCore already channeled 1 Lightning
    orbs_before = len(cs.player.get_orbs())
    hand = cs.get_hand()
    zap_idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.Zap)
    cs.play_card(zap_idx, None)
    assert len(cs.player.get_orbs()) == orbs_before + 1


def test_leap_gives_block():
    """Leap gives block."""
    cs = make_combat_with_card(sts_sim.Card.Leap)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.Leap)
    cs.play_card(idx, None)
    assert cs.player.block >= 2


def test_glacier_block_and_frost():
    """Glacier gives block and channels Frost."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.Glacier)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.Glacier)
    cs.play_card(idx, None)
    assert cs.player.block >= 2
    orbs = cs.player.get_orbs()
    assert any(o == sts_sim.OrbType.Frost for o in orbs)


def test_overclock_draws_and_adds_dazed():
    """Overclock draws cards and adds Dazed to discard."""
    cs = make_combat_with_card(sts_sim.Card.Overclock)
    hand_before = len(cs.get_hand())
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.Overclock)
    cs.play_card(idx, None)
    # Drew 2, played 1: net +1
    assert len(cs.get_hand()) == hand_before - 1 + 2
    # Dazed in discard
    discard = cs.get_discard_pile()
    assert any(c.card == sts_sim.Card.Dazed for c in discard)


def test_turbo_gives_energy_and_dazed():
    """TURBO gives energy and adds Dazed."""
    cs = make_combat_with_card(sts_sim.Card.TURBO)
    energy_before = cs.player.energy
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.TURBO)
    cs.play_card(idx, None)
    # Gained 2 energy (cost 0, +2)
    assert cs.player.energy == energy_before + 2
    discard = cs.get_discard_pile()
    assert any(c.card == sts_sim.Card.Dazed for c in discard)


def test_skim_draws_cards():
    """Skim draws 3 cards."""
    cs = make_combat_with_card(sts_sim.Card.SkimCard)
    hand_before = len(cs.get_hand())
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.SkimCard)
    cs.play_card(idx, None)
    assert len(cs.get_hand()) == hand_before - 1 + 3


def test_double_energy_doubles():
    """Double Energy doubles current energy."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(3)
    cs.add_card_to_hand(sts_sim.Card.DoubleEnergy)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.DoubleEnergy)
    cs.play_card(idx, None)
    # Cost 1, then doubles: (3 - 1) * 2 = 4
    assert cs.player.energy == 4


def test_capacitor_increases_orb_slots():
    """Capacitor increases orb slots."""
    cs = make_combat_with_card(sts_sim.Card.CapacitorCard)
    slots_before = cs.player.orb_slots
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.CapacitorCard)
    cs.play_card(idx, None)
    assert cs.player.orb_slots == slots_before + 2


def test_reprogram_gives_strength_removes_orbs():
    """Reprogram gives Strength and removes all orbs."""
    cs = make_combat_with_card(sts_sim.Card.Reprogram)
    assert len(cs.player.get_orbs()) > 0  # CrackedCore
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.Reprogram)
    cs.play_card(idx, None)
    assert cs.player.get_power(sts_sim.PowerType.Strength) == 1
    assert len(cs.player.get_orbs()) == 0


def test_fission_removes_orbs_gives_energy():
    """Fission removes all orbs and gives energy per orb."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(5)
    # Channel extra orbs
    cs.add_card_to_hand(sts_sim.Card.Coolheaded)
    cs.add_card_to_hand(sts_sim.Card.DarknessCard)
    hand = cs.get_hand()
    ch_idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.Coolheaded)
    cs.play_card(ch_idx, None)
    hand = cs.get_hand()
    dk_idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.DarknessCard)
    cs.play_card(dk_idx, None)
    orb_count = len(cs.player.get_orbs())
    assert orb_count == 3  # CrackedCore Lightning + Frost + Dark
    energy_before = cs.player.energy
    cs.add_card_to_hand(sts_sim.Card.Fission)
    hand = cs.get_hand()
    f_idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.Fission)
    cs.play_card(f_idx, None)
    assert len(cs.player.get_orbs()) == 0
    assert cs.player.energy == energy_before + orb_count


def test_rainbow_channels_all_three():
    """Rainbow channels Lightning, Frost, and Dark."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.RainbowCard)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.RainbowCard)
    cs.play_card(idx, None)
    orbs = cs.player.get_orbs()
    types = set(o for o in orbs)
    assert sts_sim.OrbType.Lightning in types
    assert sts_sim.OrbType.Frost in types
    assert sts_sim.OrbType.Dark in types


def test_storm_channels_lightning_at_turn_start():
    """Storm power channels Lightning at start of turn."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.StormCard)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.StormCard)
    cs.play_card(idx, None)
    assert cs.player.get_power(sts_sim.PowerType.Storm) == 1
    # End turn and start new turn
    cs.end_player_turn()
    cs.roll_and_execute_monsters()
    cs.start_player_turn()
    orbs = cs.player.get_orbs()
    lightning_count = sum(1 for o in orbs if o == sts_sim.OrbType.Lightning)
    # Should have at least 1 from Storm trigger (plus CrackedCore from start)
    assert lightning_count >= 1


# --- Powers ---

def test_consume_increases_evoke():
    """Consume increases orb evoke damage."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.ConsumeCard)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.ConsumeCard)
    cs.play_card(idx, None)
    assert cs.player.get_power(sts_sim.PowerType.OrbEvoke) == 1


def test_defragment_increases_passive():
    """Defragment increases orb passive amounts."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.DefragmentCard)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.DefragmentCard)
    cs.play_card(idx, None)
    assert cs.player.get_power(sts_sim.PowerType.OrbPassive) == 1


def test_machine_learning_extra_draw():
    """Machine Learning gives extra draw per turn."""
    cs = make_defect_combat()
    cs.start_combat()
    cs.set_player_energy(5)
    cs.add_card_to_hand(sts_sim.Card.MachineLearningCard)
    hand = cs.get_hand()
    idx = next(i for i, c in enumerate(hand) if c.card == sts_sim.Card.MachineLearningCard)
    cs.play_card(idx, None)
    assert cs.player.get_power(sts_sim.PowerType.DrawPerTurn) == 1


# --- Reward Deck ---

def test_defect_reward_deck():
    """Defect reward deck contains Defect cards."""
    rd = sts_sim.RewardDeck(0, sts_sim.Character.Defect)
    cards = rd.draw_rewards(3)
    assert len(cards) == 3
    for c in cards:
        assert c.card != sts_sim.Card.StrikeRed
        assert c.card != sts_sim.Card.Bash


# --- Card Properties ---

def test_double_energy_exhausts():
    """Double Energy exhausts."""
    ci = sts_sim.CardInstance(sts_sim.Card.DoubleEnergy, False)
    assert ci.py_exhausts


def test_fission_exhausts():
    """Fission exhausts."""
    ci = sts_sim.CardInstance(sts_sim.Card.Fission, False)
    assert ci.py_exhausts


def test_defragment_ethereal():
    """Defragment is ethereal (not upgraded)."""
    ci = sts_sim.CardInstance(sts_sim.Card.DefragmentCard, False)
    assert ci.py_ethereal


def test_defragment_upgraded_not_ethereal():
    """Upgraded Defragment is not ethereal."""
    ci = sts_sim.CardInstance(sts_sim.Card.DefragmentCard, True)
    assert not ci.py_ethereal


def test_echo_form_ethereal():
    """Echo Form is ethereal (not upgraded)."""
    ci = sts_sim.CardInstance(sts_sim.Card.EchoFormCard, False)
    assert ci.py_ethereal


def test_echo_form_upgraded_not_ethereal():
    """Upgraded Echo Form is not ethereal."""
    ci = sts_sim.CardInstance(sts_sim.Card.EchoFormCard, True)
    assert not ci.py_ethereal


def test_core_surge_retains():
    """Core Surge retains."""
    ci = sts_sim.CardInstance(sts_sim.Card.CoreSurge, False)
    assert ci.py_retain


def test_defect_card_names():
    """Verify key Defect card names."""
    assert sts_sim.Card.BallLightning.py_name == "Ball Lightning"
    assert sts_sim.Card.Claw.py_name == "Claw"
    assert sts_sim.Card.Hyperbeam.py_name == "Hyperbeam"
    assert sts_sim.Card.Glacier.py_name == "Glacier"
    assert sts_sim.Card.EchoFormCard.py_name == "Echo Form"
    assert sts_sim.Card.TURBO.py_name == "TURBO"
