# Silent (BGGreen) — Rare

- **Die Die Die** [Y] — BGDieDieDie — Attack, Rare, Cost 1
  AOE 3 HIT. Exhaust.
  *Upgrade: AOE 4 HIT. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic Die Die Die — AOE damage**
  Setup: Player has Die Die Die in hand, 3 energy. Two enemies: Enemy A at 20 HP, Enemy B at 15 HP, both 0 block.
  Actions: Play Die Die Die.
  Expected: Both enemies take 3 damage each. Die Die Die is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Die Die Die**
  Setup: Player has Die Die Die+ in hand, 3 energy. Two enemies: Enemy A at 20 HP, Enemy B at 15 HP, both 0 block.
  Actions: Play Die Die Die+.
  Expected: Both enemies take 4 damage each. Die Die Die+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Die Die Die with Strength**
  Setup: Player has Die Die Die in hand, 2 STR, 3 energy. Two enemies: Enemy A at 20 HP, Enemy B at 15 HP, both 0 block.
  Actions: Play Die Die Die.
  Expected: Both enemies take 3*(1+2) = 9 damage each (3 HIT at 3 damage each with STR). Die Die Die is exhausted.

- **Grand Finale** [Y] — BGGrandFinale — Attack, Rare, Cost 0
  Can only be played if there are no cards in your draw pile. AOE 10 HIT.
  *Upgrade: AOE 12 HIT.*

  - [ ] Sim - [ ] Live — **Test: Grand Finale with empty draw pile**
  Setup: Player has Grand Finale in hand, 3 energy. Draw pile has 0 cards. Two enemies: Enemy A at 20 HP, Enemy B at 15 HP.
  Actions: Play Grand Finale.
  Expected: Both enemies take 10 damage each. Enemy A at 10 HP, Enemy B at 5 HP.

  - [ ] Sim - [ ] Live — **Test: Grand Finale with cards in draw pile (unplayable)**
  Setup: Player has Grand Finale in hand, 3 energy. Draw pile has 3 cards.
  Actions: Attempt to play Grand Finale.
  Expected: Grand Finale cannot be played (draw pile is not empty).

  - [ ] Sim - [ ] Live — **Test: Upgraded Grand Finale with empty draw pile**
  Setup: Player has Grand Finale+ in hand, 3 energy. Draw pile has 0 cards. Two enemies at 20 HP each.
  Actions: Play Grand Finale+.
  Expected: Both enemies take 12 damage each. Each enemy at 8 HP.

  - [ ] Sim - [ ] Live — **Test: Grand Finale with Strength and empty draw pile**
  Setup: Player has Grand Finale in hand, 1 STR, 3 energy. Draw pile has 0 cards. Enemy at 30 HP.
  Actions: Play Grand Finale.
  Expected: Enemy takes 10*(1+1) = 20 damage (10 HIT at 2 damage each with STR). Enemy at 10 HP.

- **Skewer** [Y] — BGSkewer — Attack, Rare, Cost -1
  Deal 1 HIT X+1 times.
  *Upgrade: Deal 2 HIT X times.*

  - [ ] Sim - [ ] Live — **Test: Skewer with 3 energy (X=3)**
  Setup: Player has Skewer in hand, 3 energy. Enemy at 20 HP, 0 block.
  Actions: Play Skewer (X=3, costs 3 energy).
  Expected: Enemy takes 1*(3+1) = 4 damage (1 HIT repeated 4 times). Player at 0 energy.

  - [ ] Sim - [ ] Live — **Test: Skewer with 0 energy (X=0)**
  Setup: Player has Skewer in hand, 0 energy. Enemy at 20 HP, 0 block.
  Actions: Play Skewer (X=0, costs 0 energy).
  Expected: Enemy takes 1 damage (1 HIT repeated 0+1 = 1 time).

  - [ ] Sim - [ ] Live — **Test: Upgraded Skewer with 3 energy (X=3)**
  Setup: Player has Skewer+ in hand, 3 energy. Enemy at 20 HP, 0 block.
  Actions: Play Skewer+ (X=3, costs 3 energy).
  Expected: Enemy takes 2*3 = 6 damage (2 HIT repeated 3 times). Player at 0 energy.

  - [ ] Sim - [ ] Live — **Test: Skewer with Strength**
  Setup: Player has Skewer in hand, 2 STR, 2 energy. Enemy at 20 HP, 0 block.
  Actions: Play Skewer (X=2, costs 2 energy).
  Expected: Enemy takes (1+2)*(2+1) = 9 damage (each HIT deals 3 with STR, repeated 3 times).

- **Adrenaline** [Y] — BGAdrenaline — Skill, Rare, Cost 0
  Gain Energy(G) Energy(G). Draw 2 cards. Exhaust.
  *Upgrade: Additional draw or energy.*

  - [ ] Sim - [ ] Live — **Test: Basic Adrenaline**
  Setup: Player has Adrenaline in hand, 0 energy. Draw pile has 5 cards.
  Actions: Play Adrenaline.
  Expected: Player gains 2 energy. Player draws 2 cards. Adrenaline is exhausted.

  - [ ] Sim - [ ] Live — **Test: Adrenaline as turn starter**
  Setup: Player has Adrenaline in hand, 3 energy. Draw pile has 5 cards. Player has 2 other cards in hand.
  Actions: Play Adrenaline.
  Expected: Player gains 2 energy (now at 5 energy). Player draws 2 cards (now 4 cards in hand). Adrenaline is exhausted.

  - [ ] Sim - [ ] Live — **Test: Adrenaline with insufficient draw pile**
  Setup: Player has Adrenaline in hand, 1 energy. Draw pile has 1 card. Discard pile has 5 cards.
  Actions: Play Adrenaline.
  Expected: Player gains 2 energy (now at 3). Player draws 1 card from draw pile, then discard pile is shuffled into draw pile and player draws 1 more card. Adrenaline is exhausted.

- **Bullet Time** [Y] — BGBulletTime — Skill, Rare, Cost 3
  All cards cost 0 this turn. You can't draw additional cards this turn.
  *Upgrade: Cost 3 to 2.*

  - [ ] Sim - [ ] Live — **Test: Basic Bullet Time — cards cost 0**
  Setup: Player has Bullet Time and 3 other cards in hand (costs 1, 2, 1), 3 energy.
  Actions: Play Bullet Time.
  Expected: All remaining cards in hand now cost 0 for this turn. Player can't draw additional cards this turn. Player at 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Bullet Time — reduced cost**
  Setup: Player has Bullet Time+ and 3 other cards in hand (costs 2, 2, 1), 3 energy.
  Actions: Play Bullet Time+.
  Expected: Costs 2 energy (player at 1 energy). All remaining cards in hand cost 0. Player can't draw additional cards this turn.

  - [ ] Sim - [ ] Live — **Test: Bullet Time blocks draw effects**
  Setup: Player has Bullet Time and Predator (3 HIT, draw 2) in hand, 3 energy. Enemy at 20 HP. Draw pile has 5 cards.
  Actions: Play Bullet Time. Play Predator (now costs 0) targeting enemy.
  Expected: Enemy takes 3 damage. Draw 2 effect from Predator is prevented (can't draw additional cards this turn).

- **Malaise** [Y] — BGMalaise — Skill, Rare, Cost -1
  Apply WEAK POISON to an enemy X times. Exhaust.
  *Upgrade: Apply WEAK POISON to an enemy X+1 times. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Malaise with 3 energy (X=3)**
  Setup: Player has Malaise in hand, 3 energy. Enemy has 0 WEAK, 0 POISON.
  Actions: Play Malaise (X=3, costs 3 energy).
  Expected: Enemy gains 3 WEAK and 3 POISON. Malaise is exhausted. Player at 0 energy.

  - [ ] Sim - [ ] Live — **Test: Malaise with 1 energy (X=1)**
  Setup: Player has Malaise in hand, 1 energy. Enemy has 0 WEAK, 0 POISON.
  Actions: Play Malaise (X=1, costs 1 energy).
  Expected: Enemy gains 1 WEAK and 1 POISON. Malaise is exhausted. Player at 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Malaise with 2 energy (X=2, applies X+1=3 times)**
  Setup: Player has Malaise+ in hand, 2 energy. Enemy has 0 WEAK, 0 POISON.
  Actions: Play Malaise+ (X=2, costs 2 energy).
  Expected: Enemy gains 3 WEAK and 3 POISON (X+1 = 3 applications). Malaise+ is exhausted. Player at 0 energy.

- **Storm of Steel** [Y] — BGStormOfSteel — Skill, Rare, Cost 1
  Discard any number of cards. Gain SHIV for each card discarded.
  *Upgrade: Gain SHIV for each card discarded +1.*

  - [ ] Sim - [ ] Live — **Test: Storm of Steel — discard 3 cards**
  Setup: Player has Storm of Steel and 3 other cards in hand, 3 energy, 0 SHIV tokens.
  Actions: Play Storm of Steel. Discard 3 cards.
  Expected: Player gains 3 SHIV tokens. Hand is empty.

  - [ ] Sim - [ ] Live — **Test: Storm of Steel — discard 0 cards**
  Setup: Player has Storm of Steel in hand, 3 energy, 0 SHIV tokens.
  Actions: Play Storm of Steel. Discard 0 cards.
  Expected: Player gains 0 SHIV tokens.

  - [ ] Sim - [ ] Live — **Test: Upgraded Storm of Steel — discard 2 cards**
  Setup: Player has Storm of Steel+ and 2 other cards in hand, 3 energy, 0 SHIV tokens.
  Actions: Play Storm of Steel+. Discard 2 cards.
  Expected: Player gains 2 + 1 = 3 SHIV tokens (1 per discard +1 bonus).

  - [ ] Sim - [ ] Live — **Test: Storm of Steel triggers Reflex on discard**
  Setup: Player has Storm of Steel, Reflex, and 1 other card in hand, 3 energy. Draw pile has 5 cards.
  Actions: Play Storm of Steel. Discard Reflex and the other card.
  Expected: Player gains 2 SHIV tokens. Reflex triggers: player draws 2 cards.

- **Doppelganger** [Y] — BGDoppelganger — Skill, Rare, Cost -1
  Play a copy of the last Attack or Skill played by any player this turn with cost equal to X. Exhaust.
  *Upgrade: Play a copy of the last Attack or Skill played by any player this turn with cost equal to X. (No longer Exhausts.)*

  - [ ] Sim - [ ] Live — **Test: Doppelganger copies an Attack**
  Setup: Player has Doppelganger in hand, 3 energy. An ally played Strike (1 HIT) this turn. Enemy at 20 HP.
  Actions: Play Doppelganger (X=3, costs 3 energy).
  Expected: A copy of Strike is played. Enemy takes 1 damage. Doppelganger is exhausted. Player at 0 energy.

  - [ ] Sim - [ ] Live — **Test: Doppelganger copies a multi-HIT Attack**
  Setup: Player has Doppelganger in hand, 2 energy. Player played Die Die Die (AOE 3 HIT) earlier this turn. Two enemies at 20 HP each.
  Actions: Play Doppelganger (X=2, costs 2 energy).
  Expected: A copy of Die Die Die is played. Both enemies take 3 damage each. Doppelganger is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Doppelganger does not exhaust**
  Setup: Player has Doppelganger+ in hand, 1 energy. An ally played Defend (1 BLK) this turn.
  Actions: Play Doppelganger+ (X=1, costs 1 energy).
  Expected: A copy of Defend is played. Player gains 1 block. Doppelganger+ goes to discard pile (not exhausted).

- **Corpse Explosion** [Y] — BGCorpseExplosion — Skill, Rare, Cost 2
  POISON POISON. Attach to the target. When it dies, deal damage to its row and discard this card.
  *Upgrade: POISON POISON POISON.*

  - [ ] Sim - [ ] Live — **Test: Corpse Explosion — apply POISON and attach**
  Setup: Player has Corpse Explosion in hand, 3 energy. Enemy at 10 HP, 0 POISON.
  Actions: Play Corpse Explosion targeting enemy.
  Expected: Enemy gains 2 POISON. Corpse Explosion is attached to the enemy.

  - [ ] Sim - [ ] Live — **Test: Corpse Explosion triggers on enemy death**
  Setup: Corpse Explosion is attached to Enemy A (front row). Enemy A at 1 HP with 2 POISON. Enemy B is in the same row at 15 HP.
  Actions: Enemy A dies (from poison or damage).
  Expected: Damage is dealt to Enemy A's row (hitting Enemy B). Corpse Explosion is discarded.

  - [ ] Sim - [ ] Live — **Test: Upgraded Corpse Explosion — 3 POISON**
  Setup: Player has Corpse Explosion+ in hand, 3 energy. Enemy at 20 HP, 0 POISON.
  Actions: Play Corpse Explosion+ targeting enemy.
  Expected: Enemy gains 3 POISON. Corpse Explosion+ is attached to the enemy.

- **A Thousand Cuts** [Y] — BGAThousandCuts — Power, Rare, Cost 2
  Whenever you shuffle your draw pile, deal 5 damage to any row.
  *Upgrade: Deal 7 damage to any row.*

  - [ ] Sim - [ ] Live — **Test: A Thousand Cuts triggers on draw pile shuffle**
  Setup: Player has A Thousand Cuts in hand, 3 energy. Draw pile has 0 cards. Discard pile has 5 cards. Two enemies in front row at 20 HP each.
  Actions: Play A Thousand Cuts. Draw cards until draw pile is empty, triggering a shuffle.
  Expected: When discard pile is shuffled into draw pile, deal 5 damage to chosen row.

  - [ ] Sim - [ ] Live — **Test: Upgraded A Thousand Cuts — increased damage**
  Setup: A Thousand Cuts+ power is active. Draw pile has 0 cards. Discard pile has 5 cards.
  Actions: Trigger a draw pile shuffle.
  Expected: Deal 7 damage to chosen row.

  - [ ] Sim - [ ] Live — **Test: A Thousand Cuts triggers multiple times per turn**
  Setup: A Thousand Cuts power is active. Draw pile has 1 card. Discard pile has 3 cards. Player draws heavily causing 2 shuffles.
  Actions: Draw enough cards to trigger 2 shuffles in a single turn.
  Expected: A Thousand Cuts triggers twice, dealing 5 damage to a chosen row each time (10 total across 2 triggers).

- **Burst** [Y] — BGBurst — Power, Rare, Cost 1
  This turn, your next Skill is played twice. Burst can't be copied or 'played twice'.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Burst doubles next Skill**
  Setup: Player has Burst and Leg Sweep (WEAK, 3 BLK) in hand, 3 energy, 0 block. Enemy has 0 WEAK.
  Actions: Play Burst. Play Leg Sweep targeting enemy.
  Expected: Leg Sweep is played twice. Enemy gains 2 WEAK. Player gains 6 block. Player spent 1 + 2 = 3 energy.

  - [ ] Sim - [ ] Live — **Test: Burst only affects the next Skill**
  Setup: Player has Burst, Defend (1 BLK), and Blur (2 BLK) in hand, 3 energy, 0 block.
  Actions: Play Burst. Play Defend. Play Blur.
  Expected: Defend is played twice (2 block total from doubled Defend). Blur is played once normally (2 block). Total 4 block.

  - [ ] Sim - [ ] Live — **Test: Upgraded Burst costs 0**
  Setup: Player has Burst+ and Deadly Poison (POISON) in hand, 3 energy. Enemy has 0 POISON.
  Actions: Play Burst+ (costs 0). Play Deadly Poison targeting enemy.
  Expected: Player at 2 energy (only Deadly Poison costs 1). Enemy gains 2 POISON (Deadly Poison played twice from Burst).

  - [ ] Sim - [ ] Live — **Test: Burst does not double Attacks**
  Setup: Player has Burst and Strike (1 HIT) in hand, 3 energy. Enemy at 20 HP.
  Actions: Play Burst. Play Strike targeting enemy.
  Expected: Strike is played once (Burst only doubles Skills, not Attacks). Enemy takes 1 damage.

- **Envenom** [Y] — BGEnvenom — Power, Rare, Cost 3
  Your HIT also apply POISON. (Include SHIV.)
  *Upgrade: Cost 3 to 2.*

  - [ ] Sim - [ ] Live — **Test: Envenom adds POISON to HIT attacks**
  Setup: Player has Envenom and Strike (1 HIT) in hand, 4 energy. Enemy has 0 POISON, 20 HP.
  Actions: Play Envenom. Play Strike targeting enemy.
  Expected: Enemy takes 1 damage and gains 1 POISON (each HIT also applies POISON).

  - [ ] Sim - [ ] Live — **Test: Envenom with multi-HIT attack**
  Setup: Envenom power is active. Player has Die Die Die (AOE 3 HIT) in hand, 1 energy. Enemy has 0 POISON, 20 HP.
  Actions: Play Die Die Die targeting enemy.
  Expected: Enemy takes 3 damage and gains 3 POISON (1 POISON per HIT).

  - [ ] Sim - [ ] Live — **Test: Envenom applies to SHIVs**
  Setup: Envenom power is active. Player has 2 SHIV tokens, 3 energy. Enemy has 0 POISON, 20 HP.
  Actions: Use 1 SHIV targeting enemy.
  Expected: Enemy takes 1 damage and gains 1 POISON (SHIV counts as HIT, Envenom applies).

  - [ ] Sim - [ ] Live — **Test: Upgraded Envenom costs less**
  Setup: Player has Envenom+ in hand, 2 energy.
  Actions: Play Envenom+.
  Expected: Costs 2 energy (reduced from 3). Envenom power is now active. Player at 0 energy.

- **Tools of the Trade** [Y] — BGToolsOfTheTrade — Power, Rare, Cost 1
  Start of turn: Draw 1 card then discard 1 card.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Tools of the Trade — draw then discard at start of turn**
  Setup: Player has Tools of the Trade in hand, 3 energy. Draw pile has 5 cards.
  Actions: Play Tools of the Trade. End turn. Start of next turn.
  Expected: At start of turn, player draws 5 cards normally, then draws 1 additional card (from Tools), then discards 1 card of their choice.

  - [ ] Sim - [ ] Live — **Test: Tools of the Trade triggers Reflex on discard**
  Setup: Tools of the Trade power is active. Player draws Reflex at start of turn. Draw pile has 5 cards.
  Actions: Start of turn: draw hand + 1 extra card. Discard Reflex as the Tools of the Trade discard.
  Expected: Reflex is discarded by a card effect. Player draws 2 cards from Reflex trigger.

  - [ ] Sim - [ ] Live — **Test: Upgraded Tools of the Trade costs 0**
  Setup: Player has Tools of the Trade+ in hand, 3 energy.
  Actions: Play Tools of the Trade+.
  Expected: Costs 0 energy. Player at 3 energy. Tools of the Trade power is now active.

- **Wraith Form** [Y] — BGWraithForm — Power, Rare, Cost 3
  You can't lose more than 1 HP per round. After 2 rounds, Exhaust this card.
  *Upgrade: After 3 rounds, Exhaust this card.*

  - [ ] Sim - [ ] Live — **Test: Wraith Form caps HP loss at 1 per round**
  Setup: Player has Wraith Form in hand, 3 energy, 20 HP, 0 block.
  Actions: Play Wraith Form. Enemy attacks for 10 damage.
  Expected: Player loses only 1 HP (Wraith Form caps loss at 1 per round). Player at 19 HP.

  - [ ] Sim - [ ] Live — **Test: Wraith Form exhausts after 2 rounds**
  Setup: Wraith Form power is active, played this round.
  Actions: Complete round 1. Complete round 2.
  Expected: After 2 rounds, Wraith Form is exhausted and its protection ends.

  - [ ] Sim - [ ] Live — **Test: Upgraded Wraith Form lasts 3 rounds**
  Setup: Player has Wraith Form+ in hand, 3 energy, 20 HP.
  Actions: Play Wraith Form+. Complete round 1. Complete round 2. Complete round 3.
  Expected: Wraith Form+ protection lasts through 3 rounds. After round 3, it is exhausted.

  - [ ] Sim - [ ] Live — **Test: Wraith Form with multiple damage sources in one round**
  Setup: Wraith Form power is active. Player at 15 HP, 0 block. Two enemies attack: Enemy A deals 5 damage, Enemy B deals 8 damage.
  Actions: Both enemies attack the player in the same round.
  Expected: Player loses only 1 HP total for the round (not 1 per attack). Player at 14 HP.
