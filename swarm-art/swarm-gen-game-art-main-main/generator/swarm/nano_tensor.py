#!/usr/bin/env python3
"""
Nano-Tensor Framework - Minimal Neural Network for Swarm Agents
Ultra-lightweight (<1KB per agent), deterministic, seed-based initialization.
"""

import numpy as np
import hashlib
import json
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, asdict
from collections import deque

@dataclass
class NanoTensorConfig:
    """Configuration for nano-tensor network"""
    input_dim: int = 8
    hidden_dim: int = 16
    output_dim: int = 4
    learning_rate: float = 0.01
    activation: str = 'relu'  # relu, sigmoid, tanh
    seed: int = 42
    max_params: int = 512  # Hard limit for true "nano" networks

class NanoTensor:
    """
    Ultra-lightweight neural network (128-512 parameters).
    Deterministic weight initialization from seed.
    Online learning with gradient descent.
    """
    
    def __init__(self, config: NanoTensorConfig):
        self.config = config
        self.rng = np.random.RandomState(config.seed)
        
        # Initialize weights deterministically from seed
        self._init_weights()
        
        # Activation function
        self.activation = self._get_activation(config.activation)
        self.output_activation = self._sigmoid  # Always sigmoid for output
        
        # Experience buffer for learning
        self.experience_buffer = deque(maxlen=100)
        
        # Performance metrics
        self.total_updates = 0
        self.cumulative_error = 0.0
    
    def _init_weights(self):
        """Deterministic weight initialization"""
        # Xavier/Glorot initialization scaled for small networks
        limit1 = np.sqrt(6.0 / (self.config.input_dim + self.config.hidden_dim))
        limit2 = np.sqrt(6.0 / (self.config.hidden_dim + self.config.output_dim))
        
        self.W1 = self.rng.uniform(-limit1, limit1, 
                                   (self.config.input_dim, self.config.hidden_dim))
        self.b1 = np.zeros(self.config.hidden_dim)
        self.W2 = self.rng.uniform(-limit2, limit2,
                                   (self.config.hidden_dim, self.config.output_dim))
        self.b2 = np.zeros(self.config.output_dim)
        
        # Verify parameter count
        total_params = (self.W1.size + self.b1.size + 
                       self.W2.size + self.b2.size)
        if total_params > self.config.max_params:
            raise ValueError(f"Network too large: {total_params} > {self.config.max_params}")
    
    def _get_activation(self, name: str) -> Callable:
        """Get activation function"""
        activations = {
            'relu': lambda x: np.maximum(0, x),
            'sigmoid': self._sigmoid,
            'tanh': np.tanh,
            'leaky_relu': lambda x: np.where(x > 0, x, 0.01 * x)
        }
        return activations.get(name, activations['relu'])
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Numerically stable sigmoid"""
        return np.where(x >= 0,
                       1 / (1 + np.exp(-np.minimum(x, 500))),
                       np.exp(np.maximum(x, -500)) / (1 + np.exp(np.maximum(x, -500))))
    
    def _sigmoid_derivative(self, x: np.ndarray) -> np.ndarray:
        """Derivative of sigmoid"""
        s = self._sigmoid(x)
        return s * (1 - s)
    
    def forward(self, x: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Forward pass through network.
        Returns output and cache for backprop.
        """
        x = np.array(x).reshape(1, -1)
        
        # Layer 1
        z1 = np.dot(x, self.W1) + self.b1
        a1 = self.activation(z1)
        
        # Layer 2
        z2 = np.dot(a1, self.W2) + self.b2
        output = self.output_activation(z2)
        
        cache = {'x': x, 'z1': z1, 'a1': a1, 'z2': z2}
        return output.flatten(), cache
    
    def backward(self, cache: Dict, target: np.ndarray) -> Dict:
        """
        Backward pass - compute gradients.
        Returns gradients dict.
        """
        x, z1, a1, z2 = cache['x'], cache['z1'], cache['a1'], cache['z2']
        target = np.array(target).reshape(1, -1)
        
        m = x.shape[0]
        
        # Output layer gradient
        dz2 = self._sigmoid_derivative(z2) * (a1.dot(self.W2) + self.b2 - target)
        # Actually for MSE: dz2 = (output - target) * sigmoid_derivative
        output = self._sigmoid(z2)
        dz2 = (output - target) * self._sigmoid_derivative(z2)
        
        dW2 = np.dot(a1.T, dz2) / m
        db2 = np.sum(dz2, axis=0) / m
        
        # Hidden layer gradient
        dz1 = np.dot(dz2, self.W2.T)
        if self.config.activation == 'relu':
            dz1 = dz1 * (z1 > 0).astype(float)
        elif self.config.activation == 'sigmoid':
            dz1 = dz1 * self._sigmoid_derivative(z1)
        elif self.config.activation == 'tanh':
            dz1 = dz1 * (1 - np.tanh(z1) ** 2)
        
        dW1 = np.dot(x.T, dz1) / m
        db1 = np.sum(dz1, axis=0) / m
        
        return {'dW1': dW1, 'db1': db1, 'dW2': dW2, 'db2': db2}
    
    def update(self, gradients: Dict):
        """Apply gradients with learning rate"""
        lr = self.config.learning_rate
        
        self.W1 -= lr * gradients['dW1']
        self.b1 -= lr * gradients['db1']
        self.W2 -= lr * gradients['dW2']
        self.b2 -= lr * gradients['db2']
        
        self.total_updates += 1
    
    def train_step(self, input_vec: np.ndarray, target: np.ndarray) -> float:
        """Single training step, returns loss"""
        output, cache = self.forward(input_vec)
        
        # MSE loss
        loss = np.mean((output - target) ** 2)
        self.cumulative_error += loss
        
        # Backprop and update
        gradients = self.backward(cache, target)
        self.update(gradients)
        
        # Store experience
        self.experience_buffer.append({
            'input': input_vec.copy(),
            'target': target.copy(),
            'output': output.copy(),
            'loss': loss
        })
        
        return loss
    
    def predict(self, input_vec: np.ndarray) -> np.ndarray:
        """Inference only - no gradients"""
        output, _ = self.forward(input_vec)
        return output
    
    def get_state(self) -> Dict:
        """Serialize network state"""
        return {
            'config': asdict(self.config),
            'W1': self.W1.tolist(),
            'b1': self.b1.tolist(),
            'W2': self.W2.tolist(),
            'b2': self.b2.tolist(),
            'total_updates': self.total_updates,
            'cumulative_error': self.cumulative_error,
            'param_count': self.W1.size + self.b1.size + self.W2.size + self.b2.size
        }
    
    def set_state(self, state: Dict):
        """Load network state"""
        self.W1 = np.array(state['W1'])
        self.b1 = np.array(state['b1'])
        self.W2 = np.array(state['W2'])
        self.b2 = np.array(state['b2'])
        self.total_updates = state['total_updates']
        self.cumulative_error = state['cumulative_error']
    
    def summary(self) -> str:
        """Get network summary"""
        total_params = (self.W1.size + self.b1.size + 
                       self.W2.size + self.b2.size)
        return (f"NanoTensor({self.config.input_dim}->{self.config.hidden_dim}->{self.config.output_dim}, "
                f"params={total_params}, updates={self.total_updates})")


class EnsembleNanoTensor:
    """
    Ensemble of nano-tensors for more robust predictions.
    Uses voting/averaging across multiple small networks.
    """
    
    def __init__(self, num_agents: int = 3, config: Optional[NanoTensorConfig] = None):
        self.num_agents = num_agents
        self.config = config or NanoTensorConfig()
        
        # Create ensemble with different seeds
        self.agents = []
        for i in range(num_agents):
            agent_config = NanoTensorConfig(
                input_dim=self.config.input_dim,
                hidden_dim=self.config.hidden_dim,
                output_dim=self.config.output_dim,
                learning_rate=self.config.learning_rate,
                activation=self.config.activation,
                seed=self.config.seed + i,
                max_params=self.config.max_params
            )
            self.agents.append(NanoTensor(agent_config))
    
    def predict(self, input_vec: np.ndarray, method: str = 'mean') -> np.ndarray:
        """
        Ensemble prediction.
        method: 'mean', 'median', or 'vote'
        """
        predictions = [agent.predict(input_vec) for agent in self.agents]
        stacked = np.stack(predictions)
        
        if method == 'mean':
            return np.mean(stacked, axis=0)
        elif method == 'median':
            return np.median(stacked, axis=0)
        elif method == 'vote':
            # Binary voting for classification-like outputs
            binary = (stacked > 0.5).astype(int)
            votes = np.sum(binary, axis=0)
            return (votes >= self.num_agents / 2).astype(float)
        else:
            return np.mean(stacked, axis=0)
    
    def train_step(self, input_vec: np.ndarray, target: np.ndarray) -> float:
        """Train all agents, return average loss"""
        losses = []
        for agent in self.agents:
            loss = agent.train_step(input_vec, target)
            losses.append(loss)
        return np.mean(losses)
    
    def get_states(self) -> List[Dict]:
        """Get all agent states"""
        return [agent.get_state() for agent in self.agents]
    
    def set_states(self, states: List[Dict]):
        """Load all agent states"""
        for agent, state in zip(self.agents, states):
            agent.set_state(state)


# ==================== UTILITY FUNCTIONS ====================

def vector_hash(vec: np.ndarray, seed: int = 0) -> str:
    """Deterministic hash of a vector"""
    data = vec.tobytes() + str(seed).encode()
    return hashlib.md5(data).hexdigest()[:16]

def normalize_vector(vec: np.ndarray, target_range: Tuple[float, float] = (0, 1)) -> np.ndarray:
    """Normalize vector to target range"""
    min_val, max_val = target_range
    vec_min, vec_max = np.min(vec), np.max(vec)
    if vec_max - vec_min < 1e-8:
        return np.full_like(vec, (min_val + max_val) / 2)
    normalized = (vec - vec_min) / (vec_max - vec_min)
    return normalized * (max_val - min_val) + min_val

def encode_categorical(value: str, categories: List[str]) -> np.ndarray:
    """One-hot encode categorical value"""
    vec = np.zeros(len(categories))
    if value in categories:
        vec[categories.index(value)] = 1.0
    return vec

# ==================== DEMONSTRATION ====================

def demo():
    """Demonstrate nano-tensor capabilities"""
    print("=" * 60)
    print("NANO-TENSOR FRAMEWORK DEMO")
    print("=" * 60)
    
    # Single nano-tensor
    print("\n1. Single Nano-Tensor")
    config = NanoTensorConfig(input_dim=4, hidden_dim=8, output_dim=2, seed=42)
    net = NanoTensor(config)
    print(f"   {net.summary()}")
    
    # Inference
    test_input = np.array([0.5, 0.3, 0.7, 0.2])
    output = net.predict(test_input)
    print(f"   Input:  {test_input}")
    print(f"   Output: {output}")
    
    # Training
    print("\n2. Online Learning Demo")
    target = np.array([0.8, 0.2])
    print(f"   Target: {target}")
    
    for i in range(10):
        loss = net.train_step(test_input, target)
        if i % 3 == 0:
            print(f"   Step {i}: Loss = {loss:.6f}")
    
    final_output = net.predict(test_input)
    print(f"   Final Output: {final_output}")
    print(f"   Updates: {net.total_updates}")
    
    # Ensemble
    print("\n3. Ensemble Demo")
    ensemble = EnsembleNanoTensor(num_agents=5, config=config)
    ensemble_output = ensemble.predict(test_input)
    print(f"   Ensemble Output: {ensemble_output}")
    print(f"   Agents: {len(ensemble.agents)}")
    
    # Serialization
    print("\n4. State Serialization")
    state = net.get_state()
    print(f"   State keys: {list(state.keys())}")
    print(f"   Parameter count: {state['param_count']}")
    
    # Verify deterministic
    print("\n5. Determinism Check")
    net1 = NanoTensor(NanoTensorConfig(input_dim=4, hidden_dim=8, output_dim=2, seed=123))
    net2 = NanoTensor(NanoTensorConfig(input_dim=4, hidden_dim=8, output_dim=2, seed=123))
    test = np.array([0.1, 0.2, 0.3, 0.4])
    out1 = net1.predict(test)
    out2 = net2.predict(test)
    print(f"   Same seed -> Same output: {np.allclose(out1, out2)}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    demo()
