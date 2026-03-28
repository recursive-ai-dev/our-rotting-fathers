#!/usr/bin/env python3
"""
Pure Character Generator - Scalable sprite generator
Supports multiple resolutions: 32x32, 64x64, 128x128, etc.
All coordinates are normalized and scale with canvas size.
"""

import random
from PIL import Image, ImageDraw
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from .direction_renderer import Direction, DirectionRenderer

@dataclass
class ColorPalette:
    """Diverse, inclusive color palette for human representation"""
    skin_tones: List[Tuple[int, int, int]]
    hair_colors: List[Tuple[int, int, int]]
    clothing_colors: List[Tuple[int, int, int]]
    eye_colors: List[Tuple[int, int, int]]

class BodyPart(Enum):
    HEAD = "head"
    HAIR = "hair"
    FACE = "face"
    TORSO = "torso"
    LEGS = "legs"
    ARMS = "arms"

class PureCharacterGenerator:
    """Scalable character generator supporting multiple resolutions"""
    
    def __init__(self, canvas_size: Tuple[int, int] = (32, 32)):
        self.canvas_size = canvas_size
        self.width, self.height = canvas_size
        self.palette = self._create_inclusive_palette()
        
        # Base unit for scaling (normalized to 32x32 reference)
        self.base_size = 32
        self.scale_x = self.width / self.base_size
        self.scale_y = self.height / self.base_size
        self.scale = min(self.scale_x, self.scale_y)  # Uniform scale for proportions

        # Direction renderer for non-front views
        self.direction_renderer = DirectionRenderer(canvas_size=canvas_size)
    
    def _s(self, value: float) -> int:
        """Scale a coordinate value based on canvas size (using original 32x32 as reference)"""
        return int(value * self.scale)
    
    def _center_x(self) -> int:
        """Get horizontal center of canvas"""
        return self.width // 2
    
    def _center_y(self) -> int:
        """Get vertical center of canvas"""
        return self.height // 2
    
    def _create_inclusive_palette(self) -> ColorPalette:
        """Create a diverse, inclusive color palette"""
        return ColorPalette(
            skin_tones=[
                # European/Light tones
                (255, 220, 177), (241, 194, 125), (234, 192, 134),
                # East Asian tones  
                (243, 211, 171), (235, 195, 142),
                # South Asian tones
                (226, 183, 132), (198, 145, 88), (168, 117, 67),
                # Southeast Asian tones
                (228, 185, 130), (204, 155, 96), (180, 130, 76),
                # Indigenous tones
                (220, 175, 120), (195, 145, 85), (170, 120, 65),
                # African tones
                (141, 85, 36), (115, 65, 34), (92, 51, 23),
                # Hispanic/Latin tones
                (225, 180, 125), (200, 150, 95), (175, 125, 70),
                # Mixed heritage
                (215, 169, 127)
            ],
            hair_colors=[
                (15, 8, 4),       # Black
                (62, 39, 35),     # Dark brown
                (101, 67, 33),    # Brown
                (139, 90, 43),    # Light brown
                (184, 151, 120),  # Blonde
                (165, 42, 42),    # Red/Auburn
                (128, 128, 128),  # Gray
                (211, 211, 211)   # Silver/White
            ],
            clothing_colors=[
                (70, 130, 180),   # Steel blue
                (220, 20, 60),    # Crimson
                (34, 139, 34),    # Forest green
                (139, 69, 19),    # Brown
                (75, 0, 130),     # Purple
                (255, 140, 0),    # Orange
                (105, 105, 105),  # Gray
                (25, 25, 112),    # Navy
                (139, 0, 0),      # Dark red
                (0, 100, 0)       # Dark green
            ],
            eye_colors=[
                (101, 67, 33),    # Brown
                (139, 90, 43),    # Light brown
                (34, 139, 34),    # Green
                (70, 130, 180),   # Blue
                (128, 128, 128),  # Gray
                (160, 115, 67),   # Hazel
                (255, 191, 0)     # Amber
            ]
        )
    
    def set_canvas_size(self, size: Tuple[int, int]):
        """Change the canvas size and recalculate scales"""
        self.canvas_size = size
        self.width, self.height = size
        self.scale_x = self.width / self.base_size
        self.scale_y = self.height / self.base_size
        self.scale = min(self.scale_x, self.scale_y)
        self.direction_renderer.set_canvas_size(size)
    
    def generate_character(self, seed: Optional[int] = None) -> Image.Image:
        """Generate a single character sprite with full variation"""
        if seed is not None:
            random.seed(seed)
        
        params = self._generate_character_params()
        return self._render_character_with_params(params)
    
    def _generate_character_params(self) -> Dict:
        """Generate all parameters for a character"""
        # Basic attributes
        gender = random.choice(['male', 'female'])
        social_class = random.choice(['poor', 'working', 'middle', 'upper', 'rich'])
        
        # Choose colors
        skin_color = random.choice(self.palette.skin_tones)
        hair_color = random.choice(self.palette.hair_colors)
        eye_color = random.choice(self.palette.eye_colors)
        
        # Clothing based on social class and gender
        clothing = self._choose_clothing(social_class, gender)
        
        # Human lifecycle diversity - age affects everything
        age_category, actual_age = self._generate_age_category()
        
        # Human body diversity - realistic height and weight variations  
        height_category, body_type_category, body_metrics = self._generate_realistic_body_metrics(gender, social_class, age_category, actual_age)
        
        return {
            'skin_color': skin_color,
            'hair_color': hair_color,
            'eye_color': eye_color,
            'gender': gender,
            'social_class': social_class,
            'clothing': clothing,
            'hair_style': self._choose_hair_style(gender, social_class),
            'face_style': random.choice(['basic', 'detailed', 'minimal']),
            'body_type': random.choice(['slim', 'average', 'broad', 'curvy']),
            'has_glasses': random.random() < 0.2,
            'has_jewelry': random.random() < (0.1 if social_class == 'poor' else 0.6),
            'has_facial_hair': gender == 'male' and random.random() < 0.3,
            'beard_type': random.choice(['mustache', 'goatee', 'full_beard', 'stubble']),
            'has_hat': random.random() < 0.05,
            'hat_style': random.choice(['simple', 'baseball_cap']),
            # Enhanced human diversity
            'age_category': age_category,
            'actual_age': actual_age,
            'height_category': height_category,
            'weight_category': body_type_category,
            'body_metrics': body_metrics
        }
    
    def _render_character_with_params(self, params: Dict, direction: Direction = Direction.DOWN) -> Image.Image:
        """Render a character sprite using specific parameters"""
        # Non-front directions use the DirectionRenderer
        if direction != Direction.DOWN:
            self.direction_renderer.set_canvas_size(self.canvas_size)
            return self.direction_renderer.render(params, direction)

        # Create transparent canvas
        sprite = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(sprite)

        # Render character (bottom to top for proper layering)
        self._draw_legs(draw, params)
        self._draw_torso(draw, params)
        self._draw_arms(draw, params)
        self._draw_head(draw, params)
        self._draw_hair(draw, params)
        self._draw_face(draw, params)
        self._draw_accessories(draw, params)

        return sprite
    
    def _choose_clothing(self, social_class: str, gender: str) -> Dict:
        """Choose clothing based on social class and gender"""
        clothing_options = {
            'poor': {
                'male': {
                    'top': ['worn_tshirt', 'tank_top', 'hoodie'],
                    'bottom': ['worn_jeans', 'shorts', 'sweatpants'],
                    'colors': [(139, 69, 19), (105, 105, 105), (25, 25, 112), (139, 0, 0)]
                },
                'female': {
                    'top': ['worn_tshirt', 'tank_top', 'loose_shirt'],
                    'bottom': ['worn_jeans', 'shorts', 'skirt'],
                    'colors': [(139, 69, 19), (105, 105, 105), (25, 25, 112), (139, 0, 0)]
                }
            },
            'working': {
                'male': {
                    'top': ['basic_shirt', 'polo', 'work_shirt'],
                    'bottom': ['jeans', 'work_pants', 'khakis'],
                    'colors': [(70, 130, 180), (34, 139, 34), (139, 69, 19), (105, 105, 105)]
                },
                'female': {
                    'top': ['blouse', 'basic_shirt', 'sweater'],
                    'bottom': ['jeans', 'skirt', 'work_pants'],
                    'colors': [(70, 130, 180), (34, 139, 34), (220, 20, 60), (105, 105, 105)]
                }
            },
            'middle': {
                'male': {
                    'top': ['button_shirt', 'polo', 'sweater'],
                    'bottom': ['khakis', 'dress_pants', 'jeans'],
                    'colors': [(70, 130, 180), (34, 139, 34), (75, 0, 130), (139, 69, 19)]
                },
                'female': {
                    'top': ['blouse', 'sweater', 'nice_top'],
                    'bottom': ['dress_pants', 'skirt', 'nice_jeans'],
                    'colors': [(70, 130, 180), (220, 20, 60), (75, 0, 130), (34, 139, 34)]
                }
            },
            'upper': {
                'male': {
                    'top': ['dress_shirt', 'blazer', 'sweater_vest'],
                    'bottom': ['dress_pants', 'slacks', 'chinos'],
                    'colors': [(25, 25, 112), (139, 0, 0), (75, 0, 130), (105, 105, 105)]
                },
                'female': {
                    'top': ['blazer', 'elegant_blouse', 'cardigan'],
                    'bottom': ['dress_pants', 'pencil_skirt', 'dress'],
                    'colors': [(25, 25, 112), (139, 0, 0), (75, 0, 130), (220, 20, 60)]
                }
            },
            'rich': {
                'male': {
                    'top': ['expensive_shirt', 'suit_jacket', 'designer_sweater'],
                    'bottom': ['expensive_pants', 'suit_pants', 'designer_jeans'],
                    'colors': [(25, 25, 112), (0, 0, 0), (139, 0, 0), (105, 105, 105)]
                },
                'female': {
                    'top': ['designer_blouse', 'expensive_jacket', 'luxury_top'],
                    'bottom': ['designer_pants', 'expensive_skirt', 'luxury_dress'],
                    'colors': [(25, 25, 112), (0, 0, 0), (139, 0, 0), (75, 0, 130)]
                }
            }
        }
        
        class_options = clothing_options[social_class][gender]
        return {
            'top_style': random.choice(class_options['top']),
            'bottom_style': random.choice(class_options['bottom']),
            'top_color': random.choice(class_options['colors']),
            'bottom_color': random.choice(class_options['colors'])
        }
    
    def _choose_hair_style(self, gender: str, social_class: str) -> str:
        """Choose hair style based on gender and social class"""
        if gender == 'male':
            styles = {
                'poor': ['short_messy', 'buzzcut', 'unkempt', 'bald'],
                'working': ['short', 'crew_cut', 'basic_short'],
                'middle': ['styled_short', 'side_part', 'neat_short'],
                'upper': ['professional', 'slicked_back', 'executive_cut'],
                'rich': ['expensive_cut', 'styled_back', 'designer_short']
            }
        else:  # female
            styles = {
                'poor': ['long_messy', 'ponytail', 'unkempt_long', 'short_rough'],
                'working': ['ponytail', 'long', 'basic_short', 'simple_long'],
                'middle': ['styled_long', 'bob', 'layered', 'neat_ponytail'],
                'upper': ['professional_long', 'elegant_bob', 'styled_waves'],
                'rich': ['luxury_long', 'expensive_style', 'designer_cut', 'glamour_waves']
            }
        
        return random.choice(styles[social_class])
    
    def _generate_age_category(self) -> Tuple[str, int]:
        """Generate realistic age diversity across human lifespan"""
        # Age distribution based on demographics and story potential
        age_distribution = {
            'teenager': (0.15, 13, 19),      # Growing, awkward, energetic
            'young_adult': (0.35, 20, 34),   # Peak physical, college/early career
            'middle_aged': (0.35, 35, 54),   # Established, some decline
            'older_adult': (0.12, 55, 69),   # Pre-retirement, noticeable aging
            'elderly': (0.03, 70, 85)        # Retired, significant aging
        }
        
        # Select age category
        age_rand = random.random()
        age_cumulative = 0
        
        for category, (weight, min_age, max_age) in age_distribution.items():
            age_cumulative += weight
            if age_rand <= age_cumulative:
                actual_age = random.randint(min_age, max_age)
                return category, actual_age
        
        # Fallback
        return 'young_adult', random.randint(20, 34)
    
    def _generate_realistic_body_metrics(self, gender: str, social_class: str, age_category: str, actual_age: int) -> Tuple[str, str, Dict]:
        """Generate realistic human body diversity - height, weight, and proportions"""
        
        # Height distribution (inches) - based on real human data
        if gender == 'male':
            # US male height distribution: mean=69.1", std=2.9"
            height_weights = {
                'very_short': (0.05, 62, 66),    # Under 5'6" - 5%
                'short': (0.15, 66, 68),         # 5'6"-5'8" - 15%  
                'average': (0.60, 68, 71),       # 5'8"-5'11" - 60%
                'tall': (0.15, 71, 74),          # 5'11"-6'2" - 15%
                'very_tall': (0.05, 74, 78)      # Over 6'2" - 5%
            }
        else:  # female
            # US female height distribution: mean=63.7", std=2.7"
            height_weights = {
                'very_short': (0.05, 57, 60),    # Under 5'0" - 5%
                'short': (0.15, 60, 62),         # 5'0"-5'2" - 15%
                'average': (0.60, 62, 66),       # 5'2"-5'6" - 60%
                'tall': (0.15, 66, 69),          # 5'6"-5'9" - 15%
                'very_tall': (0.05, 69, 72)      # Over 5'9" - 5%
            }
        
        # Body type distribution - based on lifestyle, occupation, and genetics
        body_type_distribution = {
            'emaciated': 0.02,        # Extremely thin (homeless, severe illness)
            'very_thin': 0.08,        # Very underweight (runners, models)
            'lean_athletic': 0.15,    # Athletic build (swimmers, cyclists)
            'muscular_athletic': 0.12, # Jock/athlete (football, bodybuilder)
            'lean_normal': 0.20,      # Healthy normal weight
            'average': 0.25,          # Typical build
            'stocky': 0.08,           # Broad/thick (lumberjack, powerlifter)  
            'overweight': 0.07,       # Moderately overweight
            'obese': 0.03             # Significantly overweight
        }
        
        # Age affects body type distribution (biological reality)
        age_body_modifiers = {
            'teenager': {
                'very_thin': +0.10, 'lean_normal': +0.05, 'lean_athletic': +0.08,
                'average': -0.05, 'overweight': -0.05, 'obese': -0.03, 'stocky': -0.02
            },
            'young_adult': {
                'lean_athletic': +0.10, 'muscular_athletic': +0.05, 'lean_normal': +0.05,
                'overweight': -0.03, 'obese': -0.02
            },
            'middle_aged': {
                'average': +0.08, 'overweight': +0.05, 'stocky': +0.03,
                'lean_athletic': -0.05, 'muscular_athletic': -0.03, 'very_thin': -0.02
            },
            'older_adult': {
                'average': +0.05, 'overweight': +0.08, 'very_thin': +0.03,
                'lean_athletic': -0.08, 'muscular_athletic': -0.05, 'stocky': -0.02
            },
            'elderly': {
                'very_thin': +0.15, 'average': +0.05, 'overweight': +0.02,
                'lean_athletic': -0.10, 'muscular_athletic': -0.08, 'stocky': -0.05, 'obese': -0.03
            }
        }
        
        # Social class affects body type distribution (lifestyle and access to resources)
        class_body_modifiers = {
            'poor': {
                'emaciated': +0.03, 'very_thin': +0.05, 'average': +0.05,
                'overweight': +0.02, 'obese': +0.02,
                'lean_athletic': -0.08, 'muscular_athletic': -0.05, 'stocky': -0.02
            },
            'working': {
                'stocky': +0.05, 'muscular_athletic': +0.03, 'average': +0.02,
                'lean_athletic': -0.02, 'very_thin': -0.03, 'emaciated': -0.01
            },
            'middle': {
                'lean_normal': +0.05, 'lean_athletic': +0.03, 
                'emaciated': -0.01, 'obese': -0.01
            },  # baseline with slight health bias
            'upper': {
                'lean_athletic': +0.08, 'lean_normal': +0.05, 'muscular_athletic': +0.02,
                'overweight': -0.03, 'obese': -0.02, 'emaciated': -0.01
            },
            'rich': {
                'lean_athletic': +0.10, 'lean_normal': +0.08, 'muscular_athletic': +0.03,
                'overweight': -0.05, 'obese': -0.03, 'emaciated': -0.02, 'very_thin': -0.02
            }
        }
        
        # Adjust body type distribution by age and social class
        adjusted_body_types = body_type_distribution.copy()
        
        # Apply age modifiers first
        if age_category in age_body_modifiers:
            for body_type, modifier in age_body_modifiers[age_category].items():
                if body_type in adjusted_body_types:
                    adjusted_body_types[body_type] = max(0.01, adjusted_body_types[body_type] + modifier)
        
        # Then apply social class modifiers
        if social_class in class_body_modifiers:
            for body_type, modifier in class_body_modifiers[social_class].items():
                if body_type in adjusted_body_types:
                    adjusted_body_types[body_type] = max(0.01, adjusted_body_types[body_type] + modifier)
        
        # Normalize to sum to 1.0
        total = sum(adjusted_body_types.values())
        adjusted_body_types = {k: v/total for k, v in adjusted_body_types.items()}
        
        # Select height category
        height_rand = random.random()
        height_cumulative = 0
        height_category = 'average'
        height_inches = 69.0  # Default fallback
        
        for category, (weight, min_h, max_h) in height_weights.items():
            height_cumulative += weight
            if height_rand <= height_cumulative:
                height_category = category
                height_inches = random.uniform(min_h, max_h)
                break
        
        # Ensure height_inches is properly set (should always happen in loop above)
        
        # Select body type category
        body_rand = random.random()
        body_cumulative = 0
        body_type_category = 'average'
        
        for body_type, weight in adjusted_body_types.items():
            body_cumulative += weight
            if body_rand <= body_cumulative:
                body_type_category = body_type
                break
        
        # Calculate actual measurements
        height_feet = int(height_inches // 12)
        height_remaining_inches = int(height_inches % 12)
        
        # BMI and weight calculation based on body type
        body_type_specs = {
            'emaciated': {'bmi_range': (13.0, 16.5), 'muscle_mass': 0.1, 'body_fat': 0.05},
            'very_thin': {'bmi_range': (16.5, 18.4), 'muscle_mass': 0.3, 'body_fat': 0.08},
            'lean_athletic': {'bmi_range': (18.5, 23.0), 'muscle_mass': 0.8, 'body_fat': 0.12},
            'muscular_athletic': {'bmi_range': (23.0, 28.0), 'muscle_mass': 1.2, 'body_fat': 0.10},
            'lean_normal': {'bmi_range': (18.5, 24.0), 'muscle_mass': 0.5, 'body_fat': 0.15},
            'average': {'bmi_range': (20.0, 26.0), 'muscle_mass': 0.4, 'body_fat': 0.20},
            'stocky': {'bmi_range': (24.0, 30.0), 'muscle_mass': 0.9, 'body_fat': 0.18},
            'overweight': {'bmi_range': (26.0, 32.0), 'muscle_mass': 0.3, 'body_fat': 0.30},
            'obese': {'bmi_range': (30.0, 40.0), 'muscle_mass': 0.2, 'body_fat': 0.40}
        }
        
        body_spec = body_type_specs[body_type_category]
        bmi_min, bmi_max = body_spec['bmi_range']
        bmi = random.uniform(bmi_min, bmi_max)
        weight_pounds = int((bmi * (height_inches ** 2)) / 703)
        
        # Ensure realistic weight bounds (sanity check)
        min_possible_weight = max(80, int((16 * (height_inches ** 2)) / 703))  # BMI 16 minimum
        max_possible_weight = min(500, int((50 * (height_inches ** 2)) / 703))  # BMI 50 maximum
        weight_pounds = max(min_possible_weight, min(max_possible_weight, weight_pounds))
        
        # Calculate sprite scaling factors (using base 32x32 as reference)
        # Height affects overall sprite scale
        height_scale_factors = {
            'very_short': 0.75,   # 24 pixels tall
            'short': 0.85,        # 27 pixels tall  
            'average': 1.0,       # 32 pixels tall (base)
            'tall': 1.15,         # Proportions change
            'very_tall': 1.25     # Proportions change
        }
        
        # Body type affects proportions and build
        body_type_scale_factors = {
            'emaciated': {'width': 0.6, 'torso_width': 0.5, 'head_size': 1.0, 'shoulder_width': 0.7, 'depth': 0.5},
            'very_thin': {'width': 0.75, 'torso_width': 0.7, 'head_size': 0.95, 'shoulder_width': 0.85, 'depth': 0.55},
            'lean_athletic': {'width': 0.9, 'torso_width': 0.85, 'head_size': 0.95, 'shoulder_width': 1.1, 'depth': 0.6},
            'muscular_athletic': {'width': 1.2, 'torso_width': 1.1, 'head_size': 1.0, 'shoulder_width': 1.4, 'depth': 0.7},
            'lean_normal': {'width': 0.95, 'torso_width': 0.9, 'head_size': 1.0, 'shoulder_width': 1.0, 'depth': 0.6},
            'average': {'width': 1.0, 'torso_width': 1.0, 'head_size': 1.0, 'shoulder_width': 1.0, 'depth': 0.6},
            'stocky': {'width': 1.3, 'torso_width': 1.2, 'head_size': 1.0, 'shoulder_width': 1.3, 'depth': 0.7},
            'overweight': {'width': 1.4, 'torso_width': 1.5, 'head_size': 1.05, 'shoulder_width': 1.1, 'depth': 0.75},
            'obese': {'width': 1.7, 'torso_width': 1.8, 'head_size': 1.1, 'shoulder_width': 1.0, 'depth': 0.8}
        }
        
        body_metrics = {
            'height_inches': height_inches,
            'height_feet': height_feet,
            'height_remaining_inches': height_remaining_inches,
            'weight_pounds': weight_pounds,
            'bmi': bmi,
            'height_scale': height_scale_factors[height_category],
            'body_scales': body_type_scale_factors[body_type_category],
            'muscle_mass': body_spec['muscle_mass'],
            'body_fat': body_spec['body_fat'],
            'height_display': f"{height_feet}'{height_remaining_inches}\"",
            'weight_display': f"{weight_pounds} lbs",
            'bmi_display': f"BMI {bmi:.1f}",
            'body_type_display': body_type_category.replace('_', ' ').title(),
            'age_display': f"{actual_age} years old"
        }
        
        return height_category, body_type_category, body_metrics
    
    # ==================== DRAWING METHODS (SCALABLE) ====================
    
    def _draw_head(self, draw: ImageDraw, params: Dict):
        """Draw character head with realistic proportions"""
        color = params['skin_color']
        body_metrics = params['body_metrics']
        
        # Apply height and body type scaling
        height_scale = body_metrics['height_scale'] 
        head_size_modifier = body_metrics['body_scales']['head_size']
        width_modifier = body_metrics['body_scales']['width']
        
        # Base head coordinates (normalized to 32x32 reference)
        # Head: 9-23 x, 3-17 y in 32x32 space
        base_head_width = 14  # 23 - 9
        base_head_height = 14  # 17 - 3
        
        # Calculate scaled dimensions
        head_width = int(base_head_width * head_size_modifier * width_modifier * self.scale)
        head_height = int(base_head_height * head_size_modifier * self.scale)
        
        # Center the head
        center_x = self._center_x()
        center_y = int(10 * height_scale * self.scale)
        
        left = center_x - head_width // 2
        right = center_x + head_width // 2
        top = center_y - head_height // 2  
        bottom = center_y + head_height // 2
        
        # Ensure head stays within bounds
        left = max(1, left)
        right = min(self.width - 1, right)
        top = max(1, top)
        bottom = min(self.height - 1, bottom)
        
        draw.ellipse([left, top, right, bottom], fill=color)
    
    def _draw_hair(self, draw: ImageDraw, params: Dict):
        """Draw hair based on style, gender, and social class.
        Uses ellipses, polygons, and tapered shapes for organic-looking hair."""
        color = params['hair_color']
        style = params['hair_style']
        darker = tuple(max(0, c - 20) for c in color)
        lighter = tuple(min(255, c + 25) for c in color)

        cx = self._center_x()
        s = self._s  # Scale helper

        # Male hair styles
        if style in ['bald']:
            return
        elif style in ['short', 'basic_short', 'crew_cut']:
            # Rounded cap on top of head, tapered sideburns
            draw.ellipse([cx - s(7), s(1), cx + s(7), s(8)], fill=color)
            # Sideburns taper down
            draw.polygon([
                (cx - s(7), s(5)), (cx - s(8), s(5)),
                (cx - s(7), s(9)), (cx - s(6), s(8))
            ], fill=color)
            draw.polygon([
                (cx + s(7), s(5)), (cx + s(8), s(5)),
                (cx + s(7), s(9)), (cx + s(6), s(8))
            ], fill=color)
        elif style in ['short_messy', 'unkempt']:
            # Irregular rounded mass with spiky bits
            draw.ellipse([cx - s(8), s(0), cx + s(8), s(8)], fill=color)
            # Spiky tufts on top
            for offset in [-s(5), -s(2), s(1), s(4)]:
                draw.polygon([
                    (cx + offset, s(1)),
                    (cx + offset - s(1), s(3)),
                    (cx + offset + s(1), s(3))
                ], fill=lighter)
            # Messy sideburns
            draw.polygon([
                (cx - s(8), s(4)), (cx - s(9), s(6)),
                (cx - s(7), s(9)), (cx - s(7), s(5))
            ], fill=color)
            draw.polygon([
                (cx + s(8), s(4)), (cx + s(9), s(6)),
                (cx + s(7), s(9)), (cx + s(7), s(5))
            ], fill=color)
        elif style in ['buzzcut']:
            # Very thin rounded cap, barely visible
            draw.ellipse([cx - s(7), s(2), cx + s(7), s(6)], fill=color)
            # Subtle texture dots
            for offset in [-s(4), -s(1), s(2), s(5)]:
                draw.point((cx + offset, s(3)), fill=darker)
        elif style in ['styled_short', 'side_part', 'neat_short']:
            # Rounded top with volume, clean sideburns, side part
            draw.ellipse([cx - s(7), s(1), cx + s(7), s(8)], fill=color)
            # Slight volume bump on part side
            draw.ellipse([cx - s(7), s(0), cx + s(2), s(6)], fill=color)
            # Clean sideburns
            draw.polygon([
                (cx - s(7), s(5)), (cx - s(8), s(5)),
                (cx - s(7), s(8)), (cx - s(6), s(7))
            ], fill=color)
            draw.polygon([
                (cx + s(7), s(5)), (cx + s(8), s(5)),
                (cx + s(7), s(8)), (cx + s(6), s(7))
            ], fill=color)
            # Side part line
            draw.line([(cx - s(2), s(2)), (cx - s(2), s(5))], fill=darker)
        elif style in ['professional', 'slicked_back', 'executive_cut']:
            # Swept-back rounded shape with volume
            draw.ellipse([cx - s(8), s(1), cx + s(8), s(7)], fill=color)
            # Swept-back contour (darker at edges)
            draw.arc([cx - s(8), s(1), cx + s(8), s(7)], 200, 340, fill=darker)
            # Tapered sides
            draw.polygon([
                (cx - s(8), s(4)), (cx - s(8), s(7)),
                (cx - s(7), s(7))
            ], fill=color)
            draw.polygon([
                (cx + s(8), s(4)), (cx + s(8), s(7)),
                (cx + s(7), s(7))
            ], fill=color)
        elif style in ['expensive_cut', 'styled_back', 'designer_short']:
            # Voluminous top, sculpted sides
            draw.ellipse([cx - s(8), s(0), cx + s(8), s(7)], fill=color)
            # Extra volume on top
            draw.ellipse([cx - s(5), s(-1), cx + s(5), s(5)], fill=color)
            # Styled highlights
            draw.ellipse([cx - s(4), s(0), cx + s(1), s(4)], fill=lighter)
            # Clean sides
            draw.polygon([
                (cx - s(8), s(4)), (cx - s(8), s(7)),
                (cx - s(7), s(6))
            ], fill=color)
            draw.polygon([
                (cx + s(8), s(4)), (cx + s(8), s(7)),
                (cx + s(7), s(6))
            ], fill=color)

        # Female hair styles
        elif style in ['long', 'simple_long']:
            # Rounded top flowing into long side curtains
            draw.ellipse([cx - s(9), s(1), cx + s(9), s(8)], fill=color)
            # Flowing sides that taper toward bottom
            draw.polygon([
                (cx - s(9), s(5)), (cx - s(10), s(8)),
                (cx - s(9), s(20)), (cx - s(7), s(18)),
                (cx - s(8), s(6))
            ], fill=color)
            draw.polygon([
                (cx + s(9), s(5)), (cx + s(10), s(8)),
                (cx + s(9), s(20)), (cx + s(7), s(18)),
                (cx + s(8), s(6))
            ], fill=color)
        elif style in ['long_messy', 'unkempt_long']:
            # Wild rounded mass on top, uneven long sides
            draw.ellipse([cx - s(10), s(0), cx + s(10), s(9)], fill=color)
            # Uneven flowing sides
            draw.polygon([
                (cx - s(10), s(5)), (cx - s(11), s(9)),
                (cx - s(10), s(22)), (cx - s(8), s(19)),
                (cx - s(9), s(6))
            ], fill=color)
            draw.polygon([
                (cx + s(10), s(5)), (cx + s(11), s(9)),
                (cx + s(10), s(20)), (cx + s(8), s(18)),
                (cx + s(9), s(6))
            ], fill=color)
            # Wispy strands
            for offset in [-s(6), -s(2), s(3), s(7)]:
                draw.line([(cx + offset, s(0)), (cx + offset, s(2))], fill=lighter)
        elif style in ['ponytail', 'neat_ponytail']:
            # Smooth rounded top pulled back, ponytail behind
            draw.ellipse([cx - s(7), s(1), cx + s(7), s(8)], fill=color)
            # Slight sideburns
            draw.polygon([
                (cx - s(7), s(5)), (cx - s(8), s(5)),
                (cx - s(7), s(8))
            ], fill=color)
            draw.polygon([
                (cx + s(7), s(5)), (cx + s(8), s(5)),
                (cx + s(7), s(8))
            ], fill=color)
            # Ponytail (tapered oval behind head)
            draw.ellipse([cx - s(2), s(14), cx + s(2), s(24)], fill=color)
            # Hair tie
            draw.line([(cx - s(2), s(15)), (cx + s(2), s(15))], fill=darker)
        elif style in ['bob', 'elegant_bob']:
            # Rounded volumous top curving into chin-length sides
            draw.ellipse([cx - s(9), s(0), cx + s(9), s(9)], fill=color)
            # Bob sides curve inward at bottom
            draw.polygon([
                (cx - s(9), s(5)), (cx - s(10), s(7)),
                (cx - s(9), s(12)), (cx - s(7), s(11)),
                (cx - s(8), s(6))
            ], fill=color)
            draw.polygon([
                (cx + s(9), s(5)), (cx + s(10), s(7)),
                (cx + s(9), s(12)), (cx + s(7), s(11)),
                (cx + s(8), s(6))
            ], fill=color)
            # Rounded ends
            draw.ellipse([cx - s(10), s(10), cx - s(7), s(13)], fill=color)
            draw.ellipse([cx + s(7), s(10), cx + s(10), s(13)], fill=color)
        elif style in ['styled_long', 'layered']:
            # Rounded top with layered flowing sides
            draw.ellipse([cx - s(9), s(1), cx + s(9), s(8)], fill=color)
            # Layered sides - outer layer
            draw.polygon([
                (cx - s(9), s(5)), (cx - s(10), s(8)),
                (cx - s(9), s(18)), (cx - s(7), s(16)),
                (cx - s(8), s(6))
            ], fill=color)
            draw.polygon([
                (cx + s(9), s(5)), (cx + s(10), s(8)),
                (cx + s(9), s(18)), (cx + s(7), s(16)),
                (cx + s(8), s(6))
            ], fill=color)
            # Inner layer highlights
            draw.polygon([
                (cx - s(9), s(9)), (cx - s(9), s(16)),
                (cx - s(7), s(14))
            ], fill=lighter)
            draw.polygon([
                (cx + s(9), s(9)), (cx + s(9), s(16)),
                (cx + s(7), s(14))
            ], fill=lighter)
        elif style in ['professional_long', 'styled_waves']:
            # Smooth rounded shape with gentle wave texture
            draw.ellipse([cx - s(9), s(1), cx + s(9), s(8)], fill=color)
            # Flowing wavy sides
            draw.polygon([
                (cx - s(9), s(5)), (cx - s(10), s(7)),
                (cx - s(9), s(16)), (cx - s(7), s(14)),
                (cx - s(8), s(6))
            ], fill=color)
            draw.polygon([
                (cx + s(9), s(5)), (cx + s(10), s(7)),
                (cx + s(9), s(16)), (cx + s(7), s(14)),
                (cx + s(8), s(6))
            ], fill=color)
            # Wave bumps along sides
            for y_off in [s(9), s(12)]:
                draw.ellipse([cx - s(11), y_off - s(1), cx - s(8), y_off + s(1)], fill=color)
                draw.ellipse([cx + s(8), y_off - s(1), cx + s(11), y_off + s(1)], fill=color)
        elif style in ['luxury_long', 'expensive_style', 'designer_cut', 'glamour_waves']:
            # Full voluminous rounded top, flowing glamorous sides
            draw.ellipse([cx - s(10), s(0), cx + s(10), s(9)], fill=color)
            # Flowing sides with body
            draw.polygon([
                (cx - s(10), s(5)), (cx - s(11), s(8)),
                (cx - s(10), s(20)), (cx - s(8), s(18)),
                (cx - s(9), s(6))
            ], fill=color)
            draw.polygon([
                (cx + s(10), s(5)), (cx + s(11), s(8)),
                (cx + s(10), s(20)), (cx + s(8), s(18)),
                (cx + s(9), s(6))
            ], fill=color)
            # Glamour highlights
            draw.ellipse([cx - s(6), s(1), cx - s(2), s(5)], fill=lighter)
            draw.ellipse([cx + s(2), s(1), cx + s(6), s(5)], fill=lighter)
        elif style in ['short_rough', 'basic_short']:
            # Rough rounded cap with slight texture
            draw.ellipse([cx - s(7), s(1), cx + s(7), s(8)], fill=color)
            # Slight sideburns
            draw.polygon([
                (cx - s(7), s(5)), (cx - s(8), s(5)),
                (cx - s(7), s(9)), (cx - s(6), s(8))
            ], fill=color)
            draw.polygon([
                (cx + s(7), s(5)), (cx + s(8), s(5)),
                (cx + s(7), s(9)), (cx + s(6), s(8))
            ], fill=color)
    
    def _draw_face(self, draw: ImageDraw, params: Dict):
        """Draw facial features"""
        style = params['face_style']
        eye_color = params['eye_color']
        skin_color = params['skin_color']
        
        cx = self._center_x()
        s = self._s
        
        if style == 'minimal':
            # Simple dots for eyes
            draw.point((cx - s(3), s(8)), fill=eye_color)
            draw.point((cx + s(3), s(8)), fill=eye_color)
            # Simple mouth
            draw.line([(cx - s(1), s(12)), (cx + s(1), s(12))], fill=(0, 0, 0))
            
        elif style == 'basic':
            # Eyes with whites
            draw.rectangle([cx - s(4), s(7), cx - s(2), s(9)], fill=(255, 255, 255))
            draw.rectangle([cx + s(2), s(7), cx + s(4), s(9)], fill=(255, 255, 255))
            draw.point((cx - s(3), s(8)), fill=eye_color)
            draw.point((cx + s(3), s(8)), fill=eye_color)
            
            # Nose
            nose_color = tuple(max(0, c - 15) for c in skin_color)
            draw.point((cx, s(10)), fill=nose_color)
            
            # Mouth
            mouth_color = tuple(max(0, c - 30) for c in skin_color)
            draw.line([(cx - s(2), s(12)), (cx + s(2), s(12))], fill=mouth_color)
            
        elif style == 'detailed':
            # Detailed eyes with eyebrows
            eyebrow_color = tuple(max(0, c - 40) for c in params['hair_color'])
            draw.line([(cx - s(4), s(6)), (cx - s(1), s(6))], fill=eyebrow_color)
            draw.line([(cx + s(1), s(6)), (cx + s(4), s(6))], fill=eyebrow_color)
            
            # Eyes
            draw.rectangle([cx - s(4), s(7), cx - s(1), s(9)], fill=(255, 255, 255))
            draw.rectangle([cx + s(1), s(7), cx + s(4), s(9)], fill=(255, 255, 255))
            draw.point((cx - s(3), s(8)), fill=eye_color)
            draw.point((cx + s(3), s(8)), fill=eye_color)
            
            # Nose with nostrils
            nose_color = tuple(max(0, c - 15) for c in skin_color)
            draw.line([(cx, s(9)), (cx, s(11))], fill=nose_color)
            draw.point((cx - s(1), s(11)), fill=nose_color)
            draw.point((cx + s(1), s(11)), fill=nose_color)
            
            # Mouth with slight smile
            mouth_color = tuple(max(0, c - 30) for c in skin_color)
            draw.line([(cx - s(2), s(12)), (cx + s(2), s(12))], fill=mouth_color)
            draw.point((cx - s(3), s(13)), fill=mouth_color)
            draw.point((cx + s(3), s(13)), fill=mouth_color)
        
        # Add facial hair for males
        if params.get('has_facial_hair', False) and params.get('gender') == 'male':
            self._draw_facial_hair(draw, params)
    
    def _draw_facial_hair(self, draw: ImageDraw, params: Dict):
        """Draw facial hair for males"""
        hair_color = params['hair_color']
        facial_hair_color = tuple(max(0, c - 10) for c in hair_color)
        
        cx = self._center_x()
        s = self._s
        
        # Beard styles (use stored param for deterministic rendering across frames)
        beard_type = params.get('beard_type', 'stubble')
        
        if beard_type == 'mustache':
            draw.line([(cx - s(3), s(10)), (cx + s(3), s(10))], fill=facial_hair_color)
        elif beard_type == 'goatee':
            draw.line([(cx - s(3), s(10)), (cx + s(3), s(10))], fill=facial_hair_color)  # Mustache
            draw.rectangle([cx - s(2), s(13), cx + s(2), s(15)], fill=facial_hair_color)  # Goatee
        elif beard_type == 'full_beard':
            draw.line([(cx - s(3), s(10)), (cx + s(3), s(10))], fill=facial_hair_color)  # Mustache
            draw.rectangle([cx - s(5), s(13), cx + s(5), s(16)], fill=facial_hair_color)  # Full beard
        elif beard_type == 'stubble':
            # Light stubble with dots (deterministic pattern based on position)
            lighter_facial = tuple(min(255, c + 30) for c in facial_hair_color)
            for x in range(cx - s(4), cx + s(4), max(1, s(2))):
                for y in range(s(11), s(15), max(1, s(2))):
                    if (x + y) % 3 != 0:  # Deterministic pattern
                        draw.point((x, y), fill=lighter_facial)
    
    def _draw_torso(self, draw: ImageDraw, params: Dict):
        """Draw clothing based on style, gender, and body metrics"""
        clothing = params['clothing']
        top_style = clothing['top_style']
        color = clothing['top_color']
        gender = params['gender']
        body_metrics = params['body_metrics']
        
        cx = self._center_x()
        s = self._s
        
        # Apply body scaling
        height_scale = body_metrics['height_scale']
        torso_width_scale = body_metrics['body_scales']['torso_width'] 
        width_scale = body_metrics['body_scales']['width']
        shoulder_width_scale = body_metrics['body_scales']['shoulder_width']
        
        # Calculate torso dimensions
        base_torso_width = 16  # Base width
        base_torso_height = 8  # Base height
        
        torso_width = int(base_torso_width * torso_width_scale * self.scale)
        torso_height = int(base_torso_height * height_scale * self.scale)
        
        # Position torso based on height
        torso_y_start = int(17 * height_scale * self.scale)
        torso_y_end = torso_y_start + torso_height
        
        # Ensure within bounds
        torso_y_start = max(s(10), min(int(self.height * 0.8), torso_y_start))
        torso_y_end = max(torso_y_start + s(5), min(self.height - 1, torso_y_end))
        
        # Calculate torso bounds
        torso_left = cx - torso_width // 2
        torso_right = cx + torso_width // 2
        
        # Ensure within sprite bounds
        torso_left = max(s(2), torso_left)
        torso_right = min(self.width - s(2), torso_right)
        
        # Main torso
        if gender == 'female' and params['body_type'] == 'curvy':
            # Slightly curved torso for women, adjusted for weight
            draw.rectangle([torso_left, torso_y_start, torso_right, torso_y_end], fill=color)
        else:
            # Standard torso with weight scaling
            draw.rectangle([torso_left, torso_y_start, torso_right, torso_y_end], fill=color)
        
        # Sleeves (scale with body width)  
        sleeve_width = max(s(2), int(s(3) * width_scale))
        sleeve_height = max(s(3), int(s(6) * height_scale))
        sleeve_y_start = torso_y_start + s(1)
        sleeve_y_end = min(torso_y_end - s(1), sleeve_y_start + sleeve_height)
        
        # Left sleeve
        left_sleeve_right = torso_left
        left_sleeve_left = max(s(1), left_sleeve_right - sleeve_width)
        draw.rectangle([left_sleeve_left, sleeve_y_start, left_sleeve_right, sleeve_y_end], fill=color)
        
        # Right sleeve  
        right_sleeve_left = torso_right
        right_sleeve_right = min(self.width - s(1), right_sleeve_left + sleeve_width)
        draw.rectangle([right_sleeve_left, sleeve_y_start, right_sleeve_right, sleeve_y_end], fill=color)
        
        # Style-specific details
        if top_style in ['worn_tshirt', 'basic_shirt']:
            # Simple t-shirt - already drawn
            pass
        elif top_style == 'tank_top':
            # No sleeves for tank top
            draw.rectangle([cx - s(6), s(17), cx + s(6), s(25)], fill=color)
        elif top_style in ['hoodie']:
            # Add hood outline
            hood_color = tuple(max(0, c - 20) for c in color)
            draw.rectangle([cx - s(6), s(15), cx + s(6), s(17)], fill=hood_color)
        elif top_style in ['polo', 'blouse']:
            # Add collar
            collar_color = tuple(max(0, c - 15) for c in color)
            draw.rectangle([cx - s(2), s(17), cx + s(2), s(18)], fill=collar_color)
        elif top_style in ['button_shirt', 'dress_shirt']:
            # Add buttons
            button_color = (255, 255, 255)
            for y in range(s(18), s(24), max(1, s(2))):
                draw.point((cx, y), fill=button_color)
        elif top_style in ['blazer', 'suit_jacket', 'expensive_jacket']:
            # Add lapels and buttons
            lapel_color = tuple(max(0, c - 25) for c in color)
            draw.line([(cx - s(6), s(17)), (cx - s(2), s(20))], fill=lapel_color)
            draw.line([(cx + s(6), s(17)), (cx + s(2), s(20))], fill=lapel_color)
            # Expensive buttons
            button_color = (255, 215, 0) if 'expensive' in top_style else (200, 200, 200)
            draw.point((cx - s(1), s(19)), fill=button_color)
            draw.point((cx - s(1), s(22)), fill=button_color)
        elif top_style in ['sweater', 'cardigan', 'designer_sweater']:
            # Add texture with slightly different color
            texture_color = tuple(min(255, c + 10) for c in color)
            for x in range(cx - s(7), cx + s(7), max(1, s(3))):
                draw.line([(x, s(18)), (x, s(24))], fill=texture_color)
    
    def _draw_arms(self, draw: ImageDraw, params: Dict):
        """Draw arms"""
        color = params['skin_color']
        cx = self._center_x()
        s = self._s
        
        # Left arm
        draw.rectangle([cx - s(11), s(23), cx - s(8), s(26)], fill=color)
        # Right arm  
        draw.rectangle([cx + s(8), s(23), cx + s(11), s(26)], fill=color)
    
    def _draw_legs(self, draw: ImageDraw, params: Dict):
        """Draw legs/bottoms based on style and gender"""
        clothing = params['clothing']
        bottom_style = clothing['bottom_style']
        color = clothing['bottom_color']
        skin_color = params['skin_color']
        gender = params['gender']
        
        cx = self._center_x()
        s = self._s
        
        # Different bottom styles
        if bottom_style in ['skirt', 'pencil_skirt', 'expensive_skirt']:
            # Draw skirt
            if bottom_style == 'pencil_skirt':
                # Tight pencil skirt
                draw.rectangle([cx - s(5), s(25), cx + s(5), s(29)], fill=color)
            else:
                # Regular skirt
                draw.rectangle([cx - s(7), s(25), cx + s(7), s(28)], fill=color)
            # Legs showing below skirt
            draw.rectangle([cx - s(5), s(28), cx - s(2), s(31)], fill=skin_color)  # Left leg
            draw.rectangle([cx + s(2), s(28), cx + s(5), s(31)], fill=skin_color)  # Right leg
        elif bottom_style in ['dress']:
            # Draw dress (extends from torso)
            draw.rectangle([cx - s(7), s(25), cx + s(7), s(30)], fill=color)
            # Legs showing below dress
            draw.rectangle([cx - s(5), s(30), cx - s(2), s(31)], fill=skin_color)
            draw.rectangle([cx + s(2), s(30), cx + s(5), s(31)], fill=skin_color)
        elif bottom_style in ['shorts']:
            # Short pants
            draw.rectangle([cx - s(6), s(25), cx - s(1), s(27)], fill=color)  # Left leg
            draw.rectangle([cx + s(1), s(25), cx + s(6), s(27)], fill=color)  # Right leg
            # Exposed legs
            draw.rectangle([cx - s(6), s(27), cx - s(1), s(31)], fill=skin_color)
            draw.rectangle([cx + s(1), s(27), cx + s(6), s(31)], fill=skin_color)
        elif bottom_style in ['worn_jeans', 'jeans', 'nice_jeans']:
            # Regular jeans
            draw.rectangle([cx - s(6), s(25), cx - s(1), s(31)], fill=color)
            draw.rectangle([cx + s(1), s(25), cx + s(6), s(31)], fill=color)
            # Add seam lines for jeans
            seam_color = tuple(max(0, c - 30) for c in color)
            draw.line([(cx - s(4), s(25)), (cx - s(4), s(31))], fill=seam_color)
            draw.line([(cx + s(4), s(25)), (cx + s(4), s(31))], fill=seam_color)
            # Worn patches for worn jeans
            if 'worn' in bottom_style:
                patch_color = tuple(min(255, c + 20) for c in color)
                draw.point((cx - s(5), s(27)), fill=patch_color)
                draw.point((cx + s(4), s(28)), fill=patch_color)
        elif bottom_style in ['sweatpants']:
            # Loose sweatpants
            draw.rectangle([cx - s(7), s(25), cx, s(31)], fill=color)
            draw.rectangle([cx, s(25), cx + s(7), s(31)], fill=color)
        elif bottom_style in ['dress_pants', 'slacks', 'expensive_pants', 'suit_pants']:
            # Formal pants
            draw.rectangle([cx - s(6), s(25), cx - s(1), s(31)], fill=color)
            draw.rectangle([cx + s(1), s(25), cx + s(6), s(31)], fill=color)
            # Add crease for formal pants
            crease_color = tuple(max(0, c - 15) for c in color)
            draw.line([(cx - s(4), s(25)), (cx - s(4), s(31))], fill=crease_color)
            draw.line([(cx + s(4), s(25)), (cx + s(4), s(31))], fill=crease_color)
            # Gold details for expensive pants
            if 'expensive' in bottom_style or 'suit' in bottom_style:
                accent_color = (255, 215, 0)
                draw.point((cx - s(5), s(25)), fill=accent_color)
                draw.point((cx + s(4), s(25)), fill=accent_color)
        else:
            # Default pants
            draw.rectangle([cx - s(6), s(25), cx - s(1), s(31)], fill=color)
            draw.rectangle([cx + s(1), s(25), cx + s(6), s(31)], fill=color)
        
        # Feet/shoes
        shoe_color = (0, 0, 0) if params['social_class'] in ['upper', 'rich'] else (139, 69, 19)
        if bottom_style not in ['skirt', 'dress', 'pencil_skirt', 'expensive_skirt']:
            draw.rectangle([cx - s(7), s(31), cx, s(32)], fill=shoe_color)
            draw.rectangle([cx, s(31), cx + s(7), s(32)], fill=shoe_color)
        else:
            # Heels for skirts/dresses
            heel_color = (0, 0, 0) if params['social_class'] in ['upper', 'rich'] else (139, 69, 19)
            draw.rectangle([cx - s(5), s(31), cx - s(2), s(32)], fill=heel_color)
            draw.rectangle([cx + s(2), s(31), cx + s(5), s(32)], fill=heel_color)
    
    def _draw_accessories(self, draw: ImageDraw, params: Dict):
        """Draw accessories like glasses, jewelry, etc."""
        cx = self._center_x()
        s = self._s
        
        # Glasses
        if params.get('has_glasses', False):
            glass_color = (0, 0, 0)
            # Frame
            draw.rectangle([cx - s(5), s(7), cx - s(1), s(9)], outline=glass_color)
            draw.rectangle([cx + s(1), s(7), cx + s(5), s(9)], outline=glass_color)
            # Bridge
            draw.line([(cx - s(1), s(8)), (cx + s(1), s(8))], fill=glass_color)
            # Temples
            draw.line([(cx - s(5), s(8)), (cx - s(8), s(8))], fill=glass_color)
            draw.line([(cx + s(5), s(8)), (cx + s(8), s(8))], fill=glass_color)
        
        # Jewelry (for upper class and rich people)
        if params.get('has_jewelry', False):
            jewelry_color = (255, 215, 0)  # Gold
            social_class = params['social_class']
            gender = params['gender']
            
            if social_class in ['upper', 'rich']:
                # Expensive jewelry
                if gender == 'female':
                    # Earrings
                    draw.point((cx - s(8), s(9)), fill=jewelry_color)
                    draw.point((cx + s(8), s(9)), fill=jewelry_color)
                    # Necklace
                    draw.line([(cx - s(4), s(16)), (cx + s(4), s(16))], fill=jewelry_color)
                    draw.point((cx, s(17)), fill=jewelry_color)
                else:
                    # Watch
                    draw.rectangle([cx - s(12), s(24), cx - s(10), s(25)], fill=jewelry_color)
            elif social_class in ['middle']:
                # Simple jewelry
                if gender == 'female':
                    # Small earrings
                    draw.point((cx - s(8), s(9)), fill=(192, 192, 192))  # Silver
                    draw.point((cx + s(8), s(9)), fill=(192, 192, 192))
        
        # Hats (use stored param for deterministic rendering across frames)
        if params.get('has_hat', False):
            hat_color = (139, 69, 19)
            if params['social_class'] == 'rich':
                hat_color = (25, 25, 112)  # Expensive hat
            elif params['social_class'] == 'poor':
                hat_color = (105, 105, 105)  # Baseball cap

            # Simple hat
            draw.rectangle([cx - s(8), s(1), cx + s(8), s(3)], fill=hat_color)
            if params.get('hat_style') == 'baseball_cap' or params['social_class'] == 'poor':
                # Baseball cap visor
                draw.rectangle([cx - s(10), s(3), cx - s(2), s(4)], fill=hat_color)

    # ==================== BATCH GENERATION ====================
    
    def generate_batch(self, count: int, output_dir: str = "output/") -> List[str]:
        """Generate multiple characters"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        generated_files = []
        for i in range(count):
            sprite = self.generate_character(seed=i)
            filename = f"character_{i:04d}.png"
            filepath = os.path.join(output_dir, filename)
            sprite.save(filepath, "PNG")
            generated_files.append(filepath)
        
        return generated_files
    
    def generate_preview(self, character: Image.Image, scale: int = 8) -> Image.Image:
        """Create a larger preview of a character"""
        return character.resize((self.width * scale, self.height * scale), Image.NEAREST)

def main():
    """Demo the scalable generator with multiple sizes"""
    print("Scalable Character Generator - Demo")
    
    sizes = [(32, 32), (64, 64), (128, 128)]
    
    for size in sizes:
        print(f"\nGenerating {size[0]}x{size[1]} character...")
        generator = PureCharacterGenerator(canvas_size=size)
        
        # Generate single character
        character = generator.generate_character(seed=42)
        character.save(f"sample_character_{size[0]}x{size[1]}.png", "PNG")
        
        # Generate preview
        preview = generator.generate_preview(character, scale=4 if size[0] <= 64 else 2)
        preview.save(f"sample_character_{size[0]}x{size[1]}_preview.png", "PNG")
        
        print(f"  Saved: sample_character_{size[0]}x{size[1]}.png")
        print(f"  Saved: sample_character_{size[0]}x{size[1]}_preview.png")
    
    print("\nDone! All sizes generated successfully.")

if __name__ == "__main__":
    main()
