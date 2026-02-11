use pyo3::prelude::*;

#[pyclass(frozen, eq, eq_int, hash)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum Character {
    Ironclad,
    Silent,
    Defect,
    Watcher,
}

#[pyclass(frozen, eq, eq_int, hash)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum CardType {
    Attack,
    Skill,
    Power,
    Status,
    Curse,
}

#[pyclass(frozen, eq, eq_int, hash)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum PowerType {
    // Base powers
    Strength,
    Vulnerable,
    Weak,
    Ritual,
    CurlUp,
    // Extended powers for Act 1
    Dexterity,
    Thorns,
    Metallicize,
    Barricade,
    Rage,
    FeelNoPain,
    DarkEmbrace,
    Rupture,
    Combust,
    Evolve,
    FireBreathing,
    Anger,      // Gremlin Nob: gain Str when player plays Skill
    Entangled,  // Can't play attacks this turn
    Artifact,   // Negate next debuff application
    SporeCloud, // Apply Vulnerable on death
    Juggernaut, // Deal damage on block gain
    DemonForm,  // Gain Str at start of turn
    Corruption, // Skills cost 0, exhaust on play
    DoubleTap,  // Next attack plays twice
    NoDraw,     // Can't draw cards rest of turn
    // Ironclad-specific
    Berserk,    // Gain 1 energy at start of turn
    // Silent-specific
    Poison,         // Deal Poison damage at end of monster turn, reduce by 1
    Accuracy,       // Increase Shiv damage
    AfterImage,     // Gain block when discarding a card
    Envenom,        // Attacks apply poison
    NoxiousFumes,   // Apply poison at start of turn
    AThousandCuts,  // Deal damage to all enemies on deck shuffle
    InfiniteBlades, // Generate shivs at start of turn
    WellLaidPlans,  // Retain extra cards
    WraithForm,     // Invincibility turns
    ToolsOfTheTrade,// Extra card draw per turn
    Distraction,    // Enemy attack penalty
    CorpseExplosion,// Damage on poison death
    Burst,          // Next skill plays twice
    // Defect-specific
    Storm,          // Channel Lightning at start of turn
    Loop,           // Trigger orb passive/evoke extra times
    BufferPower,    // Prevent next N HP losses
    Heatsink,       // Draw card when playing a Power
    EchoForm,       // First card each turn plays twice
    DrawPerTurn,    // +N card draw per turn (Machine Learning)
    Electrodynamics,// Lightning hits all enemies
    OrbEvoke,       // Increase orb evoke amounts (Consume)
    OrbPassive,     // Increase orb passive amounts (Defragment)
    StaticDischarge,// Increase Lightning passive
    AmplifyDark,    // Increase Dark orb evoke (Amplify)
    EnergyPerTurn,  // +N energy per turn (Fusion)
    // Watcher-specific
    TripleAttack,    // Next attack plays 3x (Blasphemy)
    MentalFortress,  // Gain block on stance change
    Rushdown,        // Draw cards when entering Wrath
    LikeWater,       // Gain block at end of turn if in Calm
    OmegaPower,      // Deal damage at end of turn
    DevotionPower,   // Gain miracles at start of turn
    SimmeringFury,   // Increase Wrath damage bonus

    NirvanaPower,    // Gain block on scry
    ForesightPower,  // Scry at start of turn
    StudyPower,      // Extra draw per turn
    DevaFormPower,   // Extra energy per turn (stacking)
    EstablishmentPower, // Retained cards cost less
    BattleHymnPower, // Add Smite at start of turn
    ConclusionPower, // End of turn: enter Neutral
    MiracleCount,    // Tracks miracle tokens (extra energy)
    LoseStrength,    // Lose Strength at end of turn (MutagenicStrength relic)
    ConjureBladePower, // Bonus damage to starter Strikes only
}

#[pyclass(frozen, eq, eq_int, hash)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum Stance {
    Neutral,
    Wrath,
    Calm,
}

#[pyclass(frozen, eq, eq_int, hash)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum OrbType {
    Lightning,
    Frost,
    Dark,
}

#[pyclass(frozen, eq, eq_int, hash)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum Intent {
    Attack,
    AttackBuff,
    AttackDebuff,
    AttackDefend,
    Defend,
    DefendBuff,
    Buff,
    Debuff,
    StrongDebuff,
    Sleep,
    Stun,
    Escape,
    Unknown,
}

#[pyclass(frozen, eq, eq_int, hash)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum Relic {
    // Starter (Ironclad)
    BurningBlood,       // Heal 1 HP on victory
    // Starter (Silent)
    RingOfTheSnake,     // Draw 2 extra cards turn 1
    Shivs,              // 5 shiv tokens (Silent-specific resource)
    // Starter (Defect)
    CrackedCore,        // Channel 1 Lightning at combat start
    // Starter (Watcher)
    Miracles,           // Miracle tokens for extra energy
    // Common
    Lantern,            // +1 energy first turn
    BagOfPreparation,   // Draw 2 extra at battle start
    Anchor,             // +2 block at start of combat
    Orichalcum,         // +1 block at end of turn if block is 0
    Vajra,              // Die roll 2: +1 temp Str
    OddlySmoothStone,   // Die roll 4: +2 block
    PenNib,             // Die roll 5: 1 Vuln to first alive monster
    HornCleat,          // Die roll 1-2: +1 block
    HappyFlower,        // Die roll 3-4: +1 energy
    RedSkull,           // +1 Str when deck is shuffled
    MeatOnTheBone,      // Heal to 4 HP on victory if HP 1-3
    // Uncommon
    MercuryHourglass,   // Deal 1 damage to all enemies at start of turn
    // Boss
    BlackBlood,         // Heal 2 HP on victory (replaces Burning Blood)
    // Die-roll relics
    CaptainsWheel,      // Die 3: +3 block
    Sundial,            // Die 2: +2 energy
    TungstenRod,        // Die 5: +3 block
    RedMask,            // Die 5-6: 1 Weak to first monster
    Necronomicon,       // Die 1: DoubleTap
    InkBottle,          // Die 5-6: draw 1
    Pocketwatch,        // Die 3: draw 3
    GremlinHorn,        // Die 4: draw 1; die 5: +1 energy
    StoneCalendar,      // Die 4: 4 damage to first monster
    TheBoot,            // Die 4-6: 1 damage to first monster
    Duality,            // Die 2: +2 block; die 4: 2 damage to first monster
    // Combat start
    BloodVial,          // Heal 1 HP at battle start
    FrozenCore,         // +1 Metallicize at battle start
    MutagenicStrength,  // +1 Str, +1 LoseStrength at battle start
    // Boss die-roll
    IncenseBurner,      // Die 6: Buffer(1)
    SneckoEye,          // Die 1-2: draw 2; 3-4: +1 energy; 5-6: add Dazed
    // On card play
    BirdFacedUrn,       // +1 block when playing Power
}

#[pyclass(frozen, eq, eq_int, hash)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum EventType {
    BigFish,
    GoldenIdol,
    GoldenWing,
    WorldOfGoop,
    Cleric,
    LivingWall,
    ScrapOoze,
    DeadAdventurer,
    KnowingSkull,
}

#[pyclass(frozen, eq, eq_int, hash)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum RoomType {
    Monster,
    Elite,
    Rest,
    Shop,
    Event,
    Treasure,
    Boss,
    Empty,
}

#[pyclass(frozen, eq, eq_int, hash)]
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum CardRarity {
    Common,
    Uncommon,
    Rare,
}
