# Live Verification Plan

Comprehensive plan to verify every implemented card against the live BG mod game.
Track progress by marking items `[x]` as they are completed.

## How to Run

```bash
cd /data/code/sts_bot_2
.venv/bin/maturin develop --release && cp target/release/libsts_sim.so sts_sim.so
.venv/bin/python -m pytest tests/live/test_tier17_silent.py -v  # example
```

Game must be running with BG mod + CommunicationMod active.

### Starting the Game

From a terminal, launch Slay the Spire via ModTheSpire:

```bash
cd /home/erick/.steam/debian-installation/steamapps/common/SlayTheSpire
./jre/bin/java -jar /home/erick/.steam/debian-installation/steamapps/workshop/content/646570/1605060445/ModTheSpire.jar --skip-launcher --skip-intro &
```

The `--skip-launcher` flag bypasses the mod selection UI (uses previously selected mods).
The `--skip-intro` flag skips the STS splash screen for faster startup.

**Important:** After rebuilding CommunicationMod (`cd /data/code/CommunicationMod && mvn package`),
you must restart the game so the new jar is loaded.

## How to Add a New Card Test

1. Add card to `CARD_TO_BG` in `tests/live/conftest.py` (mapping below)
2. Add any new powers to `CLEAR_PLAYER_POWERS` if the card applies powers
3. Write test using `set_scenario()` + `make_sim()` + `play_card_both()`
4. Test both base and upgraded versions when possible

---

## Phase 1: Ironclad — Upgrade Tests (38 cards with base test but no upgrade test)

File: `tests/live/test_tier18_ironclad_upgrades.py`

Each test: play upgraded card, verify sim matches game.

- [x] Anger+
- [x] BattleTrance+
- [x] BerserkCard+
- [x] BloodForBlood+
- [x] BurningPact+
- [x] Clash+
- [x] Cleave+
- [x] Clothesline+
- [x] CombustCard+
- [x] Disarm+
- [x] DoubleTap+
- [x] Exhume+
- [x] Feed+
- [x] FiendFire+
- [x] FireBreathing+
- [x] FlameBarrier+
- [x] GhostlyArmor+
- [x] Havoc+
- [x] Headbutt+
- [x] Immolate+
- [x] LimitBreak+
- [x] Offering+
- [x] PerfectedStrike+
- [x] PowerThrough+
- [x] RageCard+
- [x] Rampage+
- [x] SecondWind+
- [x] Sentinel+
- [x] SeverSoul+
- [x] Shockwave+
- [x] ShrugItOff+
- [x] SpotWeakness+
- [x] TrueGrit+
- [x] TwinStrike+
- [x] Warcry+
- [x] Whirlwind+
- [x] WildStrike+

---

## Phase 2: Silent Cards — Base Tests (~48 cards)

File: `tests/live/test_tier17_silent.py`

### CARD_TO_BG mappings needed (add to conftest.py):
```python
# Silent starters
sts_sim.Card.StrikeGreen: "BGStrike_G",
sts_sim.Card.DefendGreen: "BGDefend_G",
sts_sim.Card.Neutralize: "BGNeutralize",
sts_sim.Card.Survivor: "BGSurvivor",
# Silent common attacks
sts_sim.Card.PoisonedStab: "BGPoisonedStab",
sts_sim.Card.DaggerThrow: "BGDaggerThrow",
sts_sim.Card.DaggerSpray: "BGDaggerSpray",
sts_sim.Card.SneakyStrike: "BGSneakyStrike",
sts_sim.Card.Slice: "BGSlice",
# Silent common skills
sts_sim.Card.Backflip: "BGBackflip",
sts_sim.Card.DodgeAndRoll: "BGDodgeAndRoll",
sts_sim.Card.Deflect: "BGDeflect",
sts_sim.Card.CloakAndDagger: "BGCloakAndDagger",
sts_sim.Card.BladeDance: "BGBladeDance",
sts_sim.Card.Prepared: "BGPrepared",
sts_sim.Card.DeadlyPoison: "BGDeadlyPoison",
sts_sim.Card.Acrobatics: "BGAcrobatics",
# Silent common powers
sts_sim.Card.AccuracyCard: "BGAccuracy",
sts_sim.Card.AfterImageCard: "BGAfterImage",
# Silent uncommon attacks
sts_sim.Card.Backstab: "BGBackstab",
sts_sim.Card.Bane: "BGBane",
sts_sim.Card.Choke: "BGChoke",
sts_sim.Card.Predator: "BGPredator",
sts_sim.Card.MasterfulStab: "BGMasterfulStab",
sts_sim.Card.Dash: "BGDash",
sts_sim.Card.Finisher: "BGFinisher",
sts_sim.Card.Flechettes: "BGFlechettes",
sts_sim.Card.AllOutAttack: "BGAllOutAttack",
sts_sim.Card.Unload: "BGUnload",
# Silent uncommon skills
sts_sim.Card.Blur: "BGBlur",
sts_sim.Card.BouncingFlask: "BGBouncingFlask",
sts_sim.Card.Concentrate: "BGConcentrate",
sts_sim.Card.CalculatedGamble: "BGCalculatedGamble",
sts_sim.Card.Catalyst: "BGCatalyst",
sts_sim.Card.CripplingCloud: "BGCripplingCloud",
sts_sim.Card.LegSweep: "BGLegSweep",
sts_sim.Card.Outmaneuver: "BGOutmaneuver",
sts_sim.Card.PiercingWail: "BGPiercingWail",
sts_sim.Card.EscapePlan: "BGEscapePlan",
sts_sim.Card.Expertise: "BGExpertise",
sts_sim.Card.RiddleWithHoles: "BGRiddleWithHoles",
sts_sim.Card.Setup: "BGSetup",
sts_sim.Card.Terror: "BGTerror",
# Silent uncommon powers
sts_sim.Card.FootworkCard: "BGFootwork",
sts_sim.Card.NoxiousFumesCard: "BGNoxiousFumes",
sts_sim.Card.WellLaidPlansCard: "BGWellLaidPlans",
sts_sim.Card.DistractionCard: "BGDistraction",
sts_sim.Card.InfiniteBlades: "BGInfinite Blades",
# Silent rare attacks
sts_sim.Card.DieDieDie: "BGDieDieDie",
sts_sim.Card.GrandFinale: "BGGrandFinale",
sts_sim.Card.Skewer: "BGSkewer",
# Silent rare skills
sts_sim.Card.Adrenaline: "BGAdrenaline",
sts_sim.Card.BulletTime: "BGBulletTime",
sts_sim.Card.Malaise: "BGMalaise",
sts_sim.Card.StormOfSteel: "BGStormOfSteel",
sts_sim.Card.Doppelganger: "BGDoppelganger",
sts_sim.Card.CorpseExplosionCard: "BGCorpseExplosion",
# Silent rare powers
sts_sim.Card.AThousandCutsCard: "BGAThousandCuts",
sts_sim.Card.BurstCard: "BGBurst",
sts_sim.Card.EnvenomCard: "BGEnvenom",
sts_sim.Card.ToolsOfTheTradeCard: "BGToolsOfTheTrade",
sts_sim.Card.WraithFormCard: "BGWraithForm",
```

### Tests (base versions):

**Starters:**
- [x] StrikeGreen
- [x] DefendGreen
- [x] Neutralize
- [x] Survivor

**Common Attacks:**
- [x] PoisonedStab
- [x] DaggerThrow
- [x] DaggerSpray
- [x] SneakyStrike
- [x] Slice

**Common Skills:**
- [x] Backflip
- [x] DodgeAndRoll
- [x] Deflect
- [x] CloakAndDagger
- [x] BladeDance
- [x] Prepared
- [x] DeadlyPoison
- [x] Acrobatics

**Common Powers:**
- [x] AccuracyCard
- [x] AfterImageCard

**Uncommon Attacks:**
- [x] Backstab
- [x] Bane
- [x] Choke
- [x] Predator
- [x] MasterfulStab
- [x] Dash
- [x] Finisher
- [x] Flechettes
- [x] AllOutAttack
- [x] Unload

**Uncommon Skills:**
- [x] Blur
- [x] BouncingFlask
- [x] Concentrate
- [x] CalculatedGamble
- [x] Catalyst
- [x] CripplingCloud
- [x] LegSweep
- [x] Outmaneuver
- [x] PiercingWail
- [x] EscapePlan
- [x] Expertise
- [x] RiddleWithHoles
- [x] Setup
- [x] Terror

**Uncommon Powers:**
- [x] FootworkCard
- [x] NoxiousFumesCard
- [x] WellLaidPlansCard
- [x] DistractionCard
- [x] InfiniteBlades

**Rare Attacks:**
- [x] DieDieDie
- [x] GrandFinale
- [x] Skewer

**Rare Skills:**
- [x] Adrenaline
- [x] BulletTime
- [x] Malaise
- [x] StormOfSteel
- [x] Doppelganger
- [x] CorpseExplosionCard

**Rare Powers:**
- [x] AThousandCutsCard
- [x] BurstCard
- [x] EnvenomCard
- [x] ToolsOfTheTradeCard
- [x] WraithFormCard

---

## Phase 3: Defect Cards — Base Tests (~56 cards)

File: `tests/live/test_tier19_defect.py`

### CARD_TO_BG mappings needed:
```python
# Defect starters
sts_sim.Card.StrikeBlue: "BGStrike_B",
sts_sim.Card.DefendBlue: "BGDefend_B",
sts_sim.Card.Zap: "BGZap",
sts_sim.Card.Dualcast: "BGDualcast",
# Defect common attacks
sts_sim.Card.BallLightning: "BGBallLightning",
sts_sim.Card.Barrage: "BGBarrage",
sts_sim.Card.BeamCell: "BGBeamCell",
sts_sim.Card.Claw: "BGClaw",
sts_sim.Card.CompileDriver: "BGCompileDriver",
sts_sim.Card.GoForTheEyes: "BGGoForTheEyes",
sts_sim.Card.SweepingBeam: "BGSweepingBeam",
# Defect common skills
sts_sim.Card.ChargeBattery: "BGChargeBattery",
sts_sim.Card.Chaos: "BGChaos",
sts_sim.Card.Coolheaded: "BGCoolheaded",
sts_sim.Card.Leap: "BGLeap",
sts_sim.Card.Recursion: "BGRecursion",
sts_sim.Card.SteamBarrier: "BGSteamBarrier",
# Defect uncommon attacks
sts_sim.Card.Blizzard: "BGBlizzard",
sts_sim.Card.ColdSnap: "BGColdSnap",
sts_sim.Card.DoomAndGloom: "BGDoomAndGloom",
sts_sim.Card.FTL: "BGFTL",
sts_sim.Card.MelterCard: "BGMelter",
sts_sim.Card.Scrape: "BGScrape",
sts_sim.Card.Streamline: "BGStreamline",
sts_sim.Card.Sunder: "BGSunder",
# Defect uncommon skills
sts_sim.Card.DarknessCard: "BGDarkness",
sts_sim.Card.DoubleEnergy: "BGDoubleEnergy",
sts_sim.Card.Equilibrium: "BGEquilibrium",
sts_sim.Card.ForceField: "BGForceField",
sts_sim.Card.Glacier: "BGGlacier",
sts_sim.Card.Hologram: "BGHologram",
sts_sim.Card.Overclock: "BGOverclock",
sts_sim.Card.RecycleCard: "BGRecycle",
sts_sim.Card.Reprogram: "BGReprogram",
sts_sim.Card.StackCard: "BGStack",
sts_sim.Card.TURBO: "BGTURBO",
sts_sim.Card.ReinforcedBody: "BGReinforcedBody",
# Defect uncommon powers
sts_sim.Card.CapacitorCard: "BGCapacitor",
sts_sim.Card.ConsumeCard: "BGConsume",
sts_sim.Card.FusionCard: "BGFusion",
sts_sim.Card.HeatsinkCard: "BGHeatsinks",
sts_sim.Card.LoopCard: "BGLoop",
sts_sim.Card.MachineLearningCard: "BGMachineLearning",
sts_sim.Card.StormCard: "BGStorm",
# Defect rare attacks
sts_sim.Card.AllForOne: "BGAllForOne",
sts_sim.Card.CoreSurge: "BGCoreSurge",
sts_sim.Card.Hyperbeam: "BGHyperbeam",
sts_sim.Card.MeteorStrike: "BGMeteorStrike",
sts_sim.Card.ThunderStrike: "BGThunderStrike",
# Defect rare skills
sts_sim.Card.AmplifyCard: "BGAmplify",
sts_sim.Card.Fission: "BGFission",
sts_sim.Card.MultiCast: "BGMultiCast",
sts_sim.Card.RainbowCard: "BGRainbow",
sts_sim.Card.SeekCard: "BGSeek",
sts_sim.Card.SkimCard: "BGSkim",
sts_sim.Card.TempestCard: "BGTempest",
# Defect rare powers
sts_sim.Card.BufferCard: "BGBuffer",
sts_sim.Card.DefragmentCard: "BGDefragment",
sts_sim.Card.EchoFormCard: "BGEchoForm",
sts_sim.Card.ElectrodynamicsCard: "BGElectrodynamics",
sts_sim.Card.StaticDischargeCard: "BGStaticDischarge",
```

### Tests (base versions):

**Starters:**
- [x] StrikeBlue
- [x] DefendBlue
- [x] Zap
- [x] Dualcast

**Common Attacks:**
- [x] BallLightning
- [x] Barrage
- [x] BeamCell
- [x] Claw
- [x] CompileDriver
- [x] GoForTheEyes
- [x] SweepingBeam

**Common Skills:**
- [x] ChargeBattery
- [x] Chaos
- [x] Coolheaded
- [x] Leap
- [x] Recursion
- [x] SteamBarrier

**Uncommon Attacks:**
- [x] Blizzard
- [x] ColdSnap
- [x] DoomAndGloom
- [x] FTL
- [x] MelterCard
- [x] Scrape
- [x] Streamline
- [x] Sunder

**Uncommon Skills:**
- [x] DarknessCard
- [x] DoubleEnergy
- [x] Equilibrium
- [x] ForceField
- [x] Glacier
- [x] Hologram
- [x] Overclock
- [x] RecycleCard
- [x] Reprogram
- [x] StackCard
- [x] TURBO
- [x] ReinforcedBody

**Uncommon Powers:**
- [x] CapacitorCard
- [x] ConsumeCard
- [x] FusionCard
- [x] HeatsinkCard
- [x] LoopCard
- [x] MachineLearningCard
- [x] StormCard

**Rare Attacks:**
- [x] AllForOne
- [x] CoreSurge
- [x] Hyperbeam
- [x] MeteorStrike
- [x] ThunderStrike

**Rare Skills:**
- [x] AmplifyCard
- [x] Fission
- [x] MultiCast
- [x] RainbowCard
- [x] SeekCard
- [x] SkimCard
- [x] TempestCard

**Rare Powers:**
- [x] BufferCard
- [x] DefragmentCard
- [x] EchoFormCard
- [x] ElectrodynamicsCard
- [x] StaticDischargeCard

---

## Phase 4: Watcher Cards — Base Tests (~60 cards)

File: `tests/live/test_tier20_watcher.py`

### CARD_TO_BG mappings needed:
```python
# Watcher starters
sts_sim.Card.StrikePurple: "BGStrike_W",
sts_sim.Card.DefendPurple: "BGDefend_W",
sts_sim.Card.Eruption: "BGEruption",
sts_sim.Card.Vigilance: "BGVigilance",
# Watcher common attacks
sts_sim.Card.FlurryOfBlows: "BGFlurryOfBlows",
sts_sim.Card.EmptyFist: "BGEmptyFist",
sts_sim.Card.Consecrate: "BGConsecrate",
sts_sim.Card.CutThroughFate: "BGCutThroughFate",
sts_sim.Card.JustLucky: "BGJustLucky",
# Watcher common skills
sts_sim.Card.EmptyBody: "BGEmptyBody",
sts_sim.Card.Protect: "BGProtect",
sts_sim.Card.Halt: "BGHalt",
sts_sim.Card.ThirdEye: "BGThirdEye",
sts_sim.Card.Tranquility: "BGTranquility",
sts_sim.Card.Crescendo: "BGCrescendo",
sts_sim.Card.Collect: "BGCollect",
# Watcher uncommon attacks
sts_sim.Card.CrushJoints: "BGCrushJoints",
sts_sim.Card.FearNoEvil: "BGFearNoEvil",
sts_sim.Card.ForeignInfluence: "BGForeignInfluence",
sts_sim.Card.SashWhip: "BGSashWhip",
sts_sim.Card.Tantrum: "BGTantrum",
sts_sim.Card.CarveReality: "BGCarveReality",
sts_sim.Card.SandsOfTime: "BGSandsOfTime",
sts_sim.Card.WindmillStrike: "BGWindmillStrike",
sts_sim.Card.Wallop: "BGWallop",
sts_sim.Card.Weave: "BGWeave",
sts_sim.Card.SignatureMove: "BGSignatureMove",
sts_sim.Card.FlyingSleeves: "BGFlyingSleeves",
sts_sim.Card.Conclude: "BGConclude",
sts_sim.Card.ReachHeaven: "BGReachHeaven",
# Watcher uncommon skills
sts_sim.Card.EmptyMind: "BGEmptyMind",
sts_sim.Card.MeditateCard: "BGMeditate",
sts_sim.Card.InnerPeace: "BGInnerPeace",
sts_sim.Card.Indignation: "BGIndignation",
sts_sim.Card.Swivel: "BGSwivel",
sts_sim.Card.Perseverance: "BGPerseverance",
sts_sim.Card.Pray: "BGPray",
sts_sim.Card.Prostrate: "BGProstrate",
sts_sim.Card.WreathOfFlameCard: "BGWreathOfFlame",
# Watcher uncommon powers
sts_sim.Card.BattleHymnCard: "BGBattleHymn",
sts_sim.Card.SimmeringFuryCard: "BGSimmeringFury",
sts_sim.Card.MentalFortressCard: "BGMentalFortress",
sts_sim.Card.NirvanaCard: "BGNirvana",
sts_sim.Card.LikeWaterCard: "BGLikeWater",
sts_sim.Card.ForesightCard: "BGForesight",
sts_sim.Card.StudyCard: "BGStudy",
sts_sim.Card.RushdownCard: "BGRushdown",
# Watcher rare attacks
sts_sim.Card.Ragnarok: "BGRagnarok",
sts_sim.Card.BrillianceCard: "BGBrilliance",
# Watcher rare skills
sts_sim.Card.Blasphemy: "BGBlasphemy",
sts_sim.Card.DeusExMachina: "BGDeusExMachina",
sts_sim.Card.OmniscienceCard: "BGOmniscience",
sts_sim.Card.ScrawlCard: "BGScrawl",
sts_sim.Card.VaultCard: "BGVault",  # NOTE: verify this ID
sts_sim.Card.WishCard: "BGWish",
sts_sim.Card.SpiritShieldCard: "BGSpiritShield",
sts_sim.Card.JudgmentCard: "BGJudgment",
sts_sim.Card.WorshipCard: "BGWorship",
# Watcher rare powers
sts_sim.Card.OmegaCard: "BGOmega",
sts_sim.Card.DevaFormCard: "BGDevaForm",
sts_sim.Card.DevotionCard: "BGDevotion",
sts_sim.Card.EstablishmentCard: "BGEstablishment",
sts_sim.Card.ConjureBladeCard: "BGConjureBlade",
```

### Tests (base versions):

**Starters:**
- [x] StrikePurple
- [x] DefendPurple
- [x] Eruption
- [x] Vigilance

**Common Attacks:**
- [x] FlurryOfBlows
- [x] EmptyFist
- [x] Consecrate
- [x] CutThroughFate
- [x] JustLucky

**Common Skills:**
- [x] EmptyBody
- [x] Protect
- [x] Halt
- [x] ThirdEye
- [x] Tranquility
- [x] Crescendo
- [x] Collect

**Uncommon Attacks:**
- [x] CrushJoints
- [x] FearNoEvil
- [x] ForeignInfluence
- [x] SashWhip
- [x] Tantrum
- [x] CarveReality
- [x] SandsOfTime
- [x] WindmillStrike
- [x] Wallop
- [x] Weave
- [x] SignatureMove
- [x] FlyingSleeves
- [x] Conclude
- [x] ReachHeaven

**Uncommon Skills:**
- [x] EmptyMind
- [x] MeditateCard
- [x] InnerPeace
- [x] Indignation
- [x] Swivel
- [x] Perseverance
- [x] Pray
- [x] Prostrate
- [x] WreathOfFlameCard

**Uncommon Powers:**
- [x] BattleHymnCard
- [x] SimmeringFuryCard
- [x] MentalFortressCard
- [x] NirvanaCard
- [x] LikeWaterCard
- [x] ForesightCard
- [x] StudyCard
- [x] RushdownCard

**Rare Attacks:**
- [x] Ragnarok
- [x] BrillianceCard

**Rare Skills:**
- [x] Blasphemy
- [x] DeusExMachina
- [x] OmniscienceCard
- [x] ScrawlCard
- [x] VaultCard
- [x] WishCard
- [x] SpiritShieldCard
- [x] JudgmentCard
- [x] WorshipCard

**Rare Powers:**
- [x] OmegaCard
- [x] DevaFormCard
- [x] DevotionCard
- [x] EstablishmentCard
- [x] ConjureBladeCard

---

## Phase 5: Silent/Defect/Watcher Upgrade Tests

Files:
- `tests/live/test_tier22_silent_upgrades.py` — 62 upgrade tests
- `tests/live/test_tier23_defect_upgrades.py` — 61 upgrade tests
- `tests/live/test_tier24_watcher_upgrades.py` — 63 upgrade tests

- [x] All Silent upgrade tests written (62 tests)
- [x] All Defect upgrade tests written (61 tests)
- [x] All Watcher upgrade tests written (63 tests)

---

## Phase 6: Status & Curse Cards

- [x] Dazed (already partially tested via WildStrike/Immolate)
- [x] Burn
- [x] Wound
- [x] Slimed
- [x] VoidCard
- [x] AscendersBane
- [x] Injury
- [x] Pain
- [x] Decay

---

## Summary

| Phase | Scope | Tests | File | Status |
|-------|-------|-------|------|--------|
| 1 | Ironclad upgrade tests | 37 | test_tier18_ironclad_upgrades.py | Done |
| 2 | Silent base tests | 60 | test_tier17_silent.py | Done |
| 3 | Defect base tests | 61 | test_tier19_defect.py | Done |
| 4 | Watcher base tests | 64 | test_tier20_watcher.py | Done |
| 5 | Character upgrade tests | 186 | test_tier22/23/24_*_upgrades.py | Done |
| 6 | Status & Curse cards | 9 | test_tier21_status_curse.py | Done |
| **Total** | | **417** | | **All done** |

Previously verified: 60 Ironclad base + 24 Ironclad upgrades = 84 tests passing.
New tests written: 417. Grand total: 501 live verification tests.
