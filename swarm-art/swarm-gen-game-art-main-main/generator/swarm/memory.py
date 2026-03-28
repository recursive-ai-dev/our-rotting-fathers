#!/usr/bin/env python3
"""
Swarm Memory - Embedding store and retrieval for learned patterns
Tiny vector database for agent experience and successful patterns.
"""

import numpy as np
import random
import time
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, asdict
from collections import deque, defaultdict
import json
import hashlib
from heapq import nlargest, nsmallest

@dataclass
class MemoryEntry:
    """Single memory entry with metadata"""
    embedding: np.ndarray
    params: Dict[str, Any]
    score: float  # Quality score (0-1)
    timestamp: float
    agent_contributions: Dict[str, float]  # Which agents contributed
    generation_id: str
    
    def to_dict(self) -> Dict:
        return {
            'embedding': self.embedding.tolist(),
            'params': self.params,
            'score': self.score,
            'timestamp': self.timestamp,
            'agent_contributions': self.agent_contributions,
            'generation_id': self.generation_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryEntry':
        return cls(
            embedding=np.array(data['embedding']),
            params=data['params'],
            score=data['score'],
            timestamp=data['timestamp'],
            agent_contributions=data['agent_contributions'],
            generation_id=data['generation_id']
        )

class VectorIndex:
    """
    Simple vector similarity index using cosine similarity.
    Optimized for small collections (<100k entries).
    """
    
    def __init__(self, dim: int, metric: str = 'cosine'):
        self.dim = dim
        self.metric = metric
        self.vectors = []  # List of (id, vector) tuples
        self.id_to_idx = {}
        
    def add(self, id: str, vector: np.ndarray):
        """Add vector to index"""
        vector = vector.flatten()
        if len(vector) != self.dim:
            raise ValueError(f"Expected dim {self.dim}, got {len(vector)}")
        
        idx = len(self.vectors)
        self.vectors.append((id, vector))
        self.id_to_idx[id] = idx
    
    def remove(self, id: str):
        """Remove vector from index"""
        if id in self.id_to_idx:
            idx = self.id_to_idx[id]
            # Mark as deleted (None)
            self.vectors[idx] = (None, None)
            del self.id_to_idx[id]
    
    def search(self, query: np.ndarray, k: int = 5) -> List[Tuple[str, float]]:
        """Search for k nearest neighbors"""
        query = query.flatten()
        
        if self.metric == 'cosine':
            query_norm = query / (np.linalg.norm(query) + 1e-8)
        else:
            query_norm = query
        
        scores = []
        for id, vector in self.vectors:
            if id is None:
                continue
            
            if self.metric == 'cosine':
                vec_norm = vector / (np.linalg.norm(vector) + 1e-8)
                score = np.dot(query_norm, vec_norm)
            elif self.metric == 'euclidean':
                score = -np.linalg.norm(query_norm - vector)
            else:
                score = -np.linalg.norm(query_norm - vector)
            
            scores.append((id, score))
        
        # Return top k
        return nlargest(k, scores, key=lambda x: x[1])
    
    def search_batch(self, queries: np.ndarray, k: int = 5) -> List[List[Tuple[str, float]]]:
        """Batch search"""
        return [self.search(q, k) for q in queries]


class SwarmMemory:
    """
    Memory system for the swarm.
    Stores successful generations, enables pattern retrieval and transfer learning.
    """
    
    def __init__(self, embedding_dim: int = 16, max_size: int = 10000):
        self.embedding_dim = embedding_dim
        self.max_size = max_size
        
        # Memory storage
        self.entries: Dict[str, MemoryEntry] = {}
        self.entry_order = deque(maxlen=max_size)  # For LRU eviction
        
        # Vector indices
        self.embedding_index = VectorIndex(embedding_dim, metric='cosine')
        
        # Categorical indices for fast filtering
        self.gender_index = defaultdict(list)  # gender -> entry_ids
        self.class_index = defaultdict(list)   # social_class -> entry_ids
        self.age_index = defaultdict(list)     # age_category -> entry_ids
        
        # Statistics
        self.total_inserts = 0
        self.total_queries = 0
        self.cache_hits = 0
        
        # Pattern summaries
        self.pattern_clusters = {}
        self.success_patterns = defaultdict(float)
    
    def compute_embedding(self, params: Dict[str, Any]) -> np.ndarray:
        """
        Compute normalized embedding vector from parameters.
        Deterministic and consistent.
        """
        features = []
        
        # Core features (normalized to 0-1)
        age = params.get('actual_age', 30)
        features.append((age - 13) / 72)  # 13-85 range
        
        gender = 1.0 if params.get('gender') == 'male' else 0.0
        features.append(gender)
        
        class_map = {'poor': 0.0, 'working': 0.25, 'middle': 0.5, 'upper': 0.75, 'rich': 1.0}
        features.append(class_map.get(params.get('social_class'), 0.5))
        
        body_metrics = params.get('body_metrics', {})
        if not isinstance(body_metrics, dict):
            body_metrics = {}
        bmi = params.get('bmi', body_metrics.get('bmi', 25))
        features.append((bmi - 13) / 27)  # 13-40 range
        
        # Color features (if present)
        skin = params.get('skin_color', (128, 128, 128))
        features.append(skin[0] / 255 if isinstance(skin, (list, tuple)) else 0.5)
        features.append(skin[1] / 255 if isinstance(skin, (list, tuple)) else 0.5)
        
        # Random/diversity features
        features.append(params.get('exploration_factor', 0.5))
        features.append(params.get('style_confidence', 0.5))
        
        # Pad or trim to embedding_dim
        while len(features) < self.embedding_dim:
            features.append(0.5)
        features = features[:self.embedding_dim]
        
        embedding = np.array(features, dtype=np.float32)
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def insert(self, entry: MemoryEntry) -> str:
        """Insert entry into memory"""
        entry_id = entry.generation_id
        
        # Check if exists
        if entry_id in self.entries:
            # Update
            self.entries[entry_id] = entry
            self.entry_order.remove(entry_id)
            self.entry_order.append(entry_id)
            return entry_id
        
        # Evict if at capacity
        if len(self.entries) >= self.max_size:
            self._evict_oldest()
        
        # Store entry
        self.entries[entry_id] = entry
        self.entry_order.append(entry_id)
        self.total_inserts += 1
        
        # Update indices
        self.embedding_index.add(entry_id, entry.embedding)
        
        # Update categorical indices
        gender = entry.params.get('gender', 'unknown')
        social_class = entry.params.get('social_class', 'unknown')
        age_cat = entry.params.get('age_category', 'unknown')
        
        self.gender_index[gender].append(entry_id)
        self.class_index[social_class].append(entry_id)
        self.age_index[age_cat].append(entry_id)
        
        # Update pattern summaries
        self._update_patterns(entry)
        
        return entry_id
    
    def _evict_oldest(self):
        """Evict oldest entry (LRU)"""
        if not self.entry_order:
            return
        
        oldest_id = self.entry_order.popleft()
        if oldest_id in self.entries:
            entry = self.entries[oldest_id]
            
            # Remove from indices
            self.embedding_index.remove(oldest_id)
            
            # Remove from categorical indices
            gender = entry.params.get('gender')
            social_class = entry.params.get('social_class')
            age_cat = entry.params.get('age_category')
            
            if gender and oldest_id in self.gender_index[gender]:
                self.gender_index[gender].remove(oldest_id)
            if social_class and oldest_id in self.class_index[social_class]:
                self.class_index[social_class].remove(oldest_id)
            if age_cat and oldest_id in self.age_index[age_cat]:
                self.age_index[age_cat].remove(oldest_id)
            
            del self.entries[oldest_id]
    
    def _update_patterns(self, entry: MemoryEntry):
        """Update pattern summaries from entry"""
        # Extract key patterns
        patterns = []
        
        # Body type pattern
        body_metrics = entry.params.get('body_metrics', {})
        if not isinstance(body_metrics, dict):
            body_metrics = {}
        bmi = entry.params.get('bmi', body_metrics.get('bmi', 25))
        age = entry.params.get('actual_age', 30)
        bmi_age_pattern = f"bmi_{self._discretize(bmi, 15, 35, 4)}_age_{self._discretize(age, 13, 85, 4)}"
        patterns.append(bmi_age_pattern)
        
        # Class-gender pattern
        gender = entry.params.get('gender')
        social_class = entry.params.get('social_class')
        patterns.append(f"{gender}_{social_class}")
        
        # Update success scores
        for pattern in patterns:
            # Exponential moving average
            alpha = 0.1
            old_score = self.success_patterns[pattern]
            self.success_patterns[pattern] = (1 - alpha) * old_score + alpha * entry.score
    
    def _discretize(self, value: float, min_val: float, max_val: float, bins: int) -> int:
        """Discretize continuous value"""
        normalized = (value - min_val) / (max_val - min_val)
        bin_idx = int(normalized * bins)
        return max(0, min(bins - 1, bin_idx))
    
    def query_similar(self, params: Dict[str, Any], k: int = 5,
                     filters: Optional[Dict[str, Any]] = None) -> List[MemoryEntry]:
        """
        Query memory for similar entries.
        Optional filters: {'gender': 'male', 'social_class': 'middle'}
        """
        self.total_queries += 1
        
        # Compute query embedding
        query_emb = self.compute_embedding(params)
        
        # Search index
        results = self.embedding_index.search(query_emb, k=k*2)  # Get more for filtering
        
        # Apply filters and fetch entries
        entries = []
        for entry_id, score in results:
            if entry_id not in self.entries:
                continue
            
            entry = self.entries[entry_id]
            
            # Apply filters
            if filters:
                match = True
                for key, value in filters.items():
                    if entry.params.get(key) != value:
                        match = False
                        break
                if not match:
                    continue
            
            entries.append(entry)
            
            if len(entries) >= k:
                break
        
        if entries:
            self.cache_hits += 1
        
        return entries
    
    def query_by_pattern(self, pattern_type: str, min_score: float = 0.6) -> List[MemoryEntry]:
        """Query entries matching a successful pattern"""
        # Find matching pattern keys
        matching_patterns = [
            p for p, score in self.success_patterns.items()
            if score >= min_score and pattern_type in p
        ]
        
        if not matching_patterns:
            return []
        
        # Get best pattern
        best_pattern = max(matching_patterns, key=lambda p: self.success_patterns[p])
        
        # Find entries matching this pattern
        # (Simplified - in practice would index patterns)
        results = []
        for entry in self.entries.values():
            if entry.score >= min_score:
                results.append(entry)
        
        return sorted(results, key=lambda e: e.score, reverse=True)[:10]
    
    def get_prototype(self, category: str, key: str) -> Optional[Dict]:
        """
        Get prototype (average) parameters for a category.
        E.g., get_prototype('gender', 'male') -> avg male params
        """
        if category == 'gender':
            entry_ids = self.gender_index.get(key, [])
        elif category == 'social_class':
            entry_ids = self.class_index.get(key, [])
        elif category == 'age_category':
            entry_ids = self.age_index.get(key, [])
        else:
            return None
        
        if not entry_ids:
            return None
        
        # Compute average
        prototype = defaultdict(list)
        for entry_id in entry_ids:
            if entry_id in self.entries:
                entry = self.entries[entry_id]
                for key, value in entry.params.items():
                    if isinstance(value, (int, float)):
                        prototype[key].append(value)
        
        # Average numeric values
        result = {}
        for key, values in prototype.items():
            if values:
                result[key] = np.mean(values)
        
        return result
    
    def get_stats(self) -> Dict:
        """Get memory statistics"""
        if self.total_queries > 0:
            hit_rate = self.cache_hits / self.total_queries
        else:
            hit_rate = 0.0
        
        # Score distribution
        scores = [e.score for e in self.entries.values()]
        avg_score = np.mean(scores) if scores else 0.0
        
        # Top patterns
        top_patterns = sorted(
            self.success_patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            'total_entries': len(self.entries),
            'max_size': self.max_size,
            'total_inserts': self.total_inserts,
            'total_queries': self.total_queries,
            'cache_hit_rate': hit_rate,
            'average_score': avg_score,
            'top_patterns': top_patterns
        }
    
    def save(self, filepath: str):
        """Save memory to disk"""
        data = {
            'embedding_dim': self.embedding_dim,
            'max_size': self.max_size,
            'entries': [e.to_dict() for e in self.entries.values()],
            'stats': self.get_stats(),
            'success_patterns': dict(self.success_patterns)
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self, filepath: str):
        """Load memory from disk"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.embedding_dim = data['embedding_dim']
        self.max_size = data['max_size']
        self.success_patterns = defaultdict(float, data.get('success_patterns', {}))
        
        # Rebuild indices
        self.entries = {}
        self.entry_order = deque(maxlen=self.max_size)
        self.embedding_index = VectorIndex(self.embedding_dim)
        self.gender_index = defaultdict(list)
        self.class_index = defaultdict(list)
        self.age_index = defaultdict(list)
        
        for entry_dict in data['entries']:
            entry = MemoryEntry.from_dict(entry_dict)
            self.insert(entry)


class TransferLearningBuffer:
    """
    Buffer for transfer learning between agents.
    Collects high-quality examples for batch training.
    """
    
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
        self.priority_scores = deque(maxlen=capacity)
    
    def add(self, params: Dict, embedding: np.ndarray, score: float,
           agent_feedback: Dict[str, float]):
        """Add example to buffer"""
        item = {
            'params': params,
            'embedding': embedding,
            'score': score,
            'agent_feedback': agent_feedback
        }
        
        # Priority based on score and novelty
        priority = score + np.random.random() * 0.1
        
        self.buffer.append(item)
        self.priority_scores.append(priority)
    
    def sample(self, batch_size: int = 32, strategy: str = 'priority') -> List[Dict]:
        """Sample batch for training"""
        if not self.buffer:
            return []
        
        if strategy == 'random':
            indices = np.random.choice(len(self.buffer), 
                                      min(batch_size, len(self.buffer)),
                                      replace=False)
        elif strategy == 'priority':
            # Sample by priority
            probs = np.array(self.priority_scores) / sum(self.priority_scores)
            indices = np.random.choice(len(self.buffer),
                                      min(batch_size, len(self.buffer)),
                                      replace=False,
                                      p=probs)
        else:
            indices = range(min(batch_size, len(self.buffer)))
        
        return [self.buffer[i] for i in indices]
    
    def get_high_quality_examples(self, threshold: float = 0.8) -> List[Dict]:
        """Get examples above quality threshold"""
        return [item for item in self.buffer if item['score'] >= threshold]
    
    def clear(self):
        """Clear buffer"""
        self.buffer.clear()
        self.priority_scores.clear()


def demo_memory():
    """Demonstrate memory system"""
    print("=" * 70)
    print("SWARM MEMORY DEMO")
    print("=" * 70)
    
    # Create memory
    memory = SwarmMemory(embedding_dim=16, max_size=100)
    
    print("\n1. Inserting 20 sample entries...")
    print("-" * 70)
    
    for i in range(20):
        params = {
            'gender': random.choice(['male', 'female']),
            'social_class': random.choice(['poor', 'working', 'middle', 'upper', 'rich']),
            'actual_age': random.randint(13, 85),
            'bmi': random.uniform(16, 35),
            'age_category': random.choice(['teenager', 'young_adult', 'middle_aged', 'older_adult', 'elderly'])
        }
        
        emb = memory.compute_embedding(params)
        entry = MemoryEntry(
            embedding=emb,
            params=params,
            score=random.uniform(0.5, 1.0),
            timestamp=time.time(),
            agent_contributions={'body': 0.8, 'style': 0.7},
            generation_id=f"gen_{i:04d}"
        )
        
        memory.insert(entry)
    
    print(f"   Inserted: {memory.total_inserts}")
    print(f"   Current size: {len(memory.entries)}")
    
    print("\n2. Querying similar entries...")
    print("-" * 70)
    
    query_params = {
        'gender': 'male',
        'social_class': 'middle',
        'actual_age': 30,
        'bmi': 24.5
    }
    
    similar = memory.query_similar(query_params, k=3)
    print(f"   Query: {query_params}")
    print(f"   Found {len(similar)} similar entries:")
    for entry in similar:
        print(f"     - {entry.generation_id}: {entry.params['gender']} "
              f"{entry.params['social_class']}, age={entry.params['actual_age']}, "
              f"score={entry.score:.2f}")
    
    print("\n3. Filtered query (only male)...")
    print("-" * 70)
    male_similar = memory.query_similar(query_params, k=3, filters={'gender': 'male'})
    print(f"   Found {len(male_similar)} male entries")
    
    print("\n4. Getting prototype...")
    print("-" * 70)
    male_proto = memory.get_prototype('gender', 'male')
    if male_proto:
        print(f"   Male prototype: avg_age={male_proto.get('actual_age', 0):.1f}, "
              f"avg_bmi={male_proto.get('bmi', 0):.1f}")
    
    print("\n5. Memory statistics...")
    print("-" * 70)
    stats = memory.get_stats()
    print(f"   Total entries: {stats['total_entries']}")
    print(f"   Cache hit rate: {stats['cache_hit_rate']:.1%}")
    print(f"   Average score: {stats['average_score']:.2f}")
    print(f"   Top patterns: {stats['top_patterns'][:3]}")
    
    print("\n6. Transfer learning buffer...")
    print("-" * 70)
    
    buffer = TransferLearningBuffer(capacity=50)
    for entry in memory.entries.values():
        buffer.add(entry.params, entry.embedding, entry.score, entry.agent_contributions)
    
    sample = buffer.sample(batch_size=5, strategy='priority')
    print(f"   Buffer size: {len(buffer.buffer)}")
    print(f"   Sampled {len(sample)} examples for training")
    
    high_quality = buffer.get_high_quality_examples(threshold=0.85)
    print(f"   High quality examples (score>=0.85): {len(high_quality)}")
    
    print("\n" + "=" * 70)
    print("MEMORY DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    import time
    demo_memory()
