# STS Board Game Simulator — Implementation State

## Status
- Step 0: Done — permissions added to `.claude/settings.json`
- Steps 1-9: Not started

## Next Action
Run these commands to scaffold the project:
```bash
which uv && uv --version
which maturin || uv tool install maturin
```
Then proceed with Step 1 below.

---

## Implementation Steps

### Step 1: Project scaffolding
- `uv init` the project (or manually create pyproject.toml)
- Set up `Cargo.toml` with pyo3 + maturin
- Set up `pyproject.toml` with maturin build backend, pytest dev dependency
- Create `src/lib.rs` with a minimal PyO3 module
- Verify: `uv run maturin develop && uv run python -c "import sts_sim"`

### Step 2: Core types (`enums.rs`, `creature.rs`)
### Step 3: Die mechanic (`die.rs`)
### Step 4: Power system (`powers.rs`)
### Step 5: Damage pipeline (`damage.rs`)
### Step 6: Cards (`cards.rs`)
### Step 7: Enemies (`enemies/`)
### Step 8: Combat engine (`combat.rs`)
### Step 9: PyO3 bindings (`lib.rs`) + verification

---

## Exact Mechanics from Mod Source (Difficulty 0 / Easy)

### Ironclad
- 10 HP / 10 max HP, 5 gold, 3 energy/turn, draw 5 cards/turn
- Block cap: 20
- Starter deck: 5x Strike (1 dmg, 1 cost), 4x Defend (1 block, 1 cost), 1x Bash (2 dmg + 1 Vulnerable, 2 cost)
- Starting relics: BGTheDieRelic, BGBurningBlood (heal 1 HP at end of combat)

### Die
- d6: rolls 1-6
- Behavior index: rolls 1-2 → index 0, 3-4 → index 1, 5-6 → index 2

### Jaw Worm (difficulty 0)
- 8 HP, die-controlled, behavior "sda"
- Bellow (s): +1 Str, +2 block — intent DEFEND_BUFF
- Thrash (d): 2 dmg, +1 block — intent ATTACK_DEFEND
- Chomp (a): 3 dmg — intent ATTACK

### Cultist
- 9 HP, NOT die-controlled
- Pre-battle: applies 1 Ritual
- Turn 1: Incantation — 1 dmg + manually applies +1 Str to self
- Turn 2+: Dark Strike — 1 dmg (base, but Ritual fires before move adding Str each turn from turn 2 onward)
- Note: Ritual fires at start of monster turn, but NOT on turn 1 for Cultist (the Incantation manually adds +1 Str instead)

### Red Louse (easy, hard=false)
- 3 HP, die-controlled, behavior "S21"
- Pre-battle: 2 Curl Up
- Strengthen (S): +1 Str — intent BUFF
- Bite 1 (1): 1 dmg — intent ATTACK
- Bite 2 (2): 2 dmg — intent ATTACK

### Green Louse
- 3 HP, die-controlled, behavior from pool ("1W2" or "21W")
- Pre-battle: 2 Curl Up
- Weaken (W): apply 1 Weak to player — intent DEBUFF
- Bite 1 (1): 1 dmg — intent ATTACK
- Bite 2 (2): 2 dmg — intent ATTACK

### Damage Pipeline (AbstractBGMonster.getCalculateDamage)
1. Start with base_damage (int)
2. Convert to float
3. Monster powers: atDamageGive(damage, NORMAL) — Weak applies here
4. Player powers: atDamageReceive(damage, NORMAL) — Vulnerable applies here
5. (Stance — skip for now)
6. Monster powers: atDamageFinalGive — (not needed for first fight)
7. Player powers: atDamageFinalReceive — (not needed for first fight)
8. Floor to int, minimum 0

### Weak (BGWeakPower)
- Cap: 3 stacks
- atDamageGive: if attacker weak AND target vulnerable → damage × 0.5; else → damage - 1
- Player weak: decays by 1 after playing an ATTACK card (onAfterUseCard)
- Monster weak: decays by 1 during monster turn if monster has attack intent (getIntentBaseDmg >= 0)

### Vulnerable (BGVulnerablePower)
- Cap: 3 stacks (4 with VulnerableProcced)
- atDamageReceive: if attacker weak AND target vuln → damage + 1; else → damage × 2
- Only applies if effective index < vuln stacks
- Consumed by attacks (tracked via BGVulnerableProccedPower)
- Player vuln: each attacking monster decays vuln by 1 at end of turn

### Curl Up
- When hit by single-target attack with damage > 0 AND damage < currentHealth (non-lethal):
  - Grants 2 block
  - Then removes itself
- Does NOT trigger on lethal damage

### Ritual
- Grants Strength equal to amount at start of each monster turn
- For Cultist: does NOT fire on turn 1 (Incantation manually adds Str instead)

### Combat Flow
1. Pre-battle: apply Ritual (Cultist), Curl Up (Lice)
2. Player turn: reset block → gain energy → draw cards → play cards → end turn
3. Die roll (d6)
4. Monster turns: each monster — Ritual fires → reset block → execute move → Weak decays on monster → player Vuln decays per attacker
5. Check win/loss → if won, Burning Blood heals 1 HP
6. Repeat from step 2

### Encounters (first fight)
- Jaw Worm solo
- Cultist solo
- 2x Louse (1 Red + 1 Green)

---

## Project Structure

```
/data/code/sts_bot_2/
├── pyproject.toml              # uv project config + maturin build backend
├── Cargo.toml                  # Rust workspace (maturin)
├── src/
│   ├── lib.rs                  # PyO3 module entry point
│   ├── enums.rs                # CardType, Intent, PowerType enums
│   ├── creature.rs             # Player/Monster structs
│   ├── powers.rs               # Power stacking, caps, hooks
│   ├── damage.rs               # Damage calculation pipeline
│   ├── cards.rs                # Card definitions (Strike, Defend, Bash)
│   ├── die.rs                  # TheDie d6 mechanic
│   ├── enemies/
│   │   ├── mod.rs
│   │   ├── jaw_worm.rs
│   │   ├── cultist.rs
│   │   ├── red_louse.rs
│   │   └── green_louse.rs
│   ├── encounters.rs           # First-fight encounter factories
│   └── combat.rs               # CombatState + CombatEngine
├── tests/                      # Python tests (pytest)
│   ├── conftest.py
│   ├── test_die.py
│   ├── test_damage.py
│   ├── test_powers.py
│   ├── test_cards.py
│   ├── test_enemies.py
│   └── test_combat.py
├── CLAUDE.md
└── .claude/settings.json
```

## Key Source Files for Reference
- `~/code/StSBoardGameMod/src/main/java/BoardGame/monsters/bgexordium/BGJawWorm.java`
- `~/code/StSBoardGameMod/src/main/java/BoardGame/monsters/bgexordium/BGCultist.java`
- `~/code/StSBoardGameMod/src/main/java/BoardGame/monsters/bgexordium/BGRedLouse.java`
- `~/code/StSBoardGameMod/src/main/java/BoardGame/monsters/bgexordium/BGGreenLouse.java`
- `~/code/StSBoardGameMod/src/main/java/BoardGame/powers/BGVulnerablePower.java`
- `~/code/StSBoardGameMod/src/main/java/BoardGame/powers/BGWeakPower.java`
- `~/code/StSBoardGameMod/src/main/java/BoardGame/characters/BGIronclad.java`
- `~/code/StSBoardGameMod/src/main/java/BoardGame/thedie/TheDie.java`
- `~/code/StSBoardGameMod/src/main/java/BoardGame/monsters/AbstractBGMonster.java`
