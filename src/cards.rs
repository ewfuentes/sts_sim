use pyo3::prelude::*;

use crate::enums::{CardType, Character};

/// Card identity — which card this is. Stats are determined by the Card + upgraded flag
/// via CardInstance.
#[pyclass(frozen, eq, eq_int, hash)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum Card {
    // Ironclad Starter
    StrikeRed,
    DefendRed,
    Bash,

    // Silent Starter
    StrikeGreen,
    DefendGreen,
    Neutralize,
    Survivor,

    // Defect Starter
    StrikeBlue,
    DefendBlue,
    Zap,
    Dualcast,

    // Watcher Starter
    StrikePurple,
    DefendPurple,
    Eruption,
    Vigilance,

    // --- Silent Common Attacks ---
    PoisonedStab,
    DaggerThrow,
    DaggerSpray,
    SneakyStrike,
    Slice,
    // --- Silent Common Skills ---
    Backflip,
    DodgeAndRoll,
    Deflect,
    CloakAndDagger,
    BladeDance,
    Prepared,
    DeadlyPoison,
    Acrobatics,
    // --- Silent Common Powers ---
    AccuracyCard,
    AfterImageCard,
    // --- Silent Uncommon Attacks ---
    Backstab,
    Bane,
    Choke,
    Predator,
    MasterfulStab,
    Dash,
    Finisher,
    Flechettes,
    AllOutAttack,
    Unload,
    // --- Silent Uncommon Skills ---
    Blur,
    BouncingFlask,
    Concentrate,
    CalculatedGamble,
    Catalyst,
    CripplingCloud,
    LegSweep,
    Outmaneuver,
    PiercingWail,
    EscapePlan,
    Expertise,
    RiddleWithHoles,
    Setup,
    Terror,
    // --- Silent Uncommon Powers ---
    FootworkCard,
    NoxiousFumesCard,
    WellLaidPlansCard,
    DistractionCard,
    InfiniteBlades,
    // --- Silent Rare Attacks ---
    DieDieDie,
    GrandFinale,
    Skewer,
    // --- Silent Rare Skills ---
    Adrenaline,
    BulletTime,
    Malaise,
    StormOfSteel,
    Doppelganger,
    CorpseExplosionCard,
    // --- Silent Rare Powers ---
    AThousandCutsCard,
    BurstCard,
    EnvenomCard,
    ToolsOfTheTradeCard,
    WraithFormCard,
    // --- Silent Unplayable ---
    Reflex,
    Tactician,

    // --- Defect Common Attacks ---
    BallLightning,
    Barrage,
    BeamCell,
    Claw,
    CompileDriver,
    GoForTheEyes,
    SweepingBeam,
    // --- Defect Common Skills ---
    ChargeBattery,
    Chaos,
    Coolheaded,
    Leap,
    Recursion,
    // Skim already referenced below if needed
    SteamBarrier,
    // --- Defect Uncommon Attacks ---
    Blizzard,
    ColdSnap,
    DoomAndGloom,
    FTL,
    MelterCard,
    Scrape,
    Streamline,
    Sunder,
    // --- Defect Uncommon Skills ---
    DarknessCard,
    DoubleEnergy,
    Equilibrium,
    ForceField,
    Glacier,
    Hologram,
    Overclock,
    RecycleCard,
    Reprogram,
    StackCard,
    TURBO,
    ReinforcedBody,
    // --- Defect Uncommon Powers ---
    CapacitorCard,
    ConsumeCard,
    FusionCard,
    HeatsinkCard,
    LoopCard,
    MachineLearningCard,
    StormCard,
    // --- Defect Rare Attacks ---
    AllForOne,
    CoreSurge,
    Hyperbeam,
    MeteorStrike,
    ThunderStrike,
    // --- Defect Rare Skills ---
    AmplifyCard,
    Fission,
    MultiCast,
    RainbowCard,
    SeekCard,
    SkimCard,
    TempestCard,
    // --- Defect Rare Powers ---
    BufferCard,
    DefragmentCard,
    EchoFormCard,
    ElectrodynamicsCard,
    StaticDischargeCard,

    // --- Watcher Common Attacks ---
    FlurryOfBlows,
    EmptyFist,
    Consecrate,
    CutThroughFate,
    JustLucky,
    // --- Watcher Common Skills ---
    EmptyBody,
    Protect,
    Halt,
    ThirdEye,
    Tranquility,
    Crescendo,
    Collect,
    // --- Watcher Uncommon Attacks ---
    CrushJoints,
    FearNoEvil,
    ForeignInfluence,
    SashWhip,
    Tantrum,
    CarveReality,
    SandsOfTime,
    WindmillStrike,
    Wallop,
    Weave,
    SignatureMove,
    FlyingSleeves,
    Conclude,
    ReachHeaven,
    // --- Watcher Uncommon Skills ---
    EmptyMind,
    MeditateCard,
    InnerPeace,
    Indignation,
    Swivel,
    Perseverance,
    Pray,
    Prostrate,
    WreathOfFlameCard,
    // --- Watcher Uncommon Powers ---
    BattleHymnCard,
    SimmeringFuryCard,
    MentalFortressCard,
    NirvanaCard,
    LikeWaterCard,
    ForesightCard,
    StudyCard,
    RushdownCard,
    // --- Watcher Rare Attacks ---
    Ragnarok,
    BrillianceCard,
    // --- Watcher Rare Skills ---
    Blasphemy,
    DeusExMachina,
    OmniscienceCard,
    ScrawlCard,
    VaultCard,
    WishCard,
    SpiritShieldCard,
    JudgmentCard,
    WorshipCard,
    // --- Watcher Rare Powers ---
    OmegaCard,
    DevaFormCard,
    DevotionCard,
    EstablishmentCard,
    ConjureBladeCard,

    // --- Ironclad Common Attacks ---
    Anger,
    BodySlam,
    Clash,
    Cleave,
    Clothesline,
    HeavyBlade,
    IronWave,
    PerfectedStrike,
    PommelStrike,
    TwinStrike,
    WildStrike,

    // --- Common Skills ---
    Flex,
    Havoc,
    SeeingRed,
    ShrugItOff,
    TrueGrit,
    Warcry,

    // --- Uncommon Attacks ---
    BloodForBlood,
    Carnage,
    Headbutt,
    Rampage,
    SeverSoul,
    Uppercut,
    Whirlwind,

    // --- Uncommon Skills ---
    BattleTrance,
    BurningPact,
    Disarm,
    Entrench,
    FlameBarrier,
    GhostlyArmor,
    PowerThrough,
    RageCard,     // Skill that applies Rage power
    SecondWind,
    Sentinel,
    Shockwave,
    SpotWeakness,

    // --- Uncommon Powers ---
    Inflame,
    Metallicize,
    CombustCard,  // Power that applies Combust
    DarkEmbrace,
    Evolve,
    FeelNoPain,
    FireBreathing,
    Rupture,

    // --- Rare Attacks ---
    Bludgeon,
    Feed,
    FiendFire,
    Immolate,

    // --- Rare Skills ---
    DoubleTap,
    Exhume,
    LimitBreak,
    Offering,
    Impervious,

    // --- Rare Powers ---
    Barricade,
    BerserkCard,
    Corruption,
    DemonForm,
    Juggernaut,

    // --- Status cards ---
    Dazed,
    Burn,
    Wound,
    Slimed,
    VoidCard,

    // --- Curses ---
    AscendersBane,
    Injury,
    Pain,
    Decay,
}

/// A card instance in a deck — wraps a Card identity with its upgraded state.
#[pyclass]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct CardInstance {
    #[pyo3(get)]
    pub card: Card,
    #[pyo3(get)]
    pub upgraded: bool,
}

#[pymethods]
impl CardInstance {
    #[new]
    #[pyo3(signature = (card, upgraded=false))]
    pub fn new(card: Card, upgraded: bool) -> Self {
        CardInstance { card, upgraded }
    }

    #[getter]
    fn py_cost(&self) -> i32 {
        self.cost()
    }

    #[getter]
    fn py_card_type(&self) -> CardType {
        self.card.card_type()
    }

    #[getter]
    fn py_base_damage(&self) -> i32 {
        self.base_damage()
    }

    #[getter]
    fn py_base_block(&self) -> i32 {
        self.base_block()
    }

    #[getter]
    fn py_base_magic(&self) -> i32 {
        self.base_magic()
    }

    #[getter]
    fn py_has_target(&self) -> bool {
        self.card.has_target()
    }

    #[getter]
    fn py_name(&self) -> String {
        let base = self.card.name();
        if self.upgraded {
            format!("{}+", base)
        } else {
            base.to_string()
        }
    }

    #[getter]
    fn py_exhausts(&self) -> bool {
        self.exhausts()
    }

    #[getter]
    fn py_ethereal(&self) -> bool {
        // Some cards lose ethereal when upgraded
        if self.upgraded {
            match self.card {
                Card::DefragmentCard | Card::EchoFormCard | Card::JudgmentCard => return false,
                _ => {}
            }
        }
        self.card.ethereal()
    }

    #[getter]
    fn py_unplayable(&self) -> bool {
        self.card.unplayable()
    }

    #[getter]
    fn py_innate(&self) -> bool {
        self.innate()
    }

    #[getter]
    fn py_retain(&self) -> bool {
        self.card.retain()
    }

    pub fn upgrade(&mut self) -> bool {
        if self.upgraded || self.card.card_type() == CardType::Status || self.card.card_type() == CardType::Curse {
            return false;
        }
        self.upgraded = true;
        true
    }
}

impl CardInstance {
    pub fn cost(&self) -> i32 {
        match (self.card, self.upgraded) {
            // Starter - Ironclad
            (Card::StrikeRed, _) => 1,
            (Card::DefendRed, _) => 1,
            (Card::Bash, _) => 2,
            // Starter - Silent
            (Card::StrikeGreen, _) => 1,
            (Card::DefendGreen, _) => 1,
            (Card::Neutralize, _) => 0,
            (Card::Survivor, _) => 1,
            // Starter - Defect
            (Card::StrikeBlue, false) => 1,
            (Card::StrikeBlue, true) => 0,
            (Card::DefendBlue, _) => 1,
            (Card::Zap, false) => 1,
            (Card::Zap, true) => 0,
            (Card::Dualcast, false) => 1,
            (Card::Dualcast, true) => 0,
            // Starter - Watcher
            (Card::StrikePurple, _) => 1,
            (Card::DefendPurple, _) => 1,
            (Card::Eruption, false) => 2,
            (Card::Eruption, true) => 1,
            (Card::Vigilance, _) => 2,
            // Watcher Common Attacks
            (Card::FlurryOfBlows, _) => 0,
            (Card::EmptyFist, _) => 1,
            (Card::Consecrate, _) => 0,
            (Card::CutThroughFate, _) => 1,
            (Card::JustLucky, _) => 0,
            // Watcher Common Skills
            (Card::EmptyBody, _) => 1,
            (Card::Protect, _) => 2,
            (Card::Halt, _) => 0,
            (Card::ThirdEye, _) => 1,
            (Card::Tranquility, false) => 1,
            (Card::Tranquility, true) => 0,
            (Card::Crescendo, _) => 0,
            (Card::Collect, _) => 1,
            // Watcher Uncommon Attacks
            (Card::CrushJoints, _) => 1,
            (Card::FearNoEvil, _) => 1,
            (Card::ForeignInfluence, _) => 2,
            (Card::SashWhip, _) => 1,
            (Card::Tantrum, _) => 1,
            (Card::CarveReality, _) => 2,
            (Card::SandsOfTime, _) => 2,
            (Card::WindmillStrike, _) => 2,
            (Card::Wallop, _) => 2,
            (Card::Weave, _) => 0,
            (Card::SignatureMove, _) => 2,
            (Card::FlyingSleeves, _) => 1,
            (Card::Conclude, _) => 1,
            (Card::ReachHeaven, _) => 1,
            // Watcher Uncommon Skills
            (Card::EmptyMind, _) => 1,
            (Card::MeditateCard, _) => 1,
            (Card::InnerPeace, _) => 1,
            (Card::Indignation, _) => 1,
            (Card::Swivel, _) => 2,
            (Card::Perseverance, _) => 1,
            (Card::Pray, _) => 1,
            (Card::Prostrate, _) => 1,
            (Card::WreathOfFlameCard, _) => -1,  // X-cost
            // Watcher Uncommon Powers
            (Card::BattleHymnCard, _) => 1,
            (Card::SimmeringFuryCard, _) => 2,
            (Card::MentalFortressCard, _) => 1,
            (Card::NirvanaCard, _) => 1,
            (Card::LikeWaterCard, _) => 1,
            (Card::ForesightCard, _) => 1,
            (Card::StudyCard, false) => 2,
            (Card::StudyCard, true) => 1,
            (Card::RushdownCard, _) => 1,
            // Watcher Rare Attacks
            (Card::Ragnarok, _) => 3,
            (Card::BrillianceCard, _) => 1,
            // Watcher Rare Skills
            (Card::Blasphemy, _) => 2,
            (Card::DeusExMachina, _) => 0,
            (Card::OmniscienceCard, false) => 3,
            (Card::OmniscienceCard, true) => 2,
            (Card::ScrawlCard, false) => 1,
            (Card::ScrawlCard, true) => 0,
            (Card::VaultCard, false) => 3,
            (Card::VaultCard, true) => 2,
            (Card::WishCard, _) => 3,
            (Card::SpiritShieldCard, _) => 2,
            (Card::JudgmentCard, _) => 1,
            (Card::WorshipCard, _) => -1,  // X-cost
            // Watcher Rare Powers
            (Card::OmegaCard, _) => 3,
            (Card::DevaFormCard, _) => 2,
            (Card::DevotionCard, _) => 1,
            (Card::EstablishmentCard, _) => 1,
            (Card::ConjureBladeCard, _) => -1,  // X-cost
            // Silent Common Attacks
            (Card::PoisonedStab, _) => 1,
            (Card::DaggerThrow, _) => 1,
            (Card::DaggerSpray, _) => 1,
            (Card::SneakyStrike, _) => 2,
            (Card::Slice, _) => 0,
            // Silent Common Skills
            (Card::Backflip, _) => 1,
            (Card::DodgeAndRoll, _) => 1,
            (Card::Deflect, _) => 0,
            (Card::CloakAndDagger, _) => 1,
            (Card::BladeDance, _) => 1,
            (Card::Prepared, _) => 0,
            (Card::DeadlyPoison, false) => 1,
            (Card::DeadlyPoison, true) => 0,
            (Card::Acrobatics, _) => 1,
            // Silent Common Powers
            (Card::AccuracyCard, false) => 1,
            (Card::AccuracyCard, true) => 0,
            (Card::AfterImageCard, false) => 1,
            (Card::AfterImageCard, true) => 0,
            // Silent Uncommon Attacks
            (Card::Backstab, _) => 0,
            (Card::Bane, _) => 1,
            (Card::Choke, _) => 2,
            (Card::Predator, _) => 2,
            (Card::MasterfulStab, _) => 0,
            (Card::Dash, _) => 2,
            (Card::Finisher, _) => 1,
            (Card::Flechettes, _) => 1,
            (Card::AllOutAttack, _) => 1,
            (Card::Unload, _) => 1,
            // Silent Uncommon Skills
            (Card::Blur, _) => 1,
            (Card::BouncingFlask, _) => 2,
            (Card::Concentrate, _) => 0,
            (Card::CalculatedGamble, _) => 0,
            (Card::Catalyst, _) => 1,
            (Card::CripplingCloud, _) => 2,
            (Card::LegSweep, _) => 2,
            (Card::Outmaneuver, _) => 0,
            (Card::PiercingWail, _) => 1,
            (Card::EscapePlan, _) => 0,
            (Card::Expertise, _) => 1,
            (Card::RiddleWithHoles, _) => 2,
            (Card::Setup, _) => 0,
            (Card::Terror, _) => 1,
            // Silent Uncommon Powers
            (Card::FootworkCard, _) => 2,
            (Card::NoxiousFumesCard, _) => 1,
            (Card::WellLaidPlansCard, _) => 1,
            (Card::DistractionCard, false) => 2,
            (Card::DistractionCard, true) => 1,
            (Card::InfiniteBlades, _) => 1,
            // Silent Rare Attacks
            (Card::DieDieDie, _) => 1,
            (Card::GrandFinale, _) => 0,
            (Card::Skewer, _) => -1,  // X-cost
            // Silent Rare Skills
            (Card::Adrenaline, _) => 0,
            (Card::BulletTime, false) => 3,
            (Card::BulletTime, true) => 2,
            (Card::Malaise, _) => -1,  // X-cost
            (Card::StormOfSteel, _) => 1,
            (Card::Doppelganger, _) => -1,  // X-cost
            (Card::CorpseExplosionCard, _) => 2,
            // Silent Rare Powers
            (Card::AThousandCutsCard, _) => 2,
            (Card::BurstCard, false) => 1,
            (Card::BurstCard, true) => 0,
            (Card::EnvenomCard, false) => 3,
            (Card::EnvenomCard, true) => 2,
            (Card::ToolsOfTheTradeCard, false) => 1,
            (Card::ToolsOfTheTradeCard, true) => 0,
            (Card::WraithFormCard, _) => 3,
            // Silent Unplayable
            (Card::Reflex, _) => -2,
            (Card::Tactician, _) => -2,
            // Defect Common Attacks
            (Card::BallLightning, _) => 1,
            (Card::Barrage, _) => 1,
            (Card::BeamCell, _) => 1,
            (Card::Claw, _) => 0,
            (Card::CompileDriver, _) => 1,
            (Card::GoForTheEyes, _) => 0,
            (Card::SweepingBeam, _) => 1,
            // Defect Common Skills
            (Card::ChargeBattery, _) => 1,
            (Card::Chaos, false) => 1,
            (Card::Chaos, true) => 0,
            (Card::Coolheaded, _) => 1,
            (Card::Leap, _) => 1,
            (Card::Recursion, false) => 1,
            (Card::Recursion, true) => 0,
            (Card::SteamBarrier, _) => 0,
            // Defect Uncommon Attacks
            (Card::Blizzard, _) => 1,
            (Card::ColdSnap, _) => 2,
            (Card::DoomAndGloom, _) => 2,
            (Card::FTL, _) => 0,
            (Card::MelterCard, _) => 1,
            (Card::Scrape, _) => 1,
            (Card::Streamline, _) => 2,
            (Card::Sunder, _) => 3,
            // Defect Uncommon Skills
            (Card::DarknessCard, false) => 1,
            (Card::DarknessCard, true) => 0,
            (Card::DoubleEnergy, false) => 1,
            (Card::DoubleEnergy, true) => 0,
            (Card::Equilibrium, _) => 2,
            (Card::ForceField, _) => 3,
            (Card::Glacier, _) => 2,
            (Card::Hologram, _) => 1,
            (Card::Overclock, _) => 0,
            (Card::RecycleCard, false) => 1,
            (Card::RecycleCard, true) => 0,
            (Card::Reprogram, false) => 1,
            (Card::Reprogram, true) => 0,
            (Card::StackCard, _) => 1,
            (Card::TURBO, _) => 0,
            (Card::ReinforcedBody, _) => -1,  // X-cost
            // Defect Uncommon Powers
            (Card::CapacitorCard, _) => 1,
            (Card::ConsumeCard, false) => 2,
            (Card::ConsumeCard, true) => 1,
            (Card::FusionCard, false) => 2,
            (Card::FusionCard, true) => 1,
            (Card::HeatsinkCard, _) => 1,
            (Card::LoopCard, _) => 1,
            (Card::MachineLearningCard, false) => 1,
            (Card::MachineLearningCard, true) => 0,
            (Card::StormCard, _) => 1,
            // Defect Rare Attacks
            (Card::AllForOne, _) => 2,
            (Card::CoreSurge, _) => 1,
            (Card::Hyperbeam, _) => 2,
            (Card::MeteorStrike, _) => 5,
            (Card::ThunderStrike, _) => 3,
            // Defect Rare Skills
            (Card::AmplifyCard, _) => 1,
            (Card::Fission, _) => 0,
            (Card::MultiCast, _) => -1,  // X-cost
            (Card::RainbowCard, _) => 2,
            (Card::SeekCard, _) => 0,
            (Card::SkimCard, _) => 1,
            (Card::TempestCard, _) => -1,  // X-cost
            // Defect Rare Powers
            (Card::BufferCard, _) => 2,
            (Card::DefragmentCard, _) => 3,
            (Card::EchoFormCard, _) => 3,
            (Card::ElectrodynamicsCard, _) => 2,
            (Card::StaticDischargeCard, _) => 2,
            // Ironclad Common Attacks
            (Card::Anger, _) => 0,
            (Card::BodySlam, false) => 1,
            (Card::BodySlam, true) => 0,
            (Card::Clash, _) => 0,
            (Card::Cleave, _) => 1,
            (Card::Clothesline, _) => 2,
            (Card::HeavyBlade, _) => 2,
            (Card::IronWave, _) => 1,
            (Card::PerfectedStrike, _) => 2,
            (Card::PommelStrike, _) => 1,
            (Card::TwinStrike, _) => 1,
            (Card::WildStrike, _) => 1,
            // Common Skills
            (Card::Flex, _) => 0,
            (Card::Havoc, false) => 1,
            (Card::Havoc, true) => 0,
            (Card::SeeingRed, false) => 1,
            (Card::SeeingRed, true) => 0,
            (Card::ShrugItOff, _) => 1,
            (Card::TrueGrit, _) => 1,
            (Card::Warcry, _) => 0,
            // Uncommon Attacks
            (Card::BloodForBlood, _) => 3,  // BG mod: upgrade changes magic number, not cost
            (Card::Carnage, _) => 2,
            (Card::Headbutt, _) => 1,
            (Card::Rampage, _) => 1,
            (Card::SeverSoul, _) => 2,
            (Card::Uppercut, _) => 2,
            (Card::Whirlwind, _) => -1,  // X-cost
            // Uncommon Skills
            (Card::BattleTrance, _) => 0,
            (Card::BurningPact, _) => 1,
            (Card::Disarm, _) => 1,
            (Card::Entrench, _) => 1,
            (Card::FlameBarrier, _) => 2,
            (Card::GhostlyArmor, _) => 1,
            (Card::PowerThrough, _) => 1,
            (Card::RageCard, false) => 1,
            (Card::RageCard, true) => 0,
            (Card::SecondWind, _) => 1,
            (Card::Sentinel, _) => 1,
            (Card::Shockwave, _) => 2,
            (Card::SpotWeakness, _) => 1,
            // Uncommon Powers
            (Card::Inflame, false) => 2,
            (Card::Inflame, true) => 1,
            (Card::Metallicize, false) => 1,
            (Card::Metallicize, true) => 0,
            (Card::CombustCard, _) => 1,
            (Card::DarkEmbrace, false) => 2,
            (Card::DarkEmbrace, true) => 1,
            (Card::Evolve, false) => 1,
            (Card::Evolve, true) => 0,
            (Card::FeelNoPain, false) => 1,
            (Card::FeelNoPain, true) => 0,
            (Card::FireBreathing, _) => 1,
            (Card::Rupture, false) => 1,
            (Card::Rupture, true) => 0,
            // Rare Attacks
            (Card::Bludgeon, _) => 3,
            (Card::Feed, _) => 1,
            (Card::FiendFire, _) => 2,
            (Card::Immolate, _) => 2,
            // Rare Skills
            (Card::DoubleTap, false) => 1,
            (Card::DoubleTap, true) => 0,
            (Card::Exhume, false) => 1,
            (Card::Exhume, true) => 0,
            (Card::LimitBreak, _) => 1,
            (Card::Offering, _) => 0,
            (Card::Impervious, _) => 2,
            // Rare Powers
            (Card::Barricade, false) => 2,
            (Card::Barricade, true) => 1,
            (Card::BerserkCard, _) => 1,
            (Card::Corruption, false) => 3,
            (Card::Corruption, true) => 2,
            (Card::DemonForm, false) => 3,
            (Card::DemonForm, true) => 2,
            (Card::Juggernaut, _) => 2,
            // Status cards
            (Card::Dazed, _) => -2,
            (Card::Burn, _) => -2,
            (Card::Wound, _) => -2,
            (Card::Slimed, _) => 1,
            (Card::VoidCard, _) => -2,
            // Curses
            (Card::AscendersBane, _) => -2,
            (Card::Injury, _) => -2,
            (Card::Pain, _) => -2,
            (Card::Decay, _) => -2,
        }
    }

    pub fn base_damage(&self) -> i32 {
        match (self.card, self.upgraded) {
            (Card::StrikeRed, false) => 1,
            (Card::StrikeRed, true) => 2,
            (Card::Bash, false) => 2,
            (Card::Bash, true) => 4,
            // Silent starter
            (Card::StrikeGreen, false) => 1,
            (Card::StrikeGreen, true) => 2,
            (Card::Neutralize, false) => 1,
            (Card::Neutralize, true) => 2,
            // Defect starter
            (Card::StrikeBlue, _) => 1,  // BG mod: upgrade reduces cost, not increases damage
            // Watcher starter
            (Card::StrikePurple, false) => 1,
            (Card::StrikePurple, true) => 2,
            (Card::Eruption, _) => 2,  // upgrade only reduces cost
            // Watcher common attacks
            (Card::FlurryOfBlows, _) => 1,
            (Card::EmptyFist, false) => 2,
            (Card::EmptyFist, true) => 3,
            (Card::Consecrate, false) => 1,
            (Card::Consecrate, true) => 2,
            (Card::CutThroughFate, false) => 1,
            (Card::CutThroughFate, true) => 2,
            (Card::JustLucky, false) => 1,
            (Card::JustLucky, true) => 2,
            // Watcher uncommon attacks
            (Card::CrushJoints, false) => 1,
            (Card::CrushJoints, true) => 2,
            (Card::FearNoEvil, false) => 2,
            (Card::FearNoEvil, true) => 3,
            (Card::ForeignInfluence, false) => 3,
            (Card::ForeignInfluence, true) => 4,
            (Card::SashWhip, _) => 2,  // BG mod: upgrade increases vuln, not damage
            (Card::Tantrum, false) => 2,
            (Card::Tantrum, true) => 1,
            (Card::CarveReality, false) => 3,
            (Card::CarveReality, true) => 4,
            (Card::SandsOfTime, _) => 3,
            (Card::WindmillStrike, _) => 2,
            (Card::Wallop, false) => 2,
            (Card::Wallop, true) => 3,
            (Card::Weave, false) => 1,
            (Card::Weave, true) => 2,
            (Card::SignatureMove, false) => 6,
            (Card::SignatureMove, true) => 8,
            (Card::FlyingSleeves, _) => 1,
            (Card::Conclude, _) => 1,
            (Card::ReachHeaven, _) => 2,
            // Watcher rare attacks
            (Card::Ragnarok, _) => 1,
            (Card::BrillianceCard, false) => 2,
            (Card::BrillianceCard, true) => 3,
            // Silent attacks
            (Card::PoisonedStab, _) => 1,
            (Card::DaggerThrow, false) => 2,
            (Card::DaggerThrow, true) => 3,
            (Card::DaggerSpray, _) => 1,
            (Card::SneakyStrike, false) => 3,
            (Card::SneakyStrike, true) => 4,
            (Card::Slice, false) => 1,
            (Card::Slice, true) => 2,
            (Card::Backstab, false) => 2,
            (Card::Backstab, true) => 4,
            (Card::Bane, false) => 2,
            (Card::Bane, true) => 3,
            (Card::Choke, false) => 3,
            (Card::Choke, true) => 4,
            (Card::Predator, false) => 3,
            (Card::Predator, true) => 4,
            (Card::MasterfulStab, false) => 2,
            (Card::MasterfulStab, true) => 3,
            (Card::Dash, false) => 2,
            (Card::Dash, true) => 3,
            (Card::Finisher, false) => 1,
            (Card::Finisher, true) => 2,
            (Card::Flechettes, _) => 1,
            (Card::AllOutAttack, false) => 2,
            (Card::AllOutAttack, true) => 3,
            (Card::Unload, _) => 2,
            (Card::DieDieDie, false) => 3,
            (Card::DieDieDie, true) => 4,
            (Card::GrandFinale, false) => 10,
            (Card::GrandFinale, true) => 12,
            (Card::Skewer, false) => 1,
            (Card::Skewer, true) => 2,
            // Defect attacks
            (Card::BallLightning, false) => 1,
            (Card::BallLightning, true) => 2,
            (Card::Barrage, _) => 1,
            (Card::BeamCell, _) => 1,  // BG mod: upgrade doesn't increase damage
            (Card::Claw, _) => 1,  // BG mod: upgrade doesn't increase damage
            (Card::CompileDriver, false) => 1,
            (Card::CompileDriver, true) => 2,
            (Card::GoForTheEyes, _) => 1,  // BG mod: upgrade doesn't increase damage
            (Card::SweepingBeam, false) => 1,
            (Card::SweepingBeam, true) => 2,
            (Card::Blizzard, false) => 2,
            (Card::Blizzard, true) => 3,
            (Card::ColdSnap, false) => 2,
            (Card::ColdSnap, true) => 3,
            (Card::DoomAndGloom, false) => 2,
            (Card::DoomAndGloom, true) => 3,
            (Card::FTL, false) => 1,
            (Card::FTL, true) => 2,
            (Card::MelterCard, false) => 2,
            (Card::MelterCard, true) => 3,
            (Card::Scrape, false) => 2,
            (Card::Scrape, true) => 3,
            (Card::Streamline, false) => 3,
            (Card::Streamline, true) => 4,
            (Card::Sunder, false) => 5,
            (Card::Sunder, true) => 7,
            (Card::AllForOne, false) => 2,
            (Card::AllForOne, true) => 3,
            (Card::CoreSurge, false) => 3,
            (Card::CoreSurge, true) => 4,
            (Card::Hyperbeam, false) => 5,
            (Card::Hyperbeam, true) => 7,
            (Card::MeteorStrike, false) => 10,
            (Card::MeteorStrike, true) => 15,
            (Card::ThunderStrike, false) => 4,
            (Card::ThunderStrike, true) => 6,
            // Ironclad Common Attacks
            (Card::Anger, false) => 1,
            (Card::Anger, true) => 2,
            (Card::BodySlam, _) => 0,  // dynamic: equal to block
            (Card::Clash, false) => 3,
            (Card::Clash, true) => 4,
            (Card::Cleave, false) => 2,
            (Card::Cleave, true) => 3,
            (Card::Clothesline, false) => 3,
            (Card::Clothesline, true) => 4,
            (Card::HeavyBlade, _) => 3,
            (Card::IronWave, false) => 1,
            (Card::IronWave, true) => 2,
            (Card::PerfectedStrike, _) => 3,  // +magic per Strike in hand
            (Card::PommelStrike, _) => 2,
            (Card::TwinStrike, false) => 1,  // hits twice
            (Card::TwinStrike, true) => 2,
            (Card::WildStrike, false) => 3,
            (Card::WildStrike, true) => 4,
            // Uncommon Attacks
            (Card::BloodForBlood, _) => 4,
            (Card::Carnage, false) => 4,
            (Card::Carnage, true) => 6,
            (Card::Headbutt, false) => 2,
            (Card::Headbutt, true) => 3,
            (Card::Rampage, _) => 0,  // dynamic: based on exhaust pile
            (Card::SeverSoul, false) => 3,
            (Card::SeverSoul, true) => 4,
            (Card::Uppercut, _) => 3,
            (Card::Whirlwind, _) => 1,  // X times
            // Rare Attacks
            (Card::Bludgeon, false) => 7,
            (Card::Bludgeon, true) => 10,
            (Card::Feed, _) => 3,
            (Card::FiendFire, false) => 1,  // per card in hand
            (Card::FiendFire, true) => 2,
            (Card::Immolate, false) => 5,
            (Card::Immolate, true) => 7,
            _ => 0,
        }
    }

    pub fn base_block(&self) -> i32 {
        match (self.card, self.upgraded) {
            (Card::DefendRed, false) => 1,
            (Card::DefendRed, true) => 2,
            // Silent starter
            (Card::DefendGreen, false) => 1,
            (Card::DefendGreen, true) => 2,
            (Card::Survivor, false) => 2,
            (Card::Survivor, true) => 3,
            // Defect starter
            (Card::DefendBlue, false) => 1,
            (Card::DefendBlue, true) => 2,
            // Watcher starter
            (Card::DefendPurple, false) => 1,
            (Card::DefendPurple, true) => 2,
            (Card::Vigilance, false) => 2,
            (Card::Vigilance, true) => 3,
            // Watcher block cards
            (Card::EmptyBody, false) => 2,
            (Card::EmptyBody, true) => 3,
            (Card::Protect, false) => 3,
            (Card::Protect, true) => 4,
            (Card::Halt, _) => 1,
            (Card::ThirdEye, false) => 2,
            (Card::ThirdEye, true) => 3,
            (Card::JustLucky, _) => 1,
            (Card::Swivel, false) => 2,
            (Card::Swivel, true) => 3,
            (Card::Perseverance, false) => 1,
            (Card::Perseverance, true) => 2,
            (Card::Prostrate, false) => 1,
            (Card::Prostrate, true) => 2,
            (Card::Conclude, _) => 1,
            (Card::SpiritShieldCard, _) => 1,
            (Card::WishCard, false) => 10,
            (Card::WishCard, true) => 15,
            (Card::Wallop, false) => 0,  // gains block equal to unblocked damage
            (Card::Wallop, true) => 0,
            // Silent block cards
            (Card::Backflip, false) => 1,
            (Card::Backflip, true) => 2,
            (Card::DodgeAndRoll, _) => 1,
            (Card::Deflect, false) => 1,
            (Card::Deflect, true) => 2,
            (Card::CloakAndDagger, _) => 1,
            (Card::Blur, false) => 2,
            (Card::Blur, true) => 3,
            (Card::LegSweep, false) => 3,
            (Card::LegSweep, true) => 4,
            (Card::PiercingWail, false) => 1,
            (Card::PiercingWail, true) => 3,
            (Card::EscapePlan, _) => 1,
            (Card::Dash, false) => 2,
            (Card::Dash, true) => 3,
            (Card::IronWave, false) => 1,
            (Card::IronWave, true) => 2,  // BG mod: choice card (Spear: 2dmg/1blk, Shield: 1dmg/2blk)
            // Skills with block
            (Card::ShrugItOff, false) => 2,
            (Card::ShrugItOff, true) => 3,
            (Card::TrueGrit, false) => 1,
            (Card::TrueGrit, true) => 2,
            (Card::FlameBarrier, false) => 3,
            (Card::FlameBarrier, true) => 4,
            (Card::GhostlyArmor, false) => 2,
            (Card::GhostlyArmor, true) => 3,
            (Card::PowerThrough, false) => 3,
            (Card::PowerThrough, true) => 4,
            (Card::RageCard, _) => 1,
            (Card::SecondWind, false) => 1,
            (Card::SecondWind, true) => 2,
            (Card::Sentinel, false) => 2,
            (Card::Sentinel, true) => 3,
            (Card::Impervious, false) => 6,
            (Card::Impervious, true) => 8,
            // Defect block cards
            (Card::ChargeBattery, false) => 2,
            (Card::ChargeBattery, true) => 3,
            (Card::Leap, false) => 2,
            (Card::Leap, true) => 3,
            (Card::SteamBarrier, false) => 1,
            (Card::SteamBarrier, true) => 2,
            (Card::Equilibrium, false) => 3,
            (Card::Equilibrium, true) => 4,
            (Card::ForceField, false) => 3,
            (Card::ForceField, true) => 4,
            (Card::Glacier, false) => 2,
            (Card::Glacier, true) => 3,
            (Card::Hologram, _) => 1,  // BG mod: upgrade removes exhaust, not increases block
            (Card::StackCard, false) => 0,
            (Card::StackCard, true) => 1,
            _ => 0,
        }
    }

    pub fn base_magic(&self) -> i32 {
        match (self.card, self.upgraded) {
            (Card::Bash, _) => 1,  // 1 Vulnerable
            (Card::Neutralize, _) => 1,  // 1 Weak
            // Silent magic numbers
            (Card::PoisonedStab, false) => 1,  // poison
            (Card::PoisonedStab, true) => 2,
            (Card::DaggerSpray, false) => 2,  // hit count
            (Card::DaggerSpray, true) => 3,
            (Card::Backstab, _) => 2,  // bonus if full HP
            (Card::Bane, _) => 2,  // bonus if poisoned
            (Card::Choke, _) => 1,  // bonus per debuff
            (Card::Predator, _) => 2,  // draw count
            (Card::MasterfulStab, false) => 2,  // cost increase
            (Card::MasterfulStab, true) => 1,
            (Card::Finisher, _) => 0,  // per attack played
            (Card::Flechettes, false) => 0,  // bonus per skill in hand
            (Card::Flechettes, true) => 1,
            (Card::Unload, false) => 1,  // discard count
            (Card::Unload, true) => 2,
            (Card::DodgeAndRoll, false) => 2,  // times
            (Card::DodgeAndRoll, true) => 3,
            (Card::Deflect, _) => 1,  // bonus if shiv played
            (Card::CloakAndDagger, false) => 1,  // shiv count
            (Card::CloakAndDagger, true) => 2,
            (Card::BladeDance, false) => 2,  // shiv count
            (Card::BladeDance, true) => 3,
            (Card::Prepared, false) => 1,  // draw+discard count
            (Card::Prepared, true) => 2,
            (Card::DeadlyPoison, _) => 1,  // poison
            (Card::Acrobatics, false) => 3,  // draw count
            (Card::Acrobatics, true) => 4,
            (Card::AccuracyCard, _) => 1,  // shiv damage bonus
            (Card::AfterImageCard, _) => 1,  // block per discard
            (Card::Slice, _) => 1,  // bonus if shivs available
            (Card::AllOutAttack, _) => 0,
            (Card::Blur, _) => 1,  // bonus block on discard
            (Card::BouncingFlask, false) => 2,  // poison
            (Card::BouncingFlask, true) => 3,
            (Card::Catalyst, _) => 0,  // double/triple
            (Card::CripplingCloud, false) => 1,  // poison to all
            (Card::CripplingCloud, true) => 2,
            (Card::LegSweep, _) => 1,  // weak
            (Card::Outmaneuver, false) => 2,  // energy if retained
            (Card::Outmaneuver, true) => 3,
            (Card::PiercingWail, _) => 1,  // weak to all
            (Card::Expertise, false) => 6,
            (Card::Expertise, true) => 7,
            (Card::RiddleWithHoles, false) => 4,  // shiv count
            (Card::RiddleWithHoles, true) => 5,
            (Card::Setup, false) => 1,  // energy
            (Card::Setup, true) => 2,
            (Card::Terror, _) => 1,  // vulnerable
            (Card::FootworkCard, _) => 1,  // dexterity
            (Card::NoxiousFumesCard, _) => 1,  // poison
            (Card::WellLaidPlansCard, false) => 1,  // retain count
            (Card::WellLaidPlansCard, true) => 2,
            (Card::DistractionCard, _) => 2,  // amount
            (Card::InfiniteBlades, false) => 1,  // shiv per turn
            (Card::InfiniteBlades, true) => 2,
            (Card::StormOfSteel, false) => 0,  // bonus
            (Card::StormOfSteel, true) => 1,
            (Card::Concentrate, false) => 0,  // BG: bonus energy on discard
            (Card::Concentrate, true) => 1,
            (Card::Malaise, false) => 0,
            (Card::Malaise, true) => 1,
            (Card::Skewer, false) => 1,
            (Card::Skewer, true) => 0,
            (Card::CorpseExplosionCard, false) => 2,  // poison
            (Card::CorpseExplosionCard, true) => 3,
            (Card::AThousandCutsCard, false) => 5,  // damage on shuffle
            (Card::AThousandCutsCard, true) => 7,
            (Card::BurstCard, _) => 1,
            (Card::EnvenomCard, _) => 1,  // poison on attack
            (Card::WraithFormCard, false) => 2,  // turns
            (Card::WraithFormCard, true) => 3,
            (Card::Reflex, false) => 2,  // draw on discard
            (Card::Reflex, true) => 3,
            (Card::Tactician, false) => 2,  // energy on discard
            (Card::Tactician, true) => 3,
            (Card::Whirlwind, false) => 0,  // extra hits (BG mod: upgrade adds +1)
            (Card::Whirlwind, true) => 1,
            (Card::Burn, _) => 1,  // 1 self-damage at end of turn
            (Card::Clothesline, _) => 1,  // 1 Weak
            (Card::HeavyBlade, false) => 3,  // Str multiplier
            (Card::HeavyBlade, true) => 5,
            (Card::PerfectedStrike, false) => 1,  // +dmg per Strike
            (Card::PerfectedStrike, true) => 2,
            (Card::PommelStrike, false) => 1,  // draw count
            (Card::PommelStrike, true) => 2,
            (Card::Flex, _) => 1,  // temp Str amount
            (Card::Warcry, false) => 2,  // draw count
            (Card::Warcry, true) => 3,
            (Card::BattleTrance, false) => 3,  // draw count
            (Card::BattleTrance, true) => 4,
            (Card::BurningPact, false) => 2,  // draw count
            (Card::BurningPact, true) => 3,
            (Card::Disarm, false) => 2,  // Weak stacks
            (Card::Disarm, true) => 3,
            (Card::Shockwave, false) => 1,  // Vuln+Weak stacks
            (Card::Shockwave, true) => 2,
            (Card::Uppercut, false) => 1,  // Vuln+Weak
            (Card::Uppercut, true) => 2,
            (Card::CombustCard, false) => 1,  // damage per turn
            (Card::CombustCard, true) => 2,
            (Card::FireBreathing, false) => 2,
            (Card::FireBreathing, true) => 3,
            (Card::BerserkCard, false) => 1,
            (Card::BerserkCard, true) => 2,
            (Card::Juggernaut, false) => 1,
            (Card::Juggernaut, true) => 2,
            (Card::Feed, false) => 1,  // max HP gain
            (Card::Feed, true) => 2,
            (Card::Offering, false) => 3,  // draw count
            (Card::Offering, true) => 5,
            // Defect magic numbers
            (Card::BallLightning, _) => 1,  // channel count
            (Card::Barrage, false) => 0,  // hit count bonus
            (Card::Barrage, true) => 1,
            (Card::CompileDriver, _) => 1,  // draw count
            (Card::SweepingBeam, _) => 1,  // draw count
            (Card::ChargeBattery, _) => 1,  // energy if 3+ orbs
            (Card::Overclock, false) => 2,  // draw count
            (Card::Overclock, true) => 3,
            (Card::TURBO, false) => 2,  // energy gain
            (Card::TURBO, true) => 3,
            (Card::SkimCard, false) => 3,  // draw count
            (Card::SkimCard, true) => 4,
            (Card::Equilibrium, false) => 1,  // retain count
            (Card::Equilibrium, true) => 2,
            (Card::CapacitorCard, false) => 2,  // orb slot increase
            (Card::CapacitorCard, true) => 3,
            (Card::ConsumeCard, _) => 1,  // orb evoke power
            (Card::FusionCard, _) => 1,  // energy per turn
            (Card::HeatsinkCard, false) => 2,  // draw on power play
            (Card::HeatsinkCard, true) => 3,
            (Card::LoopCard, false) => 1,  // extra trigger
            (Card::LoopCard, true) => 2,
            (Card::MachineLearningCard, _) => 1,  // draw per turn
            (Card::StormCard, false) => 1,  // lightning per turn
            (Card::StormCard, true) => 2,
            (Card::BufferCard, false) => 1,  // prevent HP loss
            (Card::BufferCard, true) => 2,
            (Card::ElectrodynamicsCard, false) => 2,  // channel lightning
            (Card::ElectrodynamicsCard, true) => 3,
            (Card::StaticDischargeCard, false) => 1,  // lightning passive bonus
            (Card::StaticDischargeCard, true) => 2,
            (Card::AmplifyCard, false) => 3,  // dark evoke bonus
            (Card::AmplifyCard, true) => 5,
            (Card::DefragmentCard, _) => 1,  // orb passive power
            (Card::SeekCard, false) => 1,  // draw from deck
            (Card::SeekCard, true) => 2,
            (Card::ReinforcedBody, false) => 1,  // BG: base adds +1 block
            (Card::ReinforcedBody, true) => 0,   // BG: upgraded no bonus
            (Card::MultiCast, false) => 0,  // X-cost bonus
            (Card::MultiCast, true) => 1,
            (Card::TempestCard, false) => 0,  // X-cost bonus
            (Card::TempestCard, true) => 1,
            (Card::Reprogram, _) => 1,  // +Str
            // Watcher magic numbers
            (Card::FlurryOfBlows, false) => 1,  // bonus if stance changed
            (Card::FlurryOfBlows, true) => 2,
            (Card::CutThroughFate, false) => 2,  // scry count
            (Card::CutThroughFate, true) => 3,
            (Card::JustLucky, false) => 1,  // scry count
            (Card::JustLucky, true) => 2,
            (Card::Halt, false) => 1,  // additional block
            (Card::Halt, true) => 2,
            (Card::ThirdEye, false) => 3,  // scry count
            (Card::ThirdEye, true) => 5,
            (Card::Collect, false) => 2,  // miracles to gain
            (Card::Collect, true) => 3,
            (Card::CrushJoints, _) => 1,  // weak
            (Card::SashWhip, false) => 1,  // vulnerable
            (Card::SashWhip, true) => 2,
            (Card::Tantrum, false) => 1,  // hit count
            (Card::Tantrum, true) => 2,
            (Card::SandsOfTime, false) => 2,  // per retain card
            (Card::SandsOfTime, true) => 3,
            (Card::WindmillStrike, false) => 3,  // bonus if retained
            (Card::WindmillStrike, true) => 5,
            (Card::Weave, false) => 5,  // bonus damage from scry
            (Card::Weave, true) => 6,
            (Card::FlyingSleeves, false) => 2,  // hit count
            (Card::FlyingSleeves, true) => 3,
            (Card::Conclude, false) => 2,  // hit count
            (Card::Conclude, true) => 3,
            (Card::ReachHeaven, false) => 1,  // per miracle bonus
            (Card::ReachHeaven, true) => 2,
            (Card::EmptyMind, false) => 2,  // draw count
            (Card::EmptyMind, true) => 3,
            (Card::MeditateCard, false) => 1,  // scry/draw
            (Card::MeditateCard, true) => 2,
            (Card::InnerPeace, false) => 3,  // draw count
            (Card::InnerPeace, true) => 4,
            (Card::Perseverance, _) => 2,  // bonus block if retained
            (Card::Pray, false) => 1,  // miracles
            (Card::Pray, true) => 2,
            (Card::Ragnarok, false) => 4,  // additional hits
            (Card::Ragnarok, true) => 5,
            (Card::DeusExMachina, false) => 2,  // miracles
            (Card::DeusExMachina, true) => 3,
            (Card::OmniscienceCard, _) => 2,  // scry
            (Card::ScrawlCard, _) => 5,  // draw count
            (Card::JudgmentCard, false) => 7,  // kill threshold
            (Card::JudgmentCard, true) => 8,
            (Card::BattleHymnCard, false) => 1,
            (Card::BattleHymnCard, true) => 2,
            (Card::SimmeringFuryCard, false) => 1,
            (Card::SimmeringFuryCard, true) => 2,
            (Card::MentalFortressCard, false) => 1,
            (Card::MentalFortressCard, true) => 2,
            (Card::NirvanaCard, false) => 1,
            (Card::NirvanaCard, true) => 2,
            (Card::LikeWaterCard, false) => 1,
            (Card::LikeWaterCard, true) => 2,
            (Card::ForesightCard, false) => 3,
            (Card::ForesightCard, true) => 4,
            (Card::StudyCard, _) => 2,
            (Card::RushdownCard, false) => 2,
            (Card::RushdownCard, true) => 3,
            (Card::OmegaCard, false) => 5,
            (Card::OmegaCard, true) => 6,
            (Card::DevaFormCard, false) => 1,
            (Card::DevaFormCard, true) => 2,
            (Card::DevotionCard, false) => 3,
            (Card::DevotionCard, true) => 4,
            (Card::EstablishmentCard, false) => 1,
            (Card::EstablishmentCard, true) => 2,
            (Card::ConjureBladeCard, false) => 1,
            (Card::ConjureBladeCard, true) => 2,
            _ => 0,
        }
    }

    pub fn innate(&self) -> bool {
        // Upgraded Headbutt is innate in BG mod
        false
    }

    /// Whether this card exhausts when played (may depend on upgraded state).
    pub fn exhausts(&self) -> bool {
        match (self.card, self.upgraded) {
            (Card::Slimed, _) => true,
            (Card::AscendersBane, _) => true,
            // Cards that always exhaust
            (Card::SeeingRed, _) => true,
            (Card::Warcry, _) => true,
            (Card::Disarm, _) => true,
            (Card::Shockwave, _) => true,
            (Card::Feed, _) => true,
            (Card::FiendFire, _) => true,
            (Card::Exhume, _) => true,
            (Card::Offering, _) => true,
            (Card::Impervious, _) => true,
            // Silent cards that always exhaust
            (Card::PoisonedStab, _) => true,
            (Card::Backstab, _) => true,
            (Card::Concentrate, _) => true,
            (Card::Catalyst, _) => true,
            (Card::CripplingCloud, _) => true,
            (Card::PiercingWail, _) => true,
            (Card::Setup, _) => true,
            (Card::DieDieDie, _) => true,
            (Card::Adrenaline, _) => true,
            (Card::Malaise, _) => true,
            // Cards that exhaust only when NOT upgraded
            (Card::Flex, false) => true,
            (Card::Entrench, false) => true,
            (Card::LimitBreak, false) => true,
            (Card::CalculatedGamble, false) => true,
            (Card::Terror, false) => true,
            (Card::Doppelganger, false) => true,
            // Defect cards that always exhaust
            (Card::DoubleEnergy, _) => true,
            (Card::TURBO, _) => true,
            (Card::AmplifyCard, _) => true,
            (Card::Fission, _) => true,
            (Card::SeekCard, _) => true,
            (Card::TempestCard, _) => true,
            // Defect cards that exhaust only when NOT upgraded
            (Card::Hologram, false) => true,
            (Card::RainbowCard, false) => true,
            // Watcher cards that always exhaust
            (Card::Tranquility, _) => true,
            (Card::Crescendo, _) => true,
            (Card::Collect, _) => true,
            (Card::DeusExMachina, _) => true,
            (Card::OmniscienceCard, _) => true,
            (Card::ScrawlCard, _) => true,
            (Card::VaultCard, _) => true,
            (Card::WishCard, _) => true,
            (Card::WorshipCard, _) => true,
            // Watcher cards that exhaust only when NOT upgraded
            (Card::Blasphemy, _) => true,  // BG: always exhausts even when upgraded
            (Card::WreathOfFlameCard, false) => true,
            (Card::SpiritShieldCard, false) => true,
            _ => false,
        }
    }
}

impl Card {
    pub fn card_type(&self) -> CardType {
        match self {
            // Attacks
            Card::StrikeRed | Card::StrikeGreen | Card::StrikeBlue | Card::StrikePurple |
            Card::Neutralize | Card::Eruption |
            // Watcher attacks
            Card::FlurryOfBlows | Card::EmptyFist | Card::Consecrate | Card::CutThroughFate |
            Card::JustLucky | Card::CrushJoints | Card::FearNoEvil | Card::ForeignInfluence |
            Card::SashWhip | Card::Tantrum | Card::CarveReality | Card::SandsOfTime |
            Card::WindmillStrike | Card::Wallop | Card::Weave | Card::SignatureMove |
            Card::FlyingSleeves | Card::Conclude | Card::ReachHeaven |
            Card::Ragnarok | Card::BrillianceCard |
            // Silent attacks
            Card::PoisonedStab | Card::DaggerThrow | Card::DaggerSpray | Card::SneakyStrike |
            Card::Slice | Card::Backstab | Card::Bane | Card::Choke | Card::Predator |
            Card::MasterfulStab | Card::Dash | Card::Finisher | Card::Flechettes |
            Card::AllOutAttack | Card::Unload | Card::DieDieDie | Card::GrandFinale |
            Card::Skewer |
            // Defect attacks
            Card::BallLightning | Card::Barrage | Card::BeamCell | Card::Claw |
            Card::CompileDriver | Card::GoForTheEyes | Card::SweepingBeam |
            Card::Blizzard | Card::ColdSnap | Card::DoomAndGloom | Card::FTL |
            Card::MelterCard | Card::Scrape | Card::Streamline | Card::Sunder |
            Card::AllForOne | Card::CoreSurge | Card::Hyperbeam | Card::MeteorStrike |
            Card::ThunderStrike |
            Card::Bash | Card::Anger | Card::BodySlam |
            Card::Clash | Card::Cleave | Card::Clothesline | Card::HeavyBlade |
            Card::IronWave | Card::PerfectedStrike | Card::PommelStrike |
            Card::TwinStrike | Card::WildStrike |
            Card::BloodForBlood | Card::Carnage | Card::Headbutt |
            Card::Rampage | Card::SeverSoul | Card::Uppercut | Card::Whirlwind |
            Card::Bludgeon | Card::Feed | Card::FiendFire | Card::Immolate => CardType::Attack,

            // Skills
            Card::DefendRed | Card::DefendGreen | Card::DefendBlue | Card::DefendPurple |
            Card::Survivor | Card::Zap | Card::Dualcast | Card::Vigilance |
            // Watcher skills
            Card::EmptyBody | Card::Protect | Card::Halt | Card::ThirdEye |
            Card::Tranquility | Card::Crescendo | Card::Collect |
            Card::EmptyMind | Card::MeditateCard | Card::InnerPeace | Card::Indignation |
            Card::Swivel | Card::Perseverance | Card::Pray | Card::Prostrate |
            Card::WreathOfFlameCard |
            Card::Blasphemy | Card::DeusExMachina | Card::OmniscienceCard | Card::ScrawlCard |
            Card::VaultCard | Card::WishCard | Card::SpiritShieldCard | Card::JudgmentCard |
            Card::WorshipCard |
            // Silent skills
            Card::Backflip | Card::DodgeAndRoll | Card::Deflect | Card::CloakAndDagger |
            Card::BladeDance | Card::Prepared | Card::DeadlyPoison | Card::Acrobatics |
            Card::Blur | Card::BouncingFlask | Card::Concentrate | Card::CalculatedGamble |
            Card::Catalyst | Card::CripplingCloud | Card::LegSweep | Card::Outmaneuver |
            Card::PiercingWail | Card::EscapePlan | Card::Expertise | Card::RiddleWithHoles |
            Card::Setup | Card::Terror | Card::Adrenaline | Card::BulletTime |
            Card::Malaise | Card::StormOfSteel | Card::Doppelganger | Card::CorpseExplosionCard |
            Card::Reflex | Card::Tactician |
            // Defect skills
            Card::ChargeBattery | Card::Chaos | Card::Coolheaded | Card::Leap |
            Card::Recursion | Card::SteamBarrier |
            Card::DarknessCard | Card::DoubleEnergy | Card::Equilibrium | Card::ForceField |
            Card::Glacier | Card::Hologram | Card::Overclock | Card::RecycleCard |
            Card::Reprogram | Card::StackCard | Card::TURBO | Card::ReinforcedBody |
            Card::Fission | Card::MultiCast | Card::RainbowCard | Card::SeekCard |
            Card::SkimCard | Card::TempestCard |
            Card::Flex | Card::Havoc | Card::SeeingRed |
            Card::ShrugItOff | Card::TrueGrit | Card::Warcry |
            Card::BattleTrance | Card::BurningPact | Card::Disarm | Card::Entrench |
            Card::FlameBarrier | Card::GhostlyArmor |
            Card::PowerThrough | Card::RageCard | Card::SecondWind | Card::Sentinel |
            Card::Shockwave | Card::SpotWeakness |
            Card::DoubleTap | Card::Exhume | Card::LimitBreak | Card::Offering |
            Card::Impervious | Card::Rupture => CardType::Skill,

            // Powers
            // Watcher powers
            Card::BattleHymnCard | Card::SimmeringFuryCard | Card::MentalFortressCard |
            Card::NirvanaCard | Card::LikeWaterCard | Card::ForesightCard | Card::StudyCard |
            Card::RushdownCard | Card::OmegaCard | Card::DevaFormCard | Card::DevotionCard |
            Card::EstablishmentCard | Card::ConjureBladeCard |
            Card::Inflame | Card::Metallicize | Card::CombustCard | Card::DarkEmbrace |
            Card::Evolve | Card::FeelNoPain | Card::FireBreathing |
            Card::Barricade | Card::BerserkCard | Card::Corruption | Card::DemonForm |
            Card::Juggernaut |
            // Silent powers
            Card::AccuracyCard | Card::AfterImageCard | Card::FootworkCard |
            Card::NoxiousFumesCard | Card::WellLaidPlansCard | Card::DistractionCard |
            Card::InfiniteBlades | Card::AThousandCutsCard | Card::BurstCard |
            Card::EnvenomCard | Card::ToolsOfTheTradeCard | Card::WraithFormCard |
            // Defect powers
            Card::CapacitorCard | Card::ConsumeCard | Card::FusionCard | Card::HeatsinkCard |
            Card::LoopCard | Card::MachineLearningCard | Card::StormCard |
            Card::BufferCard | Card::DefragmentCard | Card::EchoFormCard |
            Card::ElectrodynamicsCard | Card::StaticDischargeCard |
            Card::AmplifyCard => CardType::Power,

            // Status
            Card::Dazed | Card::Burn | Card::Wound | Card::Slimed | Card::VoidCard => CardType::Status,

            // Curse
            Card::AscendersBane | Card::Injury | Card::Pain | Card::Decay => CardType::Curse,
        }
    }

    pub fn can_upgrade(&self) -> bool {
        !matches!(self.card_type(), CardType::Status | CardType::Curse)
    }

    pub fn has_target(&self) -> bool {
        match self {
            // Single-target attacks
            Card::StrikeRed | Card::StrikeGreen | Card::StrikeBlue | Card::StrikePurple |
            Card::Neutralize | Card::Eruption |
            // Watcher single-target attacks
            Card::FlurryOfBlows | Card::EmptyFist | Card::CutThroughFate | Card::JustLucky |
            Card::CrushJoints | Card::FearNoEvil | Card::ForeignInfluence | Card::SashWhip |
            Card::Tantrum | Card::CarveReality | Card::SandsOfTime | Card::WindmillStrike |
            Card::Wallop | Card::Weave | Card::SignatureMove | Card::FlyingSleeves |
            Card::ReachHeaven | Card::Ragnarok | Card::BrillianceCard |
            // Silent single-target attacks
            Card::PoisonedStab | Card::DaggerThrow | Card::SneakyStrike | Card::Slice |
            Card::Backstab | Card::Bane | Card::Choke | Card::Predator | Card::MasterfulStab |
            Card::Dash | Card::Finisher | Card::Flechettes | Card::Unload | Card::Skewer |
            Card::Bash | Card::Anger | Card::BodySlam |
            Card::Clash | Card::Clothesline | Card::HeavyBlade |
            Card::IronWave | Card::PerfectedStrike | Card::PommelStrike |
            Card::TwinStrike | Card::WildStrike |
            Card::BloodForBlood | Card::Carnage | Card::Headbutt |
            Card::Rampage | Card::SeverSoul | Card::Uppercut |
            Card::Bludgeon | Card::Feed | Card::FiendFire |
            // Defect single-target attacks
            Card::BallLightning | Card::Barrage | Card::BeamCell | Card::Claw |
            Card::CompileDriver | Card::GoForTheEyes |
            Card::ColdSnap | Card::FTL | Card::MelterCard | Card::Scrape |
            Card::Streamline | Card::Sunder |
            Card::AllForOne | Card::CoreSurge | Card::MeteorStrike => true,
            // Skills that target one enemy
            Card::Disarm | Card::SpotWeakness |
            Card::DeadlyPoison | Card::BouncingFlask | Card::Catalyst | Card::LegSweep |
            Card::Terror | Card::Malaise | Card::CorpseExplosionCard |
            Card::JudgmentCard => true,
            _ => false,
        }
    }

    pub fn name(&self) -> &str {
        match self {
            Card::StrikeRed | Card::StrikeGreen | Card::StrikeBlue | Card::StrikePurple => "Strike",
            Card::DefendRed | Card::DefendGreen | Card::DefendBlue | Card::DefendPurple => "Defend",
            Card::Bash => "Bash",
            Card::Neutralize => "Neutralize",
            Card::Survivor => "Survivor",
            Card::Zap => "Zap",
            Card::Dualcast => "Dualcast",
            Card::Eruption => "Eruption",
            Card::Vigilance => "Vigilance",
            // Watcher cards
            Card::FlurryOfBlows => "Flurry of Blows",
            Card::EmptyFist => "Empty Fist",
            Card::Consecrate => "Consecrate",
            Card::CutThroughFate => "Cut Through Fate",
            Card::JustLucky => "Just Lucky",
            Card::EmptyBody => "Empty Body",
            Card::Protect => "Protect",
            Card::Halt => "Halt",
            Card::ThirdEye => "Third Eye",
            Card::Tranquility => "Tranquility",
            Card::Crescendo => "Crescendo",
            Card::Collect => "Collect",
            Card::CrushJoints => "Crush Joints",
            Card::FearNoEvil => "Fear No Evil",
            Card::ForeignInfluence => "Foreign Influence",
            Card::SashWhip => "Sash Whip",
            Card::Tantrum => "Tantrum",
            Card::CarveReality => "Carve Reality",
            Card::SandsOfTime => "Sands of Time",
            Card::WindmillStrike => "Windmill Strike",
            Card::Wallop => "Wallop",
            Card::Weave => "Weave",
            Card::SignatureMove => "Signature Move",
            Card::FlyingSleeves => "Flying Sleeves",
            Card::Conclude => "Conclude",
            Card::ReachHeaven => "Reach Heaven",
            Card::EmptyMind => "Empty Mind",
            Card::MeditateCard => "Meditate",
            Card::InnerPeace => "Inner Peace",
            Card::Indignation => "Indignation",
            Card::Swivel => "Swivel",
            Card::Perseverance => "Perseverance",
            Card::Pray => "Pray",
            Card::Prostrate => "Prostrate",
            Card::WreathOfFlameCard => "Wreath of Flame",
            Card::BattleHymnCard => "Battle Hymn",
            Card::SimmeringFuryCard => "Simmering Fury",
            Card::MentalFortressCard => "Mental Fortress",
            Card::NirvanaCard => "Nirvana",
            Card::LikeWaterCard => "Like Water",
            Card::ForesightCard => "Foresight",
            Card::StudyCard => "Study",
            Card::RushdownCard => "Rushdown",
            Card::Ragnarok => "Ragnarok",
            Card::BrillianceCard => "Brilliance",
            Card::Blasphemy => "Blasphemy",
            Card::DeusExMachina => "Deus Ex Machina",
            Card::OmniscienceCard => "Omniscience",
            Card::ScrawlCard => "Scrawl",
            Card::VaultCard => "Vault",
            Card::WishCard => "Wish",
            Card::SpiritShieldCard => "Spirit Shield",
            Card::JudgmentCard => "Judgment",
            Card::WorshipCard => "Worship",
            Card::OmegaCard => "Omega",
            Card::DevaFormCard => "Deva Form",
            Card::DevotionCard => "Devotion",
            Card::EstablishmentCard => "Establishment",
            Card::ConjureBladeCard => "Conjure Blade",
            // Silent cards
            Card::PoisonedStab => "Poisoned Stab",
            Card::DaggerThrow => "Dagger Throw",
            Card::DaggerSpray => "Dagger Spray",
            Card::SneakyStrike => "Sneaky Strike",
            Card::Slice => "Slice",
            Card::Backflip => "Backflip",
            Card::DodgeAndRoll => "Dodge and Roll",
            Card::Deflect => "Deflect",
            Card::CloakAndDagger => "Cloak and Dagger",
            Card::BladeDance => "Blade Dance",
            Card::Prepared => "Prepared",
            Card::DeadlyPoison => "Deadly Poison",
            Card::Acrobatics => "Acrobatics",
            Card::AccuracyCard => "Accuracy",
            Card::AfterImageCard => "After Image",
            Card::Backstab => "Backstab",
            Card::Bane => "Bane",
            Card::Choke => "Choke",
            Card::Predator => "Predator",
            Card::MasterfulStab => "Masterful Stab",
            Card::Dash => "Dash",
            Card::Finisher => "Finisher",
            Card::Flechettes => "Flechettes",
            Card::AllOutAttack => "All-Out Attack",
            Card::Unload => "Unload",
            Card::Blur => "Blur",
            Card::BouncingFlask => "Bouncing Flask",
            Card::Concentrate => "Concentrate",
            Card::CalculatedGamble => "Calculated Gamble",
            Card::Catalyst => "Catalyst",
            Card::CripplingCloud => "Crippling Cloud",
            Card::LegSweep => "Leg Sweep",
            Card::Outmaneuver => "Outmaneuver",
            Card::PiercingWail => "Piercing Wail",
            Card::EscapePlan => "Escape Plan",
            Card::Expertise => "Expertise",
            Card::RiddleWithHoles => "Riddle with Holes",
            Card::Setup => "Setup",
            Card::Terror => "Terror",
            Card::FootworkCard => "Footwork",
            Card::NoxiousFumesCard => "Noxious Fumes",
            Card::WellLaidPlansCard => "Well-Laid Plans",
            Card::DistractionCard => "Distraction",
            Card::InfiniteBlades => "Infinite Blades",
            Card::DieDieDie => "Die Die Die",
            Card::GrandFinale => "Grand Finale",
            Card::Skewer => "Skewer",
            Card::Adrenaline => "Adrenaline",
            Card::BulletTime => "Bullet Time",
            Card::Malaise => "Malaise",
            Card::StormOfSteel => "Storm of Steel",
            Card::Doppelganger => "Doppelganger",
            Card::CorpseExplosionCard => "Corpse Explosion",
            Card::AThousandCutsCard => "A Thousand Cuts",
            Card::BurstCard => "Burst",
            Card::EnvenomCard => "Envenom",
            Card::ToolsOfTheTradeCard => "Tools of the Trade",
            Card::WraithFormCard => "Wraith Form",
            Card::Reflex => "Reflex",
            Card::Tactician => "Tactician",
            // Defect cards
            Card::BallLightning => "Ball Lightning",
            Card::Barrage => "Barrage",
            Card::BeamCell => "Beam Cell",
            Card::Claw => "Claw",
            Card::CompileDriver => "Compile Driver",
            Card::GoForTheEyes => "Go for the Eyes",
            Card::SweepingBeam => "Sweeping Beam",
            Card::ChargeBattery => "Charge Battery",
            Card::Chaos => "Chaos",
            Card::Coolheaded => "Coolheaded",
            Card::Leap => "Leap",
            Card::Recursion => "Recursion",
            Card::SteamBarrier => "Steam Barrier",
            Card::Blizzard => "Blizzard",
            Card::ColdSnap => "Cold Snap",
            Card::DoomAndGloom => "Doom and Gloom",
            Card::FTL => "FTL",
            Card::MelterCard => "Melter",
            Card::Scrape => "Scrape",
            Card::Streamline => "Streamline",
            Card::Sunder => "Sunder",
            Card::DarknessCard => "Darkness",
            Card::DoubleEnergy => "Double Energy",
            Card::Equilibrium => "Equilibrium",
            Card::ForceField => "Force Field",
            Card::Glacier => "Glacier",
            Card::Hologram => "Hologram",
            Card::Overclock => "Overclock",
            Card::RecycleCard => "Recycle",
            Card::Reprogram => "Reprogram",
            Card::StackCard => "Stack",
            Card::TURBO => "TURBO",
            Card::ReinforcedBody => "Reinforced Body",
            Card::CapacitorCard => "Capacitor",
            Card::ConsumeCard => "Consume",
            Card::FusionCard => "Fusion",
            Card::HeatsinkCard => "Heatsinks",
            Card::LoopCard => "Loop",
            Card::MachineLearningCard => "Machine Learning",
            Card::StormCard => "Storm",
            Card::AllForOne => "All for One",
            Card::CoreSurge => "Core Surge",
            Card::Hyperbeam => "Hyperbeam",
            Card::MeteorStrike => "Meteor Strike",
            Card::ThunderStrike => "Thunder Strike",
            Card::AmplifyCard => "Amplify",
            Card::Fission => "Fission",
            Card::MultiCast => "Multi-Cast",
            Card::RainbowCard => "Rainbow",
            Card::SeekCard => "Seek",
            Card::SkimCard => "Skim",
            Card::TempestCard => "Tempest",
            Card::BufferCard => "Buffer",
            Card::DefragmentCard => "Defragment",
            Card::EchoFormCard => "Echo Form",
            Card::ElectrodynamicsCard => "Electrodynamics",
            Card::StaticDischargeCard => "Static Discharge",
            Card::Anger => "Anger",
            Card::BodySlam => "Body Slam",
            Card::Clash => "Clash",
            Card::Cleave => "Cleave",
            Card::Clothesline => "Clothesline",
            Card::HeavyBlade => "Heavy Blade",
            Card::IronWave => "Iron Wave",
            Card::PerfectedStrike => "Perfected Strike",
            Card::PommelStrike => "Pommel Strike",
            Card::TwinStrike => "Twin Strike",
            Card::WildStrike => "Wild Strike",
            Card::Flex => "Flex",
            Card::Havoc => "Havoc",
            Card::SeeingRed => "Seeing Red",
            Card::ShrugItOff => "Shrug It Off",
            Card::TrueGrit => "True Grit",
            Card::Warcry => "Warcry",
            Card::BloodForBlood => "Blood for Blood",
            Card::Carnage => "Carnage",
            Card::Headbutt => "Headbutt",
            Card::Rampage => "Rampage",
            Card::SeverSoul => "Sever Soul",
            Card::Uppercut => "Uppercut",
            Card::Whirlwind => "Whirlwind",
            Card::BattleTrance => "Battle Trance",
            Card::BurningPact => "Burning Pact",
            Card::Disarm => "Disarm",
            Card::Entrench => "Entrench",
            Card::FlameBarrier => "Flame Barrier",
            Card::GhostlyArmor => "Ghostly Armor",
            Card::PowerThrough => "Power Through",
            Card::RageCard => "Rage",
            Card::SecondWind => "Second Wind",
            Card::Sentinel => "Sentinel",
            Card::Shockwave => "Shockwave",
            Card::SpotWeakness => "Spot Weakness",
            Card::Inflame => "Inflame",
            Card::Metallicize => "Metallicize",
            Card::CombustCard => "Combust",
            Card::DarkEmbrace => "Dark Embrace",
            Card::Evolve => "Evolve",
            Card::FeelNoPain => "Feel No Pain",
            Card::FireBreathing => "Fire Breathing",
            Card::Rupture => "Rupture",
            Card::Bludgeon => "Bludgeon",
            Card::Feed => "Feed",
            Card::FiendFire => "Fiend Fire",
            Card::Immolate => "Immolate",
            Card::DoubleTap => "Double Tap",
            Card::Exhume => "Exhume",
            Card::LimitBreak => "Limit Break",
            Card::Offering => "Offering",
            Card::Impervious => "Impervious",
            Card::Barricade => "Barricade",
            Card::BerserkCard => "Berserk",
            Card::Corruption => "Corruption",
            Card::DemonForm => "Demon Form",
            Card::Juggernaut => "Juggernaut",
            Card::Dazed => "Dazed",
            Card::Burn => "Burn",
            Card::Wound => "Wound",
            Card::Slimed => "Slimed",
            Card::VoidCard => "Void",
            Card::AscendersBane => "Ascender's Bane",
            Card::Injury => "Injury",
            Card::Pain => "Pain",
            Card::Decay => "Decay",
        }
    }

    pub fn ethereal(&self) -> bool {
        match self {
            Card::Dazed | Card::VoidCard | Card::Decay => true,
            Card::Carnage | Card::GhostlyArmor => true,
            Card::DefragmentCard | Card::EchoFormCard => true,  // ethereal when not upgraded
            Card::JudgmentCard => true,  // ethereal when not upgraded
            _ => false,
        }
    }

    pub fn unplayable(&self) -> bool {
        match self {
            Card::Dazed | Card::Burn | Card::Wound | Card::VoidCard => true,
            Card::AscendersBane | Card::Injury | Card::Pain | Card::Decay => true,
            Card::Reflex | Card::Tactician => true,
            _ => false,
        }
    }

    pub fn innate(&self) -> bool {
        false
    }

    pub fn retain(&self) -> bool {
        matches!(self, Card::Outmaneuver | Card::CoreSurge |
            Card::Protect | Card::Tranquility | Card::Crescendo |
            Card::SandsOfTime | Card::WindmillStrike | Card::FlyingSleeves |
            Card::Perseverance)
    }

    /// Whether this card has "Strike" in its name (for Perfected Strike).
    pub fn is_strike(&self) -> bool {
        matches!(self, Card::StrikeRed | Card::StrikeGreen | Card::StrikeBlue | Card::StrikePurple |
            Card::PerfectedStrike | Card::TwinStrike | Card::ThunderStrike | Card::MeteorStrike |
            Card::WindmillStrike)
    }
}

// Legacy PyO3 methods on Card enum for backward compatibility with tests
#[pymethods]
impl Card {
    #[getter]
    fn py_cost(&self) -> i32 {
        CardInstance::new(*self, false).cost()
    }

    #[getter]
    fn py_card_type(&self) -> CardType {
        self.card_type()
    }

    #[getter]
    fn py_base_damage(&self) -> i32 {
        CardInstance::new(*self, false).base_damage()
    }

    #[getter]
    fn py_base_block(&self) -> i32 {
        CardInstance::new(*self, false).base_block()
    }

    #[getter]
    fn py_base_magic(&self) -> i32 {
        CardInstance::new(*self, false).base_magic()
    }

    #[getter]
    fn py_has_target(&self) -> bool {
        self.has_target()
    }

    #[getter]
    fn py_name(&self) -> &str {
        self.name()
    }
}

/// Create the Ironclad starter deck: 5x Strike, 4x Defend, 1x Bash
pub fn ironclad_starter_deck() -> Vec<CardInstance> {
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

/// Create the Silent starter deck: 5x Strike, 5x Defend, 1x Neutralize, 1x Survivor
pub fn silent_starter_deck() -> Vec<CardInstance> {
    let mut deck = Vec::with_capacity(12);
    for _ in 0..5 {
        deck.push(CardInstance::new(Card::StrikeGreen, false));
    }
    for _ in 0..5 {
        deck.push(CardInstance::new(Card::DefendGreen, false));
    }
    deck.push(CardInstance::new(Card::Neutralize, false));
    deck.push(CardInstance::new(Card::Survivor, false));
    deck
}

/// Create the Defect starter deck: 4x Strike, 4x Defend, 1x Zap, 1x Dualcast
pub fn defect_starter_deck() -> Vec<CardInstance> {
    let mut deck = Vec::with_capacity(10);
    for _ in 0..4 {
        deck.push(CardInstance::new(Card::StrikeBlue, false));
    }
    for _ in 0..4 {
        deck.push(CardInstance::new(Card::DefendBlue, false));
    }
    deck.push(CardInstance::new(Card::Zap, false));
    deck.push(CardInstance::new(Card::Dualcast, false));
    deck
}

/// Create the Watcher starter deck: 4x Strike, 4x Defend, 1x Eruption, 1x Vigilance
pub fn watcher_starter_deck() -> Vec<CardInstance> {
    let mut deck = Vec::with_capacity(10);
    for _ in 0..4 {
        deck.push(CardInstance::new(Card::StrikePurple, false));
    }
    for _ in 0..4 {
        deck.push(CardInstance::new(Card::DefendPurple, false));
    }
    deck.push(CardInstance::new(Card::Eruption, false));
    deck.push(CardInstance::new(Card::Vigilance, false));
    deck
}

/// Get the starter deck for a given character.
pub fn starter_deck(character: Character) -> Vec<CardInstance> {
    match character {
        Character::Ironclad => ironclad_starter_deck(),
        Character::Silent => silent_starter_deck(),
        Character::Defect => defect_starter_deck(),
        Character::Watcher => watcher_starter_deck(),
    }
}
