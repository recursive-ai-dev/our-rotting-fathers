#!/usr/bin/env python3
"""
Animation Generator - Create animated sprite frames for characters
Supports idle, walk, run, run variants, jump, attack, and pickup animations.
Direction-aware: generates frames for all 4 directions.
"""

import random
import math
from PIL import Image, ImageDraw, ImageChops
from typing import Dict, List, Tuple, Optional
try:
    from .pure_generator import PureCharacterGenerator
    from .direction_renderer import Direction, DirectionRenderer
    from .animation_types import ANIMATION_DEFS, get_animation_def
except ImportError:
    from pure_generator import PureCharacterGenerator
    from direction_renderer import Direction, DirectionRenderer
    from animation_types import ANIMATION_DEFS, get_animation_def

class AnimationGenerator:
    """Generate animation frames for characters"""

    def __init__(self, canvas_size: Tuple[int, int] = (32, 32)):
        self.canvas_size = canvas_size
        self.width, self.height = canvas_size
        self.base_generator = PureCharacterGenerator(canvas_size=canvas_size)
        self.direction_renderer = DirectionRenderer(canvas_size=canvas_size)

        # Frame counts from centralized definitions
        self.frame_counts = {name: d.frames for name, d in ANIMATION_DEFS.items()}

    def generate_animation(self, params: Dict, animation_type: str = 'idle',
                           direction: Direction = Direction.DOWN) -> List[Image.Image]:
        """Generate a sequence of frames for the specified animation and direction."""
        frame_count = self.frame_counts.get(animation_type, 4)
        frames = []

        for frame_idx in range(frame_count):
            anim_offsets = self._calculate_animation_offsets(animation_type, frame_idx, frame_count)
            frame = self._generate_frame_with_pose(params, anim_offsets, direction)
            frames.append(frame)

        return frames

    def _calculate_animation_offsets(self, anim_type: str, frame_idx: int, total_frames: int) -> Dict:
        """Calculate pose offsets for a specific animation frame"""
        progress = frame_idx / total_frames  # 0.0 to ~1.0

        offsets = {
            'body_y': 0,
            'body_x': 0,
            'head_y': 0,
            'head_rotation': 0,
            'arm_left_y': 0,
            'arm_right_y': 0,
            'arm_extend_x': 0,
            'leg_left_y': 0,
            'leg_right_y': 0,
            'breathing': 0,
            'bounce': 0,
        }

        if anim_type == 'idle':
            breathe_cycle = math.sin(progress * 2 * math.pi)
            offsets['breathing'] = breathe_cycle * 0.02
            offsets['body_y'] = int(breathe_cycle * self.height * 0.01)
            offsets['head_y'] = int(breathe_cycle * self.height * 0.015)

        elif anim_type == 'walk':
            walk_cycle = math.sin(progress * 2 * math.pi)
            walk_cycle_cos = math.cos(progress * 2 * math.pi)
            offsets['bounce'] = abs(walk_cycle) * 0.05
            offsets['body_y'] = int(abs(walk_cycle) * self.height * 0.03)
            arm_swing = int(walk_cycle * self.height * 0.04)
            offsets['arm_left_y'] = arm_swing
            offsets['arm_right_y'] = -arm_swing
            leg_offset = int(walk_cycle_cos * self.height * 0.02)
            offsets['leg_left_y'] = leg_offset
            offsets['leg_right_y'] = -leg_offset

        elif anim_type == 'run':
            self._apply_run_offsets(offsets, progress, phase=0.0, amp=1.0, lean=-0.1)

        elif anim_type == 'run_alt1':
            self._apply_run_offsets(offsets, progress, phase=0.0, amp=1.0, lean=-0.1)

        elif anim_type == 'run_alt2':
            self._apply_run_offsets(offsets, progress, phase=0.25, amp=1.15, lean=-0.15)

        elif anim_type == 'run_alt3':
            self._apply_run_offsets(offsets, progress, phase=0.5, amp=0.85, lean=-0.05)

        elif anim_type == 'jump':
            self._apply_jump_offsets(offsets, progress)

        elif anim_type == 'attack':
            self._apply_attack_offsets(offsets, progress)

        elif anim_type == 'pickup':
            self._apply_pickup_offsets(offsets, progress)

        return offsets

    def _apply_run_offsets(self, offsets: Dict, progress: float, phase: float, amp: float, lean: float):
        """Apply running animation offsets with configurable phase, amplitude, and lean."""
        shifted = progress + phase
        run_cycle = math.sin(shifted * 2 * math.pi)
        run_cycle_cos = math.cos(shifted * 2 * math.pi)

        offsets['bounce'] = abs(run_cycle) * 0.08 * amp
        offsets['body_y'] = int(abs(run_cycle) * self.height * 0.05 * amp)
        offsets['head_rotation'] = lean
        arm_swing = int(run_cycle * self.height * 0.06 * amp)
        offsets['arm_left_y'] = arm_swing
        offsets['arm_right_y'] = -arm_swing
        leg_offset = int(run_cycle_cos * self.height * 0.04 * amp)
        offsets['leg_left_y'] = leg_offset
        offsets['leg_right_y'] = -leg_offset

    def _apply_jump_offsets(self, offsets: Dict, progress: float):
        """Jump: crouch, launch, hang, land, recover."""
        if progress < 0.2:
            crouch_factor = progress / 0.2
            offsets['body_y'] = int(crouch_factor * self.height * 0.08)
            offsets['head_y'] = int(crouch_factor * self.height * 0.03)
        elif progress < 0.4:
            launch_factor = (progress - 0.2) / 0.2
            offsets['body_y'] = int((0.08 - launch_factor * 0.15) * self.height)
            offsets['head_y'] = int((0.03 - launch_factor * 0.08) * self.height)
            offsets['arm_left_y'] = int(-launch_factor * self.height * 0.05)
            offsets['arm_right_y'] = int(-launch_factor * self.height * 0.05)
        elif progress < 0.6:
            offsets['body_y'] = int(-0.07 * self.height)
            offsets['head_y'] = int(-0.05 * self.height)
            offsets['arm_left_y'] = int(-self.height * 0.05)
            offsets['arm_right_y'] = int(-self.height * 0.05)
        elif progress < 0.8:
            land_factor = (progress - 0.6) / 0.2
            offsets['body_y'] = int((-0.07 + land_factor * 0.15) * self.height)
            offsets['head_y'] = int((-0.05 + land_factor * 0.08) * self.height)
            offsets['arm_left_y'] = int((-0.05 + land_factor * 0.05) * self.height)
            offsets['arm_right_y'] = int((-0.05 + land_factor * 0.05) * self.height)
        else:
            recover_factor = (progress - 0.8) / 0.2
            offsets['body_y'] = int((0.08 - recover_factor * 0.08) * self.height)
            offsets['head_y'] = int((0.03 - recover_factor * 0.03) * self.height)

    def _apply_attack_offsets(self, offsets: Dict, progress: float):
        """Attack: wind-up, swing start, swing mid, contact, follow-through, recover."""
        if progress < 1/6:
            # Wind-up
            t = progress / (1/6)
            offsets['arm_right_y'] = int(-t * self.height * 0.08)
            offsets['body_x'] = int(-t * self.width * 0.02)
        elif progress < 2/6:
            # Swing start
            t = (progress - 1/6) / (1/6)
            offsets['arm_right_y'] = int((-0.08 + t * 0.12) * self.height)
            offsets['body_x'] = int((-0.02 + t * 0.04) * self.width)
            offsets['arm_extend_x'] = int(t * self.width * 0.05)
        elif progress < 3/6:
            # Swing mid
            t = (progress - 2/6) / (1/6)
            offsets['arm_right_y'] = int(0.04 * self.height)
            offsets['body_x'] = int(0.02 * self.width)
            offsets['arm_extend_x'] = int((0.05 + t * 0.03) * self.width)
            offsets['bounce'] = t * 0.04
        elif progress < 4/6:
            # Contact
            t = (progress - 3/6) / (1/6)
            offsets['arm_right_y'] = int((0.04 + t * 0.02) * self.height)
            offsets['body_x'] = int((0.02 + t * 0.01) * self.width)
            offsets['arm_extend_x'] = int(0.08 * self.width)
            offsets['bounce'] = 0.06
        elif progress < 5/6:
            # Follow-through
            t = (progress - 4/6) / (1/6)
            offsets['arm_right_y'] = int((0.06 - t * 0.04) * self.height)
            offsets['body_x'] = int((0.03 - t * 0.02) * self.width)
            offsets['arm_extend_x'] = int((0.08 - t * 0.05) * self.width)
            offsets['bounce'] = 0.06 * (1 - t)
        else:
            # Recover
            t = (progress - 5/6) / (1/6)
            offsets['arm_right_y'] = int(0.02 * (1 - t) * self.height)
            offsets['body_x'] = int(0.01 * (1 - t) * self.width)
            offsets['arm_extend_x'] = int(0.03 * (1 - t) * self.width)

    def _apply_pickup_offsets(self, offsets: Dict, progress: float):
        """Pickup: reach forward, bend down, grab, lift, stand up."""
        if progress < 0.2:
            # Reach forward
            t = progress / 0.2
            offsets['arm_left_y'] = int(t * self.height * 0.03)
            offsets['arm_right_y'] = int(t * self.height * 0.03)
            offsets['body_x'] = int(t * self.width * 0.01)
        elif progress < 0.4:
            # Bend down
            t = (progress - 0.2) / 0.2
            offsets['body_y'] = int(t * self.height * 0.08)
            offsets['head_y'] = int(t * self.height * 0.06)
            offsets['arm_left_y'] = int((0.03 + t * 0.06) * self.height)
            offsets['arm_right_y'] = int((0.03 + t * 0.06) * self.height)
        elif progress < 0.6:
            # Grab (lowest point)
            offsets['body_y'] = int(0.08 * self.height)
            offsets['head_y'] = int(0.06 * self.height)
            offsets['arm_left_y'] = int(0.09 * self.height)
            offsets['arm_right_y'] = int(0.09 * self.height)
        elif progress < 0.8:
            # Lift
            t = (progress - 0.6) / 0.2
            offsets['body_y'] = int((0.08 - t * 0.06) * self.height)
            offsets['head_y'] = int((0.06 - t * 0.04) * self.height)
            offsets['arm_left_y'] = int((0.09 - t * 0.07) * self.height)
            offsets['arm_right_y'] = int((0.09 - t * 0.07) * self.height)
        else:
            # Stand up
            t = (progress - 0.8) / 0.2
            offsets['body_y'] = int(0.02 * (1 - t) * self.height)
            offsets['head_y'] = int(0.02 * (1 - t) * self.height)
            offsets['arm_left_y'] = int(0.02 * (1 - t) * self.height)
            offsets['arm_right_y'] = int(0.02 * (1 - t) * self.height)

    def _generate_frame_with_pose(self, params: Dict, offsets: Dict,
                                  direction: Direction = Direction.DOWN) -> Image.Image:
        """Generate a single frame with pose offsets applied"""
        sprite = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(sprite)

        animated_params = self._apply_animation_params(params, offsets)

        if direction == Direction.DOWN:
            self._draw_legs_animated(draw, animated_params, offsets)
            self._draw_torso_animated(draw, animated_params, offsets)
            self._draw_arms_animated(draw, animated_params, offsets)
            self._draw_head_animated(draw, animated_params, offsets)
            self._draw_hair_animated(draw, animated_params, offsets)
            self._draw_face_animated(draw, animated_params, offsets)
            self._draw_accessories_animated(draw, animated_params, offsets)
        elif direction == Direction.UP:
            self._draw_back_animated(draw, animated_params, offsets)
        elif direction == Direction.LEFT:
            self._draw_side_animated(draw, animated_params, offsets)
        elif direction == Direction.RIGHT:
            left_frame = self._generate_frame_with_pose(params, offsets, Direction.LEFT)
            return left_frame.transpose(Image.FLIP_LEFT_RIGHT)

        return sprite

    def _draw_back_animated(self, draw: ImageDraw.ImageDraw, params: Dict, offsets: Dict):
        """Draw animated back view using direction renderer with offsets."""
        anim_offsets = params.get('_anim_offsets', {})
        body_y = anim_offsets.get('body_y', 0)
        head_y = anim_offsets.get('head_y', 0)

        self.direction_renderer.set_canvas_size(self.canvas_size)

        # Render back view on overlay, then shift
        overlay = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)

        self.direction_renderer.draw_legs_back(overlay_draw, params)
        self.direction_renderer.draw_torso_back(overlay_draw, params)
        self.direction_renderer.draw_arms_back(overlay_draw, params)
        self.direction_renderer.draw_head_back(overlay_draw, params)
        self.direction_renderer.draw_hair_back(overlay_draw, params)
        self.direction_renderer.draw_accessories_back(overlay_draw, params)

        if body_y or head_y:
            # Approximate: shift entire image by average offset
            avg_offset = (body_y + head_y) // 2
            overlay = self._offset_no_wrap(overlay, 0, avg_offset)

        target_img = getattr(draw, "_image", None)
        if target_img is not None and hasattr(target_img, "alpha_composite"):
            target_img.alpha_composite(overlay)

    def _draw_side_animated(self, draw: ImageDraw.ImageDraw, params: Dict, offsets: Dict):
        """Draw animated side view using direction renderer with offsets."""
        anim_offsets = params.get('_anim_offsets', {})
        body_y = anim_offsets.get('body_y', 0)
        head_y = anim_offsets.get('head_y', 0)
        arm_extend_x = anim_offsets.get('arm_extend_x', 0)

        self.direction_renderer.set_canvas_size(self.canvas_size)

        overlay = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)

        self.direction_renderer.draw_legs_side(overlay_draw, params)
        self.direction_renderer.draw_torso_side(overlay_draw, params)
        self.direction_renderer.draw_arms_side(overlay_draw, params)
        self.direction_renderer.draw_head_side(overlay_draw, params)
        self.direction_renderer.draw_hair_side(overlay_draw, params)
        self.direction_renderer.draw_face_side(overlay_draw, params)
        self.direction_renderer.draw_accessories_side(overlay_draw, params)

        if body_y or head_y:
            avg_offset = (body_y + head_y) // 2
            overlay = self._offset_no_wrap(overlay, 0, avg_offset)

        target_img = getattr(draw, "_image", None)
        if target_img is not None and hasattr(target_img, "alpha_composite"):
            target_img.alpha_composite(overlay)

    def _apply_animation_params(self, params: Dict, offsets: Dict) -> Dict:
        """Create modified params dict with animation offsets"""
        animated = params.copy()
        animated['_anim_offsets'] = offsets
        return animated

    def _s(self, value: float) -> int:
        """Scale a coordinate value"""
        base_size = 32
        scale = self.width / base_size
        return int(value * scale)

    def _center_x(self) -> int:
        return self.width // 2

    # ==================== ANIMATED DRAWING METHODS (DOWN/FRONT) ====================

    def _draw_head_animated(self, draw: ImageDraw.ImageDraw, params: Dict, offsets: Dict = None):
        """Draw head with animation offsets"""
        color = params['skin_color']
        body_metrics = params['body_metrics']
        anim_offsets = params.get('_anim_offsets', {})

        height_scale = body_metrics['height_scale']
        head_size_modifier = body_metrics['body_scales']['head_size']
        width_modifier = body_metrics['body_scales']['width']

        base_head_width = 14
        base_head_height = 14
        head_width = int(base_head_width * head_size_modifier * width_modifier * self._s(1))
        head_height = int(base_head_height * head_size_modifier * self._s(1))

        center_x = self._center_x()
        base_center_y = int(10 * height_scale * self._s(1))
        head_y_offset = anim_offsets.get('head_y', 0)
        center_y = base_center_y + head_y_offset

        left = max(1, center_x - head_width // 2)
        right = min(self.width - 1, center_x + head_width // 2)
        top = max(1, center_y - head_height // 2)
        bottom = min(self.height - 1, center_y + head_height // 2)

        draw.ellipse([left, top, right, bottom], fill=color)

    def _draw_hair_animated(self, draw: ImageDraw.ImageDraw, params: Dict, offsets: Dict = None):
        """Draw hair with animation offsets"""
        self._draw_base_part_with_head_offset(draw, params, self.base_generator._draw_hair)

    def _draw_face_animated(self, draw: ImageDraw.ImageDraw, params: Dict, offsets: Dict = None):
        """Draw face with animation offsets"""
        self._draw_base_part_with_head_offset(draw, params, self.base_generator._draw_face)

    def _draw_torso_animated(self, draw: ImageDraw.ImageDraw, params: Dict, offsets: Dict = None):
        """Draw torso with animation offsets"""
        clothing = params['clothing']
        color = clothing['top_color']
        body_metrics = params['body_metrics']
        anim_offsets = params.get('_anim_offsets', {})

        cx = self._center_x()
        s = self._s

        height_scale = body_metrics['height_scale']
        torso_width_scale = body_metrics['body_scales']['torso_width']
        width_scale = body_metrics['body_scales']['width']

        bounce = anim_offsets.get('bounce', 0)
        breathing = anim_offsets.get('breathing', 0)
        body_y_offset = anim_offsets.get('body_y', 0)

        base_torso_width = 16
        base_torso_height = 8
        torso_width = int(base_torso_width * torso_width_scale * s(1) * (1 + breathing))
        torso_height = int(base_torso_height * height_scale * s(1))

        torso_y_start = int(17 * height_scale * s(1)) + body_y_offset
        torso_y_end = torso_y_start + torso_height

        torso_y_start = max(s(10), min(int(self.height * 0.8), torso_y_start))
        torso_y_end = max(torso_y_start + s(5), min(self.height - 1, torso_y_end))

        torso_left = max(s(2), cx - torso_width // 2)
        torso_right = min(self.width - s(2), cx + torso_width // 2)

        draw.rectangle([torso_left, torso_y_start, torso_right, torso_y_end], fill=color)

        sleeve_width = max(s(2), int(s(3) * width_scale))
        sleeve_height = max(s(3), int(s(6) * height_scale))
        sleeve_y_start = torso_y_start + s(1)
        sleeve_y_end = min(torso_y_end - s(1), sleeve_y_start + sleeve_height)

        left_sleeve_right = torso_left
        left_sleeve_left = max(s(1), left_sleeve_right - sleeve_width)
        draw.rectangle([left_sleeve_left, sleeve_y_start, left_sleeve_right, sleeve_y_end], fill=color)

        right_sleeve_left = torso_right
        right_sleeve_right = min(self.width - s(1), right_sleeve_left + sleeve_width)
        draw.rectangle([right_sleeve_left, sleeve_y_start, right_sleeve_right, sleeve_y_end], fill=color)

    def _draw_arms_animated(self, draw: ImageDraw.ImageDraw, params: Dict, offsets: Dict = None):
        """Draw arms with animation offsets"""
        color = params['skin_color']
        anim_offsets = params.get('_anim_offsets', {})

        cx = self._center_x()
        s = self._s

        left_arm_offset = anim_offsets.get('arm_left_y', 0)
        right_arm_offset = anim_offsets.get('arm_right_y', 0)
        body_y_offset = anim_offsets.get('body_y', 0)

        left_arm_y = s(23) + body_y_offset + left_arm_offset
        draw.rectangle([cx - s(11), left_arm_y, cx - s(8), left_arm_y + s(3)], fill=color)

        right_arm_y = s(23) + body_y_offset + right_arm_offset
        draw.rectangle([cx + s(8), right_arm_y, cx + s(11), right_arm_y + s(3)], fill=color)

    def _draw_legs_animated(self, draw: ImageDraw.ImageDraw, params: Dict, offsets: Dict = None):
        """Draw legs with animation offsets"""
        clothing = params['clothing']
        bottom_style = clothing['bottom_style']
        color = clothing['bottom_color']
        skin_color = params['skin_color']
        anim_offsets = params.get('_anim_offsets', {})

        cx = self._center_x()
        s = self._s

        left_leg_offset = anim_offsets.get('leg_left_y', 0)
        right_leg_offset = anim_offsets.get('leg_right_y', 0)
        body_y_offset = anim_offsets.get('body_y', 0)

        base_leg_y = s(25) + body_y_offset

        if bottom_style in ['skirt', 'pencil_skirt', 'expensive_skirt']:
            if bottom_style == 'pencil_skirt':
                draw.rectangle([cx - s(5), base_leg_y, cx + s(5), base_leg_y + s(4)], fill=color)
            else:
                draw.rectangle([cx - s(7), base_leg_y, cx + s(7), base_leg_y + s(3)], fill=color)
            draw.rectangle([cx - s(5), base_leg_y + s(3) + left_leg_offset, cx - s(2), base_leg_y + s(6) + left_leg_offset], fill=skin_color)
            draw.rectangle([cx + s(2), base_leg_y + s(3) + right_leg_offset, cx + s(5), base_leg_y + s(6) + right_leg_offset], fill=skin_color)
        elif bottom_style in ['dress']:
            draw.rectangle([cx - s(7), base_leg_y, cx + s(7), base_leg_y + s(5)], fill=color)
            draw.rectangle([cx - s(5), base_leg_y + s(5) + left_leg_offset, cx - s(2), base_leg_y + s(6) + left_leg_offset], fill=skin_color)
            draw.rectangle([cx + s(2), base_leg_y + s(5) + right_leg_offset, cx + s(5), base_leg_y + s(6) + right_leg_offset], fill=skin_color)
        elif bottom_style in ['shorts']:
            draw.rectangle([cx - s(6), base_leg_y, cx - s(1), base_leg_y + s(2)], fill=color)
            draw.rectangle([cx + s(1), base_leg_y, cx + s(6), base_leg_y + s(2)], fill=color)
            draw.rectangle([cx - s(6), base_leg_y + s(2) + left_leg_offset, cx - s(1), base_leg_y + s(6) + left_leg_offset], fill=skin_color)
            draw.rectangle([cx + s(1), base_leg_y + s(2) + right_leg_offset, cx + s(6), base_leg_y + s(6) + right_leg_offset], fill=skin_color)
        else:
            draw.rectangle([cx - s(6), base_leg_y + left_leg_offset, cx - s(1), base_leg_y + s(6) + left_leg_offset], fill=color)
            draw.rectangle([cx + s(1), base_leg_y + right_leg_offset, cx + s(6), base_leg_y + s(6) + right_leg_offset], fill=color)

        shoe_color = (0, 0, 0) if params['social_class'] in ['upper', 'rich'] else (139, 69, 19)
        foot_y = s(31) + body_y_offset
        if bottom_style not in ['skirt', 'dress', 'pencil_skirt', 'expensive_skirt']:
            draw.rectangle([cx - s(7), foot_y + left_leg_offset, cx, foot_y + s(1) + left_leg_offset], fill=shoe_color)
            draw.rectangle([cx, foot_y + right_leg_offset, cx + s(7), foot_y + s(1) + right_leg_offset], fill=shoe_color)
        else:
            heel_color = shoe_color
            draw.rectangle([cx - s(5), foot_y + left_leg_offset, cx - s(2), foot_y + s(1) + left_leg_offset], fill=heel_color)
            draw.rectangle([cx + s(2), foot_y + right_leg_offset, cx + s(5), foot_y + s(1) + right_leg_offset], fill=heel_color)

    def _draw_accessories_animated(self, draw: ImageDraw.ImageDraw, params: Dict, offsets: Dict = None):
        """Draw accessories with animation offsets"""
        anim_offsets = params.get('_anim_offsets', {})
        body_y_offset = anim_offsets.get('body_y', 0)
        head_y_offset = anim_offsets.get('head_y', 0)

        cx = self._center_x()
        s = self._s

        if params.get('has_glasses', False):
            glass_color = (0, 0, 0)
            glasses_y = s(7) + head_y_offset
            draw.rectangle([cx - s(5), glasses_y, cx - s(1), glasses_y + s(2)], outline=glass_color)
            draw.rectangle([cx + s(1), glasses_y, cx + s(5), glasses_y + s(2)], outline=glass_color)
            draw.line([(cx - s(1), glasses_y + s(1)), (cx + s(1), glasses_y + s(1))], fill=glass_color)
            draw.line([(cx - s(5), glasses_y + s(1)), (cx - s(8), glasses_y + s(1))], fill=glass_color)
            draw.line([(cx + s(5), glasses_y + s(1)), (cx + s(8), glasses_y + s(1))], fill=glass_color)

        if params.get('has_jewelry', False):
            jewelry_color = (255, 215, 0)
            social_class = params['social_class']
            gender = params['gender']

            if social_class in ['upper', 'rich']:
                if gender == 'female':
                    earring_y = s(9) + head_y_offset
                    draw.point((cx - s(8), earring_y), fill=jewelry_color)
                    draw.point((cx + s(8), earring_y), fill=jewelry_color)
                    necklace_y = s(16) + body_y_offset
                    draw.line([(cx - s(4), necklace_y), (cx + s(4), necklace_y)], fill=jewelry_color)
                    draw.point((cx, necklace_y + s(1)), fill=jewelry_color)
                else:
                    watch_y = s(24) + body_y_offset
                    draw.rectangle([cx - s(12), watch_y, cx - s(10), watch_y + s(1)], fill=jewelry_color)
            elif social_class in ['middle']:
                if gender == 'female':
                    earring_y = s(9) + head_y_offset
                    draw.point((cx - s(8), earring_y), fill=(192, 192, 192))
                    draw.point((cx + s(8), earring_y), fill=(192, 192, 192))

    # ==================== UTILITY METHODS ====================

    def _draw_base_part_with_head_offset(self, draw: ImageDraw.ImageDraw, params: Dict, draw_fn):
        """Draw a base-generator facial feature and shift with animated head motion."""
        anim_offsets = params.get('_anim_offsets', {})
        head_y_offset = anim_offsets.get('head_y', 0)

        self.base_generator.set_canvas_size(self.canvas_size)

        overlay = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        draw_fn(overlay_draw, params)

        if head_y_offset:
            overlay = self._offset_no_wrap(overlay, 0, head_y_offset)

        target_img = getattr(draw, "_image", None)
        if target_img is not None and hasattr(target_img, "alpha_composite"):
            target_img.alpha_composite(overlay)
            return

        # Fallback: draw without offset
        overlay2 = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        overlay2_draw = ImageDraw.Draw(overlay2)
        draw_fn(overlay2_draw, params)
        target_img2 = getattr(draw, "_image", None)
        if target_img2 is not None:
            target_img2.alpha_composite(overlay2)

    def _offset_no_wrap(self, image: Image.Image, x_offset: int, y_offset: int) -> Image.Image:
        """Offset image without wrapped pixels reappearing on opposite edges."""
        shifted = ImageChops.offset(image, x_offset, y_offset)
        clear = ImageDraw.Draw(shifted)

        if y_offset > 0:
            clear.rectangle([0, 0, self.width, min(self.height, y_offset)], fill=(0, 0, 0, 0))
        elif y_offset < 0:
            clear.rectangle([0, max(0, self.height + y_offset), self.width, self.height], fill=(0, 0, 0, 0))

        if x_offset > 0:
            clear.rectangle([0, 0, min(self.width, x_offset), self.height], fill=(0, 0, 0, 0))
        elif x_offset < 0:
            clear.rectangle([max(0, self.width + x_offset), 0, self.width, self.height], fill=(0, 0, 0, 0))

        return shifted

    def create_sprite_sheet(self, frames: List[Image.Image], output_path: str,
                           direction: str = 'horizontal') -> str:
        """Create a sprite sheet from animation frames"""
        if not frames:
            return ""

        frame_width = frames[0].width
        frame_height = frames[0].height
        frame_count = len(frames)

        if direction == 'horizontal':
            sheet_width = frame_width * frame_count
            sheet_height = frame_height
        else:
            sheet_width = frame_width
            sheet_height = frame_height * frame_count

        sprite_sheet = Image.new('RGBA', (sheet_width, sheet_height), (0, 0, 0, 0))

        for i, frame in enumerate(frames):
            if direction == 'horizontal':
                x = i * frame_width
                y = 0
            else:
                x = 0
                y = i * frame_height
            sprite_sheet.paste(frame, (x, y), frame)

        sprite_sheet.save(output_path, "PNG")
        return output_path

    def create_gif(self, frames: List[Image.Image], output_path: str,
                  duration: int = 100, loop: int = 0) -> str:
        """Create an animated GIF from frames"""
        if not frames:
            return ""

        rgb_frames = []
        for frame in frames:
            rgb_frame = Image.new('RGB', frame.size, (255, 255, 255))
            rgb_frame.paste(frame, mask=frame.split()[3])
            rgb_frames.append(rgb_frame)

        rgb_frames[0].save(
            output_path,
            save_all=True,
            append_images=rgb_frames[1:],
            duration=duration,
            loop=loop
        )
        return output_path


def demo_animation():
    """Demo the animation generator"""
    print("Animation Generator Demo")
    print("=" * 40)

    from .mass_generator import MassCharacterGenerator

    canvas_size = (64, 64)
    char_gen = MassCharacterGenerator(canvas_size=canvas_size)
    params = char_gen.generate_unique_character_parameters()

    print(f"\nGenerated character: {params['gender']}, {params['age_category']}, {params['social_class']}")

    anim_gen = AnimationGenerator(canvas_size=canvas_size)

    animations = list(ANIMATION_DEFS.keys())

    import os
    os.makedirs("animation_demo", exist_ok=True)

    for anim_type in animations:
        print(f"\nGenerating {anim_type} animation...")
        frames = anim_gen.generate_animation(params, anim_type)

        for i, frame in enumerate(frames):
            frame.save(f"animation_demo/{anim_type}_frame_{i:02d}.png", "PNG")

        sheet_path = f"animation_demo/{anim_type}_spritesheet.png"
        anim_gen.create_sprite_sheet(frames, sheet_path)

        gif_path = f"animation_demo/{anim_type}_animation.gif"
        anim_gen.create_gif(frames, gif_path, duration=ANIMATION_DEFS[anim_type].speed_ms)

        print(f"  {len(frames)} frames")

    print("\nDemo complete!")


if __name__ == "__main__":
    demo_animation()
