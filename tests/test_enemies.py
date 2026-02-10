import sts_sim


def test_jaw_worm_stats():
    """Jaw Worm should have 8 HP."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    monsters = cs.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].name == "Jaw Worm"
    assert monsters[0].hp == 8
    assert monsters[0].max_hp == 8
    assert monsters[0].die_controlled is True
    assert monsters[0].behavior == "sda"


def test_cultist_stats():
    """Cultist should have 9 HP and Ritual after pre-battle."""
    cs = sts_sim.create_encounter("cultist", seed=42)
    cs.start_combat()
    monsters = cs.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].name == "Cultist"
    assert monsters[0].hp == 9
    assert monsters[0].get_power(sts_sim.PowerType.Ritual) == 1


def test_cultist_first_move_incantation():
    """Cultist should use Incantation on first turn, dealing 1 damage and gaining +1 Str."""
    cs = sts_sim.create_encounter("cultist", seed=42)
    cs.start_combat()

    # End player turn, let cultist act
    cs.end_player_turn()
    cs.roll_and_execute_monsters()

    monsters = cs.get_monsters()
    # Cultist: Incantation deals 1 dmg, manually adds +1 Str
    # Ritual does NOT fire on turn 1
    # So after turn 1: Str should be 1 (from Incantation manual add)
    assert monsters[0].get_power(sts_sim.PowerType.Strength) == 1
    # Player should have taken 1 damage (10 - 1 = 9)
    assert cs.player.hp == 9


def test_cultist_second_turn_ritual_fires():
    """On turn 2, Ritual should fire giving +1 Str, then Dark Strike deals 1+Str damage."""
    cs = sts_sim.create_encounter("cultist", seed=42)
    cs.start_combat()

    # Turn 1: end player turn, cultist does Incantation
    cs.end_player_turn()
    cs.roll_and_execute_monsters()

    # After turn 1: Str = 1
    monsters = cs.get_monsters()
    assert monsters[0].get_power(sts_sim.PowerType.Strength) == 1

    # Turn 2: end player turn, Ritual fires (+1 Str → Str=2), then Dark Strike (1+2=3 dmg)
    cs.end_player_turn()
    cs.roll_and_execute_monsters()

    monsters = cs.get_monsters()
    assert monsters[0].get_power(sts_sim.PowerType.Strength) == 2
    # Player took: 1 (turn1) + 3 (turn2, 1 base + 2 str) = 4 total
    assert cs.player.hp == 6


def test_red_louse_stats():
    """Red Louse should have 3 HP and 2 Curl Up."""
    cs = sts_sim.create_encounter("louse", seed=42)
    cs.start_combat()
    monsters = cs.get_monsters()
    red = monsters[0]
    assert red.name == "Red Louse"
    assert red.hp == 3
    assert red.get_power(sts_sim.PowerType.CurlUp) == 2


def test_green_louse_stats():
    """Green Louse should have 3 HP and 2 Curl Up."""
    cs = sts_sim.create_encounter("louse", seed=42)
    cs.start_combat()
    monsters = cs.get_monsters()
    green = monsters[1]
    assert green.name == "Green Louse"
    assert green.hp == 3
    assert green.get_power(sts_sim.PowerType.CurlUp) == 2


def test_louse_curl_up_triggers():
    """Curl Up should grant 2 block on non-lethal hit, then remove itself."""
    cs = sts_sim.create_encounter("louse", seed=42)
    cs.start_combat()

    # Strike a louse (1 damage, non-lethal to 3 HP louse)
    hand = cs.get_hand()
    for i, ci in enumerate(hand):
        if ci.card == sts_sim.Card.StrikeRed:
            cs.play_card(i, 0)  # Target Red Louse
            break

    monsters = cs.get_monsters()
    red = monsters[0]
    # Curl Up should have triggered: gained 2 block, then Curl Up removed
    # Strike does 1 damage, Curl Up triggers (1 > 0, 1 < 3), grants 2 block
    # Then damage is applied against 2 block: 1 damage, 2 block → 1 blocked, 0 HP lost
    assert red.get_power(sts_sim.PowerType.CurlUp) == 0
    assert red.hp == 3  # No HP lost because block absorbed it
    assert red.block == 1  # 2 block - 1 damage = 1 remaining


def test_louse_encounter_composition():
    """Louse encounter should have 1 Red + 1 Green."""
    cs = sts_sim.create_encounter("louse", seed=42)
    monsters = cs.get_monsters()
    assert len(monsters) == 2
    assert monsters[0].monster_id == "red_louse"
    assert monsters[1].monster_id == "green_louse"


def test_jaw_worm_behavior_mapping():
    """Jaw Worm behavior 'sda': rolls 1-2→s(Bellow), 3-4→d(Thrash), 5-6→a(Chomp)."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    # We can't directly test move selection without running monster turns
    # So just verify the behavior string is correct
    monsters = cs.get_monsters()
    assert monsters[0].behavior == "sda"
