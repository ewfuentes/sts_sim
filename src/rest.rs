use pyo3::prelude::*;

use crate::cards::CardInstance;
use crate::enums::Relic;

/// Rest site choice result.
#[pyclass]
#[derive(Clone, Debug)]
pub struct RestOutcome {
    #[pyo3(get)]
    pub description: String,
    #[pyo3(get)]
    pub hp_healed: i32,
    #[pyo3(get)]
    pub needs_card_select: bool,  // true for Smith
    #[pyo3(get)]
    pub card_select_action: String,  // "upgrade" for Smith
}

/// Rest site choices.
#[pyclass]
#[derive(Clone, Debug)]
pub struct RestChoice {
    #[pyo3(get)]
    pub label: String,
    #[pyo3(get)]
    pub description: String,
    #[pyo3(get)]
    pub enabled: bool,
}

/// Rest site state.
#[pyclass]
#[derive(Clone, Debug)]
pub struct RestSite {
    #[pyo3(get)]
    pub done: bool,
}

#[pymethods]
impl RestSite {
    #[new]
    pub fn new() -> Self {
        RestSite { done: false }
    }

    /// Get the available choices at a rest site.
    /// Pass the player's relics list and deck for checking.
    #[pyo3(signature = (relics=None, deck=None))]
    pub fn get_choices(&self, relics: Option<Vec<Relic>>, deck: Option<Vec<CardInstance>>) -> Vec<RestChoice> {
        let has_regal_pillow = relics.as_ref()
            .map(|r| r.contains(&Relic::BurningBlood))  // placeholder: no Regal Pillow relic yet
            .unwrap_or(false);

        let has_upgradable = deck.as_ref()
            .map(|d| d.iter().any(|c| !c.upgraded && c.card.can_upgrade()))
            .unwrap_or(true);

        vec![
            RestChoice {
                label: "Rest".to_string(),
                description: "Heal 3 HP".to_string(),
                enabled: true,
            },
            RestChoice {
                label: "Smith".to_string(),
                description: "Upgrade a card".to_string(),
                enabled: has_upgradable,
            },
        ]
    }

    /// Choose rest or smith.
    pub fn choose(&mut self, choice_index: i32) -> RestOutcome {
        self.done = true;
        match choice_index {
            0 => RestOutcome {
                description: "Rested and healed 3 HP".to_string(),
                hp_healed: 3,
                needs_card_select: false,
                card_select_action: String::new(),
            },
            1 => RestOutcome {
                description: "Choose a card to upgrade".to_string(),
                hp_healed: 0,
                needs_card_select: true,
                card_select_action: "upgrade".to_string(),
            },
            _ => RestOutcome {
                description: "Invalid choice".to_string(),
                hp_healed: 0,
                needs_card_select: false,
                card_select_action: String::new(),
            },
        }
    }
}

/// Create a rest site.
#[pyfunction]
pub fn create_rest_site() -> RestSite {
    RestSite::new()
}
