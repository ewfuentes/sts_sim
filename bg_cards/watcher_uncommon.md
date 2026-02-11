# Watcher (BGPurple) — Uncommon

- **Crush Joints** [Y] — BGCrushJoints — Attack, Uncommon, Cost 1
  1 HIT. If you're in Wrath, VULN.
  *Upgrade: 2 HIT. If you're in Wrath, VULN.*

  - [ ] Sim - [ ] Live — **Test: Basic damage from Neutral stance**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. Player has 0 Strength.
  Actions: Play Crush Joints targeting the enemy.
  Expected: Enemy loses 1 HP (down to 19). No Vulnerable applied. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Wrath stance applies Vulnerable**
  Setup: Player in Wrath stance, 3 energy. Enemy at 20 HP, 0 block. Player has 0 Strength.
  Actions: Play Crush Joints targeting the enemy.
  Expected: Enemy loses 2 HP (1 HIT doubled by Wrath = 2 damage). Enemy gains Vulnerable. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded version deals 2 HIT in Wrath**
  Setup: Player in Wrath stance, 3 energy. Enemy at 20 HP, 0 block. Player has 0 Strength. Crush Joints is upgraded.
  Actions: Play Crush Joints+ targeting the enemy.
  Expected: Enemy loses 4 HP (2 HIT x 2 from Wrath = 4 damage). Enemy gains Vulnerable.

- **Fear No Evil** [Y] — BGFearNoEvil — Attack, Uncommon, Cost 1
  2 HIT. If you're in Wrath, enter Calm.
  *Upgrade: 3 HIT. If you're in Wrath, enter Calm.*

  - [ ] Sim - [ ] Live — **Test: Basic damage from Neutral stance**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. Player has 0 Strength.
  Actions: Play Fear No Evil targeting the enemy.
  Expected: Enemy loses 2 HP. Player remains in Neutral stance.

  - [ ] Sim - [ ] Live — **Test: Wrath stance transitions to Calm**
  Setup: Player in Wrath stance, 3 energy. Enemy at 20 HP, 0 block. Player has 0 Strength.
  Actions: Play Fear No Evil targeting the enemy.
  Expected: Enemy loses 4 HP (2 HIT doubled by Wrath). Player enters Calm stance.

  - [ ] Sim - [ ] Live — **Test: Upgraded version deals 3 HIT from Wrath and enters Calm**
  Setup: Player in Wrath stance, 3 energy. Enemy at 20 HP, 0 block. Player has 0 Strength. Fear No Evil is upgraded.
  Actions: Play Fear No Evil+ targeting the enemy.
  Expected: Enemy loses 6 HP (3 HIT doubled by Wrath). Player enters Calm stance.

- **Foreign Influence** [Y] — BGForeignInfluence — Attack, Uncommon, Cost 0
  3 HIT - or - Play a copy of the last Attack played by another player this turn.
  *Upgrade: 4 HIT.*

  - [ ] Sim - [ ] Live — **Test: Basic 3 HIT mode**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. No other player has played an Attack this turn.
  Actions: Play Foreign Influence targeting the enemy.
  Expected: Enemy loses 3 HP. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded version deals 4 HIT**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. Foreign Influence is upgraded.
  Actions: Play Foreign Influence+ targeting the enemy.
  Expected: Enemy loses 4 HP. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Copy another player's Attack**
  Setup: Player in Neutral stance, 3 energy. Another player played a 5 HIT Attack earlier this turn. Enemy at 20 HP, 0 block.
  Actions: Play Foreign Influence, choosing the copy mode.
  Expected: A copy of the other player's 5 HIT Attack is played. Enemy loses 5 HP. Player spends 0 energy.

- **Sash Whip** [Y] — BGSashWhip — Attack, Uncommon, Cost 1
  2 HIT. If you're in Calm, WEAK.
  *Upgrade: 2 HIT. If you're in Calm, WEAK WEAK.*

  - [ ] Sim - [ ] Live — **Test: Basic damage from Neutral stance, no Weak**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block.
  Actions: Play Sash Whip targeting the enemy.
  Expected: Enemy loses 2 HP. No Weak applied.

  - [ ] Sim - [ ] Live — **Test: Calm stance applies Weak**
  Setup: Player in Calm stance, 3 energy. Enemy at 20 HP, 0 block.
  Actions: Play Sash Whip targeting the enemy.
  Expected: Enemy loses 2 HP. Enemy gains 1 stack of Weak.

  - [ ] Sim - [ ] Live — **Test: Upgraded version applies double Weak in Calm**
  Setup: Player in Calm stance, 3 energy. Enemy at 20 HP, 0 block. Sash Whip is upgraded.
  Actions: Play Sash Whip+ targeting the enemy.
  Expected: Enemy loses 2 HP. Enemy gains 2 stacks of Weak.

- **Tantrum** [Y] — BGTantrum — Attack, Uncommon, Cost 1
  2 HIT. Enter Wrath. Put this card on top of your draw pile.
  *Upgrade: 1 HIT 1 HIT. Enter Wrath. Put this card on top of your draw pile.*

  - [ ] Sim - [ ] Live — **Test: Basic damage and enters Wrath**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. Draw pile has 5 cards.
  Actions: Play Tantrum targeting the enemy.
  Expected: Enemy loses 2 HP. Player enters Wrath. Tantrum is placed on top of draw pile (not in discard).

  - [ ] Sim - [ ] Live — **Test: Upgraded version deals two separate hits**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. Player has 2 Strength. Tantrum is upgraded.
  Actions: Play Tantrum+ targeting the enemy.
  Expected: Enemy loses 6 HP (two separate hits of 1+2=3 each). Player enters Wrath. Tantrum+ placed on top of draw pile.

  - [ ] Sim - [ ] Live — **Test: Card returns to draw pile, can be drawn again**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. Draw pile is empty.
  Actions: Play Tantrum targeting the enemy. Then draw 1 card.
  Expected: Enemy loses 2 HP. Player enters Wrath. Tantrum is drawn again since it was placed on top of draw pile.

- **Carve Reality** [Y] — BGCarveReality — Attack, Uncommon, Cost 1
  Deal 3 HIT to one or two enemies.
  *Upgrade: Deal 4 HIT to one or two enemies.*

  - [ ] Sim - [ ] Live — **Test: Single target damage**
  Setup: Player in Neutral stance, 3 energy. One enemy at 20 HP, 0 block.
  Actions: Play Carve Reality targeting the single enemy.
  Expected: Enemy loses 3 HP.

  - [ ] Sim - [ ] Live — **Test: Two-target damage splits correctly**
  Setup: Player in Neutral stance, 3 energy. Enemy A at 20 HP and Enemy B at 15 HP, both 0 block.
  Actions: Play Carve Reality targeting Enemy A and Enemy B.
  Expected: Enemy A loses 3 HP (down to 17). Enemy B loses 3 HP (down to 12).

  - [ ] Sim - [ ] Live — **Test: Upgraded version with Strength bonus**
  Setup: Player in Neutral stance, 3 energy, 2 Strength. Enemy at 20 HP, 0 block. Carve Reality is upgraded.
  Actions: Play Carve Reality+ targeting the enemy.
  Expected: Enemy loses 6 HP (4 HIT + 2 Strength = 6 damage).

- **Sands of Time** [Y] — BGSandsOfTime — Attack, Uncommon, Cost 2
  Retain. 3 HIT. +2 damage for each other card with Retain in your hand.
  *Upgrade: +3 damage per Retain card.*

  - [ ] Sim - [ ] Live — **Test: Basic damage with no other Retain cards**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. No other Retain cards in hand.
  Actions: Play Sands of Time targeting the enemy.
  Expected: Enemy loses 3 HP. Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Bonus damage from other Retain cards in hand**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. Hand contains Sands of Time and 2 other cards with Retain.
  Actions: Play Sands of Time targeting the enemy.
  Expected: Enemy loses 7 HP (3 base + 2x2 from Retain cards).

  - [ ] Sim - [ ] Live — **Test: Upgraded version scales harder with Retain cards**
  Setup: Player in Neutral stance, 3 energy. Enemy at 30 HP, 0 block. Hand contains Sands of Time+ and 3 other cards with Retain.
  Actions: Play Sands of Time+ targeting the enemy.
  Expected: Enemy loses 12 HP (3 base + 3x3 from Retain cards).

  - [ ] Sim - [ ] Live — **Test: Retain keyword keeps card in hand at end of turn**
  Setup: Player in Neutral stance, 3 energy. Hand contains Sands of Time and 4 other non-Retain cards.
  Actions: End turn without playing Sands of Time.
  Expected: The 4 non-Retain cards are discarded. Sands of Time remains in hand for next turn.

- **Windmill Strike** [Y] — BGWindmillStrike — Attack, Uncommon, Cost 2
  Retain. 2 HIT. +3 damage if this was Retained last turn.
  *Upgrade: +5 damage if this was Retained last turn.*

  - [ ] Sim - [ ] Live — **Test: Base damage without being Retained**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. Windmill Strike was just drawn this turn (not Retained).
  Actions: Play Windmill Strike targeting the enemy.
  Expected: Enemy loses 2 HP.

  - [ ] Sim - [ ] Live — **Test: Bonus damage after being Retained**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. Windmill Strike was Retained from the previous turn.
  Actions: Play Windmill Strike targeting the enemy.
  Expected: Enemy loses 5 HP (2 base + 3 Retain bonus).

  - [ ] Sim - [ ] Live — **Test: Upgraded version after being Retained**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. Windmill Strike+ was Retained from the previous turn.
  Actions: Play Windmill Strike+ targeting the enemy.
  Expected: Enemy loses 7 HP (2 base + 5 Retain bonus).

- **Wallop** [Y] — BGWallop — Attack, Uncommon, Cost 2
  2 HIT. Gain BLK equal to the unblocked damage dealt.
  *Upgrade: 3 HIT.*

  - [ ] Sim - [ ] Live — **Test: Full damage converts to block**
  Setup: Player in Neutral stance, 3 energy, 0 block. Enemy at 20 HP, 0 block.
  Actions: Play Wallop targeting the enemy.
  Expected: Enemy loses 2 HP. Player gains 2 block.

  - [ ] Sim - [ ] Live — **Test: Enemy has block, only unblocked damage becomes block**
  Setup: Player in Neutral stance, 3 energy, 0 block. Enemy at 20 HP, 1 block.
  Actions: Play Wallop targeting the enemy.
  Expected: Enemy's 1 block is consumed, enemy loses 1 HP (down to 19). Player gains 1 block (only unblocked damage).

  - [ ] Sim - [ ] Live — **Test: Upgraded version with Wrath stance**
  Setup: Player in Wrath stance, 3 energy, 0 block. Enemy at 20 HP, 0 block. Wallop is upgraded.
  Actions: Play Wallop+ targeting the enemy.
  Expected: Enemy loses 6 HP (3 HIT doubled by Wrath). Player gains 6 block.

- **Weave** [Y] — BGWeave — Attack, Uncommon, Cost 0
  1 HIT. If you would discard this card while Scrying, instead play it and it deals +5 damage.
  *Upgrade: 2 HIT. +6 damage while Scrying.*

  - [ ] Sim - [ ] Live — **Test: Basic play from hand**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block.
  Actions: Play Weave targeting the enemy.
  Expected: Enemy loses 1 HP. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Auto-played when discarded during Scry**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. Weave is on top of draw pile.
  Actions: Scry 1 (revealing Weave). Choose to discard Weave.
  Expected: Instead of being discarded, Weave is played automatically. Enemy loses 6 HP (1 base + 5 Scry bonus).

  - [ ] Sim - [ ] Live — **Test: Upgraded version auto-played during Scry**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP, 0 block. Weave+ is on top of draw pile.
  Actions: Scry 1 (revealing Weave+). Choose to discard Weave+.
  Expected: Instead of being discarded, Weave+ is played automatically. Enemy loses 8 HP (2 base + 6 Scry bonus).

- **Signature Move** [Y] — BGSignatureMove — Attack, Uncommon, Cost 2
  Can only be played if this is the only Attack in your hand. 6 HIT.
  *Upgrade: 8 HIT.*

  - [ ] Sim - [ ] Live — **Test: Playable when only Attack in hand**
  Setup: Player in Neutral stance, 3 energy. Hand contains Signature Move and 3 Skill cards. Enemy at 20 HP, 0 block.
  Actions: Play Signature Move targeting the enemy.
  Expected: Enemy loses 6 HP. Player spends 2 energy.

  - [ ] Sim - [ ] Live — **Test: Unplayable when other Attacks are in hand**
  Setup: Player in Neutral stance, 3 energy. Hand contains Signature Move and 1 Strike (Attack). Enemy at 20 HP, 0 block.
  Actions: Attempt to play Signature Move.
  Expected: Signature Move cannot be played because another Attack is in hand.

  - [ ] Sim - [ ] Live — **Test: Upgraded version deals 8 HIT**
  Setup: Player in Neutral stance, 3 energy. Hand contains Signature Move+ and 2 Skill cards. Enemy at 30 HP, 0 block. Player has 0 Strength.
  Actions: Play Signature Move+ targeting the enemy.
  Expected: Enemy loses 8 HP (down to 22).

- **Conclude** [Y] — BGConclude — Attack, Uncommon, Cost 1
  AOE 1 HIT 1 HIT. You can't play additional cards this turn.
  *Upgrade: AOE 1 HIT 1 HIT 1 HIT.*

  - [ ] Sim - [ ] Live — **Test: AOE hits all enemies and ends card plays**
  Setup: Player in Neutral stance, 3 energy. Enemy A at 15 HP, Enemy B at 10 HP, both 0 block. Hand has Conclude and 2 other cards.
  Actions: Play Conclude.
  Expected: Enemy A loses 2 HP (two hits of 1). Enemy B loses 2 HP (two hits of 1). Player cannot play any more cards this turn.

  - [ ] Sim - [ ] Live — **Test: Upgraded version deals 3 hits AOE**
  Setup: Player in Neutral stance, 3 energy. Enemy A at 15 HP, Enemy B at 10 HP, both 0 block. Conclude is upgraded.
  Actions: Play Conclude+.
  Expected: Enemy A loses 3 HP (three hits of 1). Enemy B loses 3 HP (three hits of 1). Player cannot play any more cards this turn.

  - [ ] Sim - [ ] Live — **Test: Strength adds to each hit**
  Setup: Player in Neutral stance, 3 energy, 2 Strength. Enemy at 20 HP, 0 block.
  Actions: Play Conclude.
  Expected: Enemy loses 6 HP (two hits of 1+2=3 each). Player cannot play more cards this turn.

- **Reach Heaven** [Y] — BGReachHeaven — Attack, Uncommon, Cost 2
  2 HIT. +1 damage for each MIRACLE you have.
  *Upgrade: +2 damage per MIRACLE.*

  - [ ] Sim - [ ] Live — **Test: Base damage with no Miracles**
  Setup: Player in Neutral stance, 3 energy, 0 Miracles. Enemy at 20 HP, 0 block.
  Actions: Play Reach Heaven targeting the enemy.
  Expected: Enemy loses 2 HP.

  - [ ] Sim - [ ] Live — **Test: Bonus damage scales with Miracles**
  Setup: Player in Neutral stance, 3 energy, 3 Miracles. Enemy at 20 HP, 0 block.
  Actions: Play Reach Heaven targeting the enemy.
  Expected: Enemy loses 5 HP (2 base + 3x1 from Miracles).

  - [ ] Sim - [ ] Live — **Test: Upgraded version scales harder with Miracles**
  Setup: Player in Neutral stance, 3 energy, 3 Miracles. Enemy at 20 HP, 0 block. Reach Heaven is upgraded.
  Actions: Play Reach Heaven+ targeting the enemy.
  Expected: Enemy loses 8 HP (2 base + 3x2 from Miracles).

- **Empty Mind** [Y] — BGEmptyMind — Skill, Uncommon, Cost 1
  Draw 2 cards. Enter Neutral.
  *Upgrade: Draw 3 cards. Enter Neutral.*

  - [ ] Sim - [ ] Live — **Test: Draw cards and enter Neutral from Wrath**
  Setup: Player in Wrath stance, 3 energy. Draw pile has 5+ cards. Hand has 2 cards including Empty Mind.
  Actions: Play Empty Mind.
  Expected: Player draws 2 cards (hand now has 3 cards). Player enters Neutral stance. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Enter Neutral from Calm grants energy**
  Setup: Player in Calm stance, 3 energy. Draw pile has 5+ cards.
  Actions: Play Empty Mind.
  Expected: Player draws 2 cards. Player leaves Calm (gaining 2 energy from Calm exit) and enters Neutral. Player has 4 energy (3 - 1 cost + 2 from Calm).

  - [ ] Sim - [ ] Live — **Test: Upgraded version draws 3 cards**
  Setup: Player in Wrath stance, 3 energy. Draw pile has 5+ cards. Empty Mind is upgraded.
  Actions: Play Empty Mind+.
  Expected: Player draws 3 cards. Player enters Neutral stance.

- **Meditate** [Y] — BGMeditate — Skill, Uncommon, Cost 1
  Put 1 card from your discard pile into your hand and Retain it. Enter Calm. You can't play additional cards this turn.
  *Upgrade: Put 2 cards from your discard pile into your hand.*

  - [ ] Sim - [ ] Live — **Test: Retrieve card from discard, enter Calm, end plays**
  Setup: Player in Neutral stance, 3 energy. Discard pile contains Strike and Defend. Hand has Meditate and 1 other card.
  Actions: Play Meditate, choosing Strike from the discard pile.
  Expected: Strike moves from discard pile to hand with Retain. Player enters Calm. Player cannot play additional cards this turn.

  - [ ] Sim - [ ] Live — **Test: Upgraded version retrieves 2 cards**
  Setup: Player in Neutral stance, 3 energy. Discard pile contains Strike, Defend, and Eruption. Hand has Meditate+.
  Actions: Play Meditate+, choosing Strike and Defend from the discard pile.
  Expected: Strike and Defend move to hand, both with Retain. Player enters Calm. Player cannot play additional cards this turn.

  - [ ] Sim - [ ] Live — **Test: Retrieved card retains into next turn**
  Setup: Player in Neutral stance, 3 energy. Discard pile contains Windmill Strike. Hand has Meditate.
  Actions: Play Meditate, choosing Windmill Strike. End turn.
  Expected: Windmill Strike remains in hand next turn (it was given Retain). Player is in Calm at start of next turn.

- **Inner Peace** [Y] — BGInnerPeace — Skill, Uncommon, Cost 1
  If you're in Calm, draw 3 cards. Otherwise, enter Calm.
  *Upgrade: Draw 4 cards.*

  - [ ] Sim - [ ] Live — **Test: In Calm, draw 3 cards**
  Setup: Player in Calm stance, 3 energy. Draw pile has 5+ cards. Hand has Inner Peace and 1 other card.
  Actions: Play Inner Peace.
  Expected: Player draws 3 cards (hand now has 4 cards). Player remains in Calm.

  - [ ] Sim - [ ] Live — **Test: Not in Calm, enter Calm**
  Setup: Player in Neutral stance, 3 energy. Draw pile has 5+ cards.
  Actions: Play Inner Peace.
  Expected: Player enters Calm. No cards drawn. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded version draws 4 in Calm**
  Setup: Player in Calm stance, 3 energy. Draw pile has 5+ cards. Inner Peace is upgraded.
  Actions: Play Inner Peace+.
  Expected: Player draws 4 cards.

- **Indignation** [Y] — BGIndignation — Skill, Uncommon, Cost 1
  If you're in Wrath, VULN. Otherwise, enter Wrath.
  *Upgrade: If you're in Wrath, AOE VULN. Otherwise, enter Wrath.*

  - [ ] Sim - [ ] Live — **Test: Not in Wrath, enter Wrath**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP.
  Actions: Play Indignation.
  Expected: Player enters Wrath stance. No Vulnerable applied.

  - [ ] Sim - [ ] Live — **Test: In Wrath, apply Vulnerable to target**
  Setup: Player in Wrath stance, 3 energy. Enemy at 20 HP.
  Actions: Play Indignation.
  Expected: Enemy gains Vulnerable. Player remains in Wrath.

  - [ ] Sim - [ ] Live — **Test: Upgraded in Wrath, AOE Vulnerable**
  Setup: Player in Wrath stance, 3 energy. Enemy A at 20 HP, Enemy B at 15 HP. Indignation is upgraded.
  Actions: Play Indignation+.
  Expected: Both Enemy A and Enemy B gain Vulnerable. Player remains in Wrath.

- **Swivel** [Y] — BGSwivel — Skill, Uncommon, Cost 2
  2 BLK. The next Attack you play this turn costs 0.
  *Upgrade: 3 BLK to any player. The next Attack you play this turn costs 0.*

  - [ ] Sim - [ ] Live — **Test: Gain block and make next Attack free**
  Setup: Player in Neutral stance, 3 energy, 0 block. Hand has Swivel and a cost-2 Attack.
  Actions: Play Swivel. Then play the cost-2 Attack.
  Expected: Player gains 2 block. The Attack costs 0 energy to play. Total energy spent: 2 (only Swivel's cost).

  - [ ] Sim - [ ] Live — **Test: Only the next Attack is free**
  Setup: Player in Neutral stance, 4 energy, 0 block. Hand has Swivel and two cost-1 Attacks.
  Actions: Play Swivel. Play the first Attack. Play the second Attack.
  Expected: Player gains 2 block. First Attack costs 0. Second Attack costs its normal 1 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded version grants 3 block to any player**
  Setup: Player in Neutral stance, 3 energy, 0 block. Ally at 0 block. Swivel is upgraded.
  Actions: Play Swivel+, targeting the ally for block.
  Expected: Ally gains 3 block. The next Attack the player plays this turn costs 0.

- **Perseverance** [Y] — BGPerseverance — Skill, Uncommon, Cost 1
  Retain. 1 BLK. +2 BLK if this was Retained last turn.
  *Upgrade: Retain. 2 BLK. +2 BLK if this was Retained last turn.*

  - [ ] Sim - [ ] Live — **Test: Base block without being Retained**
  Setup: Player in Neutral stance, 3 energy, 0 block. Perseverance was just drawn this turn.
  Actions: Play Perseverance.
  Expected: Player gains 1 block. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Bonus block after being Retained**
  Setup: Player in Neutral stance, 3 energy, 0 block. Perseverance was Retained from the previous turn.
  Actions: Play Perseverance.
  Expected: Player gains 3 block (1 base + 2 Retain bonus).

  - [ ] Sim - [ ] Live — **Test: Upgraded version with Retain bonus**
  Setup: Player in Neutral stance, 3 energy, 0 block. Perseverance+ was Retained from the previous turn.
  Actions: Play Perseverance+.
  Expected: Player gains 4 block (2 base + 2 Retain bonus).

- **Pray** [Y] — BGPray — Skill, Uncommon, Cost 1
  MIRACLE. Draw 2 cards. You can't draw additional cards this turn.
  *Upgrade: MIRACLE MIRACLE. Draw 2 cards. You can't draw additional cards this turn.*

  - [ ] Sim - [ ] Live — **Test: Gain Miracle and draw cards**
  Setup: Player in Neutral stance, 3 energy, 0 Miracles. Draw pile has 5+ cards.
  Actions: Play Pray.
  Expected: Player gains 1 Miracle. Player draws 2 cards. Player spends 1 energy.

  - [ ] Sim - [ ] Live — **Test: Draw lock prevents further draws this turn**
  Setup: Player in Neutral stance, 3 energy, 0 Miracles. Draw pile has 5+ cards. Hand has Pray and a card that says "draw 1 card."
  Actions: Play Pray. Then play the draw card.
  Expected: Player gains 1 Miracle. Player draws 2 cards from Pray. The subsequent draw card's draw effect is prevented.

  - [ ] Sim - [ ] Live — **Test: Upgraded version grants 2 Miracles**
  Setup: Player in Neutral stance, 3 energy, 0 Miracles. Draw pile has 5+ cards. Pray is upgraded.
  Actions: Play Pray+.
  Expected: Player gains 2 Miracles. Player draws 2 cards.

- **Prostrate** [Y] — BGProstrate — Skill, Uncommon, Cost 0
  1 BLK. MIRACLE.
  *Upgrade: 2 BLK. MIRACLE.*

  - [ ] Sim - [ ] Live — **Test: Gain block and Miracle**
  Setup: Player in Neutral stance, 3 energy, 0 block, 0 Miracles.
  Actions: Play Prostrate.
  Expected: Player gains 1 block. Player gains 1 Miracle. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Upgraded version gives 2 block**
  Setup: Player in Neutral stance, 3 energy, 0 block, 0 Miracles. Prostrate is upgraded.
  Actions: Play Prostrate+.
  Expected: Player gains 2 block. Player gains 1 Miracle. Player spends 0 energy.

  - [ ] Sim - [ ] Live — **Test: Miracle can be spent for energy**
  Setup: Player in Neutral stance, 0 energy, 0 block, 0 Miracles.
  Actions: Play Prostrate (costs 0). Spend the gained Miracle for 1 energy.
  Expected: Player gains 1 block, 1 Miracle. After spending Miracle, player has 1 energy.

- **Wreath of Flame** [Y] — BGWreathOfFlame — Skill, Uncommon, Cost -1
  Gain X STR. Lose X STR at end of turn. Exhaust.
  *Upgrade: Gain X STR. Lose X STR at end of turn. (No longer Exhausts.)*

  - [ ] Sim - [ ] Live — **Test: Spend all energy for temporary Strength**
  Setup: Player in Neutral stance, 3 energy, 0 Strength. Enemy at 20 HP.
  Actions: Play Wreath of Flame (X=3, spending all 3 energy).
  Expected: Player gains 3 Strength. Player has 0 energy. Card is exhausted.

  - [ ] Sim - [ ] Live — **Test: Temporary Strength is lost at end of turn**
  Setup: Player in Neutral stance, 3 energy, 0 Strength. Enemy at 20 HP.
  Actions: Play Wreath of Flame (X=3). End turn.
  Expected: Player gains 3 Strength immediately. At end of turn, player loses 3 Strength (back to 0).

  - [ ] Sim - [ ] Live — **Test: Upgraded version does not Exhaust**
  Setup: Player in Neutral stance, 2 energy, 0 Strength. Wreath of Flame is upgraded.
  Actions: Play Wreath of Flame+ (X=2).
  Expected: Player gains 2 Strength. Card goes to discard pile instead of being exhausted. At end of turn, player loses 2 Strength.

- **Battle Hymn** [Y] — BGBattleHymn — Power, Uncommon, Cost 1
  Once per turn: Deal 1 damage, +1 if you're in Wrath.
  *Upgrade: Deal 2 damage, +2 if you're in Wrath.*

  - [ ] Sim - [ ] Live — **Test: Basic passive damage from Neutral**
  Setup: Player in Neutral stance, 3 energy. Enemy at 20 HP.
  Actions: Play Battle Hymn. End turn.
  Expected: Battle Hymn power is active. Once this turn (or at trigger point), enemy takes 1 damage.

  - [ ] Sim - [ ] Live — **Test: Wrath bonus doubles the passive damage**
  Setup: Player in Wrath stance, 3 energy. Battle Hymn already active. Enemy at 20 HP.
  Actions: End turn (or trigger Battle Hymn).
  Expected: Enemy takes 2 damage (1 base + 1 Wrath bonus).

  - [ ] Sim - [ ] Live — **Test: Upgraded version deals more base and Wrath damage**
  Setup: Player in Wrath stance, 3 energy. Enemy at 20 HP. Battle Hymn is upgraded.
  Actions: Play Battle Hymn+. Trigger its effect.
  Expected: Enemy takes 4 damage (2 base + 2 Wrath bonus).

- **Simmering Fury** [Y] — BGSimmeringFury — Power, Uncommon, Cost 1
  Your HIT deal +1 additional damage while in Wrath.
  *Upgrade: +2 additional damage while in Wrath.*

  - [ ] Sim - [ ] Live — **Test: No bonus in Neutral stance**
  Setup: Player in Neutral stance, 3 energy. Simmering Fury active. Enemy at 20 HP, 0 block.
  Actions: Play a 2 HIT Attack targeting the enemy.
  Expected: Enemy loses 2 HP. No extra damage from Simmering Fury since not in Wrath.

  - [ ] Sim - [ ] Live — **Test: Bonus damage per HIT in Wrath**
  Setup: Player in Wrath stance, 3 energy. Simmering Fury active. Enemy at 20 HP, 0 block.
  Actions: Play a 2 HIT Attack targeting the enemy.
  Expected: Enemy loses 6 HP (2 HIT, each hit = 1 base + 1 Simmering Fury, all doubled by Wrath = (1+1)*2 = 4 per hit... or 2 HIT * 2 Wrath = 4, then +1 per HIT in Wrath = 2 more = 6). Verify damage calculation order.

  - [ ] Sim - [ ] Live — **Test: Upgraded version adds +2 per HIT in Wrath**
  Setup: Player in Wrath stance, 3 energy. Simmering Fury+ active. Enemy at 20 HP, 0 block. Player has 0 Strength.
  Actions: Play a card with 3 HIT targeting the enemy.
  Expected: Each HIT deals 1 base +2 from Simmering Fury+ = 3 per hit, doubled by Wrath = 6 per hit. Total: 18 HP lost from enemy.

- **Mental Fortress** [Y] — BGMentalFortress — Power, Uncommon, Cost 1
  Whenever you switch Stances, 1 BLK.
  *Upgrade: 2 BLK.*

  - [ ] Sim - [ ] Live — **Test: Gain block on stance switch**
  Setup: Player in Neutral stance, 3 energy, 0 block. Mental Fortress active.
  Actions: Enter Wrath (via any card).
  Expected: Player gains 1 block from Mental Fortress upon switching from Neutral to Wrath.

  - [ ] Sim - [ ] Live — **Test: Multiple stance switches accumulate block**
  Setup: Player in Neutral stance, 3 energy, 0 block. Mental Fortress active.
  Actions: Enter Wrath. Then enter Calm.
  Expected: Player gains 1 block from Neutral->Wrath, and another 1 block from Wrath->Calm. Total: 2 block.

  - [ ] Sim - [ ] Live — **Test: Upgraded version grants 2 block per switch**
  Setup: Player in Neutral stance, 3 energy, 0 block. Mental Fortress+ active.
  Actions: Enter Wrath. Then enter Calm.
  Expected: Player gains 2 block per switch. Total: 4 block.

- **Nirvana** [Y] — BGNirvana — Power, Uncommon, Cost 1
  Whenever you Scry, 1 BLK.
  *Upgrade: 2 BLK.*

  - [ ] Sim - [ ] Live — **Test: Gain block when Scrying**
  Setup: Player in Neutral stance, 3 energy, 0 block. Nirvana active. Draw pile has 3+ cards.
  Actions: Play a card that Scrys (e.g., Scry 2).
  Expected: Player gains 1 block from Nirvana.

  - [ ] Sim - [ ] Live — **Test: Multiple Scrys in one turn each trigger block**
  Setup: Player in Neutral stance, 3 energy, 0 block. Nirvana active. Draw pile has 5+ cards.
  Actions: Play two cards that each Scry.
  Expected: Player gains 1 block from first Scry and 1 block from second Scry. Total: 2 block.

  - [ ] Sim - [ ] Live — **Test: Upgraded version grants 2 block per Scry**
  Setup: Player in Neutral stance, 3 energy, 0 block. Nirvana+ active. Draw pile has 3+ cards.
  Actions: Play a card that Scrys.
  Expected: Player gains 2 block from Nirvana+.

- **Like Water** [Y] — BGLikeWater — Power, Uncommon, Cost 1
  End of turn: If you're in Calm, 1 BLK.
  *Upgrade: 2 BLK.*

  - [ ] Sim - [ ] Live — **Test: Gain block at end of turn in Calm**
  Setup: Player in Calm stance, 3 energy, 0 block. Like Water active.
  Actions: End turn.
  Expected: Player gains 1 block at end of turn.

  - [ ] Sim - [ ] Live — **Test: No block if not in Calm**
  Setup: Player in Wrath stance, 3 energy, 0 block. Like Water active.
  Actions: End turn.
  Expected: Player gains 0 block from Like Water (not in Calm).

  - [ ] Sim - [ ] Live — **Test: Upgraded version grants 2 block**
  Setup: Player in Calm stance, 3 energy, 0 block. Like Water+ active.
  Actions: End turn.
  Expected: Player gains 2 block at end of turn.

- **Foresight** [Y] — BGForesight — Power, Uncommon, Cost 1
  Start of turn, before you draw: Scry 3.
  *Upgrade: Scry 4.*

  - [ ] Sim - [ ] Live — **Test: Scry at start of turn**
  Setup: Player in Neutral stance, 3 energy. Foresight active. Draw pile has 5+ cards.
  Actions: Start a new turn.
  Expected: Before drawing cards, player Scrys 3 (looks at top 3 cards, may discard any).

  - [ ] Sim - [ ] Live — **Test: Upgraded version Scrys 4**
  Setup: Player in Neutral stance, 3 energy. Foresight+ active. Draw pile has 5+ cards.
  Actions: Start a new turn.
  Expected: Before drawing cards, player Scrys 4 (looks at top 4 cards, may discard any).

  - [ ] Sim - [ ] Live — **Test: Foresight interacts with Nirvana for block**
  Setup: Player in Neutral stance, 0 block. Foresight and Nirvana both active. Draw pile has 5+ cards.
  Actions: Start a new turn.
  Expected: Foresight triggers Scry 3. Nirvana triggers, granting 1 block. Then normal card draw occurs.

- **Study** [Y] — BGStudy — Power, Uncommon, Cost 2
  Start of turn: If you're in Calm, draw 2 cards.
  *Upgrade: Cost 2 to 1.*

  - [ ] Sim - [ ] Live — **Test: Draw 2 in Calm at start of turn**
  Setup: Player in Calm stance, 3 energy. Study active. Draw pile has 10+ cards.
  Actions: Start a new turn.
  Expected: Player draws 2 extra cards from Study (total 7 cards drawn: 5 base + 2 from Study).

  - [ ] Sim - [ ] Live — **Test: No extra draw if not in Calm**
  Setup: Player in Neutral stance, 3 energy. Study active. Draw pile has 10+ cards.
  Actions: Start a new turn.
  Expected: Player draws only the normal 5 cards. Study does not trigger.

  - [ ] Sim - [ ] Live — **Test: Upgraded version costs 1 energy**
  Setup: Player in Neutral stance, 3 energy. Study+ in hand.
  Actions: Play Study+.
  Expected: Player spends 1 energy. Study power is now active.

- **Rushdown** [Y] — BGRushdown — Power, Uncommon, Cost 1
  The first time you enter Wrath each turn, draw 2 cards.
  *Upgrade: Draw 3 cards.*

  - [ ] Sim - [ ] Live — **Test: Draw on entering Wrath**
  Setup: Player in Neutral stance, 3 energy. Rushdown active. Draw pile has 5+ cards. Hand has 3 cards.
  Actions: Play a card that enters Wrath.
  Expected: Player enters Wrath. Rushdown triggers, drawing 2 cards.

  - [ ] Sim - [ ] Live — **Test: Only triggers once per turn**
  Setup: Player in Neutral stance, 3 energy. Rushdown active. Draw pile has 10+ cards.
  Actions: Enter Wrath. Then enter Calm. Then enter Wrath again.
  Expected: Rushdown draws 2 cards on the first Wrath entry. Second Wrath entry does not trigger Rushdown.

  - [ ] Sim - [ ] Live — **Test: Upgraded version draws 3 cards**
  Setup: Player in Neutral stance, 3 energy. Rushdown+ active. Draw pile has 5+ cards.
  Actions: Play a card that enters Wrath.
  Expected: Player enters Wrath. Rushdown+ triggers, drawing 3 cards.
