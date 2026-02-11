# Ironclad (BGRed) — Common

- **Anger** [Y] — BGAnger — Attack, Common, Cost 0
  1 HIT. Put this card on top of your draw pile.
  *Upgrade: 2 HIT.*

  - [ ] Sim - [ ] Live — **Test: Base Anger deals 1 damage and goes to draw pile**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Anger in hand. Draw pile has 3 cards.
  Actions: Play Anger targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Anger is placed on top of draw pile (draw pile now has 4 cards with Anger on top). Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Anger deals 2 damage**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Anger+ in hand.
  Actions: Play Anger+ targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). Anger+ is placed on top of draw pile.

  - [ ] Sim - [ ] Live — **Test: Anger with Strength**
  Setup: Player has 3 energy, 1 STR. Enemy has 20 HP, 0 block. Anger in hand.
  Actions: Play Anger targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). 1 HIT + 1 STR = 2 damage.

- **Body Slam** [Y] — BGBody Slam — Attack, Common, Cost 1
  X HIT. X is equal to your BLK.
  *Upgrade: Cost 1 to 0. (Deals 0 damage.)*

  - [ ] Sim - [ ] Live — **Test: Body Slam deals damage equal to current block**
  Setup: Player has 3 energy, 5 block. Enemy has 20 HP, 0 block. Body Slam in hand.
  Actions: Play Body Slam targeting enemy.
  Expected: Enemy loses 5 HP (15 HP remaining). Player retains 5 block. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Body Slam with 0 block deals 0 damage**
  Setup: Player has 3 energy, 0 block. Enemy has 20 HP, 0 block. Body Slam in hand.
  Actions: Play Body Slam targeting enemy.
  Expected: Enemy loses 0 HP (20 HP remaining). Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Body Slam costs 0 energy**
  Setup: Player has 3 energy, 3 block. Enemy has 20 HP, 0 block. Body Slam+ in hand.
  Actions: Play Body Slam+ targeting enemy.
  Expected: Enemy loses 3 HP (17 HP remaining). Player spends 0 energy (3 remaining).

  - [ ] Sim - [ ] Live — **Test: Body Slam with Strength adds per HIT**
  Setup: Player has 3 energy, 4 block, 2 STR. Enemy has 20 HP, 0 block. Body Slam in hand.
  Actions: Play Body Slam targeting enemy.
  Expected: Enemy loses damage equal to 4 HIT + 2 STR per HIT = (1+2)*4 = 12 damage. Enemy at 8 HP.

- **Clash** [Y] — BGClash — Attack, Common, Cost 0
  Can only be played if every card in your hand is an Attack. 3 HIT.
  *Upgrade: 4 HIT.*

  - [ ] Sim - [ ] Live — **Test: Clash is playable when all cards in hand are Attacks**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Hand contains: Clash, Strike, Anger (all Attacks).
  Actions: Play Clash targeting enemy.
  Expected: Clash is playable. Enemy loses 3 HP (17 HP remaining). Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Clash cannot be played when hand contains non-Attack cards**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Hand contains: Clash, Strike, Defend (Defend is a Skill).
  Actions: Attempt to play Clash.
  Expected: Clash cannot be played. No cards are played, no energy spent.

  - [ ] Sim - [ ] Live — **Test: Upgraded Clash deals 4 damage**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Hand contains: Clash+, Strike (all Attacks).
  Actions: Play Clash+ targeting enemy.
  Expected: Enemy loses 4 HP (16 HP remaining). Player spends 0 energy.

- **Cleave** [Y] — BGCleave — Attack, Common, Cost 1
  AOE 2 HIT.
  *Upgrade: AOE 3 HIT.*

  - [ ] Sim - [ ] Live — **Test: Base Cleave hits all enemies for 2 damage each**
  Setup: Player has 3 energy. Enemy A has 15 HP, 0 block. Enemy B has 10 HP, 0 block. Cleave in hand.
  Actions: Play Cleave.
  Expected: Enemy A loses 2 HP (13 HP remaining). Enemy B loses 2 HP (8 HP remaining). Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Cleave hits all enemies for 3 damage each**
  Setup: Player has 3 energy. Enemy A has 15 HP. Enemy B has 10 HP. Cleave+ in hand.
  Actions: Play Cleave+.
  Expected: Enemy A loses 3 HP (12 HP remaining). Enemy B loses 3 HP (7 HP remaining).

  - [ ] Sim - [ ] Live — **Test: Cleave with Strength adds per HIT to each enemy**
  Setup: Player has 3 energy, 1 STR. Enemy A has 15 HP, 0 block. Enemy B has 10 HP, 0 block. Cleave in hand.
  Actions: Play Cleave.
  Expected: Each enemy takes 2 HIT with +1 STR per HIT = (1+1)*2 = 4 damage each. Enemy A at 11 HP. Enemy B at 6 HP.

- **Clothesline** [Y] — BGClothesline — Attack, Common, Cost 2
  3 HIT WEAK.
  *Upgrade: 4 HIT WEAK.*

  - [ ] Sim - [ ] Live — **Test: Base Clothesline deals 3 damage and applies Weak**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block, no debuffs. Clothesline in hand.
  Actions: Play Clothesline targeting enemy.
  Expected: Enemy loses 3 HP (17 HP remaining). Enemy gains 1 WEAK. Player spends 2 energy (1 remaining).

  - [ ] Sim - [ ] Live — **Test: Upgraded Clothesline deals 4 damage and applies Weak**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Clothesline+ in hand.
  Actions: Play Clothesline+ targeting enemy.
  Expected: Enemy loses 4 HP (16 HP remaining). Enemy gains 1 WEAK. Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Clothesline with Strength scales per HIT**
  Setup: Player has 3 energy, 2 STR. Enemy has 20 HP, 0 block. Clothesline in hand.
  Actions: Play Clothesline targeting enemy.
  Expected: 3 HIT with +2 STR per HIT = (1+2)*3 = 9 damage. Enemy at 11 HP. Enemy gains 1 WEAK.

- **Flex** [Y] — BGFlex — Skill, Common, Cost 0
  Gain STR. Lose that STR at end of turn. Exhaust.
  *Upgrade: Gain STR. Lose that STR at end of turn. (No longer Exhausts.)*

  - [ ] Sim - [ ] Live — **Test: Base Flex grants temporary Strength and exhausts**
  Setup: Player has 3 energy, 0 STR. Flex in hand. Enemy has 20 HP.
  Actions: Play Flex. Play Strike targeting enemy.
  Expected: After playing Flex, player has 1 STR. Flex is exhausted (moved to exhaust pile, not discard). Strike deals 1 HIT + 1 STR = 2 damage. At end of turn, player loses 1 STR (back to 0 STR).

  - [ ] Sim - [ ] Live — **Test: Flex Strength is lost at end of turn**
  Setup: Player has 3 energy, 0 STR. Flex in hand.
  Actions: Play Flex. End turn.
  Expected: After playing Flex, player has 1 STR. After end of turn, player has 0 STR.

  - [ ] Sim - [ ] Live — **Test: Upgraded Flex does not exhaust**
  Setup: Player has 3 energy, 0 STR. Flex+ in hand.
  Actions: Play Flex+.
  Expected: Player gains 1 STR. Flex+ goes to discard pile (not exhaust pile). At end of turn, player loses 1 STR.

- **Heavy Blade** [Y] — BGHeavy Blade — Attack, Common, Cost 2
  3 HIT. Each STR adds +3 damage to this card (instead of +1).
  *Upgrade: Each STR adds +5 damage (instead of +1).*

  - [ ] Sim - [ ] Live — **Test: Base Heavy Blade deals 3 damage with no Strength**
  Setup: Player has 3 energy, 0 STR. Enemy has 20 HP, 0 block. Heavy Blade in hand.
  Actions: Play Heavy Blade targeting enemy.
  Expected: Enemy loses 3 HP (17 HP remaining). Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Heavy Blade with Strength triples STR bonus**
  Setup: Player has 3 energy, 2 STR. Enemy has 30 HP, 0 block. Heavy Blade in hand.
  Actions: Play Heavy Blade targeting enemy.
  Expected: 3 HIT with +3 per STR per HIT. Each HIT deals 1 + (2*3) = 7 damage. Total = 7*3 = 21 damage. Enemy at 9 HP.

  - [ ] Sim - [ ] Live — **Test: Upgraded Heavy Blade quintuples STR bonus**
  Setup: Player has 3 energy, 2 STR. Enemy has 40 HP, 0 block. Heavy Blade+ in hand.
  Actions: Play Heavy Blade+ targeting enemy.
  Expected: 3 HIT with +5 per STR per HIT. Each HIT deals 1 + (2*5) = 11 damage. Total = 11*3 = 33 damage. Enemy at 7 HP.

- **Iron Wave** [Y] — BGIron Wave — Attack, Common, Cost 1
  1 HIT 1 BLK.
  *Upgrade: 2 HIT 1 BLK - or - 1 HIT 2 BLK.*

  - [ ] Sim - [ ] Live — **Test: Base Iron Wave deals 1 damage and gains 1 block**
  Setup: Player has 3 energy, 0 block. Enemy has 20 HP, 0 block. Iron Wave in hand.
  Actions: Play Iron Wave targeting enemy.
  Expected: Enemy loses 1 HP (19 HP remaining). Player gains 1 block. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Iron Wave with Strength increases HIT damage**
  Setup: Player has 3 energy, 0 block, 1 STR. Enemy has 20 HP, 0 block. Iron Wave in hand.
  Actions: Play Iron Wave targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). 1 HIT + 1 STR = 2 damage. Player gains 1 block.

  - [ ] Sim - [ ] Live — **Test: Upgraded Iron Wave offers choice of 2 HIT 1 BLK or 1 HIT 2 BLK**
  Setup: Player has 3 energy, 0 block. Enemy has 20 HP, 0 block. Iron Wave+ in hand.
  Actions: Play Iron Wave+ targeting enemy, choosing the 2 HIT 1 BLK option.
  Expected: Enemy loses 2 HP (18 HP remaining). Player gains 1 block. Player spends 1 energy.

- **Perfected Strike** [Y] — BGPerfected Strike — Attack, Common, Cost 2
  3 HIT. +1 damage for each other card in your hand containing 'Strike'.
  *Upgrade: +2 damage per Strike card.*

  - [ ] Sim - [ ] Live — **Test: Base Perfected Strike with no other Strikes in hand**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Hand contains: Perfected Strike, Defend, Bash.
  Actions: Play Perfected Strike targeting enemy.
  Expected: Enemy loses 3 HP (17 HP remaining). No other Strike cards in hand, so no bonus damage. Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Perfected Strike with 2 other Strikes in hand**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Hand contains: Perfected Strike, Strike, Twin Strike, Defend.
  Actions: Play Perfected Strike targeting enemy.
  Expected: 2 other cards contain 'Strike', so +2 bonus damage. Total = 3 + 2 = 5 HP lost. Enemy at 15 HP.

  - [ ] Sim - [ ] Live — **Test: Upgraded Perfected Strike with 2 other Strikes in hand**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Hand contains: Perfected Strike+, Strike, Pommel Strike, Bash.
  Actions: Play Perfected Strike+ targeting enemy.
  Expected: 2 other cards contain 'Strike', +2 each = +4 bonus damage. Total = 3 + 4 = 7 HP lost. Enemy at 13 HP.

- **Pommel Strike** [Y] — BGPommel Strike — Attack, Common, Cost 1
  2 HIT. Draw a card.
  *Upgrade: 2 HIT. Draw 2 cards.*

  - [ ] Sim - [ ] Live — **Test: Base Pommel Strike deals 2 damage and draws 1 card**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Pommel Strike in hand. Draw pile has 5 cards.
  Actions: Play Pommel Strike targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). Player draws 1 card from draw pile. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Pommel Strike draws 2 cards**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Pommel Strike+ in hand. Draw pile has 5 cards.
  Actions: Play Pommel Strike+ targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). Player draws 2 cards from draw pile. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Pommel Strike with empty draw pile triggers reshuffle**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Pommel Strike in hand. Draw pile is empty. Discard pile has 3 cards.
  Actions: Play Pommel Strike targeting enemy.
  Expected: Enemy loses 2 HP. Discard pile is shuffled into draw pile, then player draws 1 card.

- **Shrug It Off** [Y] — BGShrug It Off — Skill, Common, Cost 1
  2 BLK. Draw 1 card.
  *Upgrade: 3 BLK. Draw 1 card.*

  - [ ] Sim - [ ] Live — **Test: Base Shrug It Off grants 2 block and draws 1 card**
  Setup: Player has 3 energy, 0 block. Shrug It Off in hand. Draw pile has 5 cards.
  Actions: Play Shrug It Off.
  Expected: Player gains 2 block. Player draws 1 card. Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Upgraded Shrug It Off grants 3 block**
  Setup: Player has 3 energy, 0 block. Shrug It Off+ in hand. Draw pile has 5 cards.
  Actions: Play Shrug It Off+.
  Expected: Player gains 3 block. Player draws 1 card. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Shrug It Off block stacks with existing block**
  Setup: Player has 3 energy, 3 block. Shrug It Off in hand. Draw pile has 5 cards.
  Actions: Play Shrug It Off.
  Expected: Player gains 2 additional block (now at 5 block total). Player draws 1 card.

- **Twin Strike** [Y] — BGTwin Strike — Attack, Common, Cost 1
  1 HIT 1 HIT.
  *Upgrade: 2 HIT 2 HIT.*

  - [ ] Sim - [ ] Live — **Test: Base Twin Strike deals 2 separate hits of 1 damage each**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Twin Strike in hand.
  Actions: Play Twin Strike targeting enemy.
  Expected: Enemy takes 1 damage, then 1 damage again. Enemy at 18 HP total. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Twin Strike against enemy with block**
  Setup: Player has 3 energy. Enemy has 20 HP, 1 block. Twin Strike in hand.
  Actions: Play Twin Strike targeting enemy.
  Expected: First HIT removes 1 block (0 block remaining, 0 overflow damage). Second HIT deals 1 damage to HP. Enemy at 19 HP, 0 block.

  - [ ] Sim - [ ] Live — **Test: Upgraded Twin Strike deals 2 damage per hit**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Twin Strike+ in hand.
  Actions: Play Twin Strike+ targeting enemy.
  Expected: Enemy takes 2 damage, then 2 damage again. Enemy at 16 HP total.

  - [ ] Sim - [ ] Live — **Test: Twin Strike with Strength adds per HIT**
  Setup: Player has 3 energy, 1 STR. Enemy has 20 HP, 0 block. Twin Strike in hand.
  Actions: Play Twin Strike targeting enemy.
  Expected: Each HIT deals 1 + 1 STR = 2 damage. Two hits = 4 total damage. Enemy at 16 HP.

- **Wild Strike** [Y] — BGWild Strike — Attack, Common, Cost 1
  3 HIT. DAZED.
  *Upgrade: 4 HIT. DAZED.*

  - [ ] Sim - [ ] Live — **Test: Base Wild Strike deals 3 damage and adds Dazed to discard pile**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Wild Strike in hand. Discard pile is empty.
  Actions: Play Wild Strike targeting enemy.
  Expected: Enemy loses 3 HP (17 HP remaining). 1 Dazed status card is added to player's discard pile. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Wild Strike deals 4 damage**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Wild Strike+ in hand.
  Actions: Play Wild Strike+ targeting enemy.
  Expected: Enemy loses 4 HP (16 HP remaining). 1 Dazed status card is added to player's discard pile.

  - [ ] Sim - [ ] Live — **Test: Wild Strike Dazed card pollutes future draws**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Wild Strike in hand. Draw pile has 1 card. Discard pile is empty.
  Actions: Play Wild Strike targeting enemy. End turn. Start next turn (discard pile shuffled into draw pile).
  Expected: Dazed is now in the draw pile and may be drawn into hand next turn.

- **Headbutt** [Y] — BGHeadbutt — Attack, Common, Cost 1
  2 HIT. Put a card from your discard pile on top of your draw pile.
  *Upgrade: 3 HIT.*

  - [ ] Sim - [ ] Live — **Test: Base Headbutt deals 2 damage and moves card from discard to top of draw pile**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Headbutt in hand. Discard pile contains: Bash, Defend. Draw pile has 3 cards.
  Actions: Play Headbutt targeting enemy. Choose Bash from discard pile.
  Expected: Enemy loses 2 HP (18 HP remaining). Bash is moved from discard pile to top of draw pile (draw pile now has 4 cards with Bash on top).

  - [ ] Sim - [ ] Live — **Test: Upgraded Headbutt deals 3 damage**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Headbutt+ in hand. Discard pile contains: Strike.
  Actions: Play Headbutt+ targeting enemy. Choose Strike from discard pile.
  Expected: Enemy loses 3 HP (17 HP remaining). Strike is placed on top of draw pile.

  - [ ] Sim - [ ] Live — **Test: Headbutt with empty discard pile**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Headbutt in hand. Discard pile is empty.
  Actions: Play Headbutt targeting enemy.
  Expected: Enemy loses 2 HP (18 HP remaining). No card to select from discard (discard pile retrieval step is skipped or has no valid target).

- **Havoc** [Y] — BGHavoc — Skill, Common, Cost 1
  Draw a card. Immediately play it for 0 Energy. Exhaust it, unless it's a Power.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Havoc draws and plays a card for free, then exhausts it**
  Setup: Player has 3 energy. Enemy has 20 HP, 0 block. Havoc in hand. Top of draw pile is Strike.
  Actions: Play Havoc.
  Expected: Player spends 1 energy (2 remaining). Strike is drawn and immediately played targeting an enemy for 0 energy. Enemy loses 1 HP. Strike is exhausted (not sent to discard pile).

  - [ ] Sim - [ ] Live — **Test: Havoc with a Power card does not exhaust it**
  Setup: Player has 3 energy. Havoc in hand. Top of draw pile is a Power card (e.g., Inflame).
  Actions: Play Havoc.
  Expected: Inflame is drawn and played for 0 energy. Inflame is NOT exhausted (goes to discard or stays in play as a Power normally would).

  - [ ] Sim - [ ] Live — **Test: Upgraded Havoc costs 0 energy**
  Setup: Player has 3 energy. Enemy has 20 HP. Havoc+ in hand. Top of draw pile is Strike.
  Actions: Play Havoc+.
  Expected: Player spends 0 energy (3 remaining). Strike is drawn, played for free, and exhausted.

  - [ ] Sim - [ ] Live — **Test: Havoc with empty draw pile**
  Setup: Player has 3 energy. Havoc in hand. Draw pile is empty. Discard pile has 2 cards.
  Actions: Play Havoc.
  Expected: Discard pile is shuffled into draw pile, then the top card is drawn and played for free, then exhausted (unless it is a Power).

- **Seeing Red** [Y] — BGSeeing Red — Skill, Common, Cost 1
  Gain Energy(R) Energy(R).
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Base Seeing Red grants 2 energy**
  Setup: Player has 3 energy. Seeing Red in hand.
  Actions: Play Seeing Red.
  Expected: Player spends 1 energy, then gains 2 energy. Net energy = 3 - 1 + 2 = 4 energy remaining.

  - [ ] Sim - [ ] Live — **Test: Upgraded Seeing Red costs 0, grants 2 energy**
  Setup: Player has 3 energy. Seeing Red+ in hand.
  Actions: Play Seeing Red+.
  Expected: Player spends 0 energy, gains 2 energy. Net energy = 3 + 2 = 5 energy remaining.

  - [ ] Sim - [ ] Live — **Test: Seeing Red allows playing expensive card afterward**
  Setup: Player has 1 energy. Seeing Red in hand. Bash (cost 2) in hand.
  Actions: Play Seeing Red. Play Bash targeting enemy.
  Expected: After Seeing Red: 1 - 1 + 2 = 2 energy. Bash costs 2, so it can be played. 0 energy remaining.

- **True Grit** [Y] — BGTrue Grit — Skill, Common, Cost 1
  1 BLK to any player. Exhaust a card in your hand.
  *Upgrade: 2 BLK to any player. Exhaust a card in your hand.*

  - [ ] Sim - [ ] Live — **Test: Base True Grit grants 1 block and exhausts a card from hand**
  Setup: Player has 3 energy, 0 block. True Grit in hand. Defend in hand. Strike in hand.
  Actions: Play True Grit. Choose Strike to exhaust.
  Expected: Player gains 1 block. Strike is exhausted (moved to exhaust pile). Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Upgraded True Grit grants 2 block**
  Setup: Player has 3 energy, 0 block. True Grit+ in hand. Defend in hand.
  Actions: Play True Grit+. Choose Defend to exhaust.
  Expected: Player gains 2 block. Defend is exhausted.

  - [ ] Sim - [ ] Live — **Test: True Grit when only True Grit is in hand**
  Setup: Player has 3 energy, 0 block. True Grit is the only card in hand.
  Actions: Play True Grit.
  Expected: Player gains 1 block. No other card to exhaust (exhaust step has no valid target).

- **Warcry** [Y] — BGWarcry — Skill, Common, Cost 0
  Draw 2 cards. Then put a card from your hand onto the top of your draw pile. Exhaust.
  *Upgrade: Draw 3 cards.*

  - [ ] Sim - [ ] Live — **Test: Base Warcry draws 2, puts 1 back, and exhausts**
  Setup: Player has 3 energy. Warcry in hand. Draw pile has 5 cards. Hand has 2 other cards.
  Actions: Play Warcry. Choose a card from hand to put on top of draw pile.
  Expected: Player draws 2 cards (hand now has 2 original + 2 drawn = 4 cards). Player puts 1 chosen card on top of draw pile (hand now has 3 cards). Warcry is exhausted. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Warcry draws 3 cards**
  Setup: Player has 3 energy. Warcry+ in hand. Draw pile has 5 cards. Hand has 2 other cards.
  Actions: Play Warcry+. Choose a card from hand to put on top of draw pile.
  Expected: Player draws 3 cards (hand now has 2 original + 3 drawn = 5 cards). Player puts 1 chosen card on top of draw pile (hand now has 4 cards). Warcry+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Warcry with only 1 card in draw pile**
  Setup: Player has 3 energy. Warcry in hand. Draw pile has 1 card. Discard pile has 3 cards. Hand has 1 other card.
  Actions: Play Warcry. Choose a card to put on top of draw pile.
  Expected: Player draws 1 card from draw pile. Draw pile is empty, so discard pile is shuffled into draw pile, then player draws 1 more card. Player puts 1 card from hand on top of draw pile. Warcry is exhausted.
