# Ironclad (BGRed) — Rare

- **Bludgeon** [Y] — BGBludgeon — Attack, Rare, Cost 3
  7 HIT.
  *Upgrade: 10 HIT.*

  - [ ] Sim - [ ] Live — **Test: Basic Bludgeon deals 7 damage**
  Setup: Player has 3 energy, Bludgeon in hand. Enemy has 15 HP, no block.
  Actions: Play Bludgeon targeting enemy.
  Expected: Enemy loses 7 HP (7 HIT = 7 damage). Player spent 3 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Bludgeon deals 10 damage**
  Setup: Player has 3 energy, Bludgeon+ in hand. Enemy has 15 HP, no block.
  Actions: Play Bludgeon+ targeting enemy.
  Expected: Enemy loses 10 HP (10 HIT = 10 damage). Player spent 3 energy.

  - [ ] Sim - [ ] Live — **Test: Bludgeon with Strength scales per HIT**
  Setup: Player has 3 energy, 2 STR, Bludgeon in hand. Enemy has 30 HP, no block.
  Actions: Play Bludgeon targeting enemy.
  Expected: Enemy loses 21 HP (7 HIT, each dealing 1+2 STR = 3 damage, so 7x3 = 21).

- **Impervious** [Y] — BGImpervious — Skill, Rare, Cost 2
  6 BLK. Exhaust.
  *Upgrade: 8 BLK. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic Impervious grants 6 block and exhausts**
  Setup: Player has 3 energy, Impervious in hand, 0 BLK.
  Actions: Play Impervious.
  Expected: Player gains 6 BLK. Impervious is moved to exhaust pile. Player spent 2 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Impervious grants 8 block**
  Setup: Player has 3 energy, Impervious+ in hand, 0 BLK.
  Actions: Play Impervious+.
  Expected: Player gains 8 BLK. Impervious+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Impervious block stacks with existing block**
  Setup: Player has 3 energy, Impervious in hand, 4 BLK already.
  Actions: Play Impervious.
  Expected: Player now has 10 BLK (4 existing + 6 from Impervious). Impervious is exhausted.

- **Offering** [Y] — BGOffering — Skill, Rare, Cost 0
  Lose 1 HP. Gain Energy(R) Energy(R). Draw 3 cards. Exhaust.
  *Upgrade: Draw 5 cards.*

  - [ ] Sim - [ ] Live — **Test: Basic Offering costs HP, gains energy, draws cards, and exhausts**
  Setup: Player has 0 energy, 50 HP, Offering in hand. Draw pile has 5 cards.
  Actions: Play Offering.
  Expected: Player loses 1 HP (now 49 HP). Player gains 2 energy. Player draws 3 cards. Offering is exhausted. Player spent 0 energy to play it.

  - [ ] Sim - [ ] Live — **Test: Upgraded Offering draws 5 cards**
  Setup: Player has 0 energy, 50 HP, Offering+ in hand. Draw pile has 6 cards.
  Actions: Play Offering+.
  Expected: Player loses 1 HP. Player gains 2 energy. Player draws 5 cards. Offering+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Offering at 1 HP still playable (loses HP, not lethal)**
  Setup: Player has 0 energy, 1 HP, Offering in hand. Draw pile has 5 cards.
  Actions: Play Offering.
  Expected: Player loses 1 HP (now 0 HP -- this may cause death or be handled by game rules). Player gains 2 energy. Player draws 3 cards. Offering is exhausted.

- **Barricade** [Y] — BGBarricade — Power, Rare, Cost 2
  Start of turn: Keep your leftover BLK from last turn. (Max block is 20 BLK.)
  *Upgrade: Cost 2 to 1.*

  - [ ] Sim - [ ] Live — **Test: Barricade retains block between turns**
  Setup: Player has 3 energy, Barricade in hand, 0 BLK. Player also has a Defend (2 BLK) in hand.
  Actions: Play Barricade. Play Defend targeting self (gain 2 BLK). End turn. Start next turn.
  Expected: Player retains 2 BLK at start of next turn (block is not reset to 0).

  - [ ] Sim - [ ] Live — **Test: Barricade respects 20 BLK cap**
  Setup: Player has Barricade power active, 18 BLK. Player plays a card granting 5 BLK.
  Actions: Gain 5 BLK.
  Expected: Player has 20 BLK (capped at 20, not 23). Block carries over to next turn.

  - [ ] Sim - [ ] Live — **Test: Upgraded Barricade costs 1 energy**
  Setup: Player has 1 energy, Barricade+ in hand.
  Actions: Play Barricade+.
  Expected: Barricade+ is played for 1 energy. Block retention effect is active.

- **Berserk** [Y] — BGBerserk — Power, Rare, Cost 1
  Whenever you Exhaust a card, deal 1 damage to any row.
  *Upgrade: Deal 2 damage to any row.*

  - [ ] Sim - [ ] Live — **Test: Berserk deals damage when a card is exhausted**
  Setup: Player has Berserk power active. Player has Burning Pact and a Strike in hand. Enemy row has an enemy with 10 HP.
  Actions: Play Burning Pact, choose Strike to exhaust.
  Expected: Strike is exhausted. Berserk triggers, dealing 1 damage to a chosen enemy row.

  - [ ] Sim - [ ] Live — **Test: Berserk triggers for each card exhausted**
  Setup: Player has Berserk power active. Player has Second Wind and 2 Defends in hand. Enemy row has an enemy with 10 HP.
  Actions: Play Second Wind (exhausts both Defends).
  Expected: Berserk triggers twice, dealing 1 damage to a chosen row each time (2 total damage).

  - [ ] Sim - [ ] Live — **Test: Upgraded Berserk deals 2 damage per exhaust**
  Setup: Player has Berserk+ power active. Player has a card with Exhaust. Enemy row has an enemy with 10 HP.
  Actions: Exhaust a card.
  Expected: Berserk+ triggers, dealing 2 damage to a chosen enemy row.

- **Corruption** [Y] — BGCorruption — Power, Rare, Cost 3
  Skills cost 0. Playing a Skill Exhausts it.
  *Upgrade: Cost 3 to 2.*

  - [ ] Sim - [ ] Live — **Test: Corruption makes Skills cost 0 and exhaust them**
  Setup: Player has Corruption power active, 0 energy. Player has Defend (normally cost 1) in hand.
  Actions: Play Defend targeting self.
  Expected: Defend costs 0 energy. Player gains block from Defend. Defend is exhausted (not sent to discard pile).

  - [ ] Sim - [ ] Live — **Test: Corruption does not affect Attacks**
  Setup: Player has Corruption power active, 0 energy. Player has Strike (cost 1) in hand.
  Actions: Attempt to play Strike.
  Expected: Strike still costs 1 energy. Cannot be played with 0 energy. Strike is not affected by Corruption.

  - [ ] Sim - [ ] Live — **Test: Upgraded Corruption costs 2 energy**
  Setup: Player has 2 energy, Corruption+ in hand.
  Actions: Play Corruption+.
  Expected: Corruption+ is played for 2 energy. All subsequent Skills cost 0 and exhaust when played.

  - [ ] Sim - [ ] Live — **Test: Corruption exhausts Skills even if they normally would not exhaust**
  Setup: Player has Corruption power active, 0 energy. Player has Shrug It Off (Skill, normally cost 1, no exhaust) in hand.
  Actions: Play Shrug It Off.
  Expected: Shrug It Off costs 0. Its normal effect triggers. It is exhausted instead of discarded.

- **Demon Form** [Y] — BGDemon Form — Power, Rare, Cost 3
  Start of turn: Gain STR.
  *Upgrade: Cost 3 to 2.*

  - [ ] Sim - [ ] Live — **Test: Demon Form grants STR at start of each turn**
  Setup: Player has 3 energy, 0 STR, Demon Form in hand.
  Actions: Play Demon Form. End turn. Start next turn.
  Expected: At start of next turn, player gains 1 STR (now has 1 STR).

  - [ ] Sim - [ ] Live — **Test: Demon Form STR accumulates over multiple turns**
  Setup: Player has Demon Form power active, 0 STR.
  Actions: End turn 1, start turn 2 (gain 1 STR). End turn 2, start turn 3 (gain 1 STR).
  Expected: Player has 2 STR at the start of turn 3.

  - [ ] Sim - [ ] Live — **Test: Upgraded Demon Form costs 2 energy**
  Setup: Player has 2 energy, Demon Form+ in hand.
  Actions: Play Demon Form+.
  Expected: Demon Form+ is played for 2 energy. Start of turn STR gain is active.

- **Double Tap** [Y] — BGDouble Tap — Skill, Rare, Cost 1
  This turn, your next Attack is played twice.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Double Tap causes next Attack to play twice**
  Setup: Player has 3 energy, Double Tap and a Strike (1 cost, 1 HIT) in hand. Enemy has 10 HP.
  Actions: Play Double Tap. Play Strike targeting enemy.
  Expected: Strike is played twice. Enemy loses 2 HP (1 HIT x 2 plays = 2 damage). Player spent 1 energy for Double Tap + 1 energy for Strike = 2 energy total.

  - [ ] Sim - [ ] Live — **Test: Double Tap only affects the next Attack, not subsequent ones**
  Setup: Player has 3 energy, Double Tap and 2 Strikes in hand. Enemy has 10 HP.
  Actions: Play Double Tap. Play first Strike targeting enemy. Play second Strike targeting enemy.
  Expected: First Strike plays twice (enemy loses 2 HP). Second Strike plays once (enemy loses 1 HP). Total: enemy loses 3 HP.

  - [ ] Sim - [ ] Live — **Test: Upgraded Double Tap costs 0 energy**
  Setup: Player has 2 energy, Double Tap+ and a Strike in hand. Enemy has 10 HP.
  Actions: Play Double Tap+. Play Strike targeting enemy.
  Expected: Double Tap+ costs 0 energy. Strike plays twice. Enemy loses 2 HP. Player spent 1 energy total (just the Strike).

- **Exhume** [Y] — BGExhume — Skill, Rare, Cost 1
  Put a card from your Exhaust pile into your hand. Exhaust.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Exhume retrieves a card from exhaust pile**
  Setup: Player has 3 energy, Exhume in hand. Exhaust pile contains an Impervious.
  Actions: Play Exhume, choose Impervious from exhaust pile.
  Expected: Impervious is moved from exhaust pile to player's hand. Exhume itself is exhausted.

  - [ ] Sim - [ ] Live — **Test: Exhume with empty exhaust pile**
  Setup: Player has 3 energy, Exhume in hand. Exhaust pile is empty.
  Actions: Play Exhume.
  Expected: No card is retrieved (exhaust pile is empty). Exhume is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Exhume costs 0 energy**
  Setup: Player has 0 energy, Exhume+ in hand. Exhaust pile contains a Strike.
  Actions: Play Exhume+, choose Strike.
  Expected: Strike is moved to hand. Exhume+ is exhausted. Player spent 0 energy.

- **Feed** [Y] — BGFeed — Attack, Rare, Cost 1
  3 HIT. If this kills the enemy, gain STR. Exhaust.
  *Upgrade: If this kills the enemy, gain STR STR. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Feed deals damage and gains STR on kill**
  Setup: Player has 3 energy, 0 STR, Feed in hand. Enemy has 3 HP, no block.
  Actions: Play Feed targeting enemy.
  Expected: Enemy takes 3 damage (3 HIT) and dies. Player gains 1 STR. Feed is exhausted.

  - [ ] Sim - [ ] Live — **Test: Feed does not grant STR if enemy survives**
  Setup: Player has 3 energy, 0 STR, Feed in hand. Enemy has 10 HP, no block.
  Actions: Play Feed targeting enemy.
  Expected: Enemy takes 3 damage (now 7 HP, still alive). Player does not gain STR. Feed is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Feed grants 2 STR on kill**
  Setup: Player has 3 energy, 0 STR, Feed+ in hand. Enemy has 3 HP, no block.
  Actions: Play Feed+ targeting enemy.
  Expected: Enemy takes 3 damage and dies. Player gains 2 STR. Feed+ is exhausted.

- **Fiend Fire** [Y] — BGFiend Fire — Attack, Rare, Cost 2
  Exhaust your hand. Deal 1 HIT for each other card Exhausted this way. Exhaust.
  *Upgrade: Deal 2 HIT for each card Exhausted.*

  - [ ] Sim - [ ] Live — **Test: Fiend Fire exhausts hand and deals damage per card**
  Setup: Player has 3 energy, Fiend Fire and 3 other cards (Strike, Defend, Bash) in hand. Enemy has 10 HP.
  Actions: Play Fiend Fire targeting enemy.
  Expected: Strike, Defend, and Bash are exhausted. Enemy takes 3 damage (1 HIT per card exhausted = 3 HIT). Fiend Fire itself is also exhausted.

  - [ ] Sim - [ ] Live — **Test: Fiend Fire with empty hand deals 0 damage**
  Setup: Player has 2 energy, Fiend Fire is the only card in hand. Enemy has 10 HP.
  Actions: Play Fiend Fire targeting enemy.
  Expected: No other cards to exhaust. Enemy takes 0 damage. Fiend Fire is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Fiend Fire deals 2 HIT per card exhausted**
  Setup: Player has 3 energy, Fiend Fire+ and 2 other cards in hand. Enemy has 15 HP.
  Actions: Play Fiend Fire+ targeting enemy.
  Expected: 2 cards are exhausted. Enemy takes 4 damage (2 HIT per card x 2 cards = 4 HIT = 4 damage). Fiend Fire+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Fiend Fire with Strength scales per HIT**
  Setup: Player has 3 energy, 2 STR, Fiend Fire and 3 other cards in hand. Enemy has 20 HP.
  Actions: Play Fiend Fire targeting enemy.
  Expected: 3 cards exhausted. 3 HIT, each dealing 1+2 STR = 3 damage. Enemy loses 9 HP. Fiend Fire is exhausted.

- **Immolate** [Y] — BGImmolate — Attack, Rare, Cost 2
  AOE 5 HIT. DAZED DAZED.
  *Upgrade: AOE 7 HIT. DAZED DAZED.*

  - [ ] Sim - [ ] Live — **Test: Immolate deals AOE damage and adds DAZED cards**
  Setup: Player has 3 energy, Immolate in hand. Two enemies, each with 10 HP. Discard pile has 2 cards.
  Actions: Play Immolate.
  Expected: Both enemies lose 5 HP (5 HIT = 5 damage each, AOE). 2 DAZED status cards are added to the discard pile.

  - [ ] Sim - [ ] Live — **Test: Upgraded Immolate deals 7 AOE damage**
  Setup: Player has 3 energy, Immolate+ in hand. Two enemies, each with 10 HP.
  Actions: Play Immolate+.
  Expected: Both enemies lose 7 HP (7 HIT = 7 damage each, AOE). 2 DAZED added to discard pile.

  - [ ] Sim - [ ] Live — **Test: Immolate with Strength scales per HIT**
  Setup: Player has 3 energy, 1 STR, Immolate in hand. Enemy has 15 HP.
  Actions: Play Immolate.
  Expected: Enemy loses 10 HP (5 HIT, each dealing 1+1 STR = 2 damage, so 5x2 = 10). 2 DAZED added to discard pile.

- **Juggernaut** [Y] — BGJuggernaut — Power, Rare, Cost 2
  Whenever you gain BLK, deal 1 damage.
  *Upgrade: Deal 2 damage.*

  - [ ] Sim - [ ] Live — **Test: Juggernaut deals damage when gaining block**
  Setup: Player has Juggernaut power active, 0 BLK. Player has Defend (2 BLK) in hand. Enemy has 10 HP.
  Actions: Play Defend targeting self.
  Expected: Player gains 2 BLK. Juggernaut triggers, dealing 1 damage to an enemy.

  - [ ] Sim - [ ] Live — **Test: Juggernaut triggers on each source of block gain**
  Setup: Player has Juggernaut power active, 0 BLK. Player has 2 Defends in hand. Enemy has 10 HP.
  Actions: Play first Defend. Play second Defend.
  Expected: Juggernaut triggers twice (once per Defend played), dealing 1 damage each time (2 total damage).

  - [ ] Sim - [ ] Live — **Test: Upgraded Juggernaut deals 2 damage per block gain**
  Setup: Player has Juggernaut+ power active, 0 BLK. Player has Defend in hand. Enemy has 10 HP.
  Actions: Play Defend targeting self.
  Expected: Player gains 2 BLK. Juggernaut+ triggers, dealing 2 damage to an enemy.

- **Limit Break** [Y] — BGLimit Break — Skill, Rare, Cost 1
  Double your STR. (Max STR is 8.) Exhaust.
  *Upgrade: Double your STR. (Max STR is 8.) (No longer Exhausts.)*

  - [ ] Sim - [ ] Live — **Test: Limit Break doubles STR and exhausts**
  Setup: Player has 3 energy, 2 STR, Limit Break in hand.
  Actions: Play Limit Break.
  Expected: Player now has 4 STR (doubled from 2). Limit Break is exhausted.

  - [ ] Sim - [ ] Live — **Test: Limit Break respects 8 STR cap**
  Setup: Player has 3 energy, 5 STR, Limit Break in hand.
  Actions: Play Limit Break.
  Expected: Player now has 8 STR (doubled would be 10, capped at 8). Limit Break is exhausted.

  - [ ] Sim - [ ] Live — **Test: Limit Break with 0 STR does nothing**
  Setup: Player has 3 energy, 0 STR, Limit Break in hand.
  Actions: Play Limit Break.
  Expected: Player still has 0 STR (0 doubled = 0). Limit Break is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Limit Break does not exhaust**
  Setup: Player has 3 energy, 3 STR, Limit Break+ in hand.
  Actions: Play Limit Break+.
  Expected: Player now has 6 STR. Limit Break+ goes to discard pile (not exhausted).
