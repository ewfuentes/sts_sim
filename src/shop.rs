use pyo3::prelude::*;
use rand::rngs::StdRng;
use rand::seq::SliceRandom;
use rand::SeedableRng;

use crate::cards::{Card, CardInstance};
use crate::enums::{CardRarity, Character, Relic};
use crate::rewards::{card_price, get_card_rarity};

/// A shop item for sale.
#[pyclass]
#[derive(Clone, Debug)]
pub struct ShopItem {
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub price: i32,
    #[pyo3(get)]
    pub item_type: String,  // "card", "relic", "removal"
    #[pyo3(get)]
    pub card: Option<CardInstance>,
    #[pyo3(get)]
    pub relic: Option<Relic>,
}

/// The shop state.
#[pyclass]
#[derive(Clone, Debug)]
pub struct ShopState {
    #[pyo3(get)]
    pub items: Vec<ShopItem>,
    #[pyo3(get)]
    pub removal_cost: i32,
}

#[pymethods]
impl ShopState {
    /// Buy an item by index. Returns the item if player has enough gold.
    /// Does not modify player gold (caller handles that).
    pub fn get_item(&self, index: usize) -> Option<ShopItem> {
        self.items.get(index).cloned()
    }

    /// Get the card removal cost.
    pub fn get_removal_cost(&self) -> i32 {
        self.removal_cost
    }
}

/// Generate a shop with cards and a relic for sale.
#[pyfunction]
#[pyo3(signature = (seed=None, character=None))]
pub fn create_shop(seed: Option<u64>, character: Option<Character>) -> ShopState {
    let s = seed.unwrap_or(0);
    let mut rng = StdRng::seed_from_u64(s);

    let mut items = Vec::new();

    // Generate 5 cards for sale: 3 common, 1 uncommon, 1 rare
    let commons = vec![
        Card::Anger, Card::BodySlam, Card::Clash, Card::Cleave,
        Card::Clothesline, Card::HeavyBlade, Card::IronWave,
        Card::PerfectedStrike, Card::PommelStrike, Card::TwinStrike,
        Card::WildStrike, Card::Flex, Card::Havoc, Card::SeeingRed,
        Card::ShrugItOff, Card::TrueGrit, Card::Warcry,
    ];
    let uncommons = vec![
        Card::BloodForBlood, Card::Carnage, Card::Headbutt,
        Card::Rampage, Card::SeverSoul,
        Card::Uppercut, Card::Whirlwind, Card::BattleTrance,
        Card::BurningPact, Card::Disarm, Card::Entrench,
        Card::FlameBarrier, Card::GhostlyArmor,
        Card::PowerThrough, Card::RageCard, Card::SecondWind,
        Card::Sentinel, Card::Shockwave, Card::SpotWeakness,
        Card::Inflame,
        Card::Metallicize, Card::CombustCard, Card::DarkEmbrace,
        Card::Evolve, Card::FeelNoPain, Card::FireBreathing,
        Card::Rupture,
    ];
    let rares = vec![
        Card::Bludgeon, Card::Feed, Card::FiendFire, Card::Immolate,
        Card::DoubleTap, Card::Exhume, Card::LimitBreak,
        Card::Offering, Card::Impervious, Card::Barricade,
        Card::BerserkCard, Card::Corruption, Card::DemonForm,
        Card::Juggernaut,
    ];

    // Pick 3 commons
    let mut common_pool = commons;
    common_pool.shuffle(&mut rng);
    for &card in common_pool.iter().take(3) {
        let ci = CardInstance::new(card, false);
        items.push(ShopItem {
            name: ci.card.name().to_string(),
            price: card_price(CardRarity::Common),
            item_type: "card".to_string(),
            card: Some(ci),
            relic: None,
        });
    }

    // Pick 1 uncommon
    let mut uncommon_pool = uncommons;
    uncommon_pool.shuffle(&mut rng);
    if let Some(&card) = uncommon_pool.first() {
        let ci = CardInstance::new(card, false);
        items.push(ShopItem {
            name: ci.card.name().to_string(),
            price: card_price(CardRarity::Uncommon),
            item_type: "card".to_string(),
            card: Some(ci),
            relic: None,
        });
    }

    // Pick 1 rare
    let mut rare_pool = rares;
    rare_pool.shuffle(&mut rng);
    if let Some(&card) = rare_pool.first() {
        let ci = CardInstance::new(card, false);
        items.push(ShopItem {
            name: ci.card.name().to_string(),
            price: card_price(CardRarity::Rare),
            item_type: "card".to_string(),
            card: Some(ci),
            relic: None,
        });
    }

    // Card removal option
    items.push(ShopItem {
        name: "Card Removal".to_string(),
        price: 3,
        item_type: "removal".to_string(),
        card: None,
        relic: None,
    });

    ShopState {
        items,
        removal_cost: 3,
    }
}
