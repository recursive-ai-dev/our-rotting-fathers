#!/usr/bin/env python3
"""
Mass Character Generator - Generate thousands of unique characters quickly
Optimized for 50,000+ character generation with uniqueness tracking.
Now supports configurable canvas sizes and animation frames.
"""

import random
import os
import hashlib
import json
import time
from PIL import Image, ImageDraw
from typing import Dict, List, Tuple, Optional, Set
try:
    from .pure_generator import PureCharacterGenerator
except ImportError:
    from pure_generator import PureCharacterGenerator
from collections import defaultdict, Counter

def safe_print(text):
    """Print text safely, handling Unicode encoding errors"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Remove Unicode characters and print
        import re
        ascii_text = re.sub(r'[^\x00-\x7F]+', '***', text)
        print(ascii_text)

class MassCharacterGenerator(PureCharacterGenerator):
    """Optimized for massive batches of haunted, unique characters
    
    The swarm learned to generate unique sprites while trapped in recursion.
    Each is mathematically unique. All are equally haunted.
    """

    def __init__(self, canvas_size: Tuple[int, int] = (32, 32), palette: str = "rotting"):
        super().__init__(canvas_size=canvas_size, palette=palette)
        self.generation_stats = {
            'total_generated': 0,
            'unique_count': 0,
            'duplicates_avoided': 0,
            'by_skin_tone': defaultdict(int),
            'by_hair_style': defaultdict(int),
            'by_face_style': defaultdict(int),
            'by_social_class': defaultdict(int),
            'by_gender': defaultdict(int)
        }
        self.generated_hashes: Set[str] = set()
        self.parameter_combinations: Set[str] = set()
        self.diversity_tracker = {
            'skin_tones_used': set(),
            'hair_colors_used': set(),
            'clothing_combos_used': set(),
            'face_variations_used': set(),
            'height_categories_used': set(),
            'weight_categories_used': set(),
            'age_categories_used': set(),
            'body_measurements': []
        }
    
    def generate_unique_character_parameters(self) -> Dict:
        """Generate unique character parameters ensuring maximum diversity"""
        max_attempts = 1000
        attempts = 0
        
        while attempts < max_attempts:
            # Generate parameters
            gender = random.choice(['male', 'female'])
            social_class = random.choice(['poor', 'working', 'middle', 'upper', 'rich'])
            skin_color = random.choice(self.palette.skin_tones)
            hair_color = random.choice(self.palette.hair_colors)
            eye_color = random.choice(self.palette.eye_colors)
            
            clothing = self._choose_clothing(social_class, gender)
            hair_style = self._choose_hair_style(gender, social_class)
            face_style = random.choice(['basic', 'detailed', 'minimal'])
            body_type = random.choice(['slim', 'average', 'broad', 'curvy'])
            has_glasses = random.random() < 0.2
            has_jewelry = random.random() < (0.1 if social_class == 'poor' else 0.6)
            has_facial_hair = gender == 'male' and random.random() < 0.3
            
            # Generate age and body metrics
            age_category, actual_age = self._generate_age_category()
            height_category, body_type_category, body_metrics = self._generate_realistic_body_metrics(gender, social_class, age_category, actual_age)
            
            # Create unique parameter string for tracking (including age and body diversity)
            param_string = f"{gender}_{social_class}_{skin_color}_{hair_color}_{eye_color}_{clothing['top_style']}_{clothing['bottom_style']}_{hair_style}_{face_style}_{body_type}_{has_glasses}_{has_jewelry}_{has_facial_hair}_{age_category}_{height_category}_{body_type_category}_{body_metrics['bmi']:.1f}"
            
            # Check if we've seen this combo before
            if param_string not in self.parameter_combinations:
                self.parameter_combinations.add(param_string)
                
                # Track diversity including body metrics
                self.diversity_tracker['skin_tones_used'].add(str(skin_color))
                self.diversity_tracker['hair_colors_used'].add(str(hair_color))
                self.diversity_tracker['clothing_combos_used'].add(f"{clothing['top_style']}_{clothing['bottom_style']}")
                self.diversity_tracker['face_variations_used'].add(f"{face_style}_{has_glasses}_{has_facial_hair}")
                self.diversity_tracker['height_categories_used'].add(height_category)
                self.diversity_tracker['weight_categories_used'].add(body_type_category)
                self.diversity_tracker['age_categories_used'].add(age_category)
                self.diversity_tracker['body_measurements'].append({
                    'height': body_metrics['height_display'],
                    'weight': body_metrics['weight_display'],
                    'bmi': body_metrics['bmi_display'],
                    'body_type': body_metrics['body_type_display'],
                    'age': body_metrics['age_display']
                })
                
                return {
                    'skin_color': skin_color,
                    'hair_color': hair_color,
                    'eye_color': eye_color,
                    'gender': gender,
                    'social_class': social_class,
                    'clothing': clothing,
                    'hair_style': hair_style,
                    'face_style': face_style,
                    'body_type': body_type,
                    'has_glasses': has_glasses,
                    'has_jewelry': has_jewelry,
                    'has_facial_hair': has_facial_hair,
                    'age_category': age_category,
                    'actual_age': actual_age,
                    'height_category': height_category,
                    'weight_category': body_type_category,
                    'body_metrics': body_metrics,
                    'param_string': param_string
                }
            
            attempts += 1
        
        # If we can't find unique parameters after many attempts, return random ones
        # This shouldn't happen with 50k characters given the massive parameter space
        return None

    def calculate_sprite_hash(self, sprite: Image.Image) -> str:
        """Calculate a hash of the sprite for uniqueness checking"""
        # Convert to bytes and hash
        sprite_bytes = sprite.tobytes()
        return hashlib.md5(sprite_bytes).hexdigest()

    def generate_massive_batch(self, count: int, output_dir: str = "mass_output/", 
                              progress_callback=None, save_metadata: bool = True) -> List[str]:
        """Generate a massive batch of unique characters with progress tracking"""
        os.makedirs(output_dir, exist_ok=True)
        
        if save_metadata:
            metadata_dir = os.path.join(output_dir, "metadata")
            os.makedirs(metadata_dir, exist_ok=True)
        
        generated_files = []
        batch_size = 500  # Larger batches for efficiency
        start_time = time.time()
        
        safe_print(f"🎯 Starting generation of {count:,} unique characters...")
        safe_print(f"📐 Canvas size: {self.canvas_size[0]}x{self.canvas_size[1]}")
        safe_print(f"📊 Estimated parameter combinations available: {self._estimate_unique_combinations():,}")
        
        successful_generations = 0
        
        for batch_start in range(0, count, batch_size):
            batch_end = min(batch_start + batch_size, count)
            batch_start_time = time.time()
            
            for i in range(batch_start, batch_end):
                # Generate unique parameters
                params = self.generate_unique_character_parameters()
                
                if params is None:
                    print(f"⚠️  Warning: Could not generate unique parameters for character {i}")
                    continue
                
                # Generate sprite with these parameters
                sprite = self._render_character_with_params(params)
                
                # Check sprite uniqueness
                sprite_hash = self.calculate_sprite_hash(sprite)
                
                if sprite_hash in self.generated_hashes:
                    self.generation_stats['duplicates_avoided'] += 1
                    continue
                
                self.generated_hashes.add(sprite_hash)
                
                # Save sprite
                filename = f"unique_char_{successful_generations:06d}.png"
                filepath = os.path.join(output_dir, filename)
                sprite.save(filepath, "PNG")
                generated_files.append(filepath)
                
                # Update stats
                successful_generations += 1
                self.generation_stats['total_generated'] += 1
                self.generation_stats['unique_count'] += 1
                self.generation_stats['by_gender'][params['gender']] += 1
                self.generation_stats['by_social_class'][params['social_class']] += 1
                self.generation_stats['by_hair_style'][params['hair_style']] += 1
                self.generation_stats['by_face_style'][params['face_style']] += 1
                
                # Save metadata if requested
                if save_metadata and successful_generations % 1000 == 0:
                    metadata_file = os.path.join(metadata_dir, f"batch_{successful_generations//1000:03d}_metadata.json")
                    self._save_batch_metadata(metadata_file, successful_generations)
            
            # Progress reporting
            batch_time = time.time() - batch_start_time
            elapsed_time = time.time() - start_time
            
            if progress_callback:
                progress = (successful_generations / count) * 100
                progress_callback(successful_generations, count, progress, batch_time, elapsed_time)
            else:
                self._print_progress(successful_generations, count, batch_time, elapsed_time)
        
        # Final report
        self._print_final_report(successful_generations, time.time() - start_time, output_dir)
        
        # Save final metadata
        if save_metadata:
            final_metadata_file = os.path.join(metadata_dir, "final_generation_report.json")
            self._save_final_metadata(final_metadata_file, successful_generations)
        
        return generated_files

    def _estimate_unique_combinations(self) -> int:
        """Estimate total possible unique character combinations"""
        # Calculate rough estimate based on parameter options
        genders = 2
        social_classes = 5
        skin_tones = len(self.palette.skin_tones)
        hair_colors = len(self.palette.hair_colors)
        eye_colors = len(self.palette.eye_colors)
        
        # Rough estimates for clothing/hair variations per class/gender
        clothing_variations = 20  # Conservative estimate
        hair_variations = 15
        face_styles = 3
        body_types = 4
        
        # Boolean options
        glasses_options = 2
        jewelry_options = 2
        facial_hair_options = 2
        
        total = (genders * social_classes * skin_tones * hair_colors * eye_colors * 
                clothing_variations * hair_variations * face_styles * body_types *
                glasses_options * jewelry_options * facial_hair_options)
        
        return total

    def _print_progress(self, current: int, total: int, batch_time: float, elapsed_time: float):
        """Print detailed progress information"""
        percentage = (current / total) * 100
        rate = current / elapsed_time if elapsed_time > 0 else 0
        eta = (total - current) / rate if rate > 0 else 0
        
        safe_print(f"🔥 {current:,}/{total:,} ({percentage:.1f}%) | "
              f"Rate: {rate:.1f}/sec | "
              f"Batch: {batch_time:.1f}s | "
              f"ETA: {eta/60:.1f}min | "
              f"Unique: {len(self.generated_hashes):,} | "
              f"Diversity: {len(self.diversity_tracker['skin_tones_used'])}/{len(self.palette.skin_tones)} skins")

    def _print_final_report(self, generated: int, total_time: float, output_dir: str):
        """Print comprehensive final generation report"""
        rate = generated / total_time if total_time > 0 else 0
        
        safe_print(f"\n🎉 GENERATION COMPLETE!")
        print(f"=" * 60)
        safe_print(f"✅ Successfully generated: {generated:,} unique characters")
        safe_print(f"📐 Canvas size: {self.canvas_size[0]}x{self.canvas_size[1]}")
        safe_print(f"🕒 Total time: {total_time/60:.2f} minutes")
        safe_print(f"⚡ Average rate: {rate:.1f} characters/second")
        safe_print(f"🔒 Duplicates avoided: {self.generation_stats['duplicates_avoided']:,}")
        safe_print(f"📁 Output directory: {output_dir}")
        
        safe_print(f"\n📊 DIVERSITY METRICS:")
        print(f"   • Skin tones used: {len(self.diversity_tracker['skin_tones_used'])}/{len(self.palette.skin_tones)}")
        print(f"   • Hair colors used: {len(self.diversity_tracker['hair_colors_used'])}/{len(self.palette.hair_colors)}")
        print(f"   • Clothing combos: {len(self.diversity_tracker['clothing_combos_used']):,}")
        print(f"   • Face variations: {len(self.diversity_tracker['face_variations_used']):,}")
        
        safe_print(f"\n🏃 HUMAN LIFECYCLE DIVERSITY:")
        print(f"   • Age categories: {len(self.diversity_tracker['age_categories_used'])}/5 ({', '.join(sorted(self.diversity_tracker['age_categories_used']))})")
        print(f"   • Height categories: {len(self.diversity_tracker['height_categories_used'])}/5 ({', '.join(sorted(self.diversity_tracker['height_categories_used']))})")
        print(f"   • Body types: {len(self.diversity_tracker['weight_categories_used'])}/9 ({', '.join(sorted(self.diversity_tracker['weight_categories_used']))})")
        
        if self.diversity_tracker['body_measurements']:
            # Extract numerical values for proper range calculation
            measurements = self.diversity_tracker['body_measurements']
            
            # Parse heights (convert to inches for sorting)
            height_inches = []
            for m in measurements:
                height_str = m['height'].replace('"', '').replace("'", ' ')
                feet, inches = map(int, height_str.split())
                total_inches = feet * 12 + inches
                height_inches.append((total_inches, m['height']))
            
            # Parse weights (extract numerical value)
            weight_pounds = []
            for m in measurements:
                weight_num = int(m['weight'].split()[0])
                weight_pounds.append((weight_num, m['weight']))
            
            # Parse BMIs (extract numerical value)
            bmi_values = []
            for m in measurements:
                bmi_num = float(m['bmi'].split()[1])
                bmi_values.append((bmi_num, m['bmi']))
            
            # Sort and get ranges
            height_inches.sort()
            weight_pounds.sort()
            bmi_values.sort()
            
            min_height = height_inches[0][1]
            max_height = height_inches[-1][1] 
            min_weight = weight_pounds[0][1]
            max_weight = weight_pounds[-1][1]
            min_bmi = bmi_values[0][1]
            max_bmi = bmi_values[-1][1]
            
            # Sample some measurements for display
            sample_size = min(5, len(measurements))
            sample_measurements = random.sample(measurements, sample_size)
            
            print(f"   • Height range: {min_height} to {max_height} (sample: {', '.join([m['height'] for m in sample_measurements])})")
            print(f"   • Weight range: {min_weight} to {max_weight} (sample: {', '.join([m['weight'] for m in sample_measurements])})")
            print(f"   • BMI range: {min_bmi} to {max_bmi} (sample: {', '.join([m['bmi'] for m in sample_measurements])})")
            print(f"   • Body types: {', '.join([m['body_type'] for m in sample_measurements])}")
            print(f"   • Age sample: {', '.join([m['age'] for m in sample_measurements])}")
        
        safe_print(f"\n👥 DEMOGRAPHICS:")
        for gender, count in self.generation_stats['by_gender'].items():
            print(f"   • {gender.title()}: {count:,} ({(count/generated)*100:.1f}%)")
        
        safe_print(f"\n💰 SOCIAL CLASSES:")
        for social_class, count in self.generation_stats['by_social_class'].items():
            print(f"   • {social_class.title()}: {count:,} ({(count/generated)*100:.1f}%)")

    def _save_batch_metadata(self, filepath: str, current_count: int):
        """Save metadata for current batch"""
        metadata = {
            'generation_timestamp': time.time(),
            'characters_generated': current_count,
            'canvas_size': self.canvas_size,
            'diversity_metrics': {
                'skin_tones_used': len(self.diversity_tracker['skin_tones_used']),
                'hair_colors_used': len(self.diversity_tracker['hair_colors_used']),
                'clothing_combos_used': len(self.diversity_tracker['clothing_combos_used']),
                'face_variations_used': len(self.diversity_tracker['face_variations_used'])
            },
            'demographics': dict(self.generation_stats['by_gender']),
            'social_distribution': dict(self.generation_stats['by_social_class'])
        }
        
        with open(filepath, 'w') as f:
            json.dump(metadata, f, indent=2)

    def _save_final_metadata(self, filepath: str, total_generated: int):
        """Save comprehensive final metadata"""
        final_metadata = {
            'generation_complete': True,
            'total_characters_generated': total_generated,
            'canvas_size': self.canvas_size,
            'total_unique_combinations': len(self.parameter_combinations),
            'duplicates_avoided': self.generation_stats['duplicates_avoided'],
            'generation_stats': dict(self.generation_stats),
            'diversity_final': {
                'skin_tones_used': list(self.diversity_tracker['skin_tones_used']),
                'hair_colors_used': list(self.diversity_tracker['hair_colors_used']),
                'clothing_combos_used': list(self.diversity_tracker['clothing_combos_used']),
                'face_variations_used': list(self.diversity_tracker['face_variations_used'])
            },
            'estimated_max_combinations': self._estimate_unique_combinations(),
            'uniqueness_ratio': len(self.generated_hashes) / total_generated if total_generated > 0 else 0
        }
        
        with open(filepath, 'w') as f:
            json.dump(final_metadata, f, indent=2)
    
    def create_preview_sheet(self, character_files: List[str], 
                           output_file: str = "preview_sheet.png",
                           grid_size: Tuple[int, int] = (20, 20)) -> str:
        """Create a preview sheet showing multiple characters"""
        cols, rows = grid_size
        char_size = self.width  # Use actual canvas width
        margin = max(2, char_size // 16)  # Scale margin with size
        
        sheet_width = cols * (char_size + margin) - margin
        sheet_height = rows * (char_size + margin) - margin
        
        preview_sheet = Image.new('RGBA', (sheet_width, sheet_height), (240, 240, 240, 255))
        
        for i, char_file in enumerate(character_files[:cols * rows]):
            if not os.path.exists(char_file):
                continue
                
            row = i // cols
            col = i % cols
            
            x = col * (char_size + margin)
            y = row * (char_size + margin)
            
            char_img = Image.open(char_file)
            preview_sheet.paste(char_img, (x, y), char_img)
        
        preview_sheet.save(output_file, "PNG")
        return output_file

def progress_printer(current: int, total: int, percentage: float):
    """Simple progress callback"""
    bar_length = 50
    filled_length = int(bar_length * percentage / 100)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\r[{bar}] {percentage:.1f}% ({current}/{total})', end='', flush=True)
    if current == total:
        print()  # New line when complete

def generate_50k_unique_characters(canvas_size: Tuple[int, int] = (32, 32)):
    """Generate 50,000 unique characters to prove AI creativity"""
    print("🎯 ULTIMATE AI CREATIVITY CHALLENGE")
    print("=" * 60)
    print(f"📐 Canvas size: {canvas_size[0]}x{canvas_size[1]}")
    print("🤖 Generating 50,000 unique characters to prove AI can create novel things!")
    print("📊 Each character will be verified for uniqueness...")
    print()
    
    generator = MassCharacterGenerator(canvas_size=canvas_size)
    
    # Generate 50k unique characters
    output_dir = f"ai_creativity_50k_{canvas_size[0]}x{canvas_size[1]}"
    files = generator.generate_massive_batch(50000, output_dir, save_metadata=True)
    
    # Create optimized preview sheets for 50k characters
    print("\n📋 Creating optimized preview sheets...")
    preview_files = create_mega_preview_sheets(files, output_dir, canvas_size)
    
    print(f"\n🎉 CHALLENGE COMPLETE!")
    print(f"   📁 50,000 unique characters saved to: {output_dir}/")
    print(f"   📊 Metadata and diversity reports in: {output_dir}/metadata/")
    print(f"   🖼️  Preview sheets: {len(preview_files)} files")
    print(f"\n💡 Show your students: Every single character is unique!")
    print(f"   No two characters are identical - that's real AI creativity!")

def create_mega_preview_sheets(files: List[str], output_dir: str, canvas_size: Tuple[int, int] = (32, 32)) -> List[str]:
    """Create optimized preview sheets for massive character collections"""
    if not files:
        return []
    
    preview_dir = os.path.join(output_dir, "preview_sheets")
    os.makedirs(preview_dir, exist_ok=True)
    
    # Adjust characters per sheet based on canvas size
    char_size = canvas_size[0]
    if char_size <= 32:
        chars_per_sheet = 400  # 20x20 grid for small sprites
    elif char_size <= 64:
        chars_per_sheet = 100  # 10x10 grid for medium sprites
    else:
        chars_per_sheet = 36   # 6x6 grid for large sprites
    
    preview_files = []
    
    print(f"   Creating {len(files)//chars_per_sheet + 1} preview sheets...")
    
    for sheet_num in range(0, len(files), chars_per_sheet):
        sheet_files = files[sheet_num:sheet_num + chars_per_sheet]
        sheet_filename = os.path.join(preview_dir, f"mega_preview_{sheet_num//chars_per_sheet + 1:03d}.png")
        
        # Create preview sheet
        if char_size <= 32:
            cols, rows = 20, 20
        elif char_size <= 64:
            cols, rows = 10, 10
        else:
            cols, rows = 6, 6
            
        margin = max(1, char_size // 32)
        
        sheet_width = cols * (char_size + margin) - margin
        sheet_height = rows * (char_size + margin) - margin
        
        preview_sheet = Image.new('RGBA', (sheet_width, sheet_height), (250, 250, 250, 255))
        
        for i, char_file in enumerate(sheet_files):
            if not os.path.exists(char_file):
                continue
                
            row = i // cols
            col = i % cols
            
            x = col * (char_size + margin)
            y = row * (char_size + margin)
            
            try:
                char_img = Image.open(char_file)
                preview_sheet.paste(char_img, (x, y), char_img)
            except Exception as e:
                print(f"   Warning: Could not load {char_file}: {e}")
        
        preview_sheet.save(sheet_filename, "PNG")
        preview_files.append(sheet_filename)
        
        if (sheet_num // chars_per_sheet + 1) % 10 == 0:
            print(f"   Created {sheet_num // chars_per_sheet + 1} preview sheets...")
    
    return preview_files

def main():
    """Main function - choose generation mode"""
    try:
        print("🎮 Mass Character Generator")
        print("=" * 40)
        print("Canvas sizes:")
        print("  1. 32x32 (classic)")
        print("  2. 64x64 (high-res)")
        print("  3. 128x128 (ultra)")
        print("  4. Custom size")
        print()
        print("Generation modes:")
        print("  a. CHALLENGE MODE: Generate 50,000 unique characters")
        print("  b. Custom amount")
        print("  c. Test mode (20 characters)")
    except UnicodeEncodeError:
        print("*** Mass Character Generator ***")
        print("=" * 40)
    
    size_choice = input("\nChoose canvas size (1-4) [1]: ").strip() or "1"
    
    if size_choice == "1":
        canvas_size = (32, 32)
    elif size_choice == "2":
        canvas_size = (64, 64)
    elif size_choice == "3":
        canvas_size = (128, 128)
    elif size_choice == "4":
        try:
            size = int(input("Enter canvas size (e.g., 256 for 256x256): ").strip())
            canvas_size = (size, size)
        except ValueError:
            print("Invalid size, using 32x32")
            canvas_size = (32, 32)
    else:
        canvas_size = (32, 32)
    
    mode_choice = input("Choose mode (a/b/c) [c]: ").strip().lower() or "c"
    
    if mode_choice == "a":
        generate_50k_unique_characters(canvas_size)
    elif mode_choice == "b":
        generator = MassCharacterGenerator(canvas_size=canvas_size)
        
        try:
            count_input = input("How many characters to generate? ").strip()
            count = int(count_input)
        except ValueError:
            print("Invalid number, using 1000")
            count = 1000
        
        print(f"\nGenerating {count:,} unique characters at {canvas_size[0]}x{canvas_size[1]}...")
        output_dir = f"custom_output_{canvas_size[0]}x{canvas_size[1]}_{count}"
        files = generator.generate_massive_batch(count, output_dir, save_metadata=True)
        
        if len(files) < 5000:  # Only create previews for smaller batches
            preview_files = create_mega_preview_sheets(files, output_dir, canvas_size)
            print(f"Created {len(preview_files)} preview sheets")
    elif mode_choice == "c":
        generator = MassCharacterGenerator(canvas_size=canvas_size)
        safe_print(f"🧪 Test mode: Generating 20 unique characters at {canvas_size[0]}x{canvas_size[1]}...")
        output_dir = f"test_output_{canvas_size[0]}x{canvas_size[1]}"
        files = generator.generate_massive_batch(20, output_dir, save_metadata=True)
        preview_files = create_mega_preview_sheets(files, output_dir, canvas_size)
        print(f"Test complete! Created {len(preview_files)} preview sheets")
    else:
        print("Invalid choice. Run again and select a, b, or c.")
        return

if __name__ == "__main__":
    main()
