# Silent (BGGreen) — Common

- **Poisoned Stab** [Y] — BGPoisonedStab — Attack, Common, Cost 1
  1 HIT POISON. Exhaust.
  *Upgrade: 1 HIT POISON POISON. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Poisoned Stab deals 1 damage, applies 1 Poison, and exhausts**
  Setup: Player has Poisoned Stab in hand, 3 energy. Enemy has 10 HP, 0 Poison.
  Actions: Play Poisoned Stab targeting enemy.
  Expected: Enemy loses 1 HP (now 9 HP). Enemy gains 1 POISON. Poisoned Stab moves to exhaust pile (not discard pile). Player spends 1 energy (now 2).

  - [ ] Sim - [ ] Live — **Test: Upgraded Poisoned Stab applies 2 Poison**
  Setup: Player has Poisoned Stab+ in hand, 3 energy. Enemy has 10 HP, 0 Poison.
  Actions: Play Poisoned Stab+ targeting enemy.
  Expected: Enemy loses 1 HP (now 9 HP). Enemy gains 2 POISON. Poisoned Stab+ moves to exhaust pile.

  - [ ] Sim - [ ] Live — **Test: Poisoned Stab with Strength adds damage per HIT**
  Setup: Player has Poisoned Stab in hand, 3 energy, 2 STR. Enemy has 10 HP, 0 Poison.
  Actions: Play Poisoned Stab targeting enemy.
  Expected: Enemy loses 3 HP (1 HIT + 2 STR = 3 damage, now 7 HP). Enemy gains 1 POISON. Card is exhausted.

- **Dagger Throw** [Y] — BGDaggerThrow — Attack, Common, Cost 1
  2 HIT. Draw 1 card. Discard 1 card.
  *Upgrade: 3 HIT. Draw 1 card. Discard 1 card.*

  - [ ] Sim - [ ] Live — **Test: Dagger Throw deals 2 HIT, draws 1, discards 1**
  Setup: Player has Dagger Throw in hand (4 cards total in hand), 3 energy. Enemy has 10 HP. Draw pile has 5 cards.
  Actions: Play Dagger Throw targeting enemy. Draw 1 card, then discard 1 card from hand.
  Expected: Enemy loses 2 HP (now 8 HP). Player draws 1 card, then discards 1 card of their choice. Net hand size change: -1 (played Dagger Throw) +1 (draw) -1 (discard) = hand has 3 cards.

  - [ ] Sim - [ ] Live — **Test: Upgraded Dagger Throw deals 3 HIT**
  Setup: Player has Dagger Throw+ in hand, 3 energy. Enemy has 10 HP. Draw pile has 3 cards.
  Actions: Play Dagger Throw+ targeting enemy. Draw 1 card, discard 1 card.
  Expected: Enemy loses 3 HP (now 7 HP). Player draws 1 card, then discards 1 card.

  - [ ] Sim - [ ] N/A — **Test: Dagger Throw discard triggers After Image**
  Setup: Player has Dagger Throw and Strike in hand, 3 energy, 0 block. After Image power active. Enemy has 10 HP. Draw pile has 3 cards.
  Actions: Play Dagger Throw targeting enemy. Draw 1 card, discard Strike.
  Expected: Enemy loses 2 HP. Player draws 1 card, discards Strike. After Image triggers granting 1 BLK.

- **Dagger Spray** [Y] — BGDaggerSpray — Attack, Common, Cost 1
  AOE 1 HIT 1 HIT.
  *Upgrade: AOE 1 HIT 1 HIT 1 HIT.*

  - [ ] Sim - [ ] Live — **Test: Dagger Spray hits all enemies twice**
  Setup: Player has Dagger Spray in hand, 3 energy. Enemy A has 10 HP. Enemy B has 8 HP.
  Actions: Play Dagger Spray.
  Expected: Enemy A loses 2 HP (now 8 HP). Enemy B loses 2 HP (now 6 HP). Player spends 1 energy (now 2).

  - [ ] Sim - [ ] Live — **Test: Upgraded Dagger Spray hits all enemies three times**
  Setup: Player has Dagger Spray+ in hand, 3 energy. Enemy A has 10 HP. Enemy B has 8 HP.
  Actions: Play Dagger Spray+.
  Expected: Enemy A loses 3 HP (now 7 HP). Enemy B loses 3 HP (now 5 HP).

  - [ ] Sim - [ ] Live — **Test: Dagger Spray with Strength adds to each HIT on each enemy**
  Setup: Player has Dagger Spray in hand, 3 energy, 1 STR. Enemy A has 10 HP. Enemy B has 10 HP.
  Actions: Play Dagger Spray.
  Expected: Each enemy takes 2 HIT at 2 damage each (1+1 STR). Enemy A loses 4 HP (now 6 HP). Enemy B loses 4 HP (now 6 HP).

- **Sneaky Strike** [Y] — BGSneakyStrike — Attack, Common, Cost 2
  3 HIT. If you discarded a card this turn, gain Energy(G) Energy(G).
  *Upgrade: 4 HIT.*

  - [ ] Sim - [ ] Live — **Test: Sneaky Strike deals 3 damage without discard, no energy refund**
  Setup: Player has Sneaky Strike in hand, 3 energy. Enemy has 10 HP. No cards discarded this turn.
  Actions: Play Sneaky Strike targeting enemy.
  Expected: Enemy loses 3 HP (now 7 HP). Player spends 2 energy (now 1). No energy refunded.

  - [ ] Sim - [ ] N/A — **Test: Sneaky Strike refunds 2 energy when a card was discarded this turn**
  Setup: Player has Survivor, Sneaky Strike, and Strike in hand, 3 energy. Enemy has 10 HP.
  Actions: Play Survivor (discard Strike). Then play Sneaky Strike targeting enemy.
  Expected: After Survivor: 1 energy remaining. After Sneaky Strike: enemy loses 3 HP (now 7 HP), player gains 2 energy. Final energy: 1 (from Survivor cost and Sneaky Strike cost are offset by the 2 energy refund).

  - [ ] Sim - [ ] Live — **Test: Upgraded Sneaky Strike deals 4 HIT**
  Setup: Player has Sneaky Strike+ in hand, 3 energy, 1 STR. Enemy has 20 HP. No cards discarded this turn.
  Actions: Play Sneaky Strike+ targeting enemy.
  Expected: Enemy loses 8 HP (4 HIT, each dealing 1+1 STR = 2 damage, now 12 HP). Player spends 2 energy (now 1).

- **Slice** [Y] — BGSlice — Attack, Common, Cost 0
  1 HIT. +1 damage if you have a SHIV.
  *Upgrade: 2 HIT. +1 damage if you have a SHIV.*

  - [ ] Sim - [ ] Live — **Test: Slice deals 1 damage at zero cost without SHIV**
  Setup: Player has Slice in hand, 3 energy, no SHIV. Enemy has 10 HP.
  Actions: Play Slice targeting enemy.
  Expected: Enemy loses 1 HP (now 9 HP). Player energy remains 3.

  - [ ] Sim - [ ] N/A — **Test: Slice deals bonus damage with SHIV**
  Setup: Player has Slice in hand, 3 energy, 1 SHIV. Enemy has 10 HP.
  Actions: Play Slice targeting enemy.
  Expected: Enemy loses 2 HP (1 HIT base + 1 bonus from SHIV = 2 damage, now 8 HP).

  - [ ] Sim - [ ] N/A — **Test: Upgraded Slice with SHIV adds bonus to total**
  Setup: Player has Slice+ in hand, 3 energy, 1 SHIV, 1 STR. Enemy has 10 HP.
  Actions: Play Slice+ targeting enemy.
  Expected: Enemy takes 2 HIT at 2 damage each (1+1 STR) = 4 damage, plus 1 bonus from SHIV = 5 total damage. Enemy now at 5 HP.

- **Backflip** [Y] — BGBackflip — Skill, Common, Cost 1
  1 BLK. Draw 2 cards.
  *Upgrade: 2 BLK. Draw 2 cards.*

  - [ ] Sim - [ ] Live — **Test: Backflip grants 1 block and draws 2 cards**
  Setup: Player has Backflip in hand (and 4 other cards), 3 energy, 0 block. Draw pile has 5 cards.
  Actions: Play Backflip.
  Expected: Player gains 1 block. Player draws 2 cards. Hand now has 6 cards (4 remaining + 2 drawn). Player spends 1 energy (now 2).

  - [ ] Sim - [ ] Live — **Test: Upgraded Backflip grants 2 block and draws 2 cards**
  Setup: Player has Backflip+ in hand, 3 energy, 0 block. Draw pile has 5 cards.
  Actions: Play Backflip+.
  Expected: Player gains 2 block. Player draws 2 cards.

  - [ ] Sim - [ ] N/A — **Test: Backflip with insufficient draw pile reshuffles discard**
  Setup: Player has Backflip in hand, 3 energy, 0 block. Draw pile has 1 card. Discard pile has 5 cards.
  Actions: Play Backflip.
  Expected: Player gains 1 block. Player draws 1 card from draw pile, discard pile is shuffled into draw pile, player draws 1 more card.

- **Dodge and Roll** [Y] — BGDodgeAndRoll — Skill, Common, Cost 1
  1 BLK 1 BLK. Each BLK can go to any player.
  *Upgrade: 1 BLK 1 BLK 1 BLK. Each BLK can go to any player.*

  - [ ] Sim - [ ] Live — **Test: Dodge and Roll assigns 2 BLK to self**
  Setup: Player has Dodge and Roll in hand, 3 energy, 0 block.
  Actions: Play Dodge and Roll, assign both BLK to self.
  Expected: Player gains 2 block. Player spends 1 energy (now 2).

  - [ ] Sim - [ ] N/A — **Test: Dodge and Roll splits BLK between players**
  Setup: Player has Dodge and Roll in hand, 3 energy, 0 block. Ally has 0 block.
  Actions: Play Dodge and Roll, assign 1 BLK to self and 1 BLK to ally.
  Expected: Player gains 1 block. Ally gains 1 block.

  - [ ] Sim - [ ] N/A — **Test: Upgraded Dodge and Roll distributes 3 BLK**
  Setup: Player has Dodge and Roll+ in hand, 3 energy, 0 block. Ally has 0 block.
  Actions: Play Dodge and Roll+, assign 2 BLK to self and 1 BLK to ally.
  Expected: Player gains 2 block. Ally gains 1 block.

- **Deflect** [Y] — BGDeflect — Skill, Common, Cost 0
  1 BLK. +1 BLK if you have a SHIV.
  *Upgrade: 2 BLK. +1 BLK if you have a SHIV.*

  - [ ] Sim - [ ] Live — **Test: Deflect grants 1 block at zero cost without SHIV**
  Setup: Player has Deflect in hand, 3 energy, 0 block, no SHIV.
  Actions: Play Deflect.
  Expected: Player gains 1 block. Player energy remains 3.

  - [ ] Sim - [ ] N/A — **Test: Deflect grants bonus block with SHIV**
  Setup: Player has Deflect in hand, 3 energy, 0 block, 1 SHIV.
  Actions: Play Deflect.
  Expected: Player gains 2 block (1 base + 1 bonus from SHIV).

  - [ ] Sim - [ ] N/A — **Test: Upgraded Deflect with SHIV grants 3 block total**
  Setup: Player has Deflect+ in hand, 3 energy, 0 block, 1 SHIV.
  Actions: Play Deflect+.
  Expected: Player gains 3 block (2 base + 1 bonus from SHIV).

- **Cloak and Dagger** [Y] — BGCloakAndDagger — Skill, Common, Cost 1
  SHIV. 1 BLK.
  *Upgrade: SHIV SHIV. 1 BLK.*

  - [ ] Sim - [ ] Live — **Test: Cloak and Dagger gives 1 SHIV and 1 block**
  Setup: Player has Cloak and Dagger in hand, 3 energy, 0 block, 0 SHIV.
  Actions: Play Cloak and Dagger.
  Expected: Player gains 1 SHIV token. Player gains 1 block. Player spends 1 energy (now 2).

  - [ ] Sim - [ ] Live — **Test: Upgraded Cloak and Dagger gives 2 SHIV and 1 block**
  Setup: Player has Cloak and Dagger+ in hand, 3 energy, 0 block, 0 SHIV.
  Actions: Play Cloak and Dagger+.
  Expected: Player gains 2 SHIV tokens. Player gains 1 block. Player spends 1 energy (now 2).

  - [ ] Sim - [ ] N/A — **Test: Cloak and Dagger SHIV interacts with Accuracy**
  Setup: Player has Cloak and Dagger in hand, 3 energy, 0 SHIV. Accuracy power is active (+1 SHIV damage). Enemy has 10 HP.
  Actions: Play Cloak and Dagger. Then play Slice targeting enemy.
  Expected: Player gains 1 SHIV and 1 block from Cloak and Dagger. Slice with SHIV and Accuracy deals 1 HIT + 1 SHIV bonus + 1 Accuracy bonus = 3 damage. Enemy now at 7 HP.

- **Blade Dance** [Y] — BGBladeDance — Skill, Common, Cost 1
  SHIV SHIV.
  *Upgrade: SHIV SHIV SHIV.*

  - [ ] Sim - [ ] Live — **Test: Blade Dance gives 2 SHIV tokens**
  Setup: Player has Blade Dance in hand, 3 energy, 0 SHIV.
  Actions: Play Blade Dance.
  Expected: Player gains 2 SHIV tokens. Player spends 1 energy (now 2).

  - [ ] Sim - [ ] Live — **Test: Upgraded Blade Dance gives 3 SHIV tokens**
  Setup: Player has Blade Dance+ in hand, 3 energy, 0 SHIV.
  Actions: Play Blade Dance+.
  Expected: Player gains 3 SHIV tokens. Player spends 1 energy (now 2).

  - [ ] Sim - [ ] Live — **Test: Blade Dance SHIV stacks with existing SHIV**
  Setup: Player has Blade Dance in hand, 3 energy, 1 SHIV already.
  Actions: Play Blade Dance.
  Expected: Player now has 3 SHIV tokens total (1 existing + 2 gained).

- **Prepared** [Y] — BGPrepared — Skill, Common, Cost 0
  Draw 1 card. Discard 1 card.
  *Upgrade: Draw 2 cards. Discard 2 cards.*

  - [ ] Sim - [ ] Live — **Test: Prepared draws 1 and discards 1 at zero cost**
  Setup: Player has Prepared and 3 other cards in hand, 3 energy. Draw pile has 5 cards.
  Actions: Play Prepared. Draw 1 card, discard 1 card from hand.
  Expected: Player draws 1 card, then discards 1 card of choice. Hand size remains 3 (played Prepared, drew 1, discarded 1). Energy remains 3.

  - [ ] Sim - [ ] Live — **Test: Upgraded Prepared draws 2 and discards 2**
  Setup: Player has Prepared+ and 3 other cards in hand, 3 energy. Draw pile has 5 cards.
  Actions: Play Prepared+. Draw 2 cards, discard 2 cards from hand.
  Expected: Player draws 2 cards, then discards 2 cards of choice. Hand size remains 3.

  - [ ] Sim - [ ] N/A — **Test: Prepared discard triggers After Image**
  Setup: Player has Prepared and Strike in hand, 3 energy, 0 block. After Image power active. Draw pile has 5 cards.
  Actions: Play Prepared. Draw 1 card, discard Strike.
  Expected: Player draws 1 card, discards Strike. After Image triggers granting 1 BLK.

- **Deadly Poison** [Y] — BGDeadlyPoison — Skill, Common, Cost 1
  POISON.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Deadly Poison applies 1 Poison to enemy**
  Setup: Player has Deadly Poison in hand, 3 energy. Enemy has 10 HP, 0 Poison.
  Actions: Play Deadly Poison targeting enemy.
  Expected: Enemy gains 1 POISON. Player spends 1 energy (now 2).

  - [ ] Sim - [ ] Live — **Test: Deadly Poison stacks with existing Poison**
  Setup: Player has Deadly Poison in hand, 3 energy. Enemy has 10 HP, 2 Poison.
  Actions: Play Deadly Poison targeting enemy.
  Expected: Enemy now has 3 POISON.

  - [ ] Sim - [ ] Live — **Test: Upgraded Deadly Poison costs 0 energy**
  Setup: Player has Deadly Poison+ in hand, 0 energy. Enemy has 10 HP, 0 Poison.
  Actions: Play Deadly Poison+ targeting enemy.
  Expected: Enemy gains 1 POISON. Player energy remains 0 (card costs 0).

- **Acrobatics** [Y] — BGAcrobatics — Skill, Common, Cost 1
  Draw 3 cards. Discard 1 card.
  *Upgrade: Draw 4 cards. Discard 1 card.*

  - [ ] Sim - [ ] Live — **Test: Acrobatics draws 3 cards and discards 1**
  Setup: Player has Acrobatics and 2 other cards in hand, 3 energy. Draw pile has 5 cards.
  Actions: Play Acrobatics. Draw 3 cards, discard 1 card from hand.
  Expected: Player draws 3 cards, then discards 1 card of choice. Hand size = 2 (original) + 3 (drawn) - 1 (discarded) = 4. Player spends 1 energy (now 2).

  - [ ] Sim - [ ] Live — **Test: Upgraded Acrobatics draws 4 cards and discards 1**
  Setup: Player has Acrobatics+ and 1 other card in hand, 3 energy. Draw pile has 5 cards.
  Actions: Play Acrobatics+. Draw 4 cards, discard 1 card.
  Expected: Player draws 4 cards, then discards 1 card of choice. Hand size = 1 + 4 - 1 = 4.

  - [ ] Sim - [ ] N/A — **Test: Acrobatics discard triggers After Image**
  Setup: Player has Acrobatics and 2 other cards in hand, 3 energy, 0 block. After Image power active. Draw pile has 5 cards.
  Actions: Play Acrobatics. Draw 3 cards, discard 1 card.
  Expected: Player draws 3 cards, discards 1 card. After Image triggers granting 1 BLK.

- **Accuracy** [Y] — BGAccuracy — Power, Common, Cost 1
  Your SHIV deal +1 damage.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] N/A — **Test: Accuracy boosts SHIV bonus damage on Slice**
  Setup: Player has Accuracy and Slice in hand, 3 energy, 1 SHIV. Enemy has 10 HP.
  Actions: Play Accuracy. Then play Slice targeting enemy.
  Expected: Accuracy is now active. Slice deals 1 HIT + 1 SHIV bonus + 1 Accuracy bonus = 3 damage. Enemy now at 7 HP.

  - [ ] Sim - [ ] N/A — **Test: Accuracy stacks with multiple plays**
  Setup: Player has 2 Accuracy cards and Slice in hand, 3 energy, 1 SHIV. Enemy has 10 HP.
  Actions: Play first Accuracy. Play second Accuracy. Play Slice targeting enemy.
  Expected: Slice deals 1 HIT + 1 SHIV bonus + 2 Accuracy bonus = 4 damage. Enemy now at 6 HP.

  - [ ] Sim - [ ] Live — **Test: Upgraded Accuracy costs 0 energy**
  Setup: Player has Accuracy+ in hand, 0 energy.
  Actions: Play Accuracy+.
  Expected: Accuracy power becomes active. Player energy remains 0.

- **After Image** [Y] — BGAfterImage — Power, Common, Cost 1
  Whenever you discard one or more cards during your turn, 1 BLK.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] N/A — **Test: After Image triggers on discard from Survivor**
  Setup: Player has After Image, Survivor, and Strike in hand, 3 energy, 0 block.
  Actions: Play After Image. Play Survivor, discard Strike.
  Expected: After Image becomes active. Survivor grants 2 BLK. Discarding Strike triggers After Image for 1 BLK. Total block = 3.

  - [ ] Sim - [ ] N/A — **Test: After Image triggers once per discard event, not per card discarded**
  Setup: Player has After Image active, Acrobatics and 3 other cards in hand, 3 energy, 0 block. Draw pile has 5 cards.
  Actions: Play Acrobatics. Draw 3 cards, discard 1 card.
  Expected: After Image triggers once for the discard event, granting 1 BLK total (not 1 BLK per card if multiple were discarded).

  - [ ] Sim - [ ] Live — **Test: Upgraded After Image costs 0 energy**
  Setup: Player has After Image+ in hand, 0 energy.
  Actions: Play After Image+.
  Expected: After Image power becomes active. Player energy remains 0.

  - [ ] Sim - [ ] N/A — **Test: After Image does not trigger on exhaust**
  Setup: Player has After Image active, Poisoned Stab in hand, 3 energy, 0 block. Enemy has 10 HP.
  Actions: Play Poisoned Stab targeting enemy.
  Expected: Poisoned Stab is exhausted (not discarded). After Image does NOT trigger. Player block remains 0 (aside from any other sources).
