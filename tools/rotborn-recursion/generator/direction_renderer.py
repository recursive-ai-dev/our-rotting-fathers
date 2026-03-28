#!/usr/bin/env python3
"""
Direction Renderer - 4-directional character rendering.
Supports DOWN (front), UP (back), LEFT (side), RIGHT (mirrored side).
"""

from enum import Enum
from PIL import Image, ImageDraw
from typing import Dict, Tuple


class Direction(Enum):
    DOWN = "down"    # Front-facing (existing code)
    UP = "up"        # Back-facing
    LEFT = "left"    # Left-facing side profile
    RIGHT = "right"  # Mirror of LEFT


class DirectionRenderer:
    """Renders character sprites for non-front directions (UP, LEFT, RIGHT)."""

    def __init__(self, canvas_size: Tuple[int, int] = (32, 32)):
        self.canvas_size = canvas_size
        self.width, self.height = canvas_size
        self.base_size = 32
        self.scale = min(self.width / self.base_size, self.height / self.base_size)

    def _s(self, value: float) -> int:
        return int(value * self.scale)

    def _center_x(self) -> int:
        return self.width // 2

    def set_canvas_size(self, size: Tuple[int, int]):
        self.canvas_size = size
        self.width, self.height = size
        self.scale = min(self.width / self.base_size, self.height / self.base_size)

    # ==================== BACK VIEW (UP) ====================

    def draw_head_back(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw head from behind - same shape as front."""
        color = params['skin_color']
        body_metrics = params['body_metrics']
        height_scale = body_metrics['height_scale']
        head_size_modifier = body_metrics['body_scales']['head_size']
        width_modifier = body_metrics['body_scales']['width']

        base_head_width = 14
        base_head_height = 14
        head_width = int(base_head_width * head_size_modifier * width_modifier * self.scale)
        head_height = int(base_head_height * head_size_modifier * self.scale)

        cx = self._center_x()
        center_y = int(10 * height_scale * self.scale)

        left = max(1, cx - head_width // 2)
        right = min(self.width - 1, cx + head_width // 2)
        top = max(1, center_y - head_height // 2)
        bottom = min(self.height - 1, center_y + head_height // 2)

        draw.ellipse([left, top, right, bottom], fill=color)

    def draw_hair_back(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw hair from behind - fuller coverage of back of head."""
        color = params['hair_color']
        style = params['hair_style']
        cx = self._center_x()
        s = self._s

        if style in ['bald']:
            return

        # Back view: hair covers back of head more fully
        if style in ['short', 'basic_short', 'crew_cut', 'buzzcut',
                      'styled_short', 'side_part', 'neat_short',
                      'professional', 'slicked_back', 'executive_cut',
                      'expensive_cut', 'styled_back', 'designer_short',
                      'short_messy', 'unkempt', 'short_rough']:
            # Short hair - covers top and back of head
            draw.rectangle([cx - s(7), s(2), cx + s(7), s(10)], fill=color)
            # Nape coverage
            draw.rectangle([cx - s(5), s(10), cx + s(5), s(13)], fill=color)

        elif style in ['ponytail', 'neat_ponytail']:
            # Top coverage
            draw.rectangle([cx - s(7), s(2), cx + s(7), s(8)], fill=color)
            # Ponytail hanging down back
            draw.rectangle([cx - s(2), s(8), cx + s(2), s(24)], fill=color)
            # Tie
            darker = tuple(max(0, c - 30) for c in color)
            draw.rectangle([cx - s(2), s(8), cx + s(2), s(9)], fill=darker)

        elif style in ['long', 'simple_long', 'long_messy', 'unkempt_long',
                        'styled_long', 'layered', 'professional_long', 'styled_waves',
                        'luxury_long', 'expensive_style', 'designer_cut', 'glamour_waves']:
            # Long hair - full back coverage
            draw.rectangle([cx - s(8), s(2), cx + s(8), s(8)], fill=color)
            draw.rectangle([cx - s(9), s(8), cx + s(9), s(20)], fill=color)
            # Taper at bottom
            draw.rectangle([cx - s(7), s(20), cx + s(7), s(22)], fill=color)

        elif style in ['bob', 'elegant_bob']:
            # Bob - back coverage to neck
            draw.rectangle([cx - s(8), s(2), cx + s(8), s(12)], fill=color)

    def draw_torso_back(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw torso from behind - no buttons/lapels, add collar line."""
        clothing = params['clothing']
        color = clothing['top_color']
        body_metrics = params['body_metrics']

        cx = self._center_x()
        s = self._s
        height_scale = body_metrics['height_scale']
        torso_width_scale = body_metrics['body_scales']['torso_width']
        width_scale = body_metrics['body_scales']['width']

        base_torso_width = 16
        base_torso_height = 8
        torso_width = int(base_torso_width * torso_width_scale * self.scale)
        torso_height = int(base_torso_height * height_scale * self.scale)

        torso_y_start = int(17 * height_scale * self.scale)
        torso_y_end = torso_y_start + torso_height

        torso_y_start = max(s(10), min(int(self.height * 0.8), torso_y_start))
        torso_y_end = max(torso_y_start + s(5), min(self.height - 1, torso_y_end))

        torso_left = max(s(2), cx - torso_width // 2)
        torso_right = min(self.width - s(2), cx + torso_width // 2)

        # Main torso
        draw.rectangle([torso_left, torso_y_start, torso_right, torso_y_end], fill=color)

        # Collar back line
        collar_color = tuple(max(0, c - 20) for c in color)
        draw.line([(cx - s(3), torso_y_start), (cx + s(3), torso_y_start)], fill=collar_color)

        # Sleeves
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

    def draw_arms_back(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw arms from behind - same positions as front."""
        color = params['skin_color']
        cx = self._center_x()
        s = self._s

        draw.rectangle([cx - s(11), s(23), cx - s(8), s(26)], fill=color)
        draw.rectangle([cx + s(8), s(23), cx + s(11), s(26)], fill=color)

    def draw_legs_back(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw legs from behind."""
        clothing = params['clothing']
        color = clothing['bottom_color']
        skin_color = params['skin_color']
        bottom_style = clothing['bottom_style']

        cx = self._center_x()
        s = self._s

        if bottom_style in ['skirt', 'pencil_skirt', 'expensive_skirt']:
            draw.rectangle([cx - s(7), s(25), cx + s(7), s(28)], fill=color)
            draw.rectangle([cx - s(5), s(28), cx - s(2), s(31)], fill=skin_color)
            draw.rectangle([cx + s(2), s(28), cx + s(5), s(31)], fill=skin_color)
        elif bottom_style in ['dress']:
            draw.rectangle([cx - s(7), s(25), cx + s(7), s(30)], fill=color)
            draw.rectangle([cx - s(5), s(30), cx - s(2), s(31)], fill=skin_color)
            draw.rectangle([cx + s(2), s(30), cx + s(5), s(31)], fill=skin_color)
        elif bottom_style in ['shorts']:
            draw.rectangle([cx - s(6), s(25), cx - s(1), s(27)], fill=color)
            draw.rectangle([cx + s(1), s(25), cx + s(6), s(27)], fill=color)
            draw.rectangle([cx - s(6), s(27), cx - s(1), s(31)], fill=skin_color)
            draw.rectangle([cx + s(1), s(27), cx + s(6), s(31)], fill=skin_color)
        else:
            draw.rectangle([cx - s(6), s(25), cx - s(1), s(31)], fill=color)
            draw.rectangle([cx + s(1), s(25), cx + s(6), s(31)], fill=color)

        # Shoes
        shoe_color = (0, 0, 0) if params['social_class'] in ['upper', 'rich'] else (139, 69, 19)
        if bottom_style not in ['skirt', 'dress', 'pencil_skirt', 'expensive_skirt']:
            draw.rectangle([cx - s(7), s(31), cx, s(32)], fill=shoe_color)
            draw.rectangle([cx, s(31), cx + s(7), s(32)], fill=shoe_color)
        else:
            draw.rectangle([cx - s(5), s(31), cx - s(2), s(32)], fill=shoe_color)
            draw.rectangle([cx + s(2), s(31), cx + s(5), s(32)], fill=shoe_color)

    def draw_accessories_back(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw accessories from behind - only earrings and hat visible."""
        cx = self._center_x()
        s = self._s

        # Earrings visible from behind
        if params.get('has_jewelry', False):
            social_class = params['social_class']
            gender = params['gender']
            if social_class in ['upper', 'rich'] and gender == 'female':
                jewelry_color = (255, 215, 0)
                draw.point((cx - s(8), s(9)), fill=jewelry_color)
                draw.point((cx + s(8), s(9)), fill=jewelry_color)

        # Hat visible from behind
        if params.get('has_hat', False):
            hat_color = (139, 69, 19)
            if params['social_class'] == 'rich':
                hat_color = (25, 25, 112)
            elif params['social_class'] == 'poor':
                hat_color = (105, 105, 105)
            draw.rectangle([cx - s(8), s(1), cx + s(8), s(3)], fill=hat_color)

    # ==================== SIDE VIEW (LEFT) ====================

    def draw_head_side(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw head in side profile - narrower ellipse."""
        color = params['skin_color']
        body_metrics = params['body_metrics']
        height_scale = body_metrics['height_scale']
        head_size_modifier = body_metrics['body_scales']['head_size']

        # Narrower head for side view (~70% of front width)
        base_head_width = 10
        base_head_height = 14
        head_width = int(base_head_width * head_size_modifier * self.scale)
        head_height = int(base_head_height * head_size_modifier * self.scale)

        cx = self._center_x()
        center_y = int(10 * height_scale * self.scale)

        left = max(1, cx - head_width // 2)
        right = min(self.width - 1, cx + head_width // 2)
        top = max(1, center_y - head_height // 2)
        bottom = min(self.height - 1, center_y + head_height // 2)

        draw.ellipse([left, top, right, bottom], fill=color)

        # Protruding nose (extends beyond head edge, facing left)
        s = self._s
        nose_color = tuple(max(0, c - 15) for c in color)
        nose_x = left - s(1) if s(1) > 0 else left
        nose_x = max(0, nose_x)
        draw.point((nose_x, center_y + s(1)), fill=nose_color)

    def draw_hair_side(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw hair in side profile - asymmetric, visible on back half."""
        color = params['hair_color']
        style = params['hair_style']
        cx = self._center_x()
        s = self._s

        if style in ['bald']:
            return

        if style in ['short', 'basic_short', 'crew_cut', 'buzzcut',
                      'styled_short', 'side_part', 'neat_short',
                      'professional', 'slicked_back', 'executive_cut',
                      'expensive_cut', 'styled_back', 'designer_short',
                      'short_messy', 'unkempt', 'short_rough']:
            # Short hair side view - mostly on top and back
            draw.rectangle([cx - s(3), s(2), cx + s(5), s(6)], fill=color)
            draw.rectangle([cx + s(3), s(6), cx + s(5), s(10)], fill=color)

        elif style in ['ponytail', 'neat_ponytail']:
            draw.rectangle([cx - s(3), s(2), cx + s(5), s(6)], fill=color)
            # Ponytail extends back
            draw.rectangle([cx + s(3), s(6), cx + s(6), s(20)], fill=color)

        elif style in ['long', 'simple_long', 'long_messy', 'unkempt_long',
                        'styled_long', 'layered', 'professional_long', 'styled_waves',
                        'luxury_long', 'expensive_style', 'designer_cut', 'glamour_waves']:
            draw.rectangle([cx - s(3), s(2), cx + s(5), s(6)], fill=color)
            # Long hair flows down back side
            draw.rectangle([cx + s(3), s(6), cx + s(7), s(20)], fill=color)

        elif style in ['bob', 'elegant_bob']:
            draw.rectangle([cx - s(3), s(2), cx + s(5), s(6)], fill=color)
            draw.rectangle([cx + s(3), s(6), cx + s(6), s(12)], fill=color)

    def draw_face_side(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw face in side profile - single eye, side mouth."""
        style = params['face_style']
        eye_color = params['eye_color']
        skin_color = params['skin_color']
        cx = self._center_x()
        s = self._s

        if style == 'minimal':
            # Single eye dot
            draw.point((cx - s(2), s(8)), fill=eye_color)
            # Side mouth
            draw.point((cx - s(3), s(12)), fill=(0, 0, 0))

        elif style == 'basic':
            # Single eye with white
            draw.rectangle([cx - s(3), s(7), cx - s(1), s(9)], fill=(255, 255, 255))
            draw.point((cx - s(2), s(8)), fill=eye_color)
            # Side mouth
            mouth_color = tuple(max(0, c - 30) for c in skin_color)
            draw.line([(cx - s(4), s(12)), (cx - s(2), s(12))], fill=mouth_color)

        elif style == 'detailed':
            # Eyebrow
            eyebrow_color = tuple(max(0, c - 40) for c in params['hair_color'])
            draw.line([(cx - s(3), s(6)), (cx - s(1), s(6))], fill=eyebrow_color)
            # Eye
            draw.rectangle([cx - s(3), s(7), cx - s(1), s(9)], fill=(255, 255, 255))
            draw.point((cx - s(2), s(8)), fill=eye_color)
            # Mouth
            mouth_color = tuple(max(0, c - 30) for c in skin_color)
            draw.line([(cx - s(4), s(12)), (cx - s(2), s(12))], fill=mouth_color)

        # Side facial hair
        if params.get('has_facial_hair', False) and params.get('gender') == 'male':
            self._draw_facial_hair_side(draw, params)

    def _draw_facial_hair_side(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw facial hair in side profile."""
        hair_color = params['hair_color']
        facial_hair_color = tuple(max(0, c - 10) for c in hair_color)
        cx = self._center_x()
        s = self._s
        beard_type = params.get('beard_type', 'stubble')

        if beard_type == 'mustache':
            draw.line([(cx - s(4), s(10)), (cx - s(2), s(10))], fill=facial_hair_color)
        elif beard_type == 'goatee':
            draw.line([(cx - s(4), s(10)), (cx - s(2), s(10))], fill=facial_hair_color)
            draw.rectangle([cx - s(3), s(13), cx - s(1), s(15)], fill=facial_hair_color)
        elif beard_type == 'full_beard':
            draw.line([(cx - s(4), s(10)), (cx - s(2), s(10))], fill=facial_hair_color)
            draw.rectangle([cx - s(4), s(13), cx + s(1), s(16)], fill=facial_hair_color)
        elif beard_type == 'stubble':
            lighter_facial = tuple(min(255, c + 30) for c in facial_hair_color)
            for x in range(cx - s(4), cx, max(1, s(2))):
                for y in range(s(11), s(15), max(1, s(2))):
                    if (x + y) % 3 != 0:
                        draw.point((x, y), fill=lighter_facial)

    def draw_torso_side(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw torso in side profile - narrower (depth view ~60% of front)."""
        clothing = params['clothing']
        color = clothing['top_color']
        body_metrics = params['body_metrics']

        cx = self._center_x()
        s = self._s
        height_scale = body_metrics['height_scale']
        torso_width_scale = body_metrics['body_scales']['torso_width']
        depth_scale = body_metrics['body_scales'].get('depth', 0.6)

        base_torso_width = 16
        base_torso_height = 8
        torso_width = int(base_torso_width * torso_width_scale * depth_scale * self.scale)
        torso_height = int(base_torso_height * height_scale * self.scale)

        torso_y_start = int(17 * height_scale * self.scale)
        torso_y_end = torso_y_start + torso_height

        torso_y_start = max(s(10), min(int(self.height * 0.8), torso_y_start))
        torso_y_end = max(torso_y_start + s(5), min(self.height - 1, torso_y_end))

        torso_left = max(s(2), cx - torso_width // 2)
        torso_right = min(self.width - s(2), cx + torso_width // 2)

        draw.rectangle([torso_left, torso_y_start, torso_right, torso_y_end], fill=color)

        # Single sleeve (near arm only, facing left so right side)
        width_scale = body_metrics['body_scales']['width']
        sleeve_width = max(s(2), int(s(3) * width_scale))
        sleeve_height = max(s(3), int(s(6) * height_scale))
        sleeve_y_start_s = torso_y_start + s(1)
        sleeve_y_end_s = min(torso_y_end - s(1), sleeve_y_start_s + sleeve_height)

        # Only near arm sleeve (left side when facing left)
        near_sleeve_right = torso_left
        near_sleeve_left = max(s(1), near_sleeve_right - sleeve_width)
        draw.rectangle([near_sleeve_left, sleeve_y_start_s, near_sleeve_right, sleeve_y_end_s], fill=color)

    def draw_arms_side(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw single visible arm in side profile."""
        color = params['skin_color']
        cx = self._center_x()
        s = self._s

        # Only near arm visible (facing left)
        draw.rectangle([cx - s(7), s(23), cx - s(4), s(26)], fill=color)

    def draw_legs_side(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw legs in side profile - narrower, profile stance."""
        clothing = params['clothing']
        color = clothing['bottom_color']
        skin_color = params['skin_color']
        bottom_style = clothing['bottom_style']

        cx = self._center_x()
        s = self._s

        if bottom_style in ['skirt', 'pencil_skirt', 'expensive_skirt', 'dress']:
            draw.rectangle([cx - s(4), s(25), cx + s(4), s(28)], fill=color)
            draw.rectangle([cx - s(3), s(28), cx + s(1), s(31)], fill=skin_color)
        elif bottom_style in ['shorts']:
            draw.rectangle([cx - s(4), s(25), cx + s(2), s(27)], fill=color)
            draw.rectangle([cx - s(4), s(27), cx + s(2), s(31)], fill=skin_color)
        else:
            # Default pants side view - narrower
            draw.rectangle([cx - s(4), s(25), cx + s(2), s(31)], fill=color)

        # Shoes
        shoe_color = (0, 0, 0) if params['social_class'] in ['upper', 'rich'] else (139, 69, 19)
        draw.rectangle([cx - s(5), s(31), cx + s(2), s(32)], fill=shoe_color)

    def draw_accessories_side(self, draw: ImageDraw.ImageDraw, params: Dict):
        """Draw accessories in side profile."""
        cx = self._center_x()
        s = self._s

        # Glasses - single lens visible
        if params.get('has_glasses', False):
            glass_color = (0, 0, 0)
            draw.rectangle([cx - s(4), s(7), cx - s(1), s(9)], outline=glass_color)
            draw.line([(cx - s(4), s(8)), (cx - s(6), s(8))], fill=glass_color)

        # Earring on visible side only
        if params.get('has_jewelry', False):
            social_class = params['social_class']
            gender = params['gender']
            if social_class in ['upper', 'rich'] and gender == 'female':
                jewelry_color = (255, 215, 0)
                draw.point((cx + s(5), s(9)), fill=jewelry_color)

        # Hat
        if params.get('has_hat', False):
            hat_color = (139, 69, 19)
            if params['social_class'] == 'rich':
                hat_color = (25, 25, 112)
            elif params['social_class'] == 'poor':
                hat_color = (105, 105, 105)
            draw.rectangle([cx - s(5), s(1), cx + s(5), s(3)], fill=hat_color)
            if params.get('hat_style') == 'baseball_cap' or params['social_class'] == 'poor':
                draw.rectangle([cx - s(7), s(3), cx - s(2), s(4)], fill=hat_color)

    # ==================== FULL RENDER DISPATCHERS ====================

    def render_back(self, params: Dict) -> Image.Image:
        """Render full character from behind (UP direction)."""
        sprite = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(sprite)

        self.draw_legs_back(draw, params)
        self.draw_torso_back(draw, params)
        self.draw_arms_back(draw, params)
        self.draw_head_back(draw, params)
        self.draw_hair_back(draw, params)
        # No face drawing for back view
        self.draw_accessories_back(draw, params)

        return sprite

    def render_left(self, params: Dict) -> Image.Image:
        """Render full character facing left (LEFT direction)."""
        sprite = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(sprite)

        self.draw_legs_side(draw, params)
        self.draw_torso_side(draw, params)
        self.draw_arms_side(draw, params)
        self.draw_head_side(draw, params)
        self.draw_hair_side(draw, params)
        self.draw_face_side(draw, params)
        self.draw_accessories_side(draw, params)

        return sprite

    def render_right(self, params: Dict) -> Image.Image:
        """Render full character facing right (RIGHT direction) - mirror of left."""
        left_sprite = self.render_left(params)
        return left_sprite.transpose(Image.FLIP_LEFT_RIGHT)

    def render(self, params: Dict, direction: Direction) -> Image.Image:
        """Dispatch to the appropriate direction renderer."""
        if direction == Direction.UP:
            return self.render_back(params)
        elif direction == Direction.LEFT:
            return self.render_left(params)
        elif direction == Direction.RIGHT:
            return self.render_right(params)
        else:
            # DOWN is handled by the base PureCharacterGenerator
            raise ValueError("DOWN direction should use PureCharacterGenerator._render_character_with_params()")
