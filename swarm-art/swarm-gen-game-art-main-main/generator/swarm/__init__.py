#!/usr/bin/env python3
"""
GeneSwarm - Multi-Agent Character Generation System

A deterministic swarm of nano-tensor agents that collaboratively
generate unique human characters through consensus.

Components:
- nano_tensor: Ultra-lightweight neural networks (<512 params)
- agents: Specialized decision-making agents
- orchestrator: Swarm coordination and consensus
- memory: Embedding-based experience storage
- swarm_generator: Integration with existing generators
"""

from .nano_tensor import NanoTensor, NanoTensorConfig, EnsembleNanoTensor
from .agents import (
    SwarmAgent, BodyAgent, StyleAgent, DiversityAgent, 
    CriticAgent, AnimatorAgent, create_agent_swarm, AgentDecision
)
from .orchestrator import SwarmOrchestrator, ConsensusResult, SwarmGeneration
from .memory import SwarmMemory, MemoryEntry, TransferLearningBuffer

__version__ = "1.0.0"
__all__ = [
    # Nano-Tensor
    'NanoTensor', 'NanoTensorConfig', 'EnsembleNanoTensor',
    # Agents
    'SwarmAgent', 'BodyAgent', 'StyleAgent', 'DiversityAgent',
    'CriticAgent', 'AnimatorAgent', 'create_agent_swarm', 'AgentDecision',
    # Orchestrator
    'SwarmOrchestrator', 'ConsensusResult', 'SwarmGeneration',
    # Memory
    'SwarmMemory', 'MemoryEntry', 'TransferLearningBuffer'
]
