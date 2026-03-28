#!/usr/bin/env python3
"""
Character Model - QObject wrapping character parameters with signals.
Central data model connecting controls, generators, and preview widgets.
"""

from PyQt6.QtCore import QObject, pyqtSignal
from PIL import Image
from typing import Dict, List, Optional, Tuple
import random

from generator.pure_generator import PureCharacterGenerator
from generator.animation_generator import AnimationGenerator
from generator.direction_renderer import Direction
from generator.animation_types import ANIMATION_DEFS, get_animation_def


class CharacterModel(QObject):
    """Central model for character state, generation, and animation."""

    # Signals
    params_changed = pyqtSignal(dict)
    character_generated = pyqtSignal(dict)  # {Direction: Image}
    animation_generated = pyqtSignal(str, dict)  # anim_type, {Direction: [frames]}
    direction_changed = pyqtSignal(str)  # direction name
    generation_started = pyqtSignal()
    generation_finished = pyqtSignal()

    def __init__(self, canvas_size: Tuple[int, int] = (32, 32), parent=None):
        super().__init__(parent)
        self._canvas_size = canvas_size
        self._params: Optional[Dict] = None
        self._seed: Optional[int] = None
        self._use_swarm = False
        self._current_direction = Direction.DOWN

        # Generators
        self._generator = PureCharacterGenerator(canvas_size=canvas_size)
        self._anim_generator = AnimationGenerator(canvas_size=canvas_size)

        # Cached renders
        self._static_renders: Dict[Direction, Image.Image] = {}
        self._animation_cache: Dict[str, Dict[Direction, List[Image.Image]]] = {}

    @property
    def canvas_size(self) -> Tuple[int, int]:
        return self._canvas_size

    @canvas_size.setter
    def canvas_size(self, size: Tuple[int, int]):
        self._canvas_size = size
        self._generator.set_canvas_size(size)
        self._anim_generator = AnimationGenerator(canvas_size=size)
        self._clear_cache()

    @property
    def params(self) -> Optional[Dict]:
        return self._params

    @property
    def current_direction(self) -> Direction:
        return self._current_direction

    @current_direction.setter
    def current_direction(self, direction: Direction):
        self._current_direction = direction
        self.direction_changed.emit(direction.value)

    @property
    def seed(self) -> Optional[int]:
        return self._seed

    @seed.setter
    def seed(self, value: Optional[int]):
        self._seed = value

    @property
    def use_swarm(self) -> bool:
        return self._use_swarm

    @use_swarm.setter
    def use_swarm(self, value: bool):
        self._use_swarm = value

    def generate_character(self, gender: Optional[str] = None,
                           social_class: Optional[str] = None,
                           age_category: Optional[str] = None,
                           body_type: Optional[str] = None,
                           hair_style: Optional[str] = None,
                           face_style: Optional[str] = None):
        """Generate a new character, optionally overriding specific params."""
        self.generation_started.emit()
        self._clear_cache()

        if self._seed is not None:
            random.seed(self._seed)

        self._params = self._generator._generate_character_params()

        # Apply overrides
        if gender is not None:
            self._params['gender'] = gender
        if social_class is not None:
            self._params['social_class'] = social_class
        if age_category is not None:
            self._params['age_category'] = age_category
        if body_type is not None:
            self._params['body_type'] = body_type
        if hair_style is not None:
            self._params['hair_style'] = hair_style
        if face_style is not None:
            self._params['face_style'] = face_style

        self.params_changed.emit(self._params)

        # Render all 4 directions
        self._render_all_directions()
        self.generation_finished.emit()

    def randomize(self):
        """Generate a completely random character (no seed)."""
        self._seed = None
        self.generate_character()

    def _render_all_directions(self):
        """Render character in all 4 directions and emit signal."""
        if self._params is None:
            return

        self._static_renders = {}
        for d in Direction:
            self._static_renders[d] = self._generator._render_character_with_params(
                self._params, direction=d
            )

        self.character_generated.emit(self._static_renders)

    def get_static_render(self, direction: Direction) -> Optional[Image.Image]:
        """Get the cached static render for a direction."""
        return self._static_renders.get(direction)

    def generate_animation_frames(self, anim_type: str,
                                  directions: Optional[List[Direction]] = None):
        """Generate animation frames for specified directions."""
        if self._params is None:
            return

        if directions is None:
            directions = list(Direction)

        frames_by_dir: Dict[Direction, List[Image.Image]] = {}
        for d in directions:
            frames_by_dir[d] = self._anim_generator.generate_animation(
                self._params, anim_type, direction=d
            )

        self._animation_cache[anim_type] = frames_by_dir
        self.animation_generated.emit(anim_type, frames_by_dir)

    def get_cached_animation(self, anim_type: str) -> Optional[Dict[Direction, List[Image.Image]]]:
        """Get cached animation frames."""
        return self._animation_cache.get(anim_type)

    def _clear_cache(self):
        """Clear all render caches."""
        self._static_renders.clear()
        self._animation_cache.clear()
