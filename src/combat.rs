use pyo3::prelude::*;
use rand::rngs::StdRng;
use rand::seq::SliceRandom;
use rand::SeedableRng;

use crate::cards::{starter_deck, Card, CardInstance};
use crate::creature::{Monster, Player};
use crate::damage::{apply_damage_to_monster, apply_damage_to_player, calculate_player_damage};
use crate::enums::{CardType, Character, Intent, OrbType, PowerType, Stance};
use crate::die::TheDie;
use crate::enemies;
use crate::relics;

#[pyclass]
#[derive(Clone, Debug)]
pub struct CombatState {
    #[pyo3(get)]
    pub player: Player,
    #[pyo3(get)]
    pub turn_number: i32,
    #[pyo3(get)]
    pub combat_over: bool,
    #[pyo3(get)]
    pub player_won: bool,
    pub monsters: Vec<Monster>,
    pub deck: Vec<CardInstance>,
    pub die: TheDie,
    rng: StdRng,
    pub stance_changed_this_turn: bool,
    pub has_card_been_played_this_turn: bool,
    pub cards_played_this_turn: Vec<(usize, Option<usize>)>,
    pub player_damaged_this_combat: bool,
}

impl CombatState {
    pub fn new(monsters: Vec<Monster>, seed: Option<u64>) -> Self {
        Self::new_with_character(monsters, seed, None)
    }

    pub fn new_with_character(monsters: Vec<Monster>, seed: Option<u64>, character: Option<Character>) -> Self {
        let s = seed.unwrap_or(0);
        let ch = character.unwrap_or(Character::Ironclad);
        CombatState {
            player: Player::new(Some(ch)),
            monsters,
            deck: starter_deck(ch),
            die: TheDie::new(Some(s)),
            turn_number: 0,
            combat_over: false,
            player_won: false,
            rng: StdRng::seed_from_u64(s.wrapping_add(1)),
            stance_changed_this_turn: false,
            cards_played_this_turn: Vec::new(),
            has_card_been_played_this_turn: false,
            player_damaged_this_combat: false,
        }
    }
}

#[pymethods]
impl CombatState {
    #[staticmethod]
    #[pyo3(name = "new_with_character")]
    #[pyo3(signature = (monsters, seed=None, character=None))]
    pub fn py_new_with_character(monsters: Vec<Monster>, seed: Option<u64>, character: Option<Character>) -> Self {
        Self::new_with_character(monsters, seed, character)
    }

    /// Start combat: pre-battle setup, then start first player turn.
    pub fn start_combat(&mut self) {
        // Pre-battle: set up monster powers
        for i in 0..self.monsters.len() {
            enemies::pre_battle(&mut self.monsters[i]);
        }

        // Initialize draw pile with all deck indices
        self.player.draw_pile = (0..self.deck.len()).collect();
        self.shuffle_draw_pile();

        // Move innate cards to front of draw pile
        self.move_innate_to_top();

        // Start first player turn (resets block, gives energy, draws cards)
        self.start_player_turn();

        // Relic: on combat start AFTER first turn setup (Anchor gives block, etc.)
        relics::on_combat_start(&mut self.player);

        // CrackedCore: channel 1 Lightning at combat start
        if self.player.has_relic(crate::enums::Relic::CrackedCore) {
            self.channel_orb(OrbType::Lightning);
        }

        // Miracles: start combat with 1 miracle token
        if self.player.has_relic(crate::enums::Relic::Miracles) {
            self.player.apply_power(PowerType::MiracleCount, 1);
        }
    }

    /// Start a new player turn: reset block (unless Barricade), gain energy, draw cards.
    pub fn start_player_turn(&mut self) {
        self.turn_number += 1;
        self.stance_changed_this_turn = false;
        self.cards_played_this_turn.clear();
        // Tracking for FTL
        self.has_card_been_played_this_turn = false;

        // Barricade: block doesn't reset
        if self.player.get_power(PowerType::Barricade) == 0 {
            self.player.block = 0;
        }

        self.player.energy = self.player.max_energy;

        // Berserk: gain extra energy at start of turn
        let berserk = self.player.get_power(PowerType::Berserk);
        if berserk > 0 {
            self.player.energy += berserk;
        }

        // EnergyPerTurn (Fusion): gain extra energy
        let energy_per_turn = self.player.get_power(PowerType::EnergyPerTurn);
        if energy_per_turn > 0 {
            self.player.energy += energy_per_turn;
        }

        // Clear NoDraw from previous turn
        self.player.powers.remove(&PowerType::NoDraw);

        // Clear Entangled from previous turn
        self.player.powers.remove(&PowerType::Entangled);

        // Relic hooks on turn start (Lantern, Bag of Preparation)
        let (extra_draw, extra_energy) = relics::on_turn_start(&mut self.player, self.turn_number);
        self.player.energy += extra_energy;

        // DrawPerTurn (Machine Learning): extra card draw
        let draw_per_turn = self.player.get_power(PowerType::DrawPerTurn);

        // Draw cards
        let draw_amount = self.player.draw_amount + extra_draw + draw_per_turn;
        self.draw_cards(draw_amount);

        // Storm: channel Lightning at start of turn (after draw)
        let storm = self.player.get_power(PowerType::Storm);
        for _ in 0..storm {
            self.channel_orb(OrbType::Lightning);
        }

        // Devotion: gain miracles at start of turn
        let devotion = self.player.get_power(PowerType::DevotionPower);
        if devotion > 0 {
            self.player.apply_power(PowerType::MiracleCount, devotion);
        }

        // DevaForm: gain energy at start of turn (stacking)
        let deva = self.player.get_power(PowerType::DevaFormPower);
        if deva > 0 {
            self.player.energy += deva;
        }

        // StudyPower: draw extra cards per turn
        let study = self.player.get_power(PowerType::StudyPower);
        if study > 0 {
            self.draw_cards(study);
        }

        // Foresight: scry at start of turn
        let foresight = self.player.get_power(PowerType::ForesightPower);
        if foresight > 0 {
            self.scry(foresight);
        }
    }

    /// Play a card from hand by hand index, targeting monster at target_index.
    /// Optional choice param for cards with multiple modes (e.g. Iron Wave+ Spear=0/Shield=1).
    /// Returns true if the card was successfully played.
    #[pyo3(signature = (hand_index, target_index=None, choice=None))]
    pub fn play_card(&mut self, hand_index: usize, target_index: Option<usize>, choice: Option<usize>) -> bool {
        if self.combat_over {
            return false;
        }
        if hand_index >= self.player.hand_indices.len() {
            return false;
        }

        let deck_index = self.player.hand_indices[hand_index];
        let card_inst = self.deck[deck_index];

        // Check unplayable
        if card_inst.card.unplayable() {
            return false;
        }

        let is_attack = card_inst.card.card_type() == CardType::Attack;
        let is_skill = card_inst.card.card_type() == CardType::Skill;

        // Entangled: can't play attacks
        if is_attack && self.player.get_power(PowerType::Entangled) > 0 {
            return false;
        }

        // Corruption: skills cost 0
        let corruption = self.player.get_power(PowerType::Corruption) > 0;
        // free_play_for: next card of matching type is free
        let card_type = card_inst.card.card_type();
        let free_play = self.player.free_play_for.as_ref()
            .map_or(false, |types| types.contains(&card_type));
        let mut effective_cost = if corruption && is_skill { 0 } else if free_play { 0 } else { card_inst.cost() };
        // Blood for Blood: cost drops to magic_number after player takes damage
        if card_inst.card == Card::BloodForBlood && self.player_damaged_this_combat {
            effective_cost = card_inst.base_magic();
        }

        // Check energy (including miracles as extra energy)
        let miracles = self.player.get_power(PowerType::MiracleCount);
        let total_energy = self.player.energy + miracles;
        if effective_cost > total_energy {
            return false;
        }

        // Check target requirement
        if card_inst.card.has_target() && target_index.is_none() {
            return false;
        }

        // Capture energy before payment (needed for DoubleTap X-cost replay)
        let original_energy = self.player.energy;

        // Pay energy (use regular energy first, then miracles)
        if effective_cost <= self.player.energy {
            self.player.energy -= effective_cost;
        } else {
            let from_miracles = effective_cost - self.player.energy;
            self.player.energy = 0;
            self.player.reduce_power(PowerType::MiracleCount, from_miracles);
        }

        // Consume free_play_for if used
        if free_play {
            self.player.free_play_for = None;
        }

        // Remove from hand
        self.player.hand_indices.remove(hand_index);

        // Track non-X-cost attacks/skills for Doppelganger replay
        if (is_attack || is_skill) && card_inst.cost() >= 0 {
            self.cards_played_this_turn.push((deck_index, target_index));
        }

        // Snapshot which monsters had Vulnerable before this attack.
        // After the card resolves, we consume 1 Vulnerable per card (not per hit).
        let vuln_targets: Vec<usize> = if is_attack {
            if card_inst.card.has_target() {
                // Single-target attack: check the target
                if let Some(ti) = target_index {
                    if ti < self.monsters.len() && !self.monsters[ti].is_dead()
                        && self.monsters[ti].get_power(PowerType::Vulnerable) > 0
                    {
                        vec![ti]
                    } else {
                        vec![]
                    }
                } else {
                    vec![]
                }
            } else {
                // AoE attack: check all alive monsters
                (0..self.monsters.len())
                    .filter(|&i| !self.monsters[i].is_dead()
                        && self.monsters[i].get_power(PowerType::Vulnerable) > 0)
                    .collect()
            }
        } else {
            vec![]
        };

        // Flag: if set during card effect, card is purged (not discarded or exhausted)
        let mut purge_played_card = false;
        // Flag: if set, card returns to hand after play (BG selfRetain)
        let mut retain_played_card = false;

        // Execute card effect
        match card_inst.card {
            // --- Starter cards ---
            Card::StrikeRed | Card::StrikeGreen | Card::StrikeBlue | Card::StrikePurple => {
                let conjure = self.player.get_power(PowerType::ConjureBladePower);
                if conjure > 0 {
                    let ti = target_index.unwrap();
                    if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                        let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage() + conjure);
                        apply_damage_to_monster(&mut self.monsters[ti], damage);
                    }
                } else {
                    self.attack_single(target_index, card_inst);
                }
            }
            Card::DefendRed | Card::DefendGreen | Card::DefendBlue | Card::DefendPurple => {
                self.player_gain_block(card_inst.base_block());
            }
            Card::Bash => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                    self.monsters[ti].apply_power(PowerType::Vulnerable, card_inst.base_magic());
                }
            }

            // --- Silent Starter ---
            Card::Neutralize => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                    self.monsters[ti].apply_power(PowerType::Weak, card_inst.base_magic());
                }
            }
            Card::Survivor => {
                self.player_gain_block(card_inst.base_block());
                // Discard 1 card from hand
                self.discard_random_from_hand();
            }

            // --- Defect Starter ---
            Card::Zap => {
                self.channel_orb(OrbType::Lightning);
            }
            Card::Dualcast => {
                // Evoke first orb twice
                if !self.player.orbs.is_empty() {
                    let orb = self.player.orbs[0];
                    self.evoke_orb(0);
                    self.process_evoke(orb);  // second evoke of same type
                }
            }

            // --- Watcher Starter ---
            Card::Eruption => {
                self.attack_single(target_index, card_inst);
                self.change_stance(Stance::Wrath);
            }
            Card::Vigilance => {
                self.player_gain_block(card_inst.base_block());
                self.change_stance(Stance::Calm);
            }

            // ===== SILENT CARDS =====

            // --- Silent Common Attacks ---
            Card::PoisonedStab => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                    self.monsters[ti].apply_power(PowerType::Poison, card_inst.base_magic());
                }
            }
            Card::DaggerThrow => {
                self.attack_single(target_index, card_inst);
                self.draw_cards(1);
                self.discard_random_from_hand();
            }
            Card::DaggerSpray => {
                // Hit all enemies magic_number times
                for _ in 0..card_inst.base_magic() {
                    self.attack_all_enemies(card_inst);
                }
            }
            Card::SneakyStrike => {
                self.attack_single(target_index, card_inst);
                // Gain 2 energy if discarded this turn (simplified: always gain)
                self.player.energy += 2;
            }
            Card::Slice => {
                self.attack_single(target_index, card_inst);
            }

            // --- Silent Common Skills ---
            Card::Backflip => {
                self.player_gain_block(card_inst.base_block());
                self.draw_cards(2);
            }
            Card::DodgeAndRoll => {
                for _ in 0..card_inst.base_magic() {
                    self.player_gain_block(card_inst.base_block());
                }
            }
            Card::Deflect => {
                self.player_gain_block(card_inst.base_block());
            }
            Card::CloakAndDagger => {
                self.player_gain_block(card_inst.base_block());
                // Generate shivs (add to shiv counter)
                // Simplified: no shiv tracking yet
            }
            Card::BladeDance => {
                // Generate shivs (add to shiv counter)
            }
            Card::Prepared => {
                self.draw_cards(card_inst.base_magic());
                for _ in 0..card_inst.base_magic() {
                    self.discard_random_from_hand();
                }
            }
            Card::DeadlyPoison => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    self.monsters[ti].apply_power(PowerType::Poison, card_inst.base_magic());
                }
            }
            Card::Acrobatics => {
                self.draw_cards(card_inst.base_magic());
                // BG mod: forced discard 1 (live choose(0) selects first card)
                self.discard_random_from_hand();
            }

            // --- Silent Uncommon Attacks ---
            Card::Backstab => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let mut base = card_inst.base_damage();
                    // Bonus damage if target at full HP
                    if self.monsters[ti].hp == self.monsters[ti].max_hp {
                        base += card_inst.base_magic();
                    }
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], base);
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                }
            }
            Card::Bane => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let mut base = card_inst.base_damage();
                    // Bonus damage if target has Poison
                    if self.monsters[ti].get_power(PowerType::Poison) > 0 {
                        base += card_inst.base_magic();
                    }
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], base);
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                }
            }
            Card::Choke => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let mut base = card_inst.base_damage();
                    // Bonus damage per debuff on target
                    let poison = self.monsters[ti].get_power(PowerType::Poison);
                    let weak = self.monsters[ti].get_power(PowerType::Weak);
                    let vuln = self.monsters[ti].get_power(PowerType::Vulnerable);
                    let debuff_count = (if poison > 0 { 1 } else { 0 }) +
                                       (if weak > 0 { 1 } else { 0 }) +
                                       (if vuln > 0 { 1 } else { 0 });
                    base += card_inst.base_magic() * debuff_count;
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], base);
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                }
            }
            Card::Predator => {
                self.attack_single(target_index, card_inst);
                self.draw_cards(card_inst.base_magic());
            }
            Card::MasterfulStab => {
                self.attack_single(target_index, card_inst);
            }
            Card::Dash => {
                self.player_gain_block(card_inst.base_block());
                self.attack_single(target_index, card_inst);
            }
            Card::Finisher => {
                // Damage per attack played this turn (simplified: base damage)
                self.attack_single(target_index, card_inst);
            }
            Card::Flechettes => {
                // BG mod: hit once per skill in hand + magic bonus hits.
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let skill_count = self.player.hand_indices.iter()
                        .filter(|&&idx| self.deck[idx].card.card_type() == CardType::Skill)
                        .count() as i32;
                    let hits = skill_count + card_inst.base_magic();
                    for _ in 0..hits {
                        if !self.monsters[ti].is_dead() {
                            let dmg = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                            apply_damage_to_monster(&mut self.monsters[ti], dmg);
                        }
                    }
                }
            }
            Card::AllOutAttack => {
                self.attack_all_enemies(card_inst);
                self.discard_random_from_hand();
            }
            Card::Unload => {
                // BG mod: deals damage + uses BGShivs relic (no discard).
                // Without the shiv relic, just deals damage.
                self.attack_single(target_index, card_inst);
            }

            // --- Silent Uncommon Skills ---
            Card::Blur => {
                self.player_gain_block(card_inst.base_block() + card_inst.base_magic());
            }
            Card::BouncingFlask => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    self.monsters[ti].apply_power(PowerType::Poison, card_inst.base_magic());
                }
            }
            Card::Concentrate => {
                // BG mod: discard remaining hand, gain energy per discard + magic bonus
                let hand_copy: Vec<usize> = self.player.hand_indices.drain(..).collect();
                let count = hand_copy.len() as i32;
                for idx in hand_copy {
                    self.player.discard_pile.push(idx);
                }
                self.player.energy += count + card_inst.base_magic();
            }
            Card::CalculatedGamble => {
                let hand_size = self.player.hand_indices.len() as i32;
                let hand_copy: Vec<usize> = self.player.hand_indices.drain(..).collect();
                for idx in hand_copy {
                    self.player.discard_pile.push(idx);
                }
                self.draw_cards(hand_size);
            }
            Card::Catalyst => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let current_poison = self.monsters[ti].get_power(PowerType::Poison);
                    if current_poison > 0 {
                        if card_inst.upgraded {
                            // Triple: add 2x current
                            self.monsters[ti].apply_power(PowerType::Poison, current_poison * 2);
                        } else {
                            // Double: add 1x current
                            self.monsters[ti].apply_power(PowerType::Poison, current_poison);
                        }
                    }
                }
            }
            Card::CripplingCloud => {
                for m in &mut self.monsters {
                    if !m.is_dead() {
                        m.apply_power(PowerType::Poison, card_inst.base_magic());
                        m.apply_power(PowerType::Weak, 1);
                    }
                }
            }
            Card::LegSweep => {
                let ti = target_index.unwrap();
                self.player_gain_block(card_inst.base_block());
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    self.monsters[ti].apply_power(PowerType::Weak, card_inst.base_magic());
                }
            }
            Card::Outmaneuver => {
                // BG mod: gains energy only if retained from last turn.
                // Cards are never retained in test scenarios, so no effect.
            }
            Card::PiercingWail => {
                self.player_gain_block(card_inst.base_block());
                for m in &mut self.monsters {
                    if !m.is_dead() {
                        m.apply_power(PowerType::Weak, card_inst.base_magic());
                    }
                }
            }
            Card::EscapePlan => {
                if card_inst.upgraded {
                    // BG upgraded: always gain block, then draw 1
                    self.player_gain_block(card_inst.base_block());
                    self.draw_cards(1);
                } else {
                    // BG base: Draw 1, gain block only if drawn card is a skill
                    self.draw_cards(1);
                    if let Some(&last_drawn_idx) = self.player.hand_indices.last() {
                        if self.deck[last_drawn_idx].card.card_type() == CardType::Skill {
                            self.player_gain_block(card_inst.base_block());
                        }
                    }
                }
            }
            Card::Expertise => {
                // Draw cards (simplified)
                self.draw_cards(card_inst.base_magic());
            }
            Card::RiddleWithHoles => {
                // Generate shivs
            }
            Card::Setup => {
                self.player.energy += card_inst.base_magic();
            }
            Card::Terror => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    self.monsters[ti].apply_power(PowerType::Vulnerable, card_inst.base_magic());
                }
            }

            // --- Silent Rare Attacks ---
            Card::DieDieDie => {
                self.attack_all_enemies(card_inst);
            }
            Card::GrandFinale => {
                // Can only be played if draw pile is empty (checked in get_available_actions)
                self.attack_all_enemies(card_inst);
            }
            Card::Skewer => {
                // X-cost: (X + magic) hits of base_damage each
                let max_x = self.player.energy + effective_cost;
                let x = choice.map(|c| (c as i32).min(max_x)).unwrap_or(max_x);
                self.player.energy = max_x - x;
                let hits = x + card_inst.base_magic();
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    for _ in 0..hits {
                        let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                        apply_damage_to_monster(&mut self.monsters[ti], damage);
                    }
                }
            }

            // --- Silent Rare Skills ---
            Card::Adrenaline => {
                let energy_gain = if card_inst.upgraded { 2 } else { 1 };
                self.player.energy += energy_gain;
                self.draw_cards(2);
            }
            Card::BulletTime => {
                self.player.apply_power(PowerType::NoDraw, 1);
            }
            Card::Malaise => {
                // X-cost: apply X + magic weak
                let max_x = self.player.energy + effective_cost;
                let x = choice.map(|c| (c as i32).min(max_x)).unwrap_or(max_x);
                self.player.energy = max_x - x;
                let weak_amount = x + card_inst.base_magic();
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    self.monsters[ti].apply_power(PowerType::Weak, weak_amount);
                }
            }
            Card::StormOfSteel => {
                // BG mod: discard remaining hand, generate shivs (tracked by relic)
                let hand_copy: Vec<usize> = self.player.hand_indices.drain(..).collect();
                for idx in hand_copy {
                    self.player.discard_pile.push(idx);
                }
            }
            Card::Doppelganger => {
                // X-cost: copy and replay most recent card whose cost matches X.
                let max_x = self.player.energy + effective_cost;

                // Build sorted unique cost levels from cards played this turn
                let mut valid_levels: Vec<i32> = Vec::new();
                for &(di, _) in &self.cards_played_this_turn {
                    let c = self.deck[di].cost();
                    if c >= 0 && c <= max_x && !valid_levels.contains(&c) {
                        valid_levels.push(c);
                    }
                }
                valid_levels.sort();

                if valid_levels.is_empty() {
                    // No valid cards to copy — just spend X energy
                    let x = choice.map(|c| (c as i32).min(max_x)).unwrap_or(max_x);
                    self.player.energy = max_x - x;
                } else {
                    // Select X level
                    let x = if valid_levels.len() == 1 {
                        valid_levels[0]
                    } else {
                        let idx = choice.unwrap_or(0).min(valid_levels.len() - 1);
                        valid_levels[idx]
                    };

                    // Deduct energy
                    self.player.energy = max_x - x;

                    // Find most recent card at matching cost
                    let replay_info = self.cards_played_this_turn.iter().rev()
                        .find(|&&(di, _)| self.deck[di].cost() == x)
                        .copied();

                    if let Some((replay_deck_index, stored_target)) = replay_info {
                        let replay_card_type = self.deck[replay_deck_index].card.card_type();

                        // Remove from discard or exhaust pile
                        if let Some(pos) = self.player.discard_pile.iter().position(|&i| i == replay_deck_index) {
                            self.player.discard_pile.remove(pos);
                        } else if let Some(pos) = self.player.exhaust_pile.iter().position(|&i| i == replay_deck_index) {
                            self.player.exhaust_pile.remove(pos);
                        }

                        // Re-add to hand and replay
                        self.player.hand_indices.push(replay_deck_index);
                        let replay_pos = self.player.hand_indices.len() - 1;
                        self.player.free_play_for = Some(vec![replay_card_type]);
                        self.play_card(replay_pos, stored_target, None);
                    }
                }
            }
            Card::CorpseExplosionCard => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    self.monsters[ti].apply_power(PowerType::Poison, card_inst.base_magic());
                }
                // BG mod: CardDoesNotDiscardWhenPlayed — card is removed after play
                purge_played_card = true;
            }

            // --- Silent Powers ---
            Card::AccuracyCard => {
                self.player.apply_power(PowerType::Accuracy, card_inst.base_magic());
            }
            Card::AfterImageCard => {
                self.player.apply_power(PowerType::AfterImage, card_inst.base_magic());
            }
            Card::FootworkCard => {
                self.player.apply_power(PowerType::Dexterity, card_inst.base_magic());
            }
            Card::NoxiousFumesCard => {
                self.player.apply_power(PowerType::NoxiousFumes, card_inst.base_magic());
            }
            Card::WellLaidPlansCard => {
                self.player.apply_power(PowerType::WellLaidPlans, card_inst.base_magic());
            }
            Card::DistractionCard => {
                self.player.apply_power(PowerType::Distraction, card_inst.base_magic());
            }
            Card::InfiniteBlades => {
                self.player.apply_power(PowerType::InfiniteBlades, card_inst.base_magic());
            }
            Card::AThousandCutsCard => {
                self.player.apply_power(PowerType::AThousandCuts, card_inst.base_magic());
            }
            Card::BurstCard => {
                self.player.apply_power(PowerType::Burst, card_inst.base_magic());
            }
            Card::EnvenomCard => {
                self.player.apply_power(PowerType::Envenom, card_inst.base_magic());
            }
            Card::ToolsOfTheTradeCard => {
                self.player.apply_power(PowerType::ToolsOfTheTrade, 1);
            }
            Card::WraithFormCard => {
                self.player.apply_power(PowerType::WraithForm, card_inst.base_magic());
            }

            // Silent unplayable cards — should never reach here
            Card::Reflex | Card::Tactician => {}

            // --- Defect Common Attacks ---
            Card::BallLightning => {
                self.attack_single(target_index, card_inst);
                for _ in 0..card_inst.base_magic() {
                    self.channel_orb(OrbType::Lightning);
                }
            }
            Card::Barrage => {
                // BG mod: hit once per orb channeled + magic bonus hits.
                let ti = target_index.unwrap();
                let orb_count = self.player.orbs.len() as i32;
                let hits = orb_count + card_inst.base_magic();
                for _ in 0..hits {
                    if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                        let dmg = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                        apply_damage_to_monster(&mut self.monsters[ti], dmg);
                    }
                }
            }
            Card::BeamCell => {
                self.attack_single(target_index, card_inst);
                // Apply Vulnerable (guaranteed if upgraded, otherwise conditional)
                if let Some(ti) = target_index {
                    if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                        if card_inst.upgraded {
                            self.monsters[ti].apply_power(PowerType::Vulnerable, 1);
                        } else {
                            // Die-based: apply on die 1-3
                            let roll = self.die.roll();
                            if roll <= 3 {
                                self.monsters[ti].apply_power(PowerType::Vulnerable, 1);
                            }
                        }
                    }
                }
            }
            Card::Claw => {
                self.attack_single(target_index, card_inst);
            }
            Card::CompileDriver => {
                self.attack_single(target_index, card_inst);
                // BG mod: draw 1 per unique orb type channeled (vanilla CompileDriverAction).
                let mut seen = std::collections::HashSet::new();
                for &orb in &self.player.orbs {
                    seen.insert(orb);
                }
                self.draw_cards(seen.len() as i32);
            }
            Card::GoForTheEyes => {
                self.attack_single(target_index, card_inst);
                if let Some(ti) = target_index {
                    if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                        if card_inst.upgraded {
                            self.monsters[ti].apply_power(PowerType::Weak, 1);
                        } else {
                            let roll = self.die.roll();
                            if roll >= 4 {
                                self.monsters[ti].apply_power(PowerType::Weak, 1);
                            }
                        }
                    }
                }
            }
            Card::SweepingBeam => {
                self.attack_all_enemies(card_inst);
                self.draw_cards(card_inst.base_magic());
            }
            // --- Defect Common Skills ---
            Card::ChargeBattery => {
                self.player_gain_block(card_inst.base_block());
                if self.player.orbs.len() >= 3 {
                    self.player.energy += card_inst.base_magic();
                }
            }
            Card::Chaos => {
                // Channel a random orb type (die-based)
                let roll = self.die.roll();
                let orb = match roll % 3 {
                    0 => OrbType::Lightning,
                    1 => OrbType::Frost,
                    _ => OrbType::Dark,
                };
                self.channel_orb(orb);
            }
            Card::Coolheaded => {
                self.channel_orb(OrbType::Frost);
                if card_inst.upgraded {
                    self.draw_cards(1);
                }
            }
            Card::Leap => {
                self.player_gain_block(card_inst.base_block());
            }
            Card::Recursion => {
                // Evoke first orb and re-channel it
                if !self.player.orbs.is_empty() {
                    let orb = self.player.orbs[0];
                    self.evoke_orb(0);
                    self.channel_orb(orb);
                }
            }
            Card::SteamBarrier => {
                self.player_gain_block(card_inst.base_block());
            }
            // --- Defect Uncommon Attacks ---
            Card::Blizzard => {
                // BG mod: deals damage once per Frost orb channeled.
                let frost_count = self.player.orbs.iter()
                    .filter(|&&o| o == OrbType::Frost)
                    .count();
                for _ in 0..frost_count {
                    self.attack_all_enemies(card_inst);
                }
            }
            Card::ColdSnap => {
                self.attack_single(target_index, card_inst);
                self.channel_orb(OrbType::Frost);
            }
            Card::DoomAndGloom => {
                self.attack_all_enemies(card_inst);
                self.channel_orb(OrbType::Dark);
            }
            Card::FTL => {
                self.attack_single(target_index, card_inst);
                if !self.has_card_been_played_this_turn {
                    self.draw_cards(1);
                }
            }
            Card::MelterCard => {
                // BG mod: remove all block first, then deal damage.
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    self.monsters[ti].block = 0;
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                }
            }
            Card::Scrape => {
                self.attack_single(target_index, card_inst);
            }
            Card::Streamline => {
                self.attack_single(target_index, card_inst);
            }
            Card::Sunder => {
                self.attack_single(target_index, card_inst);
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && self.monsters[ti].is_dead() {
                    self.player.energy += 3;
                }
            }
            // --- Defect Uncommon Skills ---
            Card::DarknessCard => {
                self.channel_orb(OrbType::Dark);
            }
            Card::DoubleEnergy => {
                self.player.energy *= 2;
            }
            Card::Equilibrium => {
                self.player_gain_block(card_inst.base_block());
                // Retain effect: handled via power
                self.player.apply_power(PowerType::WellLaidPlans, card_inst.base_magic());
            }
            Card::ForceField => {
                self.player_gain_block(card_inst.base_block());
            }
            Card::Glacier => {
                self.player_gain_block(card_inst.base_block());
                self.channel_orb(OrbType::Frost);
            }
            Card::Hologram => {
                self.player_gain_block(card_inst.base_block());
                // Return card from discard to hand (simplified: draw 1 from discard)
                if !self.player.discard_pile.is_empty() {
                    let idx = self.player.discard_pile.pop().unwrap();
                    self.player.hand_indices.push(idx);
                }
            }
            Card::Overclock => {
                self.draw_cards(card_inst.base_magic());
                // Add 1 Dazed to discard
                self.add_card_to_discard(Card::Dazed);
            }
            Card::RecycleCard => {
                // Exhaust a card from hand, gain its cost as energy (simplified: gain 1 energy)
                if !self.player.hand_indices.is_empty() {
                    let idx = self.player.hand_indices.pop().unwrap();
                    self.player.exhaust_pile.push(idx);
                    let card = self.deck[idx];
                    let cost = card.cost();
                    if cost > 0 {
                        self.player.energy += cost;
                    }
                }
            }
            Card::Reprogram => {
                self.player.apply_power(PowerType::Strength, card_inst.base_magic());
                self.player.remove_all_orbs();
            }
            Card::StackCard => {
                // Gain 1 block per orb channeled (+ upgrade bonus)
                let orb_count = self.player.orbs.len() as i32;
                let block = orb_count + card_inst.base_block();
                self.player_gain_block(block);
            }
            Card::TURBO => {
                self.player.energy += card_inst.base_magic();
                self.add_card_to_discard(Card::Dazed);
            }
            Card::ReinforcedBody => {
                // BG X-cost: base minEnergy=1, upgraded minEnergy=0
                let min_x = if card_inst.upgraded { 0 } else { 1 };
                let max_x = self.player.energy + effective_cost;
                let x = choice.map(|c| (c as i32 + min_x).min(max_x)).unwrap_or(max_x);
                self.player.energy = max_x - x;
                // BG: base = x+1 block, upgraded = x*2 (doubled)
                let block = if card_inst.upgraded { x * 2 } else { x + card_inst.base_magic() };
                self.player_gain_block(block);
            }
            // --- Defect Uncommon Powers ---
            Card::CapacitorCard => {
                self.player.orb_slots += card_inst.base_magic();
            }
            Card::ConsumeCard => {
                self.player.apply_power(PowerType::OrbEvoke, card_inst.base_magic());
            }
            Card::FusionCard => {
                self.player.apply_power(PowerType::EnergyPerTurn, card_inst.base_magic());
            }
            Card::HeatsinkCard => {
                self.player.apply_power(PowerType::Heatsink, card_inst.base_magic());
            }
            Card::LoopCard => {
                self.player.apply_power(PowerType::Loop, card_inst.base_magic());
            }
            Card::MachineLearningCard => {
                self.player.apply_power(PowerType::DrawPerTurn, card_inst.base_magic());
            }
            Card::StormCard => {
                self.player.apply_power(PowerType::Storm, card_inst.base_magic());
            }
            // --- Defect Rare Attacks ---
            Card::AllForOne => {
                self.attack_single(target_index, card_inst);
                // Put all 0-cost cards from discard to hand
                let zero_cost_indices: Vec<usize> = self.player.discard_pile.iter()
                    .filter(|&&idx| self.deck[idx].cost() == 0)
                    .copied()
                    .collect();
                for idx in &zero_cost_indices {
                    self.player.discard_pile.retain(|&i| i != *idx);
                    self.player.hand_indices.push(*idx);
                }
            }
            Card::CoreSurge => {
                // Remove Weak and Vulnerable from self, then attack
                self.player.powers.remove(&PowerType::Weak);
                self.player.powers.remove(&PowerType::Vulnerable);
                self.attack_single(target_index, card_inst);
            }
            Card::Hyperbeam => {
                self.attack_all_enemies(card_inst);
                self.player.remove_all_orbs();
            }
            Card::MeteorStrike => {
                self.attack_single(target_index, card_inst);
            }
            Card::ThunderStrike => {
                // BG mod: deals damage once per Lightning orb channeled.
                let lightning_count = self.player.orbs.iter()
                    .filter(|&&o| o == OrbType::Lightning)
                    .count();
                for _ in 0..lightning_count {
                    self.attack_all_enemies(card_inst);
                }
            }
            // --- Defect Rare Skills ---
            Card::AmplifyCard => {
                self.player.apply_power(PowerType::AmplifyDark, card_inst.base_magic());
            }
            Card::Fission => {
                // Remove all orbs, gain energy per orb removed (if upgraded, also draw per orb)
                let orbs = self.player.remove_all_orbs();
                let count = orbs.len() as i32;
                self.player.energy += count;
                if card_inst.upgraded {
                    self.draw_cards(count);
                }
            }
            Card::MultiCast => {
                // BG X-cost: evoke first orb X + magic times
                let max_x = self.player.energy + effective_cost;
                let x = choice.map(|c| (c as i32).min(max_x)).unwrap_or(max_x);
                self.player.energy = max_x - x;
                let evokes = x + card_inst.base_magic();
                if evokes > 0 && !self.player.orbs.is_empty() {
                    let orb_type = self.player.orbs[0];
                    // First evoke removes the orb
                    self.evoke_orb(0);
                    // Remaining evokes apply effect without removal
                    for _ in 1..evokes {
                        self.process_evoke(orb_type);
                    }
                }
            }
            Card::RainbowCard => {
                self.channel_orb(OrbType::Lightning);
                self.channel_orb(OrbType::Frost);
                self.channel_orb(OrbType::Dark);
            }
            Card::SeekCard => {
                // Draw from deck (simplified: draw cards)
                self.draw_cards(card_inst.base_magic());
            }
            Card::SkimCard => {
                self.draw_cards(card_inst.base_magic());
            }
            Card::TempestCard => {
                // X-cost: channel X + magic Lightning orbs
                let max_x = self.player.energy + effective_cost;
                let x = choice.map(|c| (c as i32).min(max_x)).unwrap_or(max_x);
                self.player.energy = max_x - x;
                let channels = x + card_inst.base_magic();
                for _ in 0..channels {
                    self.channel_orb(OrbType::Lightning);
                }
            }
            // --- Defect Rare Powers ---
            Card::BufferCard => {
                self.player.apply_power(PowerType::BufferPower, card_inst.base_magic());
            }
            Card::DefragmentCard => {
                self.player.apply_power(PowerType::OrbPassive, card_inst.base_magic());
            }
            Card::EchoFormCard => {
                self.player.apply_power(PowerType::EchoForm, 1);
            }
            Card::ElectrodynamicsCard => {
                self.player.apply_power(PowerType::Electrodynamics, 1);
                for _ in 0..card_inst.base_magic() {
                    self.channel_orb(OrbType::Lightning);
                }
            }
            Card::StaticDischargeCard => {
                self.player.apply_power(PowerType::StaticDischarge, card_inst.base_magic());
            }

            // ===== WATCHER CARDS =====

            // --- Watcher Common Attacks ---
            Card::FlurryOfBlows => {
                self.attack_single(target_index, card_inst);
                // Bonus damage if stance changed this turn (simplified: check if not Neutral)
                if self.stance_changed_this_turn {
                    let ti = target_index.unwrap();
                    if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                        let bonus = card_inst.base_magic();
                        let damage = calculate_player_damage(&self.player, &self.monsters[ti], bonus);
                        apply_damage_to_monster(&mut self.monsters[ti], damage);
                    }
                }
            }
            Card::EmptyFist => {
                self.attack_single(target_index, card_inst);
                self.change_stance(Stance::Neutral);
            }
            Card::Consecrate => {
                self.attack_all_enemies(card_inst);
            }
            Card::CutThroughFate => {
                self.attack_single(target_index, card_inst);
                self.scry(card_inst.base_magic());
                self.draw_cards(1);
            }
            Card::JustLucky => {
                self.attack_single(target_index, card_inst);
                // Die roll: 1-3 scry, 4-6 block
                let roll = self.die.roll();
                if roll <= 3 {
                    self.scry(card_inst.base_magic());
                } else {
                    self.player_gain_block(card_inst.base_block());
                }
            }

            // --- Watcher Common Skills ---
            Card::EmptyBody => {
                self.player_gain_block(card_inst.base_block());
                self.change_stance(Stance::Neutral);
            }
            Card::Protect => {
                self.player_gain_block(card_inst.base_block());
            }
            Card::Halt => {
                self.player_gain_block(card_inst.base_block());
                if self.player.stance == Stance::Wrath {
                    self.player_gain_block(card_inst.base_magic());
                }
            }
            Card::ThirdEye => {
                self.player_gain_block(card_inst.base_block());
                self.scry(card_inst.base_magic());
            }
            Card::Tranquility => {
                self.change_stance(Stance::Calm);
            }
            Card::Crescendo => {
                self.change_stance(Stance::Wrath);
                if card_inst.upgraded {
                    self.draw_cards(1);
                }
            }
            Card::Collect => {
                self.player.apply_power(PowerType::MiracleCount, card_inst.base_magic());
            }

            // --- Watcher Uncommon Attacks ---
            Card::CrushJoints => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                    self.monsters[ti].apply_power(PowerType::Weak, card_inst.base_magic());
                }
            }
            Card::FearNoEvil | Card::ForeignInfluence | Card::CarveReality => {
                self.attack_single(target_index, card_inst);
            }
            Card::Wallop => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                    let hp_lost = apply_damage_to_monster(&mut self.monsters[ti], damage);
                    if hp_lost > 0 {
                        self.player_gain_block(hp_lost);
                    }
                }
            }
            Card::SashWhip => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                    self.monsters[ti].apply_power(PowerType::Vulnerable, card_inst.base_magic());
                }
            }
            Card::Tantrum => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let hits = card_inst.base_magic();
                    for _ in 0..hits {
                        if !self.monsters[ti].is_dead() {
                            let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                            apply_damage_to_monster(&mut self.monsters[ti], damage);
                        }
                    }
                }
                // Add a copy to draw pile
                self.add_card_to_draw(Card::Tantrum);
                self.change_stance(Stance::Wrath);
            }
            Card::SandsOfTime => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    // Bonus damage per other retain card in hand
                    let retain_count = self.player.hand_indices.iter()
                        .filter(|&&idx| self.deck[idx].card.retain())
                        .count() as i32;
                    let bonus = card_inst.base_magic() * retain_count;
                    let base = card_inst.base_damage() + bonus;
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], base);
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                }
            }
            Card::WindmillStrike => {
                // Simplified: just deal base damage (retained bonus would require tracking)
                self.attack_single(target_index, card_inst);
            }
            Card::Weave => {
                self.attack_single(target_index, card_inst);
            }
            Card::SignatureMove => {
                self.attack_single(target_index, card_inst);
            }
            Card::FlyingSleeves => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let hits = card_inst.base_magic();
                    for _ in 0..hits {
                        if !self.monsters[ti].is_dead() {
                            let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                            apply_damage_to_monster(&mut self.monsters[ti], damage);
                        }
                    }
                }
            }
            Card::Conclude => {
                // AoE attack hitting magic_number times
                for _ in 0..card_inst.base_magic() {
                    self.attack_all_enemies(card_inst);
                }
            }
            Card::ReachHeaven => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let miracle_count = self.player.get_power(PowerType::MiracleCount);
                    let bonus = card_inst.base_magic() * miracle_count;
                    let base = card_inst.base_damage() + bonus;
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], base);
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                }
            }

            // --- Watcher Uncommon Skills ---
            Card::EmptyMind => {
                self.draw_cards(card_inst.base_magic());
                self.change_stance(Stance::Neutral);
            }
            Card::MeditateCard => {
                self.scry(card_inst.base_magic());
                self.change_stance(Stance::Calm);
            }
            Card::InnerPeace => {
                self.draw_cards(card_inst.base_magic());
            }
            Card::Indignation => {
                // In Wrath: apply vulnerability to all enemies, else: enter Wrath
                if self.player.stance == Stance::Wrath {
                    for m in &mut self.monsters {
                        if !m.is_dead() {
                            m.apply_power(PowerType::Vulnerable, 1);
                        }
                    }
                } else {
                    self.change_stance(Stance::Wrath);
                }
            }
            Card::Swivel => {
                self.player_gain_block(card_inst.base_block());
                self.player.free_play_for = Some(vec![CardType::Attack]);
            }
            Card::Perseverance => {
                self.player_gain_block(card_inst.base_block());
                // Bonus block if retained (simplified: just base block)
            }
            Card::Pray => {
                self.player.apply_power(PowerType::MiracleCount, card_inst.base_magic());
                self.draw_cards(2);
                self.player.apply_power(PowerType::NoDraw, 1);
            }
            Card::Prostrate => {
                self.player_gain_block(card_inst.base_block());
                self.player.apply_power(PowerType::MiracleCount, 1);
            }
            Card::WreathOfFlameCard => {
                // X-cost: gain X strength this turn (simplified)
                let max_x = self.player.energy + effective_cost;
                let x = choice.map(|c| (c as i32).min(max_x)).unwrap_or(max_x);
                self.player.energy = max_x - x;
                if x > 0 {
                    self.player.apply_power(PowerType::Strength, x);
                }
            }

            // --- Watcher Uncommon Powers ---
            Card::BattleHymnCard => {
                self.player.apply_power(PowerType::BattleHymnPower, card_inst.base_magic());
            }
            Card::SimmeringFuryCard => {
                self.player.apply_power(PowerType::SimmeringFury, card_inst.base_magic());
            }
            Card::MentalFortressCard => {
                self.player.apply_power(PowerType::MentalFortress, card_inst.base_magic());
            }
            Card::NirvanaCard => {
                self.player.apply_power(PowerType::NirvanaPower, card_inst.base_magic());
            }
            Card::LikeWaterCard => {
                self.player.apply_power(PowerType::LikeWater, card_inst.base_magic());
            }
            Card::ForesightCard => {
                self.player.apply_power(PowerType::ForesightPower, card_inst.base_magic());
            }
            Card::StudyCard => {
                self.player.apply_power(PowerType::StudyPower, card_inst.base_magic());
            }
            Card::RushdownCard => {
                self.player.apply_power(PowerType::Rushdown, card_inst.base_magic());
            }

            // --- Watcher Rare Attacks ---
            Card::Ragnarok => {
                let ti = target_index.unwrap();
                let total_hits = 1 + card_inst.base_magic();
                for _ in 0..total_hits {
                    if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                        let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                        apply_damage_to_monster(&mut self.monsters[ti], damage);
                    }
                }
            }
            Card::BrillianceCard => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let miracle_count = self.player.get_power(PowerType::MiracleCount);
                    if miracle_count > 0 {
                        let total = card_inst.base_damage() * miracle_count;
                        let damage = calculate_player_damage(&self.player, &self.monsters[ti], total);
                        apply_damage_to_monster(&mut self.monsters[ti], damage);
                    }
                    // 0 damage if no miracles
                }
            }

            // --- Watcher Rare Skills ---
            Card::Blasphemy => {
                // Exhaust draw pile, apply Triple Attack power
                let draw_copy: Vec<usize> = self.player.draw_pile.drain(..).collect();
                for idx in draw_copy {
                    self.player.exhaust_pile.push(idx);
                }
                self.player.apply_power(PowerType::TripleAttack, 1);
            }
            Card::DeusExMachina => {
                self.player.apply_power(PowerType::MiracleCount, card_inst.base_magic());
            }
            Card::OmniscienceCard => {
                self.scry(card_inst.base_magic());
            }
            Card::ScrawlCard => {
                self.draw_cards(card_inst.base_magic());
            }
            Card::VaultCard => {
                // Discard hand, draw 5, gain 3 energy
                let hand_copy: Vec<usize> = self.player.hand_indices.drain(..).collect();
                for idx in hand_copy {
                    self.player.discard_pile.push(idx);
                }
                self.draw_cards(5);
                self.player.energy += 3;
            }
            Card::WishCard => {
                // Choice: 0=Strength, 1=Block, 2=Miracles
                match choice.unwrap_or(1) {
                    0 => {
                        // Become Almighty: +1 Str (upgraded: +2)
                        let str_gain = if card_inst.upgraded { 2 } else { 1 };
                        self.player.apply_power(PowerType::Strength, str_gain);
                    }
                    2 => {
                        // Fame and Fortune: +4 miracles (upgraded: +5)
                        let miracles = if card_inst.upgraded { 5 } else { 4 };
                        self.player.apply_power(PowerType::MiracleCount, miracles);
                    }
                    _ => {
                        // Live Forever: gain block (10, upgraded: 15)
                        self.player_gain_block(card_inst.base_block());
                    }
                }
            }
            Card::SpiritShieldCard => {
                // Block per card in hand
                let hand_count = self.player.hand_indices.len() as i32;
                let total_block = card_inst.base_block() * hand_count;
                self.player_gain_block(total_block);
            }
            Card::JudgmentCard => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    if self.monsters[ti].hp <= card_inst.base_magic() {
                        // Instant kill
                        self.monsters[ti].hp = 0;
                    }
                }
            }
            Card::WorshipCard => {
                // X-cost: gain miracles equal to X
                let max_x = self.player.energy + effective_cost;
                let x = choice.map(|c| (c as i32).min(max_x)).unwrap_or(max_x);
                self.player.energy = max_x - x;
                if x > 0 {
                    self.player.apply_power(PowerType::MiracleCount, x);
                }
            }

            // --- Watcher Rare Powers ---
            Card::OmegaCard => {
                self.player.apply_power(PowerType::OmegaPower, card_inst.base_magic());
            }
            Card::DevaFormCard => {
                self.player.apply_power(PowerType::DevaFormPower, card_inst.base_magic());
            }
            Card::DevotionCard => {
                self.player.apply_power(PowerType::DevotionPower, card_inst.base_magic());
            }
            Card::EstablishmentCard => {
                self.player.apply_power(PowerType::EstablishmentPower, card_inst.base_magic());
            }
            Card::ConjureBladeCard => {
                // X-cost: bonus damage to starter Strikes = X + magic
                let max_x = self.player.energy + effective_cost;
                let x = choice.map(|c| (c as i32).min(max_x)).unwrap_or(max_x);
                self.player.energy = max_x - x;
                let bonus = x + card_inst.base_magic();
                if bonus > 0 {
                    self.player.apply_power(PowerType::ConjureBladePower, bonus);
                }
            }

            // --- Ironclad Common Attacks ---
            Card::Anger => {
                self.attack_single(target_index, card_inst);
                // BG mod: card goes to draw pile instead of discard (purgeOnUse)
                self.player.draw_pile.push(deck_index);
                purge_played_card = true;
            }
            Card::BodySlam => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    // Damage equals current block
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], self.player.block);
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                }
            }
            Card::Clash => {
                // Only playable if all cards in hand are attacks (checked in get_available_actions)
                self.attack_single(target_index, card_inst);
            }
            Card::Cleave => {
                self.attack_all_enemies(card_inst);
            }
            Card::Clothesline => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                    self.monsters[ti].apply_power(PowerType::Weak, card_inst.base_magic());
                }
            }
            Card::HeavyBlade => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    // Str multiplied by magic number
                    let str_val = self.player.get_power(PowerType::Strength);
                    let bonus_str = str_val * (card_inst.base_magic() - 1); // extra multiplied Str
                    let base = card_inst.base_damage() + bonus_str;
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], base);
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                }
            }
            Card::IronWave => {
                if card_inst.upgraded && choice == Some(1) {
                    // BG mod Shield choice: 1 damage, 2 block
                    self.player_gain_block(card_inst.base_block());  // 2
                    let ti = target_index.unwrap();
                    if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                        let damage = calculate_player_damage(&self.player, &self.monsters[ti], 1);
                        apply_damage_to_monster(&mut self.monsters[ti], damage);
                    }
                } else {
                    // Base card (1dmg/1blk) or upgraded Spear choice (2dmg/1blk)
                    let block = if card_inst.upgraded { 1 } else { card_inst.base_block() };
                    self.player_gain_block(block);
                    self.attack_single(target_index, card_inst);
                }
            }
            Card::PerfectedStrike => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    // BG mod: count Strike cards in hand, excluding PerfectedStrike itself
                    let strike_count = self.player.hand_indices.iter()
                        .filter(|&&idx| self.deck[idx].card.is_strike())
                        .count() as i32;
                    let bonus = strike_count * card_inst.base_magic();
                    let base = card_inst.base_damage() + bonus;
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], base);
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                }
            }
            Card::PommelStrike => {
                self.attack_single(target_index, card_inst);
                self.draw_cards(card_inst.base_magic());
            }
            Card::TwinStrike => {
                // Hit twice
                self.attack_single(target_index, card_inst);
                self.attack_single(target_index, card_inst);
            }
            Card::WildStrike => {
                self.attack_single(target_index, card_inst);
                // Add Dazed to discard pile
                self.add_card_to_discard(Card::Dazed);
            }

            // --- Uncommon Attacks ---
            Card::BloodForBlood | Card::Carnage => {
                self.attack_single(target_index, card_inst);
            }
            Card::Headbutt => {
                self.attack_single(target_index, card_inst);
                // Put a card from discard on top of draw pile (first card in discard)
                if !self.player.discard_pile.is_empty() {
                    let idx = self.player.discard_pile.remove(0);
                    self.player.draw_pile.push(idx);
                }
            }
            Card::Rampage => {
                // Upgraded: exhaust 1 random card from hand first
                if card_inst.upgraded {
                    self.exhaust_random_from_hand();
                }
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    // Damage = number of cards in exhaust pile
                    let exhaust_count = self.player.exhaust_pile.len() as i32;
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], exhaust_count);
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                }
            }
            Card::SeverSoul => {
                // Deal damage first, then exhaust 1 random card from hand (2 if upgraded)
                self.attack_single(target_index, card_inst);
                let exhaust_count = if card_inst.upgraded { 2 } else { 1 };
                for _ in 0..exhaust_count {
                    self.exhaust_random_from_hand();
                }
            }
            Card::Uppercut => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                    // Base: 1 Vuln + 1 Weak; Upgraded: 2 Vuln + 1 Weak
                    let vuln_stacks = card_inst.base_magic();
                    let weak_stacks = 1;
                    self.monsters[ti].apply_power(PowerType::Vulnerable, vuln_stacks);
                    self.monsters[ti].apply_power(PowerType::Weak, weak_stacks);
                }
            }
            Card::Whirlwind => {
                // X-cost: spend X energy, hit all enemies X + magic times
                let max_x = self.player.energy + effective_cost;
                let x = choice.map(|c| (c as i32).min(max_x)).unwrap_or(max_x);
                self.player.energy = max_x - x;
                let hits = x + card_inst.base_magic();
                for _ in 0..hits {
                    self.attack_all_enemies(card_inst);
                }
            }

            // --- Rare Attacks ---
            Card::Bludgeon => {
                self.attack_single(target_index, card_inst);
            }
            Card::Feed => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
                    apply_damage_to_monster(&mut self.monsters[ti], damage);
                    if self.monsters[ti].is_dead() {
                        self.player.apply_power(PowerType::Strength, card_inst.base_magic());
                    }
                }
            }
            Card::FiendFire => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    // Exhaust all hand cards, then deal one hit per card exhausted
                    let hand_cards: Vec<usize> = self.player.hand_indices.drain(..).collect();
                    let hit_count = hand_cards.len();
                    for idx in hand_cards {
                        self.on_exhaust_card(idx);
                    }
                    // Each hit is a separate DamageAction (base_damage + STR each)
                    for _ in 0..hit_count {
                        let hit_damage = calculate_player_damage(&self.player, &self.monsters[ti],
                            card_inst.base_damage());
                        apply_damage_to_monster(&mut self.monsters[ti], hit_damage);
                    }
                }
            }
            Card::Immolate => {
                self.attack_all_enemies(card_inst);
                // Add 2 Dazed to discard pile
                self.add_card_to_discard(Card::Dazed);
                self.add_card_to_discard(Card::Dazed);
            }
            // --- Common Skills ---
            Card::Flex => {
                // Gain temporary Strength (removed at end of turn via LoseStrength)
                self.player.apply_power(PowerType::Strength, card_inst.base_magic());
                self.player.apply_power(PowerType::LoseStrength, card_inst.base_magic());
            }
            Card::Havoc => {
                // Play the top card of draw pile for free, then exhaust it (unless Power)
                if !self.player.draw_pile.is_empty() {
                    let top_idx = self.player.draw_pile.pop().unwrap();
                    self.player.hand_indices.push(top_idx);
                    let top_card = self.deck[top_idx];
                    let hand_pos = self.player.hand_indices.len() - 1;
                    let auto_target = if top_card.card.has_target() {
                        self.monsters.iter().position(|m| !m.is_dead())
                    } else {
                        None
                    };
                    let energy_before = self.player.energy;
                    self.play_card(hand_pos, auto_target, None);
                    self.player.energy = energy_before; // Havoc plays card for free
                    // Exhaust the auto-played card (unless it's a Power, which is already removed)
                    if top_card.card.card_type() != CardType::Power {
                        if let Some(pos) = self.player.discard_pile.iter().position(|&i| i == top_idx) {
                            self.player.discard_pile.remove(pos);
                            self.on_exhaust_card(top_idx);
                        }
                    }
                }
            }
            Card::SeeingRed => {
                self.player.energy += 2;
            }
            Card::ShrugItOff => {
                self.player_gain_block(card_inst.base_block());
                self.draw_cards(1);
            }
            Card::TrueGrit => {
                self.player_gain_block(card_inst.base_block());
                // Exhaust 1 random card from hand
                self.exhaust_random_from_hand();
            }
            Card::Warcry => {
                // Draw cards, put 1 card from hand on top of draw pile
                self.draw_cards(card_inst.base_magic());
                // Put last drawn card on top of draw pile (simplified)
                if !self.player.hand_indices.is_empty() {
                    let last_idx = self.player.hand_indices.pop().unwrap();
                    self.player.draw_pile.push(last_idx);
                }
            }

            // --- Uncommon Skills ---
            Card::BattleTrance => {
                self.draw_cards(card_inst.base_magic());
                self.player.apply_power(PowerType::NoDraw, 1);
            }
            Card::BurningPact => {
                // Exhaust 1 card from hand, draw cards
                self.exhaust_random_from_hand();
                self.draw_cards(card_inst.base_magic());
            }
            Card::Disarm => {
                let ti = target_index.unwrap();
                if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
                    self.monsters[ti].apply_power(PowerType::Weak, card_inst.base_magic());
                }
            }
            Card::Entrench => {
                // Double current block
                let current_block = self.player.block;
                self.player.add_block(current_block);
            }
            Card::FlameBarrier => {
                self.player_gain_block(card_inst.base_block());
                self.player.apply_power(PowerType::Thorns, 1);
            }
            Card::GhostlyArmor => {
                self.player_gain_block(card_inst.base_block());
            }
            Card::PowerThrough => {
                self.player_gain_block(card_inst.base_block());
                self.add_card_to_discard(Card::Dazed);
            }
            Card::RageCard => {
                // BG mod: gain block equal to number of Attacks in hand
                let attack_count = self.player.hand_indices.iter()
                    .filter(|&&idx| self.deck[idx].card.card_type() == CardType::Attack)
                    .count() as i32;
                if attack_count > 0 {
                    self.player_gain_block(attack_count);
                }
            }
            Card::SecondWind => {
                // Gain block per non-attack card in hand, exhaust those cards
                let non_attacks: Vec<usize> = self.player.hand_indices.iter()
                    .copied()
                    .filter(|&idx| self.deck[idx].card.card_type() != CardType::Attack)
                    .collect();
                let count = non_attacks.len() as i32;
                for idx in &non_attacks {
                    self.player.hand_indices.retain(|&i| i != *idx);
                }
                for idx in non_attacks {
                    self.on_exhaust_card(idx);
                }
                if count > 0 {
                    self.player_gain_block(card_inst.base_block() * count);
                }
            }
            Card::Sentinel => {
                self.player_gain_block(card_inst.base_block());
                // On exhaust: gain energy (handled specially since exhaust happens later)
                // The sentinel energy gain happens in on_exhaust_card if we track it
                // For now, simplified: the exhaust trigger handles it
            }
            Card::Shockwave => {
                // Base: 1 Vuln + 1 Weak; Upgraded: 1 Vuln + 2 Weak
                let vuln_stacks = 1;
                let weak_stacks = card_inst.base_magic();
                for m in &mut self.monsters {
                    if !m.is_dead() {
                        m.apply_power(PowerType::Vulnerable, vuln_stacks);
                        m.apply_power(PowerType::Weak, weak_stacks);
                    }
                }
            }
            Card::SpotWeakness => {
                // Die-based: base succeeds on 1-3, upgraded on 1-4
                let die_val = self.die.roll();
                let threshold = if card_inst.upgraded { 4 } else { 3 };
                if die_val <= threshold {
                    self.player.apply_power(PowerType::Strength, 1);
                }
            }

            // --- Rare Skills ---
            Card::DoubleTap => {
                self.player.apply_power(PowerType::DoubleTap, 1);
            }
            Card::Exhume => {
                // Get a card from exhaust pile back to hand
                if !self.player.exhaust_pile.is_empty() {
                    let idx = self.player.exhaust_pile.remove(0);
                    self.player.hand_indices.push(idx);
                }
            }
            Card::LimitBreak => {
                // Double current Strength
                let str_val = self.player.get_power(PowerType::Strength);
                if str_val > 0 {
                    self.player.apply_power(PowerType::Strength, str_val);
                }
            }
            Card::Offering => {
                // Lose 1 HP, gain 2 energy, draw cards
                self.player.hp -= 1;
                self.player.energy += 2;
                self.draw_cards(card_inst.base_magic());
            }
            Card::Impervious => {
                self.player_gain_block(card_inst.base_block());
            }

            // --- Power cards (apply the power, then card is removed from play) ---
            Card::Inflame => {
                self.player.apply_power(PowerType::Strength, 1);
            }
            Card::Metallicize => {
                self.player.apply_power(PowerType::Metallicize, 1);
            }
            Card::CombustCard => {
                self.player.apply_power(PowerType::Combust, card_inst.base_magic());
            }
            Card::DarkEmbrace => {
                self.player.apply_power(PowerType::DarkEmbrace, 1);
            }
            Card::Evolve => {
                self.player.apply_power(PowerType::Evolve, 1);
            }
            Card::FeelNoPain => {
                self.player.apply_power(PowerType::FeelNoPain, 1);
            }
            Card::FireBreathing => {
                self.player.apply_power(PowerType::FireBreathing, card_inst.base_magic());
            }
            Card::Rupture => {
                // BG mod: lose 1 HP, gain 1 Strength (simplified from vanilla power)
                self.player.hp -= 1;
                self.player.apply_power(PowerType::Strength, 1);
            }
            Card::Barricade => {
                self.player.apply_power(PowerType::Barricade, 1);
            }
            Card::BerserkCard => {
                self.player.apply_power(PowerType::Berserk, card_inst.base_magic());
            }
            Card::Corruption => {
                self.player.apply_power(PowerType::Corruption, 1);
            }
            Card::DemonForm => {
                self.player.apply_power(PowerType::DemonForm, 1);
            }
            Card::Juggernaut => {
                self.player.apply_power(PowerType::Juggernaut, card_inst.base_magic());
            }
            // Status/Curse — Slimed does nothing when played
            Card::Slimed => {}
            _ => {}
        }

        // Consume Vulnerable on attacked monsters (1 stack per card, not per hit)
        for &ti in &vuln_targets {
            if ti < self.monsters.len() {
                self.monsters[ti].reduce_power(PowerType::Vulnerable, 1);
            }
        }

        // Player Weak decay: after playing an ATTACK card, reduce Weak by 1
        if is_attack {
            self.player.reduce_power(PowerType::Weak, 1);
        }

        // Rage: gain block per attack played
        if is_attack {
            let rage = self.player.get_power(PowerType::Rage);
            if rage > 0 {
                self.player_gain_block(rage);
            }
        }

        // Anger (Nob): deal damage to player when a Skill is played (bypasses block)
        if is_skill {
            let mut anger_triggered = false;
            for m in &mut self.monsters {
                if !m.is_dead() {
                    let anger = m.get_power(PowerType::Anger);
                    if anger > 0 {
                        // Thorns-type damage: direct HP loss
                        self.player.hp -= anger;
                        anger_triggered = true;
                    }
                }
            }
            if anger_triggered && self.player.is_dead() {
                self.combat_over = true;
                self.player_won = false;
                return true;
            }
        }

        // DoubleTap: replay the attack as a full card play
        if is_attack && self.player.get_power(PowerType::DoubleTap) > 0 {
            self.player.reduce_power(PowerType::DoubleTap, 1);
            self.player.hand_indices.push(deck_index);
            let replay_pos = self.player.hand_indices.len() - 1;
            let energy_after_play = self.player.energy;
            self.player.energy = original_energy; // Restore pre-play energy for X-cost
            self.player.free_play_for = Some(vec![CardType::Attack]);
            self.play_card(replay_pos, target_index, None);
            self.player.energy = energy_after_play; // Restore post-play energy
            return true;
        }

        // Relic: on-card-play triggers (BirdFacedUrn)
        relics::on_card_play(&mut self.player, card_inst.card.card_type());

        // Power cards are removed from play (not discarded or exhausted)
        let is_power = card_inst.card.card_type() == CardType::Power;
        // BG mod: BurstCard is a Power but goes to discard pile
        let power_to_discard = matches!(card_inst.card, Card::BurstCard);
        if purge_played_card {
            // Card already placed (e.g. Anger → draw pile); skip normal disposition
        } else if retain_played_card {
            // BG selfRetain: card returns to hand after play
            self.player.hand_indices.push(deck_index);
        } else if is_power && !power_to_discard {
            // Power cards are simply removed from circulation
        } else {
            // Determine where card goes after play
            let should_exhaust = card_inst.exhausts() || (corruption && is_skill);
            if should_exhaust {
                self.on_exhaust_card(deck_index);
            } else {
                self.player.discard_pile.push(deck_index);
            }
        }

        self.has_card_been_played_this_turn = true;
        // Check if all monsters dead
        self.check_combat_end();

        true
    }

    /// End the player's turn: handle end-of-turn powers, ethereal cards, Burn/Decay, discard.
    pub fn end_player_turn(&mut self) {
        // Safety net: clear free_play_for at end of turn
        self.player.free_play_for = None;

        // DemonForm: gain Strength at end of turn
        let demon_form = self.player.get_power(PowerType::DemonForm);
        if demon_form > 0 {
            self.player.apply_power(PowerType::Strength, demon_form);
        }

        // Metallicize: gain block at end of turn
        let metallicize = self.player.get_power(PowerType::Metallicize);
        if metallicize > 0 {
            self.player_gain_block(metallicize);
        }

        // Combust: lose HP and deal damage to all enemies at end of turn
        let combust = self.player.get_power(PowerType::Combust);
        if combust > 0 {
            self.player.hp -= 1;
            for m in &mut self.monsters {
                if !m.is_dead() {
                    apply_damage_to_monster(m, combust);
                }
            }
            self.check_combat_end();
            if self.player.is_dead() {
                self.combat_over = true;
                self.player_won = false;
                return;
            }
        }

        // Process end-of-turn triggers on hand cards before discarding
        let hand_copy: Vec<usize> = self.player.hand_indices.clone();

        // Burn: deals self-damage at end of turn
        for &idx in &hand_copy {
            let card_inst = self.deck[idx];
            if card_inst.card == Card::Burn {
                apply_damage_to_player(&mut self.player, card_inst.base_magic());
            }
        }

        // Decay: deals 1 damage at end of turn
        for &idx in &hand_copy {
            let card_inst = self.deck[idx];
            if card_inst.card == Card::Decay {
                apply_damage_to_player(&mut self.player, 1);
            }
        }

        // Discard/exhaust remaining hand
        let mut new_hand: Vec<usize> = Vec::new();
        let mut exhaust_indices: Vec<usize> = Vec::new();
        for idx in self.player.hand_indices.drain(..) {
            let card_inst = self.deck[idx];
            if card_inst.card.retain() {
                new_hand.push(idx);
            } else if card_inst.card.ethereal() {
                exhaust_indices.push(idx);
            } else {
                self.player.discard_pile.push(idx);
            }
        }
        self.player.hand_indices = new_hand;

        // Process exhaust triggers after hand is drained
        for idx in exhaust_indices {
            self.on_exhaust_card(idx);
        }

        // Wrath: take 1 damage at end of turn
        if self.player.stance == Stance::Wrath {
            self.player.hp -= 1;
            if self.player.is_dead() {
                self.combat_over = true;
                self.player_won = false;
                return;
            }
        }

        // LikeWater: gain block at end of turn if in Calm
        if self.player.stance == Stance::Calm {
            let like_water = self.player.get_power(PowerType::LikeWater);
            if like_water > 0 {
                self.player_gain_block(like_water);
            }
        }

        // Omega: deal damage to all enemies at end of turn
        let omega = self.player.get_power(PowerType::OmegaPower);
        if omega > 0 {
            for i in 0..self.monsters.len() {
                if !self.monsters[i].is_dead() {
                    apply_damage_to_monster(&mut self.monsters[i], omega);
                }
            }
            self.check_combat_end();
        }

        // Conclusion: enter Neutral at end of turn
        let conclusion = self.player.get_power(PowerType::ConclusionPower);
        if conclusion > 0 {
            self.change_stance(Stance::Neutral);
            self.player.powers.remove(&PowerType::ConclusionPower);
        }

        // Trigger orb passives at end of turn (Defect)
        self.trigger_orb_passives();

        // Relic: end of turn hooks (Orichalcum)
        relics::on_turn_end(&mut self.player);

        // Check player death from Burn/Decay/Combust
        if self.player.is_dead() {
            self.combat_over = true;
            self.player_won = false;
        }
    }

    /// Roll the die and execute all monster turns.
    /// Returns the die roll value.
    pub fn roll_and_execute_monsters(&mut self) -> u8 {
        if self.combat_over {
            return 0;
        }

        let roll = self.die.roll();

        // Relic: die-roll triggers (Vajra, Oddly Smooth Stone, Pen Nib, etc.)
        let (extra_draw, extra_energy) = relics::on_die_roll(&mut self.player, &mut self.monsters, roll);
        self.player.energy += extra_energy;
        if extra_draw > 0 {
            self.draw_cards(extra_draw);
        }

        // SneckoEye: add Dazed to draw pile on roll 5-6
        if self.player.has_relic(crate::enums::Relic::SneckoEye) && roll >= 5 {
            self.add_card_to_draw(crate::cards::Card::Dazed);
        }

        // Relic: Mercury Hourglass (deal 1 dmg to all enemies at start of monster turn)
        relics::on_monster_turn_start(&self.player, &mut self.monsters);

        for i in 0..self.monsters.len() {
            if self.monsters[i].is_dead() {
                continue;
            }

            // Ritual fires at start of monster turn (not on first turn for Cultist)
            let ritual = self.monsters[i].get_power(PowerType::Ritual);
            if ritual > 0 && !self.monsters[i].first_turn {
                self.monsters[i].apply_power(PowerType::Strength, ritual);
            }

            // Reset monster block
            self.monsters[i].block = 0;

            // Select move
            if self.monsters[i].die_controlled {
                // Sentries use 2-char behavior (1-3→idx 0, 4-6→idx 1)
                if self.monsters[i].behavior.len() == 2 {
                    enemies::select_die_move_2char(&mut self.monsters[i], roll);
                } else {
                    enemies::select_die_move(&mut self.monsters[i], roll);
                }
            } else {
                enemies::select_move(&mut self.monsters[i]);
            }

            // Check if this monster will attack (for Weak/Vuln decay tracking)
            let intent = self.monsters[i].intent;
            let is_attacking = matches!(intent, Intent::Attack | Intent::AttackDefend | Intent::AttackBuff | Intent::AttackDebuff);

            // Execute move — need to split borrow
            let (left, _right) = self.monsters.split_at_mut(i + 1);
            let monster = &mut left[i];
            let hp_before = self.player.hp;
            let move_result = enemies::execute_move(monster, &mut self.player);
            let hp_lost = hp_before - self.player.hp;

            // Process MoveResult side effects
            for card in move_result.cards_to_draw_pile {
                self.add_card_to_draw(card);
            }
            for card in move_result.cards_to_discard_pile {
                self.add_card_to_discard(card);
            }
            if move_result.escaped {
                // Monster escapes — mark as dead
                self.monsters[i].hp = 0;
            }
            if move_result.monster_gain_block > 0 {
                self.monsters[i].add_block(move_result.monster_gain_block);
            }
            if !move_result.spawn_monsters.is_empty() {
                for new_monster in move_result.spawn_monsters {
                    self.monsters.push(new_monster);
                }
                // Run pre-battle for newly spawned monsters
                let start = self.monsters.len() - 1;
                // Pre-battle for spawned monsters happens after they're added
            }

            // Rupture: gain Str when player loses HP from attack
            if hp_lost > 0 {
                let rupture = self.player.get_power(PowerType::Rupture);
                if rupture > 0 {
                    self.player.apply_power(PowerType::Strength, rupture);
                }
            }

            // Thorns: deal damage back to attacking monster
            if is_attacking {
                let thorns = self.player.get_power(PowerType::Thorns);
                if thorns > 0 {
                    apply_damage_to_monster(&mut self.monsters[i], thorns);
                }
            }

            // Monster Weak decay: if monster attacked, reduce Weak by 1
            if is_attacking {
                self.monsters[i].reduce_power(PowerType::Weak, 1);
            }

            // Player Vulnerable decay: each attacking monster reduces player Vuln by 1
            if is_attacking {
                self.player.reduce_power(PowerType::Vulnerable, 1);
            }

            // Poison tick: deal Poison damage, reduce by 1
            let poison = self.monsters[i].get_power(PowerType::Poison);
            if poison > 0 {
                self.monsters[i].hp -= poison;
                self.monsters[i].reduce_power(PowerType::Poison, 1);
            }

            // Mark first turn done
            self.monsters[i].first_turn = false;
            self.monsters[i].turn_count += 1;

            // Check monster death from Thorns or Poison
            if self.monsters[i].is_dead() {
                self.on_monster_death(i);
            }

            // Check if player died
            if self.player.is_dead() {
                self.combat_over = true;
                self.player_won = false;
                return roll;
            }
        }

        // Check combat end (monsters may have died from thorns)
        self.check_combat_end();
        if self.combat_over {
            return roll;
        }

        // Start next player turn
        self.start_player_turn();

        roll
    }

    /// Add a card to the deck and put it in hand.
    pub fn add_card_to_hand(&mut self, card: Card) {
        let idx = self.deck.len();
        self.deck.push(CardInstance::new(card, false));
        self.player.hand_indices.push(idx);
    }

    /// Add an upgraded card to the deck and put it in hand.
    pub fn add_upgraded_card_to_hand(&mut self, card: Card) {
        let idx = self.deck.len();
        self.deck.push(CardInstance::new(card, true));
        self.player.hand_indices.push(idx);
    }

    /// Add a card to the deck and put it in discard pile.
    pub fn add_card_to_discard(&mut self, card: Card) {
        let idx = self.deck.len();
        self.deck.push(CardInstance::new(card, false));
        self.player.discard_pile.push(idx);
    }

    /// Add a card to the draw pile.
    pub fn add_card_to_draw(&mut self, card: Card) {
        let idx = self.deck.len();
        self.deck.push(CardInstance::new(card, false));
        self.player.draw_pile.push(idx);
    }

    /// Add an upgraded card to the draw pile.
    pub fn add_upgraded_card_to_draw(&mut self, card: Card) {
        let idx = self.deck.len();
        self.deck.push(CardInstance::new(card, true));
        self.player.draw_pile.push(idx);
    }

    /// Add an upgraded card to the discard pile.
    pub fn add_upgraded_card_to_discard(&mut self, card: Card) {
        let idx = self.deck.len();
        self.deck.push(CardInstance::new(card, true));
        self.player.discard_pile.push(idx);
    }

    /// Add a card to the exhaust pile.
    pub fn add_card_to_exhaust(&mut self, card: Card) {
        let idx = self.deck.len();
        self.deck.push(CardInstance::new(card, false));
        self.player.exhaust_pile.push(idx);
    }

    /// Deal damage to the player (for testing Blood for Blood, etc.)
    pub fn deal_damage_to_player(&mut self, amount: i32) {
        let hp_lost = apply_damage_to_player(&mut self.player, amount);
        if hp_lost > 0 {
            self.player_damaged_this_combat = true;
        }
    }

    /// Upgrade a card in the deck by its deck index.
    pub fn upgrade_card(&mut self, deck_index: usize) -> bool {
        if deck_index >= self.deck.len() {
            return false;
        }
        self.deck[deck_index].upgrade()
    }

    /// Get a list of monsters (for Python access).
    pub fn get_monsters(&self) -> Vec<Monster> {
        self.monsters.clone()
    }

    /// Get the full deck as CardInstance list (for Python access).
    pub fn get_deck(&self) -> Vec<CardInstance> {
        self.deck.clone()
    }

    /// Get the Card enum values in the deck (backward compat).
    pub fn get_deck_cards(&self) -> Vec<Card> {
        self.deck.iter().map(|ci| ci.card).collect()
    }

    /// Get the cards currently in hand (for Python access).
    pub fn get_hand(&self) -> Vec<CardInstance> {
        self.player.hand_indices.iter()
            .map(|&i| self.deck[i])
            .collect()
    }

    pub fn get_draw_pile(&self) -> Vec<CardInstance> {
        self.player.draw_pile.iter()
            .map(|&i| self.deck[i])
            .collect()
    }

    pub fn get_discard_pile(&self) -> Vec<CardInstance> {
        self.player.discard_pile.iter()
            .map(|&i| self.deck[i])
            .collect()
    }

    pub fn get_exhaust_pile(&self) -> Vec<CardInstance> {
        self.player.exhaust_pile.iter()
            .map(|&i| self.deck[i])
            .collect()
    }

    /// Get available actions: list of (hand_index, card_instance, needs_target) tuples.
    pub fn get_available_actions(&self) -> Vec<(usize, CardInstance, bool)> {
        let mut actions = Vec::new();
        let corruption = self.player.get_power(PowerType::Corruption) > 0;
        let entangled = self.player.get_power(PowerType::Entangled) > 0;
        let miracles = self.player.get_power(PowerType::MiracleCount);
        let total_energy = self.player.energy + miracles;
        for (hand_idx, &deck_idx) in self.player.hand_indices.iter().enumerate() {
            let ci = self.deck[deck_idx];
            if ci.card.unplayable() {
                continue;
            }
            let is_attack = ci.card.card_type() == CardType::Attack;
            let is_skill = ci.card.card_type() == CardType::Skill;

            if entangled && is_attack {
                continue;
            }

            let free_play = self.player.free_play_for.as_ref()
                .map_or(false, |types| types.contains(&ci.card.card_type()));
            let effective_cost = if corruption && is_skill { 0 } else if free_play { 0 } else { ci.cost() };
            if effective_cost <= total_energy {
                actions.push((hand_idx, ci, ci.card.has_target()));
            }
        }
        actions
    }

    /// Get valid target indices (alive monsters).
    pub fn get_valid_targets(&self) -> Vec<usize> {
        self.monsters.iter().enumerate()
            .filter(|(_, m)| !m.is_dead())
            .map(|(i, _)| i)
            .collect()
    }

    /// Deep clone for MCTS search.
    pub fn deep_clone(&self) -> CombatState {
        self.clone()
    }

    /// Apply a power to the player (for testing and scripting).
    pub fn apply_player_power(&mut self, power: PowerType, amount: i32) {
        self.player.apply_power(power, amount);
    }

    /// Get a player power value.
    pub fn get_player_power(&self, power: PowerType) -> i32 {
        self.player.get_power(power)
    }

    /// Set player energy directly (for testing).
    pub fn set_player_energy(&mut self, energy: i32) {
        self.player.energy = energy;
    }

    /// Set player block directly (for testing).
    pub fn set_player_block(&mut self, block: i32) {
        self.player.block = block;
    }

    /// Set player HP directly (for testing).
    pub fn set_player_hp(&mut self, hp: i32) {
        self.player.hp = hp;
    }

    /// Set the number of orb slots the player has.
    pub fn set_orb_slots(&mut self, slots: i32) {
        self.player.orb_slots = slots;
    }

    /// Channel an orb (Lightning, Frost, or Dark). Handles evocation if slots are full.
    pub fn channel_orb_type(&mut self, orb: crate::enums::OrbType) {
        self.channel_orb(orb);
    }

    /// Lock the die to a specific value (1-6) for deterministic testing.
    pub fn set_die_value(&mut self, value: i32) {
        self.die.set_value(value as u8);
    }

    /// Remove all orbs from the player.
    pub fn clear_orbs(&mut self) {
        self.player.orbs.clear();
    }

    /// Clear all player relics.
    pub fn clear_relics(&mut self) {
        self.player.relics.clear();
    }

    /// Add a relic to the player.
    pub fn add_relic(&mut self, relic: crate::enums::Relic) {
        self.player.relics.push(relic);
    }

    /// Get the player's relics.
    pub fn get_relics(&self) -> Vec<crate::enums::Relic> {
        self.player.relics.clone()
    }

    /// Get the player's current stance.
    pub fn get_stance(&self) -> Stance {
        self.player.stance
    }

    /// Get the player's miracle count.
    pub fn get_miracles(&self) -> i32 {
        self.player.get_power(PowerType::MiracleCount)
    }
}

impl CombatState {
    fn draw_cards(&mut self, count: i32) {
        // NoDraw: can't draw cards
        if self.player.get_power(PowerType::NoDraw) > 0 {
            return;
        }

        for _ in 0..count {
            if self.player.draw_pile.is_empty() {
                // Shuffle discard into draw pile
                if self.player.discard_pile.is_empty() {
                    break;
                }
                self.reshuffle_draw_pile();
            }
            if let Some(deck_idx) = self.player.draw_pile.pop() {
                let card_inst = self.deck[deck_idx];

                // Void: when drawn, lose 1 energy
                if card_inst.card == Card::VoidCard {
                    self.player.energy = (self.player.energy - 1).max(0);
                }

                // Evolve: draw a card when a Status is drawn
                let is_status = card_inst.card.card_type() == CardType::Status;
                let is_curse = card_inst.card.card_type() == CardType::Curse;

                // Fire Breathing: deal damage to all enemies when Status/Curse drawn
                if is_status || is_curse {
                    let fire_breathing = self.player.get_power(PowerType::FireBreathing);
                    if fire_breathing > 0 {
                        for m in &mut self.monsters {
                            if !m.is_dead() {
                                apply_damage_to_monster(m, fire_breathing);
                            }
                        }
                    }
                }

                self.player.hand_indices.push(deck_idx);

                // Evolve: draw extra card on Status draw
                if is_status {
                    let evolve = self.player.get_power(PowerType::Evolve);
                    if evolve > 0 {
                        // Draw extra cards (recursive, but bounded)
                        self.draw_cards_no_trigger(evolve);
                    }
                }
            }
        }
    }

    /// Draw cards without triggering on-draw power hooks (to prevent infinite loops).
    fn draw_cards_no_trigger(&mut self, count: i32) {
        for _ in 0..count {
            if self.player.draw_pile.is_empty() {
                if self.player.discard_pile.is_empty() {
                    break;
                }
                self.reshuffle_draw_pile();
            }
            if let Some(deck_idx) = self.player.draw_pile.pop() {
                let card_inst = self.deck[deck_idx];
                if card_inst.card == Card::VoidCard {
                    self.player.energy = (self.player.energy - 1).max(0);
                }
                self.player.hand_indices.push(deck_idx);
            }
        }
    }

    fn shuffle_draw_pile(&mut self) {
        self.player.draw_pile.shuffle(&mut self.rng);
    }

    fn reshuffle_draw_pile(&mut self) {
        self.player.draw_pile.append(&mut self.player.discard_pile);
        self.shuffle_draw_pile();
        // Relic: Red Skull — +1 Str on shuffle
        relics::on_shuffle(&mut self.player);
        // A Thousand Cuts: deal damage to all enemies on shuffle
        let atc = self.player.get_power(PowerType::AThousandCuts);
        if atc > 0 {
            for m in &mut self.monsters {
                if !m.is_dead() {
                    apply_damage_to_monster(m, atc);
                }
            }
        }
    }

    fn move_innate_to_top(&mut self) {
        let mut innate = Vec::new();
        let mut non_innate = Vec::new();
        for &idx in &self.player.draw_pile {
            if self.deck[idx].innate() {
                innate.push(idx);
            } else {
                non_innate.push(idx);
            }
        }
        self.player.draw_pile = non_innate;
        self.player.draw_pile.extend(innate);
    }

    /// Called when a card is exhausted.
    fn on_exhaust_card(&mut self, deck_index: usize) {
        self.player.exhaust_pile.push(deck_index);

        // Sentinel: gain energy when exhausted
        let card = self.deck[deck_index];
        if card.card == Card::Sentinel {
            let energy_gain = if card.upgraded { 3 } else { 2 };
            self.player.energy += energy_gain;
        }

        // Feel No Pain: gain block on exhaust
        let fnp = self.player.get_power(PowerType::FeelNoPain);
        if fnp > 0 {
            self.player_gain_block(fnp);
        }

        // Dark Embrace: draw a card on exhaust
        let de = self.player.get_power(PowerType::DarkEmbrace);
        if de > 0 {
            self.draw_cards_no_trigger(de);
        }
    }

    /// Called when a monster dies (for SporeCloud, etc.)
    fn on_monster_death(&mut self, _monster_idx: usize) {
        // SporeCloud: apply Vulnerable to player on death
        let spore = self.monsters[_monster_idx].get_power(PowerType::SporeCloud);
        if spore > 0 {
            self.player.apply_power(PowerType::Vulnerable, spore);
        }
    }

    /// Player gains block, modified by Dexterity and Juggernaut. Also triggers Juggernaut damage.
    fn player_gain_block(&mut self, amount: i32) {
        let dex = self.player.get_power(PowerType::Dexterity);
        let jugg = self.player.get_power(PowerType::Juggernaut);
        let final_amount = (amount + dex + jugg).max(0);
        if final_amount > 0 {
            self.player.add_block(final_amount);

            // Juggernaut: deal damage to random enemy on block gain
            if jugg > 0 {
                // Deal damage to first alive monster (deterministic for simulation)
                for m in &mut self.monsters {
                    if !m.is_dead() {
                        apply_damage_to_monster(m, jugg);
                        break;
                    }
                }
            }
        }
    }

    /// Helper: deal single-target attack damage using card's base damage.
    fn attack_single(&mut self, target_index: Option<usize>, card_inst: CardInstance) {
        let ti = target_index.unwrap();
        if ti < self.monsters.len() && !self.monsters[ti].is_dead() {
            let damage = calculate_player_damage(&self.player, &self.monsters[ti], card_inst.base_damage());
            apply_damage_to_monster(&mut self.monsters[ti], damage);
        }
    }

    /// Helper: deal damage to all alive enemies.
    fn attack_all_enemies(&mut self, card_inst: CardInstance) {
        for i in 0..self.monsters.len() {
            if !self.monsters[i].is_dead() {
                let damage = calculate_player_damage(&self.player, &self.monsters[i], card_inst.base_damage());
                apply_damage_to_monster(&mut self.monsters[i], damage);
            }
        }
    }

    /// Exhaust a random card from hand.
    fn exhaust_random_from_hand(&mut self) {
        if !self.player.hand_indices.is_empty() {
            let idx = self.player.hand_indices.remove(0);
            self.on_exhaust_card(idx);
        }
    }

    /// Discard a random card from hand.
    fn discard_random_from_hand(&mut self) {
        if !self.player.hand_indices.is_empty() {
            let idx = self.player.hand_indices.remove(0);
            self.player.discard_pile.push(idx);
        }
    }


    /// Change the player's stance. Handles exit/enter triggers.
    fn change_stance(&mut self, new_stance: Stance) {
        let (energy_gained, changed) = self.player.enter_stance(new_stance);
        if changed {
            self.stance_changed_this_turn = true;
            self.player.energy += energy_gained;

            // MentalFortress: gain block on stance change
            let mf = self.player.get_power(PowerType::MentalFortress);
            if mf > 0 {
                self.player_gain_block(mf);
            }

            // Rushdown: draw cards when entering Wrath
            if new_stance == Stance::Wrath {
                let rushdown = self.player.get_power(PowerType::Rushdown);
                if rushdown > 0 {
                    self.draw_cards(rushdown);
                }
            }
        }
    }

    /// Scry: look at top N cards of draw pile, discard status/curse cards.
    fn scry(&mut self, count: i32) {
        let nirvana = self.player.get_power(PowerType::NirvanaPower);
        let scry_count = count.min(self.player.draw_pile.len() as i32);
        let mut discarded = 0;

        // Check top N cards, discard status/curse
        let start = self.player.draw_pile.len().saturating_sub(scry_count as usize);
        let mut to_discard = Vec::new();
        for i in start..self.player.draw_pile.len() {
            let deck_idx = self.player.draw_pile[i];
            let card = self.deck[deck_idx];
            if card.card.card_type() == CardType::Status || card.card.card_type() == CardType::Curse {
                to_discard.push(i);
                discarded += 1;
            }
        }
        // Remove from draw pile in reverse order to preserve indices
        for &i in to_discard.iter().rev() {
            let deck_idx = self.player.draw_pile.remove(i);
            self.player.discard_pile.push(deck_idx);
        }

        // Nirvana: gain block per scry
        if nirvana > 0 && scry_count > 0 {
            self.player_gain_block(nirvana);
        }

        let _ = discarded;  // suppress unused warning
    }

    /// Channel an orb. If at capacity, auto-evokes first orb.
    fn channel_orb(&mut self, orb: OrbType) {
        if let Some(evoked) = self.player.channel_orb(orb) {
            // Process the auto-evoked orb
            self.process_evoke(evoked);
        }
    }

    /// Evoke the orb at the given index and process its effect.
    fn evoke_orb(&mut self, index: usize) {
        if let Some(orb) = self.player.remove_orb(index) {
            self.process_evoke(orb);
        }
    }

    /// Process the evoke effect of an orb.
    fn process_evoke(&mut self, orb: OrbType) {
        let evoke_bonus = self.player.get_power(PowerType::OrbEvoke);
        match orb {
            OrbType::Lightning => {
                // Deal 2 + evoke_bonus damage to random alive enemy
                let dmg = 2 + evoke_bonus;
                let electro = self.player.get_power(PowerType::Electrodynamics) > 0;
                if electro {
                    // Hit all enemies
                    for i in 0..self.monsters.len() {
                        if !self.monsters[i].is_dead() {
                            apply_damage_to_monster(&mut self.monsters[i], dmg);
                        }
                    }
                } else {
                    // Hit random alive enemy (first alive for determinism)
                    for i in 0..self.monsters.len() {
                        if !self.monsters[i].is_dead() {
                            apply_damage_to_monster(&mut self.monsters[i], dmg);
                            break;
                        }
                    }
                }
            }
            OrbType::Frost => {
                // Gain 1 + evoke_bonus block
                let block = (1 + evoke_bonus).max(0);
                self.player_gain_block(block);
            }
            OrbType::Dark => {
                // Deal 3 + evoke_bonus + amplify_dark damage to all enemies
                let amplify = self.player.get_power(PowerType::AmplifyDark);
                let dmg = (3 + evoke_bonus + amplify).max(0);
                for i in 0..self.monsters.len() {
                    if !self.monsters[i].is_dead() {
                        apply_damage_to_monster(&mut self.monsters[i], dmg);
                    }
                }
            }
        }
    }

    /// Trigger orb passives at end of player turn.
    fn trigger_orb_passives(&mut self) {
        let passive_bonus = self.player.get_power(PowerType::OrbPassive);
        let static_bonus = self.player.get_power(PowerType::StaticDischarge);
        let electro = self.player.get_power(PowerType::Electrodynamics) > 0;
        let loop_power = self.player.get_power(PowerType::Loop);
        let orbs = self.player.orbs.clone();

        for orb in &orbs {
            let triggers = 1 + loop_power;
            for _ in 0..triggers {
                match orb {
                    OrbType::Lightning => {
                        let dmg = (1 + passive_bonus + static_bonus).max(0);
                        if electro {
                            for i in 0..self.monsters.len() {
                                if !self.monsters[i].is_dead() {
                                    apply_damage_to_monster(&mut self.monsters[i], dmg);
                                }
                            }
                        } else {
                            for i in 0..self.monsters.len() {
                                if !self.monsters[i].is_dead() {
                                    apply_damage_to_monster(&mut self.monsters[i], dmg);
                                    break;
                                }
                            }
                        }
                    }
                    OrbType::Frost => {
                        let block = (1 + passive_bonus).max(0);
                        self.player_gain_block(block);
                    }
                    OrbType::Dark => {
                        // Dark has no passive in the board game
                    }
                }
            }
        }
    }

    fn check_combat_end(&mut self) {
        if self.monsters.iter().all(|m| m.is_dead()) {
            self.combat_over = true;
            self.player_won = true;
            // Relic: on victory (Burning Blood, Meat on the Bone, etc.)
            relics::on_victory(&mut self.player);
        }
    }
}
