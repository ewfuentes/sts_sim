use pyo3::prelude::*;
use rand::rngs::StdRng;
use rand::seq::SliceRandom;
use rand::SeedableRng;

use crate::cards::{Card, CardInstance};
use crate::enums::{CardRarity, Character};

/// The Ironclad card reward pool, split by rarity.
fn ironclad_commons() -> Vec<Card> {
    vec![
        Card::Anger, Card::BodySlam, Card::Clash, Card::Cleave,
        Card::Clothesline, Card::HeavyBlade, Card::IronWave,
        Card::PerfectedStrike, Card::PommelStrike, Card::TwinStrike,
        Card::WildStrike,
        Card::Flex, Card::Havoc, Card::SeeingRed, Card::ShrugItOff,
        Card::TrueGrit, Card::Warcry,
    ]
}

fn ironclad_uncommons() -> Vec<Card> {
    vec![
        Card::BloodForBlood, Card::Carnage, Card::Headbutt,
        Card::Rampage, Card::SeverSoul,
        Card::Uppercut, Card::Whirlwind,
        Card::BattleTrance, Card::BurningPact, Card::Disarm,
        Card::Entrench, Card::FlameBarrier, Card::GhostlyArmor,
        Card::PowerThrough, Card::RageCard,
        Card::SecondWind, Card::Sentinel, Card::Shockwave,
        Card::SpotWeakness,
        Card::Inflame, Card::Metallicize, Card::CombustCard,
        Card::DarkEmbrace, Card::Evolve, Card::FeelNoPain,
        Card::FireBreathing, Card::Rupture,
    ]
}

fn ironclad_rares() -> Vec<Card> {
    vec![
        Card::Bludgeon, Card::Feed, Card::FiendFire, Card::Immolate,
        Card::DoubleTap, Card::Exhume, Card::LimitBreak,
        Card::Offering, Card::Impervious,
        Card::Barricade, Card::BerserkCard, Card::Corruption,
        Card::DemonForm, Card::Juggernaut,
    ]
}

fn silent_commons() -> Vec<Card> {
    vec![
        Card::PoisonedStab, Card::DaggerThrow, Card::DaggerSpray, Card::SneakyStrike,
        Card::Slice,
        Card::Backflip, Card::DodgeAndRoll, Card::Deflect, Card::CloakAndDagger,
        Card::BladeDance, Card::Prepared, Card::DeadlyPoison, Card::Acrobatics,
        Card::AccuracyCard, Card::AfterImageCard,
    ]
}

fn silent_uncommons() -> Vec<Card> {
    vec![
        Card::Backstab, Card::Bane, Card::Choke, Card::Predator,
        Card::MasterfulStab, Card::Dash, Card::Finisher, Card::Flechettes,
        Card::AllOutAttack, Card::Unload,
        Card::Blur, Card::BouncingFlask, Card::Concentrate, Card::CalculatedGamble,
        Card::Catalyst, Card::CripplingCloud, Card::LegSweep, Card::Outmaneuver,
        Card::PiercingWail, Card::EscapePlan, Card::Expertise, Card::RiddleWithHoles,
        Card::Setup, Card::Terror,
        Card::FootworkCard, Card::NoxiousFumesCard, Card::WellLaidPlansCard,
        Card::DistractionCard, Card::InfiniteBlades,
    ]
}

fn silent_rares() -> Vec<Card> {
    vec![
        Card::DieDieDie, Card::GrandFinale, Card::Skewer,
        Card::Adrenaline, Card::BulletTime, Card::Malaise,
        Card::StormOfSteel, Card::Doppelganger, Card::CorpseExplosionCard,
        Card::AThousandCutsCard, Card::BurstCard, Card::EnvenomCard,
        Card::ToolsOfTheTradeCard, Card::WraithFormCard,
    ]
}

fn defect_commons() -> Vec<Card> {
    vec![
        Card::BallLightning, Card::Barrage, Card::BeamCell, Card::Claw,
        Card::CompileDriver, Card::GoForTheEyes, Card::SweepingBeam,
        Card::ChargeBattery, Card::Chaos, Card::Coolheaded, Card::Leap,
        Card::Recursion, Card::SteamBarrier,
    ]
}

fn defect_uncommons() -> Vec<Card> {
    vec![
        Card::Blizzard, Card::ColdSnap, Card::DoomAndGloom, Card::FTL,
        Card::MelterCard, Card::Scrape, Card::Streamline, Card::Sunder,
        Card::DarknessCard, Card::DoubleEnergy, Card::Equilibrium, Card::ForceField,
        Card::Glacier, Card::Hologram, Card::Overclock, Card::RecycleCard,
        Card::Reprogram, Card::StackCard, Card::TURBO, Card::ReinforcedBody,
        Card::CapacitorCard, Card::ConsumeCard, Card::FusionCard, Card::HeatsinkCard,
        Card::LoopCard, Card::MachineLearningCard, Card::StormCard,
    ]
}

fn defect_rares() -> Vec<Card> {
    vec![
        Card::AllForOne, Card::CoreSurge, Card::Hyperbeam, Card::MeteorStrike,
        Card::ThunderStrike,
        Card::AmplifyCard, Card::Fission, Card::MultiCast, Card::RainbowCard,
        Card::SeekCard, Card::SkimCard, Card::TempestCard,
        Card::BufferCard, Card::DefragmentCard, Card::EchoFormCard,
        Card::ElectrodynamicsCard, Card::StaticDischargeCard,
    ]
}

fn watcher_commons() -> Vec<Card> {
    vec![
        Card::FlurryOfBlows, Card::EmptyFist, Card::Consecrate,
        Card::CutThroughFate, Card::JustLucky,
        Card::EmptyBody, Card::Protect, Card::Halt, Card::ThirdEye,
        Card::Tranquility, Card::Crescendo, Card::Collect,
    ]
}

fn watcher_uncommons() -> Vec<Card> {
    vec![
        Card::CrushJoints, Card::FearNoEvil, Card::ForeignInfluence,
        Card::SashWhip, Card::Tantrum, Card::CarveReality,
        Card::SandsOfTime, Card::WindmillStrike, Card::Wallop,
        Card::Weave, Card::SignatureMove, Card::FlyingSleeves,
        Card::Conclude, Card::ReachHeaven,
        Card::EmptyMind, Card::MeditateCard, Card::InnerPeace,
        Card::Indignation, Card::Swivel, Card::Perseverance,
        Card::Pray, Card::Prostrate, Card::WreathOfFlameCard,
        Card::BattleHymnCard, Card::SimmeringFuryCard,
        Card::MentalFortressCard, Card::NirvanaCard, Card::LikeWaterCard,
        Card::ForesightCard, Card::StudyCard, Card::RushdownCard,
    ]
}

fn watcher_rares() -> Vec<Card> {
    vec![
        Card::Ragnarok, Card::BrillianceCard,
        Card::Blasphemy, Card::DeusExMachina, Card::OmniscienceCard,
        Card::ScrawlCard, Card::VaultCard, Card::WishCard,
        Card::SpiritShieldCard, Card::JudgmentCard, Card::WorshipCard,
        Card::OmegaCard, Card::DevaFormCard, Card::DevotionCard,
        Card::EstablishmentCard, Card::ConjureBladeCard,
    ]
}

/// The reward deck for Ironclad: 2x each common, 1x each uncommon, 2 golden tickets.
/// Golden tickets represent rare pulls when drawn.
#[pyclass]
#[derive(Clone, Debug)]
pub struct RewardDeck {
    cards: Vec<(Card, CardRarity)>,
    rare_pool: Vec<Card>,
    rng: StdRng,
}

#[pymethods]
impl RewardDeck {
    #[new]
    #[pyo3(signature = (seed=None, character=None))]
    pub fn new(seed: Option<u64>, character: Option<Character>) -> Self {
        let s = seed.unwrap_or(0);
        let mut rng = StdRng::seed_from_u64(s);
        let ch = character.unwrap_or(Character::Ironclad);

        let (commons_fn, uncommons_fn, rares_fn) = match ch {
            Character::Ironclad => (ironclad_commons as fn() -> Vec<Card>, ironclad_uncommons as fn() -> Vec<Card>, ironclad_rares as fn() -> Vec<Card>),
            Character::Silent => (silent_commons as fn() -> Vec<Card>, silent_uncommons as fn() -> Vec<Card>, silent_rares as fn() -> Vec<Card>),
            Character::Defect => (defect_commons as fn() -> Vec<Card>, defect_uncommons as fn() -> Vec<Card>, defect_rares as fn() -> Vec<Card>),
            Character::Watcher => (watcher_commons as fn() -> Vec<Card>, watcher_uncommons as fn() -> Vec<Card>, watcher_rares as fn() -> Vec<Card>),
        };

        let mut cards: Vec<(Card, CardRarity)> = Vec::new();

        // 2x each common
        for card in commons_fn() {
            cards.push((card, CardRarity::Common));
            cards.push((card, CardRarity::Common));
        }

        // 1x each uncommon
        for card in uncommons_fn() {
            cards.push((card, CardRarity::Uncommon));
        }

        // Shuffle the deck
        cards.shuffle(&mut rng);

        let rare_pool = rares_fn();

        RewardDeck {
            cards,
            rare_pool,
            rng,
        }
    }

    /// Draw 3 card rewards. Returns list of CardInstance.
    /// Golden ticket draws pull from the rare pool instead.
    #[pyo3(signature = (count=3))]
    pub fn draw_rewards(&mut self, count: i32) -> Vec<CardInstance> {
        let mut result = Vec::new();
        let mut golden_ticket_counter = 0;

        for _ in 0..count {
            if self.cards.is_empty() {
                // Reshuffle if deck is empty
                self.reshuffle();
            }
            if let Some((card, rarity)) = self.cards.pop() {
                // Every ~15-20 cards, one is a "golden ticket" (rare)
                // We use a counter: every 15th draw is a golden ticket
                golden_ticket_counter += 1;
                if golden_ticket_counter >= 15 {
                    golden_ticket_counter = 0;
                    // Pull a rare instead
                    if let Some(&rare) = self.rare_pool.choose(&mut self.rng) {
                        result.push(CardInstance::new(rare, false));
                        continue;
                    }
                }
                result.push(CardInstance::new(card, false));
            }
        }
        result
    }

    /// Get the number of cards remaining in the reward deck.
    pub fn remaining(&self) -> usize {
        self.cards.len()
    }
}

impl RewardDeck {
    fn reshuffle(&mut self) {
        let mut cards: Vec<(Card, CardRarity)> = Vec::new();
        for card in ironclad_commons() {
            cards.push((card, CardRarity::Common));
            cards.push((card, CardRarity::Common));
        }
        for card in ironclad_uncommons() {
            cards.push((card, CardRarity::Uncommon));
        }
        cards.shuffle(&mut self.rng);
        self.cards = cards;
    }
}

/// Card prices for the shop.
pub fn card_price(rarity: CardRarity) -> i32 {
    match rarity {
        CardRarity::Common => 2,
        CardRarity::Uncommon => 3,
        CardRarity::Rare => 6,
    }
}

/// Get the rarity of a card.
pub fn get_card_rarity(card: Card) -> CardRarity {
    let commons = ironclad_commons();
    if commons.contains(&card) {
        return CardRarity::Common;
    }
    let uncommons = ironclad_uncommons();
    if uncommons.contains(&card) {
        return CardRarity::Uncommon;
    }
    CardRarity::Rare
}
