use pyo3::prelude::*;

mod enums;
mod creature;
mod die;
mod powers;
mod damage;
mod cards;
mod enemies;
mod encounters;
mod combat;
mod relics;
mod events;
mod map;
mod rewards;
mod shop;
mod rest;

#[pymodule]
fn sts_sim(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<enums::Character>()?;
    m.add_class::<enums::CardType>()?;
    m.add_class::<enums::PowerType>()?;
    m.add_class::<enums::Intent>()?;
    m.add_class::<enums::Relic>()?;
    m.add_class::<enums::EventType>()?;
    m.add_class::<enums::RoomType>()?;
    m.add_class::<enums::OrbType>()?;
    m.add_class::<enums::Stance>()?;
    m.add_class::<enums::CardRarity>()?;
    m.add_class::<creature::Player>()?;
    m.add_class::<creature::Monster>()?;
    m.add_class::<die::TheDie>()?;
    m.add_class::<combat::CombatState>()?;
    m.add_class::<cards::Card>()?;
    m.add_class::<cards::CardInstance>()?;
    m.add_class::<events::EventState>()?;
    m.add_class::<events::EventChoice>()?;
    m.add_class::<events::EventOutcome>()?;
    m.add_class::<map::MapNode>()?;
    m.add_class::<map::ActMap>()?;
    m.add_class::<rewards::RewardDeck>()?;
    m.add_class::<shop::ShopState>()?;
    m.add_class::<shop::ShopItem>()?;
    m.add_class::<rest::RestSite>()?;
    m.add_class::<rest::RestChoice>()?;
    m.add_class::<rest::RestOutcome>()?;
    m.add_function(wrap_pyfunction!(encounters::create_encounter, m)?)?;
    m.add_function(wrap_pyfunction!(events::create_event, m)?)?;
    m.add_function(wrap_pyfunction!(map::generate_map, m)?)?;
    m.add_function(wrap_pyfunction!(shop::create_shop, m)?)?;
    m.add_function(wrap_pyfunction!(rest::create_rest_site, m)?)?;
    Ok(())
}
