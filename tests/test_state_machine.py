"""Tests for the GameState state machine."""
import sts_sim


def play_combat_greedy(g):
    """Play all affordable cards each turn until combat ends."""
    while g.get_phase() == "combat":
        played = True
        while played and g.get_phase() == "combat":
            played = False
            hand = g.get_hand()
            energy = g.get_energy()
            for i, c in enumerate(hand):
                if c.py_cost <= energy:
                    target = 0 if c.py_card_type == sts_sim.CardType.Attack else None
                    if g.play_card(i, target):
                        played = True
                        break
        if g.get_phase() == "combat":
            g.end_turn()


def enter_room(g):
    """Choose the next room from the map (linear map: always index 0)."""
    assert g.get_phase() == "map"
    rooms = g.get_available_rooms()
    assert len(rooms) >= 1
    g.choose_next_room(0)


# ---- Construction ----

def test_new_game_state():
    g = sts_sim.GameState(seed=42)
    assert g.get_phase() == "not_started"
    assert g.get_player_hp() == 10
    assert g.get_player_max_hp() == 10
    assert g.get_deck_size() == 10
    assert g.get_current_room() == 0


# ---- Start run ----

def test_start_run_enters_map():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    assert g.get_phase() == "map"
    assert g.get_current_room() == 0
    rooms = g.get_available_rooms()
    assert len(rooms) == 1
    assert rooms[0].room_type == sts_sim.RoomType.Monster


def test_choose_room_enters_combat():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    assert g.get_phase() == "combat"
    assert len(g.get_hand()) == 5
    assert g.get_energy() == 3
    monsters = g.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].name == "Dummy"
    assert monsters[0].hp == 8


# ---- Combat ----

def test_play_card_in_combat():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    hand = g.get_hand()
    for i, c in enumerate(hand):
        if c.py_card_type == sts_sim.CardType.Attack:
            result = g.play_card(i, 0)
            assert result is True
            break


def test_combat_victory_goes_to_card_reward():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    assert g.get_phase() == "card_reward"
    options = g.get_reward_options()
    assert len(options) == 3
    card_names = [str(c.card) for c in options]
    assert "Card.SpotWeakness" in card_names
    assert "Card.BurningPact" in card_names
    assert "Card.WildStrike" in card_names


def test_play_card_outside_combat_fails():
    g = sts_sim.GameState(seed=42)
    result = g.play_card(0, 0)
    assert result is False


# ---- Card reward ----

def test_pick_card_adds_to_deck():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    assert g.get_phase() == "card_reward"
    initial_deck_size = g.get_deck_size()
    g.pick_card(0)
    assert g.get_deck_size() == initial_deck_size + 1


def test_skip_card_does_not_add():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    assert g.get_phase() == "card_reward"
    initial_deck_size = g.get_deck_size()
    g.skip_card()
    assert g.get_deck_size() == initial_deck_size


def test_card_reward_advances_to_map():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.pick_card(0)
    assert g.get_phase() == "map"
    assert g.get_current_room() == 1


# ---- Map navigation ----

def test_map_shows_next_room():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    assert g.get_phase() == "map"
    rooms = g.get_available_rooms()
    assert len(rooms) == 1
    assert rooms[0].room_type == sts_sim.RoomType.Event


def test_available_rooms_empty_outside_map():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    assert g.get_phase() == "combat"
    rooms = g.get_available_rooms()
    assert len(rooms) == 0


def test_choose_next_room_outside_map_is_noop():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    assert g.get_phase() == "combat"
    g.choose_next_room(0)  # should be no-op
    assert g.get_phase() == "combat"


# ---- Event ----

def test_event_choices():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    enter_room(g)
    assert g.get_phase() == "event"
    choices = g.get_event_choices()
    assert len(choices) >= 2
    assert choices[0].label == "Banana"


def test_event_heal():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    enter_room(g)
    g.event_choose(0)  # Banana: heal 2
    assert g.get_player_hp() == 10  # already at max
    assert g.get_phase() == "map"


def test_event_advances_to_map():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    enter_room(g)
    g.event_choose(0)
    assert g.get_phase() == "map"
    assert g.get_current_room() == 2


# ---- Shop ----

def test_shop_items():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    enter_room(g)
    g.event_choose(0)
    enter_room(g)
    assert g.get_phase() == "shop"
    items = g.get_shop_items()
    assert len(items) > 0


def test_shop_leave_advances_to_map():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    enter_room(g)
    g.event_choose(0)
    enter_room(g)
    g.shop_leave()
    assert g.get_phase() == "map"
    assert g.get_current_room() == 3


# ---- Rest site ----

def test_rest_choices():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    enter_room(g)
    g.event_choose(0)
    enter_room(g)
    g.shop_leave()
    enter_room(g)
    assert g.get_phase() == "rest"
    choices = g.get_rest_choices()
    assert len(choices) == 2
    assert choices[0].label == "Rest"
    assert choices[1].label == "Smith"


def test_rest_heal():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    enter_room(g)
    g.event_choose(0)
    enter_room(g)
    g.shop_leave()
    enter_room(g)
    g.rest_choose(0)  # Rest: heal 3
    assert g.get_player_hp() <= g.get_player_max_hp()
    assert g.get_phase() == "map"


def test_smith_upgrade():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    enter_room(g)
    g.event_choose(0)
    enter_room(g)
    g.shop_leave()
    enter_room(g)
    g.rest_choose(1)  # Smith
    assert g.get_phase() == "rest_upgrade_card"
    g.rest_upgrade_card(0)
    deck = g.get_deck()
    assert deck[0].upgraded is True
    assert g.get_phase() == "map"


# ---- Boss ----

def test_boss_has_more_hp():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    enter_room(g)
    g.event_choose(0)
    enter_room(g)
    g.shop_leave()
    enter_room(g)
    g.rest_choose(0)
    enter_room(g)
    assert g.get_phase() == "combat"
    assert g.get_current_room() == 4
    monsters = g.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].name == "Dummy Boss"
    assert monsters[0].hp == 16


def test_boss_victory_wins_game():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    enter_room(g)
    g.event_choose(0)
    enter_room(g)
    g.shop_leave()
    enter_room(g)
    g.rest_choose(0)
    enter_room(g)
    play_combat_greedy(g)
    assert g.get_phase() == "victory"
    assert g.is_game_over() is True
    assert g.did_player_win() is True


# ---- Full run ----

def test_full_run_with_card_pick():
    """Play through all 5 rooms, picking a card reward."""
    g = sts_sim.GameState(seed=42)
    g.start_run()

    # Room 0: Fight
    enter_room(g)
    assert g.get_phase() == "combat"
    play_combat_greedy(g)
    assert g.get_phase() == "card_reward"
    g.pick_card(0)  # Pick Spot Weakness
    assert g.get_deck_size() == 11

    # Room 1: Event
    enter_room(g)
    assert g.get_phase() == "event"
    g.event_choose(0)  # Banana

    # Room 2: Shop
    enter_room(g)
    assert g.get_phase() == "shop"
    g.shop_leave()

    # Room 3: Rest
    enter_room(g)
    assert g.get_phase() == "rest"
    g.rest_choose(0)  # Rest

    # Room 4: Boss
    enter_room(g)
    assert g.get_phase() == "combat"
    play_combat_greedy(g)
    assert g.get_phase() == "victory"
    assert g.did_player_win() is True


def test_full_run_skip_card():
    """Full run but skip the card reward."""
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    assert g.get_deck_size() == 10
    enter_room(g)
    g.event_choose(0)
    enter_room(g)
    g.shop_leave()
    enter_room(g)
    g.rest_choose(0)
    enter_room(g)
    play_combat_greedy(g)
    assert g.did_player_win() is True


# ---- Edge cases ----

def test_end_turn_outside_combat():
    """end_turn should be a no-op outside combat."""
    g = sts_sim.GameState(seed=42)
    g.end_turn()
    assert g.get_phase() == "not_started"


def test_event_choose_outside_event():
    """event_choose should be a no-op outside event phase."""
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    g.event_choose(0)  # In combat, should be no-op
    assert g.get_phase() == "combat"


def test_shop_leave_outside_shop():
    """shop_leave should be a no-op outside shop phase."""
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    g.shop_leave()  # In combat, should be no-op
    assert g.get_phase() == "combat"


def test_deterministic_with_seed():
    """Same seed should produce the same game."""
    def run_game(seed):
        g = sts_sim.GameState(seed=seed)
        g.start_run()
        enter_room(g)
        play_combat_greedy(g)
        hp = g.get_player_hp()
        g.skip_card()
        enter_room(g)
        g.event_choose(0)
        enter_room(g)
        g.shop_leave()
        enter_room(g)
        g.rest_choose(0)
        enter_room(g)
        play_combat_greedy(g)
        return hp, g.get_player_hp(), g.did_player_win()

    r1 = run_game(123)
    r2 = run_game(123)
    assert r1 == r2


# ---- Action API ----

def test_actions_not_started():
    """No actions available before starting."""
    g = sts_sim.GameState(seed=42)
    assert g.get_available_actions() == []


def test_actions_map_phase():
    """Map phase has ChooseRoom actions."""
    g = sts_sim.GameState(seed=42)
    g.start_run()
    actions = g.get_available_actions()
    assert len(actions) == 1
    assert isinstance(actions[0], sts_sim.Action.ChooseRoom)
    assert actions[0].index == 0


def test_actions_combat_phase():
    """Combat phase lists playable cards + EndTurn."""
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    actions = g.get_available_actions()
    play_card_actions = [a for a in actions if isinstance(a, sts_sim.Action.PlayCard)]
    end_turn_actions = [a for a in actions if isinstance(a, sts_sim.Action.EndTurn)]
    assert len(end_turn_actions) == 1
    assert len(play_card_actions) > 0
    # All PlayCard actions targeting the single monster should have target=0
    for a in play_card_actions:
        assert a.target == 0


def test_actions_card_reward():
    """Card reward has PickCard + SkipCard actions."""
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    assert g.get_phase() == "card_reward"
    actions = g.get_available_actions()
    pick_actions = [a for a in actions if isinstance(a, sts_sim.Action.PickCard)]
    skip_actions = [a for a in actions if isinstance(a, sts_sim.Action.SkipCard)]
    assert len(pick_actions) == 3
    assert len(skip_actions) == 1


def test_actions_event():
    """Event phase has EventChoose actions."""
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    enter_room(g)
    assert g.get_phase() == "event"
    actions = g.get_available_actions()
    assert all(isinstance(a, sts_sim.Action.EventChoose) for a in actions)
    assert len(actions) >= 2


def test_actions_rest():
    """Rest phase has RestChoose actions."""
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    enter_room(g)
    g.event_choose(0)
    enter_room(g)
    g.shop_leave()
    enter_room(g)
    assert g.get_phase() == "rest"
    actions = g.get_available_actions()
    assert len(actions) == 2
    assert all(isinstance(a, sts_sim.Action.RestChoose) for a in actions)


def test_actions_game_over():
    """No actions after game over."""
    g = sts_sim.GameState(seed=42)
    g.start_run()
    enter_room(g)
    play_combat_greedy(g)
    g.skip_card()
    enter_room(g)
    g.event_choose(0)
    enter_room(g)
    g.shop_leave()
    enter_room(g)
    g.rest_choose(0)
    enter_room(g)
    play_combat_greedy(g)
    assert g.get_phase() == "victory"
    assert g.get_available_actions() == []


def test_take_action_full_run():
    """Play a full run using only take_action."""
    g = sts_sim.GameState(seed=42)
    g.start_run()

    # Room 0: Map -> Combat -> Card reward
    actions = g.get_available_actions()
    assert g.take_action(actions[0]) is True  # ChooseRoom
    assert g.get_phase() == "combat"

    # Play combat via actions
    while g.get_phase() == "combat":
        actions = g.get_available_actions()
        played = False
        for a in actions:
            if isinstance(a, sts_sim.Action.PlayCard):
                g.take_action(a)
                played = True
                break
        if not played:
            # EndTurn
            end = [a for a in actions if isinstance(a, sts_sim.Action.EndTurn)][0]
            g.take_action(end)

    assert g.get_phase() == "card_reward"
    actions = g.get_available_actions()
    skip = [a for a in actions if isinstance(a, sts_sim.Action.SkipCard)][0]
    g.take_action(skip)

    # Room 1: Map -> Event
    actions = g.get_available_actions()
    g.take_action(actions[0])  # ChooseRoom
    assert g.get_phase() == "event"
    actions = g.get_available_actions()
    g.take_action(actions[0])  # EventChoose

    # Room 2: Map -> Shop
    actions = g.get_available_actions()
    g.take_action(actions[0])  # ChooseRoom
    assert g.get_phase() == "shop"
    actions = g.get_available_actions()
    leave = [a for a in actions if isinstance(a, sts_sim.Action.ShopLeave)][0]
    g.take_action(leave)

    # Room 3: Map -> Rest
    actions = g.get_available_actions()
    g.take_action(actions[0])  # ChooseRoom
    assert g.get_phase() == "rest"
    actions = g.get_available_actions()
    g.take_action(actions[0])  # Rest (heal)

    # Room 4: Map -> Boss combat
    actions = g.get_available_actions()
    g.take_action(actions[0])  # ChooseRoom
    assert g.get_phase() == "combat"

    while g.get_phase() == "combat":
        actions = g.get_available_actions()
        played = False
        for a in actions:
            if isinstance(a, sts_sim.Action.PlayCard):
                g.take_action(a)
                played = True
                break
        if not played:
            end = [a for a in actions if isinstance(a, sts_sim.Action.EndTurn)][0]
            g.take_action(end)

    assert g.get_phase() == "victory"
    assert g.did_player_win() is True
