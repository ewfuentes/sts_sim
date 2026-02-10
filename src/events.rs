use pyo3::prelude::*;

use crate::cards::{Card, CardInstance};
use crate::enums::{EventType, Relic};

/// Describes a single choice in an event.
#[pyclass]
#[derive(Clone, Debug)]
pub struct EventChoice {
    #[pyo3(get)]
    pub label: String,
    #[pyo3(get)]
    pub description: String,
    #[pyo3(get)]
    pub enabled: bool,
}

/// Describes the outcome of choosing an event option.
#[pyclass]
#[derive(Clone, Debug)]
pub struct EventOutcome {
    #[pyo3(get)]
    pub description: String,
    #[pyo3(get)]
    pub hp_change: i32,
    #[pyo3(get)]
    pub max_hp_change: i32,
    #[pyo3(get)]
    pub gold_change: i32,
    #[pyo3(get)]
    pub cards_added: Vec<CardInstance>,
    #[pyo3(get)]
    pub card_removed_index: Option<usize>,  // index into deck
    #[pyo3(get)]
    pub card_upgraded_index: Option<usize>,  // index into deck
    #[pyo3(get)]
    pub relic_added: Option<Relic>,
    #[pyo3(get)]
    pub done: bool,  // event is complete after this outcome
    #[pyo3(get)]
    pub needs_card_select: bool,  // player must select a card
    #[pyo3(get)]
    pub card_select_action: String,  // "remove", "upgrade", "transform"
}

impl EventOutcome {
    fn simple(desc: &str, hp: i32, gold: i32, done: bool) -> Self {
        EventOutcome {
            description: desc.to_string(),
            hp_change: hp,
            max_hp_change: 0,
            gold_change: gold,
            cards_added: vec![],
            card_removed_index: None,
            card_upgraded_index: None,
            relic_added: None,
            done,
            needs_card_select: false,
            card_select_action: String::new(),
        }
    }
}

/// Event state machine. Tracks an event's current stage and applies choices.
#[pyclass]
#[derive(Clone, Debug)]
pub struct EventState {
    #[pyo3(get)]
    pub event_type: EventType,
    #[pyo3(get)]
    pub stage: i32,
    #[pyo3(get)]
    pub done: bool,
    // Internal tracking
    picks_made: i32,  // for KnowingSkull
}

#[pymethods]
impl EventState {
    #[new]
    pub fn new(event_type: EventType) -> Self {
        EventState {
            event_type,
            stage: 0,
            done: false,
            picks_made: 0,
        }
    }

    /// Get the available choices at the current stage.
    /// `gold` and `hp` are used to determine which options are enabled.
    #[pyo3(signature = (gold=0, hp=0, max_hp=0, deck=None))]
    #[allow(unused_variables)]
    pub fn get_choices(&self, gold: i32, hp: i32, max_hp: i32, deck: Option<Vec<CardInstance>>) -> Vec<EventChoice> {
        match self.event_type {
            EventType::BigFish => self.big_fish_choices(&deck.unwrap_or_default()),
            EventType::GoldenIdol => self.golden_idol_choices(),
            EventType::GoldenWing => self.golden_wing_choices(),
            EventType::WorldOfGoop => self.world_of_goop_choices(gold),
            EventType::Cleric => self.cleric_choices(gold, &deck.unwrap_or_default()),
            EventType::LivingWall => self.living_wall_choices(&deck.unwrap_or_default()),
            EventType::ScrapOoze => self.scrap_ooze_choices(),
            EventType::DeadAdventurer => self.dead_adventurer_choices(),
            EventType::KnowingSkull => self.knowing_skull_choices(hp),
        }
    }

    /// Resolve a die roll for events that need it (Scrap Ooze, Dead Adventurer).
    /// roll should be 1-6.
    pub fn resolve_die_roll(&mut self, roll: i32) -> EventOutcome {
        match self.event_type {
            EventType::ScrapOoze => {
                match roll {
                    1 | 2 => EventOutcome::simple("The ooze stings! Take 1 damage. Try again?", -1, 0, false),
                    3 | 4 => EventOutcome::simple("Found 2 gold!", 0, 2, true),
                    5 | 6 => {
                        let mut outcome = EventOutcome::simple("Found a relic!", 0, 0, true);
                        outcome.relic_added = Some(Relic::Anchor);
                        outcome
                    },
                    _ => EventOutcome::simple("Invalid roll", 0, 0, false),
                }
            },
            EventType::DeadAdventurer => {
                match roll {
                    1 | 2 => EventOutcome::simple("An elite monster appears! Prepare for battle.", 0, 0, true),
                    3 | 4 => EventOutcome::simple("Found 2 gold on the body", 0, 2, true),
                    5 | 6 => {
                        let mut outcome = EventOutcome::simple("Found a relic!", 0, 0, true);
                        outcome.relic_added = Some(Relic::Anchor);
                        outcome
                    },
                    _ => EventOutcome::simple("Invalid roll", 0, 0, false),
                }
            },
            _ => EventOutcome::simple("This event doesn't use die rolls", 0, 0, false),
        }
    }

    /// Choose an option. Returns the outcome to apply.
    pub fn choose(&mut self, choice_index: i32) -> EventOutcome {
        let outcome = match self.event_type {
            EventType::BigFish => self.big_fish_choose(choice_index),
            EventType::GoldenIdol => self.golden_idol_choose(choice_index),
            EventType::GoldenWing => self.golden_wing_choose(choice_index),
            EventType::WorldOfGoop => self.world_of_goop_choose(choice_index),
            EventType::Cleric => self.cleric_choose(choice_index),
            EventType::LivingWall => self.living_wall_choose(choice_index),
            EventType::ScrapOoze => self.scrap_ooze_choose(choice_index),
            EventType::DeadAdventurer => self.dead_adventurer_choose(choice_index),
            EventType::KnowingSkull => self.knowing_skull_choose(choice_index),
        };
        if outcome.done {
            self.done = true;
        }
        outcome
    }
}

// ============================================================
// Event implementations
// ============================================================

impl EventState {
    // ---- Big Fish ----
    // Option 0: Banana — heal 2 HP
    // Option 1: Donut — upgrade a starter Strike
    // Option 2: Box — gain random relic + random curse
    // Option 3: Remove Strike — remove a starter Strike from deck

    fn big_fish_choices(&self, deck: &[CardInstance]) -> Vec<EventChoice> {
        let has_strike = deck.iter().any(|c| c.card == Card::StrikeRed && !c.upgraded);
        let has_any_strike = deck.iter().any(|c| c.card == Card::StrikeRed);
        vec![
            EventChoice {
                label: "Banana".to_string(),
                description: "Heal 2 HP".to_string(),
                enabled: true,
            },
            EventChoice {
                label: "Donut".to_string(),
                description: "Upgrade a Strike".to_string(),
                enabled: has_strike,
            },
            EventChoice {
                label: "Box".to_string(),
                description: "Gain a random curse and a random relic".to_string(),
                enabled: true,
            },
            EventChoice {
                label: "Remove Strike".to_string(),
                description: "Remove a Strike from your deck".to_string(),
                enabled: has_any_strike,
            },
        ]
    }

    fn big_fish_choose(&mut self, choice: i32) -> EventOutcome {
        self.done = true;
        match choice {
            0 => EventOutcome::simple("Healed 2 HP", 2, 0, true),
            1 => {
                // Upgrade a Strike — needs card select
                let mut outcome = EventOutcome::simple("Upgrade a Strike", 0, 0, true);
                outcome.needs_card_select = true;
                outcome.card_select_action = "upgrade".to_string();
                outcome
            },
            2 => {
                // Gain curse + relic
                let mut outcome = EventOutcome::simple("Gained a curse and a relic", 0, 0, true);
                outcome.cards_added = vec![CardInstance::new(Card::Injury, false)];
                // Relic would be random — for now give a fixed common relic
                outcome.relic_added = Some(Relic::Anchor);
                outcome
            },
            3 => {
                // Remove Strike — needs card select
                let mut outcome = EventOutcome::simple("Remove a Strike", 0, 0, true);
                outcome.needs_card_select = true;
                outcome.card_select_action = "remove".to_string();
                outcome
            },
            _ => EventOutcome::simple("Invalid choice", 0, 0, true),
        }
    }

    // ---- Golden Idol ----
    // Stage 0: Touch idol or Leave
    // Stage 1 (after touching): Take 1 damage (boulder trap)

    fn golden_idol_choices(&self) -> Vec<EventChoice> {
        match self.stage {
            0 => vec![
                EventChoice {
                    label: "Touch the idol".to_string(),
                    description: "Gain a relic, then face a boulder trap".to_string(),
                    enabled: true,
                },
                EventChoice {
                    label: "Leave".to_string(),
                    description: "Nothing happens".to_string(),
                    enabled: true,
                },
            ],
            _ => vec![
                EventChoice {
                    label: "Outrun the boulder".to_string(),
                    description: "Take 1 damage".to_string(),
                    enabled: true,
                },
            ],
        }
    }

    fn golden_idol_choose(&mut self, choice: i32) -> EventOutcome {
        match self.stage {
            0 => {
                if choice == 1 {
                    // Leave
                    return EventOutcome::simple("Left the idol alone", 0, 0, true);
                }
                // Touch — gain relic, advance to boulder stage
                self.stage = 1;
                let mut outcome = EventOutcome::simple("Took the idol!", 0, 0, false);
                outcome.relic_added = Some(Relic::Anchor);
                outcome
            },
            _ => {
                // Boulder — take 1 damage
                EventOutcome::simple("The boulder hits you for 1 damage", -1, 0, true)
            },
        }
    }

    // ---- Golden Wing ----
    // Option 0: Pursue — take 2 damage, remove a card from deck
    // Option 1: Demand Gold — gain 2 gold

    fn golden_wing_choices(&self) -> Vec<EventChoice> {
        match self.stage {
            0 => vec![
                EventChoice {
                    label: "Pursue".to_string(),
                    description: "Take 2 damage, remove a card".to_string(),
                    enabled: true,
                },
                EventChoice {
                    label: "Demand Gold".to_string(),
                    description: "Gain 2 gold".to_string(),
                    enabled: true,
                },
            ],
            _ => vec![], // Card select happens externally
        }
    }

    fn golden_wing_choose(&mut self, choice: i32) -> EventOutcome {
        match choice {
            0 => {
                // Pursue — take 2 damage, then remove a card
                let mut outcome = EventOutcome::simple("Took 2 damage, remove a card", -2, 0, true);
                outcome.needs_card_select = true;
                outcome.card_select_action = "remove".to_string();
                outcome
            },
            1 => EventOutcome::simple("Gained 2 gold", 0, 2, true),
            _ => EventOutcome::simple("Invalid choice", 0, 0, true),
        }
    }

    // ---- World of Goop ----
    // Option 0: Gather Gold — take 2 damage, gain 3 gold
    // Option 1: Demand Relic — gain relic + curse
    // Option 2: Leave — lose 1 gold

    fn world_of_goop_choices(&self, gold: i32) -> Vec<EventChoice> {
        vec![
            EventChoice {
                label: "Gather Gold".to_string(),
                description: "Take 2 damage, gain 3 gold".to_string(),
                enabled: true,
            },
            EventChoice {
                label: "Demand Relic".to_string(),
                description: "Gain a relic and a curse".to_string(),
                enabled: true,
            },
            EventChoice {
                label: "Leave".to_string(),
                description: format!("Lose {} gold", gold.min(1)),
                enabled: true,
            },
        ]
    }

    fn world_of_goop_choose(&mut self, choice: i32) -> EventOutcome {
        match choice {
            0 => EventOutcome::simple("Took 2 damage, gained 3 gold", -2, 3, true),
            1 => {
                let mut outcome = EventOutcome::simple("Gained a relic and a curse", 0, 0, true);
                outcome.relic_added = Some(Relic::Anchor);
                outcome.cards_added = vec![CardInstance::new(Card::Injury, false)];
                outcome
            },
            2 => EventOutcome::simple("Left with less gold", 0, -1, true),
            _ => EventOutcome::simple("Invalid choice", 0, 0, true),
        }
    }

    // ---- Cleric ----
    // Option 0: Heal — cost 1 gold, heal 3 HP
    // Option 1: Upgrade — cost 2 gold, upgrade a card
    // Option 2: Purify — cost 3 gold, remove a card
    // Option 3: Leave

    fn cleric_choices(&self, gold: i32, deck: &[CardInstance]) -> Vec<EventChoice> {
        let has_upgradable = deck.iter().any(|c| !c.upgraded && c.card.can_upgrade());
        let has_removable = deck.len() > 1; // don't allow removing last card
        vec![
            EventChoice {
                label: "Heal".to_string(),
                description: "Pay 1 gold, heal 3 HP".to_string(),
                enabled: gold >= 1,
            },
            EventChoice {
                label: "Upgrade".to_string(),
                description: "Pay 2 gold, upgrade a card".to_string(),
                enabled: gold >= 2 && has_upgradable,
            },
            EventChoice {
                label: "Purify".to_string(),
                description: "Pay 3 gold, remove a card".to_string(),
                enabled: gold >= 3 && has_removable,
            },
            EventChoice {
                label: "Leave".to_string(),
                description: "Nothing happens".to_string(),
                enabled: true,
            },
        ]
    }

    fn cleric_choose(&mut self, choice: i32) -> EventOutcome {
        match choice {
            0 => EventOutcome::simple("Healed 3 HP for 1 gold", 3, -1, true),
            1 => {
                let mut outcome = EventOutcome::simple("Upgrade a card for 2 gold", 0, -2, true);
                outcome.needs_card_select = true;
                outcome.card_select_action = "upgrade".to_string();
                outcome
            },
            2 => {
                let mut outcome = EventOutcome::simple("Remove a card for 3 gold", 0, -3, true);
                outcome.needs_card_select = true;
                outcome.card_select_action = "remove".to_string();
                outcome
            },
            3 => EventOutcome::simple("Left the cleric", 0, 0, true),
            _ => EventOutcome::simple("Invalid choice", 0, 0, true),
        }
    }

    // ---- Living Wall ----
    // Option 0: Forget — remove a card
    // Option 1: Change — transform a card (remove + add random)
    // Option 2: Grow — upgrade a card

    fn living_wall_choices(&self, deck: &[CardInstance]) -> Vec<EventChoice> {
        let has_upgradable = deck.iter().any(|c| !c.upgraded && c.card.can_upgrade());
        let has_removable = deck.len() > 1;
        vec![
            EventChoice {
                label: "Forget".to_string(),
                description: "Remove a card from your deck".to_string(),
                enabled: has_removable,
            },
            EventChoice {
                label: "Change".to_string(),
                description: "Transform a card".to_string(),
                enabled: has_removable,
            },
            EventChoice {
                label: "Grow".to_string(),
                description: "Upgrade a card".to_string(),
                enabled: has_upgradable,
            },
        ]
    }

    fn living_wall_choose(&mut self, choice: i32) -> EventOutcome {
        match choice {
            0 => {
                let mut outcome = EventOutcome::simple("Remove a card", 0, 0, true);
                outcome.needs_card_select = true;
                outcome.card_select_action = "remove".to_string();
                outcome
            },
            1 => {
                let mut outcome = EventOutcome::simple("Transform a card", 0, 0, true);
                outcome.needs_card_select = true;
                outcome.card_select_action = "transform".to_string();
                outcome
            },
            2 => {
                let mut outcome = EventOutcome::simple("Upgrade a card", 0, 0, true);
                outcome.needs_card_select = true;
                outcome.card_select_action = "upgrade".to_string();
                outcome
            },
            _ => EventOutcome::simple("Invalid choice", 0, 0, true),
        }
    }

    // ---- Scrap Ooze ----
    // Roll die: 1-2 = take 1 damage + reroll, 3-4 = gain 2 gold, 5-6 = gain relic
    // Option 0: Reach in (roll)
    // Option 1: Leave

    fn scrap_ooze_choices(&self) -> Vec<EventChoice> {
        vec![
            EventChoice {
                label: "Reach in".to_string(),
                description: "Roll the die: 1-2 take damage, 3-4 gain gold, 5-6 gain relic".to_string(),
                enabled: true,
            },
            EventChoice {
                label: "Leave".to_string(),
                description: "Nothing happens".to_string(),
                enabled: true,
            },
        ]
    }

    fn scrap_ooze_choose(&mut self, choice: i32) -> EventOutcome {
        match choice {
            0 => {
                // Roll result is determined externally (die roll).
                // Return a "needs die roll" marker. The caller should roll and call choose_with_roll.
                EventOutcome::simple("Roll the die!", 0, 0, false)
            },
            1 => EventOutcome::simple("Left the scrap ooze alone", 0, 0, true),
            _ => EventOutcome::simple("Invalid choice", 0, 0, true),
        }
    }

    // ---- Dead Adventurer ----
    // Same die-roll pattern as Scrap Ooze
    // 1-2: elite fight, 3-4: gain 2 gold, 5-6: gain relic

    fn dead_adventurer_choices(&self) -> Vec<EventChoice> {
        vec![
            EventChoice {
                label: "Search the body".to_string(),
                description: "Roll the die: 1-2 elite fight, 3-4 gain gold, 5-6 gain relic".to_string(),
                enabled: true,
            },
            EventChoice {
                label: "Leave".to_string(),
                description: "Nothing happens".to_string(),
                enabled: true,
            },
        ]
    }

    fn dead_adventurer_choose(&mut self, choice: i32) -> EventOutcome {
        match choice {
            0 => EventOutcome::simple("Roll the die!", 0, 0, false),
            1 => EventOutcome::simple("Left the dead adventurer", 0, 0, true),
            _ => EventOutcome::simple("Invalid choice", 0, 0, true),
        }
    }

    // ---- Knowing Skull ----
    // Up to 2 picks with escalating cost
    // Option 0: Potion — cost (picks+1) HP
    // Option 1: Gold — cost (picks+1) HP, gain 3 gold
    // Option 2: Card — cost (picks+1) HP, gain a card
    // Option 3: Leave

    fn knowing_skull_choices(&self, hp: i32) -> Vec<EventChoice> {
        if self.picks_made >= 2 {
            return vec![
                EventChoice {
                    label: "Leave".to_string(),
                    description: "The skull has nothing left to offer".to_string(),
                    enabled: true,
                },
            ];
        }
        let cost = self.picks_made + 1;
        let can_afford = hp > cost; // must survive
        vec![
            EventChoice {
                label: "Potion".to_string(),
                description: format!("Lose {} HP, gain a potion", cost),
                enabled: can_afford,
            },
            EventChoice {
                label: "Gold".to_string(),
                description: format!("Lose {} HP, gain 3 gold", cost),
                enabled: can_afford,
            },
            EventChoice {
                label: "Card".to_string(),
                description: format!("Lose {} HP, gain a card", cost),
                enabled: can_afford,
            },
            EventChoice {
                label: "Leave".to_string(),
                description: "Walk away".to_string(),
                enabled: true,
            },
        ]
    }

    fn knowing_skull_choose(&mut self, choice: i32) -> EventOutcome {
        if self.picks_made >= 2 || choice == 3 {
            return EventOutcome::simple("Left the skull behind", 0, 0, true);
        }
        let cost = self.picks_made + 1;
        self.picks_made += 1;
        let is_last = self.picks_made >= 2;
        match choice {
            0 => {
                // Potion — we don't model potions yet, so just take the HP loss
                EventOutcome::simple(
                    &format!("Lost {} HP, gained a potion", cost),
                    -cost, 0, is_last,
                )
            },
            1 => {
                EventOutcome::simple(
                    &format!("Lost {} HP, gained 3 gold", cost),
                    -cost, 3, is_last,
                )
            },
            2 => {
                // Card — needs card reward selection
                let mut outcome = EventOutcome::simple(
                    &format!("Lost {} HP, choose a card", cost),
                    -cost, 0, is_last,
                );
                outcome.needs_card_select = true;
                outcome.card_select_action = "add".to_string();
                outcome
            },
            _ => EventOutcome::simple("Invalid choice", 0, 0, true),
        }
    }
}


/// Create an event by name.
#[pyfunction]
pub fn create_event(name: &str) -> PyResult<EventState> {
    let event_type = match name {
        "big_fish" => EventType::BigFish,
        "golden_idol" => EventType::GoldenIdol,
        "golden_wing" => EventType::GoldenWing,
        "world_of_goop" => EventType::WorldOfGoop,
        "cleric" => EventType::Cleric,
        "living_wall" => EventType::LivingWall,
        "scrap_ooze" => EventType::ScrapOoze,
        "dead_adventurer" => EventType::DeadAdventurer,
        "knowing_skull" => EventType::KnowingSkull,
        _ => return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            format!("Unknown event: {}", name),
        )),
    };
    Ok(EventState::new(event_type))
}
