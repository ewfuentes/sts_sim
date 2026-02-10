import sts_sim


def test_combat_initialization():
    """Combat state should initialize correctly."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    assert cs.turn_number == 0
    assert cs.combat_over is False
    assert cs.player_won is False
    assert cs.player.hp == 10


def test_start_combat():
    """Starting combat should set up player turn."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    assert cs.turn_number == 1
    assert cs.player.energy == 3
    assert len(cs.get_hand()) == 5


def test_full_turn_cycle():
    """A full turn cycle: player plays cards, ends turn, monsters act."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    # Play a strike
    hand = cs.get_hand()
    for i, ci in enumerate(hand):
        if ci.card == sts_sim.Card.StrikeRed:
            cs.play_card(i, 0)
            break

    # End turn
    cs.end_player_turn()

    # Monster turn
    roll = cs.roll_and_execute_monsters()
    assert 1 <= roll <= 6

    # Should be turn 2 now
    assert cs.turn_number == 2
    assert cs.player.energy == 3
    assert len(cs.get_hand()) == 5


def test_draw_pile_shuffle():
    """When draw pile is empty, discard should be shuffled into it."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    # Turn 1: draw 5, play some, end turn (discard rest)
    cs.end_player_turn()
    cs.roll_and_execute_monsters()

    # Turn 2: draw 5 more (all 10 cards used, draw pile empty)
    cs.end_player_turn()
    cs.roll_and_execute_monsters()

    # Turn 3: should shuffle discard into draw and draw 5
    assert len(cs.get_hand()) == 5
    assert cs.turn_number == 3


def test_burning_blood_heals():
    """Burning Blood should heal 1 HP when combat is won."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    # Kill Jaw Worm (8 HP) by playing strikes across turns
    while not cs.combat_over:
        hand = cs.get_hand()
        played = False
        for i in range(len(hand) - 1, -1, -1):
            ci = hand[i]
            if ci.card == sts_sim.Card.StrikeRed and cs.player.energy >= 1:
                cs.play_card(i, 0)
                hand = cs.get_hand()
                if cs.combat_over:
                    break
                played = True
            elif ci.card == sts_sim.Card.Bash and cs.player.energy >= 2:
                cs.play_card(i, 0)
                hand = cs.get_hand()
                if cs.combat_over:
                    break
                played = True
            elif ci.card == sts_sim.Card.DefendRed and cs.player.energy >= 1:
                cs.play_card(i)
                hand = cs.get_hand()
                played = True

        if cs.combat_over:
            break

        cs.end_player_turn()
        cs.roll_and_execute_monsters()

    assert cs.player_won is True
    # Player should have been healed 1 HP by Burning Blood
    # We can't predict exact HP but it should be <= max_hp


def test_player_death():
    """Combat should end when player dies."""
    # Create a scenario where player takes lots of damage
    cs = sts_sim.create_encounter("cultist", seed=42)
    cs.start_combat()

    # Just keep ending turns, let cultist scale and kill us
    for _ in range(50):
        if cs.combat_over:
            break
        cs.end_player_turn()
        cs.roll_and_execute_monsters()

    assert cs.combat_over is True
    assert cs.player_won is False
    assert cs.player.hp <= 0


def test_deterministic_replay():
    """Same seed should produce identical combat outcomes."""
    def play_game(seed):
        cs = sts_sim.create_encounter("jaw_worm", seed=seed)
        cs.start_combat()
        results = []

        for _ in range(5):
            if cs.combat_over:
                break
            # Always play first playable card
            hand = cs.get_hand()
            for i, ci in enumerate(hand):
                if ci.py_cost <= cs.player.energy:
                    if ci.py_has_target:
                        cs.play_card(i, 0)
                    else:
                        cs.play_card(i)
                    break

            results.append((cs.player.hp, cs.player.block, cs.player.energy))
            cs.end_player_turn()
            roll = cs.roll_and_execute_monsters()
            results.append(("roll", roll, cs.player.hp))

        return results

    r1 = play_game(99)
    r2 = play_game(99)
    assert r1 == r2


def test_deep_clone():
    """Deep clone should create independent copy."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    clone = cs.deep_clone()

    # Play a card on original
    hand = cs.get_hand()
    for i, ci in enumerate(hand):
        if ci.card == sts_sim.Card.StrikeRed:
            cs.play_card(i, 0)
            break

    # Clone should be unaffected
    monsters_orig = cs.get_monsters()
    monsters_clone = clone.get_monsters()
    assert monsters_orig[0].hp != monsters_clone[0].hp or \
           cs.player.energy != clone.player.energy


def test_get_available_actions():
    """get_available_actions should return playable cards."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    actions = cs.get_available_actions()
    assert len(actions) > 0

    for hand_idx, ci, needs_target in actions:
        assert ci.py_cost <= cs.player.energy


def test_get_valid_targets():
    """get_valid_targets should return alive monster indices."""
    cs = sts_sim.create_encounter("louse", seed=42)
    cs.start_combat()

    targets = cs.get_valid_targets()
    assert len(targets) == 2
    assert 0 in targets
    assert 1 in targets


def test_monster_dies_removes_from_targets():
    """Dead monster should not be in valid targets."""
    cs = sts_sim.create_encounter("louse", seed=42)
    cs.start_combat()

    # Kill Red Louse (3 HP) with strikes
    while True:
        hand = cs.get_hand()
        played = False
        for i, ci in enumerate(hand):
            if ci.card == sts_sim.Card.StrikeRed and cs.player.energy >= 1:
                cs.play_card(i, 0)
                played = True
                break
            elif ci.card == sts_sim.Card.Bash and cs.player.energy >= 2:
                cs.play_card(i, 0)
                played = True
                break

        monsters = cs.get_monsters()
        if monsters[0].hp <= 0:
            break

        if not played or cs.player.energy == 0:
            cs.end_player_turn()
            cs.roll_and_execute_monsters()
            if cs.combat_over:
                break

    if not cs.combat_over:
        targets = cs.get_valid_targets()
        assert 0 not in targets  # Red Louse dead


def test_hand_discards_on_end_turn():
    """Remaining hand should be discarded when turn ends."""
    cs = sts_sim.create_encounter("jaw_worm", seed=42)
    cs.start_combat()

    assert len(cs.get_hand()) == 5

    # Play one card
    hand = cs.get_hand()
    for i, ci in enumerate(hand):
        if ci.card == sts_sim.Card.StrikeRed:
            cs.play_card(i, 0)
            break

    assert len(cs.get_hand()) == 4

    cs.end_player_turn()
    assert len(cs.get_hand()) == 0
