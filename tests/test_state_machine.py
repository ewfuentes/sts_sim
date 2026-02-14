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


# ---- Construction ----

def test_new_game_state():
    g = sts_sim.GameState(seed=42)
    assert g.get_phase() == "not_started"
    assert g.get_player_hp() == 10
    assert g.get_player_max_hp() == 10
    assert g.get_deck_size() == 10
    assert g.get_current_room() == 0


# ---- Start run ----

def test_start_run_enters_combat():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    assert g.get_phase() == "combat"
    assert g.get_current_room() == 0
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
    hand = g.get_hand()
    # Find a Strike (attack card)
    for i, c in enumerate(hand):
        if c.py_card_type == sts_sim.CardType.Attack:
            result = g.play_card(i, 0)
            assert result is True
            break


def test_combat_victory_goes_to_card_reward():
    g = sts_sim.GameState(seed=42)
    g.start_run()
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
    # Not started yet
    result = g.play_card(0, 0)
    assert result is False


# ---- Card reward ----

def test_pick_card_adds_to_deck():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    assert g.get_phase() == "card_reward"
    initial_deck_size = g.get_deck_size()
    g.pick_card(0)  # Pick first reward
    assert g.get_deck_size() == initial_deck_size + 1


def test_skip_card_does_not_add():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    assert g.get_phase() == "card_reward"
    initial_deck_size = g.get_deck_size()
    g.skip_card()
    assert g.get_deck_size() == initial_deck_size


def test_card_reward_advances_to_event():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    g.pick_card(0)
    assert g.get_phase() == "event"
    assert g.get_current_room() == 1


# ---- Event ----

def test_event_choices():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    g.skip_card()
    assert g.get_phase() == "event"
    choices = g.get_event_choices()
    assert len(choices) >= 2
    assert choices[0].label == "Banana"


def test_event_heal():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    g.skip_card()
    # BigFish: option 0 = Banana (heal 2)
    g.event_choose(0)
    # HP should still be 10 (was already at max)
    assert g.get_player_hp() == 10
    assert g.get_phase() == "shop"


def test_event_advances_to_shop():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    g.skip_card()
    g.event_choose(0)
    assert g.get_phase() == "shop"
    assert g.get_current_room() == 2


# ---- Shop ----

def test_shop_items():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    g.skip_card()
    g.event_choose(0)
    assert g.get_phase() == "shop"
    items = g.get_shop_items()
    assert len(items) > 0


def test_shop_leave_advances_to_rest():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    g.skip_card()
    g.event_choose(0)
    g.shop_leave()
    assert g.get_phase() == "rest"
    assert g.get_current_room() == 3


# ---- Rest site ----

def test_rest_choices():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    g.skip_card()
    g.event_choose(0)
    g.shop_leave()
    assert g.get_phase() == "rest"
    choices = g.get_rest_choices()
    assert len(choices) == 2
    assert choices[0].label == "Rest"
    assert choices[1].label == "Smith"


def test_rest_heal():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    g.skip_card()
    g.event_choose(0)
    g.shop_leave()
    # HP is already at max, so heal won't increase it
    hp_before = g.get_player_hp()
    g.rest_choose(0)  # Rest: heal 3
    assert g.get_player_hp() <= g.get_player_max_hp()
    # Should advance to combat (boss)
    assert g.get_phase() == "combat"


def test_smith_upgrade():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    g.skip_card()
    g.event_choose(0)
    g.shop_leave()
    g.rest_choose(1)  # Smith
    assert g.get_phase() == "rest_upgrade_card"
    # Upgrade first card in deck (Strike)
    g.rest_upgrade_card(0)
    deck = g.get_deck()
    assert deck[0].upgraded is True
    # Should advance to boss combat
    assert g.get_phase() == "combat"


# ---- Boss ----

def test_boss_has_more_hp():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    g.skip_card()
    g.event_choose(0)
    g.shop_leave()
    g.rest_choose(0)
    assert g.get_phase() == "combat"
    assert g.get_current_room() == 4
    monsters = g.get_monsters()
    assert len(monsters) == 1
    assert monsters[0].name == "Dummy Boss"
    assert monsters[0].hp == 16


def test_boss_victory_wins_game():
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    g.skip_card()
    g.event_choose(0)
    g.shop_leave()
    g.rest_choose(0)
    # Boss fight
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
    assert g.get_phase() == "combat"
    play_combat_greedy(g)
    assert g.get_phase() == "card_reward"
    g.pick_card(0)  # Pick Spot Weakness
    assert g.get_deck_size() == 11

    # Room 1: Event
    assert g.get_phase() == "event"
    g.event_choose(0)  # Banana

    # Room 2: Shop
    assert g.get_phase() == "shop"
    g.shop_leave()

    # Room 3: Rest
    assert g.get_phase() == "rest"
    g.rest_choose(0)  # Rest

    # Room 4: Boss
    assert g.get_phase() == "combat"
    play_combat_greedy(g)
    assert g.get_phase() == "victory"
    assert g.did_player_win() is True


def test_full_run_skip_card():
    """Full run but skip the card reward."""
    g = sts_sim.GameState(seed=42)
    g.start_run()
    play_combat_greedy(g)
    g.skip_card()
    assert g.get_deck_size() == 10
    g.event_choose(0)
    g.shop_leave()
    g.rest_choose(0)
    play_combat_greedy(g)
    assert g.did_player_win() is True


# ---- Edge cases ----

def test_end_turn_outside_combat():
    """end_turn should be a no-op outside combat."""
    g = sts_sim.GameState(seed=42)
    g.end_turn()  # Should not crash
    assert g.get_phase() == "not_started"


def test_event_choose_outside_event():
    """event_choose should be a no-op outside event phase."""
    g = sts_sim.GameState(seed=42)
    g.start_run()
    g.event_choose(0)  # In combat, should be no-op
    assert g.get_phase() == "combat"


def test_shop_leave_outside_shop():
    """shop_leave should be a no-op outside shop phase."""
    g = sts_sim.GameState(seed=42)
    g.start_run()
    g.shop_leave()  # In combat, should be no-op
    assert g.get_phase() == "combat"


def test_deterministic_with_seed():
    """Same seed should produce the same game."""
    def run_game(seed):
        g = sts_sim.GameState(seed=seed)
        g.start_run()
        play_combat_greedy(g)
        hp = g.get_player_hp()
        g.skip_card()
        g.event_choose(0)
        g.shop_leave()
        g.rest_choose(0)
        play_combat_greedy(g)
        return hp, g.get_player_hp(), g.did_player_win()

    r1 = run_game(123)
    r2 = run_game(123)
    assert r1 == r2
