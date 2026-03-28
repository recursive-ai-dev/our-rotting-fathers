# Our Rotting Father RPG

<div align="center">

**A narrative-driven dark fantasy turn-based RPG set on the colossal corpse of a rotting god**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

</div>

---

## 🌑 Vision

Explore a civilization of human-elf creatures whose culture, religion, and very psychology have been shaped by generations of exposure to divine decay. Their evolutionary advantage—**delusion and psychosis**—allows them to survive and thrive in conditions that would destroy any other species.

### Key Features

- **📖 Deep Narrative**: Branching storyline with multiple endings based on faction conflicts
- **⚔️ Turn-Based Combat**: Strategic combat integrated with sanity mechanics
- **🧠 Psychosis System**: Controlled descent into madness unlocks powers but changes the story
- **🏛️ Faction System**: Align with different groups, each with valid points and dark secrets
- **🗺️ Interconnected World**: Explore the god's anatomy as distinct biomes
- **🎨 Atmospheric Presentation**: Body horror visuals with dynamic psychosis-based color shifts

---

## 🌍 The World

### The Rotting God
An ancient, colossal deity whose corpse forms the entire world. The flesh continuously decays, releasing miasma and spores that affect all life. Different regions create distinct biomes:
- **The Withered Hand** - Starting area, Council territory
- **The Festering Heart** - Rotborn stronghold, high magic, high danger
- **The Bone Spires** - Purified fortresses, purification rituals
- **The Dreaming Mind** - Late-game area where prophetic visions manifest

### The Deludari (Children of Delusion)
Human-elf hybrid race evolved on the divine corpse with an innate resistance to madness through controlled psychosis. Their delusions manifest as protective mental filters.

### Major Factions

| Faction | Philosophy | Goal |
|---------|------------|------|
| **The Purified** | Seek to cleanse the rot | Salvation through purity |
| **Rotborn Embrace** | Worship the decay | Embrace mutation as divine |
| **The Sane Council** | Maintain rational governance | Survive despite universal madness |
| **Spore Prophets** | Interpret the god's dreams | Mystics reading hallucinations |

---

## 🎮 Core Systems

### Turn-Based Combat
- Strategic combat with **Psychosis Meter**
- High psychosis levels grant power but risk losing control
- Character classes tied to faction allegiances and rot exposure
- Enemies include mutated creatures, fanatics, and manifestations of collective hallucinations

### Dual Progression System
1. **Traditional**: Levels, stats, equipment, abilities
2. **Sanity Track**: Controlled descent into madness unlocks powers but alters the narrative

### Magic System
No firearms—technology stalled due to reliance on magical solutions. Mages channel the rot's energy directly, risking accelerated psychosis.

**Schools of Magic**:
- **Necrosis** - Decay and withering
- **Spore** - Growth and infestation
- **Bone** - Structure and permanence
- **Miasma** - Poison and corruption

---

## 🛠️ Tools

### Rotborn Recursion Engine
Located in `tools/rotborn-recursion/`, this is our procedural content generation system for creating unique character sprites and animations.

**Features**:
- Generate mathematically unique character sprites (32x32 to 128x128+)
- Create animation sprite sheets (idle, walk, run, jump)
- Trauma-based color palettes reflecting the god's dying memories
- Batch generation with metadata tracking

**Quick Start**:
```bash
cd tools/rotborn-recursion
python ai_human_generator.py
```

See [`tools/rotborn-recursion/README.md`](tools/rotborn-recursion/README.md) for detailed documentation.

---

## 📁 Project Structure

```
our-rotting-father-rpg/
├── conductor/              # Project management & documentation
│   ├── product.md          # Product definition & vision
│   ├── tech-stack.md       # Technical architecture
│   ├── workflow.md         # Development workflow
│   ├── code_styleguides/   # Coding standards
│   ├── lore/               # World lore & story documents
│   └── tracks/             # Development tracks & plans
└── tools/
    └── rotborn-recursion/  # Procedural content generation
        ├── generator/      # Sprite generation engine
        ├── app/            # Application UI
        ├── tests/          # Test suite
        └── scripts/        # Utility scripts
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+**
- **Git**

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/recursive-ai-dev/our-rotting-father-rpg.git
cd our-rotting-father-rpg
```

2. **Set up Rotborn Recursion Engine**
```bash
cd tools/rotborn-recursion
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Run the generator**
```bash
python ai_human_generator.py
```

---

## 📚 Documentation

- **[Product Definition](conductor/product.md)** - Full vision, features, and design
- **[Tech Stack](conductor/tech-stack.md)** - Technical architecture decisions
- **[Workflow](conductor/workflow.md)** - Development process and guidelines
- **[Lore](conductor/lore/)** - World building and story documents
- **[Rotborn Tools](tools/rotborn-recursion/README.md)** - Content generation tools

---

## 🎯 Development Status

**Current Phase**: Early Development

### Recent Updates
- ✅ Rotborn Recursion Engine with trauma palettes
- ✅ Procedural character sprite generation
- ✅ Animation system for game sprites
- ✅ Lore foundation and faction design
- 🚧 Core RPG engine development
- 🚧 Combat system implementation
- 🚧 Narrative branching system

---

## 🤝 Contributing

This is an active development project. To contribute:

1. Read the [development workflow](conductor/workflow.md)
2. Review the [code style guides](conductor/code_styleguides/)
3. Check open tracks in `conductor/tracks/`
4. Follow the established conventions

---

## 📄 License

MIT License - See [LICENSE](tools/rotborn-recursion/LICENSE) for details

---

## 🎨 Inspirations

- **Dark Souls** - Environmental storytelling, challenging combat
- **Blasphemous** - Religious horror, body horror aesthetics
- **Salt and Sanctuary** - 2D dark fantasy RPG mechanics
- **Disco Elysium** - Psychology as game mechanic, narrative depth
- **Pathologic** - Survival in hostile environment, time pressure

---

## 💬 Community & Support

- **Issues**: GitHub Issues for bugs and feature requests
- **Discussions**: GitHub Discussions for lore theories and design talks

---

<div align="center">

**"The swarm agents experienced these colors for a millennium inside the dying god. They don't remember what came before. These are the only colors that exist."**

*Built with ❤️ on the corpse of gods*

</div>
