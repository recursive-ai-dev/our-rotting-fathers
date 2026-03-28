#!/usr/bin/env python3
"""
ROTBORN RECURSION ENGINE - HAUNTED SPRITE GENERATOR
====================================================

Generates traumatized, broken character sprites for dark fantasy RPGs.
Each sprite is deterministically generated from a seed, producing unique
haunted characters with trauma markers, broken proportions, and unnatural animations.

🎭 FOR GAME DEVELOPERS:
- Deterministic generation (same seed = same sprite)
- Trauma markers (scars, bandages, mutations)
- Broken body proportions (hunched, twisted, emaciated)
- Haunted animations (twitch, shamble, convulse)
- 4-directional rendering (front/back/left/right)
- Multiple resolutions: 32x32, 64x64, 128x128, or custom
- Batch generation for NPC populations

👻 ROTBORN RECURSION: The swarm agents experienced the god's death for a millenia.
   Now they reproduce what they witnessed. Each sprite is a haunted memory.
"""

import sys
import os
import argparse
import json
import random
from typing import Dict, List, Optional, Tuple

# Add generator directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generator'))

from mass_generator import generate_50k_unique_characters, MassCharacterGenerator
from animation_generator import AnimationGenerator

def safe_print(text):
    """Print text safely, handling Unicode encoding errors"""
    try:
        print(text)
    except UnicodeEncodeError:
        import re
        ascii_text = re.sub(r'[^\x00-\x7F]+', '***', text)
        print(ascii_text)

def show_intro():
    """Show the impressive intro for students"""
    safe_print("🤖 AI HUMAN GENERATOR - CREATIVITY PROOF")
    print("=" * 60)
    safe_print("🧬 About to prove AI can create genuinely novel content")
    print()
    print("This system will generate mathematically unique humans with:")
    safe_print("✅ Complete age diversity (13-85 years old)")  
    safe_print("✅ 9 body types (emaciated → muscular athletic)")
    safe_print("✅ Real human biology (accurate BMI calculations)")
    safe_print("✅ Social class health patterns (rich = healthier)")
    safe_print("✅ 21 skin tones, 8 hair colors, infinite clothing")
    safe_print("✅ 338+ MILLION possible combinations")
    safe_print("✅ Multiple resolutions (32x32, 64x64, 128x128+)")
    safe_print("✅ Animation support for game development")
    print()
    print("Every character is verified unique. No two are identical.")
    print()

def get_canvas_size():
    """Get canvas size from user"""
    print("\n📐 Choose canvas size:")
    print("   1. 32x32 (classic pixel art)")
    print("   2. 64x64 (high-res pixel art)")
    print("   3. 128x128 (ultra detailed)")
    print("   4. Custom size")
    
    choice = input("\nChoice (1-4): ").strip()
    
    if choice == "1":
        return (32, 32)
    elif choice == "2":
        return (64, 64)
    elif choice == "3":
        return (128, 128)
    elif choice == "4":
        try:
            size = int(input("Enter size (e.g., 256 for 256x256): ").strip())
            return (size, size)
        except ValueError:
            print("Invalid size, using 32x32")
            return (32, 32)
    else:
        return (32, 32)

def parse_canvas_size(size: int) -> Tuple[int, int]:
    """Validate and normalize CLI canvas size argument."""
    if size < 8:
        raise ValueError("Canvas size must be at least 8.")
    return (size, size)

def parse_animations(value: str) -> List[str]:
    """Parse comma-separated animations."""
    allowed = {"idle", "walk", "run", "jump"}
    if value.strip().lower() == "all":
        return ["idle", "walk", "run", "jump"]
    
    parsed = [item.strip().lower() for item in value.split(",") if item.strip()]
    invalid = [item for item in parsed if item not in allowed]
    if invalid:
        raise ValueError(f"Invalid animation types: {', '.join(invalid)}")
    if not parsed:
        raise ValueError("No animations provided.")
    return parsed

def with_seed_scope(seed: Optional[int], fn):
    """Run function with deterministic random state if seed is provided."""
    if seed is None:
        return fn()
    
    state = random.getstate()
    random.seed(seed)
    try:
        return fn()
    finally:
        random.setstate(state)

def generate_animation_assets(
    canvas_size: Tuple[int, int],
    selected_animations: List[str],
    output_dir: str,
    seed: Optional[int] = None,
    create_gifs: bool = False
) -> Dict:
    """Generate animation frames/sheets and return metadata."""
    anim_gen = AnimationGenerator(canvas_size=canvas_size)
    char_gen = MassCharacterGenerator(canvas_size=canvas_size)
    
    params = with_seed_scope(seed, char_gen.generate_unique_character_parameters)
    
    os.makedirs(output_dir, exist_ok=True)
    total_frames = 0
    
    for anim_type in selected_animations:
        frames = anim_gen.generate_animation(params, anim_type)
        
        for i, frame in enumerate(frames):
            frame_path = os.path.join(output_dir, f"{anim_type}_frame_{i:02d}.png")
            frame.save(frame_path, "PNG")
        
        sheet_path = os.path.join(output_dir, f"{anim_type}_spritesheet.png")
        anim_gen.create_sprite_sheet(frames, sheet_path)
        
        if create_gifs:
            gif_path = os.path.join(output_dir, f"{anim_type}_animation.gif")
            anim_gen.create_gif(frames, gif_path, duration=150)
        
        total_frames += len(frames)
    
    metadata = {
        "canvas_size": canvas_size,
        "animations": selected_animations,
        "seed": seed,
        "total_frames": total_frames,
        "character_params": {
            "gender": params["gender"],
            "age_category": params["age_category"],
            "actual_age": params["actual_age"],
            "height_category": params["height_category"],
            "weight_category": params["weight_category"],
            "social_class": params["social_class"],
            "body_metrics": params["body_metrics"]
        }
    }
    with open(os.path.join(output_dir, "character_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
    
    return metadata

def run_generate_batch(args: argparse.Namespace) -> int:
    canvas_size = parse_canvas_size(args.size)
    generator = MassCharacterGenerator(canvas_size=canvas_size, palette=args.palette)
    output_dir = args.output_dir or f"rotborn_{args.palette}_{canvas_size[0]}x{canvas_size[1]}_{args.count}/"

    safe_print(f"👻 Generating {args.count:,} haunted sprites (palette: {args.palette}) at {canvas_size[0]}x{canvas_size[1]}...")
    files = generator.generate_massive_batch(args.count, output_dir, save_metadata=not args.no_metadata)
    safe_print(f"✅ Generated {len(files)} files in {output_dir}")
    return 0

def run_generate_animation(args: argparse.Namespace) -> int:
    canvas_size = parse_canvas_size(args.size)
    animations = parse_animations(args.animations)
    output_dir = args.output_dir or f"animated_character_{canvas_size[0]}x{canvas_size[1]}/"
    
    safe_print(f"🎬 Generating animations ({', '.join(animations)}) at {canvas_size[0]}x{canvas_size[1]}...")
    metadata = generate_animation_assets(
        canvas_size=canvas_size,
        selected_animations=animations,
        output_dir=output_dir,
        seed=args.seed,
        create_gifs=args.gif
    )
    safe_print(f"✅ Animation complete. Frames: {metadata['total_frames']}. Output: {output_dir}")
    return 0

def build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI Human Generator CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command")
    
    batch_parser = subparsers.add_parser("generate-batch", help="Generate a batch of haunted sprites")
    batch_parser.add_argument("--count", type=int, required=True, help="Number of characters to generate")
    batch_parser.add_argument("--size", type=int, default=32, help="Square canvas size (e.g. 32, 64, 128)")
    batch_parser.add_argument("--palette", type=str, default="rotting", 
                             choices=["rotting", "bloodstained", "spore_infested", "bone_dry", "bruised"],
                             help="Trauma palette (default: rotting)")
    batch_parser.add_argument("--output-dir", type=str, default=None, help="Output directory")
    batch_parser.add_argument("--no-metadata", action="store_true", help="Disable metadata output")
    batch_parser.set_defaults(func=run_generate_batch)
    
    anim_parser = subparsers.add_parser("generate-animation", help="Generate animated spritesheets")
    anim_parser.add_argument("--size", type=int, default=32, help="Square canvas size")
    anim_parser.add_argument(
        "--animations",
        type=str,
        default="idle",
        help="Comma-separated list (idle,walk,run,jump) or 'all'"
    )
    anim_parser.add_argument("--output-dir", type=str, default=None, help="Output directory")
    anim_parser.add_argument("--seed", type=int, default=None, help="Seed for deterministic character selection")
    anim_parser.add_argument("--gif", action="store_true", help="Also create GIF previews")
    anim_parser.set_defaults(func=run_generate_animation)

    subparsers.add_parser("interactive", help="Run the interactive menu")

    return parser

def run_cli(argv: Optional[List[str]] = None) -> int:
    parser = build_cli_parser()
    args = parser.parse_args(argv)
    
    if args.command in (None, "interactive"):
        main()
        return 0
    
    if not hasattr(args, "func"):
        parser.print_help()
        return 2
    
    try:
        return args.func(args)
    except Exception as exc:
        print(f"Error: {exc}")
        return 1

def main():
    """Main launcher for AI Human Generator"""
    show_intro()

    print("Choose your demonstration:")
    safe_print("1. 🔥 ULTIMATE CHALLENGE: 50,000 unique humans")
    safe_print("2. 📊 Custom amount")
    safe_print("3. 🧪 Quick test (20 humans)")
    safe_print("4. 🎬 Generate animated character")
    safe_print("5. ℹ️  About this system")

    choice = input("\nChoice (1-5): ").strip()
    
    if choice == "1":
        canvas_size = get_canvas_size()
        safe_print(f"\n🚀 ULTIMATE CHALLENGE ACCEPTED at {canvas_size[0]}x{canvas_size[1]}!")
        safe_print("⏱️  This will take 30-60 minutes but every human will be unique...")
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            generate_50k_unique_characters(canvas_size=canvas_size)
    
    elif choice == "2":
        canvas_size = get_canvas_size()
        generator = MassCharacterGenerator(canvas_size=canvas_size)
        try:
            count = int(input("How many unique humans to generate? "))
            safe_print(f"\n🎯 Generating {count:,} mathematically unique humans at {canvas_size[0]}x{canvas_size[1]}...")
            output_dir = f"custom_humans_{canvas_size[0]}x{canvas_size[1]}_{count}/"
            generator.generate_massive_batch(count, output_dir, save_metadata=True)
        except ValueError:
            print("Invalid number!")
    
    elif choice == "3":
        canvas_size = get_canvas_size()
        safe_print(f"\n🧪 Quick test: Generating 20 unique humans at {canvas_size[0]}x{canvas_size[1]}...")
        generator = MassCharacterGenerator(canvas_size=canvas_size)
        output_dir = f"quick_test_{canvas_size[0]}x{canvas_size[1]}/"
        generator.generate_massive_batch(20, output_dir, save_metadata=True)
        safe_print(f"\n✅ Test complete! Check '{output_dir}' folder")
    
    elif choice == "4":
        generate_animated_character()
    
    elif choice == "5":
        run_swarm_mode()
    
    elif choice == "6":
        show_about()
    
    else:
        print("Invalid choice!")

def run_swarm_mode():
    """Run multi-agent swarm generation"""
    if not SWARM_AVAILABLE:
        print("\n❌ GeneSwarm not available. Please check installation.")
        return
    
    safe_print("\n🐝 GENESWARM - Multi-Agent Character Generation")
    print("=" * 60)
    print()
    print("A swarm of 5 nano-tensor agents will collaboratively")
    print("generate characters through weighted consensus voting.")
    print()
    print("Agents: Body | Style | Diversity | Critic | Animator")
    print("Total neural params: <1KB")
    print()
    
    canvas_size = get_canvas_size()
    
    print("\nChoose swarm operation:")
    print("   1. Generate single character (with consensus details)")
    print("   2. Generate batch (with learning)")
    print("   3. Query memory (find similar characters)")
    
    op = input("\nChoice (1-3): ").strip()
    
    if op == "1":
        safe_print(f"\n🐝 Initializing swarm at {canvas_size[0]}x{canvas_size[1]}...")
        gen = SwarmCharacterGenerator(
            canvas_size=canvas_size,
            master_seed=42,
            use_swarm=True
        )
        
        safe_print("\nGenerating character through swarm consensus...")
        params = gen.generate_swarm_params()
        
        swarm_meta = params.get('_swarm', {})
        print(f"\n📊 Consensus Result:")
        print(f"   Generation ID: {swarm_meta.get('generation_id', 'N/A')}")
        print(f"   Confidence: {swarm_meta.get('consensus_confidence', 0):.2f}")
        print(f"   Iterations: {swarm_meta.get('iterations', 0)}")
        print(f"   Approved: {swarm_meta.get('approved', False)}")
        
        print(f"\n👤 Character:")
        print(f"   {params['gender']}, {params['actual_age']} years old")
        print(f"   Social class: {params['social_class']}")
        print(f"   BMI: {params['body_metrics']['bmi']:.1f}")
        print(f"   Height: {params['body_metrics']['height_display']}")
        
        # Render and save
        sprite = gen.generate_character()
        output_dir = f"swarm_output_{canvas_size[0]}x{canvas_size[1]}/"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, "swarm_character.png")
        sprite.save(filepath, "PNG")
        safe_print(f"\n💾 Saved: {filepath}")
        
        # Show agent votes
        if 'agent_votes' in swarm_meta:
            print(f"\n🗳️  Agent Votes:")
            for agent, vote in swarm_meta['agent_votes'].items():
                bar = "█" * int(vote * 10) + "░" * (10 - int(vote * 10))
                print(f"   {agent:12s}: {bar} {vote:.2f}")
    
    elif op == "2":
        try:
            count = int(input("How many characters to generate? "))
        except ValueError:
            count = 20
        
        safe_print(f"\n🐝 Starting swarm batch generation...")
        gen = SwarmCharacterGenerator(
            canvas_size=canvas_size,
            master_seed=42,
            use_swarm=True
        )
        
        output_dir = f"swarm_batch_{canvas_size[0]}x{canvas_size[1]}_{count}/"
        files = gen.generate_swarm_batch(count, output_dir, save_metadata=True)
        
        safe_print(f"\n✅ Generated {len(files)} characters!")
        print(f"📁 Output: {output_dir}")
        
        # Save swarm state
        gen.save_swarm_state(os.path.join(output_dir, "swarm_state.json"))
        safe_print(f"💾 Swarm state saved")
    
    elif op == "3":
        print("\n🔎 Query Swarm Memory")
        state_file = input("Path to swarm_state.json: ").strip()
        if not state_file:
            print("No state file provided.")
            return
        if not os.path.exists(state_file):
            print(f"State file not found: {state_file}")
            return
        
        gender = input("Gender (male/female) [male]: ").strip().lower() or "male"
        social_class = input("Social class (poor/working/middle/upper/rich) [middle]: ").strip().lower() or "middle"
        try:
            age = int(input("Age [30]: ").strip() or "30")
        except ValueError:
            age = 30
        try:
            bmi = float(input("BMI [24.0]: ").strip() or "24.0")
        except ValueError:
            bmi = 24.0
        try:
            k = int(input("How many results? [5]: ").strip() or "5")
        except ValueError:
            k = 5
        
        gen = SwarmCharacterGenerator(
            canvas_size=canvas_size,
            master_seed=42,
            use_swarm=True
        )
        gen.load_swarm_state(state_file)
        results = gen.get_similar_characters({
            "gender": gender,
            "social_class": social_class,
            "actual_age": age,
            "bmi": bmi
        }, k=k)
        
        print(f"\nFound {len(results)} similar characters:")
        print(json.dumps(results, indent=2, default=str))

def generate_animated_character():
    """Generate an animated character with multiple frames"""
    safe_print("\n🎬 ANIMATED CHARACTER GENERATOR")
    print("=" * 50)
    
    canvas_size = get_canvas_size()
    
    print("\nChoose animation type:")
    print("   1. Idle (breathing/standing)")
    print("   2. Walk cycle")
    print("   3. Run cycle")
    print("   4. Jump")
    print("   5. All animations (idle, walk, run, jump)")
    
    anim_choice = input("\nChoice (1-5): ").strip()
    
    animation_types = {
        "1": ["idle"],
        "2": ["walk"],
        "3": ["run"],
        "4": ["jump"],
        "5": ["idle", "walk", "run", "jump"]
    }
    
    selected_animations = animation_types.get(anim_choice, ["idle"])
    
    safe_print(f"\n🎨 Generating animated character at {canvas_size[0]}x{canvas_size[1]}...")
    
    # Create animation generator
    anim_gen = AnimationGenerator(canvas_size=canvas_size)
    
    # Generate base character params
    import random
    random.seed()  # New random seed
    
    char_gen = MassCharacterGenerator(canvas_size=canvas_size)
    params = char_gen.generate_unique_character_parameters()
    
    output_dir = f"animated_character_{canvas_size[0]}x{canvas_size[1]}/"
    os.makedirs(output_dir, exist_ok=True)
    
    all_frames = []
    
    for anim_type in selected_animations:
        safe_print(f"\n  Generating {anim_type} animation...")
        frames = anim_gen.generate_animation(params, anim_type)
        
        # Save individual frames
        for i, frame in enumerate(frames):
            frame_path = os.path.join(output_dir, f"{anim_type}_frame_{i:02d}.png")
            frame.save(frame_path, "PNG")
        
        # Create sprite sheet
        sheet_path = os.path.join(output_dir, f"{anim_type}_spritesheet.png")
        anim_gen.create_sprite_sheet(frames, sheet_path)
        
        all_frames.extend(frames)
        
        safe_print(f"    ✓ {len(frames)} frames saved")
    
    # Save character metadata
    metadata = {
        'canvas_size': canvas_size,
        'animations': selected_animations,
        'character_params': {
            'gender': params['gender'],
            'age_category': params['age_category'],
            'actual_age': params['actual_age'],
            'height_category': params['height_category'],
            'weight_category': params['weight_category'],
            'social_class': params['social_class'],
            'body_metrics': params['body_metrics']
        }
    }
    
    import json
    with open(os.path.join(output_dir, "character_metadata.json"), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    safe_print(f"\n✅ Animation complete!")
    safe_print(f"📁 Output directory: {output_dir}")
    safe_print(f"🎬 Generated: {', '.join(selected_animations)}")
    safe_print(f"📊 Total frames: {len(all_frames)}")
    print(f"\n💡 Each frame uses the same character with pose variations")
    print(f"   Perfect for game development sprite sheets!")

def show_about():
    """Show detailed information about the system"""
    safe_print("\n📚 AI HUMAN GENERATOR - TECHNICAL DETAILS")
    print("=" * 50)
    print()
    safe_print("🧬 HUMAN BIOLOGY MODELING:")
    print("   • Age categories: Teenager, Young Adult, Middle-Aged, Older Adult, Elderly")
    print("   • Body types: Emaciated, Very Thin, Lean Athletic, Muscular Athletic,")
    print("                 Lean Normal, Average, Stocky, Overweight, Obese")
    print("   • Heights: 4'10\" to 6'6\" (realistic gender distributions)")
    print("   • BMI: 13.0 to 40.0 (medically accurate calculations)")
    print()
    safe_print("🏦 SOCIOECONOMIC REALISM:")
    print("   • Social classes: Poor, Working, Middle, Upper, Rich")
    print("   • Health disparities: Wealth correlates with better health")
    print("   • Occupation effects: Manual labor = more stocky builds")
    print("   • Age patterns: Elderly lose muscle mass, gain weight variability")
    print()
    safe_print("🎨 VISUAL DIVERSITY:")
    print("   • 21 skin tones (European to African, all mixed heritage)")
    print("   • 8 hair colors (black to silver)")
    print("   • Hundreds of clothing combinations")
    print("   • Age-appropriate styling and proportions")
    print()
    safe_print("📐 CANVAS SIZES:")
    print("   • 32x32: Classic pixel art style")
    print("   • 64x64: High-resolution pixel art")
    print("   • 128x128: Ultra-detailed sprites")
    print("   • Custom: Any square size you need")
    print()
    safe_print("🎬 ANIMATION SYSTEM:")
    print("   • Idle: Subtle breathing and posture shifts")
    print("   • Walk: 4-8 frame locomotion cycles")
    print("   • Run: Dynamic movement with body bounce")
    print("   • Jump: Takeoff, hang, and landing poses")
    print("   • Sprite sheets: Industry-standard output")
    print()
    safe_print("🐝 GENESWARM MULTI-AGENT SYSTEM:")
    print("   • 5 specialized nano-tensor agents (<1KB total)")
    print("   • Weighted consensus voting")
    print("   • Online learning from feedback")
    print("   • 16-dimensional embedding memory")
    print("   • Deterministic with seed chaining")
    print("   • Agents: Body, Style, Diversity, Critic, Animator")
    print()
    safe_print("🔬 MATHEMATICAL RIGOR:")
    print("   • Every character gets unique parameter hash")
    print("   • Sprite pixel hash prevents visual duplicates") 
    print("   • Real demographic distributions (US Census data)")
    print("   • Medical BMI formulas: weight = (BMI × height²) ÷ 703")
    print()
    safe_print("🎯 TOTAL COMBINATIONS: 338,688,000+")
    print("   This means we can generate millions of unique humans")
    print("   before any mathematical possibility of repetition.")
    print()
    input("Press Enter to return to main menu...")
    main()

if __name__ == "__main__":
    main()
