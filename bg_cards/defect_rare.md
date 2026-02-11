# Defect (BGBlue) — Rare

- **All for One** [Y] — BGAllForOne — Attack, Rare, Cost 2
  2 HIT. Put all 0 cost cards from your discard pile into your hand.
  *Upgrade: 3 HIT.*

  - [ ] Sim - [ ] Live — **Test: Basic All for One retrieves 0-cost cards**
  Setup: Player has 3 energy, All for One in hand. Discard pile contains Zap (cost 0), FTL (cost 0), and Strike (cost 1). One enemy with 20 HP.
  Actions: Play All for One targeting enemy.
  Expected: Enemy takes 2 damage (2 HIT). Zap and FTL are moved from discard pile to hand. Strike remains in discard pile (costs 1, not 0). Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: All for One with no 0-cost cards in discard**
  Setup: Player has 3 energy, All for One in hand. Discard pile contains only Strike (cost 1) and Glacier (cost 2). One enemy with 20 HP.
  Actions: Play All for One targeting enemy.
  Expected: Enemy takes 2 damage (2 HIT). No cards are retrieved (no 0-cost cards in discard pile).

  - [ ] Sim - [ ] Live — **Test: Upgraded All for One**
  Setup: Player has 3 energy, All for One+ in hand. Discard pile contains Zap (cost 0). One enemy with 20 HP.
  Actions: Play All for One+ targeting enemy.
  Expected: Enemy takes 3 damage (3 HIT). Zap is moved from discard pile to hand.

- **Core Surge** [Y] — BGCoreSurge — Attack, Rare, Cost 1
  Retain. Remove all WEAK VULN from any player. 3 HIT.
  *Upgrade: Remove all WEAK VULN from all players. 4 HIT.*

  - [ ] Sim - [ ] Live — **Test: Core Surge removes debuffs from self**
  Setup: Player has 3 energy, Core Surge in hand, player has 2 stacks of WEAK and 1 stack of VULN. One enemy with 20 HP.
  Actions: Play Core Surge targeting self for debuff removal, targeting enemy for damage.
  Expected: All WEAK and VULN are removed from the player. Enemy takes 3 damage (3 HIT). Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Core Surge retains between turns**
  Setup: Player has 3 energy, Core Surge in hand plus 4 other cards. No debuffs on anyone.
  Actions: End turn without playing Core Surge.
  Expected: Core Surge remains in hand next turn (Retain). Other non-retained cards are discarded.

  - [ ] Sim - [ ] Live — **Test: Upgraded Core Surge removes debuffs from all players**
  Setup: Player has 3 energy, Core Surge+ in hand. Player has 2 WEAK, ally has 1 VULN. One enemy with 20 HP.
  Actions: Play Core Surge+ targeting enemy.
  Expected: All WEAK and VULN are removed from all players (player and ally). Enemy takes 4 damage (4 HIT).

- **Hyperbeam** [Y] — BGHyperbeam — Attack, Rare, Cost 2
  AOE 5 HIT. Remove all of your Orbs.
  *Upgrade: AOE 7 HIT. Remove all of your Orbs.*

  - [ ] Sim - [ ] Live — **Test: Basic Hyperbeam**
  Setup: Player has 3 energy, Hyperbeam in hand, 2 orbs channeled (Lightning, Frost). Two enemies with 20 HP each.
  Actions: Play Hyperbeam.
  Expected: Each enemy takes 5 damage (AOE 5 HIT). All player orbs are removed (not evoked). Player has 0 orbs. Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Hyperbeam with no orbs**
  Setup: Player has 3 energy, Hyperbeam in hand, 0 orbs. Two enemies with 20 HP each.
  Actions: Play Hyperbeam.
  Expected: Each enemy takes 5 damage (AOE 5 HIT). No orbs to remove. Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Hyperbeam**
  Setup: Player has 3 energy, Hyperbeam+ in hand, 3 orbs channeled (Frost, Frost, Dark). Two enemies with 20 HP each.
  Actions: Play Hyperbeam+.
  Expected: Each enemy takes 7 damage (AOE 7 HIT). All 3 orbs are removed. Player spends 2 energy.

- **Meteor Strike** [Y] — BGMeteorStrike — Attack, Rare, Cost 5
  10 HIT. Costs 1 less Energy(B) for each Power you have in play.
  *Upgrade: 15 HIT.*

  - [ ] Sim - [ ] Live — **Test: Meteor Strike with no powers (unplayable at 3 energy)**
  Setup: Player has 3 energy, Meteor Strike in hand. No powers in play. One enemy with 20 HP.
  Actions: Attempt to play Meteor Strike.
  Expected: Cannot play — costs 5 energy but player only has 3.

  - [ ] Sim - [ ] Live — **Test: Meteor Strike with 3 powers**
  Setup: Player has 3 energy, Meteor Strike in hand. 3 powers in play (e.g., Loop, Storm, Defragment). One enemy with 20 HP.
  Actions: Play Meteor Strike targeting enemy.
  Expected: Meteor Strike costs 2 energy (5 - 3 = 2). Enemy takes 10 damage (10 HIT). Player has 1 energy remaining.

  - [ ] Sim - [ ] Live — **Test: Upgraded Meteor Strike with 5 powers (free)**
  Setup: Player has 3 energy, Meteor Strike+ in hand. 5 powers in play. One enemy with 30 HP.
  Actions: Play Meteor Strike+ targeting enemy.
  Expected: Meteor Strike+ costs 0 energy (5 - 5 = 0). Enemy takes 15 damage (15 HIT). Player has 3 energy remaining.

  - [ ] Sim - [ ] Live — **Test: Meteor Strike with Strength**
  Setup: Player has 5 energy, Meteor Strike in hand, 2 Strength. No powers in play. One enemy with 30 HP.
  Actions: Play Meteor Strike targeting enemy.
  Expected: Player spends 5 energy. 10 HIT tokens, each dealing 1 + 2 Strength = 3 damage. Enemy takes 30 damage total.

- **Thunder Strike** [Y] — BGThunderStrike — Attack, Rare, Cost 3
  Deal AOE 4 HIT for each Lightning Orb you have.
  *Upgrade: Deal AOE 6 HIT for each Lightning Orb you have.*

  - [ ] Sim - [ ] Live — **Test: Thunder Strike with 2 Lightning orbs**
  Setup: Player has 3 energy, Thunder Strike in hand, 2 Lightning orbs and 1 Frost orb channeled. Two enemies with 30 HP each.
  Actions: Play Thunder Strike.
  Expected: Each enemy takes 8 damage (4 HIT x 2 Lightning orbs = 8 damage instances). Player spends 3 energy.

  - [ ] Sim - [ ] Live — **Test: Thunder Strike with no Lightning orbs**
  Setup: Player has 3 energy, Thunder Strike in hand, 2 Frost orbs channeled, 0 Lightning orbs. One enemy with 20 HP.
  Actions: Play Thunder Strike.
  Expected: Enemy takes 0 damage (4 HIT x 0 Lightning orbs = 0). Player spends 3 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Thunder Strike with 3 Lightning orbs**
  Setup: Player has 3 energy, Thunder Strike+ in hand, 3 Lightning orbs channeled. Two enemies with 40 HP each.
  Actions: Play Thunder Strike+.
  Expected: Each enemy takes 18 damage (6 HIT x 3 Lightning orbs = 18 damage instances). Player spends 3 energy.

- **Amplify** [Y] — BGAmplify — Skill, Rare, Cost 1
  Dark Orbs Evoke for +3 damage.
  *Upgrade: Dark Orbs Evoke for +5 damage.*

  - [ ] Sim - [ ] Live — **Test: Basic Amplify boosts Dark orb evoke**
  Setup: Player has 3 energy, Amplify in hand, 3 orb slots all full (Dark, Frost, Lightning). One enemy with 30 HP.
  Actions: Play Amplify. Then channel 1 new orb (forcing evoke of the Dark orb).
  Expected: Amplify is played. When the Dark orb is evoked, it deals its accumulated damage + 3 bonus damage to the enemy with the lowest HP.

  - [ ] Sim - [ ] Live — **Test: Upgraded Amplify boosts by +5**
  Setup: Player has 3 energy, Amplify+ in hand, 3 orb slots all full (Dark, Frost, Lightning). One enemy with 30 HP.
  Actions: Play Amplify+. Then channel 1 new orb (forcing evoke of the Dark orb).
  Expected: When the Dark orb is evoked, it deals its accumulated damage + 5 bonus damage.

  - [ ] Sim - [ ] Live — **Test: Amplify does not affect non-Dark orb evokes**
  Setup: Player has 3 energy, Amplify in play. 3 orb slots all full (Lightning, Frost, Frost). One enemy with 20 HP.
  Actions: Channel 1 new orb (forcing evoke of the Lightning orb).
  Expected: The Lightning orb evokes at its normal evoke damage. Amplify does not add bonus damage (only affects Dark orbs).

- **Fission** [Y] — BGFission — Skill, Rare, Cost 0
  Remove all of your Orbs. For each Orb removed, gain Energy(B) and draw a card. Exhaust.
  *Upgrade: Evoke all of your Orbs. For each Orb Evoked, gain Energy(B) and draw a card. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Basic Fission with 3 orbs**
  Setup: Player has 3 energy, Fission in hand, 3 orbs channeled (Lightning, Frost, Dark). 5 cards in draw pile.
  Actions: Play Fission.
  Expected: All 3 orbs are removed (not evoked). Player gains 3 energy (now 6). Player draws 3 cards. Fission is exhausted. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Fission with 0 orbs**
  Setup: Player has 3 energy, Fission in hand, 0 orbs. 5 cards in draw pile.
  Actions: Play Fission.
  Expected: No orbs to remove. Player gains 0 energy and draws 0 cards. Fission is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Fission evokes all orbs**
  Setup: Player has 3 energy, Fission+ in hand, 3 orbs channeled (Lightning, Frost, Dark). 5 cards in draw pile. One enemy with 30 HP.
  Actions: Play Fission+.
  Expected: All 3 orbs are evoked (Lightning deals evoke damage to a random enemy, Frost grants evoke block, Dark deals evoke damage to the enemy with lowest HP). Player gains 3 energy and draws 3 cards. Fission+ is exhausted.

- **Multi-Cast** [Y] — BGMultiCast — Skill, Rare, Cost -1
  Evoke 1 Orb X times.
  *Upgrade: Evoke 1 Orb X+1 times.*

  - [ ] Sim - [ ] Live — **Test: Multi-Cast with X=2 on Lightning orb**
  Setup: Player has 3 energy, Multi-Cast in hand, 1 Lightning orb in first slot (plus 2 other orbs). One enemy with 20 HP.
  Actions: Play Multi-Cast with X=2.
  Expected: Player spends 2 energy. The first orb (Lightning) is evoked 2 times, dealing its evoke damage to a random enemy twice.

  - [ ] Sim - [ ] Live — **Test: Multi-Cast with X=3 on Frost orb**
  Setup: Player has 3 energy, Multi-Cast in hand, 1 Frost orb in first slot (plus 2 other orbs). Player has 0 block.
  Actions: Play Multi-Cast with X=3.
  Expected: Player spends 3 energy. The first orb (Frost) is evoked 3 times, granting evoke block 3 times.

  - [ ] Sim - [ ] Live — **Test: Upgraded Multi-Cast with X=2 evokes 3 times**
  Setup: Player has 3 energy, Multi-Cast+ in hand, 1 Dark orb in first slot (plus 2 other orbs). One enemy with 30 HP.
  Actions: Play Multi-Cast+ with X=2.
  Expected: Player spends 2 energy. The first orb (Dark) is evoked 3 times (X+1 = 2+1 = 3), dealing its evoke damage three times.

- **Rainbow** [Y] — BGRainbow — Skill, Rare, Cost 2
  Channel 1 Lightning. Channel 1 Frost. Channel 1 Dark. Exhaust.
  *Upgrade: Channel 1 Lightning. Channel 1 Frost. Channel 1 Dark. (No longer Exhausts.)*

  - [ ] Sim - [ ] Live — **Test: Basic Rainbow channels 3 orbs**
  Setup: Player has 3 energy, Rainbow in hand, 0 orbs, 3 orb slots.
  Actions: Play Rainbow.
  Expected: Player channels 1 Lightning, 1 Frost, and 1 Dark orb (filling all 3 slots). Rainbow is exhausted. Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Rainbow when orb slots are partially full**
  Setup: Player has 3 energy, Rainbow in hand, 1 Frost orb in first slot, 3 orb slots total.
  Actions: Play Rainbow.
  Expected: Lightning is channeled (slot 2). Frost is channeled (slot 3). Dark is channeled, but slots are full, so the oldest orb (first Frost) is evoked first, then Dark occupies the freed slot. Rainbow is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Rainbow does not exhaust**
  Setup: Player has 3 energy, Rainbow+ in hand, 0 orbs, 3 orb slots.
  Actions: Play Rainbow+.
  Expected: Player channels 1 Lightning, 1 Frost, and 1 Dark orb. Rainbow+ goes to discard pile (not exhausted). Player spends 2 energy.

- **Seek** [Y] — BGSeek — Skill, Rare, Cost 0
  Search your draw pile for 1 card. Put that card into your hand, then shuffle your draw pile. Exhaust.
  *Upgrade: Search for 2 cards.*

  - [ ] Sim - [ ] Live — **Test: Basic Seek finds a card**
  Setup: Player has 3 energy, Seek in hand. Draw pile contains 10 cards including Glacier.
  Actions: Play Seek, choose Glacier from draw pile.
  Expected: Glacier moves from draw pile to hand. Draw pile is shuffled. Seek is exhausted. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Seek finds 2 cards**
  Setup: Player has 3 energy, Seek+ in hand. Draw pile contains 10 cards including Glacier and Ball Lightning.
  Actions: Play Seek+, choose Glacier and Ball Lightning from draw pile.
  Expected: Both Glacier and Ball Lightning move from draw pile to hand. Draw pile is shuffled. Seek+ is exhausted. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Seek with only 1 card in draw pile**
  Setup: Player has 3 energy, Seek in hand. Draw pile contains only 1 card (Zap).
  Actions: Play Seek, choose Zap.
  Expected: Zap moves to hand. Draw pile is now empty and shuffled (still empty). Seek is exhausted.

- **Skim** [Y] — BGSkim — Skill, Rare, Cost 1
  Draw 3 cards.
  *Upgrade: Draw 4 cards.*

  - [ ] Sim - [ ] Live — **Test: Basic Skim**
  Setup: Player has 3 energy, Skim in hand. 5 cards in draw pile.
  Actions: Play Skim.
  Expected: Player draws 3 cards from draw pile. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded Skim draws 4**
  Setup: Player has 3 energy, Skim+ in hand. 6 cards in draw pile.
  Actions: Play Skim+.
  Expected: Player draws 4 cards from draw pile. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Skim with fewer cards in draw pile than draw amount**
  Setup: Player has 3 energy, Skim in hand. 1 card in draw pile, 5 cards in discard pile.
  Actions: Play Skim.
  Expected: Player draws 1 card from draw pile. Discard pile is shuffled into draw pile. Player draws 2 more cards. Player spends 1 energy.

- **Tempest** [Y] — BGTempest — Skill, Rare, Cost -1
  Channel X Lightning. Exhaust.
  *Upgrade: Channel X+1 Lightning. Exhaust.*

  - [ ] Sim - [ ] Live — **Test: Tempest with X=3**
  Setup: Player has 3 energy, Tempest in hand, 0 orbs, 3 orb slots.
  Actions: Play Tempest with X=3.
  Expected: Player spends 3 energy. 3 Lightning orbs are channeled (filling all 3 slots). Tempest is exhausted.

  - [ ] Sim - [ ] Live — **Test: Tempest with X=0**
  Setup: Player has 0 energy, Tempest in hand, 0 orbs, 3 orb slots.
  Actions: Play Tempest with X=0.
  Expected: Player spends 0 energy. 0 Lightning orbs are channeled. Tempest is exhausted.

  - [ ] Sim - [ ] Live — **Test: Upgraded Tempest with X=2 channels 3**
  Setup: Player has 3 energy, Tempest+ in hand, 0 orbs, 3 orb slots.
  Actions: Play Tempest+ with X=2.
  Expected: Player spends 2 energy. 3 Lightning orbs are channeled (X+1 = 2+1 = 3). Tempest+ is exhausted.

  - [ ] Sim - [ ] Live — **Test: Tempest overflows orb slots causing evokes**
  Setup: Player has 3 energy, Tempest in hand, 2 Frost orbs channeled, 3 orb slots.
  Actions: Play Tempest with X=3.
  Expected: Player spends 3 energy. First Lightning fills slot 3. Second Lightning causes evoke of oldest Frost (slot 1). Third Lightning causes evoke of remaining Frost (slot 2). Player ends with 3 Lightning orbs. Tempest is exhausted.

- **Buffer** [Y] — BGBuffer — Power, Rare, Cost 2
  The next time you would lose HP, prevent it and Exhaust this card.
  *Upgrade: The next 2 times you would lose HP, prevent it and Exhaust this card.*

  - [ ] Sim - [ ] Live — **Test: Buffer prevents damage once**
  Setup: Player has 3 energy, Buffer in hand, 50 HP, 0 block. One enemy intending to deal 10 damage.
  Actions: Play Buffer. End turn. Enemy attacks for 10 damage.
  Expected: Buffer prevents the 10 damage. Player remains at 50 HP. Buffer is exhausted (removed from play).

  - [ ] Sim - [ ] Live — **Test: Buffer does not prevent block loss**
  Setup: Player has 3 energy, Buffer in play, 50 HP, 15 block. One enemy intending to deal 10 damage.
  Actions: End turn. Enemy attacks for 10 damage.
  Expected: Block absorbs the 10 damage (block goes from 15 to 5). Player remains at 50 HP. Buffer is NOT consumed (no HP was lost).

  - [ ] Sim - [ ] Live — **Test: Upgraded Buffer prevents damage twice**
  Setup: Player has 3 energy, Buffer+ in hand, 50 HP, 0 block. One enemy attacks twice for 8 damage each.
  Actions: Play Buffer+. End turn. Enemy attacks twice.
  Expected: First attack: Buffer+ prevents 8 damage (1 use consumed). Second attack: Buffer+ prevents 8 damage (2nd use consumed). Buffer+ is now exhausted. Player remains at 50 HP.

- **Defragment** [Y] — BGDefragment — Power, Rare, Cost 1
  Ethereal. Orb End of turn effects get +1.
  *Upgrade: Orb End of turn effects get +1. (No longer Ethereal.)*

  - [ ] Sim - [ ] Live — **Test: Defragment boosts orb passive**
  Setup: Player has 3 energy, Defragment in hand, 1 Lightning orb channeled. One enemy with 20 HP.
  Actions: Play Defragment. End turn.
  Expected: Defragment enters play. At end of turn, Lightning orb's passive deals its base passive damage + 1 from Defragment.

  - [ ] Sim - [ ] Live — **Test: Defragment is Ethereal (exhausts if not played)**
  Setup: Player has 3 energy, Defragment in hand plus 4 other cards.
  Actions: End turn without playing Defragment.
  Expected: Defragment is exhausted at end of turn (Ethereal). It does not go to discard pile.

  - [ ] Sim - [ ] Live — **Test: Upgraded Defragment is not Ethereal**
  Setup: Player has 3 energy, Defragment+ in hand plus 4 other cards.
  Actions: End turn without playing Defragment+.
  Expected: Defragment+ goes to discard pile at end of turn (no longer Ethereal). It is not exhausted.

  - [ ] Sim - [ ] Live — **Test: Defragment boosts Frost passive**
  Setup: Player has 3 energy, Defragment in play as a power. 1 Frost orb channeled. Player has 0 block.
  Actions: End turn.
  Expected: At end of turn, Frost orb's passive grants its base block + 1 additional block from Defragment.

- **Echo Form** [Y] — BGEchoForm — Power, Rare, Cost 3
  Ethereal. Start of turn: The first Attack or Skill you play is played twice.
  *Upgrade: Start of turn: The first Attack or Skill you play is played twice. (No longer Ethereal.)*

  - [ ] Sim - [ ] Live — **Test: Echo Form doubles first attack**
  Setup: Player has 3 energy, Echo Form in play (played previous turn). Ball Lightning (1 HIT, channel 1 Lightning) in hand. One enemy with 20 HP.
  Actions: Play Ball Lightning targeting enemy.
  Expected: Ball Lightning is played twice. Enemy takes 2 damage total (1 HIT x 2 plays). Player channels 2 Lightning orbs (1 per play). Player spends 1 energy (only pays once).

  - [ ] Sim - [ ] Live — **Test: Echo Form does not double second card**
  Setup: Player has 3 energy, Echo Form in play. Strike and Zap in hand. One enemy with 20 HP.
  Actions: Play Strike targeting enemy. Play Zap.
  Expected: Strike is played twice (first card, doubled by Echo Form). Zap is played once (second card, not doubled).

  - [ ] Sim - [ ] Live — **Test: Echo Form is Ethereal**
  Setup: Player has 3 energy, Echo Form in hand plus 4 other cards.
  Actions: End turn without playing Echo Form.
  Expected: Echo Form is exhausted at end of turn (Ethereal).

  - [ ] Sim - [ ] Live — **Test: Upgraded Echo Form is not Ethereal**
  Setup: Player has 3 energy, Echo Form+ in hand plus 4 other cards.
  Actions: End turn without playing Echo Form+.
  Expected: Echo Form+ goes to discard pile (no longer Ethereal). It is not exhausted.

- **Electrodynamics** [Y] — BGElectrodynamics — Power, Rare, Cost 2
  Lightning deals damage to any row instead of a single target. When played, Channel 2 Lightning.
  *Upgrade: Channel 3 Lightning.*

  - [ ] Sim - [ ] Live — **Test: Basic Electrodynamics channels 2 Lightning on play**
  Setup: Player has 3 energy, Electrodynamics in hand, 0 orbs, 3 orb slots.
  Actions: Play Electrodynamics.
  Expected: Electrodynamics enters play. 2 Lightning orbs are channeled. Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Electrodynamics makes Lightning hit any row**
  Setup: Player has 3 energy, Electrodynamics in play. 1 Lightning orb channeled. Two enemies in different rows with 20 HP each.
  Actions: End turn (Lightning passive triggers).
  Expected: Lightning orb's passive damage hits all enemies in the targeted row (instead of just a single target), due to Electrodynamics.

  - [ ] Sim - [ ] Live — **Test: Upgraded Electrodynamics channels 3 Lightning**
  Setup: Player has 3 energy, Electrodynamics+ in hand, 0 orbs, 3 orb slots.
  Actions: Play Electrodynamics+.
  Expected: Electrodynamics+ enters play. 3 Lightning orbs are channeled (filling all 3 slots). Player spends 2 energy.

- **Static Discharge** [Y] — BGStaticDischarge — Power, Rare, Cost 1
  Lightning Orb End of turn effects get +1.
  *Upgrade: Lightning Orb End of turn effects get +2.*

  - [ ] Sim - [ ] Live — **Test: Static Discharge boosts Lightning passive**
  Setup: Player has 3 energy, Static Discharge in hand, 1 Lightning orb channeled. One enemy with 20 HP.
  Actions: Play Static Discharge. End turn.
  Expected: Static Discharge enters play. At end of turn, Lightning orb's passive deals its base passive damage + 1 from Static Discharge.

  - [ ] Sim - [ ] Live — **Test: Static Discharge does not affect Frost passive**
  Setup: Player has 3 energy, Static Discharge in play. 1 Frost orb channeled. Player has 0 block.
  Actions: End turn.
  Expected: Frost orb's passive grants its base block only. Static Discharge does not boost Frost (only Lightning).

  - [ ] Sim - [ ] Live — **Test: Upgraded Static Discharge boosts by +2**
  Setup: Player has 3 energy, Static Discharge+ in hand, 1 Lightning orb channeled. One enemy with 20 HP.
  Actions: Play Static Discharge+. End turn.
  Expected: At end of turn, Lightning orb's passive deals its base passive damage + 2 from Static Discharge+.
