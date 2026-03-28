#!/usr/bin/env python3
"""
Swarm Orchestrator - Coordinates multi-agent consensus for character generation
Deterministic seed chaining, weighted voting, iterative refinement.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass, field
from collections import defaultdict
import random
import time
import json

from .agents import (SwarmAgent, BodyAgent, StyleAgent, DiversityAgent, 
                    CriticAgent, AnimatorAgent, AgentDecision, create_agent_swarm)
from .nano_tensor import vector_hash

@dataclass
class ConsensusResult:
    """Result from swarm consensus"""
    approved: bool
    final_params: Dict[str, Any]
    agent_votes: Dict[str, float]
    confidence: float
    iterations: int
    timestamp: float = field(default_factory=time.time)
    metadata: Dict = field(default_factory=dict)

@dataclass
class SwarmGeneration:
    """A complete character generation with swarm decisions"""
    generation_id: str
    seed: int
    params: Dict[str, Any]
    consensus: ConsensusResult
    agent_decisions: Dict[str, AgentDecision]
    learning_feedback: Optional[float] = None

class SwarmOrchestrator:
    """
    Orchestrates the agent swarm through deterministic consensus rounds.
    Each generation is a structured debate between specialized agents.
    """
    
    def __init__(self, master_seed: int = 42, max_iterations: int = 10):
        self.master_seed = master_seed
        self.max_iterations = max_iterations
        self.rng = np.random.RandomState(master_seed)
        
        # Create agent swarm
        self.agents = create_agent_swarm(seed=master_seed)
        
        # Consensus configuration
        self.voting_weights = {
            'body': 1.0,
            'style': 0.8,
            'diversity': 1.2,  # Higher weight for novelty
            'critic': 1.5,     # Critic has veto power
            'animator': 0.5    # Only relevant for animations
        }
        
        self.approval_threshold = 0.45
        self.unanimity_bonus = 0.1
        
        # Generation tracking
        self.generation_history: List[SwarmGeneration] = []
        self.total_generations = 0
        self.approved_generations = 0
        
        # Learning state
        self.learning_enabled = True
        self.feedback_buffer = []
    
    def derive_seed(self, base_seed: int, generation_id: int, iteration: int) -> int:
        """Deterministically derive seed for specific generation/iteration"""
        # Hash-based seed derivation ensures reproducibility
        data = f"{base_seed}:{generation_id}:{iteration}"
        hash_val = int(vector_hash(np.array([base_seed, generation_id, iteration]))[:8], 16)
        return hash_val
    
    def gather_agent_votes(self, context: Dict, iteration: int) -> Dict[str, AgentDecision]:
        """Get decisions from all agents"""
        decisions = {}
        
        for agent_name, agent in self.agents.items():
            try:
                if agent_name == 'animator' and not context.get('generate_animation', False):
                    continue
                
                decision = agent.decide(context)
                decisions[agent_name] = decision
            except Exception as e:
                # Agent failure - use neutral decision
                decisions[agent_name] = AgentDecision(
                    values=np.zeros(5),
                    confidence=0.5,
                    reasoning=f"Error: {str(e)}",
                    metadata={'error': True}
                )
        
        return decisions
    
    def compute_consensus(self, decisions: Dict[str, AgentDecision], 
                         context: Dict) -> Tuple[bool, float, Dict[str, float]]:
        """
        Compute weighted consensus from agent votes.
        Returns (approved, confidence, vote_scores)
        """
        vote_scores = {}
        weighted_sum = 0.0
        total_weight = 0.0
        
        for agent_name, decision in decisions.items():
            weight = self.voting_weights.get(agent_name, 1.0)
            
            # Compute agent's vote score
            if agent_name == 'critic':
                # Critic votes on approval
                score = decision.values[0] * (1 - decision.values[1])  # quality * (1 - conflict)
            elif agent_name == 'diversity':
                # Diversity votes on novelty
                score = decision.values[0]  # novelty score
            elif agent_name == 'body':
                # Body votes on biological plausibility
                bmi = context.get('bmi', 25)
                score = decision.confidence * (0.8 if 15 < bmi < 35 else 0.3)
            elif agent_name == 'style':
                # Style votes on aesthetic quality
                score = decision.confidence
            else:
                score = decision.confidence
            
            vote_scores[agent_name] = score
            weighted_sum += score * weight
            total_weight += weight
        
        # Compute final score
        if total_weight > 0:
            consensus_score = weighted_sum / total_weight
        else:
            consensus_score = 0.0
        
        # Unanimity bonus
        all_scores = list(vote_scores.values())
        if all(s > 0.7 for s in all_scores):
            consensus_score += self.unanimity_bonus
        
        # Check approval
        approved = consensus_score >= self.approval_threshold
        
        return approved, min(1.0, consensus_score), vote_scores
    
    def refine_parameters(self, params: Dict, decisions: Dict[str, AgentDecision], 
                         iteration: int) -> Dict:
        """Refine parameters based on agent feedback"""
        refined = params.copy()
        
        # Body agent refinements
        if 'body' in decisions:
            body_vals = decisions['body'].values
            if len(body_vals) >= 3:
                # Adjust BMI toward agent recommendation
                current_bmi = refined.get('bmi', 25)
                target_bmi = body_vals[0]
                # Smooth interpolation
                alpha = 0.3 / (iteration + 1)  # Less adjustment each iteration
                refined['bmi'] = current_bmi * (1 - alpha) + target_bmi * alpha
        
        # Style agent refinements
        if 'style' in decisions:
            style_vals = decisions['style'].values
            # Could adjust color choices, etc.
            refined['style_confidence'] = decisions['style'].confidence
        
        # Diversity agent may suggest exploration
        if 'diversity' in decisions:
            diversity_vals = decisions['diversity'].values
            if diversity_vals[1] > 0.5:  # should_explore
                # Add more randomness
                refined['exploration_factor'] = diversity_vals[0]
        
        return refined
    
    def generate_character(self, base_seed: Optional[int] = None, 
                          initial_params: Optional[Dict] = None) -> SwarmGeneration:
        """
        Generate a character through swarm consensus.
        Deterministic given seed.
        """
        gen_id = self.total_generations
        seed = base_seed if base_seed is not None else self.derive_seed(
            self.master_seed, gen_id, 0)
        
        # Initialize parameters
        if initial_params is None:
            params = self._generate_initial_params(seed)
        else:
            params = initial_params.copy()
        
        # Iterative consensus
        final_decisions = {}
        approved = False
        confidence = 0.0
        vote_scores = {}
        
        for iteration in range(self.max_iterations):
            iter_seed = self.derive_seed(seed, gen_id, iteration)
            
            # Create context for agents
            context = {
                **params,
                'proposed_params': params,
                'iteration': iteration,
                'seed': iter_seed
            }
            
            # Gather votes
            decisions = self.gather_agent_votes(context, iteration)
            final_decisions = decisions
            
            # Compute consensus
            approved, confidence, vote_scores = self.compute_consensus(decisions, context)
            
            if approved:
                break
            
            # Refine and try again
            params = self.refine_parameters(params, decisions, iteration)
        
        # Create consensus result
        consensus = ConsensusResult(
            approved=approved,
            final_params=params,
            agent_votes=vote_scores,
            confidence=confidence,
            iterations=iteration + 1,
            metadata={'seed': seed, 'gen_id': gen_id}
        )
        
        # Record generation
        generation = SwarmGeneration(
            generation_id=f"swarm_{gen_id:06d}",
            seed=seed,
            params=params,
            consensus=consensus,
            agent_decisions=final_decisions
        )
        
        self.generation_history.append(generation)
        self.total_generations += 1
        if approved:
            self.approved_generations += 1
        
        # Record in diversity agent
        self.agents['diversity'].record_generation(params)
        
        return generation
    
    def _generate_initial_params(self, seed: int) -> Dict:
        """Generate initial random parameters"""
        rng = np.random.RandomState(seed)
        
        # Use original generator logic but seeded
        from ..pure_generator import PureCharacterGenerator
        temp_gen = PureCharacterGenerator()
        
        # Manually create parameters using the seeded RNG
        gender = 'male' if rng.random() < 0.5 else 'female'
        social_classes = ['poor', 'working', 'middle', 'upper', 'rich']
        social_class = social_classes[rng.randint(0, 5)]
        
        # Age distribution
        age_rand = rng.random()
        if age_rand < 0.15:
            age_cat, actual_age = 'teenager', rng.randint(13, 20)
        elif age_rand < 0.5:
            age_cat, actual_age = 'young_adult', rng.randint(20, 35)
        elif age_rand < 0.85:
            age_cat, actual_age = 'middle_aged', rng.randint(35, 55)
        elif age_rand < 0.97:
            age_cat, actual_age = 'older_adult', rng.randint(55, 70)
        else:
            age_cat, actual_age = 'elderly', rng.randint(70, 86)
        
        return {
            'gender': gender,
            'social_class': social_class,
            'age_category': age_cat,
            'actual_age': actual_age,
            'seed': seed,
            'bmi': rng.uniform(16, 32)
        }
    
    def provide_feedback(self, generation_id: str, feedback: float, 
                        correction: Optional[Dict] = None):
        """
        Provide learning feedback for a generation.
        feedback: 0.0 (bad) to 1.0 (perfect)
        """
        # Find generation
        gen = None
        for g in self.generation_history:
            if g.generation_id == generation_id:
                gen = g
                break
        
        if gen is None:
            return
        
        gen.learning_feedback = feedback
        self.feedback_buffer.append((gen, feedback, correction))
        
        if not self.learning_enabled:
            return
        
        # Train agents
        for agent_name, decision in gen.agent_decisions.items():
            agent = self.agents.get(agent_name)
            if agent:
                agent.learn(decision, feedback)
        
        # Adjust voting weights based on long-term performance
        if len(self.feedback_buffer) >= 10:
            self._adapt_weights()
    
    def _adapt_weights(self):
        """Adapt voting weights based on agent performance"""
        for agent_name, agent in self.agents.items():
            perf = agent.get_performance()
            if perf['total_decisions'] > 10:
                # Weight adjustment
                accuracy = perf['accuracy']
                old_weight = self.voting_weights.get(agent_name, 1.0)
                # Smooth adjustment
                new_weight = old_weight * 0.9 + accuracy * 0.1
                self.voting_weights[agent_name] = max(0.1, min(2.0, new_weight))
    
    def get_stats(self) -> Dict:
        """Get swarm statistics"""
        agent_perfs = {name: agent.get_performance() 
                      for name, agent in self.agents.items()}
        
        diversity_stats = self.agents['diversity'].get_coverage_stats()
        
        return {
            'total_generations': self.total_generations,
            'approved_generations': self.approved_generations,
            'approval_rate': self.approved_generations / max(1, self.total_generations),
            'agent_performance': agent_perfs,
            'diversity_coverage': diversity_stats,
            'voting_weights': self.voting_weights.copy()
        }
    
    def save_state(self, filepath: str):
        """Save swarm state"""
        state = {
            'master_seed': self.master_seed,
            'total_generations': self.total_generations,
            'voting_weights': self.voting_weights,
            'agent_states': {name: agent.get_performance() 
                           for name, agent in self.agents.items()},
            'stats': self.get_stats()
        }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2, default=str)
    
    def load_state(self, filepath: str):
        """Load swarm state"""
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        self.master_seed = state['master_seed']
        self.total_generations = state['total_generations']
        self.voting_weights = state['voting_weights']


def demo_orchestrator():
    """Demonstrate orchestrator capabilities"""
    print("=" * 70)
    print("SWARM ORCHESTRATOR DEMO")
    print("=" * 70)
    
    # Create orchestrator
    orch = SwarmOrchestrator(master_seed=42, max_iterations=5)
    
    print("\n1. Generating 10 characters through swarm consensus...")
    print("-" * 70)
    
    for i in range(10):
        gen = orch.generate_character()
        status = "✓ APPROVED" if gen.consensus.approved else "✗ REJECTED"
        print(f"   {gen.generation_id}: {status} "
              f"(conf={gen.consensus.confidence:.2f}, "
              f"iter={gen.consensus.iterations})")
        
        # Simulate feedback
        feedback = 0.7 + np.random.random() * 0.3  # Mostly positive
        orch.provide_feedback(gen.generation_id, feedback)
    
    print("\n2. Swarm Statistics")
    print("-" * 70)
    stats = orch.get_stats()
    print(f"   Total generations: {stats['total_generations']}")
    print(f"   Approved: {stats['approved_generations']} "
          f"({stats['approval_rate']:.1%})")
    print(f"   Diversity coverage: {stats['diversity_coverage']['coverage_ratio']:.1%}")
    
    print("\n3. Agent Performance")
    print("-" * 70)
    for name, perf in stats['agent_performance'].items():
        print(f"   {name:12s}: {perf['total_decisions']:3d} decisions, "
              f"{perf['accuracy']:.1%} accuracy, "
              f"weight={stats['voting_weights'].get(name, 1.0):.2f}")
    
    print("\n4. Determinism Check")
    print("-" * 70)
    orch2 = SwarmOrchestrator(master_seed=42, max_iterations=5)
    gen1 = orch.generate_character(base_seed=12345)
    gen2 = orch2.generate_character(base_seed=12345)
    print(f"   Same seed -> Same params: {gen1.params == gen2.params}")
    print(f"   Same seed -> Same consensus: {gen1.consensus.approved == gen2.consensus.approved}")
    
    print("\n" + "=" * 70)
    print("ORCHESTRATOR DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demo_orchestrator()
