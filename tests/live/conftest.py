"""Fixtures for live verification tests.

Session-scoped fixtures handle:
- Connecting to the CommunicationMod relay
- Starting a game and navigating to combat
- Cleaning up (abandoning the run) after all tests
"""

import sys
import os
import time

import pytest

# Ensure project root is on path so comms package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import sts_sim
from comms.client import Client


# ---------------------------------------------------------------------------
# Card ID mapping: simulator Card enum -> Board Game mod card ID string
# Used by the set command to place specific cards in hand/draw/discard piles.
# ---------------------------------------------------------------------------
CARD_TO_BG = {
    # Ironclad starters
    sts_sim.Card.StrikeRed: "BGStrike_R",
    sts_sim.Card.DefendRed: "BGDefend_R",
    sts_sim.Card.Bash: "BGBash",
    # Ironclad commons
    sts_sim.Card.Anger: "BGAnger",
    sts_sim.Card.BodySlam: "BGBody Slam",
    sts_sim.Card.Clash: "BGClash",
    sts_sim.Card.Cleave: "BGCleave",
    sts_sim.Card.Clothesline: "BGClothesline",
    sts_sim.Card.Flex: "BGFlex",
    sts_sim.Card.HeavyBlade: "BGHeavy Blade",
    sts_sim.Card.IronWave: "BGIron Wave",
    sts_sim.Card.PerfectedStrike: "BGPerfected Strike",
    sts_sim.Card.PommelStrike: "BGPommel Strike",
    sts_sim.Card.ShrugItOff: "BGShrug It Off",
    sts_sim.Card.TwinStrike: "BGTwin Strike",
    sts_sim.Card.WildStrike: "BGWild Strike",
    sts_sim.Card.Headbutt: "BGHeadbutt",
    sts_sim.Card.Havoc: "BGHavoc",
    sts_sim.Card.SeeingRed: "BGSeeing Red",
    sts_sim.Card.TrueGrit: "BGTrue Grit",
    sts_sim.Card.Warcry: "BGWarcry",
    # Ironclad uncommons
    sts_sim.Card.Uppercut: "BGUppercut",
    sts_sim.Card.Entrench: "BGEntrench",
    sts_sim.Card.Shockwave: "BGShockwave",
    sts_sim.Card.Whirlwind: "BGWhirlwind",
    sts_sim.Card.BattleTrance: "BGBattle Trance",
    sts_sim.Card.BurningPact: "BGBurning Pact",
    sts_sim.Card.Carnage: "BGCarnage",
    sts_sim.Card.BloodForBlood: "BGBlood for Blood",
    sts_sim.Card.Disarm: "BGDisarm",
    sts_sim.Card.FlameBarrier: "BGFlame Barrier",
    sts_sim.Card.GhostlyArmor: "BGGhostly Armor",
    sts_sim.Card.Inflame: "BGInflame",
    sts_sim.Card.Metallicize: "BGMetallicize",
    sts_sim.Card.PowerThrough: "BGPower Through",
    sts_sim.Card.Rampage: "BGRampage",
    sts_sim.Card.SecondWind: "BGSecond Wind",
    sts_sim.Card.Sentinel: "BGSentinel",
    sts_sim.Card.SeverSoul: "BGSever Soul",
    sts_sim.Card.SpotWeakness: "BGSpot Weakness",
    sts_sim.Card.RageCard: "BGRage",
    # Ironclad uncommon powers
    sts_sim.Card.CombustCard: "BGCombust",
    sts_sim.Card.DarkEmbrace: "BGDark Embrace",
    sts_sim.Card.Evolve: "BGEvolve",
    sts_sim.Card.FeelNoPain: "BGFeel No Pain",
    sts_sim.Card.FireBreathing: "BGFire Breathing",
    sts_sim.Card.Rupture: "BGRupture",
    # Ironclad rares
    sts_sim.Card.Bludgeon: "BGBludgeon",
    sts_sim.Card.Impervious: "BGImpervious",
    sts_sim.Card.Offering: "BGOffering",
    sts_sim.Card.Barricade: "BGBarricade",
    sts_sim.Card.BerserkCard: "BGBerserk",
    sts_sim.Card.Corruption: "BGCorruption",
    sts_sim.Card.DemonForm: "BGDemon Form",
    sts_sim.Card.DoubleTap: "BGDouble Tap",
    sts_sim.Card.Exhume: "BGExhume",
    sts_sim.Card.Feed: "BGFeed",
    sts_sim.Card.FiendFire: "BGFiend Fire",
    sts_sim.Card.Immolate: "BGImmolate",
    sts_sim.Card.Juggernaut: "BGJuggernaut",
    sts_sim.Card.LimitBreak: "BGLimit Break",
    # Status cards
    sts_sim.Card.Dazed: "BGDazed",
    sts_sim.Card.Burn: "BGBurn",
    # Note: Wound has no BG mod implementation (no BGWound card)
    sts_sim.Card.Slimed: "BGSlimed",
    sts_sim.Card.VoidCard: "BGVoidCard",
    # Curse cards
    sts_sim.Card.AscendersBane: "BGAscendersBane",
    sts_sim.Card.Injury: "BGInjury",
    sts_sim.Card.Pain: "BGPain",
    sts_sim.Card.Decay: "BGDecay",
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
    sts_sim.Card.MasterfulStab: "BGMasterful Stab",
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
    sts_sim.Card.VaultCard: "BGVault",
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
}


# ---------------------------------------------------------------------------
# Relic ID mapping: simulator Relic enum -> Board Game mod relic ID string
# ---------------------------------------------------------------------------
RELIC_TO_BG = {
    sts_sim.Relic.BurningBlood: "BoardGame:BurningBlood",
    sts_sim.Relic.RingOfTheSnake: "BGRing of the Snake",
    sts_sim.Relic.CrackedCore: "BGCrackedCore",
    sts_sim.Relic.Miracles: "BoardGame:BGMiracles",
    sts_sim.Relic.Lantern: "BGLantern",
    sts_sim.Relic.BagOfPreparation: "BGBag of Preparation",
    sts_sim.Relic.Anchor: "BGAnchor",
    sts_sim.Relic.Orichalcum: "BGOrichalcum",
    sts_sim.Relic.Vajra: "BGVajra",
    sts_sim.Relic.OddlySmoothStone: "BGOddly Smooth Stone",
    sts_sim.Relic.PenNib: "BGPen Nib",
    sts_sim.Relic.HornCleat: "BGHornCleat",
    sts_sim.Relic.HappyFlower: "BGHappy Flower",
    sts_sim.Relic.RedSkull: "BGRed Skull",
    sts_sim.Relic.MeatOnTheBone: "BGMeat on the Bone",
    sts_sim.Relic.MercuryHourglass: "BGMercury Hourglass",
    sts_sim.Relic.BlackBlood: "BGBlack Blood",
    sts_sim.Relic.CaptainsWheel: "BGCaptainsWheel",
    sts_sim.Relic.Sundial: "BGSundial",
    sts_sim.Relic.TungstenRod: "BGTungstenRod",
    sts_sim.Relic.RedMask: "BGRedMask",
    sts_sim.Relic.Necronomicon: "BGNecronomicon",
    sts_sim.Relic.InkBottle: "BGInkBottle",
    sts_sim.Relic.Pocketwatch: "BGPocketwatch",
    sts_sim.Relic.GremlinHorn: "Gremlin Horn",
    sts_sim.Relic.StoneCalendar: "BGStoneCalendar",
    sts_sim.Relic.TheBoot: "BGTheBoot",
    sts_sim.Relic.Duality: "BGDuality",
    sts_sim.Relic.BloodVial: "BGBlood Vial",
    sts_sim.Relic.FrozenCore: "BGFrozenCore",
    sts_sim.Relic.MutagenicStrength: "BGMutagenicStrength",
    sts_sim.Relic.IncenseBurner: "BGIncense Burner",
    sts_sim.Relic.SneckoEye: "BGSnecko Eye",
    sts_sim.Relic.BirdFacedUrn: "BGBird Faced Urn",
}


# ---------------------------------------------------------------------------
# Power clearing: SetStateCommand now clears ALL existing powers on a creature
# before applying the specified map.  We only need to send powers we actually
# want on the creature (amount > 0).  Empty dict {} means "clear everything".
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Session fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def client():
    """Connect to the CommunicationMod relay. Skip all tests if not reachable."""
    c = Client()
    try:
        c.connect(timeout=3.0)
    except ConnectionError:
        pytest.skip("Game relay not running on localhost:38281")
    yield c
    c.disconnect()


@pytest.fixture(scope="session")
def in_combat(client):
    """Ensure we are in an active combat encounter.

    Tries, in order:
    1. Already in combat -> use it
    2. At main menu -> start BG_IRONCLAD game, navigate to first fight
    3. On map screen -> choose first available node
    If none work, skip with a helpful message.
    """
    _drain(client)
    state, raw_cmds = _get_state_and_cmds(client)

    # Already in combat?
    if state and state.combat_state is not None:
        yield client
        return

    # If in a game but not in combat, abandon and start fresh
    if "abandon" in raw_cmds:
        client.abandon()
        state, raw_cmds = _wait_and_get(client, delay=2.0)

    # Navigate through death screen / post-game screens to main menu
    for _ in range(10):
        if "start" in raw_cmds:
            break
        for cmd in ("proceed", "confirm", "return", "skip", "leave"):
            if cmd in raw_cmds:
                client.send_command(cmd)
                state, raw_cmds = _wait_and_get(client, delay=1.5)
                break
        else:
            state, raw_cmds = _wait_and_get(client, delay=1.5)

    # Start a new game
    if "start" not in raw_cmds:
        pytest.skip("Could not reach main menu to start a game.")

    client.start_game("BG_IRONCLAD", 0)
    # BG mod takes a while to initialize — give it plenty of time
    state, raw_cmds = _wait_and_get(client, retries=8, delay=2.0)

    # Navigate through Neow event, card rewards, map until we reach combat.
    # The board game mod has: Neow card pick → Neow bonus → "start game" → map.
    for attempt in range(40):
        if state and state.combat_state is not None:
            break

        screen = state.screen_type.value if state and state.screen_type else None

        # Map screen — choose first available node (should be a fight)
        if screen == "MAP":
            if state.choice_list:
                client.choose(0)
                state, raw_cmds = _wait_and_get(client, delay=2.0)
                continue

        # Any chooseable screen (card rewards, events, etc.)
        if "choose" in raw_cmds and state and state.choice_list:
            client.choose(0)
            state, raw_cmds = _wait_and_get(client, delay=1.5)
            continue

        # Proceed / confirm through transition screens
        acted = False
        for cmd in ("proceed", "confirm", "skip", "return", "leave"):
            if cmd in raw_cmds:
                client.send_command(cmd)
                state, raw_cmds = _wait_and_get(client, delay=1.5)
                acted = True
                break

        if not acted:
            # No recognized command — wait for the game to finish its transition
            state, raw_cmds = _wait_and_get(client, delay=2.0)

    if state is None or state.combat_state is None:
        pytest.skip(
            "Could not reach combat. Please navigate to a combat encounter "
            "manually and re-run the tests."
        )

    yield client


def _drain(client):
    """Drain any stale buffered messages."""
    while True:
        try:
            client._recv_line(timeout=0.1)
        except (TimeoutError, OSError):
            break


def _get_state_and_cmds(client, timeout=10.0):
    """Request state and return (GameState_or_None, available_commands_list).

    Never raises on timeout — returns (None, []) instead.
    """
    try:
        client.request_state()
        state = client.wait_for_state(timeout=timeout)
    except (TimeoutError, OSError):
        return None, []
    raw_cmds = []
    if client.last_raw:
        raw_cmds = client.last_raw.get("available_commands", [])
    if state and state.available_commands:
        raw_cmds = state.available_commands
    return state, raw_cmds


def _wait_and_get(client, retries=5, delay=1.0):
    """Wait for state to stabilize, then return (state, raw_cmds)."""
    for _ in range(retries):
        time.sleep(delay)
        _drain(client)
        state, raw_cmds = _get_state_and_cmds(client)
        if state is not None or raw_cmds:
            return state, raw_cmds
    return None, []


# ---------------------------------------------------------------------------
# Per-test helper fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def game(in_combat):
    """Provides the connected client, guaranteed to be in combat."""
    return in_combat


# ---------------------------------------------------------------------------
# Helper functions (importable by test files)
# ---------------------------------------------------------------------------

def _dismiss_blocking_screens(client):
    """Dismiss any overlay screens (card rewards, energy choices, etc.)
    that prevent card play commands.

    Some card effects (e.g. X-cost energy choice) leave the game in a
    choose-only screen if a previous test failed mid-interaction.
    """
    for _ in range(5):
        _drain(client)
        client.request_state()
        try:
            state = client.wait_for_state(timeout=5.0)
        except (TimeoutError, OSError):
            return
        cmds = client.last_raw.get("available_commands", [])
        if "play" in cmds or "end" in cmds:
            return  # Combat is ready for card play
        if "choose" in cmds:
            if "confirm" in cmds:
                # Optional choice screen (scry, etc.) — just confirm
                client.send_command("confirm")
            else:
                # Mandatory choice — dismiss with first option
                client.choose(0)
            time.sleep(0.5)
            continue
        # HAND_SELECT stuck after choose — press confirm key directly
        if state and state.screen_type and state.screen_type.value == "HAND_SELECT":
            client.send_command("key confirm")
            time.sleep(0.5)
            continue
        for cmd in ("proceed", "confirm", "skip", "return", "leave"):
            if cmd in cmds:
                client.send_command(cmd)
                time.sleep(0.5)
                break
        else:
            time.sleep(0.5)


def _resolve_choices(client, game_state, choices):
    """Resolve post-play choice screens by sending choose commands."""
    state = game_state
    for i, choice in enumerate(choices):
        cmds = client.last_raw.get("available_commands", [])
        if "play" in cmds or "end" in cmds:
            return state  # Back in combat
        assert "choose" in cmds, (
            f"Expected choice screen #{i}, got commands: {cmds}"
        )
        client.choose(choice)
        state = client.wait_for_state(timeout=10.0)
    return state


def _wait_for_play_resolution(client, choices=None):
    """Wait for a card play to fully resolve, handling intermediate screens.

    Some BG mod card effects produce intermediate choice screens
    (TargetSelectScreen for Havoc auto-play, Juggernaut damage target,
    DoubleTap follow-up cards, etc.).  This helper auto-handles "choose"
    screens and returns once the game is back in normal combat or no more
    state updates are coming (e.g. confirm screen waiting for caller).

    ``choices`` is an optional list of explicit choice indices for known
    choice screens.  Any additional intermediate choice screens beyond the
    explicit list default to choosing index 0 (first/only option).
    """
    choices = list(choices) if choices else []
    choice_idx = 0
    state = None
    # After sending a choose command, we expect a response soon (10s).
    # After an unrecognized state with no command sent, use a short timeout
    # to detect that no more updates are coming (e.g. confirm screen).
    next_timeout = 10.0

    for _ in range(30):
        try:
            state = client.wait_for_state(timeout=next_timeout)
        except (TimeoutError, OSError):
            return state  # No more state updates — return what we have

        cmds = client.last_raw.get("available_commands", [])

        # Back to normal combat — we're done
        if client.ready_for_command and ("play" in cmds or "end" in cmds):
            return state

        # Auto-handle choice screens (TargetSelectScreen, card selection, etc.)
        screen_name = state.screen_type.value if state and state.screen_type else None
        if "choose" in cmds:
            if choice_idx < len(choices):
                client.choose(choices[choice_idx])
                choice_idx += 1
                next_timeout = 10.0
                continue
            elif screen_name == "HAND_SELECT":
                # HAND_SELECT with anyNumber: choose(0) to select a card,
                # then the confirm/key-confirm flow handles finalization.
                client.choose(0)
                next_timeout = 10.0
                continue
            elif "confirm" in cmds or "proceed" in cmds:
                # Non-HAND_SELECT optional screen (scry, etc.) — confirm to skip.
                client.send_command("confirm" if "confirm" in cmds else "proceed")
                next_timeout = 10.0
                continue
            else:
                # Mandatory choice — pick first option
                client.choose(0)
                next_timeout = 10.0
                continue

        # Confirm/proceed screens (no choose available)
        if "confirm" in cmds or "proceed" in cmds:
            client.send_command("confirm" if "confirm" in cmds else "proceed")
            next_timeout = 10.0
            continue

        # HAND_SELECT screen stuck after choose — the game selected the
        # card but the confirm button isn't visible to CommunicationMod.
        # Sending "key confirm" bypasses the button state check and
        # presses the confirm key directly.
        if state and state.screen_type and state.screen_type.value == "HAND_SELECT":
            client.send_command("key confirm")
            next_timeout = 10.0
            continue

        # Unrecognized state — request fresh state in case game finished
        # processing but didn't proactively send an update.
        client.request_state()
        next_timeout = 3.0

    return state


def set_scenario(client, *,
                 hand=None,
                 draw_pile=None,
                 discard_pile=None,
                 energy=3,
                 player_hp=9,
                 player_block=0,
                 player_powers=None,
                 player_relics=None,
                 orbs=None,
                 monster_hp=8,
                 monster_block=0,
                 monster_powers=None,
                 monsters=None):
    """Configure exact game state via the set command.

    Modifies existing monsters in-place (no encounter replacement, as the
    BG mod reverts encounter changes on the next action). Sets player stats,
    hand, draw/discard piles, and monster[0] stats.

    Use ``monsters`` (list of dicts with hp/block/powers keys) to configure
    multiple monsters.  When omitted the single-monster ``monster_hp`` /
    ``monster_block`` / ``monster_powers`` params are used for monster[0].

    Returns the GameState after the set command is applied.
    """
    # Dismiss any leftover overlay screens from a previous test failure
    _dismiss_blocking_screens(client)

    hand = hand or []
    draw_pile = draw_pile or []
    discard_pile = discard_pile or []

    # Build player section
    player_section = {
        "current_hp": player_hp,
        "max_hp": 9,
        "energy": energy,
        "block": player_block,
        "max_orbs": 3,  # Ensure orb slots exist for Defect cards
        "hand": [_card_spec_to_bg(c) for c in hand],
        "draw_pile": [_card_spec_to_bg(c) for c in draw_pile],
        "discard_pile": [_card_spec_to_bg(c) for c in discard_pile],
        "exhaust_pile": [],
        "powers": player_powers or {},
    }
    if orbs is not None:
        player_section["orbs"] = orbs

    # Build monster section
    if monsters is not None:
        monster_section = []
        for i, m in enumerate(monsters):
            monster_section.append({
                "index": i,
                "current_hp": m.get("hp", 30),
                "max_hp": m.get("hp", 30),
                "block": m.get("block", 0),
                "powers": m.get("powers") or {},
            })
    else:
        monster_section = [{
            "index": 0,
            "current_hp": monster_hp,
            "max_hp": monster_hp,
            "block": monster_block,
            "powers": monster_powers or {},
        }]

    # Build relic list — always include TheDie relic
    bg_relics = ["BoardGame:BGTheDieRelic"]
    if player_relics is not None:
        bg_relics.extend(RELIC_TO_BG[r] for r in player_relics)
    else:
        # Default: keep BurningBlood (Ironclad starter)
        bg_relics.append(RELIC_TO_BG[sts_sim.Relic.BurningBlood])

    payload = {
        "clear_turn": True,  # Reset cardsPlayedThisTurn to prevent accumulated state
        "relics": bg_relics,
        "player": player_section,
        "monsters": monster_section,
        "die": 1,  # Safe roll (1-3) — avoids die relic granting block on card play
    }

    _drain(client)
    client.set_state(payload)
    # The set command triggers a state update from CommunicationMod.
    # Read until ready_for_command is True (all actions resolved).
    state = None
    for _ in range(20):
        state = client.wait_for_state(timeout=10.0)
        if client.ready_for_command:
            break
        time.sleep(0.1)
    return state


def make_sim(*, hand=None, draw_pile=None, discard_pile=None,
             energy=3, player_hp=9, player_block=0,
             player_powers=None, player_relics=None, orbs=None,
             monster_hp=8, monster_block=0, monster_powers=None,
             monsters=None):
    """Create a simulator CombatState matching the game scenario.

    Use ``monsters`` (list of dicts with hp/block/powers keys) to configure
    multiple monsters.  When omitted the single-monster ``monster_hp`` /
    ``monster_block`` / ``monster_powers`` params are used.

    Returns the CombatState ready for play_card().
    """
    hand = hand or []
    draw_pile = draw_pile or []
    discard_pile = discard_pile or []

    if monsters is not None:
        monster_list = []
        for i, m in enumerate(monsters):
            mon = sts_sim.Monster(f"Monster_{i}", m.get("hp", 30), "jaw_worm", "A", False)
            blk = m.get("block", 0)
            if blk > 0:
                mon.add_block(blk)
            if m.get("powers"):
                for power_name, amount in m["powers"].items():
                    pt = getattr(sts_sim.PowerType, power_name)
                    mon.apply_power(pt, amount)
            monster_list.append(mon)
    else:
        monster = sts_sim.Monster("Jaw Worm", monster_hp, "jaw_worm", "A", False)
        if monster_block > 0:
            monster.add_block(monster_block)
        if monster_powers:
            for power_name, amount in monster_powers.items():
                pt = getattr(sts_sim.PowerType, power_name)
                monster.apply_power(pt, amount)
        monster_list = [monster]

    sim = sts_sim.CombatState.new_with_character(
        monster_list, seed=0, character=sts_sim.Character.Ironclad,
    )
    sim.set_player_energy(energy)
    sim.set_player_max_hp(9)  # Match live game max_hp default
    sim.set_player_hp(player_hp)
    sim.set_player_block(player_block)

    if player_relics is not None:
        sim.clear_relics()
        for relic in player_relics:
            sim.add_relic(relic)

    if player_powers:
        for power_name, amount in player_powers.items():
            pt = getattr(sts_sim.PowerType, power_name)
            sim.apply_player_power(pt, amount)

    # Set up orb slots and channel orbs
    sim.set_orb_slots(3)  # Always ensure orb slots exist
    if orbs:
        for orb_name in orbs:
            orb_type = getattr(sts_sim.OrbType, orb_name)
            sim.channel_orb_type(orb_type)

    for card_spec in draw_pile:
        card = _card_spec_card(card_spec)
        if _card_spec_upgraded(card_spec):
            sim.add_upgraded_card_to_draw(card)
        else:
            sim.add_card_to_draw(card)

    for card_spec in discard_pile:
        card = _card_spec_card(card_spec)
        if _card_spec_upgraded(card_spec):
            sim.add_upgraded_card_to_discard(card)
        else:
            sim.add_card_to_discard(card)

    for card_spec in hand:
        card = _card_spec_card(card_spec)
        if _card_spec_upgraded(card_spec):
            sim.add_upgraded_card_to_hand(card)
        else:
            sim.add_card_to_hand(card)

    # Lock die to 1 to match the live game's set_scenario die=1
    sim.set_die_value(1)

    return sim


def play_card_both(client, sim, hand_index, target_index=None, choices=None):
    """Play a card in both the live game and the simulator.

    Waits for all actions to resolve (including BG mod intermediate
    screens like TargetSelectScreen) before returning.

    Returns the new GameState from the live game.
    """
    client.play_card(hand_index, target_index=target_index)
    game_state = _wait_for_play_resolution(client, choices)

    sim_choice = choices[0] if choices else None
    sim.play_card(hand_index, target_index, sim_choice)

    return game_state


def play_named_card(client, sim, setup_state, card, target_index=None,
                    choices=None, upgraded=False):
    """Play a card by Card enum in both game and simulator.

    Finds the correct hand index in both the live game and simulator
    to handle potential hand reordering. Waits for full resolution.
    Returns the new GameState.
    """
    bg_id = CARD_TO_BG[card]

    # Find in live hand (upgraded cards keep same BG ID)
    live_idx = None
    for i, c in enumerate(setup_state.combat_state.hand):
        if c.card_id == bg_id:
            live_idx = i
            break
    assert live_idx is not None, f"Card {bg_id} not found in live hand"

    # Find in sim hand — match card AND upgraded flag
    sim_idx = None
    for i, ci in enumerate(sim.get_hand()):
        if ci.card == card and ci.upgraded == upgraded:
            sim_idx = i
            break
    assert sim_idx is not None, f"Card {card} (upgraded={upgraded}) not found in sim hand"

    client.play_card(live_idx, target_index=target_index)
    game_state = _wait_for_play_resolution(client, choices)

    # Pass first choice to the sim (if any) for cards like WishCard
    sim_choice = choices[0] if choices else None
    sim.play_card(sim_idx, target_index, sim_choice)

    return game_state


def assert_monsters_match(game_state, sim):
    """Assert that monster[0] HP and block match between game and simulator."""
    live_monsters = [m for m in game_state.combat_state.monsters if not m.is_gone]
    sim_monsters = sim.get_monsters()

    assert len(live_monsters) >= 1, "No live monsters in game"
    assert len(sim_monsters) >= 1, "No monsters in simulator"

    # Compare only monster[0] — the one we configured via set_scenario
    lm = live_monsters[0]
    sm = sim_monsters[0]
    assert lm.current_hp == sm.hp, (
        f"Monster[0] HP mismatch: live={lm.current_hp}, sim={sm.hp}"
    )
    assert lm.block == sm.block, (
        f"Monster[0] block mismatch: live={lm.block}, sim={sm.block}"
    )


def assert_player_matches(game_state, sim):
    """Assert that player HP, block, and energy match."""
    lp = game_state.combat_state.player
    sp = sim.player

    assert lp.current_hp == sp.hp, (
        f"Player HP mismatch: live={lp.current_hp}, sim={sp.hp}"
    )
    assert lp.block == sp.block, (
        f"Player block mismatch: live={lp.block}, sim={sp.block}"
    )
    assert lp.energy == sp.energy, (
        f"Player energy mismatch: live={lp.energy}, sim={sp.energy}"
    )


def assert_relics_match(game_state, sim):
    """Assert that player relics match (order-independent, ignoring TheDie)."""
    live_ids = sorted(
        r.relic_id for r in game_state.relics
        if r.relic_id != "BoardGame:BGTheDieRelic"
    )
    sim_ids = sorted(RELIC_TO_BG.get(r, f"?{r}") for r in sim.get_relics())
    assert live_ids == sim_ids, f"Relic mismatch:\n  live={live_ids}\n  sim ={sim_ids}"


# ---------------------------------------------------------------------------
# Card spec helpers — cards can be Card enum (unupgraded) or (Card, True) tuple
# ---------------------------------------------------------------------------

def _card_spec_to_bg(card_spec):
    """Convert a card spec to BG mod format for the set command."""
    if isinstance(card_spec, tuple):
        card, upgraded = card_spec
        if upgraded:
            return {"id": CARD_TO_BG[card], "upgraded": True}
        return CARD_TO_BG[card]
    return CARD_TO_BG[card_spec]

def _card_spec_card(card_spec):
    """Extract the Card enum from a card spec."""
    if isinstance(card_spec, tuple):
        return card_spec[0]
    return card_spec

def _card_spec_upgraded(card_spec):
    """Extract the upgraded flag from a card spec."""
    if isinstance(card_spec, tuple):
        return card_spec[1]
    return False


# Reverse mapping: BG card ID -> simulator Card enum
BG_TO_CARD = {v: k for k, v in CARD_TO_BG.items()}


def _pile_card_ids(live_cards):
    """Extract sorted card_id list from live game Card objects."""
    return sorted(c.card_id for c in live_cards)


def _sim_pile_card_ids(sim_cards):
    """Extract sorted BG card IDs from simulator CardInstance objects."""
    return sorted(CARD_TO_BG.get(c.card, f"?{c.card}") for c in sim_cards)


def assert_hand_matches(game_state, sim):
    """Assert that hand contents match (order-independent)."""
    live = _pile_card_ids(game_state.combat_state.hand)
    sim_ids = _sim_pile_card_ids(sim.get_hand())
    assert live == sim_ids, f"Hand mismatch:\n  live={live}\n  sim ={sim_ids}"


def assert_draw_pile_matches(game_state, sim):
    """Assert that draw pile contents match (order-independent)."""
    live = _pile_card_ids(game_state.combat_state.draw_pile)
    sim_ids = _sim_pile_card_ids(sim.get_draw_pile())
    assert live == sim_ids, f"Draw pile mismatch:\n  live={live}\n  sim ={sim_ids}"


def assert_discard_matches(game_state, sim):
    """Assert that discard pile contents match (order-independent)."""
    live = _pile_card_ids(game_state.combat_state.discard_pile)
    sim_ids = _sim_pile_card_ids(sim.get_discard_pile())
    assert live == sim_ids, f"Discard mismatch:\n  live={live}\n  sim ={sim_ids}"


def assert_exhaust_matches(game_state, sim):
    """Assert that exhaust pile contents match (order-independent)."""
    live = _pile_card_ids(game_state.combat_state.exhaust_pile)
    sim_ids = _sim_pile_card_ids(sim.get_exhaust_pile())
    assert live == sim_ids, f"Exhaust mismatch:\n  live={live}\n  sim ={sim_ids}"
