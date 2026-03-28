#!/usr/bin/env python3
"""
Swarm Agents - Specialized nano-tensor agents for character generation
Each agent has a specific domain expertise and learns from experience.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from collections import defaultdict
import random

from .nano_tensor import NanoTensor, NanoTensorConfig, EnsembleNanoTensor, normalize_vector, encode_categorical

# ==================== AGENT BASE CLASS ====================

@dataclass
class AgentDecision:
    """Output from an agent decision"""
    values: np.ndarray
    confidence: float
    reasoning: str
    metadata: Dict[str, Any]

class SwarmAgent:
    """Base class for all swarm agents"""
    
    def __init__(self, name: str, seed: int = 42):
        self.name = name
        self.seed = seed
        self.rng = np.random.RandomState(seed)
        self.decision_history = []
        self.total_decisions = 0
        self.successful_decisions = 0
        
    def decide(self, context: Dict) -> AgentDecision:
        """Make a decision based on context - override in subclass"""
        raise NotImplementedError
    
    def learn(self, decision: AgentDecision, feedback: float, correction: Optional[np.ndarray] = None):
        """Learn from feedback - override in subclass"""
        self.total_decisions += 1
        if feedback > 0.5:
            self.successful_decisions += 1
    
    def get_performance(self) -> Dict:
        """Get agent performance metrics"""
        accuracy = (self.successful_decisions / max(1, self.total_decisions))
        return {
            'name': self.name,
            'total_decisions': self.total_decisions,
            'successful': self.successful_decisions,
            'accuracy': accuracy
        }

# ==================== SPECIALIZED AGENTS ====================

class BodyAgent(SwarmAgent):
    """
    Nano-Agent for anatomical/biological decisions.
    Learns: BMI rules, age-body correlations, proportion relationships.
    """
    
    def __init__(self, seed: int = 42):
        super().__init__("BodyAgent", seed)
        
        # Ensemble of nano-networks for different aspects
        self.bmi_network = NanoTensor(NanoTensorConfig(
            input_dim=6,  # age, gender, social_class, height, random1, random2
            hidden_dim=12,
            output_dim=3,  # BMI, weight, body_fat
            seed=seed,
            learning_rate=0.02
        ))
        
        self.proportion_network = NanoTensor(NanoTensorConfig(
            input_dim=5,  # BMI, height, age, gender, body_type
            hidden_dim=10,
            output_dim=4,  # head_scale, torso_scale, limb_scale, shoulder_width
            seed=seed + 1,
            learning_rate=0.015
        ))
        
        # Knowledge base (rules learned)
        self.known_correlations = defaultdict(float)
    
    def encode_input(self, age: int, gender: str, social_class: str, 
                     height_category: str) -> np.ndarray:
        """Encode biological parameters to vector"""
        # Normalize age
        age_norm = (age - 13) / 72  # 13-85 range
        
        # Encode gender
        gender_val = 1.0 if gender == 'male' else 0.0
        
        # Encode social class
        class_map = {'poor': 0.0, 'working': 0.25, 'middle': 0.5, 'upper': 0.75, 'rich': 1.0}
        class_val = class_map.get(social_class, 0.5)
        
        # Encode height
        height_map = {'very_short': 0.0, 'short': 0.25, 'average': 0.5, 'tall': 0.75, 'very_tall': 1.0}
        height_val = height_map.get(height_category, 0.5)
        
        # Random exploration factors
        rand1 = self.rng.random()
        rand2 = self.rng.random()
        
        return np.array([age_norm, gender_val, class_val, height_val, rand1, rand2])
    
    def decide(self, context: Dict) -> AgentDecision:
        """Generate body metrics decision"""
        age = context['actual_age']
        gender = context['gender']
        social_class = context['social_class']
        height_category = context.get('height_category', 'average')
        
        # Get BMI prediction
        input_vec = self.encode_input(age, gender, social_class, height_category)
        bmi_output = self.bmi_network.predict(input_vec)
        
        # Decode BMI output
        bmi = bmi_output[0] * 27 + 13  # Scale to 13-40 range
        weight_factor = bmi_output[1]
        body_fat = bmi_output[2]
        
        # Get proportion predictions
        proportion_input = np.array([
            (bmi - 13) / 27,
            {'very_short': 0.0, 'short': 0.25, 'average': 0.5, 'tall': 0.75, 'very_tall': 1.0}.get(height_category, 0.5),
            (age - 13) / 72,
            1.0 if gender == 'male' else 0.0,
            weight_factor
        ])
        proportion_output = self.proportion_network.predict(proportion_input)
        
        # Combine into decision
        values = np.array([
            bmi,
            weight_factor,
            body_fat,
            proportion_output[0],  # head_scale
            proportion_output[1],  # torso_scale
            proportion_output[2],  # limb_scale
            proportion_output[3],  # shoulder_width
        ])
        
        # Confidence based on training experience
        confidence = min(0.95, 0.5 + self.bmi_network.total_updates / 1000)
        
        reasoning = f"BMI={bmi:.1f} for {age}yo {gender} ({social_class}), height={height_category}"
        
        decision = AgentDecision(
            values=values,
            confidence=confidence,
            reasoning=reasoning,
            metadata={'bmi_output': bmi_output, 'proportion_output': proportion_output}
        )
        
        self.decision_history.append(decision)
        return decision
    
    def learn(self, decision: AgentDecision, feedback: float, correction: Optional[np.ndarray] = None):
        """Learn from body metric feedback"""
        super().learn(decision, feedback, correction)
        
        if correction is not None:
            # Update BMI network
            # Reconstruct input (simplified - in practice store in decision)
            last_context = self.decision_history[-1].metadata if self.decision_history else {}
            
            # Train toward correction
            target_bmi = correction[0] if len(correction) > 0 else decision.values[0]
            target_bmi_norm = (target_bmi - 13) / 27
            
            # Create synthetic training example
            if 'bmi_output' in last_context:
                synthetic_input = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5])  # Placeholder
                target = np.array([target_bmi_norm, decision.values[1] / 200, decision.values[2]])
                self.bmi_network.train_step(synthetic_input, target)


class StyleAgent(SwarmAgent):
    """
    Nano-Agent for aesthetic/style decisions.
    Learns: Color harmony, fashion rules, social class styling.
    """
    
    def __init__(self, seed: int = 42):
        super().__init__("StyleAgent", seed)
        
        self.color_network = NanoTensor(NanoTensorConfig(
            input_dim=8,  # skin_tone_r, skin_tone_g, skin_tone_b, age, social_class, gender, season, formality
            hidden_dim=16,
            output_dim=6,  # clothing_h, clothing_s, clothing_v, hair_adjust, complementary, contrast
            seed=seed,
            learning_rate=0.025
        ))
        
        self.fashion_network = NanoTensor(NanoTensorConfig(
            input_dim=5,  # social_class, age, gender, body_type, occasion
            hidden_dim=12,
            output_dim=4,  # formality, casualness, trendiness, accessories
            seed=seed + 1,
            learning_rate=0.02
        ))
        
        # Color palette knowledge
        self.harmony_scores = defaultdict(list)
    
    def rgb_to_hsv(self, r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Convert RGB to HSV"""
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        else:
            h = (60 * ((r - g) / df) + 240) % 360
        s = 0 if mx == 0 else df / mx
        v = mx
        return h / 360, s, v
    
    def decide(self, context: Dict) -> AgentDecision:
        """Generate style/color decisions"""
        skin_color = context['skin_color']
        age = context['actual_age']
        social_class = context['social_class']
        gender = context['gender']
        
        # Encode input
        skin_h, skin_s, skin_v = self.rgb_to_hsv(*skin_color)
        age_norm = (age - 13) / 72
        class_map = {'poor': 0.0, 'working': 0.25, 'middle': 0.5, 'upper': 0.75, 'rich': 1.0}
        class_val = class_map.get(social_class, 0.5)
        gender_val = 1.0 if gender == 'male' else 0.0
        season = self.rng.random()  # Random season factor
        formality_seed = self.rng.random()
        
        input_vec = np.array([skin_h, skin_s, skin_v, age_norm, class_val, gender_val, season, formality_seed])
        color_output = self.color_network.predict(input_vec)
        
        # Decode color decisions
        clothing_hue = color_output[0]
        clothing_sat = color_output[1] * 0.5 + 0.25  # 0.25-0.75
        clothing_val = color_output[2] * 0.5 + 0.25
        hair_adjust = color_output[3] - 0.5  # -0.5 to 0.5
        complementary = color_output[4]
        contrast = color_output[5]
        
        # Get fashion decisions
        fashion_input = np.array([class_val, age_norm, gender_val, 0.5, formality_seed])
        fashion_output = self.fashion_network.predict(fashion_input)
        
        values = np.array([
            clothing_hue,
            clothing_sat,
            clothing_val,
            hair_adjust,
            complementary,
            contrast,
            fashion_output[0],  # formality
            fashion_output[1],  # casualness
        ])
        
        confidence = min(0.9, 0.4 + self.color_network.total_updates / 800)
        
        reasoning = f"Style for {social_class} {gender}: hue={clothing_hue:.2f}, formality={fashion_output[0]:.2f}"
        
        return AgentDecision(
            values=values,
            confidence=confidence,
            reasoning=reasoning,
            metadata={'color_output': color_output, 'fashion_output': fashion_output}
        )
    
    def learn(self, decision: AgentDecision, feedback: float, correction: Optional[np.ndarray] = None):
        """Learn from style feedback"""
        super().learn(decision, feedback, correction)
        
        # Update harmony scores
        key = tuple(decision.values[:3].round(2))
        self.harmony_scores[key].append(feedback)


class DiversityAgent(SwarmAgent):
    """
    Nano-Agent for ensuring parameter space coverage.
    Learns: Which regions have been explored, novelty maximization.
    """
    
    def __init__(self, seed: int = 42, memory_size: int = 10000):
        super().__init__("DiversityAgent", seed)
        
        self.novelty_network = NanoTensor(NanoTensorConfig(
            input_dim=10,  # Parameter vector
            hidden_dim=20,
            output_dim=1,  # Novelty score
            seed=seed,
            learning_rate=0.01
        ))
        
        # Memory of generated parameters
        self.memory_size = memory_size
        self.parameter_memory = []
        self.embedding_memory = []
        
        # Coverage tracking
        self.grid_coverage = defaultdict(int)
        self.grid_resolution = 10  # 10x10 grid per dimension pair
    
    def compute_embedding(self, params: Dict) -> np.ndarray:
        """Compute embedding vector from parameters"""
        # Extract key features
        features = [
            params.get('actual_age', 30) / 100,
            1.0 if params.get('gender') == 'male' else 0.0,
            {'poor': 0, 'working': 0.25, 'middle': 0.5, 'upper': 0.75, 'rich': 1.0}.get(params.get('social_class'), 0.5),
            params.get('skin_color', (128, 128, 128))[0] / 255,
            params.get('hair_color', (128, 128, 128))[0] / 255,
            params.get('bmi', 25) / 40,
            random.random(),
            random.random(),
            random.random(),
            random.random(),
        ]
        return np.array(features)
    
    def compute_novelty(self, embedding: np.ndarray) -> float:
        """Compute novelty score based on distance from memory"""
        if not self.embedding_memory:
            return 1.0
        
        # Compute average distance to k nearest neighbors
        k = min(5, len(self.embedding_memory))
        distances = []
        for mem_emb in self.embedding_memory:
            dist = np.linalg.norm(embedding - mem_emb)
            distances.append(dist)
        
        distances.sort()
        avg_dist = np.mean(distances[:k])
        
        # Normalize to 0-1
        novelty = min(1.0, avg_dist / np.sqrt(len(embedding)))
        return novelty
    
    def decide(self, context: Dict) -> AgentDecision:
        """Decide diversity/exploration strategy"""
        proposed_params = context.get('proposed_params', {})
        
        # Compute embedding
        embedding = self.compute_embedding(proposed_params)
        
        # Get novelty score
        novelty = self.compute_novelty(embedding)
        
        # Use network to predict if we should accept
        network_novelty = self.novelty_network.predict(embedding)
        
        # Combined score
        combined_novelty = 0.6 * novelty + 0.4 * network_novelty[0]
        
        # Decide exploration vs exploitation
        should_explore = combined_novelty > 0.3  # Threshold
        
        values = np.array([
            combined_novelty,
            float(should_explore),
            len(self.parameter_memory) / self.memory_size,  # Memory fullness
            novelty,
            network_novelty[0]
        ])
        
        confidence = min(0.95, 0.6 + len(self.parameter_memory) / 2000)
        
        reasoning = f"Novelty={combined_novelty:.3f}, Memory={len(self.parameter_memory)}, Explore={should_explore}"
        
        return AgentDecision(
            values=values,
            confidence=confidence,
            reasoning=reasoning,
            metadata={'embedding': embedding, 'should_explore': should_explore}
        )
    
    def record_generation(self, params: Dict):
        """Record a generated character for diversity tracking"""
        embedding = self.compute_embedding(params)
        
        self.parameter_memory.append(params)
        self.embedding_memory.append(embedding)
        
        # Maintain memory size
        if len(self.parameter_memory) > self.memory_size:
            self.parameter_memory.pop(0)
            self.embedding_memory.pop(0)
        
        # Update grid coverage
        # Use first two dimensions for grid
        x = int(embedding[0] * self.grid_resolution) % self.grid_resolution
        y = int(embedding[1] * self.grid_resolution) % self.grid_resolution
        self.grid_coverage[(x, y)] += 1
    
    def get_coverage_stats(self) -> Dict:
        """Get diversity coverage statistics"""
        total_cells = self.grid_resolution ** 2
        filled_cells = len(self.grid_coverage)
        coverage_ratio = filled_cells / total_cells
        
        # Entropy of distribution
        if self.grid_coverage:
            values = np.array(list(self.grid_coverage.values()))
            probs = values / values.sum()
            entropy = -np.sum(probs * np.log(probs + 1e-10))
            max_entropy = np.log(total_cells)
            normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        else:
            normalized_entropy = 0
        
        return {
            'coverage_ratio': coverage_ratio,
            'entropy': normalized_entropy,
            'total_generated': len(self.parameter_memory),
            'unique_cells': filled_cells
        }


class CriticAgent(SwarmAgent):
    """
    Nano-Agent for validation and quality control.
    Learns: Conflict detection, quality scoring, biological plausibility.
    """
    
    def __init__(self, seed: int = 42):
        super().__init__("CriticAgent", seed)
        
        self.quality_network = NanoTensor(NanoTensorConfig(
            input_dim=12,  # Combined feature vector
            hidden_dim=16,
            output_dim=3,  # quality_score, conflict_score, plausibility
            seed=seed,
            learning_rate=0.015
        ))
        
        self.conflict_rules = []
        self.quality_threshold = 0.6
    
    def encode_validation_input(self, params: Dict) -> np.ndarray:
        """Encode parameters for validation"""
        features = [
            params.get('actual_age', 30) / 100,
            1.0 if params.get('gender') == 'male' else 0.0,
            {'poor': 0, 'working': 0.25, 'middle': 0.5, 'upper': 0.75, 'rich': 1.0}.get(params.get('social_class'), 0.5),
            params.get('bmi', 25) / 40,
            {'very_short': 0, 'short': 0.25, 'average': 0.5, 'tall': 0.75, 'very_tall': 1.0}.get(params.get('height_category'), 0.5),
            random.random(),  # Body type encoding placeholder
            params.get('skin_color', (128, 128, 128))[0] / 255,
            random.random(),
            random.random(),
            random.random(),
            random.random(),
            random.random(),
        ]
        return np.array(features)
    
    def check_conflicts(self, params: Dict) -> List[str]:
        """Check for logical/biological conflicts"""
        conflicts = []
        
        # Age-body conflicts
        age = params.get('actual_age', 30)
        bmi = params.get('bmi', 25)
        
        if age < 18 and bmi > 35:
            conflicts.append("teenager_high_bmi")
        if age > 70 and bmi < 16:
            conflicts.append("elderly_very_underweight")
        
        # Social class conflicts
        social_class = params.get('social_class', 'middle')
        has_expensive_jewelry = params.get('has_jewelry', False) and social_class in ['poor', 'working']
        if has_expensive_jewelry:
            conflicts.append("class_jewelry_mismatch")
        
        # Gender-style conflicts (very loose)
        # (Intentionally permissive - modern fashion breaks rules)
        
        return conflicts
    
    def decide(self, context: Dict) -> AgentDecision:
        """Validate proposed character"""
        proposed = context.get('proposed_params', {})
        
        # Check explicit conflicts
        conflicts = self.check_conflicts(proposed)
        conflict_score = len(conflicts) / 5.0  # Normalize
        
        # Network-based quality assessment
        input_vec = self.encode_validation_input(proposed)
        quality_output = self.quality_network.predict(input_vec)
        
        quality_score = quality_output[0]
        network_conflict = quality_output[1]
        plausibility = quality_output[2]
        
        # Combined validation
        final_quality = (quality_score + (1 - conflict_score) + plausibility) / 3
        final_conflict = max(conflict_score, network_conflict)
        
        values = np.array([
            final_quality,
            final_conflict,
            plausibility,
            float(final_quality > self.quality_threshold),
            float(len(conflicts) == 0)
        ])
        
        confidence = quality_output[0]
        
        reasoning = f"Quality={final_quality:.2f}, Conflicts={len(conflicts)}, Plausible={plausibility:.2f}"
        
        return AgentDecision(
            values=values,
            confidence=confidence,
            reasoning=reasoning,
            metadata={
                'conflicts': conflicts,
                'quality_output': quality_output,
                'approved': final_quality > self.quality_threshold and len(conflicts) == 0
            }
        )
    
    def learn(self, decision: AgentDecision, feedback: float, correction: Optional[np.ndarray] = None):
        """Learn from validation feedback"""
        super().learn(decision, feedback, correction)
        
        # Update conflict rules based on feedback
        if feedback < 0.3 and 'conflicts' in decision.metadata:
            # False negative - add new rule
            pass  # Simplified - would add rule learning here


class AnimatorAgent(SwarmAgent):
    """
    Nano-Agent for animation/motion decisions.
    Learns: Natural movement patterns, physics-based animation.
    """
    
    def __init__(self, seed: int = 42):
        super().__init__("AnimatorAgent", seed)
        
        self.motion_network = NanoTensor(NanoTensorConfig(
            input_dim=7,  # body_type, age, height, weight, animation_type, frame, total_frames
            hidden_dim=14,
            output_dim=5,  # body_y, head_y, arm_offset, leg_offset, bounce
            seed=seed,
            learning_rate=0.02
        ))
        
        self.animation_types = ['idle', 'walk', 'run', 'jump']
    
    def decide_frame(self, context: Dict, frame_idx: int, total_frames: int) -> AgentDecision:
        """Generate animation frame offsets"""
        params = context.get('body_metrics', {})
        anim_type = context.get('animation_type', 'idle')
        
        # Encode
        body_type_map = {'emaciated': 0, 'very_thin': 0.1, 'lean_athletic': 0.3,
                        'muscular_athletic': 0.5, 'lean_normal': 0.6, 'average': 0.7,
                        'stocky': 0.8, 'overweight': 0.9, 'obese': 1.0}
        body_type_val = body_type_map.get(params.get('body_type_display', '').lower().replace(' ', '_'), 0.7)
        
        age_norm = params.get('actual_age', 30) / 100
        height_map = {'very_short': 0, 'short': 0.25, 'average': 0.5, 'tall': 0.75, 'very_tall': 1.0}
        height_val = height_map.get(context.get('height_category', 'average'), 0.5)
        weight_norm = params.get('weight_pounds', 150) / 300
        anim_type_val = self.animation_types.index(anim_type) / len(self.animation_types)
        frame_norm = frame_idx / max(1, total_frames - 1)
        
        input_vec = np.array([body_type_val, age_norm, height_val, weight_norm, 
                             anim_type_val, frame_norm, total_frames / 10])
        
        motion_output = self.motion_network.predict(input_vec)
        
        values = motion_output  # Direct mapping to animation offsets
        
        confidence = 0.7 + self.motion_network.total_updates / 500
        
        reasoning = f"{anim_type} frame {frame_idx}/{total_frames}: bounce={motion_output[4]:.2f}"
        
        return AgentDecision(
            values=values,
            confidence=min(0.95, confidence),
            reasoning=reasoning,
            metadata={'animation_type': anim_type, 'frame': frame_idx}
        )
    
    def decide(self, context: Dict) -> AgentDecision:
        """Decide animation parameters"""
        return self.decide_frame(context, 0, 1)


# ==================== AGENT FACTORY ====================

def create_agent_swarm(seed: int = 42) -> Dict[str, SwarmAgent]:
    """Create a full swarm of specialized agents"""
    return {
        'body': BodyAgent(seed=seed),
        'style': StyleAgent(seed=seed + 10),
        'diversity': DiversityAgent(seed=seed + 20),
        'critic': CriticAgent(seed=seed + 30),
        'animator': AnimatorAgent(seed=seed + 40)
    }


def demo_agents():
    """Demonstrate agent capabilities"""
    print("=" * 70)
    print("SWARM AGENTS DEMO")
    print("=" * 70)
    
    # Create swarm
    swarm = create_agent_swarm(seed=42)
    
    # Test context
    test_context = {
        'actual_age': 25,
        'gender': 'male',
        'social_class': 'middle',
        'height_category': 'average',
        'skin_color': (200, 150, 100),
        'hair_color': (60, 40, 20),
        'proposed_params': {
            'actual_age': 25,
            'gender': 'male',
            'social_class': 'middle',
            'bmi': 24.5,
            'height_category': 'average'
        },
        'body_metrics': {
            'actual_age': 25,
            'body_type_display': 'average',
            'weight_pounds': 165
        }
    }
    
    print("\n1. Body Agent - Anatomical Decisions")
    print("-" * 40)
    body_decision = swarm['body'].decide(test_context)
    print(f"   Decision: {body_decision.reasoning}")
    print(f"   Values: BMI={body_decision.values[0]:.1f}, Confidence={body_decision.confidence:.2f}")
    
    print("\n2. Style Agent - Aesthetic Decisions")
    print("-" * 40)
    style_decision = swarm['style'].decide(test_context)
    print(f"   Decision: {style_decision.reasoning}")
    print(f"   Values: Hue={style_decision.values[0]:.2f}, Sat={style_decision.values[1]:.2f}")
    
    print("\n3. Diversity Agent - Novelty Assessment")
    print("-" * 40)
    diversity_decision = swarm['diversity'].decide(test_context)
    print(f"   Decision: {diversity_decision.reasoning}")
    print(f"   Novelty Score: {diversity_decision.values[0]:.3f}")
    
    # Record some generations
    for _ in range(10):
        test_params = {
            'actual_age': random.randint(13, 85),
            'gender': random.choice(['male', 'female']),
            'social_class': random.choice(['poor', 'working', 'middle', 'upper', 'rich']),
            'bmi': random.uniform(15, 35),
            'height_category': random.choice(['very_short', 'short', 'average', 'tall', 'very_tall'])
        }
        swarm['diversity'].record_generation(test_params)
    
    coverage = swarm['diversity'].get_coverage_stats()
    print(f"   Coverage: {coverage['coverage_ratio']:.2%}, Entropy: {coverage['entropy']:.3f}")
    
    print("\n4. Critic Agent - Validation")
    print("-" * 40)
    critic_decision = swarm['critic'].decide(test_context)
    print(f"   Decision: {critic_decision.reasoning}")
    print(f"   Approved: {critic_decision.metadata['approved']}")
    
    print("\n5. Animator Agent - Motion")
    print("-" * 40)
    anim_context = {**test_context, 'animation_type': 'walk'}
    anim_decision = swarm['animator'].decide_frame(anim_context, 3, 8)
    print(f"   Decision: {anim_decision.reasoning}")
    print(f"   Offsets: body_y={anim_decision.values[0]:.3f}")
    
    print("\n6. Performance Summary")
    print("-" * 40)
    for name, agent in swarm.items():
        perf = agent.get_performance()
        print(f"   {name:12s}: {perf['total_decisions']:3d} decisions, "
              f"{perf['accuracy']:.1%} success rate")
    
    print("\n" + "=" * 70)
    print("AGENT DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demo_agents()
