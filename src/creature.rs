use pyo3::prelude::*;
use std::collections::HashMap;

use crate::enums::{CardType, Character, Intent, OrbType, PowerType, Relic, Stance};

#[pyclass]
#[derive(Clone, Debug)]
pub struct Player {
    #[pyo3(get, set)]
    pub name: String,
    #[pyo3(get, set)]
    pub hp: i32,
    #[pyo3(get, set)]
    pub max_hp: i32,
    #[pyo3(get, set)]
    pub block: i32,
    #[pyo3(get, set)]
    pub block_cap: i32,
    #[pyo3(get, set)]
    pub energy: i32,
    #[pyo3(get, set)]
    pub max_energy: i32,
    #[pyo3(get, set)]
    pub draw_amount: i32,
    #[pyo3(get, set)]
    pub gold: i32,
    pub powers: HashMap<PowerType, i32>,
    pub draw_pile: Vec<usize>,    // indices into deck
    pub discard_pile: Vec<usize>, // indices into deck
    pub exhaust_pile: Vec<usize>, // indices into deck
    pub hand_indices: Vec<usize>, // indices into deck
    pub relics: Vec<Relic>,
    // Defect orb system
    pub orbs: Vec<OrbType>,
    #[pyo3(get, set)]
    pub orb_slots: i32,
    // Watcher stance system
    pub stance: Stance,
    // Free play: next card of matching type costs 0 energy
    pub free_play_for: Option<Vec<CardType>>,
}

#[pymethods]
impl Player {
    #[new]
    #[pyo3(signature = (character=None))]
    pub fn new(character: Option<Character>) -> Self {
        let ch = character.unwrap_or(Character::Ironclad);
        let (name, hp, relics) = match ch {
            Character::Ironclad => ("Ironclad", 10, vec![Relic::BurningBlood]),
            Character::Silent => ("Silent", 9, vec![Relic::RingOfTheSnake, Relic::Shivs]),
            Character::Defect => ("Defect", 9, vec![Relic::CrackedCore]),
            Character::Watcher => ("Watcher", 9, vec![Relic::Miracles]),
        };
        Player {
            name: name.to_string(),
            hp,
            max_hp: hp,
            block: 0,
            block_cap: 20,
            energy: 0,
            max_energy: 3,
            draw_amount: 5,
            gold: 0,
            powers: HashMap::new(),
            draw_pile: Vec::new(),
            discard_pile: Vec::new(),
            exhaust_pile: Vec::new(),
            hand_indices: Vec::new(),
            relics,
            orbs: Vec::new(),
            orb_slots: if ch == Character::Defect { 3 } else { 0 },
            stance: Stance::Neutral,
            free_play_for: None,
        }
    }

    pub fn has_relic(&self, relic: Relic) -> bool {
        self.relics.contains(&relic)
    }

    pub fn get_power(&self, power: PowerType) -> i32 {
        *self.powers.get(&power).unwrap_or(&0)
    }

    pub fn get_powers_dict(&self) -> HashMap<String, i32> {
        self.powers.iter().map(|(k, v)| (format!("{:?}", k), *v)).collect()
    }

    pub fn get_hand_indices(&self) -> Vec<usize> {
        self.hand_indices.clone()
    }

    pub fn get_draw_pile(&self) -> Vec<usize> {
        self.draw_pile.clone()
    }

    pub fn get_discard_pile(&self) -> Vec<usize> {
        self.discard_pile.clone()
    }

    pub fn get_exhaust_pile(&self) -> Vec<usize> {
        self.exhaust_pile.clone()
    }

    pub fn apply_power(&mut self, power: PowerType, amount: i32) {
        // Artifact blocks debuffs
        if amount > 0 && is_debuff(power) {
            let artifact = self.powers.get(&PowerType::Artifact).copied().unwrap_or(0);
            if artifact > 0 {
                self.reduce_power(PowerType::Artifact, 1);
                return;
            }
        }

        let cap = power_cap(power);
        let current = self.powers.entry(power).or_insert(0);
        *current = (*current + amount).min(cap);
        if *current <= 0 && !can_be_negative(power) {
            self.powers.remove(&power);
        }
    }

    pub fn reduce_power(&mut self, power: PowerType, amount: i32) {
        if let Some(current) = self.powers.get_mut(&power) {
            *current -= amount;
            if *current <= 0 && !can_be_negative(power) {
                self.powers.remove(&power);
            }
        }
    }

    /// Get the list of orbs currently channeled.
    pub fn get_orbs(&self) -> Vec<OrbType> {
        self.orbs.clone()
    }

    /// Get number of orbs currently channeled.
    pub fn get_orb_count(&self) -> i32 {
        self.orbs.len() as i32
    }

    /// Get the current stance.
    pub fn get_stance(&self) -> Stance {
        self.stance
    }

    /// Get the current miracle count.
    pub fn get_miracles(&self) -> i32 {
        self.get_power(PowerType::MiracleCount)
    }
}

impl Player {
    pub fn add_block(&mut self, amount: i32) {
        self.block = (self.block + amount).min(self.block_cap);
    }

    pub fn is_dead(&self) -> bool {
        self.hp <= 0
    }

    pub fn heal(&mut self, amount: i32) {
        self.hp = (self.hp + amount).min(self.max_hp);
    }

    /// Channel an orb. Returns Some(OrbType) if an orb was auto-evoked due to full slots.
    pub fn channel_orb(&mut self, orb: OrbType) -> Option<OrbType> {
        if self.orb_slots <= 0 {
            return None;
        }
        let mut evoked = None;
        if self.orbs.len() >= self.orb_slots as usize {
            // Auto-evoke first orb (index 0) when at capacity
            evoked = Some(self.orbs.remove(0));
        }
        self.orbs.push(orb);
        evoked
    }

    /// Remove and return orb at given index. Returns None if index invalid.
    pub fn remove_orb(&mut self, index: usize) -> Option<OrbType> {
        if index < self.orbs.len() {
            Some(self.orbs.remove(index))
        } else {
            None
        }
    }

    /// Remove all orbs and return them.
    pub fn remove_all_orbs(&mut self) -> Vec<OrbType> {
        std::mem::take(&mut self.orbs)
    }

    /// Enter a new stance. Returns the energy gained from exiting Calm (0 otherwise).
    /// Returns (energy_gained, stance_changed).
    pub fn enter_stance(&mut self, new_stance: Stance) -> (i32, bool) {
        if self.stance == new_stance {
            return (0, false);
        }
        let mut energy_gained = 0;
        // Exit current stance
        if self.stance == Stance::Calm {
            energy_gained = 2;
        }
        self.stance = new_stance;
        (energy_gained, true)
    }
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct Monster {
    #[pyo3(get, set)]
    pub name: String,
    #[pyo3(get, set)]
    pub hp: i32,
    #[pyo3(get, set)]
    pub max_hp: i32,
    #[pyo3(get, set)]
    pub block: i32,
    #[pyo3(get, set)]
    pub monster_id: String,
    #[pyo3(get, set)]
    pub behavior: String,
    #[pyo3(get, set)]
    pub die_controlled: bool,
    #[pyo3(get, set)]
    pub first_turn: bool,
    #[pyo3(get, set)]
    pub turn_count: i32,
    #[pyo3(get, set)]
    pub half_dead: bool,
    pub powers: HashMap<PowerType, i32>,
    pub current_move: char,
    pub intent: Intent,
}

#[pymethods]
impl Monster {
    #[new]
    #[pyo3(signature = (name, hp, monster_id, behavior, die_controlled))]
    pub fn new(name: String, hp: i32, monster_id: String, behavior: String, die_controlled: bool) -> Self {
        Monster {
            name,
            max_hp: hp,
            hp,
            block: 0,
            monster_id,
            behavior,
            die_controlled,
            first_turn: true,
            turn_count: 0,
            half_dead: false,
            powers: HashMap::new(),
            current_move: ' ',
            intent: Intent::Unknown,
        }
    }

    pub fn get_power(&self, power: PowerType) -> i32 {
        *self.powers.get(&power).unwrap_or(&0)
    }

    pub fn get_powers_dict(&self) -> HashMap<String, i32> {
        self.powers.iter().map(|(k, v)| (format!("{:?}", k), *v)).collect()
    }

    pub fn get_current_move(&self) -> String {
        self.current_move.to_string()
    }

    pub fn get_intent(&self) -> Intent {
        self.intent
    }

    pub fn is_dead(&self) -> bool {
        self.hp <= 0 && !self.half_dead
    }

    pub fn add_block(&mut self, amount: i32) {
        self.block += amount;
    }

    pub fn apply_power(&mut self, power: PowerType, amount: i32) {
        // Artifact blocks debuffs
        if amount > 0 && is_debuff(power) {
            let artifact = self.powers.get(&PowerType::Artifact).copied().unwrap_or(0);
            if artifact > 0 {
                self.reduce_power(PowerType::Artifact, 1);
                return;
            }
        }

        let cap = power_cap(power);
        let current = self.powers.entry(power).or_insert(0);
        *current = (*current + amount).min(cap);
        if *current <= 0 && !can_be_negative(power) {
            self.powers.remove(&power);
        }
    }

    pub fn reduce_power(&mut self, power: PowerType, amount: i32) {
        if let Some(current) = self.powers.get_mut(&power) {
            *current -= amount;
            if *current <= 0 && !can_be_negative(power) {
                self.powers.remove(&power);
            }
        }
    }
}

/// Get the power cap for a given power type.
pub fn power_cap(power: PowerType) -> i32 {
    match power {
        PowerType::Vulnerable => 3,
        PowerType::Weak => 3,
        PowerType::Entangled | PowerType::NoDraw | PowerType::Barricade | PowerType::Corruption => 1,
        _ => 999,
    }
}

/// Returns true if this power is a debuff (blocked by Artifact).
pub fn is_debuff(power: PowerType) -> bool {
    matches!(power,
        PowerType::Vulnerable |
        PowerType::Weak |
        PowerType::Entangled |
        PowerType::NoDraw
    )
}

/// Returns true if this power can have negative values (e.g. Strength, Dexterity).
pub fn can_be_negative(power: PowerType) -> bool {
    matches!(power, PowerType::Strength | PowerType::Dexterity)
}
