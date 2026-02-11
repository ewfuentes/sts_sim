# Tests that cannot be live tests (require multi-turn, end_player_turn, or special mechanics)

## Silent Uncommon

### Backstab — Damaged enemy (non-full HP)
- **Test: Backstab against damaged enemy (no bonus)** — Requires the enemy to have taken damage prior to playing Backstab. The set_scenario sets monster_hp = max_hp, so the enemy is always at "full HP" from the game's perspective. Would need a way to set current_hp < max_hp that the BG mod recognizes as "damaged".

### Masterful Stab — Reduced cost after HP loss
- **Test: Masterful Stab at reduced cost (HP lost this combat)** — Requires the player to have lost HP this combat. The "lost HP" flag is tracked internally and cannot be set via set_scenario alone. Multi-turn or enemy attack required.
- **Test: Upgraded Masterful Stab after losing HP** — Same issue, requires HP loss tracking.

### Finisher — After playing attacks (multi-card sequence with SHIV)
- **Test: Upgraded Finisher after 2 attacks and 1 SHIV** — Requires SHIV usage counting as an "attack played this turn". SHIV tokens are consumed via a separate mechanism, not standard card play. Complex interaction.

### All-Out Attack — Reflex interaction
- **Test: All-Out Attack triggers Reflex on discard** — Requires specific discard targeting (choosing to discard Reflex specifically). The live game's discard selection UI may auto-select or have a choice screen that needs careful handling.

### Unload — SHIV interaction
- **Test: Unload with 3 SHIVs** — Requires SHIV tokens to be present (player_powers Shiv). The SHIV consumption during Unload involves multiple separate attacks and targeting choices per SHIV.
- **Test: Upgraded Unload with 2 SHIVs** — Same SHIV consumption complexity.

### Blur — After discarding a card
- **Test: Blur after discarding a card this turn** — Requires playing a discard-triggering card first (e.g., Survivor) before Blur. Multi-card sequence with discard state tracking.
- **Test: Upgraded Blur after discarding with Footwork** — Same discard tracking + Footwork power interaction.

### Bouncing Flask — Split POISON across enemies
- **Test: Bouncing Flask — split POISON across enemies** — Requires multiple choice screens to assign each POISON to a different target. Complex choice handling.
- **Test: Upgraded Bouncing Flask — 3 POISON distributed** — Same, with 3 choice screens.

### Concentrate — Discard choice
- **Test: Concentrate — discard 2 cards for 2 energy** — Requires HAND_SELECT screen to choose which cards to discard. Complex choice handling with anyNumber selection.
- **Test: Concentrate — discard 0 cards** — Requires confirming with 0 cards selected on HAND_SELECT.
- **Test: Upgraded Concentrate — discard 3 cards for 4 energy** — Same HAND_SELECT complexity.

### Calculated Gamble — Reflex interaction
- **Test: Calculated Gamble triggers Reflex in hand** — Requires Reflex to be in hand when Calculated Gamble discards. The Reflex trigger draws additional cards, creating complex state.

### Crippling Cloud — Distraction interaction
- **Test: Crippling Cloud triggers Distraction** — Requires Distraction power to be active (play Distraction first, then Crippling Cloud). Multi-card sequence with power interaction.

### Outmaneuver — Multi-turn retain mechanic
- **Test: Outmaneuver retained and played next turn** — Requires ending the turn (Outmaneuver is retained), then starting a new turn and playing it. Multi-turn.
- **Test: Upgraded Outmaneuver retained and played** — Same multi-turn requirement.

### Piercing Wail — Footwork interaction
- **Test: Piercing Wail with Footwork** — Requires Footwork power active. Could be done by setting player_powers Dexterity, but the single-enemy scenario already tests this.

### Footwork — Upgraded retain
- **Test: Upgraded Footwork has Retain** — Requires ending the turn and verifying the card is retained in hand. Multi-turn.

### Noxious Fumes — Multi-turn poison application
- **Test: Noxious Fumes applies POISON each turn** — Requires ending the turn and starting the next to see the POISON application. Multi-turn.
- **Test: Noxious Fumes accumulates over multiple turns** — Requires 2+ turn cycles. Multi-turn.
- **Test: Upgraded Noxious Fumes — AOE POISON** — Same multi-turn requirement.

### Well-Laid Plans — End of turn retain
- **Test: Well-Laid Plans — retain 1 card at end of turn** — Requires ending the turn with Well-Laid Plans active and selecting a card to retain. Multi-turn with choice screen.
- **Test: Upgraded Well-Laid Plans — retain 2 cards** — Same, with 2 card selections.
- **Test: Well-Laid Plans — choose not to retain** — Requires ending the turn and declining the retain. Multi-turn.

### Distraction — Token trigger interaction
- **Test: Distraction triggers on applying POISON** — Requires playing Distraction power first, then a POISON card. Multi-card sequence.
- **Test: Distraction triggers only once per turn** — Requires playing 2 POISON cards with Distraction active. Multi-card sequence.

### Infinite Blades — Multi-turn SHIV generation
- **Test: Infinite Blades grants SHIV at start of turn** — Requires ending the turn and starting the next. Multi-turn.
- **Test: Upgraded Infinite Blades grants 2 SHIVs** — Same multi-turn.
- **Test: Infinite Blades accumulates SHIVs over turns** — Requires 2+ turn cycles. Multi-turn.

### Reflex — End of turn non-trigger
- **Test: Reflex does NOT trigger at end of turn discard** — Requires ending the turn with Reflex in hand and verifying no draw. Multi-turn.
- **Test: Upgraded Reflex draws 3 cards on discard** — Requires discarding via Concentrate's HAND_SELECT. Complex choice handling.

### Tactician — End of turn non-trigger
- **Test: Tactician does NOT trigger at end of turn** — Requires ending the turn with Tactician in hand. Multi-turn.
- **Test: Upgraded Tactician grants 3 energy** — Requires Concentrate's HAND_SELECT to discard Tactician+. Complex choice handling.

## Silent Rare

### Grand Finale — Unplayable with cards in draw pile
- **Test: Grand Finale with cards in draw pile (unplayable)** — Requires verifying the card cannot be played. The live game prevents playing it, but assertion of "could not play" is not straightforward.

### Bullet Time — Draw block interaction
- **Test: Bullet Time blocks draw effects** — Requires playing Bullet Time then Predator in sequence and verifying no draws. Multi-card sequence with draw prevention.

### Storm of Steel — Discard choice and Reflex
- **Test: Storm of Steel — discard 3 cards** — Requires HAND_SELECT screen to choose which cards to discard. Complex choice handling.
- **Test: Storm of Steel — discard 0 cards** — Requires confirming with 0 cards on HAND_SELECT.
- **Test: Upgraded Storm of Steel — discard 2 cards** — Same HAND_SELECT complexity.
- **Test: Storm of Steel triggers Reflex on discard** — Requires discarding Reflex specifically via HAND_SELECT. Complex interaction.

### Doppelganger — Copy last card played
- **Test: Doppelganger copies an Attack** — Requires an ally to have played a card this turn. Ally mechanics are not available in single-player live tests.
- **Test: Doppelganger copies a multi-HIT Attack** — Same, requires card copy mechanics.
- **Test: Upgraded Doppelganger does not exhaust** — Same ally/copy mechanics issue.

### Corpse Explosion — Death trigger
- **Test: Corpse Explosion triggers on enemy death** — Requires the enemy to die after Corpse Explosion is attached. Killing the last enemy ends combat, making post-assertion impossible.

### A Thousand Cuts — Shuffle trigger
- **Test: A Thousand Cuts triggers on draw pile shuffle** — Requires drawing enough cards to trigger a shuffle. Multi-turn or complex draw sequence.
- **Test: Upgraded A Thousand Cuts — increased damage** — Same shuffle-trigger issue.
- **Test: A Thousand Cuts triggers multiple times per turn** — Requires 2 shuffles in one turn. Very complex.

### Burst — Multi-card sequence
- **Test: Burst only affects the next Skill** — Requires playing Burst + Defend + Blur (3 cards). Multi-card sequence doable but complex.

### Envenom — Multi-HIT and SHIV interaction
- **Test: Envenom with multi-HIT attack** — Requires Envenom power active, then playing Die Die Die. Multi-card or power-preset sequence.
- **Test: Envenom applies to SHIVs** — Requires Envenom power active + SHIV token usage. Complex interaction.

### Tools of the Trade — Start of turn effect
- **Test: Tools of the Trade — draw then discard at start of turn** — Requires ending the turn and starting the next. Multi-turn.
- **Test: Tools of the Trade triggers Reflex on discard** — Multi-turn + Reflex trigger interaction.

### Wraith Form — Multi-round mechanics
- **Test: Wraith Form caps HP loss at 1 per round** — Requires enemy attack after playing Wraith Form. Multi-turn.
- **Test: Wraith Form exhausts after 2 rounds** — Requires 2 full round cycles. Multi-turn.
- **Test: Upgraded Wraith Form lasts 3 rounds** — Requires 3 full round cycles. Multi-turn.
- **Test: Wraith Form with multiple damage sources in one round** — Requires multiple enemies attacking. Multi-turn.
