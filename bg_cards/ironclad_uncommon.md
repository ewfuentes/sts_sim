# Ironclad (BGRed) — Uncommon

- **Uppercut** [Y] — BGUppercut — Attack, Uncommon, Cost 2
  3 HIT VULN WEAK.
  *Upgrade: 3 HIT VULN VULN WEAK.*

  - [ ] Sim - [ ] Live — **Test: Basic Uppercut deals damage and applies debuffs**
  Setup: Player has 3 energy, Uppercut in hand. Enemy has 10 HP, no block, no debuffs.
  Actions: Play Uppercut targeting enemy.
  Expected: Enemy loses 3 HP (3 HIT = 3 damage), enemy has 1 VULN and 1 WEAK applied. Player spent 2 energy.

  - [ ] Sim - [ ] Live — **Test: Uppercut with Strength adds damage per HIT**
  Setup: Player has 3 energy, 2 STR, Uppercut in hand. Enemy has 15 HP, no block.
  Actions: Play Uppercut targeting enemy.
  Expected: Enemy loses 9 HP (3 HIT, each HIT deals 1+2 STR = 3 damage, so 3x3 = 9). Enemy has 1 VULN and 1 WEAK.

  - [ ] Sim - [ ] Live — **Test: Upgraded Uppercut applies double VULN**
  Setup: Player has 3 energy, Uppercut+ in hand. Enemy has 10 HP, no debuffs.
  Actions: Play Uppercut+ targeting enemy.
  Expected: Enemy loses 3 HP. Enemy has 2 VULN and 1 WEAK applied.

- **Entrench** [Y] — BGEntrench — Skill, Uncommon, Cost 2
  Double your BLK. (Max block is 20 BLK.) Exhaust.
  *Upgrade: Double your BLK. (Max block is 20 BLK.) (No longer Exhausts.)*

  - [ ] Sim - [ ] Live — **Test: Basic Entrench doubles existing block and exhausts**
  Setup: Player has 3 energy, 4 BLK, Entrench in hand.
  Actions: Play Entrench.
  Expected: Player now has 8 BLK. Entrench is moved to the exhaust pile.

  - [ ] Sim - [ ] Live — **Test: Entrench respects 20 BLK cap**
  Setup: Player has 3 energy, 12 BLK, Entrench in hand.
  Actions: Play Entrench.
  Expected: Player now has 20 BLK (doubled would be 24, capped at 20). Entrench is exhausted.

  - [ ] Sim - [ ] Live — **Test: Entrench with zero block does nothing**
  Setup: Player has 3 energy, 0 BLK, Entrench in hand.
  Actions: Play Entrench.
  Expected: Player still has 0 BLK. Entrench is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Entrench does not exhaust**
  Setup: Player has 3 energy, 5 BLK, Entrench+ in hand.
  Actions: Play Entrench+.
  Expected: Player now has 10 BLK. Entrench+ goes to discard pile (not exhausted).

- **Shockwave** [Y] — BGShockwave — Skill, Uncommon, Cost 2
  AOE VULN WEAK. Exhaust.
  *Upgrade: AOE VULN WEAK WEAK. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic Shockwave applies debuffs to all enemies**
  Setup: Player has 3 energy, Shockwave in hand. Two enemies present, no debuffs.
  Actions: Play Shockwave.
  Expected: Both enemies gain 1 VULN and 1 WEAK. Shockwave is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Shockwave applies extra WEAK**
  Setup: Player has 3 energy, Shockwave+ in hand. Two enemies present, no debuffs.
  Actions: Play Shockwave+.
  Expected: Both enemies gain 1 VULN and 2 WEAK. Shockwave+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Shockwave stacks with existing debuffs**
  Setup: Player has 3 energy, Shockwave in hand. Enemy already has 1 VULN. Second enemy has no debuffs.
  Actions: Play Shockwave.
  Expected: First enemy now has 2 VULN and 1 WEAK. Second enemy has 1 VULN and 1 WEAK. Shockwave is exhausted.

- **Whirlwind** [Y] — BGWhirlwind — Attack, Uncommon, Cost -1
  Deal AOE 1 HIT X times.
  *Upgrade: Deal AOE 1 HIT X+1 times.*

  - [ ] Sim - [ ] Live — **Test: Whirlwind spends all energy and hits all enemies**
  Setup: Player has 3 energy, Whirlwind in hand. Two enemies, each with 10 HP.
  Actions: Play Whirlwind.
  Expected: Each enemy loses 3 HP (1 HIT x 3 energy = 3 damage each). Player has 0 energy remaining.

  - [ ] Sim - [ ] Live — **Test: Whirlwind with 0 energy does nothing**
  Setup: Player has 0 energy, Whirlwind in hand. Enemy has 10 HP.
  Actions: Play Whirlwind.
  Expected: Enemy takes 0 damage. Player has 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Whirlwind hits X+1 times**
  Setup: Player has 2 energy, Whirlwind+ in hand. Enemy has 10 HP, no block.
  Actions: Play Whirlwind+.
  Expected: Enemy loses 3 HP (1 HIT x (2+1) = 3 damage). Player has 0 energy.

  - [ ] Sim - [ ] Live — **Test: Whirlwind with Strength scales per HIT**
  Setup: Player has 2 energy, 1 STR, Whirlwind in hand. Enemy has 10 HP.
  Actions: Play Whirlwind.
  Expected: Enemy loses 4 HP (each HIT deals 1+1 STR = 2 damage, x 2 hits = 4 damage). Player has 0 energy.

- **Battle Trance** [Y] — BGBattle Trance — Skill, Uncommon, Cost 0
  Draw 3 cards.
  *Upgrade: Draw 4 cards.*

  - [ ] Sim - [ ] Live — **Test: Basic Battle Trance draws 3 cards for free**
  Setup: Player has 3 energy, Battle Trance in hand. Draw pile has 5 cards.
  Actions: Play Battle Trance.
  Expected: Player draws 3 cards from draw pile. Player still has 3 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Battle Trance draws 4 cards**
  Setup: Player has 3 energy, Battle Trance+ in hand. Draw pile has 5 cards.
  Actions: Play Battle Trance+.
  Expected: Player draws 4 cards from draw pile. Player still has 3 energy.

  - [ ] Sim - [ ] Live — **Test: Battle Trance with fewer cards in draw pile than needed**
  Setup: Player has 3 energy, Battle Trance in hand. Draw pile has 1 card. Discard pile has 5 cards.
  Actions: Play Battle Trance.
  Expected: Player draws 1 card from draw pile, discard pile is shuffled into draw pile, then player draws 2 more cards.

- **Burning Pact** [Y] — BGBurning Pact — Skill, Uncommon, Cost 1
  Exhaust a card. Draw 2 cards.
  *Upgrade: Exhaust a card. Draw 3 cards.*

  - [ ] Sim - [ ] Live — **Test: Basic Burning Pact exhausts a card and draws 2**
  Setup: Player has 3 energy, Burning Pact and a Strike in hand. Draw pile has 5 cards.
  Actions: Play Burning Pact, choose Strike to exhaust.
  Expected: Strike is moved to the exhaust pile. Player draws 2 cards. Player spent 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Burning Pact draws 3 cards**
  Setup: Player has 3 energy, Burning Pact+ and a Defend in hand. Draw pile has 5 cards.
  Actions: Play Burning Pact+, choose Defend to exhaust.
  Expected: Defend is moved to exhaust pile. Player draws 3 cards. Player spent 1 energy.

  - [ ] Sim - [ ] Live — **Test: Burning Pact synergy with exhaust-trigger powers**
  Setup: Player has Dark Embrace power active, 3 energy, Burning Pact and a Strike in hand. Draw pile has 5 cards.
  Actions: Play Burning Pact, choose Strike to exhaust.
  Expected: Strike is exhausted (triggers Dark Embrace: draw 1 card). Burning Pact draws 2 cards. Player draws 3 total cards.

- **Carnage** [Y] — BGCarnage — Attack, Uncommon, Cost 2
  Ethereal. 4 HIT.
  *Upgrade: Ethereal. 6 HIT.*

  - [ ] Sim - [ ] Live — **Test: Basic Carnage deals 4 damage**
  Setup: Player has 3 energy, Carnage in hand. Enemy has 10 HP, no block.
  Actions: Play Carnage targeting enemy.
  Expected: Enemy loses 4 HP (4 HIT = 4 damage). Player spent 2 energy.

  - [ ] Sim - [ ] Live — **Test: Carnage is exhausted if not played (Ethereal)**
  Setup: Player has 3 energy, Carnage in hand along with other cards.
  Actions: Do not play Carnage. End turn.
  Expected: Carnage is exhausted at end of turn because it is Ethereal.

  - [ ] Sim - [ ] Live — **Test: Upgraded Carnage deals 6 damage**
  Setup: Player has 3 energy, Carnage+ in hand. Enemy has 10 HP, no block.
  Actions: Play Carnage+ targeting enemy.
  Expected: Enemy loses 6 HP (6 HIT = 6 damage).

- **Blood for Blood** [Y] — BGBlood for Blood — Attack, Uncommon, Cost 4
  Costs 1 Energy(R) if you lost HP this combat. 4 HIT.
  *Upgrade: Costs 0 Energy(R) if you lost HP this combat. 4 HIT.*

  - [ ] Sim - [ ] Live — **Test: Blood for Blood at full cost when no HP lost**
  Setup: Player has not lost HP this combat, has 4 energy, Blood for Blood in hand. Enemy has 10 HP.
  Actions: Play Blood for Blood targeting enemy.
  Expected: Enemy loses 4 HP. Player spent 4 energy.

  - [ ] Sim - [ ] Live — **Test: Blood for Blood costs 1 after losing HP**
  Setup: Player has lost HP this combat, has 3 energy, Blood for Blood in hand. Enemy has 10 HP.
  Actions: Play Blood for Blood targeting enemy.
  Expected: Enemy loses 4 HP. Player spent 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Blood for Blood costs 0 after losing HP**
  Setup: Player has lost HP this combat, has 3 energy, Blood for Blood+ in hand. Enemy has 10 HP.
  Actions: Play Blood for Blood+ targeting enemy.
  Expected: Enemy loses 4 HP. Player spent 0 energy.

- **Disarm** [Y] — BGDisarm — Skill, Uncommon, Cost 1
  WEAK WEAK. Exhaust.
  *Upgrade: WEAK WEAK WEAK. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic Disarm applies 2 WEAK and exhausts**
  Setup: Player has 3 energy, Disarm in hand. Enemy has no debuffs.
  Actions: Play Disarm targeting enemy.
  Expected: Enemy gains 2 WEAK. Disarm is moved to exhaust pile. Player spent 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Disarm applies 3 WEAK**
  Setup: Player has 3 energy, Disarm+ in hand. Enemy has no debuffs.
  Actions: Play Disarm+ targeting enemy.
  Expected: Enemy gains 3 WEAK. Disarm+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Disarm stacks WEAK on an already-weakened enemy**
  Setup: Player has 3 energy, Disarm in hand. Enemy already has 1 WEAK.
  Actions: Play Disarm targeting enemy.
  Expected: Enemy now has 3 WEAK (1 existing + 2 from Disarm). Disarm is exhausted.

- **Flame Barrier** [Y] — BGFlame Barrier — Skill, Uncommon, Cost 2
  3 BLK. Deal 1 damage to all enemies that intend to attack you for each HIT in their next action.
  *Upgrade: 4 BLK.*

  - [ ] Sim - [ ] Live — **Test: Flame Barrier grants block and retaliates against attackers**
  Setup: Player has 3 energy, Flame Barrier in hand. Enemy intends to attack with 3 HIT.
  Actions: Play Flame Barrier. End turn. Enemy attacks.
  Expected: Player gains 3 BLK. Enemy takes 3 damage (1 damage per HIT in its attack action, which has 3 HIT).

  - [ ] Sim - [ ] Live — **Test: Flame Barrier does not retaliate against non-attacking enemies**
  Setup: Player has 3 energy, Flame Barrier in hand. Enemy intends to buff (not attack).
  Actions: Play Flame Barrier. End turn.
  Expected: Player gains 3 BLK. Enemy takes 0 damage (no attack intent).

  - [ ] Sim - [ ] Live — **Test: Upgraded Flame Barrier grants 4 BLK**
  Setup: Player has 3 energy, Flame Barrier+ in hand. Enemy intends to attack with 2 HIT.
  Actions: Play Flame Barrier+. End turn. Enemy attacks.
  Expected: Player gains 4 BLK. Enemy takes 2 damage (1 per HIT in its attack).

- **Ghostly Armor** [Y] — BGGhostly Armor — Skill, Uncommon, Cost 1
  Ethereal. 2 BLK to any player.
  *Upgrade: Ethereal. 3 BLK to any player.*

  - [ ] Sim - [ ] Live — **Test: Ghostly Armor grants 2 block to self**
  Setup: Player has 3 energy, Ghostly Armor in hand, 0 BLK.
  Actions: Play Ghostly Armor targeting self.
  Expected: Player gains 2 BLK. Player spent 1 energy.

  - [ ] Sim - [ ] Live — **Test: Ghostly Armor is exhausted if not played (Ethereal)**
  Setup: Player has 3 energy, Ghostly Armor in hand.
  Actions: Do not play Ghostly Armor. End turn.
  Expected: Ghostly Armor is exhausted at end of turn because it is Ethereal.

  - [ ] Sim - [ ] Live — **Test: Upgraded Ghostly Armor grants 3 block**
  Setup: Player has 3 energy, Ghostly Armor+ in hand, 0 BLK.
  Actions: Play Ghostly Armor+ targeting self.
  Expected: Player gains 3 BLK. Player spent 1 energy.

- **Inflame** [Y] — BGInflame — Power, Uncommon, Cost 2
  When played, gain STR.
  *Upgrade: Cost 2 to 1.*

  - [ ] Sim - [ ] Live — **Test: Basic Inflame grants 1 STR**
  Setup: Player has 3 energy, 0 STR, Inflame in hand.
  Actions: Play Inflame.
  Expected: Player gains 1 STR. Player spent 2 energy. Inflame is removed from play (Power).

  - [ ] Sim - [ ] Live — **Test: Inflame stacks with existing STR**
  Setup: Player has 3 energy, 2 STR, Inflame in hand.
  Actions: Play Inflame.
  Expected: Player now has 3 STR.

  - [ ] Sim - [ ] Live — **Test: Upgraded Inflame costs 1 energy**
  Setup: Player has 1 energy, 0 STR, Inflame+ in hand.
  Actions: Play Inflame+.
  Expected: Player gains 1 STR. Player spent 1 energy.

- **Metallicize** [Y] — BGMetallicize — Power, Uncommon, Cost 1
  End of turn: 1 BLK.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Metallicize grants 1 BLK at end of turn**
  Setup: Player has 3 energy, 0 BLK, Metallicize in hand.
  Actions: Play Metallicize. End turn.
  Expected: Player gains 1 BLK at end of turn from Metallicize.

  - [ ] Sim - [ ] Live — **Test: Metallicize triggers every turn**
  Setup: Player has Metallicize power active, 0 BLK.
  Actions: End turn 1. Start turn 2 (block resets to 0). End turn 2.
  Expected: Player gains 1 BLK at end of each turn. After ending turn 2, player has 1 BLK.

  - [ ] Sim - [ ] Live — **Test: Upgraded Metallicize costs 0 energy**
  Setup: Player has 0 energy, Metallicize+ in hand.
  Actions: Play Metallicize+.
  Expected: Metallicize+ is played for 0 energy. At end of turn, player gains 1 BLK.

- **Power Through** [Y] — BGPower Through — Skill, Uncommon, Cost 1
  3 BLK to any player. DAZED.
  *Upgrade: 4 BLK to any player. DAZED.*

  - [ ] Sim - [ ] Live — **Test: Basic Power Through grants block and adds DAZED**
  Setup: Player has 3 energy, Power Through in hand, 0 BLK. Discard pile has 2 cards.
  Actions: Play Power Through targeting self.
  Expected: Player gains 3 BLK. 1 DAZED status card is added to the discard pile. Player spent 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Power Through grants 4 block**
  Setup: Player has 3 energy, Power Through+ in hand, 0 BLK.
  Actions: Play Power Through+ targeting self.
  Expected: Player gains 4 BLK. 1 DAZED is added to discard pile.

  - [ ] Sim - [ ] Live — **Test: Power Through DAZED interacts with Evolve**
  Setup: Player has Evolve power active, 3 energy, Power Through in hand. Draw pile has 5 cards.
  Actions: Play Power Through targeting self. Next turn, draw DAZED from the deck.
  Expected: Player gains 3 BLK. DAZED is added to discard pile. When DAZED is drawn on a future turn, Evolve triggers and player draws 1 additional card.

- **Rampage** [Y] — BGRampage — Attack, Uncommon, Cost 1
  X HIT. X is the # of cards in your Exhaust pile.
  *Upgrade: Exhaust a card. X HIT. X is the # of cards in your Exhaust pile.*

  - [ ] Sim - [ ] Live — **Test: Rampage deals damage equal to exhaust pile size**
  Setup: Player has 3 energy, Rampage in hand. Exhaust pile has 3 cards. Enemy has 10 HP.
  Actions: Play Rampage targeting enemy.
  Expected: Enemy loses 3 HP (3 HIT, since exhaust pile had 3 cards).

  - [ ] Sim - [ ] Live — **Test: Rampage with empty exhaust pile deals 0 damage**
  Setup: Player has 3 energy, Rampage in hand. Exhaust pile is empty. Enemy has 10 HP.
  Actions: Play Rampage targeting enemy.
  Expected: Enemy loses 0 HP (0 HIT).

  - [ ] Sim - [ ] Live — **Test: Upgraded Rampage exhausts a card first, then counts**
  Setup: Player has 3 energy, Rampage+ and a Strike in hand. Exhaust pile has 2 cards. Enemy has 10 HP.
  Actions: Play Rampage+ targeting enemy, choose Strike to exhaust.
  Expected: Strike is exhausted (exhaust pile now has 3 cards). Enemy loses 3 HP (3 HIT).

  - [ ] Sim - [ ] Live — **Test: Rampage scales with Strength**
  Setup: Player has 3 energy, 2 STR, Rampage in hand. Exhaust pile has 2 cards. Enemy has 10 HP.
  Actions: Play Rampage targeting enemy.
  Expected: Enemy loses 6 HP (2 HIT, each dealing 1+2 STR = 3 damage, so 2x3 = 6).

- **Second Wind** [Y] — BGSecond Wind — Skill, Uncommon, Cost 1
  Exhaust all non-Attack cards in your hand. Gain 1 BLK for each card Exhausted this way.
  *Upgrade: Gain 2 BLK for each card Exhausted.*

  - [ ] Sim - [ ] Live — **Test: Second Wind exhausts non-Attacks and gains block**
  Setup: Player has 3 energy, Second Wind, 2 Defends, and 1 Strike in hand. 0 BLK.
  Actions: Play Second Wind.
  Expected: 2 Defends are exhausted. Player gains 2 BLK (1 per card exhausted). Strike remains in hand. Second Wind itself is discarded (it is played, not exhausted by its own effect).

  - [ ] Sim - [ ] Live — **Test: Second Wind with only Attacks in hand**
  Setup: Player has 3 energy, Second Wind and 3 Strikes in hand. 0 BLK.
  Actions: Play Second Wind.
  Expected: No cards are exhausted (Strikes are Attacks). Player gains 0 BLK.

  - [ ] Sim - [ ] Live — **Test: Upgraded Second Wind gains 2 BLK per card exhausted**
  Setup: Player has 3 energy, Second Wind+, 3 Defends, and 1 Strike in hand. 0 BLK.
  Actions: Play Second Wind+.
  Expected: 3 Defends are exhausted. Player gains 6 BLK (2 per card x 3 cards).

- **Sentinel** [Y] — BGSentinel — Skill, Uncommon, Cost 1
  2 BLK to any player. If this card is Exhausted, gain Energy(R) Energy(R).
  *Upgrade: 3 BLK to any player. If this card is Exhausted, gain Energy(R) Energy(R) Energy(R).*

  - [ ] Sim - [ ] Live — **Test: Basic Sentinel grants 2 block when played normally**
  Setup: Player has 3 energy, Sentinel in hand, 0 BLK.
  Actions: Play Sentinel targeting self.
  Expected: Player gains 2 BLK. Player spent 1 energy. Sentinel goes to discard pile. No energy gained (it was not exhausted).

  - [ ] Sim - [ ] Live — **Test: Sentinel grants energy when exhausted by another effect**
  Setup: Player has 3 energy, Second Wind and Sentinel in hand, 0 BLK.
  Actions: Play Second Wind (Sentinel is a non-Attack, so it gets exhausted).
  Expected: Sentinel is exhausted, triggering its effect: player gains 2 energy. Player also gains 1 BLK from Second Wind for exhausting Sentinel.

  - [ ] Sim - [ ] Live — **Test: Upgraded Sentinel grants 3 BLK and 3 energy on exhaust**
  Setup: Player has 3 energy, Sentinel+ in hand, 0 BLK. Player also has Burning Pact in hand.
  Actions: Play Burning Pact, choose Sentinel+ to exhaust.
  Expected: Sentinel+ is exhausted, player gains 3 energy. Player also draws 2 cards from Burning Pact.

- **Sever Soul** [Y] — BGSever Soul — Attack, Uncommon, Cost 2
  3 HIT. Exhaust 1 card in your hand.
  *Upgrade: 4 HIT. Exhaust 1 or 2 cards in your hand.*

  - [ ] Sim - [ ] Live — **Test: Basic Sever Soul deals damage and exhausts a card**
  Setup: Player has 3 energy, Sever Soul and a Defend in hand. Enemy has 10 HP.
  Actions: Play Sever Soul targeting enemy, choose Defend to exhaust.
  Expected: Enemy loses 3 HP (3 HIT). Defend is moved to exhaust pile.

  - [ ] Sim - [ ] Live — **Test: Upgraded Sever Soul deals 4 damage and can exhaust 2 cards**
  Setup: Player has 3 energy, Sever Soul+ and 2 Defends in hand. Enemy has 10 HP.
  Actions: Play Sever Soul+ targeting enemy, choose both Defends to exhaust.
  Expected: Enemy loses 4 HP (4 HIT). Both Defends are moved to exhaust pile.

  - [ ] Sim - [ ] Live — **Test: Sever Soul with Strength**
  Setup: Player has 3 energy, 2 STR, Sever Soul and a Strike in hand. Enemy has 15 HP.
  Actions: Play Sever Soul targeting enemy, choose Strike to exhaust.
  Expected: Enemy loses 9 HP (3 HIT, each dealing 1+2 STR = 3 damage, so 3x3 = 9). Strike is exhausted.

- **Spot Weakness** [Y] — BGSpot Weakness — Skill, Uncommon, Cost 1
  1 STR to any player if the die is on [1] [2] or [3].
  *Upgrade: 1 STR to any player if the die is on [1] [2] [3] or [4].*

  - [ ] Sim - [ ] Live — **Test: Spot Weakness grants STR when die is on valid face**
  Setup: Player has 3 energy, 0 STR, Spot Weakness in hand. Die is showing [2].
  Actions: Play Spot Weakness targeting self.
  Expected: Player gains 1 STR. Player spent 1 energy.

  - [ ] Sim - [ ] Live — **Test: Spot Weakness fails when die is on invalid face**
  Setup: Player has 3 energy, 0 STR, Spot Weakness in hand. Die is showing [5].
  Actions: Play Spot Weakness targeting self.
  Expected: Player does not gain STR. Player spent 1 energy. Card is still consumed.

  - [ ] Sim - [ ] Live — **Test: Upgraded Spot Weakness succeeds on die face [4]**
  Setup: Player has 3 energy, 0 STR, Spot Weakness+ in hand. Die is showing [4].
  Actions: Play Spot Weakness+ targeting self.
  Expected: Player gains 1 STR. Player spent 1 energy.

- **Rage** [Y] — BGRage — Skill, Uncommon, Cost 1
  1 BLK for each Attack in your hand.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Rage grants block equal to number of Attacks in hand**
  Setup: Player has 3 energy, Rage, 2 Strikes, and 1 Defend in hand. 0 BLK.
  Actions: Play Rage.
  Expected: Player gains 2 BLK (2 Attacks in hand: the 2 Strikes). Player spent 1 energy.

  - [ ] Sim - [ ] Live — **Test: Rage with no Attacks in hand**
  Setup: Player has 3 energy, Rage and 3 Defends in hand. 0 BLK.
  Actions: Play Rage.
  Expected: Player gains 0 BLK (no Attacks in hand).

  - [ ] Sim - [ ] Live — **Test: Upgraded Rage costs 0 energy**
  Setup: Player has 0 energy, Rage+ and 3 Strikes in hand. 0 BLK.
  Actions: Play Rage+.
  Expected: Player gains 3 BLK (3 Attacks in hand). Player spent 0 energy.

- **Combust** [Y] — BGCombust — Power, Uncommon, Cost 1
  Once per turn: Deal 1 damage to any row.
  *Upgrade: Deal 2 damage to any row.*

  - [ ] Sim - [ ] Live — **Test: Combust deals 1 damage once per turn**
  Setup: Player has 3 energy, Combust in hand. Enemy row has an enemy with 10 HP.
  Actions: Play Combust. Activate Combust targeting enemy row.
  Expected: All enemies in the targeted row take 1 damage.

  - [ ] Sim - [ ] Live — **Test: Combust can only fire once per turn**
  Setup: Player has Combust power active, already used this turn. Enemy has 9 HP.
  Actions: Attempt to activate Combust again.
  Expected: Combust cannot be activated a second time this turn. It refreshes at start of next turn.

  - [ ] Sim - [ ] Live — **Test: Upgraded Combust deals 2 damage**
  Setup: Player has 3 energy, Combust+ in hand. Enemy row has an enemy with 10 HP.
  Actions: Play Combust+. Activate Combust targeting enemy row.
  Expected: All enemies in the targeted row take 2 damage.

- **Dark Embrace** [Y] — BGDark Embrace — Power, Uncommon, Cost 2
  Whenever you Exhaust a card, draw a card.
  *Upgrade: Cost 2 to 1.*

  - [ ] Sim - [ ] Live — **Test: Dark Embrace draws a card on exhaust**
  Setup: Player has Dark Embrace power active. Player has a card in hand and 5 cards in draw pile. Player plays a card that exhausts another card.
  Actions: Exhaust a card (e.g., play Burning Pact, choose a card to exhaust).
  Expected: When the card is exhausted, Dark Embrace triggers and player draws 1 additional card.

  - [ ] Sim - [ ] Live — **Test: Dark Embrace triggers for each card exhausted**
  Setup: Player has Dark Embrace power active. Player has Second Wind and 2 Defends in hand. Draw pile has 5 cards.
  Actions: Play Second Wind (exhausts both Defends).
  Expected: Dark Embrace triggers twice (once per Defend exhausted), player draws 2 additional cards.

  - [ ] Sim - [ ] Live — **Test: Upgraded Dark Embrace costs 1 energy**
  Setup: Player has 1 energy, Dark Embrace+ in hand.
  Actions: Play Dark Embrace+.
  Expected: Dark Embrace+ is played for 1 energy.

- **Evolve** [Y] — BGEvolve — Power, Uncommon, Cost 1
  Whenever you draw DAZED, BURN, or SLIMED, draw 1 card.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Evolve triggers when drawing a DAZED**
  Setup: Player has Evolve power active. Draw pile has DAZED on top, then a Strike beneath it.
  Actions: Draw a card (start of turn or card draw effect).
  Expected: Player draws the DAZED. Evolve triggers and player draws 1 additional card (the Strike).

  - [ ] Sim - [ ] Live — **Test: Evolve triggers on BURN and SLIMED as well**
  Setup: Player has Evolve power active. Draw pile has BURN on top, then 2 other cards.
  Actions: Draw a card.
  Expected: Player draws BURN. Evolve triggers, player draws 1 additional card.

  - [ ] Sim - [ ] Live — **Test: Upgraded Evolve costs 0 energy**
  Setup: Player has 0 energy, Evolve+ in hand.
  Actions: Play Evolve+.
  Expected: Evolve+ is played for 0 energy.

- **Feel No Pain** [Y] — BGFeel No Pain — Power, Uncommon, Cost 1
  Whenever you Exhaust a card, 1 BLK.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Feel No Pain grants block on exhaust**
  Setup: Player has Feel No Pain power active, 0 BLK. Player has a card to exhaust.
  Actions: Exhaust a card (e.g., play a card with Exhaust keyword).
  Expected: Player gains 1 BLK from Feel No Pain trigger.

  - [ ] Sim - [ ] Live — **Test: Feel No Pain triggers for each card exhausted**
  Setup: Player has Feel No Pain power active, 0 BLK. Player has Second Wind and 3 Defends in hand.
  Actions: Play Second Wind (exhausts all 3 Defends).
  Expected: Feel No Pain triggers 3 times, player gains 3 BLK (1 per exhaust) plus 3 BLK from Second Wind itself = 6 BLK total.

  - [ ] Sim - [ ] Live — **Test: Upgraded Feel No Pain costs 0 energy**
  Setup: Player has 0 energy, Feel No Pain+ in hand.
  Actions: Play Feel No Pain+.
  Expected: Feel No Pain+ is played for 0 energy.

- **Fire Breathing** [Y] — BGFire Breathing — Power, Uncommon, Cost 1
  Whenever you draw DAZED, BURN, SLIMED or a Curse, deal 2 damage to any row.
  *Upgrade: Deal 3 damage to any row.*

  - [ ] Sim - [ ] Live — **Test: Fire Breathing deals damage when drawing a status card**
  Setup: Player has Fire Breathing power active. Draw pile has a DAZED on top. Enemy row has an enemy with 10 HP.
  Actions: Draw a card (drawing the DAZED).
  Expected: Fire Breathing triggers, dealing 2 damage to a chosen enemy row.

  - [ ] Sim - [ ] Live — **Test: Fire Breathing triggers on Curse cards**
  Setup: Player has Fire Breathing power active. Draw pile has a Curse card on top. Enemy with 10 HP.
  Actions: Draw a card (drawing the Curse).
  Expected: Fire Breathing triggers, dealing 2 damage to a chosen enemy row.

  - [ ] Sim - [ ] Live — **Test: Upgraded Fire Breathing deals 3 damage**
  Setup: Player has Fire Breathing+ power active. Draw pile has a DAZED on top. Enemy with 10 HP.
  Actions: Draw a card (drawing the DAZED).
  Expected: Fire Breathing+ triggers, dealing 3 damage to a chosen enemy row.

- **Rupture** [Y] — BGRupture — Power, Uncommon, Cost 1
  Gain STR. Lose 1 HP.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Basic Rupture grants STR and costs HP**
  Setup: Player has 3 energy, 0 STR, 50 HP. Rupture in hand.
  Actions: Play Rupture.
  Expected: Player gains 1 STR. Player loses 1 HP (now 49 HP). Player spent 1 energy.

  - [ ] Sim - [ ] Live — **Test: Rupture stacks with existing STR**
  Setup: Player has 3 energy, 2 STR, 50 HP. Rupture in hand.
  Actions: Play Rupture.
  Expected: Player now has 3 STR. Player loses 1 HP.

  - [ ] Sim - [ ] Live — **Test: Upgraded Rupture costs 0 energy**
  Setup: Player has 0 energy, 0 STR, 50 HP. Rupture+ in hand.
  Actions: Play Rupture+.
  Expected: Player gains 1 STR. Player loses 1 HP. Player spent 0 energy.
