# 🌌 AXIOM v1.0

**Adaptive eXemplary Intelligence Operating Matrix**

*An exploratory cognitive architecture integrating biologically-grounded neural dynamics, hierarchical predictive coding, and multi-system memory consolidation into a unified framework for studying emergent intelligence.*

---

## Overview

AXIOM is a research-oriented cognitive architecture that attempts to bridge the gap between computational neuroscience and artificial intelligence. Rather than treating cognition as a single monolithic process, AXIOM models it as an ensemble of interacting subsystems — each grounded in established neuroscience theory — that together give rise to behaviors we associate with learning, memory, attention, creativity, and self-awareness.

This project is an exercise in synthesis: taking well-studied computational principles (spiking neural dynamics, predictive coding, global workspace theory, hippocampal replay, neuromodulation) and exploring what happens when they operate together within a single integrated system.

> **Note:** AXIOM is an experimental research prototype. It is not a production AI system. The goal is exploration and understanding, not benchmark performance.

## Architecture

AXIOM's cognitive pipeline processes each input through 17 stages, organized across the following subsystems:

### Neural Substrate

- **32,000 adaptive spiking neurons** organized into 16 cortical columns
- Leaky integrate-and-fire dynamics with spike-frequency adaptation
- Spike-timing dependent plasticity (STDP) with dopamine-modulated three-factor learning
- Homeostatic plasticity and metaplasticity for long-term stability
- Inter-column connectivity with distance-dependent probability

### Hierarchical Predictive Coding

- 6-level hierarchy with increasing temporal integration constants (10ms → 3000ms)
- Precision-weighted prediction error minimization at each level
- Adaptive precision learning based on error statistics
- Top-down generative model for imagination and mental simulation

### Memory Systems

| System | Capacity | Inspired By |
|--------|----------|-------------|
| Working Memory | 7 ± 2 slots | Miller (1956) |
| Episodic Memory | 100,000 traces | Hippocampal rapid encoding |
| Semantic Memory | 500,000 concepts | Neocortical consolidation |

- Hippocampal replay with TD-error prioritization
- Synaptic tagging and capture for selective consolidation
- Awake replay (0.1 Hz) and sleep replay (2.0 Hz) cycles

### Attention & Consciousness

- Multi-head attention (8 heads) with salience computation
- **Global Workspace Theory** implementation: winner-take-all competition among cognitive coalitions
- Ignition threshold for conscious access (activation > 0.7)
- Integration measure (Φ) combining integration and differentiation

### Intrinsic Motivation

- Epistemic curiosity driven by prediction error and learning progress
- Competence tracking and novelty detection
- Autonomy and diversive curiosity as exploration signals

### Creativity & Insight

- Divergent thinking through temperature-controlled sampling
- Conceptual blending in embedding space
- Insight detection via sudden drops in cognitive load paired with large conceptual distances
- Analogical reasoning between distant memory traces

### Self-Model & Metacognition

- Recursive self-modeling with personality trait tracking (Big Five + curiosity/creativity)
- Confidence and uncertainty estimation
- Autobiographical narrative construction
- Metacognitive monitoring history

### Neuromodulation

| Modulator | Role | Baseline |
|-----------|------|----------|
| Dopamine | Reward prediction error, learning gating | 0.5 |
| Serotonin | Mood regulation, temporal discounting | 0.6 |
| Norepinephrine | Arousal, attention modulation | 0.4 |
| Acetylcholine | Attention, memory encoding | 0.5 |

### Dream Engine

- NREM-like consolidation through prioritized memory replay
- Semantic integration of frequently-replayed episodic traces
- Creative blending of distant memory traces during dream cycles

### Language Interface

AXIOM's internal cognitive processing is independent of language models. An optional LLM backend provides a natural language surface for interaction:

| Backend | Description |
|---------|-------------|
| `none` | Pure cognitive simulation (no LLM required) |
| `local_llama` | Local GGUF models via llama.cpp |
| `transformers_local` | HuggingFace Transformers (local) |
| `openai_http` | OpenAI-compatible API |
| `anthropic_http` | Anthropic Messages API |

When an LLM backend is active, AXIOM constructs a system prompt containing its internal state (surprise levels, active memories, curiosity signals, self-model) and asks the LLM to generate a first-person response that reflects that cognitive state. When no LLM is available, a simpler template-based response is generated.

## Theoretical Foundations

AXIOM draws on the following theoretical frameworks:

- **Free Energy Principle** (Friston, 2010) — Predictive coding and active inference as a unifying theory of brain function
- **Global Workspace Theory** (Baars, 1988) — Consciousness as a competitive broadcast mechanism
- **Complementary Learning Systems** (McClelland et al., 1995) — Dual hippocampal/neocortical memory with sleep consolidation
- **Self-Organized Criticality** (Bak et al., 1987) — Neural dynamics poised at the edge of chaos for optimal information processing
- **Intrinsic Motivation** (Oudeyer & Kaplan, 2007) — Curiosity-driven learning through prediction error and learning progress
- **STDP and Three-Factor Learning** (Gerstner et al., 2018) — Biologically plausible synaptic plasticity with neuromodulatory gating
- **Integrated Information Theory** (Tononi, 2004) — Quantifying consciousness through integration (Φ)

## Getting Started

### Requirements

| Component | Minimum |
|-----------|---------|
| Python | 3.11+ |
| RAM | 8 GB (16 GB recommended for local LLMs) |
| OS | Windows / Linux / macOS |

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/axiom.git
cd axiom

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate
# Activate (Linux/macOS)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

On Windows, `setup.bat` automates the full installation including PyTorch (CPU).

### Running

**CLI Mode:**
```bash
python axiom_v1.py
```

**Web UI (Gradio):**
```bash
python axiom_ui.py
```
Opens a browser interface at `http://localhost:7860` with real-time monitoring panels for neural dynamics, memory, consciousness, motivation, creativity, neuromodulation, and self-model states.

### Configuring an LLM Backend

Set environment variables before running:

```bash
# Local GGUF model (recommended for offline use)
export AXIOM_LLM_BACKEND=local_llama
export AXIOM_LLAMA_MODEL_PATH=/path/to/model.gguf
export AXIOM_LLM_CTX_WINDOW=2048
export AXIOM_LLM_MAX_TOKENS=512

# Or use an API
export AXIOM_LLM_BACKEND=openai_http
export OPENAI_API_KEY=sk-...
```

AXIOM runs fully without an LLM backend (`AXIOM_LLM_BACKEND=none`). All cognitive processing — neural simulation, memory, attention, creativity, self-modeling — operates independently. The LLM only provides natural language articulation of the internal state.

## Interactive Commands

| Command | Description |
|---------|-------------|
| `<text>` | Process input through the full cognitive pipeline |
| `/introspect` | Complete system state (JSON) |
| `/neural` | Neural substrate: columns, neurons, synapses, firing rates |
| `/memory` | Memory systems: working, episodic, semantic, replay statistics |
| `/consciousness` | Global workspace metrics and conscious content |
| `/creativity` | Insight detection and conceptual blending history |
| `/self` | Personality traits, confidence, self-awareness, narrative |
| `/motivation` | Curiosity, competence, novelty, learning progress |
| `/neuromod` | Dopamine, serotonin, norepinephrine, acetylcholine levels |
| `/criticality` | Avalanche exponents and branching ratios |
| `/performance` | Prediction accuracy, learning efficiency, creativity score |
| `/dream [min]` | Initiate offline consolidation cycle |
| `/checkpoint [name]` | Save brain state to disk |
| `/analytics` | Session metrics and timing statistics |

## Project Structure

```
axiom/
├── axiom_v1.py          # Core cognitive engine (~4,000 lines)
├── axiom_ui.py           # Gradio web interface
├── requirements.txt      # Python dependencies
├── setup.bat             # Windows automated setup
├── run.bat               # Windows CLI launcher
├── run_ui.bat            # Windows Web UI launcher
└── README.md
```

Runtime data is stored in `~/.axiom/`:

```
~/.axiom/
├── logs/                 # Session logs
├── memories/             # Persistent memory storage
├── dreams/               # Dream cycle records
├── insights/             # Detected creative insights
├── checkpoints/          # Brain state snapshots (pickle + SQLite)
└── analytics/            # Performance analytics
```

## Limitations & Honest Notes

- **This is not AGI.** AXIOM is a structured simulation that models cognitive *processes*, not cognitive *capabilities*. The spiking neurons do not learn representations in the way biological neurons do at scale.
- **The embedding engine is hash-based**, not learned. Semantic similarity is approximate at best. Replacing it with a proper embedding model would significantly improve memory retrieval quality.
- **Consciousness metrics (Φ) are simplified proxies.** They capture structural properties (integration, differentiation) but should not be interpreted as evidence of phenomenal consciousness.
- **Performance on CPU is modest.** Simulating 32,000 spiking neurons per input takes roughly 1–3 seconds. The LLM generation step (if using a local model) adds 10–60 seconds depending on model size and hardware.
- **The architecture is monolithic.** A future refactor into modular, testable components would improve both research utility and code quality.

## Future Directions

Some open questions and possible extensions:

- Replace hash-based embeddings with a lightweight learned encoder
- Implement proper synaptic consolidation with complementary learning system dynamics
- Add sensory grounding (vision, audio) beyond text
- Explore emergent communication between multiple AXIOM instances
- Integrate with reinforcement learning environments for embodied cognition
- Formalize the relationship between free energy minimization and the global workspace
- Benchmark internal representations against cognitive science experimental data

## References

- Baars, B. J. (1988). *A Cognitive Theory of Consciousness*. Cambridge University Press.
- Bak, P., Tang, C., & Wiesenfeld, K. (1987). Self-organized criticality. *Physical Review Letters*, 59(4), 381.
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127–138.
- Gerstner, W., Lehmann, M., Liakoni, V., Corneil, D., & Brea, J. (2018). Eligibility traces and plasticity on behavioral time scales. *Frontiers in Neural Circuits*, 12, 53.
- McClelland, J. L., McNaughton, B. L., & O'Reilly, R. C. (1995). Why there are complementary learning systems in the hippocampus and neocortex. *Psychological Review*, 102(3), 419.
- Miller, G. A. (1956). The magical number seven, plus or minus two. *Psychological Review*, 63(2), 81.
- Oudeyer, P.-Y., & Kaplan, F. (2007). What is intrinsic motivation? A typology of computational approaches. *Frontiers in Neurorobotics*, 1, 6.
- Tononi, G. (2004). An information integration theory of consciousness. *BMC Neuroscience*, 5(1), 42.

## License

MIT

---

<p align="center"><em>"The Foundation of Next-Generation Cognitive Systems"</em></p>
