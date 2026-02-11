# Silent (BGGreen) — Uncommon

- **Backstab** [Y] — BGBackstab — Attack, Uncommon, Cost 0
  2 HIT. +2 damage if the enemy is at full HP. Exhaust.
  *Upgrade: 4 HIT. +2 damage if the enemy is at full HP. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic Backstab against full HP enemy**
  Setup: Player has Backstab in hand, 3 energy. Enemy at 20/20 HP, 0 block.
  Actions: Play Backstab targeting enemy.
  Expected: Enemy takes 2 + 2 = 4 damage (2 HIT at 1 damage each, +2 bonus for full HP). Enemy at 16 HP. Backstab is exhausted.

  - [ ] Sim - [ ] Live — **Test: Backstab against damaged enemy (no bonus)**
  Setup: Player has Backstab in hand, 3 energy. Enemy at 15/20 HP, 0 block.
  Actions: Play Backstab targeting enemy.
  Expected: Enemy takes 2 damage (2 HIT at 1 damage each, no bonus). Enemy at 13 HP. Backstab is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Backstab against full HP enemy with Strength**
  Setup: Player has Backstab+ in hand, 1 STR, 3 energy. Enemy at 20/20 HP, 0 block.
  Actions: Play Backstab+ targeting enemy.
  Expected: Enemy takes 4*(1+1) + 2 = 10 damage (4 HIT at 2 damage each from STR, +2 bonus for full HP). Enemy at 10 HP. Backstab+ is exhausted.

- **Bane** [Y] — BGBane — Attack, Uncommon, Cost 1
  2 HIT. +2 damage if the target has POISON.
  *Upgrade: 3 HIT. +2 damage if the target has POISON.*

  - [ ] Sim - [ ] Live — **Test: Bane against poisoned enemy**
  Setup: Player has Bane in hand, 3 energy. Enemy has 3 POISON, 20 HP, 0 block.
  Actions: Play Bane targeting enemy.
  Expected: Enemy takes 2 + 2 = 4 damage (2 HIT + 2 bonus for POISON). Enemy at 16 HP.

  - [ ] Sim - [ ] Live — **Test: Bane against non-poisoned enemy (no bonus)**
  Setup: Player has Bane in hand, 3 energy. Enemy has 0 POISON, 20 HP, 0 block.
  Actions: Play Bane targeting enemy.
  Expected: Enemy takes 2 damage (2 HIT, no bonus). Enemy at 18 HP.

  - [ ] Sim - [ ] Live — **Test: Upgraded Bane against poisoned enemy with Strength**
  Setup: Player has Bane+ in hand, 2 STR, 3 energy. Enemy has 1 POISON, 30 HP, 0 block.
  Actions: Play Bane+ targeting enemy.
  Expected: Enemy takes 3*(1+2) + 2 = 11 damage (3 HIT at 3 damage each with STR, +2 bonus for POISON). Enemy at 19 HP.

- **Choke** [Y] — BGChoke — Attack, Uncommon, Cost 2
  3 HIT. +1 damage for each WEAK and POISON on the target.
  *Upgrade: 4 HIT.*

  - [ ] Sim - [ ] Live — **Test: Choke against enemy with WEAK and POISON**
  Setup: Player has Choke in hand, 3 energy. Enemy has 2 WEAK, 3 POISON, 30 HP, 0 block.
  Actions: Play Choke targeting enemy.
  Expected: Enemy takes 3*(1 + 2 + 3) = 18 damage (3 HIT, each boosted by +2 from WEAK and +3 from POISON). Enemy at 12 HP.

  - [ ] Sim - [ ] Live — **Test: Choke against clean enemy (no debuffs)**
  Setup: Player has Choke in hand, 3 energy. Enemy has 0 WEAK, 0 POISON, 20 HP, 0 block.
  Actions: Play Choke targeting enemy.
  Expected: Enemy takes 3 damage (3 HIT at base 1 damage each). Enemy at 17 HP.

  - [ ] Sim - [ ] Live — **Test: Upgraded Choke against debuffed enemy**
  Setup: Player has Choke+ in hand, 3 energy. Enemy has 1 WEAK, 1 POISON, 25 HP, 0 block.
  Actions: Play Choke+ targeting enemy.
  Expected: Enemy takes 4*(1 + 1 + 1) = 12 damage (4 HIT, each +1 from WEAK and +1 from POISON). Enemy at 13 HP.

- **Predator** [Y] — BGPredator — Attack, Uncommon, Cost 2
  3 HIT. Any player draws 2 cards.
  *Upgrade: 4 HIT. Any player draws 2 cards.*

  - [ ] Sim - [ ] Live — **Test: Basic Predator — damage and draw**
  Setup: Player has Predator in hand, 3 energy. Enemy at 20 HP, 0 block. Player has 4 other cards in hand, 5 cards in draw pile.
  Actions: Play Predator targeting enemy.
  Expected: Enemy takes 3 damage. Player (or chosen ally) draws 2 cards.

  - [ ] Sim - [ ] Live — **Test: Upgraded Predator — increased damage**
  Setup: Player has Predator+ in hand, 3 energy. Enemy at 20 HP, 0 block. Player has 4 cards in hand, 5 cards in draw pile.
  Actions: Play Predator+ targeting enemy.
  Expected: Enemy takes 4 damage. Chosen player draws 2 cards.

  - [ ] Sim - [ ] Live — **Test: Predator with Strength**
  Setup: Player has Predator in hand, 2 STR, 3 energy. Enemy at 20 HP, 0 block.
  Actions: Play Predator targeting enemy.
  Expected: Enemy takes 3*(1+2) = 9 damage (3 HIT at 3 each with STR). Chosen player draws 2 cards.

- **Masterful Stab** [Y] — BGMasterful Stab — Attack, Uncommon, Cost 4
  Costs 2 if you lost HP this combat. 2 HIT.
  *Upgrade: Costs 1 if you lost HP this combat. 3 HIT.*

  - [ ] Sim - [ ] Live — **Test: Masterful Stab at full cost (no HP lost)**
  Setup: Player has Masterful Stab in hand, 4 energy. Player has not lost HP this combat. Enemy at 20 HP, 0 block.
  Actions: Play Masterful Stab targeting enemy.
  Expected: Costs 4 energy. Enemy takes 2 damage. Player at 0 energy.

  - [ ] Sim - [ ] Live — **Test: Masterful Stab at reduced cost (HP lost this combat)**
  Setup: Player has Masterful Stab in hand, 3 energy. Player lost HP earlier this combat. Enemy at 20 HP, 0 block.
  Actions: Play Masterful Stab targeting enemy.
  Expected: Costs 2 energy. Enemy takes 2 damage. Player at 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Masterful Stab after losing HP**
  Setup: Player has Masterful Stab+ in hand, 3 energy. Player lost HP earlier this combat. Enemy at 20 HP, 0 block.
  Actions: Play Masterful Stab+ targeting enemy.
  Expected: Costs 1 energy. Enemy takes 3 damage. Player at 2 energy.

- **Dash** [Y] — BGDash — Attack, Uncommon, Cost 2
  2 HIT 2 BLK. You may switch rows with another player.
  *Upgrade: 3 HIT 3 BLK. You may switch rows with another player.*

  - [ ] Sim - [ ] Live — **Test: Basic Dash — damage and block**
  Setup: Player has Dash in hand, 3 energy, 0 block. Enemy at 20 HP, 0 block.
  Actions: Play Dash targeting enemy. Decline row switch.
  Expected: Enemy takes 2 damage. Player gains 2 block. Player at 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Dash — increased HIT and BLK**
  Setup: Player has Dash+ in hand, 3 energy, 0 block. Enemy at 20 HP, 0 block.
  Actions: Play Dash+ targeting enemy. Decline row switch.
  Expected: Enemy takes 3 damage. Player gains 3 block. Player at 1 energy.

  - [ ] Sim - [ ] Live — **Test: Dash with Footwork (BLK bonus)**
  Setup: Player has Dash in hand, 3 energy, 0 block. Footwork power active (+1 per BLK). Enemy at 20 HP.
  Actions: Play Dash targeting enemy. Decline row switch.
  Expected: Enemy takes 2 damage. Player gains 2*(1+1) = 4 block (Footwork adds +1 per BLK token).

- **Finisher** [Y] — BGFinisher — Attack, Uncommon, Cost 1
  Deal 1 HIT for each other Attack you played this turn (including SHIV).
  *Upgrade: Deal 2 HIT for each other Attack you played this turn (including SHIV).*

  - [ ] Sim - [ ] Live — **Test: Finisher after playing 3 attacks**
  Setup: Player has Finisher and other cards in hand, 3 energy. Player already played 3 Attacks this turn. Enemy at 20 HP, 0 block.
  Actions: Play Finisher targeting enemy.
  Expected: Enemy takes 3 damage (1 HIT per attack played = 3 HIT).

  - [ ] Sim - [ ] Live — **Test: Finisher with no attacks played this turn**
  Setup: Player has Finisher in hand, 3 energy. Player has played 0 Attacks this turn. Enemy at 20 HP.
  Actions: Play Finisher targeting enemy.
  Expected: Enemy takes 0 damage (0 HIT, no attacks were played).

  - [ ] Sim - [ ] Live — **Test: Upgraded Finisher after 2 attacks and 1 SHIV**
  Setup: Player has Finisher+ in hand, 3 energy. Player played 2 Attacks and used 1 SHIV this turn (3 total). Enemy at 20 HP.
  Actions: Play Finisher+ targeting enemy.
  Expected: Enemy takes 6 damage (2 HIT per attack, 3 attacks = 6 HIT).

- **Flechettes** [Y] — BGFlechettes — Attack, Uncommon, Cost 1
  Deal 1 HIT for each Skill in your hand.
  *Upgrade: Deal 1 HIT for each Skill in your hand +1.*

  - [ ] Sim - [ ] Live — **Test: Flechettes with 3 Skills in hand**
  Setup: Player has Flechettes and 3 Skill cards in hand, 3 energy. Enemy at 20 HP, 0 block.
  Actions: Play Flechettes targeting enemy.
  Expected: Enemy takes 3 damage (1 HIT per Skill = 3 HIT).

  - [ ] Sim - [ ] Live — **Test: Flechettes with 0 Skills in hand**
  Setup: Player has Flechettes and 2 Attack cards in hand (no Skills), 3 energy. Enemy at 20 HP.
  Actions: Play Flechettes targeting enemy.
  Expected: Enemy takes 0 damage (no Skills in hand).

  - [ ] Sim - [ ] Live — **Test: Upgraded Flechettes with 2 Skills in hand**
  Setup: Player has Flechettes+ and 2 Skill cards in hand, 3 energy. Enemy at 20 HP, 0 block.
  Actions: Play Flechettes+ targeting enemy.
  Expected: Enemy takes 3 damage (1 HIT per Skill + 1 = 2 + 1 = 3 HIT).

- **All-Out Attack** [Y] — BGAllOutAttack — Attack, Uncommon, Cost 1
  AOE 2 HIT. Discard 1 card.
  *Upgrade: AOE 3 HIT. Discard 1 card.*

  - [ ] Sim - [ ] Live — **Test: Basic All-Out Attack — AOE damage and discard**
  Setup: Player has All-Out Attack and 3 other cards in hand, 3 energy. Two enemies: Enemy A at 15 HP, Enemy B at 10 HP.
  Actions: Play All-Out Attack. Discard 1 card from hand.
  Expected: Both enemies take 2 damage each. 1 card is discarded from hand.

  - [ ] Sim - [ ] Live — **Test: Upgraded All-Out Attack**
  Setup: Player has All-Out Attack+ and 2 other cards in hand, 3 energy. Two enemies: Enemy A at 15 HP, Enemy B at 10 HP.
  Actions: Play All-Out Attack+. Discard 1 card from hand.
  Expected: Both enemies take 3 damage each. 1 card is discarded from hand.

  - [ ] Sim - [ ] Live — **Test: All-Out Attack triggers Reflex on discard**
  Setup: Player has All-Out Attack and Reflex in hand, 3 energy. Two enemies in play. Draw pile has 4 cards.
  Actions: Play All-Out Attack. Discard Reflex.
  Expected: Both enemies take 2 damage. Reflex is discarded by a card effect, so player draws 2 cards from Reflex trigger.

- **Unload** [Y] — BGUnload — Attack, Uncommon, Cost 1
  2 HIT. Use all of your SHIV now. They each deal +1 damage. (Each SHIV is a separate attack.)
  *Upgrade: +2 damage per SHIV.*

  - [ ] Sim - [ ] Live — **Test: Unload with 3 SHIVs**
  Setup: Player has Unload in hand, 3 SHIV tokens, 3 energy. Enemy at 30 HP, 0 block.
  Actions: Play Unload targeting enemy.
  Expected: Enemy takes 2 damage from Unload's HIT, then 3 separate SHIV attacks at 1+1 = 2 damage each = 6 SHIV damage. Total 8 damage. All SHIVs consumed.

  - [ ] Sim - [ ] Live — **Test: Unload with 0 SHIVs**
  Setup: Player has Unload in hand, 0 SHIV tokens, 3 energy. Enemy at 20 HP, 0 block.
  Actions: Play Unload targeting enemy.
  Expected: Enemy takes 2 damage (2 HIT only, no SHIVs to use).

  - [ ] Sim - [ ] Live — **Test: Upgraded Unload with 2 SHIVs**
  Setup: Player has Unload+ in hand, 2 SHIV tokens, 3 energy. Enemy at 30 HP, 0 block.
  Actions: Play Unload+ targeting enemy.
  Expected: Enemy takes 2 damage from HIT, then 2 SHIV attacks at 1+2 = 3 damage each = 6 SHIV damage. Total 8 damage. All SHIVs consumed.

- **Blur** [Y] — BGBlur — Skill, Uncommon, Cost 1
  2 BLK. +1 BLK if you discarded a card this turn.
  *Upgrade: 3 BLK. +1 BLK if you discarded a card this turn.*

  - [ ] Sim - [ ] Live — **Test: Blur without discarding**
  Setup: Player has Blur in hand, 3 energy, 0 block. Player has not discarded a card this turn.
  Actions: Play Blur.
  Expected: Player gains 2 block.

  - [ ] Sim - [ ] Live — **Test: Blur after discarding a card this turn**
  Setup: Player has Blur in hand, 3 energy, 0 block. Player discarded a card earlier this turn.
  Actions: Play Blur.
  Expected: Player gains 2 + 1 = 3 block (2 BLK base + 1 BLK bonus for discard).

  - [ ] Sim - [ ] Live — **Test: Upgraded Blur after discarding with Footwork**
  Setup: Player has Blur+ in hand, 3 energy, 0 block. Footwork active (+1 per BLK). Player discarded a card this turn.
  Actions: Play Blur+.
  Expected: Player gains (3 + 1) * 2 = 8 block (3 base BLK + 1 bonus BLK = 4 BLK tokens, each worth 2 from Footwork).

- **Bouncing Flask** [Y] — BGBouncingFlask — Skill, Uncommon, Cost 2
  POISON POISON. Each Poison may have a different target.
  *Upgrade: POISON POISON POISON.*

  - [ ] Sim - [ ] Live — **Test: Bouncing Flask — split POISON across enemies**
  Setup: Player has Bouncing Flask in hand, 3 energy. Enemy A at 20 HP, Enemy B at 15 HP.
  Actions: Play Bouncing Flask. Assign 1 POISON to Enemy A, 1 POISON to Enemy B.
  Expected: Enemy A gains 1 POISON. Enemy B gains 1 POISON.

  - [ ] Sim - [ ] Live — **Test: Bouncing Flask — stack both POISON on one enemy**
  Setup: Player has Bouncing Flask in hand, 3 energy. Enemy at 20 HP, 0 POISON.
  Actions: Play Bouncing Flask. Assign both POISON to the same enemy.
  Expected: Enemy gains 2 POISON.

  - [ ] Sim - [ ] Live — **Test: Upgraded Bouncing Flask — 3 POISON distributed**
  Setup: Player has Bouncing Flask+ in hand, 3 energy. Enemy A at 20 HP, Enemy B at 15 HP.
  Actions: Play Bouncing Flask+. Assign 2 POISON to Enemy A, 1 POISON to Enemy B.
  Expected: Enemy A gains 2 POISON. Enemy B gains 1 POISON.

- **Concentrate** [Y] — BGConcentrate — Skill, Uncommon, Cost 0
  Discard any number of cards. Gain Energy(G) for each card discarded. Exhaust.
  *Upgrade: Gain Energy(G) for each card discarded +1.*

  - [ ] Sim - [ ] Live — **Test: Concentrate — discard 2 cards for 2 energy**
  Setup: Player has Concentrate and 3 other cards in hand, 0 energy.
  Actions: Play Concentrate. Discard 2 cards.
  Expected: Player gains 2 energy. Concentrate is exhausted. 1 card remains in hand.

  - [ ] Sim - [ ] Live — **Test: Concentrate — discard 0 cards**
  Setup: Player has Concentrate in hand, 0 energy.
  Actions: Play Concentrate. Discard 0 cards.
  Expected: Player gains 0 energy. Concentrate is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Concentrate — discard 3 cards for 4 energy**
  Setup: Player has Concentrate+ and 3 other cards in hand, 0 energy.
  Actions: Play Concentrate+. Discard 3 cards.
  Expected: Player gains 3 + 1 = 4 energy. Concentrate+ is exhausted.

- **Calculated Gamble** [Y] — BGCalculatedGamble — Skill, Uncommon, Cost 0
  Discard your hand. Draw that many cards.
  *Upgrade: Cost remains 0.*

  - [ ] Sim - [ ] Live — **Test: Calculated Gamble with 4 cards in hand**
  Setup: Player has Calculated Gamble and 3 other cards in hand (4 total besides Gamble), 3 energy. Draw pile has 5 cards.
  Actions: Play Calculated Gamble.
  Expected: All remaining 3 cards in hand are discarded. Player draws 3 new cards from draw pile.

  - [ ] Sim - [ ] Live — **Test: Calculated Gamble with empty hand (only Gamble)**
  Setup: Player has only Calculated Gamble in hand, 3 energy. Draw pile has 5 cards.
  Actions: Play Calculated Gamble.
  Expected: 0 cards discarded. Player draws 0 cards.

  - [ ] Sim - [ ] Live — **Test: Calculated Gamble triggers Reflex in hand**
  Setup: Player has Calculated Gamble, Reflex, and 1 other card in hand, 3 energy. Draw pile has 5 cards.
  Actions: Play Calculated Gamble.
  Expected: Reflex and the other card are discarded. Player draws 2 cards (from Gamble). Reflex triggers on discard: player draws 2 more cards.

- **Catalyst** [Y] — BGCatalyst — Skill, Uncommon, Cost 1
  Double the enemy's POISON. Exhaust.
  *Upgrade: Triple the enemy's POISON. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Catalyst doubles POISON**
  Setup: Player has Catalyst in hand, 3 energy. Enemy has 4 POISON.
  Actions: Play Catalyst targeting enemy.
  Expected: Enemy POISON goes from 4 to 8. Catalyst is exhausted.

  - [ ] Sim - [ ] Live — **Test: Catalyst on enemy with 0 POISON**
  Setup: Player has Catalyst in hand, 3 energy. Enemy has 0 POISON.
  Actions: Play Catalyst targeting enemy.
  Expected: Enemy POISON remains 0 (double of 0). Catalyst is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Catalyst triples POISON**
  Setup: Player has Catalyst+ in hand, 3 energy. Enemy has 5 POISON.
  Actions: Play Catalyst+ targeting enemy.
  Expected: Enemy POISON goes from 5 to 15. Catalyst+ is exhausted.

- **Crippling Cloud** [Y] — BGCripplingCloud — Skill, Uncommon, Cost 2
  AOE POISON WEAK. Exhaust.
  *Upgrade: AOE POISON POISON WEAK. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic Crippling Cloud — AOE debuffs**
  Setup: Player has Crippling Cloud in hand, 3 energy. Two enemies: Enemy A at 20 HP, Enemy B at 15 HP, neither has debuffs.
  Actions: Play Crippling Cloud.
  Expected: Both enemies gain 1 POISON and 1 WEAK. Crippling Cloud is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Crippling Cloud — extra POISON**
  Setup: Player has Crippling Cloud+ in hand, 3 energy. Two enemies, no debuffs.
  Actions: Play Crippling Cloud+.
  Expected: Both enemies gain 2 POISON and 1 WEAK. Crippling Cloud+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Crippling Cloud triggers Distraction**
  Setup: Player has Crippling Cloud in hand, 3 energy, 0 block. Distraction power active (2 BLK on first token placed on enemy per turn). Two enemies.
  Actions: Play Crippling Cloud.
  Expected: Both enemies gain 1 POISON and 1 WEAK. Player gains 2 block from Distraction (triggers once per turn on first token placed).

- **Leg Sweep** [Y] — BGLegSweep — Skill, Uncommon, Cost 2
  WEAK. 3 BLK.
  *Upgrade: WEAK. 4 BLK.*

  - [ ] Sim - [ ] Live — **Test: Basic Leg Sweep**
  Setup: Player has Leg Sweep in hand, 3 energy, 0 block. Enemy has 0 WEAK.
  Actions: Play Leg Sweep targeting enemy.
  Expected: Enemy gains 1 WEAK. Player gains 3 block.

  - [ ] Sim - [ ] Live — **Test: Upgraded Leg Sweep with Footwork**
  Setup: Player has Leg Sweep+ in hand, 3 energy, 0 block. Footwork active (+1 per BLK). Enemy has 0 WEAK.
  Actions: Play Leg Sweep+ targeting enemy.
  Expected: Enemy gains 1 WEAK. Player gains 4*(1+1) = 8 block (4 BLK tokens, each worth 2 with Footwork).

  - [ ] Sim - [ ] Live — **Test: Leg Sweep stacking WEAK**
  Setup: Player has Leg Sweep in hand, 3 energy. Enemy already has 2 WEAK.
  Actions: Play Leg Sweep targeting enemy.
  Expected: Enemy now has 3 WEAK. Player gains 3 block.

- **Outmaneuver** [Y] — BGOutmaneuver — Skill, Uncommon, Cost 1
  Retain. When played, if you Retained this last turn, gain Energy(G) Energy(G).
  *Upgrade: Gain Energy(G) Energy(G) Energy(G).*

  - [ ] Sim - [ ] Live — **Test: Outmaneuver played immediately (not retained)**
  Setup: Player has Outmaneuver in hand (drawn this turn), 3 energy.
  Actions: Play Outmaneuver.
  Expected: No energy gained (was not retained from last turn). Player spent 1 energy, now at 2 energy.

  - [ ] Sim - [ ] Live — **Test: Outmaneuver retained and played next turn**
  Setup: Player has Outmaneuver in hand, 3 energy. Turn 1.
  Actions: End turn (Outmaneuver is retained). Start turn 2 with 3 energy. Play Outmaneuver.
  Expected: Player gains 2 energy (was retained from last turn). Player spent 1 energy to play, net +1 energy, now at 4 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Outmaneuver retained and played**
  Setup: Player has Outmaneuver+ in hand. Turn 1.
  Actions: End turn (Outmaneuver+ is retained). Start turn 2 with 3 energy. Play Outmaneuver+.
  Expected: Player gains 3 energy (was retained). Spent 1 to play, net +2 energy, now at 5 energy.

- **Piercing Wail** [Y] — BGPiercingWail — Skill, Uncommon, Cost 1
  1 BLK. AOE WEAK. Exhaust.
  *Upgrade: 3 BLK. AOE WEAK. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic Piercing Wail**
  Setup: Player has Piercing Wail in hand, 3 energy, 0 block. Two enemies, no WEAK.
  Actions: Play Piercing Wail.
  Expected: Player gains 1 block. Both enemies gain 1 WEAK. Piercing Wail is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Piercing Wail**
  Setup: Player has Piercing Wail+ in hand, 3 energy, 0 block. Two enemies, no WEAK.
  Actions: Play Piercing Wail+.
  Expected: Player gains 3 block. Both enemies gain 1 WEAK. Piercing Wail+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Piercing Wail with Footwork**
  Setup: Player has Piercing Wail in hand, 3 energy, 0 block. Footwork active (+1 per BLK). One enemy.
  Actions: Play Piercing Wail.
  Expected: Player gains 1*(1+1) = 2 block (Footwork boosts each BLK token). Enemy gains 1 WEAK. Piercing Wail is exhausted.

- **Escape Plan** [Y] — BGEscapePlan — Skill, Uncommon, Cost 0
  Draw 1 card. If you draw a Skill, 1 BLK.
  *Upgrade: 1 BLK. Draw 1 card. (Always gives block.)*

  - [ ] Sim - [ ] Live — **Test: Escape Plan draws a Skill**
  Setup: Player has Escape Plan in hand, 3 energy, 0 block. Top card of draw pile is a Skill card.
  Actions: Play Escape Plan.
  Expected: Player draws 1 card (the Skill). Player gains 1 block (drew a Skill).

  - [ ] Sim - [ ] Live — **Test: Escape Plan draws an Attack (no block)**
  Setup: Player has Escape Plan in hand, 3 energy, 0 block. Top card of draw pile is an Attack card.
  Actions: Play Escape Plan.
  Expected: Player draws 1 card (the Attack). Player gains 0 block (did not draw a Skill).

  - [ ] Sim - [ ] Live — **Test: Upgraded Escape Plan always gives block**
  Setup: Player has Escape Plan+ in hand, 3 energy, 0 block. Top card of draw pile is an Attack card.
  Actions: Play Escape Plan+.
  Expected: Player gains 1 block (unconditional). Player draws 1 card (the Attack). Total 1 block regardless of drawn card type.

- **Expertise** [Y] — BGExpertise — Skill, Uncommon, Cost 1
  Draw cards until you have 6 in hand.
  *Upgrade: Draw cards until you have 7 in hand.*

  - [ ] Sim - [ ] Live — **Test: Expertise with 2 cards in hand**
  Setup: Player has Expertise and 1 other card in hand (2 total), 3 energy. Draw pile has 6 cards.
  Actions: Play Expertise (hand goes to 1 card after playing).
  Expected: Player draws 5 cards (from 1 in hand up to 6).

  - [ ] Sim - [ ] Live — **Test: Expertise with full hand (6+ cards)**
  Setup: Player has Expertise and 6 other cards in hand (7 total), 3 energy.
  Actions: Play Expertise (hand goes to 6 after playing).
  Expected: Player draws 0 cards (already at 6 in hand).

  - [ ] Sim - [ ] Live — **Test: Upgraded Expertise with 3 cards in hand**
  Setup: Player has Expertise+ and 2 other cards in hand (3 total), 3 energy. Draw pile has 6 cards.
  Actions: Play Expertise+ (hand goes to 2 after playing).
  Expected: Player draws 5 cards (from 2 in hand up to 7).

- **Riddle with Holes** [Y] — BGRiddleWithHoles — Skill, Uncommon, Cost 2
  SHIV SHIV SHIV SHIV.
  *Upgrade: SHIV SHIV SHIV SHIV SHIV.*

  - [ ] Sim - [ ] Live — **Test: Basic Riddle with Holes**
  Setup: Player has Riddle with Holes in hand, 3 energy, 0 SHIV tokens.
  Actions: Play Riddle with Holes.
  Expected: Player gains 4 SHIV tokens. Player at 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Riddle with Holes**
  Setup: Player has Riddle with Holes+ in hand, 3 energy, 0 SHIV tokens.
  Actions: Play Riddle with Holes+.
  Expected: Player gains 5 SHIV tokens. Player at 1 energy.

  - [ ] Sim - [ ] Live — **Test: Riddle with Holes stacks with existing SHIVs**
  Setup: Player has Riddle with Holes in hand, 3 energy, 2 SHIV tokens already.
  Actions: Play Riddle with Holes.
  Expected: Player now has 2 + 4 = 6 SHIV tokens.

- **Setup** [Y] — BGSetup — Skill, Uncommon, Cost 1
  Energy(G) to any player. Exhaust.
  *Upgrade: Energy(G) Energy(G) to any player. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic Setup — give energy to self**
  Setup: Player has Setup in hand, 3 energy.
  Actions: Play Setup targeting self.
  Expected: Player gains 1 energy (net 0 after cost). Setup is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Setup — give energy to ally**
  Setup: Player has Setup+ in hand, 3 energy. Ally exists.
  Actions: Play Setup+ targeting ally.
  Expected: Ally gains 2 energy. Player spends 1 energy (now at 2 energy). Setup+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Setup is exhausted after use**
  Setup: Player has Setup in hand, 3 energy.
  Actions: Play Setup targeting self.
  Expected: Setup is moved to exhaust pile, not discard pile.

- **Terror** [Y] — BGTerror — Skill, Uncommon, Cost 1
  VULN. Exhaust.
  *Upgrade: VULN. (No longer Exhausts.)*

  - [ ] Sim - [ ] Live — **Test: Basic Terror — apply VULN and exhaust**
  Setup: Player has Terror in hand, 3 energy. Enemy has 0 VULN.
  Actions: Play Terror targeting enemy.
  Expected: Enemy gains 1 VULN. Terror is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Terror — no longer exhausts**
  Setup: Player has Terror+ in hand, 3 energy. Enemy has 0 VULN.
  Actions: Play Terror+ targeting enemy.
  Expected: Enemy gains 1 VULN. Terror+ goes to discard pile (not exhausted).

  - [ ] Sim - [ ] Live — **Test: Terror stacks VULN**
  Setup: Player has Terror in hand, 3 energy. Enemy already has 2 VULN.
  Actions: Play Terror targeting enemy.
  Expected: Enemy now has 3 VULN. Terror is exhausted.

- **Footwork** [Y] — BGFootwork — Power, Uncommon, Cost 1
  Each BLK on your Attacks and Skills gets +1 Block.
  *Upgrade: Each BLK on your Attacks and Skills gets +1 Block. Retain.*

  - [ ] Sim - [ ] Live — **Test: Footwork boosts BLK on subsequent cards**
  Setup: Player has Footwork and Defend (1 BLK) in hand, 3 energy, 0 block.
  Actions: Play Footwork. Play Defend.
  Expected: Defend's 1 BLK now grants 1*(1+1) = 2 block instead of 1.

  - [ ] Sim - [ ] Live — **Test: Two Footworks stack**
  Setup: Player has 2 Footwork cards and Defend (1 BLK) in hand, 3 energy, 0 block.
  Actions: Play Footwork. Play second Footwork. Play Defend.
  Expected: Defend's 1 BLK now grants 1*(1+2) = 3 block (+1 from each Footwork).

  - [ ] Sim - [ ] Live — **Test: Upgraded Footwork has Retain**
  Setup: Player has Footwork+ in hand, 3 energy. Turn 1.
  Actions: End turn without playing Footwork+.
  Expected: Footwork+ is retained in hand for next turn (not discarded).

- **Noxious Fumes** [Y] — BGNoxiousFumes — Power, Uncommon, Cost 1
  Start of turn: POISON.
  *Upgrade: Start of turn: AOE POISON.*

  - [ ] Sim - [ ] Live — **Test: Noxious Fumes applies POISON each turn**
  Setup: Player has Noxious Fumes in hand, 3 energy. One enemy with 0 POISON.
  Actions: Play Noxious Fumes. End turn. Start of next turn.
  Expected: At start of player's next turn, enemy gains 1 POISON.

  - [ ] Sim - [ ] Live — **Test: Noxious Fumes accumulates over multiple turns**
  Setup: Noxious Fumes power is active. One enemy with 0 POISON.
  Actions: End turn (turn 1 start: enemy gains 1 POISON). End turn (turn 2 start: enemy gains 1 more POISON).
  Expected: After 2 turn starts, enemy has gained 2 total POISON applications (POISON also ticks down each turn from existing stacks).

  - [ ] Sim - [ ] Live — **Test: Upgraded Noxious Fumes — AOE POISON**
  Setup: Player has Noxious Fumes+ in hand, 3 energy. Two enemies, both at 0 POISON.
  Actions: Play Noxious Fumes+. End turn. Start of next turn.
  Expected: At start of player's next turn, ALL enemies each gain 1 POISON.

- **Well-Laid Plans** [Y] — BGWellLaidPlans — Power, Uncommon, Cost 1
  End of turn: You may Retain 1 card.
  *Upgrade: End of turn: Retain up to 2 cards.*

  - [ ] Sim - [ ] Live — **Test: Well-Laid Plans — retain 1 card at end of turn**
  Setup: Player has Well-Laid Plans and 3 other cards in hand, 3 energy.
  Actions: Play Well-Laid Plans. End turn, choose to retain 1 card.
  Expected: 1 chosen card is retained in hand. Other 2 cards are discarded.

  - [ ] Sim - [ ] Live — **Test: Upgraded Well-Laid Plans — retain 2 cards**
  Setup: Player has Well-Laid Plans+ and 3 other cards in hand, 3 energy.
  Actions: Play Well-Laid Plans+. End turn, choose to retain 2 cards.
  Expected: 2 chosen cards are retained in hand. 1 card is discarded.

  - [ ] Sim - [ ] Live — **Test: Well-Laid Plans — choose not to retain**
  Setup: Well-Laid Plans power is active. Player has 3 cards in hand.
  Actions: End turn, choose not to retain any card.
  Expected: All 3 cards are discarded normally.

- **Distraction** [Y] — BGDistraction — Power, Uncommon, Cost 2
  Once per turn: When you put a token on an enemy, 2 BLK.
  *Upgrade: Cost 2 to 1.*

  - [ ] Sim - [ ] Live — **Test: Distraction triggers on applying POISON**
  Setup: Player has Distraction and Deadly Poison (POISON) in hand, 3 energy, 0 block. Enemy at 20 HP.
  Actions: Play Distraction. Play Deadly Poison targeting enemy.
  Expected: Enemy gains 1 POISON. Player gains 2 block from Distraction trigger.

  - [ ] Sim - [ ] Live — **Test: Distraction triggers only once per turn**
  Setup: Distraction power is active. Player has two POISON cards in hand, 3 energy, 0 block. Enemy at 20 HP.
  Actions: Play first POISON card. Play second POISON card.
  Expected: Player gains 2 block from the first token placed. Second token placement does NOT trigger Distraction again this turn.

  - [ ] Sim - [ ] Live — **Test: Upgraded Distraction costs less**
  Setup: Player has Distraction+ in hand, 1 energy, 0 block.
  Actions: Play Distraction+.
  Expected: Distraction+ costs 1 energy (reduced from 2). Player at 0 energy. Distraction power is now active.

- **Infinite Blades** [Y] — BGInfinite Blades — Power, Uncommon, Cost 1
  Start of turn: SHIV.
  *Upgrade: Start of turn: SHIV SHIV.*

  - [ ] Sim - [ ] Live — **Test: Infinite Blades grants SHIV at start of turn**
  Setup: Player has Infinite Blades in hand, 3 energy, 0 SHIV tokens.
  Actions: Play Infinite Blades. End turn. Start of next turn.
  Expected: At start of player's next turn, player gains 1 SHIV token.

  - [ ] Sim - [ ] Live — **Test: Upgraded Infinite Blades grants 2 SHIVs**
  Setup: Player has Infinite Blades+ in hand, 3 energy, 0 SHIV tokens.
  Actions: Play Infinite Blades+. End turn. Start of next turn.
  Expected: At start of player's next turn, player gains 2 SHIV tokens.

  - [ ] Sim - [ ] Live — **Test: Infinite Blades accumulates SHIVs over turns**
  Setup: Infinite Blades power is active. Player has 0 SHIV tokens.
  Actions: Start of turn 1 (gain 1 SHIV). Do not use SHIV. Start of turn 2 (gain 1 SHIV).
  Expected: Player has 2 SHIV tokens accumulated.

- **Reflex** [Y] — BGReflex — Skill, Uncommon, Cost -2
  Unplayable. If this card is discarded by a card's effect, draw 2 cards.
  *Upgrade: Draw 3 cards.*

  - [ ] Sim - [ ] Live — **Test: Reflex triggers when discarded by card effect**
  Setup: Player has Calculated Gamble and Reflex in hand, 3 energy. Draw pile has 5 cards.
  Actions: Play Calculated Gamble (discards entire hand including Reflex).
  Expected: Reflex is discarded by Calculated Gamble's effect. Player draws 2 cards from Reflex trigger (in addition to Calculated Gamble's draws).

  - [ ] Sim - [ ] Live — **Test: Reflex does NOT trigger at end of turn discard**
  Setup: Player has Reflex in hand, 3 energy. Draw pile has 5 cards.
  Actions: End turn (Reflex is discarded at end of turn).
  Expected: Reflex is discarded normally. No cards are drawn (end of turn discard is not a card effect).

  - [ ] Sim - [ ] Live — **Test: Upgraded Reflex draws 3 cards on discard**
  Setup: Player has Concentrate and Reflex+ in hand, 3 energy. Draw pile has 5 cards.
  Actions: Play Concentrate, discard Reflex+.
  Expected: Reflex+ is discarded by Concentrate's effect. Player draws 3 cards from Reflex+ trigger.

- **Tactician** [Y] — BGTactician — Skill, Uncommon, Cost -2
  Unplayable. If this card is discarded by a card's effect, gain Energy(G) Energy(G) and Exhaust.
  *Upgrade: Gain Energy(G) Energy(G) Energy(G) and Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Tactician triggers when discarded by card effect**
  Setup: Player has Calculated Gamble and Tactician in hand, 1 energy. Draw pile has 5 cards.
  Actions: Play Calculated Gamble (discards hand including Tactician).
  Expected: Tactician is discarded by card effect. Player gains 2 energy. Tactician is exhausted (goes to exhaust pile, not discard pile).

  - [ ] Sim - [ ] Live — **Test: Tactician does NOT trigger at end of turn**
  Setup: Player has Tactician in hand, 0 energy.
  Actions: End turn (Tactician discarded at end of turn).
  Expected: Tactician is discarded normally. No energy gained (end of turn discard is not a card effect). Tactician goes to discard pile.

  - [ ] Sim - [ ] Live — **Test: Upgraded Tactician grants 3 energy**
  Setup: Player has Concentrate and Tactician+ in hand, 0 energy. Draw pile has 3 cards.
  Actions: Play Concentrate (costs 0), discard Tactician+.
  Expected: Player gains 3 energy from Tactician+ trigger. Tactician+ is exhausted. Player also gains 1 energy from Concentrate for discarding 1 card. Total 4 energy gained.
