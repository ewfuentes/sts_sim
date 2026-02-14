use pyo3::prelude::*;

use crate::cards::{Card, CardInstance};
use crate::combat::CombatState;
use crate::creature::Monster;
use crate::enemies;
use crate::enums::{EventType, Relic, RoomType};
use crate::events::EventState;
use crate::rest::RestSite;
use crate::shop::ShopState;

/// The linear map of rooms for a mini-run.
fn default_rooms() -> Vec<RoomType> {
    vec![
        RoomType::Monster, // Room 0: fight
        RoomType::Event,   // Room 1: event
        RoomType::Shop,    // Room 2: shop
        RoomType::Rest,    // Room 3: campfire
        RoomType::Boss,    // Room 4: boss
    ]
}

/// The fixed reward card pool.
fn reward_cards() -> Vec<CardInstance> {
    vec![
        CardInstance::new(Card::SpotWeakness, false),
        CardInstance::new(Card::BurningPact, false),
        CardInstance::new(Card::WildStrike, false),
    ]
}

/// Ironclad starter deck.
fn starter_deck() -> Vec<CardInstance> {
    let mut deck = Vec::with_capacity(10);
    for _ in 0..5 {
        deck.push(CardInstance::new(Card::StrikeRed, false));
    }
    for _ in 0..4 {
        deck.push(CardInstance::new(Card::DefendRed, false));
    }
    deck.push(CardInstance::new(Card::Bash, false));
    deck
}

// ---- Sub-phase enums ----

#[derive(Clone, Debug)]
pub enum ShopPhase {
    Browsing,
    ChoosingCardToRemove,
}

#[derive(Clone, Debug)]
pub enum RestPhase {
    ChoosingAction,
    ChoosingCardToUpgrade,
}

// ---- Game phase ----

pub enum GamePhase {
    NotStarted,
    Combat(CombatState),
    Event(EventState),
    Shop {
        shop: ShopState,
        phase: ShopPhase,
    },
    RestSite {
        rest: RestSite,
        phase: RestPhase,
    },
    CardReward {
        options: Vec<CardInstance>,
    },
    GameOver {
        won: bool,
    },
}

// ---- GameState ----

#[pyclass]
pub struct GameState {
    // Persistent player state
    player_hp: i32,
    player_max_hp: i32,
    deck: Vec<CardInstance>,
    relics: Vec<Relic>,
    gold: i32,

    // Run structure
    rooms: Vec<RoomType>,
    current_room: usize,
    phase: GamePhase,

    // Reward cards
    reward_cards: Vec<CardInstance>,

    // RNG
    seed: u64,
}

#[pymethods]
impl GameState {
    #[new]
    #[pyo3(signature = (seed=None))]
    pub fn new(seed: Option<u64>) -> Self {
        let s = seed.unwrap_or(0);
        GameState {
            player_hp: 10,
            player_max_hp: 10,
            deck: starter_deck(),
            relics: vec![Relic::BurningBlood],
            gold: 0,
            rooms: default_rooms(),
            current_room: 0,
            phase: GamePhase::NotStarted,
            reward_cards: reward_cards(),
            seed: s,
        }
    }

    /// Start the run. Enters the first room (combat with dummy enemy).
    pub fn start_run(&mut self) {
        self.current_room = 0;
        self.enter_current_room();
    }

    // ---- Combat delegation ----

    /// Play a card during combat. Returns true if card was played successfully.
    #[pyo3(signature = (hand_index, target_index=None, choice=None))]
    pub fn play_card(
        &mut self,
        hand_index: usize,
        target_index: Option<usize>,
        choice: Option<usize>,
    ) -> bool {
        let combat = match &mut self.phase {
            GamePhase::Combat(cs) => cs,
            _ => return false,
        };
        let result = combat.play_card(hand_index, target_index, choice);

        // Check if combat ended from the card play (e.g. killed all monsters)
        self.check_combat_end();
        result
    }

    /// End the player's turn: runs end-of-turn effects + monster turn.
    pub fn end_turn(&mut self) {
        let combat = match &mut self.phase {
            GamePhase::Combat(cs) => cs,
            _ => return,
        };
        combat.end_player_turn();
        combat.roll_and_execute_monsters();

        self.check_combat_end();
    }

    // ---- Card reward ----

    /// Pick a card reward by index. Adds it to the deck and advances.
    pub fn pick_card(&mut self, index: usize) {
        let card = match &self.phase {
            GamePhase::CardReward { options } => {
                if index >= options.len() {
                    return;
                }
                options[index]
            }
            _ => return,
        };
        self.deck.push(card);
        self.advance_to_next_room();
    }

    /// Skip the card reward and advance.
    pub fn skip_card(&mut self) {
        if !matches!(self.phase, GamePhase::CardReward { .. }) {
            return;
        }
        self.advance_to_next_room();
    }

    // ---- Event delegation ----

    /// Choose an event option.
    pub fn event_choose(&mut self, choice: usize) {
        let outcome = match &mut self.phase {
            GamePhase::Event(es) => es.choose(choice as i32),
            _ => return,
        };

        // Apply outcome to persistent state
        self.player_hp = (self.player_hp + outcome.hp_change)
            .min(self.player_max_hp)
            .max(0);
        self.player_max_hp += outcome.max_hp_change;
        self.gold = (self.gold + outcome.gold_change).max(0);
        for card in &outcome.cards_added {
            self.deck.push(*card);
        }
        if let Some(idx) = outcome.card_removed_index {
            if idx < self.deck.len() {
                self.deck.remove(idx);
            }
        }
        if let Some(idx) = outcome.card_upgraded_index {
            if idx < self.deck.len() {
                self.deck[idx] = CardInstance::new(self.deck[idx].card, true);
            }
        }
        if let Some(relic) = outcome.relic_added {
            self.relics.push(relic);
        }

        // Check if event is done
        let done = match &self.phase {
            GamePhase::Event(es) => es.done,
            _ => true,
        };
        if done {
            // Check player death from event damage
            if self.player_hp <= 0 {
                self.phase = GamePhase::GameOver { won: false };
            } else {
                self.advance_to_next_room();
            }
        }
    }

    // ---- Shop delegation ----

    /// Buy an item from the shop by index.
    pub fn shop_buy(&mut self, index: usize) {
        let item = match &self.phase {
            GamePhase::Shop { shop, phase: ShopPhase::Browsing } => {
                match shop.get_item(index) {
                    Some(item) => item,
                    None => return,
                }
            }
            _ => return,
        };

        if item.price > self.gold {
            return;
        }

        self.gold -= item.price;

        if item.item_type == "card" {
            if let Some(card) = item.card {
                self.deck.push(card);
            }
        } else if item.item_type == "relic" {
            if let Some(relic) = item.relic {
                self.relics.push(relic);
            }
        } else if item.item_type == "removal" {
            // Transition to card removal selection
            self.phase = match std::mem::replace(&mut self.phase, GamePhase::NotStarted) {
                GamePhase::Shop { shop, .. } => GamePhase::Shop {
                    shop,
                    phase: ShopPhase::ChoosingCardToRemove,
                },
                other => other,
            };
        }
    }

    /// Choose a card to remove from deck (during shop removal).
    pub fn shop_remove_card(&mut self, card_index: usize) {
        match &self.phase {
            GamePhase::Shop { phase: ShopPhase::ChoosingCardToRemove, .. } => {}
            _ => return,
        }
        if card_index < self.deck.len() {
            self.deck.remove(card_index);
        }
        // Return to browsing
        self.phase = match std::mem::replace(&mut self.phase, GamePhase::NotStarted) {
            GamePhase::Shop { shop, .. } => GamePhase::Shop {
                shop,
                phase: ShopPhase::Browsing,
            },
            other => other,
        };
    }

    /// Leave the shop and advance to the next room.
    pub fn shop_leave(&mut self) {
        if !matches!(self.phase, GamePhase::Shop { .. }) {
            return;
        }
        self.advance_to_next_room();
    }

    // ---- Rest site delegation ----

    /// Choose a rest site action (0 = rest, 1 = smith).
    pub fn rest_choose(&mut self, choice: usize) {
        let outcome = match &mut self.phase {
            GamePhase::RestSite { rest, .. } => rest.choose(choice as i32),
            _ => return,
        };

        // Apply healing
        if outcome.hp_healed > 0 {
            self.player_hp = (self.player_hp + outcome.hp_healed).min(self.player_max_hp);
        }

        if outcome.needs_card_select && outcome.card_select_action == "upgrade" {
            // Transition to card upgrade selection
            self.phase = match std::mem::replace(&mut self.phase, GamePhase::NotStarted) {
                GamePhase::RestSite { rest, .. } => GamePhase::RestSite {
                    rest,
                    phase: RestPhase::ChoosingCardToUpgrade,
                },
                other => other,
            };
        } else {
            self.advance_to_next_room();
        }
    }

    /// Choose a card to upgrade at the smithy.
    pub fn rest_upgrade_card(&mut self, card_index: usize) {
        match &self.phase {
            GamePhase::RestSite { phase: RestPhase::ChoosingCardToUpgrade, .. } => {}
            _ => return,
        }
        if card_index < self.deck.len() {
            let card = self.deck[card_index];
            if !card.upgraded && card.card.can_upgrade() {
                self.deck[card_index] = CardInstance::new(card.card, true);
            }
        }
        self.advance_to_next_room();
    }

    // ---- Query methods ----

    /// Get the current phase as a string.
    pub fn get_phase(&self) -> String {
        match &self.phase {
            GamePhase::NotStarted => "not_started".to_string(),
            GamePhase::Combat(_) => "combat".to_string(),
            GamePhase::Event(_) => "event".to_string(),
            GamePhase::Shop { phase, .. } => match phase {
                ShopPhase::Browsing => "shop".to_string(),
                ShopPhase::ChoosingCardToRemove => "shop_remove_card".to_string(),
            },
            GamePhase::RestSite { phase, .. } => match phase {
                RestPhase::ChoosingAction => "rest".to_string(),
                RestPhase::ChoosingCardToUpgrade => "rest_upgrade_card".to_string(),
            },
            GamePhase::CardReward { .. } => "card_reward".to_string(),
            GamePhase::GameOver { won } => {
                if *won { "victory".to_string() } else { "defeat".to_string() }
            }
        }
    }

    pub fn is_game_over(&self) -> bool {
        matches!(self.phase, GamePhase::GameOver { .. })
    }

    pub fn did_player_win(&self) -> bool {
        matches!(self.phase, GamePhase::GameOver { won: true })
    }

    pub fn get_current_room(&self) -> usize {
        self.current_room
    }

    pub fn get_player_hp(&self) -> i32 {
        match &self.phase {
            GamePhase::Combat(cs) => cs.player.hp,
            _ => self.player_hp,
        }
    }

    pub fn get_player_max_hp(&self) -> i32 {
        match &self.phase {
            GamePhase::Combat(cs) => cs.player.max_hp,
            _ => self.player_max_hp,
        }
    }

    pub fn get_gold(&self) -> i32 {
        self.gold
    }

    pub fn get_deck(&self) -> Vec<CardInstance> {
        self.deck.clone()
    }

    pub fn get_deck_size(&self) -> usize {
        self.deck.len()
    }

    /// Get the card reward options (when in CardReward phase).
    pub fn get_reward_options(&self) -> Vec<CardInstance> {
        match &self.phase {
            GamePhase::CardReward { options } => options.clone(),
            _ => vec![],
        }
    }

    /// Get the combat state's available actions (when in combat).
    pub fn get_hand(&self) -> Vec<CardInstance> {
        match &self.phase {
            GamePhase::Combat(cs) => cs.get_hand(),
            _ => vec![],
        }
    }

    /// Get monsters (when in combat).
    pub fn get_monsters(&self) -> Vec<Monster> {
        match &self.phase {
            GamePhase::Combat(cs) => cs.get_monsters(),
            _ => vec![],
        }
    }

    /// Get the combat player's energy (when in combat).
    pub fn get_energy(&self) -> i32 {
        match &self.phase {
            GamePhase::Combat(cs) => cs.player.energy,
            _ => 0,
        }
    }

    /// Get event choices (when in event phase).
    pub fn get_event_choices(&self) -> Vec<crate::events::EventChoice> {
        match &self.phase {
            GamePhase::Event(es) => es.get_choices(self.gold, self.player_hp, self.player_max_hp, Some(self.deck.clone())),
            _ => vec![],
        }
    }

    /// Get shop items (when in shop phase).
    pub fn get_shop_items(&self) -> Vec<crate::shop::ShopItem> {
        match &self.phase {
            GamePhase::Shop { shop, .. } => shop.items.clone(),
            _ => vec![],
        }
    }

    /// Get rest site choices (when in rest phase).
    pub fn get_rest_choices(&self) -> Vec<crate::rest::RestChoice> {
        match &self.phase {
            GamePhase::RestSite { rest, .. } => {
                rest.get_choices(Some(self.relics.clone()), Some(self.deck.clone()))
            }
            _ => vec![],
        }
    }
}

// ---- Internal methods ----

impl GameState {
    /// Check if combat has ended and transition accordingly.
    fn check_combat_end(&mut self) {
        let (combat_over, player_won, player_hp) = match &self.phase {
            GamePhase::Combat(cs) => (cs.combat_over, cs.player_won, cs.player.hp),
            _ => return,
        };

        if !combat_over {
            return;
        }

        // Sync player HP back from combat
        self.player_hp = player_hp;

        if player_won {
            // After boss, game is won — no card reward
            if self.rooms[self.current_room] == RoomType::Boss {
                self.phase = GamePhase::GameOver { won: true };
            } else {
                self.phase = GamePhase::CardReward {
                    options: self.reward_cards.clone(),
                };
            }
        } else {
            self.phase = GamePhase::GameOver { won: false };
        }
    }

    /// Advance to the next room in the linear map.
    fn advance_to_next_room(&mut self) {
        self.current_room += 1;
        if self.current_room >= self.rooms.len() {
            self.phase = GamePhase::GameOver { won: true };
            return;
        }
        self.enter_current_room();
    }

    /// Enter the current room, setting up the appropriate phase.
    fn enter_current_room(&mut self) {
        let room = self.rooms[self.current_room];
        match room {
            RoomType::Monster => {
                let monster = enemies::dummy::create();
                self.enter_combat(vec![monster]);
            }
            RoomType::Boss => {
                let monster = enemies::dummy::create_boss();
                self.enter_combat(vec![monster]);
            }
            RoomType::Event => {
                self.phase = GamePhase::Event(EventState::new(EventType::BigFish));
            }
            RoomType::Shop => {
                let shop = crate::shop::create_shop(Some(self.seed), None);
                self.phase = GamePhase::Shop {
                    shop,
                    phase: ShopPhase::Browsing,
                };
            }
            RoomType::Rest => {
                let rest = crate::rest::create_rest_site();
                self.phase = GamePhase::RestSite {
                    rest,
                    phase: RestPhase::ChoosingAction,
                };
            }
            _ => {
                // Skip unknown room types
                self.advance_to_next_room();
            }
        }
    }

    /// Set up and start combat with the given monsters.
    fn enter_combat(&mut self, monsters: Vec<Monster>) {
        let mut combat = CombatState::new_with_deck(
            monsters,
            Some(self.seed),
            self.deck.clone(),
            self.player_hp,
            self.player_max_hp,
            self.relics.clone(),
        );
        combat.start_combat();
        self.phase = GamePhase::Combat(combat);
    }
}
