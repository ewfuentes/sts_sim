# Defect (BGBlue) — Uncommon

- **Blizzard** [Y] — BGBlizzard — Attack, Uncommon, Cost 1
  Deal AOE 2 HIT for each Frost orb you have.
  *Upgrade: Deal AOE 3 HIT for each Frost orb you have.*

  - [ ] Sim - [ ] Live — **Test: Basic Blizzard with 2 Frost orbs**
  Setup: Player has 3 energy, Blizzard in hand, 2 Frost orbs channeled. Two enemies present with 20 HP each.
  Actions: Play Blizzard.
  Expected: Each enemy takes 4 damage (2 HIT x 2 Frost orbs = 4 damage instances). Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Blizzard with no Frost orbs deals no damage**
  Setup: Player has 3 energy, Blizzard in hand, 1 Lightning orb channeled, 0 Frost orbs. One enemy with 20 HP.
  Actions: Play Blizzard.
  Expected: Enemy takes 0 damage (2 HIT x 0 Frost orbs = 0 damage instances). Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Blizzard with 3 Frost orbs**
  Setup: Player has 3 energy, Blizzard+ in hand, 3 Frost orbs channeled. Two enemies present with 30 HP each.
  Actions: Play Blizzard+.
  Expected: Each enemy takes 9 damage (3 HIT x 3 Frost orbs = 9 damage instances). Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Blizzard with Strength**
  Setup: Player has 3 energy, 2 Strength, Blizzard in hand, 2 Frost orbs channeled. One enemy with 30 HP.
  Actions: Play Blizzard.
  Expected: Enemy takes 8 damage (2 Frost orbs x 2 HIT = 4 hits, each hit deals 1+2 Strength = 3 damage, but HIT = 1 per token + Strength adds +1 per HIT, so 4 HIT each dealing 1+2=3 => 12 damage). Correction: 2 HIT per Frost orb x 2 orbs = 4 HIT tokens. Each HIT deals 1 + 2 Strength = 3. Total = 12 damage.

- **Cold Snap** [Y] — BGColdSnap — Attack, Uncommon, Cost 2
  2 HIT. Channel 1 Frost.
  *Upgrade: 3 HIT. Channel 1 Frost.*

  - [ ] Sim - [ ] Live — **Test: Basic Cold Snap**
  Setup: Player has 3 energy, Cold Snap in hand, 0 orbs, 3 orb slots. One enemy with 20 HP.
  Actions: Play Cold Snap targeting enemy.
  Expected: Enemy takes 2 damage (2 HIT). Player channels 1 Frost orb (now has 1 Frost orb in slot 1). Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Cold Snap upgraded**
  Setup: Player has 3 energy, Cold Snap+ in hand, 0 orbs, 3 orb slots. One enemy with 20 HP.
  Actions: Play Cold Snap+ targeting enemy.
  Expected: Enemy takes 3 damage (3 HIT). Player channels 1 Frost orb. Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Cold Snap when orb slots are full**
  Setup: Player has 3 energy, Cold Snap in hand, 3 orb slots all occupied (Lightning, Lightning, Frost). One enemy with 20 HP.
  Actions: Play Cold Snap targeting enemy.
  Expected: Enemy takes 2 damage from Cold Snap. The oldest orb (first Lightning) is evoked (dealing its evoke damage to a random enemy), then the new Frost orb is channeled in the freed slot.

- **Doom and Gloom** [Y] — BGDoomAndGloom — Attack, Uncommon, Cost 2
  AOE 2 HIT. Channel 1 Dark.
  *Upgrade: AOE 3 HIT. Channel 1 Dark.*

  - [ ] Sim - [ ] Live — **Test: Basic Doom and Gloom**
  Setup: Player has 3 energy, Doom and Gloom in hand, 0 orbs, 3 orb slots. Two enemies with 20 HP each.
  Actions: Play Doom and Gloom.
  Expected: Each enemy takes 2 damage (AOE 2 HIT). Player channels 1 Dark orb. Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Doom and Gloom**
  Setup: Player has 3 energy, Doom and Gloom+ in hand, 0 orbs, 3 orb slots. Two enemies with 15 HP each.
  Actions: Play Doom and Gloom+.
  Expected: Each enemy takes 3 damage (AOE 3 HIT). Player channels 1 Dark orb. Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Doom and Gloom with full orb slots**
  Setup: Player has 3 energy, Doom and Gloom in hand, 3 orb slots filled with Frost, Frost, Lightning. Two enemies with 20 HP each.
  Actions: Play Doom and Gloom.
  Expected: Each enemy takes 2 damage from AOE. The oldest Frost orb is evoked (granting block), then 1 Dark orb is channeled in the freed slot.

- **FTL** [Y] — BGFTL — Attack, Uncommon, Cost 0
  1 HIT. If this is the first card you played this turn, draw 1 card.
  *Upgrade: 2 HIT.*

  - [ ] Sim - [ ] Live — **Test: FTL as first card of turn**
  Setup: Player has 3 energy, FTL in hand plus 3 other cards, 5 cards in draw pile. One enemy with 20 HP. No cards played this turn.
  Actions: Play FTL targeting enemy.
  Expected: Enemy takes 1 damage (1 HIT). Player draws 1 card. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: FTL not first card of turn**
  Setup: Player has 3 energy, FTL in hand, already played a Strike this turn. One enemy with 20 HP. 5 cards in draw pile.
  Actions: Play FTL targeting enemy.
  Expected: Enemy takes 1 damage (1 HIT). Player does NOT draw a card (not first card played this turn). Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded FTL as first card**
  Setup: Player has 3 energy, FTL+ in hand, no cards played this turn. One enemy with 20 HP. 5 cards in draw pile.
  Actions: Play FTL+ targeting enemy.
  Expected: Enemy takes 2 damage (2 HIT). Player draws 1 card. Player spends 0 energy.

- **Melter** [Y] — BGMelter — Attack, Uncommon, Cost 1
  First remove all BLK from the target. 2 HIT.
  *Upgrade: 3 HIT.*

  - [ ] Sim - [ ] Live — **Test: Melter on enemy with block**
  Setup: Player has 3 energy, Melter in hand. One enemy with 20 HP and 10 block.
  Actions: Play Melter targeting enemy.
  Expected: Enemy's 10 block is removed first, then enemy takes 2 damage to HP (2 HIT, each dealing 1 damage). Enemy is now at 18 HP, 0 block.

  - [ ] Sim - [ ] Live — **Test: Melter on enemy with no block**
  Setup: Player has 3 energy, Melter in hand. One enemy with 20 HP, 0 block.
  Actions: Play Melter targeting enemy.
  Expected: No block to remove. Enemy takes 2 damage (2 HIT). Enemy is now at 18 HP.

  - [ ] Sim - [ ] Live — **Test: Upgraded Melter on enemy with block**
  Setup: Player has 3 energy, Melter+ in hand. One enemy with 20 HP and 15 block.
  Actions: Play Melter+ targeting enemy.
  Expected: Enemy's 15 block is removed first, then enemy takes 3 damage to HP (3 HIT). Enemy is now at 17 HP, 0 block.

- **Scrape** [Y] — BGScrape — Attack, Uncommon, Cost 1
  2 HIT. If the topmost card in your discard pile costs 0, return it to your hand.
  *Upgrade: 3 HIT.*

  - [ ] Sim - [ ] Live — **Test: Scrape with a 0-cost card on top of discard**
  Setup: Player has 3 energy, Scrape in hand, 4 cards in hand total. Discard pile top card is Zap (cost 0). One enemy with 20 HP.
  Actions: Play Scrape targeting enemy.
  Expected: Enemy takes 2 damage (2 HIT). Zap is returned from discard pile to hand.

  - [ ] Sim - [ ] Live — **Test: Scrape with non-zero cost card on top of discard**
  Setup: Player has 3 energy, Scrape in hand. Discard pile top card is Strike (cost 1). One enemy with 20 HP.
  Actions: Play Scrape targeting enemy.
  Expected: Enemy takes 2 damage (2 HIT). No card is returned to hand (top of discard costs 1, not 0).

  - [ ] Sim - [ ] Live — **Test: Scrape with empty discard pile**
  Setup: Player has 3 energy, Scrape in hand. Discard pile is empty. One enemy with 20 HP.
  Actions: Play Scrape targeting enemy.
  Expected: Enemy takes 2 damage (2 HIT). No card is returned (discard pile is empty).

  - [ ] Sim - [ ] Live — **Test: Upgraded Scrape**
  Setup: Player has 3 energy, Scrape+ in hand. Discard pile top card is TURBO (cost 0). One enemy with 20 HP.
  Actions: Play Scrape+ targeting enemy.
  Expected: Enemy takes 3 damage (3 HIT). TURBO is returned from discard pile to hand.

- **Streamline** [Y] — BGStreamline — Attack, Uncommon, Cost 2
  3 HIT. Costs 1 less Energy(B) for each Power you have in play.
  *Upgrade: 4 HIT.*

  - [ ] Sim - [ ] Live — **Test: Streamline at base cost with no powers**
  Setup: Player has 3 energy, Streamline in hand. No powers in play. One enemy with 20 HP.
  Actions: Play Streamline targeting enemy.
  Expected: Player spends 2 energy. Enemy takes 3 damage (3 HIT).

  - [ ] Sim - [ ] Live — **Test: Streamline cost reduction with 2 powers**
  Setup: Player has 3 energy, Streamline in hand. 2 powers in play (e.g., Loop and Storm). One enemy with 20 HP.
  Actions: Play Streamline targeting enemy.
  Expected: Streamline costs 0 energy (2 - 2 = 0). Enemy takes 3 damage (3 HIT).

  - [ ] Sim - [ ] Live — **Test: Upgraded Streamline with 1 power**
  Setup: Player has 3 energy, Streamline+ in hand. 1 power in play (e.g., Defragment). One enemy with 20 HP.
  Actions: Play Streamline+ targeting enemy.
  Expected: Player spends 1 energy (2 - 1 = 1). Enemy takes 4 damage (4 HIT).

- **Sunder** [Y] — BGSunder — Attack, Uncommon, Cost 3
  5 HIT. If this kills the enemy, gain Energy(B) Energy(B) Energy(B).
  *Upgrade: 7 HIT.*

  - [ ] Sim - [ ] Live — **Test: Sunder kills enemy and refunds energy**
  Setup: Player has 3 energy, Sunder in hand. One enemy with 4 HP, 0 block.
  Actions: Play Sunder targeting enemy.
  Expected: Enemy takes 5 damage (5 HIT), which kills it (4 HP). Player gains 3 energy (refund). Player energy is now 3 (spent 3, gained 3).

  - [ ] Sim - [ ] Live — **Test: Sunder does not kill enemy**
  Setup: Player has 3 energy, Sunder in hand. One enemy with 20 HP, 0 block.
  Actions: Play Sunder targeting enemy.
  Expected: Enemy takes 5 damage (5 HIT). Enemy survives at 15 HP. Player does NOT gain energy. Player has 0 energy remaining.

  - [ ] Sim - [ ] Live — **Test: Upgraded Sunder kills enemy**
  Setup: Player has 3 energy, Sunder+ in hand. One enemy with 6 HP, 0 block.
  Actions: Play Sunder+ targeting enemy.
  Expected: Enemy takes 7 damage (7 HIT), killing it. Player gains 3 energy. Player energy is now 3.

- **Darkness** [Y] — BGDarkness — Skill, Uncommon, Cost 1
  Channel 1 Dark.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Basic Darkness**
  Setup: Player has 3 energy, Darkness in hand, 0 orbs, 3 orb slots.
  Actions: Play Darkness.
  Expected: Player channels 1 Dark orb. Player spends 1 energy (2 remaining).

  - [ ] Sim - [ ] Live — **Test: Upgraded Darkness costs 0**
  Setup: Player has 3 energy, Darkness+ in hand, 0 orbs, 3 orb slots.
  Actions: Play Darkness+.
  Expected: Player channels 1 Dark orb. Player spends 0 energy (3 remaining).

  - [ ] Sim - [ ] Live — **Test: Darkness when orb slots are full**
  Setup: Player has 3 energy, Darkness in hand, 3 orb slots all filled (Lightning, Frost, Frost).
  Actions: Play Darkness.
  Expected: The oldest orb (Lightning) is evoked (deals its evoke damage to a random enemy), then 1 Dark orb is channeled in the freed slot.

- **Double Energy** [Y] — BGDoubleEnergy — Skill, Uncommon, Cost 1
  Double your Energy(B). (Max Energy(B) is 6.) Exhaust.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Basic Double Energy**
  Setup: Player has 3 energy, Double Energy in hand.
  Actions: Play Double Energy.
  Expected: Player spends 1 energy (now 2), then energy is doubled to 4. Card is exhausted.

  - [ ] Sim - [ ] Live — **Test: Double Energy capped at 6**
  Setup: Player has 5 energy, Double Energy in hand.
  Actions: Play Double Energy.
  Expected: Player spends 1 energy (now 4), then energy doubles to 6 (capped at 6, not 8). Card is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Double Energy at 0 cost**
  Setup: Player has 3 energy, Double Energy+ in hand.
  Actions: Play Double Energy+.
  Expected: Player spends 0 energy (still 3), then energy is doubled to 6. Card is exhausted.

- **Equilibrium** [Y] — BGEquilibrium — Skill, Uncommon, Cost 2
  3 BLK. You may Retain 1 card this turn.
  *Upgrade: 4 BLK. Retain up to 2 cards this turn.*

  - [ ] Sim - [ ] Live — **Test: Basic Equilibrium grants block and retain**
  Setup: Player has 3 energy, Equilibrium in hand, 0 block. Player has 3 other cards in hand.
  Actions: Play Equilibrium. Choose to retain 1 card. End turn.
  Expected: Player gains 3 block. Player spends 2 energy. The 1 retained card remains in hand next turn.

  - [ ] Sim - [ ] Live — **Test: Upgraded Equilibrium retains 2 cards**
  Setup: Player has 3 energy, Equilibrium+ in hand, 0 block. Player has 3 other cards in hand.
  Actions: Play Equilibrium+. Choose to retain 2 cards. End turn.
  Expected: Player gains 4 block. Player spends 2 energy. The 2 retained cards remain in hand next turn.

  - [ ] Sim - [ ] Live — **Test: Equilibrium block stacks**
  Setup: Player has 3 energy, Equilibrium in hand, 5 block already.
  Actions: Play Equilibrium.
  Expected: Player gains 3 block (total 8 block). Player spends 2 energy.

- **Force Field** [Y] — BGForceField — Skill, Uncommon, Cost 4
  3 BLK. Costs 1 less Energy(B) for each Power you have in play.
  *Upgrade: 4 BLK.*

  - [ ] Sim - [ ] Live — **Test: Force Field with no powers (unplayable at 3 energy)**
  Setup: Player has 3 energy, Force Field in hand. No powers in play.
  Actions: Attempt to play Force Field.
  Expected: Cannot play — costs 4 energy but player only has 3.

  - [ ] Sim - [ ] Live — **Test: Force Field with 2 powers in play**
  Setup: Player has 3 energy, Force Field in hand. 2 powers in play (e.g., Loop and Defragment).
  Actions: Play Force Field.
  Expected: Force Field costs 2 energy (4 - 2 = 2). Player gains 3 block. Player has 1 energy remaining.

  - [ ] Sim - [ ] Live — **Test: Upgraded Force Field with 3 powers**
  Setup: Player has 3 energy, Force Field+ in hand. 3 powers in play.
  Actions: Play Force Field+.
  Expected: Force Field+ costs 1 energy (4 - 3 = 1). Player gains 4 block. Player has 2 energy remaining.

  - [ ] Sim - [ ] Live — **Test: Force Field with 4+ powers costs 0**
  Setup: Player has 3 energy, Force Field in hand. 4 powers in play.
  Actions: Play Force Field.
  Expected: Force Field costs 0 energy (4 - 4 = 0, minimum 0). Player gains 3 block. Player has 3 energy remaining.

- **Glacier** [Y] — BGGlacier — Skill, Uncommon, Cost 2
  2 BLK. Channel 1 Frost.
  *Upgrade: 3 BLK to any player. Channel 1 Frost.*

  - [ ] Sim - [ ] Live — **Test: Basic Glacier**
  Setup: Player has 3 energy, Glacier in hand, 0 block, 0 orbs, 3 orb slots.
  Actions: Play Glacier.
  Expected: Player gains 2 block. Player channels 1 Frost orb. Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Glacier targeting ally**
  Setup: Player has 3 energy, Glacier+ in hand, 0 block, 0 orbs, 3 orb slots. An allied player with 0 block present.
  Actions: Play Glacier+ targeting the ally.
  Expected: The ally gains 3 block. Player channels 1 Frost orb. Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Glacier when orb slots are full**
  Setup: Player has 3 energy, Glacier in hand, 3 orb slots filled with Dark, Dark, Lightning.
  Actions: Play Glacier.
  Expected: Player gains 2 block. The oldest orb (first Dark) is evoked (deals its accumulated damage to an enemy with the lowest HP). Then 1 Frost orb is channeled in the freed slot.

- **Hologram** [Y] — BGHologram — Skill, Uncommon, Cost 1
  1 BLK. Put a card from your discard pile into your hand. Exhaust.
  *Upgrade: 1 BLK. Put a card from your discard pile into your hand. (No longer Exhausts.)*

  - [ ] Sim - [ ] Live — **Test: Basic Hologram retrieves card and exhausts**
  Setup: Player has 3 energy, Hologram in hand, 0 block. Discard pile contains Ball Lightning and Zap.
  Actions: Play Hologram, choose Ball Lightning from discard pile.
  Expected: Player gains 1 block. Ball Lightning moves from discard pile to hand. Hologram is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Hologram does not exhaust**
  Setup: Player has 3 energy, Hologram+ in hand, 0 block. Discard pile contains Ball Lightning.
  Actions: Play Hologram+, choose Ball Lightning from discard pile.
  Expected: Player gains 1 block. Ball Lightning moves from discard pile to hand. Hologram+ goes to discard pile (not exhausted).

  - [ ] Sim - [ ] Live — **Test: Hologram with empty discard pile**
  Setup: Player has 3 energy, Hologram in hand, 0 block. Discard pile is empty.
  Actions: Play Hologram.
  Expected: Player gains 1 block. No card is retrieved (discard pile is empty). Hologram is exhausted.

- **Overclock** [Y] — BGOverclock — Skill, Uncommon, Cost 1
  Draw 2 cards. Put a DAZED in your discard pile.
  *Upgrade: Draw 3 cards. Put a DAZED in your discard pile.*

  - [ ] Sim - [ ] Live — **Test: Basic Overclock**
  Setup: Player has 3 energy, Overclock in hand, 5 cards in draw pile. Discard pile is empty.
  Actions: Play Overclock.
  Expected: Player draws 2 cards from draw pile. 1 DAZED status card is added to discard pile. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Overclock draws 3**
  Setup: Player has 3 energy, Overclock+ in hand, 5 cards in draw pile. Discard pile is empty.
  Actions: Play Overclock+.
  Expected: Player draws 3 cards from draw pile. 1 DAZED status card is added to discard pile. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Overclock with fewer cards in draw pile than draw amount**
  Setup: Player has 3 energy, Overclock in hand, 1 card in draw pile, 3 cards in discard pile.
  Actions: Play Overclock.
  Expected: Player draws 1 card from draw pile. Discard pile is shuffled into draw pile (including the DAZED just added). Player draws 1 more card. Player spends 1 energy.

- **Recycle** [Y] — BGRecycle — Skill, Uncommon, Cost 1
  Exhaust a card. Gain Energy(B) equal to its cost. If it costs 'X', instead double your Energy.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Recycle a 2-cost card**
  Setup: Player has 3 energy, Recycle and Glacier (cost 2) in hand.
  Actions: Play Recycle, choose Glacier to exhaust.
  Expected: Glacier is exhausted. Player gains 2 energy. Player spent 1 on Recycle, gained 2, so net energy is 4.

  - [ ] Sim - [ ] Live — **Test: Recycle a 0-cost card**
  Setup: Player has 3 energy, Recycle and Zap (cost 0) in hand.
  Actions: Play Recycle, choose Zap to exhaust.
  Expected: Zap is exhausted. Player gains 0 energy. Player has 2 energy remaining (3 - 1 = 2).

  - [ ] Sim - [ ] Live — **Test: Recycle an X-cost card doubles energy**
  Setup: Player has 3 energy, Recycle and Multi-Cast (cost X) in hand.
  Actions: Play Recycle, choose Multi-Cast to exhaust.
  Expected: Multi-Cast is exhausted. Player's energy is doubled. Player spent 1 on Recycle (now 2), then doubles to 4.

  - [ ] Sim - [ ] Live — **Test: Upgraded Recycle costs 0**
  Setup: Player has 3 energy, Recycle+ and Doom and Gloom (cost 2) in hand.
  Actions: Play Recycle+, choose Doom and Gloom to exhaust.
  Expected: Doom and Gloom is exhausted. Player gains 2 energy. Player spent 0 on Recycle+, gained 2, so net energy is 5.

- **Reprogram** [Y] — BGReprogram — Skill, Uncommon, Cost 1
  Gain STR. Remove all of your Orbs.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Basic Reprogram with orbs**
  Setup: Player has 3 energy, Reprogram in hand, 0 Strength, 2 orbs channeled (Lightning, Frost).
  Actions: Play Reprogram.
  Expected: Player gains 1 Strength. All orbs are removed (not evoked). Player has 0 orbs. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Reprogram with no orbs**
  Setup: Player has 3 energy, Reprogram in hand, 0 Strength, 0 orbs.
  Actions: Play Reprogram.
  Expected: Player gains 1 Strength. No orbs to remove. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Reprogram costs 0**
  Setup: Player has 3 energy, Reprogram+ in hand, 0 Strength, 3 orbs channeled (Frost, Frost, Dark).
  Actions: Play Reprogram+.
  Expected: Player gains 1 Strength. All 3 orbs are removed. Player spends 0 energy (3 remaining).

- **Stack** [Y] — BGStack — Skill, Uncommon, Cost 1
  X BLK to any player. X is how many Orbs you have.
  *Upgrade: X+1 BLK to any player.*

  - [ ] Sim - [ ] Live — **Test: Stack with 3 orbs**
  Setup: Player has 3 energy, Stack in hand, 0 block, 3 orbs channeled (Lightning, Frost, Dark).
  Actions: Play Stack targeting self.
  Expected: Player gains 3 block (X = 3 orbs). Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Stack with 0 orbs**
  Setup: Player has 3 energy, Stack in hand, 0 block, 0 orbs.
  Actions: Play Stack targeting self.
  Expected: Player gains 0 block (X = 0 orbs). Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Stack with 2 orbs**
  Setup: Player has 3 energy, Stack+ in hand, 0 block, 2 orbs channeled (Frost, Frost).
  Actions: Play Stack+ targeting self.
  Expected: Player gains 3 block (X+1 = 2+1 = 3). Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Stack targeting an ally**
  Setup: Player has 3 energy, Stack in hand, 3 orbs channeled. An allied player with 0 block present.
  Actions: Play Stack targeting the ally.
  Expected: The ally gains 3 block (X = 3 orbs).

- **TURBO** [Y] — BGTURBO — Skill, Uncommon, Cost 0
  Gain Energy(B) Energy(B). Put a DAZED in your discard pile. Exhaust.
  *Upgrade: Gain Energy(B) Energy(B) Energy(B). Put a DAZED in your discard pile. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic TURBO**
  Setup: Player has 3 energy, TURBO in hand. Discard pile is empty.
  Actions: Play TURBO.
  Expected: Player gains 2 energy (now 5). 1 DAZED status card is added to discard pile. TURBO is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded TURBO**
  Setup: Player has 3 energy, TURBO+ in hand. Discard pile is empty.
  Actions: Play TURBO+.
  Expected: Player gains 3 energy (now 6). 1 DAZED status card is added to discard pile. TURBO+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: TURBO does not exceed energy cap**
  Setup: Player has 5 energy, TURBO in hand. Discard pile is empty.
  Actions: Play TURBO.
  Expected: Player gains 2 energy (now 7, or capped at 6 if energy cap applies). 1 DAZED is added to discard pile. TURBO is exhausted.

- **Reinforced Body** [Y] — BGReinforcedBody — Skill, Uncommon, Cost -1
  X+1 BLK. X can't be 0.
  *Upgrade: X BLK X BLK.*

  - [ ] Sim - [ ] Live — **Test: Reinforced Body spending 1 energy**
  Setup: Player has 3 energy, Reinforced Body in hand, 0 block.
  Actions: Play Reinforced Body with X=1.
  Expected: Player spends 1 energy. Player gains 2 block (X+1 = 1+1 = 2).

  - [ ] Sim - [ ] Live — **Test: Reinforced Body spending 3 energy**
  Setup: Player has 3 energy, Reinforced Body in hand, 0 block.
  Actions: Play Reinforced Body with X=3.
  Expected: Player spends 3 energy. Player gains 4 block (X+1 = 3+1 = 4).

  - [ ] Sim - [ ] Live — **Test: Reinforced Body X can't be 0**
  Setup: Player has 3 energy, Reinforced Body in hand.
  Actions: Attempt to play Reinforced Body with X=0.
  Expected: Cannot play — X can't be 0. Player must spend at least 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Reinforced Body applies block twice**
  Setup: Player has 3 energy, Reinforced Body+ in hand, 0 block.
  Actions: Play Reinforced Body+ with X=2.
  Expected: Player spends 2 energy. Player gains 4 block (X BLK applied twice: 2 + 2 = 4).

- **Capacitor** [Y] — BGCapacitor — Power, Uncommon, Cost 1
  Gain 2 Orb slots.
  *Upgrade: Gain 3 Orb slots.*

  - [ ] Sim - [ ] Live — **Test: Basic Capacitor**
  Setup: Player has 3 energy, Capacitor in hand, 3 orb slots.
  Actions: Play Capacitor.
  Expected: Player gains 2 orb slots (now 5 total). Player spends 1 energy. Capacitor enters play as a power.

  - [ ] Sim - [ ] Live — **Test: Upgraded Capacitor**
  Setup: Player has 3 energy, Capacitor+ in hand, 3 orb slots.
  Actions: Play Capacitor+.
  Expected: Player gains 3 orb slots (now 6 total). Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Capacitor allows more orbs to be channeled**
  Setup: Player has 3 energy, Capacitor in hand, 3 orb slots all filled with Frost orbs.
  Actions: Play Capacitor. Then channel 1 Lightning orb.
  Expected: After Capacitor, player has 5 orb slots (3 Frost orbs + 2 empty). Lightning orb is channeled into an empty slot without evoking any existing orbs.

- **Consume** [Y] — BGConsume — Power, Uncommon, Cost 2
  Orb Evoke effects get +1.
  *Upgrade: Cost 2 to 1.*

  - [ ] Sim - [ ] Live — **Test: Consume boosts Lightning evoke**
  Setup: Player has 3 energy, Consume in hand, 1 Lightning orb in first slot, 3 orb slots all full (Lightning, Frost, Frost). One enemy with 20 HP.
  Actions: Play Consume. Then channel 1 Dark orb (forcing evoke of oldest Lightning).
  Expected: Consume enters play as a power. When the Lightning orb is evoked, it deals its base evoke damage + 1 bonus damage.

  - [ ] Sim - [ ] Live — **Test: Upgraded Consume costs 1**
  Setup: Player has 3 energy, Consume+ in hand, 0 orbs.
  Actions: Play Consume+.
  Expected: Player spends 1 energy (instead of 2). Consume+ enters play as a power. Orb evoke effects get +1.

  - [ ] Sim - [ ] Live — **Test: Consume boosts Frost evoke**
  Setup: Player has 3 energy, Consume in play as a power already. 3 orb slots all filled with Frost, Frost, Lightning.
  Actions: Channel 1 new orb (forcing evoke of oldest Frost).
  Expected: The evoked Frost orb grants its base block + 1 additional block from Consume.

- **Fusion** [Y] — BGFusion — Power, Uncommon, Cost 2
  Start of turn: Gain Energy(B).
  *Upgrade: Cost 2 to 1.*

  - [ ] Sim - [ ] Live — **Test: Basic Fusion**
  Setup: Player has 3 energy, Fusion in hand.
  Actions: Play Fusion. End turn. Start next turn.
  Expected: Fusion enters play as a power. Player spends 2 energy. At start of next turn, player gains 1 additional energy (4 total instead of 3).

  - [ ] Sim - [ ] Live — **Test: Upgraded Fusion costs 1**
  Setup: Player has 3 energy, Fusion+ in hand.
  Actions: Play Fusion+. End turn. Start next turn.
  Expected: Player spends 1 energy. At start of next turn, player gains 1 additional energy (4 total instead of 3).

  - [ ] Sim - [ ] Live — **Test: Multiple Fusions stack**
  Setup: Player has 2 Fusion powers already in play.
  Actions: End turn. Start next turn.
  Expected: At start of turn, player gains 2 additional energy (3 base + 2 from two Fusions = 5).

- **Heatsinks** [Y] — BGHeatsinks — Power, Uncommon, Cost 1
  Whenever you play a Power, draw 2 cards.
  *Upgrade: Draw 3 cards.*

  - [ ] Sim - [ ] Live — **Test: Heatsinks triggers on playing a power**
  Setup: Player has 3 energy, Heatsinks in play as a power. Storm (a power card) in hand. 5 cards in draw pile.
  Actions: Play Storm.
  Expected: Storm enters play. Heatsinks triggers, player draws 2 cards.

  - [ ] Sim - [ ] Live — **Test: Heatsinks does not trigger on non-power cards**
  Setup: Player has 3 energy, Heatsinks in play as a power. Ball Lightning (an attack) in hand. 5 cards in draw pile.
  Actions: Play Ball Lightning.
  Expected: Heatsinks does NOT trigger. No extra cards are drawn.

  - [ ] Sim - [ ] Live — **Test: Upgraded Heatsinks draws 3**
  Setup: Player has 3 energy, Heatsinks+ in play as a power. Loop (a power card) in hand. 5 cards in draw pile.
  Actions: Play Loop.
  Expected: Loop enters play. Heatsinks+ triggers, player draws 3 cards.

- **Loop** [Y] — BGLoop — Power, Uncommon, Cost 1
  End of turn: Trigger 1 Orb's End of turn ability.
  *Upgrade: End of turn: Trigger 1 Orb's End of turn ability twice.*

  - [ ] Sim - [ ] Live — **Test: Loop triggers Lightning orb end of turn**
  Setup: Player has 3 energy, Loop in play as a power. 1 Lightning orb in first orb slot. One enemy with 20 HP.
  Actions: End turn.
  Expected: The Lightning orb's end-of-turn ability triggers once (dealing its passive damage to a random enemy), plus once more from Loop (total 2 triggers for the Lightning orb's passive).

  - [ ] Sim - [ ] Live — **Test: Loop triggers Frost orb end of turn**
  Setup: Player has 3 energy, Loop in play as a power. 1 Frost orb in first orb slot. Player has 0 block.
  Actions: End turn.
  Expected: The Frost orb's end-of-turn ability triggers once (gaining passive block), plus once more from Loop (total 2 triggers of Frost passive block).

  - [ ] Sim - [ ] Live — **Test: Upgraded Loop triggers twice**
  Setup: Player has 3 energy, Loop+ in play as a power. 1 Lightning orb in first orb slot. One enemy with 20 HP.
  Actions: End turn.
  Expected: The Lightning orb's end-of-turn ability triggers once normally, plus twice from Loop+ (total 3 triggers of Lightning passive).

- **Machine Learning** [Y] — BGMachineLearning — Power, Uncommon, Cost 1
  Start of turn: Draw a card.
  *Upgrade: Cost 1 to 0.*

  - [ ] Sim - [ ] Live — **Test: Basic Machine Learning**
  Setup: Player has 3 energy, Machine Learning in hand. 10 cards in draw pile.
  Actions: Play Machine Learning. End turn. Start next turn.
  Expected: Machine Learning enters play. At start of next turn, player draws 6 cards (5 base + 1 from Machine Learning).

  - [ ] Sim - [ ] Live — **Test: Upgraded Machine Learning costs 0**
  Setup: Player has 3 energy, Machine Learning+ in hand. 10 cards in draw pile.
  Actions: Play Machine Learning+. End turn. Start next turn.
  Expected: Player spends 0 energy. At start of next turn, player draws 6 cards (5 base + 1).

  - [ ] Sim - [ ] Live — **Test: Multiple Machine Learnings stack**
  Setup: Player has 2 Machine Learning powers in play. 15 cards in draw pile.
  Actions: End turn. Start next turn.
  Expected: Player draws 7 cards at start of turn (5 base + 2 from two Machine Learnings).

- **Storm** [Y] — BGStorm — Power, Uncommon, Cost 1
  Start of turn: Channel 1 Lightning.
  *Upgrade: Start of turn: Channel 2 Lightning.*

  - [ ] Sim - [ ] Live — **Test: Basic Storm channels Lightning at start of turn**
  Setup: Player has 3 energy, Storm in hand, 0 orbs, 3 orb slots.
  Actions: Play Storm. End turn. Start next turn.
  Expected: Storm enters play. At start of next turn, 1 Lightning orb is channeled.

  - [ ] Sim - [ ] Live — **Test: Upgraded Storm channels 2 Lightning**
  Setup: Player has 3 energy, Storm+ in hand, 0 orbs, 3 orb slots.
  Actions: Play Storm+. End turn. Start next turn.
  Expected: At start of next turn, 2 Lightning orbs are channeled.

  - [ ] Sim - [ ] Live — **Test: Storm with full orb slots causes evoke**
  Setup: Player has Storm in play as a power. 3 orb slots all filled (Frost, Frost, Dark).
  Actions: End turn. Start next turn.
  Expected: At start of turn, Storm tries to channel 1 Lightning. Orb slots are full, so the oldest Frost orb is evoked first, then Lightning is channeled in the freed slot.
