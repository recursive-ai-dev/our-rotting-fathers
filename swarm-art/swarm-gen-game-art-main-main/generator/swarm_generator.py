#!/usr/bin/env python3
"""
Swarm Character Generator - Integration layer for GeneSwarm
Connects the multi-agent swarm to the existing character generation pipeline.
"""

import numpy as np
import random
from typing import Dict, List, Tuple, Optional, Any
from PIL import Image
import os
import json
import time
import copy

from .pure_generator import PureCharacterGenerator
from .mass_generator import MassCharacterGenerator
from .swarm.orchestrator import SwarmOrchestrator, SwarmGeneration
from .swarm.memory import SwarmMemory, MemoryEntry, TransferLearningBuffer
from .swarm.agents import AnimatorAgent

class SwarmCharacterGenerator(MassCharacterGenerator):
    """
    Character generator powered by nano-tensor agent swarm.
    Extends the mass generator with swarm-based decision making.
    """
    
    def __init__(self, canvas_size: Tuple[int, int] = (32, 32), 
                 master_seed: int = 42, use_swarm: bool = True,
                 deterministic_replay: bool = True):
        super().__init__(canvas_size=canvas_size)
        
        self.use_swarm = use_swarm
        self.master_seed = master_seed
        self.deterministic_replay = deterministic_replay
        self._seed_replay_cache: Dict[int, Dict[str, Any]] = {}
        
        # Initialize swarm
        if use_swarm:
            self.orchestrator = SwarmOrchestrator(master_seed=master_seed)
            self.memory = SwarmMemory(embedding_dim=16, max_size=5000)
            self.transfer_buffer = TransferLearningBuffer(capacity=1000)
        else:
            self.orchestrator = None
            self.memory = None
            self.transfer_buffer = None
        
        # Statistics
        self.swarm_stats = {
            'swarm_generations': 0,
            'consensus_approvals': 0,
            'memory_queries': 0,
            'learning_feedback_count': 0,
            'replay_hits': 0
        }
    
    def generate_swarm_params(self, seed: Optional[int] = None) -> Dict:
        """Generate parameters through swarm consensus"""
        if not self.use_swarm or self.orchestrator is None:
            # Fall back to original method
            return self._generate_random_params(seed)
        
        if seed is not None and self.deterministic_replay and seed in self._seed_replay_cache:
            self.swarm_stats['replay_hits'] += 1
            return copy.deepcopy(self._seed_replay_cache[seed])
        
        # Generate through swarm
        generation = self.orchestrator.generate_character(base_seed=seed)
        self.swarm_stats['swarm_generations'] += 1
        
        if generation.consensus.approved:
            self.swarm_stats['consensus_approvals'] += 1
        
        # Merge swarm params with complete parameter set.
        # Seed-scoped completion keeps params deterministic per generation.
        params = self._with_seed_scope(
            generation.seed,
            lambda: self._complete_params(generation.params)
        )
        
        # Add swarm metadata
        params['_swarm'] = {
            'generation_id': generation.generation_id,
            'seed': generation.seed,
            'consensus_confidence': generation.consensus.confidence,
            'iterations': generation.consensus.iterations,
            'approved': generation.consensus.approved,
            'agent_votes': generation.consensus.agent_votes
        }
        
        # Store in memory
        if self.memory is not None:
            embedding = self.memory.compute_embedding(params)
            entry = MemoryEntry(
                embedding=embedding,
                params={k: v for k, v in params.items() if not k.startswith('_')},
                score=generation.consensus.confidence,
                timestamp=generation.consensus.timestamp,
                agent_contributions=generation.consensus.agent_votes,
                generation_id=generation.generation_id
            )
            self.memory.insert(entry)
        
        if seed is not None and self.deterministic_replay:
            self._seed_replay_cache[seed] = copy.deepcopy(params)
        
        return params
    
    def _generate_random_params(self, seed: Optional[int] = None) -> Dict:
        """Generate random parameters (fallback)"""
        def build_params() -> Dict:
            gender = random.choice(['male', 'female'])
            social_class = random.choice(['poor', 'working', 'middle', 'upper', 'rich'])
            
            # Age
            age_category, actual_age = self._generate_age_category()
            
            # Body metrics
            height_category, body_type_category, body_metrics = \
                self._generate_realistic_body_metrics(gender, social_class, age_category, actual_age)
            
            return {
                'gender': gender,
                'social_class': social_class,
                'age_category': age_category,
                'actual_age': actual_age,
                'height_category': height_category,
                'weight_category': body_type_category,
                'body_metrics': body_metrics,
                'skin_color': random.choice(self.palette.skin_tones),
                'hair_color': random.choice(self.palette.hair_colors),
                'eye_color': random.choice(self.palette.eye_colors),
                'clothing': self._choose_clothing(social_class, gender),
                'hair_style': self._choose_hair_style(gender, social_class),
                'face_style': random.choice(['basic', 'detailed', 'minimal']),
                'body_type': random.choice(['slim', 'average', 'broad', 'curvy']),
                'has_glasses': random.random() < 0.2,
                'has_jewelry': random.random() < (0.1 if social_class == 'poor' else 0.6),
                'has_facial_hair': gender == 'male' and random.random() < 0.3,
                'beard_type': random.choice(['mustache', 'goatee', 'full_beard', 'stubble']),
                'has_hat': random.random() < 0.05,
                'hat_style': random.choice(['simple', 'baseball_cap']),
            }
        
        return self._with_seed_scope(seed, build_params)
    
    def _complete_params(self, partial_params: Dict) -> Dict:
        """Complete partial params from swarm with additional attributes"""
        # Get base params
        gender = partial_params.get('gender', random.choice(['male', 'female']))
        social_class = partial_params.get('social_class', 'middle')
        actual_age = partial_params.get('actual_age', 30)
        age_category = partial_params.get('age_category', 'young_adult')
        
        # Get body metrics
        height_category = partial_params.get('height_category', 'average')
        _, body_type_category, body_metrics = \
            self._generate_realistic_body_metrics(gender, social_class, age_category, actual_age)
        
        # Override BMI if swarm provided it
        if 'bmi' in partial_params:
            body_metrics['bmi'] = partial_params['bmi']
            # Recalculate weight from BMI
            height_inches = body_metrics['height_inches']
            body_metrics['weight_pounds'] = int((partial_params['bmi'] * (height_inches ** 2)) / 703)
            body_metrics['weight_display'] = f"{body_metrics['weight_pounds']} lbs"
            body_metrics['bmi_display'] = f"BMI {partial_params['bmi']:.1f}"
        
        return {
            'gender': gender,
            'social_class': social_class,
            'age_category': age_category,
            'actual_age': actual_age,
            'height_category': height_category,
            'weight_category': body_type_category,
            'body_metrics': body_metrics,
            'skin_color': partial_params.get('skin_color', random.choice(self.palette.skin_tones)),
            'hair_color': partial_params.get('hair_color', random.choice(self.palette.hair_colors)),
            'eye_color': partial_params.get('eye_color', random.choice(self.palette.eye_colors)),
            'clothing': partial_params.get('clothing', self._choose_clothing(social_class, gender)),
            'hair_style': partial_params.get('hair_style', self._choose_hair_style(gender, social_class)),
            'face_style': partial_params.get('face_style', random.choice(['basic', 'detailed', 'minimal'])),
            'body_type': partial_params.get('body_type', random.choice(['slim', 'average', 'broad', 'curvy'])),
            'has_glasses': partial_params.get('has_glasses', random.random() < 0.2),
            'has_jewelry': partial_params.get('has_jewelry', random.random() < (0.1 if social_class == 'poor' else 0.6)),
            'has_facial_hair': partial_params.get('has_facial_hair', gender == 'male' and random.random() < 0.3),
            'beard_type': partial_params.get('beard_type', random.choice(['mustache', 'goatee', 'full_beard', 'stubble'])),
            'has_hat': partial_params.get('has_hat', random.random() < 0.05),
            'hat_style': partial_params.get('hat_style', random.choice(['simple', 'baseball_cap'])),
        }

    def _with_seed_scope(self, seed: Optional[int], fn):
        """
        Run a function with deterministic RNG state scoped to this call.
        Restores global RNG state afterward.
        """
        if seed is None:
            return fn()
        
        state = random.getstate()
        random.seed(seed)
        try:
            return fn()
        finally:
            random.setstate(state)
    
    def generate_character(self, seed: Optional[int] = None) -> Image.Image:
        """Generate a single character using swarm (if enabled)"""
        if self.use_swarm:
            params = self.generate_swarm_params(seed)
        else:
            params = self._with_seed_scope(seed, self._generate_character_params)
        
        return self._render_character_with_params(params)
    
    def generate_swarm_batch(self, count: int, output_dir: str = "swarm_output/",
                            progress_callback=None, save_metadata: bool = True) -> List[str]:
        """Generate batch using swarm consensus"""
        os.makedirs(output_dir, exist_ok=True)
        
        if save_metadata:
            metadata_dir = os.path.join(output_dir, "metadata")
            os.makedirs(metadata_dir, exist_ok=True)
        
        generated_files = []
        start_time = time.time()
        
        print(f"🐝 Starting Swarm Generation: {count} characters")
        print(f"   Canvas: {self.canvas_size[0]}x{self.canvas_size[1]}")
        print(f"   Swarm: {'ENABLED' if self.use_swarm else 'DISABLED'}")
        print()
        
        for i in range(count):
            # Generate through swarm
            params = self.generate_swarm_params(seed=self.master_seed + i)
            
            # Render
            sprite = self._render_character_with_params(params)
            
            # Check uniqueness
            sprite_hash = self.calculate_sprite_hash(sprite)
            if sprite_hash in self.generated_hashes:
                self.generation_stats['duplicates_avoided'] += 1
                continue
            
            self.generated_hashes.add(sprite_hash)
            
            # Save
            filename = f"swarm_char_{len(generated_files):06d}.png"
            filepath = os.path.join(output_dir, filename)
            sprite.save(filepath, "PNG")
            generated_files.append(filepath)
            
            # Update stats
            self.generation_stats['total_generated'] += 1
            self.generation_stats['unique_count'] += 1
            self.generation_stats['by_gender'][params['gender']] += 1
            self.generation_stats['by_social_class'][params['social_class']] += 1
            
            # Progress
            if progress_callback and i % 10 == 0:
                progress_callback(i, count, (i/count)*100, 0, time.time()-start_time)
            elif i % 50 == 0:
                print(f"   Generated {i+1}/{count}...")
            
            # Save metadata periodically
            if save_metadata and len(generated_files) % 100 == 0:
                self._save_swarm_metadata(metadata_dir, len(generated_files))
        
        # Final report
        self._print_swarm_report(len(generated_files), time.time() - start_time, output_dir)
        
        if save_metadata:
            self._save_swarm_metadata(metadata_dir, len(generated_files), final=True)
        
        return generated_files
    
    def _save_swarm_metadata(self, metadata_dir: str, count: int, final: bool = False):
        """Save swarm-specific metadata"""
        metadata = {
            'timestamp': time.time(),
            'characters_generated': count,
            'swarm_enabled': self.use_swarm,
            'deterministic_replay': self.deterministic_replay,
            'canvas_size': self.canvas_size,
            'swarm_stats': self.swarm_stats
        }
        
        if self.use_swarm and self.orchestrator:
            metadata['orchestrator_stats'] = self.orchestrator.get_stats()
        
        if self.memory:
            metadata['memory_stats'] = self.memory.get_stats()
        
        suffix = "final" if final else f"batch_{count:05d}"
        filepath = os.path.join(metadata_dir, f"swarm_metadata_{suffix}.json")
        
        with open(filepath, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
    
    def _print_swarm_report(self, generated: int, total_time: float, output_dir: str):
        """Print swarm generation report"""
        rate = generated / total_time if total_time > 0 else 0
        
        print(f"\n🎉 SWARM GENERATION COMPLETE!")
        print("=" * 60)
        print(f"✅ Characters: {generated:,}")
        print(f"⏱️  Time: {total_time:.2f}s ({rate:.1f}/sec)")
        print(f"📁 Output: {output_dir}")
        
        if self.use_swarm:
            print(f"\n🐝 Swarm Stats:")
            print(f"   Generations: {self.swarm_stats['swarm_generations']}")
            print(f"   Approvals: {self.swarm_stats['consensus_approvals']}")
            print(f"   Approval rate: {self.swarm_stats['consensus_approvals']/max(1,self.swarm_stats['swarm_generations']):.1%}")
            
            if self.orchestrator:
                orch_stats = self.orchestrator.get_stats()
                print(f"\n📊 Agent Performance:")
                for name, perf in orch_stats['agent_performance'].items():
                    if perf['total_decisions'] > 0:
                        print(f"   {name}: {perf['accuracy']:.1%} accuracy")
        
        if self.memory:
            mem_stats = self.memory.get_stats()
            print(f"\n💾 Memory:")
            print(f"   Entries: {mem_stats['total_entries']}")
            print(f"   Avg score: {mem_stats['average_score']:.2f}")
    
    def provide_feedback(self, generation_id: str, quality_score: float,
                        user_notes: str = ""):
        """
        Provide learning feedback for swarm.
        quality_score: 0.0 (terrible) to 1.0 (perfect)
        """
        if not self.use_swarm or not self.orchestrator:
            return
        
        self.orchestrator.provide_feedback(generation_id, quality_score)
        self.swarm_stats['learning_feedback_count'] += 1
        
        # Store in transfer buffer
        if self.transfer_buffer and self.memory:
            # Find entry
            entry = self.memory.entries.get(generation_id)
            if entry:
                self.transfer_buffer.add(
                    entry.params,
                    entry.embedding,
                    quality_score,
                    entry.agent_contributions
                )
    
    def get_similar_characters(self, params: Dict, k: int = 5) -> List[Dict]:
        """Query memory for similar characters"""
        if not self.memory:
            return []
        
        self.swarm_stats['memory_queries'] += 1
        entries = self.memory.query_similar(params, k=k)
        return [e.params for e in entries]
    
    def save_swarm_state(self, filepath: str):
        """Save complete swarm state"""
        if self.orchestrator:
            self.orchestrator.save_state(filepath)
        if self.memory:
            mem_path = filepath.replace('.json', '_memory.json')
            self.memory.save(mem_path)
    
    def load_swarm_state(self, filepath: str):
        """Load swarm state"""
        if self.orchestrator:
            self.orchestrator.load_state(filepath)
        if self.memory:
            mem_path = filepath.replace('.json', '_memory.json')
            if os.path.exists(mem_path):
                self.memory.load(mem_path)


def demo_swarm_generator():
    """Demonstrate swarm generator"""
    print("=" * 70)
    print("SWARM CHARACTER GENERATOR DEMO")
    print("=" * 70)
    
    # Create generator with swarm
    print("\n1. Creating Swarm Generator (64x64)...")
    gen = SwarmCharacterGenerator(
        canvas_size=(64, 64),
        master_seed=42,
        use_swarm=True
    )
    
    print("   ✓ Swarm initialized")
    print(f"   ✓ Canvas: {gen.canvas_size}")
    print(f"   ✓ Agents: {list(gen.orchestrator.agents.keys())}")
    
    # Generate characters
    print("\n2. Generating 5 characters through swarm consensus...")
    print("-" * 70)
    
    for i in range(5):
        params = gen.generate_swarm_params(seed=1000 + i)
        swarm_meta = params.get('_swarm', {})
        
        print(f"\n   Character {i+1}:")
        print(f"     ID: {swarm_meta.get('generation_id', 'N/A')}")
        print(f"     {params['gender']}, {params['actual_age']}yo, {params['social_class']}")
        print(f"     BMI: {params['body_metrics']['bmi']:.1f}")
        print(f"     Consensus: {swarm_meta.get('consensus_confidence', 0):.2f} "
              f"({swarm_meta.get('iterations', 0)} iterations)")
        print(f"     Approved: {swarm_meta.get('approved', False)}")
    
    # Generate sprites
    print("\n3. Rendering sprites...")
    print("-" * 70)
    
    import os
    os.makedirs("swarm_demo", exist_ok=True)
    
    for i in range(3):
        sprite = gen.generate_character(seed=2000 + i)
        sprite.save(f"swarm_demo/character_{i}.png", "PNG")
        print(f"   Saved: swarm_demo/character_{i}.png")
    
    # Memory query
    print("\n4. Memory query (finding similar characters)...")
    print("-" * 70)
    
    query = {
        'gender': 'male',
        'social_class': 'middle',
        'actual_age': 30,
        'bmi': 24.0
    }
    similar = gen.get_similar_characters(query, k=3)
    print(f"   Query: {query}")
    print(f"   Found {len(similar)} similar in memory")
    
    # Statistics
    print("\n5. Swarm Statistics...")
    print("-" * 70)
    stats = gen.swarm_stats
    print(f"   Generations: {stats['swarm_generations']}")
    print(f"   Approvals: {stats['consensus_approvals']}")
    print(f"   Memory queries: {stats['memory_queries']}")
    
    orch_stats = gen.orchestrator.get_stats()
    print(f"\n   Agent Performance:")
    for name, perf in orch_stats['agent_performance'].items():
        print(f"     {name:12s}: {perf['total_decisions']:3d} decisions, "
              f"{perf['accuracy']:.1%} accuracy")
    
    # Learning feedback
    print("\n6. Simulating learning feedback...")
    print("-" * 70)
    
    for gen_id in ["swarm_000000", "swarm_000001", "swarm_000002"]:
        feedback = 0.7 + np.random.random() * 0.3
        gen.provide_feedback(gen_id, feedback)
        print(f"   Feedback for {gen_id}: {feedback:.2f}")
    
    print(f"\n   Total feedback provided: {gen.swarm_stats['learning_feedback_count']}")
    
    # Save state
    print("\n7. Saving swarm state...")
    print("-" * 70)
    gen.save_swarm_state("swarm_demo/swarm_state.json")
    print("   Saved: swarm_demo/swarm_state.json")
    print("   Saved: swarm_demo/swarm_state_memory.json")
    
    print("\n" + "=" * 70)
    print("SWARM GENERATOR DEMO COMPLETE")
    print("=" * 70)
    print("\nThe swarm has:")
    print("  - 5 specialized nano-tensor agents (<512 params each)")
    print("  - Consensus-based decision making")
    print("  - Memory with embedding-based similarity search")
    print("  - Online learning from feedback")
    print("  - Deterministic generation with seed chaining")


if __name__ == "__main__":
    demo_swarm_generator()
