#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🌌 AXIOM v1.0 - Adaptive eXemplary Intelligence Operating Matrix          ║
║                                                                              ║
║   "The Foundation of Next-Generation Cognitive Systems"                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Author: Advanced Synthesis
Version: 1.0.0
Build: 2026-01-29
License: MIT
Python: >=3.11
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import math
import os
import pickle
import random
import sqlite3
import sys
import time
import uuid
from collections import defaultdict, deque
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Deque, Dict, List, Optional, Set, Tuple, Union

import numpy as np
from ddgs import DDGS
from langdetect import detect as detect_language
from numpy.typing import NDArray

# ── Windows UTF-8 fix (emoji support in console/logging) ─────────────────────
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

VERSION = "1.0.0"
CODENAME = "AXIOM"
SYMBOL = "🌌"
BUILD_DATE = "2025-01-29"

HOME = Path(os.getenv("AXIOM_HOME", "~/.axiom")).expanduser()
HOME.mkdir(parents=True, exist_ok=True)
for subdir in ["logs", "memories", "dreams", "insights", "checkpoints", "analytics"]:
    (HOME / subdir).mkdir(exist_ok=True)

FloatArray = NDArray[np.float32]


@dataclass(frozen=True)
class AxiomConfig:
    """Complete AXIOM configuration with scientific grounding."""

    # === NEURAL SUBSTRATE ===
    state_dim: int = 1024
    num_cortical_columns: int = 16
    neurons_per_column: int = 2000
    excitatory_ratio: float = 0.85

    # === SPIKING DYNAMICS ===
    dt_ms: float = 0.5  # Integration timestep
    V_rest: float = -70.0  # mV
    V_threshold: float = -50.0
    V_reset: float = -65.0
    tau_membrane: float = 20.0
    tau_adaptation: float = 100.0
    refractory_period_ms: float = 2.0

    # === SPIKE-TIMING DEPENDENT PLASTICITY ===
    stdp_enabled: bool = True
    stdp_tau_plus: float = 20.0  # LTP time constant
    stdp_tau_minus: float = 20.0  # LTD time constant
    stdp_A_plus: float = 0.005  # LTP amplitude
    stdp_A_minus: float = 0.00525  # LTD amplitude (slightly larger)
    stdp_w_min: float = 0.0
    stdp_w_max: float = 2.0
    dopamine_modulation: bool = True

    # === HOMEOSTATIC PLASTICITY ===
    target_firing_rate_hz: float = 5.0
    homeostasis_tau_hours: float = 24.0
    bcm_threshold_adaptive: bool = True
    metaplasticity_enabled: bool = True

    # === HIERARCHICAL PREDICTIVE CODING ===
    hierarchy_levels: int = 6
    prediction_error_weight: float = 0.6
    precision_learning_rate: float = 0.01
    hierarchical_tau_ms: List[float] = field(
        default_factory=lambda: [10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0]
    )

    # === ACTIVE INFERENCE ===
    free_energy_enabled: bool = True
    belief_update_rate: float = 0.1
    action_selection_temperature: float = 0.5
    epistemic_value_weight: float = 0.3
    pragmatic_value_weight: float = 0.7

    # === MEMORY SYSTEMS ===
    working_memory_capacity: int = 7
    episodic_capacity: int = 100000
    semantic_capacity: int = 500000
    consolidation_threshold: float = 0.75
    synaptic_tagging_duration_hours: float = 3.0

    # === HIPPOCAMPAL REPLAY ===
    replay_enabled: bool = True
    awake_replay_rate_hz: float = 0.1
    sleep_replay_rate_hz: float = 2.0
    replay_sequence_length: int = 50
    prioritized_replay: bool = True
    td_error_priority_weight: float = 0.8

    # === ATTENTION & CONSCIOUSNESS ===
    attention_heads: int = 8
    attention_temperature: float = 0.5
    gw_ignition_threshold: float = 0.7
    gw_competition_strength: float = 0.8
    consciousness_integration_window_ms: float = 100.0

    # === INTRINSIC MOTIVATION ===
    curiosity_weight: float = 0.4
    competence_weight: float = 0.3
    novelty_bonus_scale: float = 0.5
    learning_progress_window: int = 100

    # === META-LEARNING ===
    meta_learning_enabled: bool = True
    maml_inner_steps: int = 5
    maml_inner_lr: float = 0.01
    maml_outer_lr: float = 0.001
    meta_plasticity_tau_hours: float = 12.0

    # === CRITICALITY & EMERGENCE ===
    self_organized_criticality: bool = True
    avalanche_threshold: float = 0.65
    branching_ratio_target: float = 1.0

    # === CREATIVITY & INSIGHT ===
    divergent_temperature: float = 1.5
    constraint_relaxation_rate: float = 0.1
    conceptual_blending_enabled: bool = True
    insight_detection_threshold: float = 0.8

    # === SOCIAL COGNITION ===
    theory_of_mind_depth: int = 3
    empathy_coefficient: float = 0.7
    mirror_neuron_system: bool = True

    # === AUTOBIOGRAPHICAL SELF ===
    narrative_construction: bool = True
    self_model_update_rate: float = 0.001
    identity_coherence_weight: float = 0.6

    # === DREAMING & CONSOLIDATION ===
    dream_enabled: bool = True
    nrem_duration_minutes: float = 5.0
    rem_duration_minutes: float = 2.0
    dream_replay_temperature: float = 2.0
    consolidation_strength: float = 0.2

    # === NEUROMODULATION ===
    dopamine_baseline: float = 0.5
    serotonin_baseline: float = 0.6
    norepinephrine_baseline: float = 0.4
    acetylcholine_baseline: float = 0.5

    # === SYSTEM ===
    seed: int = 42
    log_level: str = "INFO"
    analytics_enabled: bool = True


def _auto_scale_config() -> AxiomConfig:
    """Scale neural substrate based on available system RAM."""
    try:
        import ctypes
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(stat)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
        avail_gb = stat.ullAvailPhys / (1024**3)
    except Exception:
        avail_gb = 8.0  # conservative fallback

    # Scale: <6GB → tiny, <10GB → small, <20GB → medium, else → full
    if avail_gb < 6:
        cols, neurons = 4, 200
    elif avail_gb < 10:
        cols, neurons = 6, 500
    elif avail_gb < 20:
        cols, neurons = 8, 800
    else:
        cols, neurons = 16, 2000

    return AxiomConfig(num_cortical_columns=cols, neurons_per_column=neurons)

CFG = _auto_scale_config()
random.seed(CFG.seed)
np.random.seed(CFG.seed)

# ══════════════════════════════════════════════════════════════════════════════
# LOGGING SYSTEM WITH ADVANCED METRICS
# ══════════════════════════════════════════════════════════════════════════════


class AxiomLogger:
    """Advanced logging with real-time metrics tracking."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.start_time = time.time()

        self.logger = logging.getLogger(f"AXIOM.{session_id}")
        self.logger.setLevel(getattr(logging, CFG.log_level.upper(), logging.INFO))

        if not self.logger.handlers:
            # Console handler
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(
                logging.Formatter(
                    f"{SYMBOL} %(asctime)s | %(levelname)-8s | %(message)s",
                    datefmt="%H:%M:%S",
                )
            )
            self.logger.addHandler(ch)

            # File handler
            log_file = (
                HOME
                / "logs"
                / f"axiom_{session_id}_{datetime.now():%Y%m%d_%H%M%S}.log"
            )
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setFormatter(
                logging.Formatter(
                    "%(asctime)s | %(levelname)-8s | %(funcName)s | %(message)s"
                )
            )
            self.logger.addHandler(fh)

        # Metrics storage
        self.metrics: Dict[str, Deque[Tuple[float, float]]] = defaultdict(
            lambda: deque(maxlen=10000)
        )
        self.counters: Dict[str, int] = defaultdict(int)
        self.timers: Dict[str, List[float]] = defaultdict(list)

    def log(self, msg: str, level: str = "info", **kwargs: Any) -> None:
        """Log message with optional metadata."""
        if kwargs:
            try:
                meta = json.dumps(kwargs, default=str)
            except Exception:
                meta = str(kwargs)
            msg = f"{msg} | {meta}"
        getattr(self.logger, level.lower())(msg)

    def metric(self, name: str, value: float, timestamp: Optional[float] = None) -> None:
        """Record time-series metric."""
        t = timestamp or (time.time() - self.start_time)
        self.metrics[name].append((t, float(value)))

    def counter(self, name: str, delta: int = 1) -> None:
        """Increment counter."""
        self.counters[name] += delta

    def timer_start(self, name: str) -> float:
        """Start timer for operation."""
        t = time.perf_counter()
        self.timers[f"{name}_start"] = [t]
        return t

    def timer_end(self, name: str) -> float:
        """End timer and record duration."""
        if f"{name}_start" not in self.timers:
            return 0.0
        start = self.timers[f"{name}_start"][0]
        duration = time.perf_counter() - start
        self.timers[name].append(duration)
        return duration

    def get_stats(self, metric_name: str) -> Dict[str, float]:
        """Get statistics for a metric."""
        if metric_name not in self.metrics:
            return {}
        values = [v for _, v in self.metrics[metric_name]]
        if not values:
            return {}
        return {
            "mean": float(np.mean(values)),
            "std": float(np.std(values)),
            "min": float(np.min(values)),
            "max": float(np.max(values)),
            "count": len(values),
        }


LOG: Optional[AxiomLogger] = None


def get_log() -> AxiomLogger:
    """Get global logger instance."""
    global LOG
    if LOG is None:
        LOG = AxiomLogger("bootstrap")
    return LOG


# ══════════════════════════════════════════════════════════════════════════════
# OPTIONAL DEPENDENCIES & LLM CONFIG (LUMINA-STYLE ROUTER)
# ══════════════════════════════════════════════════════════════════════════════

DEPS: Dict[str, bool] = {
    "numpy": True,
    "torch": False,
    "transformers": False,
    "openai": False,
    "anthropic": False,
    "llama_cpp": False,
    "sentence_transformers": False,
}

# --- PyTorch (for local Transformers) -----------------------------------------
try:
    import torch
    from torch import Tensor

    DEPS["torch"] = True
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
except ImportError:  # pragma: no cover
    torch = None  # type: ignore
    Tensor = None  # type: ignore
    DEVICE = "cpu"

# --- HuggingFace Transformers -------------------------------------------------
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer

    DEPS["transformers"] = True
except ImportError:  # pragma: no cover
    AutoModelForCausalLM = None  # type: ignore
    AutoTokenizer = None  # type: ignore
    DEPS["transformers"] = False

# --- OpenAI / OpenAI-compatible HTTP -----------------------------------------
try:
    from openai import AsyncOpenAI

    DEPS["openai"] = True
except ImportError:  # pragma: no cover
    AsyncOpenAI = None  # type: ignore
    DEPS["openai"] = False

# --- Anthropic ----------------------------------------------------------------
try:
    import anthropic

    DEPS["anthropic"] = True
except ImportError:  # pragma: no cover
    anthropic = None  # type: ignore
    DEPS["anthropic"] = False

# --- llama.cpp (local GGUF: Qwen2.5, LLaMA, ...) -----------------------------
os.environ.setdefault("GGML_CPU_NO_REPACK", "1")  # avoid 3GB+ repack buffer OOM
try:
    from llama_cpp import Llama  # type: ignore

    DEPS["llama_cpp"] = True
except ImportError:  # pragma: no cover
    Llama = None  # type: ignore
    DEPS["llama_cpp"] = False

# --- Sentence Transformers ----------------------------------------------------
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
try:
    from sentence_transformers import SentenceTransformer
    DEPS["sentence_transformers"] = True
except ImportError:
    SentenceTransformer = None  # type: ignore
    DEPS["sentence_transformers"] = False

# --- LLM ENV CONFIG -----------------------------------------------------------

DEFAULT_LLAMA_MODEL_PATH = os.getenv(
    "AXIOM_LLAMA_MODEL_PATH",
    r"D:/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf",
)

DEFAULT_TRANSFORMERS_MODEL = os.getenv(
    "AXIOM_TRANSFORMERS_MODEL",
    "Qwen/Qwen2.5-7B-Instruct",
)

AXIOM_LLM_BACKEND = os.getenv("AXIOM_LLM_BACKEND", "none").lower()
OPENAI_MODEL = os.getenv("AXIOM_OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_BASE_URL = os.getenv("AXIOM_OPENAI_BASE_URL")
ANTHROPIC_MODEL = os.getenv("AXIOM_ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")

LLM_MAX_TOKENS_DEFAULT = int(os.getenv("AXIOM_LLM_MAX_TOKENS", "8192"))
LLM_TEMPERATURE_DEFAULT = float(os.getenv("AXIOM_LLM_TEMPERATURE", "0.75"))
LLM_CTX_WINDOW = int(os.getenv("AXIOM_LLM_CTX_WINDOW", "32768"))


class LLMRouter:
    """
    Unified LLM router for AXIOM.

    Backends:
      - none              : disabled
      - openai_http       : OpenAI / compatible endpoint (AsyncOpenAI)
      - anthropic_http    : Anthropic Messages API
      - transformers_local: local HF Transformers model
      - local_llama       : local llama.cpp GGUF (Qwen2.5, LLaMA, ...)
    """

    def __init__(self) -> None:
        self.backend: str = AXIOM_LLM_BACKEND
        self.device: str = str(DEVICE) if "DEVICE" in globals() else "cpu"

        self.hf_tokenizer = None
        self.hf_model = None
        self.llama = None

        self._init_backend()

    def _init_backend(self) -> None:
        log = get_log()
        if self.backend == "none":
            log.log("LLM backend: none (AXIOM running in pure simulation mode)")
            return

        if self.backend == "transformers_local":
            if not (DEPS["transformers"] and DEPS["torch"]):
                log.log(
                    "Transformers / torch not available; disabling transformers_local backend",
                    level="warning",
                )
                self.backend = "none"
                return
            try:
                log.log(
                    f"Loading local Transformers model: {DEFAULT_TRANSFORMERS_MODEL}"
                )
                self.hf_tokenizer = AutoTokenizer.from_pretrained(
                    DEFAULT_TRANSFORMERS_MODEL
                )
                self.hf_model = AutoModelForCausalLM.from_pretrained(
                    DEFAULT_TRANSFORMERS_MODEL
                ).to(self.device)
                if (
                    self.hf_tokenizer.pad_token_id is None
                    and self.hf_tokenizer.eos_token_id is not None
                ):
                    self.hf_tokenizer.pad_token_id = self.hf_tokenizer.eos_token_id
                log.log("Transformers backend ready")
            except Exception as e:  # noqa: BLE001
                log.log(
                    f"Failed to initialize transformers_local backend: {e}",
                    level="error",
                )
                self.backend = "none"

        elif self.backend == "local_llama":
            if not DEPS["llama_cpp"]:
                log.log(
                    "llama_cpp not available; disabling local_llama backend",
                    level="warning",
                )
                self.backend = "none"
                return
            try:
                n_threads = min(max(2, os.cpu_count() or 4), 8)
                log.log(f"Loading llama.cpp model: {DEFAULT_LLAMA_MODEL_PATH}")
                log.log(f"  n_ctx={LLM_CTX_WINDOW}, n_threads={n_threads}")
                self.llama = Llama(
                    model_path=DEFAULT_LLAMA_MODEL_PATH,
                    n_ctx=LLM_CTX_WINDOW,
                    n_threads=n_threads,
                    logits_all=False,
                    verbose=False,
                )
                log.log("llama.cpp backend ready")
            except Exception as e:  # noqa: BLE001
                log.log(
                    f"Failed to initialize local_llama backend: {e}", level="error"
                )
                self.backend = "none"

        elif self.backend == "openai_http":
            if not DEPS["openai"]:
                log.log(
                    "openai library not available; disabling openai_http backend",
                    level="warning",
                )
                self.backend = "none"
            else:
                log.log(
                    f"OpenAI-style HTTP backend selected | model={OPENAI_MODEL}",
                    level="info",
                )

        elif self.backend == "anthropic_http":
            if not DEPS["anthropic"]:
                log.log(
                    "anthropic library not available; disabling anthropic_http backend",
                    level="warning",
                )
                self.backend = "none"
            else:
                log.log(
                    f"Anthropic HTTP backend selected | model={ANTHROPIC_MODEL}",
                    level="info",
                )

        else:
            log.log(
                f"Unknown AXIOM_LLM_BACKEND='{self.backend}', disabling LLM backend",
                level="warning",
            )
            self.backend = "none"

    def is_available(self) -> bool:
        return self.backend != "none"

    async def acomplete(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = LLM_TEMPERATURE_DEFAULT,
        max_tokens: int = LLM_MAX_TOKENS_DEFAULT,
    ) -> Optional[str]:
        """Unified async completion method."""
        if self.backend == "none":
            return None

        if self.backend == "openai_http" and AsyncOpenAI is not None:
            client = AsyncOpenAI(
                base_url=OPENAI_BASE_URL or None,
            )
            resp = await client.chat.completions.create(
                model=OPENAI_MODEL,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            text = resp.choices[0].message.content or ""
            return text.strip()

        if self.backend == "anthropic_http" and anthropic is not None:
            client = anthropic.Anthropic()
            msg = client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt},
                ],
            )
            parts = getattr(msg, "content", [])
            text = ""
            for p in parts:
                if getattr(p, "type", None) == "text":
                    text += getattr(p, "text", "")
            return text.strip() or None

        if self.backend == "transformers_local" and self.hf_model is not None:
            # Run local HF model
            full_prompt = system_prompt.strip() + "\n\n" + user_prompt.strip()
            inputs = self.hf_tokenizer(
                full_prompt,
                return_tensors="pt",
            ).to(self.device)
            input_len = inputs["input_ids"].shape[1]
            with torch.no_grad():
                output_ids = self.hf_model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    do_sample=True,
                    temperature=temperature,
                    pad_token_id=self.hf_tokenizer.pad_token_id,
                )
            gen_ids = output_ids[0, input_len:]
            text = self.hf_tokenizer.decode(
                gen_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
            )
            return text.strip() or None

        if self.backend == "local_llama" and self.llama is not None:
            # Use ChatML format for instruct models (Qwen2.5, etc.)
            full_prompt = (
                "<|im_start|>system\n"
                f"{system_prompt.strip()}\n"
                "<|im_end|>\n"
                "<|im_start|>user\n"
                f"{user_prompt.strip()}\n"
                "<|im_end|>\n"
                "<|im_start|>assistant\n"
            )
            res = self.llama(
                full_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["</s>", "<|im_end|>", "<|im_start|>", "USER:", "SYSTEM:"],
                repeat_penalty=1.15,
            )
            # llama.cpp returns dict with "choices"
            try:
                text = res["choices"][0]["text"]
            except Exception:
                text = str(res)
            return text.strip() or None

        # Fallback if something went wrong
        return None

    async def astream_complete(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = LLM_TEMPERATURE_DEFAULT,
        max_tokens: int = LLM_MAX_TOKENS_DEFAULT,
    ):
        """Unified async streaming completion. Yields text chunks."""
        if self.backend == "none":
            return

        if self.backend == "local_llama" and self.llama is not None:
            full_prompt = (
                "<|im_start|>system\n"
                f"{system_prompt.strip()}\n"
                "<|im_end|>\n"
                "<|im_start|>user\n"
                f"{user_prompt.strip()}\n"
                "<|im_end|>\n"
                "<|im_start|>assistant\n"
            )
            for chunk in self.llama(
                full_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["</s>", "<|im_end|>", "<|im_start|>", "USER:", "SYSTEM:"],
                repeat_penalty=1.15,
                stream=True,
            ):
                try:
                    token = chunk["choices"][0]["text"]
                    if token:
                        yield token
                except (KeyError, IndexError):
                    pass
            return

        if self.backend == "openai_http" and AsyncOpenAI is not None:
            client = AsyncOpenAI(base_url=OPENAI_BASE_URL or None)
            stream = await client.chat.completions.create(
                model=OPENAI_MODEL,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                stream=True,
            )
            async for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield delta.content
            return

        if self.backend == "anthropic_http" and anthropic is not None:
            client = anthropic.Anthropic()
            with client.messages.stream(
                model=ANTHROPIC_MODEL,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            ) as stream:
                for text_chunk in stream.text_stream:
                    yield text_chunk
            return

        if self.backend == "transformers_local" and self.hf_model is not None:
            full_prompt = system_prompt.strip() + "\n\n" + user_prompt.strip()
            inputs = self.hf_tokenizer(full_prompt, return_tensors="pt").to(self.device)
            input_len = inputs["input_ids"].shape[1]
            with torch.no_grad():
                output_ids = self.hf_model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    do_sample=True,
                    temperature=temperature,
                    pad_token_id=self.hf_tokenizer.pad_token_id,
                )
            gen_ids = output_ids[0, input_len:]
            text = self.hf_tokenizer.decode(
                gen_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
            )
            if text.strip():
                yield text.strip()
            return


# ══════════════════════════════════════════════════════════════════════════════
# MATHEMATICAL UTILITIES & SIGNAL PROCESSING
# ══════════════════════════════════════════════════════════════════════════════

class MathOps:
    """Advanced mathematical operations for neural computation."""

    @staticmethod
    def sigmoid(x: FloatArray, temperature: float = 1.0) -> FloatArray:
        """Numerically stable sigmoid with temperature."""
        x = np.clip(x / temperature, -500, 500)
        return 1.0 / (1.0 + np.exp(-x))

    @staticmethod
    def softmax(x: FloatArray, temperature: float = 1.0, axis: int = -1) -> FloatArray:
        """Numerically stable softmax."""
        x = x / temperature
        x_max = np.max(x, axis=axis, keepdims=True)
        exp_x = np.exp(x - x_max)
        return exp_x / (np.sum(exp_x, axis=axis, keepdims=True) + 1e-12)

    @staticmethod
    def cosine_similarity(a: FloatArray, b: FloatArray) -> float:
        """Cosine similarity between vectors."""
        a = np.asarray(a, dtype=np.float32).flatten()
        b = np.asarray(b, dtype=np.float32).flatten()
        n = min(len(a), len(b))
        a, b = a[:n], b[:n]
        norm_product = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-12
        return float(np.dot(a, b) / norm_product)

    @staticmethod
    def gaussian_kernel(size: int, sigma: float = 1.0) -> FloatArray:
        """1D Gaussian kernel for smoothing."""
        x = np.arange(size) - size // 2
        kernel = np.exp(-x**2 / (2 * sigma**2))
        return (kernel / np.sum(kernel)).astype(np.float32)

    @staticmethod
    def convolve_1d(signal: FloatArray, kernel: FloatArray) -> FloatArray:
        """1D convolution."""
        result = np.convolve(signal, kernel, mode="same")
        return result.astype(np.float32)

    @staticmethod
    def power_law_sample(alpha: float, size: int = 1) -> FloatArray:
        """Sample from power law distribution: P(x) ~ x^(-alpha)."""
        u = np.random.uniform(0, 1, size)
        samples = (1 - u) ** (1 / (1 - alpha))
        return samples.astype(np.float32)

    @staticmethod
    def entropy(probabilities: FloatArray) -> float:
        """Shannon entropy: H = -Σ p log p."""
        p = np.asarray(probabilities, dtype=np.float32)
        p = p[p > 0]  # Remove zeros
        return float(-np.sum(p * np.log2(p + 1e-12)))

    @staticmethod
    def mutual_information(joint_prob: FloatArray) -> float:
        """Mutual information from joint probability matrix."""
        joint = np.asarray(joint_prob, dtype=np.float32)
        joint = joint / (np.sum(joint) + 1e-12)

        p_x = np.sum(joint, axis=1, keepdims=True)
        p_y = np.sum(joint, axis=0, keepdims=True)
        independent = p_x @ p_y

        # MI = Σ p(x,y) log(p(x,y) / (p(x)p(y)))
        mask = joint > 0
        mi = np.sum(
            joint[mask]
            * np.log2((joint[mask] / (independent[mask] + 1e-12)) + 1e-12)
        )
        return float(mi)


class EmbeddingEngine:
    """Production-ready embedding engine."""

    _model = None
    _api_client = None

    @classmethod
    def init_engine(cls, llm_router=None):
        """Initialize sentence-transformers or API fallback."""
        if cls._model is not None or cls._api_client is not None:
            return

        if DEPS.get("sentence_transformers") and SentenceTransformer is not None:
            try:
                device = "cuda" if DEPS.get("torch") and getattr(torch, "cuda", None) and torch.cuda.is_available() else "cpu"
                cls._model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
                get_log().log(f"EmbeddingEngine initialized with sentence-transformers on {device}")
                return
            except Exception as e:
                get_log().log(f"Failed to load sentence-transformers: {e}", level="warning")
        
        if llm_router and getattr(llm_router, "backend", "") == "openai_http" and AsyncOpenAI is not None:
            try:
                cls._api_client = AsyncOpenAI(base_url=OPENAI_BASE_URL or None)
                get_log().log("EmbeddingEngine initialized with OpenAI fallback")
                return
            except Exception:
                pass
             
        get_log().log("EmbeddingEngine using heuristic hash fallback (no semantic models found)", level="warning")

    @classmethod
    async def aembed(cls, text: str, dim: int) -> FloatArray:
        """Generate semantic embeddings asynchronously."""
        raw_emb = None

        if cls._model is not None:
            raw_emb = cls._model.encode([text], convert_to_numpy=True)[0]
        elif cls._api_client is not None:
            try:
                resp = await cls._api_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text
                )
                raw_emb = np.array(resp.data[0].embedding, dtype=np.float32)
            except Exception as e:
                get_log().log(f"API embedding failed: {e}", level="error")

        if raw_emb is None:
            h1 = hashlib.sha512(text.encode("utf-8")).digest()
            h2 = hashlib.blake2b(text.encode("utf-8"), digest_size=64).digest()
            combined = h1 + h2
            raw = np.frombuffer(combined, dtype=np.uint8).astype(np.float32)
            if len(raw) < dim:
                raw = np.tile(raw, (dim // len(raw)) + 1)[:dim]
            else:
                raw = raw[:dim]
            embedding = (raw / 255.0) * 2.0 - 1.0
        else:
            raw_dim = len(raw_emb)
            if raw_dim != dim:
                np.random.seed(42)  # Deterministic projection
                projection = np.random.randn(raw_dim, dim).astype(np.float32) / np.sqrt(raw_dim)
                embedding = raw_emb @ projection
                np.random.seed()
            else:
                embedding = raw_emb

        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        return embedding.astype(np.float32)


# ══════════════════════════════════════════════════════════════════════════════
# ADAPTIVE SPIKING NEURONS WITH HOMEOSTASIS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class SpikeEvent:
    """Record of a spike event."""

    neuron_id: int
    timestamp: float
    voltage: float


class AdaptiveSpikingNeuron:
    """
    Leaky Integrate-and-Fire neuron with:

    - Adaptive threshold (BCM-like)
    - Spike-frequency adaptation
    - Homeostatic plasticity
    - Intrinsic excitability regulation
    """

    def __init__(
        self,
        neuron_id: int,
        neuron_type: str = "excitatory",
        target_rate: float = CFG.target_firing_rate_hz,
    ):
        self.neuron_id = neuron_id
        self.neuron_type = neuron_type
        self.target_rate = target_rate

        # Membrane dynamics
        self.V = CFG.V_rest
        self.V_threshold = CFG.V_threshold
        self.w_adaptation = 0.0  # Adaptation current

        # Input currents
        self.I_syn = 0.0
        self.I_external = 0.0

        # Spike history
        self.spike_times: Deque[float] = deque(maxlen=1000)
        self.last_spike_time = -np.inf
        self.refractory_until = -np.inf

        # Homeostatic regulation
        self.intrinsic_excitability = 1.0
        self.firing_rate_ema = 0.0  # Exponential moving average
        self.homeostasis_tau = CFG.homeostasis_tau_hours * 3600.0 * 1000.0  # ms

        # Meta-plasticity (learning rate modulation)
        self.plasticity_factor = 1.0
        self.recent_activity: Deque[float] = deque(maxlen=100)

        # Statistics
        self.total_spikes = 0
        self.isi_history: Deque[float] = deque(maxlen=100)

    def receive_synaptic_input(self, current: float) -> None:
        """Receive synaptic current from presynaptic neurons."""
        self.I_syn += float(current)

    def set_external_input(self, current: float) -> None:
        """Set external input current."""
        self.I_external = float(current)

    def step(self, dt_ms: float, t_ms: float) -> bool:
        """
        Integrate membrane dynamics for one timestep.
        Returns True if neuron fired.
        """
        # Check refractory period
        if t_ms < self.refractory_until:
            self.V = CFG.V_reset
            self.I_syn = 0.0
            self.I_external = 0.0
            return False

        # Total input current (modulated by intrinsic excitability)
        I_total = (self.I_syn + self.I_external) * self.intrinsic_excitability

        # Membrane potential dynamics: dV/dt = (V_rest - V + R·I) / tau
        dV = (
            (CFG.V_rest - self.V + 10.0 * I_total - self.w_adaptation)
            / CFG.tau_membrane
        ) * dt_ms
        self.V += dV

        # Adaptation dynamics: dw/dt = (a(V - V_rest) - w) / tau_w
        dw = (
            (0.001 * (self.V - CFG.V_rest) - self.w_adaptation)
            / CFG.tau_adaptation
            * dt_ms
        )
        self.w_adaptation += dw

        # Reset inputs
        self.I_syn = 0.0
        self.I_external = 0.0

        # Check for spike
        if self.V >= self.V_threshold:
            # Fire spike
            self.V = CFG.V_reset
            self.w_adaptation += 0.1  # Spike-triggered adaptation
            self.refractory_until = t_ms + CFG.refractory_period_ms

            # Record spike
            if self.spike_times:
                isi = t_ms - self.last_spike_time
                self.isi_history.append(isi)

            self.spike_times.append(t_ms)
            self.last_spike_time = t_ms
            self.total_spikes += 1

            # Update firing rate estimate
            if len(self.spike_times) >= 2:
                recent_rate = len(self.spike_times) / (
                    (self.spike_times[-1] - self.spike_times[0]) / 1000.0 + 1e-6
                )
                alpha = 0.1
                self.firing_rate_ema = (1 - alpha) * self.firing_rate_ema + alpha * (
                    recent_rate
                )

            self.recent_activity.append(1.0)

            return True

        self.recent_activity.append(0.0)
        return False

    def homeostatic_update(self, dt_ms: float) -> None:
        """
        Homeostatic plasticity: regulate firing rate toward target.
        Based on Turrigiano & Nelson (2004).
        """
        if len(self.spike_times) < 5:
            return

        # Compute recent firing rate
        window_ms = 1000.0  # 1 second window
        recent_spikes = sum(
            1 for t in self.spike_times if self.last_spike_time - t <= window_ms
        )
        actual_rate = recent_spikes  # Hz

        # Error signal
        error = self.target_rate - actual_rate

        # Update intrinsic excitability with slow time constant
        alpha = dt_ms / self.homeostasis_tau
        self.intrinsic_excitability += alpha * error * 0.01
        self.intrinsic_excitability = float(
            np.clip(self.intrinsic_excitability, 0.1, 5.0)
        )

        # BCM-like adaptive threshold
        if CFG.bcm_threshold_adaptive:
            threshold_shift = 0.001 * (actual_rate - self.target_rate)
            self.V_threshold += threshold_shift
            self.V_threshold = float(np.clip(self.V_threshold, -60.0, -45.0))

    def metaplasticity_update(self) -> None:
        """
        Meta-plasticity: modulate learning rate based on recent activity.
        High variance -> increase plasticity (exploration)
        Low variance -> decrease plasticity (consolidation)
        """
        if not CFG.metaplasticity_enabled or len(self.recent_activity) < 20:
            return

        activity_variance = float(np.var(list(self.recent_activity)))

        # Plasticity increases with variance
        target_plasticity = 0.5 + 1.0 * activity_variance
        self.plasticity_factor = (
            0.95 * self.plasticity_factor + 0.05 * target_plasticity
        )
        self.plasticity_factor = float(
            np.clip(self.plasticity_factor, 0.1, 2.0)
        )

    def get_firing_rate(self) -> float:
        """Get current firing rate estimate."""
        return float(self.firing_rate_ema)

    def get_cv_isi(self) -> float:
        """Get coefficient of variation of inter-spike intervals (regularity measure)."""
        if len(self.isi_history) < 2:
            return 0.0
        isi_array = np.array(list(self.isi_history))
        cv = float(np.std(isi_array) / (np.mean(isi_array) + 1e-6))
        return cv


# ══════════════════════════════════════════════════════════════════════════════
# ADVANCED STDP SYNAPSES WITH DOPAMINE MODULATION
# ══════════════════════════════════════════════════════════════════════════════

class STDPSynapse:
    """
    Spike-Timing-Dependent Plasticity synapse with:

    - Classical STDP (Bi & Poo, 1998)
    - Dopamine modulation (Izhikevich, 2007)
    - Synaptic tagging & capture (Redondo & Morris, 2011)
    - Weight bounds with soft saturation
    """

    def __init__(
        self,
        pre_id: Union[int, Tuple[int, int]],
        post_id: Union[int, Tuple[int, int]],
        weight: float = 0.5,
        is_inhibitory: bool = False,
    ):
        self.pre_id = pre_id
        self.post_id = post_id
        self.is_inhibitory = is_inhibitory

        # Weight
        self.weight = float(np.clip(weight, CFG.stdp_w_min, CFG.stdp_w_max))
        if is_inhibitory:
            self.weight = -abs(self.weight)

        # STDP eligibility traces
        self.pre_trace = 0.0
        self.post_trace = 0.0

        # Synaptic tag (eligibility for consolidation)
        self.tag = 0.0
        self.tag_decay = 0.98
        self.tag_created_at = 0.0

        # Weight change accumulator (for dopamine-modulated learning)
        self.dw_accumulator = 0.0

        # Statistics
        self.total_updates = 0
        self.ltp_count = 0
        self.ltd_count = 0

    def update_traces(self, dt_ms: float, pre_spiked: bool, post_spiked: bool) -> None:
        """Update STDP eligibility traces."""
        # Decay traces
        decay_pre = math.exp(-dt_ms / CFG.stdp_tau_plus)
        decay_post = math.exp(-dt_ms / CFG.stdp_tau_minus)

        self.pre_trace *= decay_pre
        self.post_trace *= decay_post

        # Increment traces on spike
        if pre_spiked:
            self.pre_trace += 1.0
        if post_spiked:
            self.post_trace += 1.0

    def compute_weight_change(
        self,
        pre_spiked: bool,
        post_spiked: bool,
        plasticity_factor: float = 1.0,
    ) -> float:
        """
        Compute weight change based on STDP rule.
        Returns the weight change (before dopamine modulation).
        """
        if not CFG.stdp_enabled:
            return 0.0

        dw = 0.0

        # LTD: pre spike when post trace is present
        if pre_spiked and self.post_trace > 0:
            dw_ltd = -CFG.stdp_A_minus * self.post_trace
            dw += dw_ltd
            self.ltd_count += 1
            # Create tag
            self.tag = abs(dw_ltd)
            self.tag_created_at = time.time()

        # LTP: post spike when pre trace is present
        if post_spiked and self.pre_trace > 0:
            dw_ltp = CFG.stdp_A_plus * self.pre_trace
            dw += dw_ltp
            self.ltp_count += 1
            # Create tag
            self.tag = abs(dw_ltp)
            self.tag_created_at = time.time()

        # Modulate by meta-plasticity factor
        dw *= plasticity_factor

        return float(dw)

    def apply_weight_change(
        self,
        dw: float,
        dopamine: float = 1.0,
        immediate: bool = False,
    ) -> None:
        """
        Apply weight change, potentially modulated by dopamine.

        Args:
            dw: Raw weight change
            dopamine: Dopamine level (0-2, 1=baseline)
            immediate: If True, apply immediately; else accumulate for later
        """
        if not immediate and CFG.dopamine_modulation:
            # Three-factor learning: STDP + dopamine
            self.dw_accumulator += dw
        else:
            # Apply immediately with dopamine modulation
            modulated_dw = dw * dopamine
            self._update_weight(modulated_dw)

    def consolidate_with_reward(self, reward: float) -> None:
        """
        Consolidate tagged synapses with reward signal.
        Implements synaptic tagging & capture mechanism.
        """
        if self.tag < 0.01:
            return

        # Check if tag is still active
        tag_age_hours = (time.time() - self.tag_created_at) / 3600.0
        if tag_age_hours > CFG.synaptic_tagging_duration_hours:
            self.tag = 0.0
            return

        # Consolidate: apply accumulated weight change modulated by reward
        consolidated_dw = self.dw_accumulator * reward * self.tag
        self._update_weight(consolidated_dw)

        # Reset accumulator and decay tag
        self.dw_accumulator = 0.0
        self.tag *= self.tag_decay

    def _update_weight(self, dw: float) -> None:
        """Apply weight change with soft bounds."""
        self.weight += dw

        # Soft saturation near boundaries
        if self.is_inhibitory:
            w_min = -CFG.stdp_w_max
            w_max = 0.0
        else:
            w_min = CFG.stdp_w_min
            w_max = CFG.stdp_w_max

        # Soft clipping
        if self.weight > w_max:
            excess = self.weight - w_max
            self.weight = w_max + 0.1 * np.tanh(excess)
        elif self.weight < w_min:
            deficit = w_min - self.weight
            self.weight = w_min - 0.1 * np.tanh(deficit)

        self.weight = float(self.weight)
        self.total_updates += 1

    def get_efficacy(self) -> float:
        """Get effective synaptic strength."""
        return abs(self.weight)


# ══════════════════════════════════════════════════════════════════════════════
# CORTICAL COLUMN ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════════

class CorticalColumn:
    """
    Cortical column with hierarchical organization.
    Contains excitatory and inhibitory neurons with realistic connectivity.
    """

    def __init__(self, column_id: int, num_neurons: int = CFG.neurons_per_column):
        self.column_id = column_id
        self.num_neurons = num_neurons

        # Create neurons
        num_excitatory = int(num_neurons * CFG.excitatory_ratio)
        self.neurons: List[AdaptiveSpikingNeuron] = []

        for i in range(num_neurons):
            neuron_type = "excitatory" if i < num_excitatory else "inhibitory"
            target_rate = 5.0 if neuron_type == "excitatory" else 15.0
            self.neurons.append(AdaptiveSpikingNeuron(i, neuron_type, target_rate))

        # Local connectivity within column
        self.local_synapses: List[STDPSynapse] = []
        self._build_local_connectivity()

        # Column-level statistics
        self.population_rate = 0.0
        self.synchrony_index = 0.0
        self.avalanche_sizes: Deque[int] = deque(maxlen=1000)

        get_log().log(f"Column {column_id} created: {num_neurons} neurons")

    def _build_local_connectivity(self) -> None:
        """Build local recurrent connectivity."""
        num_exc = int(self.num_neurons * CFG.excitatory_ratio)

        for post_idx in range(self.num_neurons):
            post_is_exc = post_idx < num_exc

            # Connection probability depends on cell types
            for pre_idx in range(self.num_neurons):
                if pre_idx == post_idx:
                    continue

                pre_is_exc = pre_idx < num_exc

                # Dale's law: neurons are either excitatory or inhibitory
                if pre_is_exc:
                    # E->E: sparse (10%)
                    # E->I: dense (40%)
                    prob = 0.1 if post_is_exc else 0.4
                    weight = 0.5
                else:
                    # I->E: moderate (30%)
                    # I->I: sparse (20%)
                    prob = 0.3 if post_is_exc else 0.2
                    weight = 0.8

                if random.random() < prob:
                    is_inhibitory = not pre_is_exc
                    syn = STDPSynapse(pre_idx, post_idx, weight, is_inhibitory)
                    self.local_synapses.append(syn)

    def step(
        self,
        dt_ms: float,
        t_ms: float,
        external_input: Optional[FloatArray] = None,
    ) -> FloatArray:
        """
        Run one simulation step.
        Returns: spike vector (1 if neuron fired, 0 otherwise)
        """
        spikes = np.zeros(self.num_neurons, dtype=bool)

        # Set external input
        if external_input is not None:
            for i, inp in enumerate(external_input):
                if i < len(self.neurons):
                    self.neurons[i].set_external_input(float(inp))

        # Propagate spikes through local synapses
        for syn in self.local_synapses:
            if isinstance(syn.pre_id, tuple):
                # This type of synapse is used for inter-column, skip here
                continue
            if spikes[syn.pre_id]:
                self.neurons[syn.post_id].receive_synaptic_input(syn.weight)

        # Integrate all neurons
        for i, neuron in enumerate(self.neurons):
            fired = neuron.step(dt_ms, t_ms)
            spikes[i] = fired

        # Update population statistics
        spike_count = int(np.sum(spikes))
        self.population_rate = spike_count / (self.num_neurons * dt_ms / 1000.0)

        # Track avalanche sizes (for criticality)
        if spike_count > 0:
            self.avalanche_sizes.append(spike_count)

        # Update STDP traces for all synapses
        for syn in self.local_synapses:
            if isinstance(syn.pre_id, tuple):
                continue
            pre_spiked = bool(spikes[syn.pre_id])
            post_spiked = bool(spikes[syn.post_id])
            syn.update_traces(dt_ms, pre_spiked, post_spiked)

        return spikes

    def update_plasticity(self, dopamine: float = 1.0) -> None:
        """Update synaptic weights based on recent activity."""
        for syn in self.local_synapses:
            # Get plasticity factor from postsynaptic neuron
            if isinstance(syn.post_id, tuple):
                continue
            post_neuron = self.neurons[syn.post_id]
            plasticity_factor = post_neuron.plasticity_factor

            syn.consolidate_with_reward(dopamine)

    def homeostatic_update(self, dt_ms: float) -> None:
        """Apply homeostatic plasticity to all neurons."""
        for neuron in self.neurons:
            neuron.homeostatic_update(dt_ms)
            neuron.metaplasticity_update()

    def get_activity_vector(self) -> FloatArray:
        """Get current activity state (firing rates)."""
        rates = np.array([n.get_firing_rate() for n in self.neurons], dtype=np.float32)
        return rates

    def compute_synchrony(self, spike_vector: FloatArray) -> float:
        """Compute population synchrony index."""
        if np.sum(spike_vector) == 0:
            return 0.0
        spike_indices = np.where(spike_vector > 0)[0]
        if len(spike_indices) < 2:
            return 0.0
        synchrony = 1.0 / (1.0 + np.var(spike_indices))
        return float(synchrony)


# ══════════════════════════════════════════════════════════════════════════════
# HIERARCHICAL PREDICTIVE CODING
# ══════════════════════════════════════════════════════════════════════════════

class PredictiveCodingLayer:
    """
    Single layer in hierarchical predictive coding network.
    Implements precision-weighted prediction error minimization.
    """

    def __init__(self, layer_id: int, dim: int, tau_ms: float, upper_dim: int | None = None):
        self.layer_id = layer_id
        self.dim = dim
        self.upper_dim = upper_dim if upper_dim is not None else dim
        self.tau_ms = tau_ms  # Temporal integration constant

        # State variables
        self.representation = np.zeros(dim, dtype=np.float32)
        self.prediction = np.zeros(dim, dtype=np.float32)
        self.error = np.zeros(dim, dtype=np.float32)
        self._last_top_down: FloatArray = np.zeros(self.upper_dim, dtype=np.float32)

        # Precision (inverse variance)
        self.precision = np.ones(dim, dtype=np.float32)

        # Generative weights (top-down): maps upper_dim → dim
        self.W_generative = np.random.randn(dim, self.upper_dim).astype(np.float32) * 0.02

        # Recognition weights (bottom-up)
        self.W_recognition = np.random.randn(dim, dim).astype(np.float32) * 0.02

        # Learning rates
        self.lr_representation = CFG.belief_update_rate
        self.lr_precision = CFG.precision_learning_rate

        # History
        self.error_history: Deque[float] = deque(maxlen=1000)
        self.free_energy_history: Deque[float] = deque(maxlen=1000)

    def forward(
        self,
        bottom_up: FloatArray,
        top_down: FloatArray,
        dt_ms: float,
    ) -> Tuple[FloatArray, float]:
        """
        Compute prediction error and update representation.

        Returns:
            - Precision-weighted error (to pass upward)
            - Local free energy
        """
        # Generate prediction from top-down
        self._last_top_down = top_down
        self.prediction = np.tanh(self.W_generative @ top_down)

        # Compute raw error
        self.error = bottom_up - self.prediction

        # Precision-weighted error
        weighted_error = self.precision * self.error

        # Free energy (simplified): F = 0.5 * error^T * Precision * error
        free_energy = 0.5 * float(np.sum(weighted_error * self.error))
        self.free_energy_history.append(free_energy)

        # Update representation (gradient descent on free energy)
        alpha = dt_ms / self.tau_ms
        error_gradient = self.W_recognition.T @ weighted_error
        self.representation += alpha * self.lr_representation * error_gradient

        # Adapt precision based on error statistics
        error_variance = float(np.var(self.error) + 1e-6)
        target_precision = 1.0 / error_variance
        self.precision += self.lr_precision * (target_precision - self.precision)
        self.precision = np.clip(self.precision, 0.1, 10.0)

        # Store error statistics
        self.error_history.append(float(np.mean(np.abs(self.error))))

        return weighted_error, free_energy

    def update_weights(self, error_from_above: FloatArray) -> None:
        """Update generative model weights (Hebbian-like)."""
        top_down_norm = np.linalg.norm(self._last_top_down) + 1e-6
        normalized_td = self._last_top_down / top_down_norm

        dW = self.lr_representation * np.outer(self.error, normalized_td)
        self.W_generative += dW

        # Weight decay for stability
        self.W_generative *= 0.9999

    def get_surprise(self) -> float:
        """Get current surprise (prediction error magnitude)."""
        if not self.error_history:
            return 0.0
        return float(np.mean(list(self.error_history)[-10:]))


class HierarchicalPredictiveCoding:
    """
    Multi-layer hierarchical predictive coding network.
    Implements active inference for perception and action.
    """

    def __init__(self, layer_dims: List[int]):
        self.num_layers = len(layer_dims)
        self.layer_dims = layer_dims

        # Create layers with increasing temporal constants
        self.layers: List[PredictiveCodingLayer] = []
        for i, dim in enumerate(layer_dims):
            tau_ms = (
                CFG.hierarchical_tau_ms[i]
                if i < len(CFG.hierarchical_tau_ms)
                else 1000.0
            )
            upper_dim = layer_dims[i + 1] if i + 1 < len(layer_dims) else dim
            self.layers.append(PredictiveCodingLayer(i, dim, tau_ms, upper_dim))

        # Total free energy
        self.total_free_energy = 0.0

        get_log().log(f"Hierarchical PC: {self.num_layers} layers, dims={layer_dims}")

    def infer(
        self,
        sensory_input: FloatArray,
        n_iterations: int = 5,
        dt_ms: float = 10.0,
    ) -> Dict[str, Any]:
        """
        Iterative inference to minimize prediction error.
        """
        # Initialize bottom layer
        bottom_input = np.asarray(sensory_input, dtype=np.float32)
        if len(bottom_input) > self.layers[0].dim:
            bottom_input = bottom_input[: self.layers[0].dim]
        elif len(bottom_input) < self.layers[0].dim:
            padded = np.zeros(self.layers[0].dim, dtype=np.float32)
            padded[: len(bottom_input)] = bottom_input
            bottom_input = padded

        self.layers[0].representation = bottom_input

        free_energy_trajectory: List[float] = []

        # Iterative inference
        for _ in range(n_iterations):
            total_fe = 0.0

            # Forward pass: compute errors
            errors: List[FloatArray] = []

            for layer_idx in range(self.num_layers - 1):
                current_layer = self.layers[layer_idx]
                next_layer = self.layers[layer_idx + 1]

                bottom_up = current_layer.representation
                top_down = next_layer.representation

                weighted_error, fe = current_layer.forward(
                    bottom_up, top_down, dt_ms
                )
                errors.append(weighted_error)
                total_fe += fe

            # Backward pass: update weights
            for layer_idx in range(self.num_layers - 2, -1, -1):
                if layer_idx < len(errors):
                    error_from_above = errors[layer_idx]
                    self.layers[layer_idx].update_weights(error_from_above)

            free_energy_trajectory.append(total_fe)

        self.total_free_energy = free_energy_trajectory[-1] if free_energy_trajectory else 0.0

        return {
            "free_energy": self.total_free_energy,
            "trajectory": free_energy_trajectory,
            "top_level_representation": self.layers[-1].representation.copy(),
            "surprise": self.get_total_surprise(),
        }

    def get_total_surprise(self) -> float:
        """Get surprise summed across hierarchy."""
        return sum(layer.get_surprise() for layer in self.layers)

    def imagine(self, top_level_state: FloatArray) -> FloatArray:
        """
        Generate sensory prediction from high-level state.
        (Top-down generative pass)
        """
        # Set top level
        self.layers[-1].representation = np.asarray(
            top_level_state, dtype=np.float32
        )

        # Generate downward
        for layer_idx in range(self.num_layers - 2, -1, -1):
            current_layer = self.layers[layer_idx]
            layer_above = self.layers[layer_idx + 1]

            prediction = np.tanh(current_layer.W_generative @ layer_above.representation)
            current_layer.representation = prediction

        return self.layers[0].representation.copy()


# ══════════════════════════════════════════════════════════════════════════════
# MEMORY SYSTEMS WITH CONSOLIDATION
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class MemoryTrace:
    """Unified memory representation with rich metadata."""

    trace_id: str
    content: Any
    embedding: FloatArray
    timestamp: float

    # Memory type
    memory_type: str  # "episodic", "semantic", "procedural"

    # Importance & emotion
    importance: float
    valence: float  # -1 (negative) to +1 (positive)
    arousal: float  # 0 (calm) to 1 (excited)

    # Consolidation
    consolidation_score: float = 0.0
    replay_count: int = 0

    # TD-error (for prioritized replay)
    td_error: float = 0.0

    # Access statistics
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)

    # Tags & context
    tags: Set[str] = field(default_factory=set)
    context: Dict[str, Any] = field(default_factory=dict)


class HippocampalSystem:
    """
    Hippocampal memory system with:
    - Rapid encoding
    - Pattern separation & completion
    - Replay (awake & sleep)
    - Consolidation to cortex
    """

    def __init__(self, capacity: int = CFG.episodic_capacity):
        self.capacity = capacity
        self.traces: Dict[str, MemoryTrace] = {}

        # Replay statistics
        self.awake_replay_count = 0
        self.sleep_replay_count = 0
        self.replay_history: Deque[Dict[str, Any]] = deque(maxlen=10000)

        get_log().log(f"Hippocampal system initialized: capacity={capacity}")

    def encode(
        self,
        content: Any,
        embedding: FloatArray,
        importance: float,
        valence: float = 0.0,
        arousal: float = 0.5,
        td_error: float = 0.0,
        tags: Optional[Set[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Encode new episodic memory."""
        trace_id = f"epi_{uuid.uuid4().hex[:16]}"

        # Normalize embedding
        embedding = np.asarray(embedding, dtype=np.float32)
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        trace = MemoryTrace(
            trace_id=trace_id,
            content=content,
            embedding=embedding,
            timestamp=time.time(),
            memory_type="episodic",
            importance=float(np.clip(importance, 0.0, 1.0)),
            valence=float(np.clip(valence, -1.0, 1.0)),
            arousal=float(np.clip(arousal, 0.0, 1.0)),
            td_error=float(td_error),
            tags=tags or set(),
            context=context or {},
        )

        self.traces[trace_id] = trace

        # Capacity management
        if len(self.traces) > self.capacity:
            self._evict_weakest()

        return trace_id

    def retrieve(
        self,
        query_embedding: FloatArray,
        k: int = 5,
        min_similarity: float = 0.3,
    ) -> List[Tuple[MemoryTrace, float]]:
        """
        Pattern completion retrieval.
        Returns top-k most similar memories.
        """
        if not self.traces:
            return []

        query = np.asarray(query_embedding, dtype=np.float32)
        query_norm = np.linalg.norm(query)
        if query_norm > 0:
            query = query / query_norm

        candidates: List[Tuple[float, MemoryTrace]] = []
        current_time = time.time()

        for trace in self.traces.values():
            # Cosine similarity
            similarity = float(np.dot(query, trace.embedding))

            if similarity < min_similarity:
                continue

            # Recency bonus (exponential decay with 24h half-life)
            age_hours = (current_time - trace.timestamp) / 3600.0
            recency = math.exp(-age_hours / 24.0)

            # Emotional enhancement (arousal increases memorability)
            emotional_boost = 1.0 + 0.3 * trace.arousal

            # Combined score
            score = (
                0.5 * similarity * emotional_boost
                + 0.3 * trace.importance
                + 0.2 * recency
            )

            candidates.append((score, trace))

        # Sort by score
        candidates.sort(key=lambda x: x[0], reverse=True)

        # Update access statistics
        results: List[Tuple[MemoryTrace, float]] = []
        for score, trace in candidates[:k]:
            trace.access_count += 1
            trace.last_accessed = current_time
            results.append((trace, score))

        return results

    def replay_sequence(
        self,
        prioritized: bool = True,
        batch_size: int = CFG.replay_sequence_length,
    ) -> List[MemoryTrace]:
        """
        Sample memories for replay.
        If prioritized, sample based on TD-error and importance.
        """
        if not self.traces:
            return []

        traces = list(self.traces.values())

        if prioritized and CFG.prioritized_replay:
            priorities = np.array(
                [
                    CFG.td_error_priority_weight * abs(t.td_error)
                    + (1 - CFG.td_error_priority_weight) * t.importance
                    for t in traces
                ],
                dtype=np.float32,
            )

            priorities += 0.01
            priorities = priorities / np.sum(priorities)

            sample_size = min(batch_size, len(traces))
            indices = np.random.choice(
                len(traces), size=sample_size, replace=False, p=priorities
            )
            sampled = [traces[i] for i in indices]
        else:
            sample_size = min(batch_size, len(traces))
            sampled = random.sample(traces, sample_size)

        for trace in sampled:
            trace.replay_count += 1

        self.replay_history.append(
            {
                "timestamp": time.time(),
                "batch_size": len(sampled),
                "prioritized": prioritized,
            }
        )

        return sampled

    def consolidate_batch(self) -> List[str]:
        """Identify memories ready for consolidation."""
        consolidated_ids: List[str] = []

        for trace_id, trace in list(self.traces.items()):
            if trace.replay_count >= 3 or trace.importance > 0.8:
                trace.consolidation_score += CFG.consolidation_strength

            if trace.consolidation_score >= CFG.consolidation_threshold:
                consolidated_ids.append(trace_id)

        return consolidated_ids

    def _evict_weakest(self) -> None:
        """Evict least important memories when at capacity."""
        if not self.traces:
            return

        scores: List[Tuple[float, str]] = []
        current_time = time.time()

        for trace_id, trace in self.traces.items():
            age_hours = (current_time - trace.timestamp) / 3600.0
            recency = math.exp(-age_hours / 48.0)

            keep_score = (
                0.4 * trace.importance
                + 0.2 * recency
                + 0.2 * min(1.0, trace.replay_count / 10.0)
                + 0.2 * trace.consolidation_score
            )

            scores.append((keep_score, trace_id))

        scores.sort()
        num_remove = max(1, int(0.1 * len(scores)))

        for _, trace_id in scores[:num_remove]:
            self.traces.pop(trace_id, None)

    def save_to_db(self, db: sqlite3.Connection) -> int:
        """Persist all episodic memories to database. Returns count saved."""
        count = 0
        for trace in self.traces.values():
            try:
                db.execute(
                    """INSERT OR REPLACE INTO episodic_memories
                       (trace_id, content, embedding, timestamp, importance, valence,
                        arousal, td_error, consolidation_score, replay_count,
                        access_count, last_accessed, tags, context)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        trace.trace_id,
                        str(trace.content)[:2000],
                        trace.embedding.tobytes(),
                        trace.timestamp,
                        trace.importance,
                        trace.valence,
                        trace.arousal,
                        trace.td_error,
                        trace.consolidation_score,
                        trace.replay_count,
                        trace.access_count,
                        trace.last_accessed,
                        json.dumps(list(trace.tags)),
                        json.dumps(trace.context, default=str),
                    ),
                )
                count += 1
            except Exception:
                pass
        db.commit()
        return count

    def load_from_db(self, db: sqlite3.Connection, dim: int = CFG.state_dim) -> int:
        """Load episodic memories from database. Returns count loaded."""
        count = 0
        try:
            rows = db.execute(
                """SELECT trace_id, content, embedding, timestamp, importance,
                          valence, arousal, td_error, consolidation_score,
                          replay_count, access_count, last_accessed, tags, context
                   FROM episodic_memories
                   ORDER BY importance DESC, timestamp DESC
                   LIMIT ?""",
                (self.capacity,)
            ).fetchall()

            for row in rows:
                (trace_id, content, emb_bytes, ts, importance,
                 valence, arousal, td_error, consol_score,
                 replay_count, access_count, last_accessed, tags_json, ctx_json) = row

                embedding = np.frombuffer(emb_bytes, dtype=np.float32).copy()
                if len(embedding) != dim:
                    continue

                tags = set(json.loads(tags_json)) if tags_json else set()
                context = json.loads(ctx_json) if ctx_json else {}

                trace = MemoryTrace(
                    trace_id=trace_id,
                    content=content,
                    embedding=embedding,
                    timestamp=ts,
                    memory_type="episodic",
                    importance=importance,
                    valence=valence,
                    arousal=arousal,
                    td_error=td_error,
                    consolidation_score=consol_score,
                    replay_count=replay_count,
                    access_count=access_count,
                    last_accessed=last_accessed,
                    tags=tags,
                    context=context,
                )
                self.traces[trace_id] = trace
                count += 1
        except Exception:
            pass
        return count


class SemanticMemory:
    """Long-term semantic memory with schema extraction."""

    def __init__(self, capacity: int = CFG.semantic_capacity):
        self.capacity = capacity
        self.concepts: Dict[str, MemoryTrace] = {}
        self.schemas: Dict[str, Dict[str, Any]] = {}

        get_log().log(f"Semantic memory initialized: capacity={capacity}")

    def integrate_from_hippocampus(self, trace: MemoryTrace) -> bool:
        """Integrate consolidated hippocampal memory into semantic store."""
        semantic_key = self._extract_semantic_key(trace.content)

        if semantic_key in self.concepts:
            existing = self.concepts[semantic_key]
            alpha = 0.1
            existing.embedding = (
                1 - alpha
            ) * existing.embedding + alpha * trace.embedding
            existing.access_count += 1
            return True
        else:
            semantic_trace = MemoryTrace(
                trace_id=f"sem_{uuid.uuid4().hex[:16]}",
                content=trace.content,
                embedding=trace.embedding.copy(),
                timestamp=time.time(),
                memory_type="semantic",
                importance=trace.importance,
                valence=trace.valence,
                arousal=0.0,
            )
            self.concepts[semantic_key] = semantic_trace

            if len(self.concepts) > self.capacity:
                self._evict_least_accessed()

            return True

    def _extract_semantic_key(self, content: Any) -> str:
        """Extract semantic category from content."""
        if isinstance(content, str):
            words = content.lower().split()
            meaningful = [w for w in words if len(w) > 3][:3]
            return "_".join(meaningful) if meaningful else "general"
        return str(hash(str(content)))[:16]

    def _evict_least_accessed(self) -> None:
        """Evict least accessed concepts."""
        if not self.concepts:
            return

        sorted_concepts = sorted(
            self.concepts.items(), key=lambda x: x[1].access_count
        )

        num_remove = max(1, int(0.05 * len(sorted_concepts)))
        for key, _ in sorted_concepts[:num_remove]:
            self.concepts.pop(key, None)

    def retrieve(
        self,
        query_embedding: FloatArray,
        k: int = 3,
        min_similarity: float = 0.25,
    ) -> List[Tuple[MemoryTrace, float]]:
        """Retrieve semantically similar concepts."""
        if not self.concepts:
            return []

        query = np.asarray(query_embedding, dtype=np.float32)
        norm = np.linalg.norm(query)
        if norm > 0:
            query = query / norm

        results: List[Tuple[float, MemoryTrace]] = []
        for trace in self.concepts.values():
            sim = float(np.dot(query, trace.embedding))
            if sim >= min_similarity:
                score = 0.6 * sim + 0.4 * trace.importance
                results.append((score, trace))

        results.sort(key=lambda x: x[0], reverse=True)
        out = []
        for score, trace in results[:k]:
            trace.access_count += 1
            out.append((trace, score))
        return out

    def save_to_db(self, db: sqlite3.Connection) -> int:
        """Persist semantic concepts to database."""
        count = 0
        for key, trace in self.concepts.items():
            try:
                db.execute(
                    """INSERT OR REPLACE INTO semantic_concepts
                       (concept_key, content, embedding, timestamp, importance, access_count)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (key, str(trace.content)[:2000], trace.embedding.tobytes(),
                     trace.timestamp, trace.importance, trace.access_count),
                )
                count += 1
            except Exception:
                pass
        db.commit()
        return count

    def load_from_db(self, db: sqlite3.Connection, dim: int = CFG.state_dim) -> int:
        """Load semantic concepts from database."""
        count = 0
        try:
            rows = db.execute(
                """SELECT concept_key, content, embedding, timestamp, importance, access_count
                   FROM semantic_concepts"""
            ).fetchall()
            for key, content, emb_bytes, ts, importance, access_count in rows:
                embedding = np.frombuffer(emb_bytes, dtype=np.float32).copy()
                if len(embedding) != dim:
                    continue
                trace = MemoryTrace(
                    trace_id=f"sem_{key}",
                    content=content,
                    embedding=embedding,
                    timestamp=ts,
                    memory_type="semantic",
                    importance=importance,
                    valence=0.0,
                    arousal=0.0,
                    access_count=access_count,
                )
                self.concepts[key] = trace
                count += 1
        except Exception:
            pass
        return count


class WorkingMemory:
    """
    Working memory with limited capacity (Miller's 7±2).
    Active maintenance with decay.
    """

    def __init__(self, capacity: int = CFG.working_memory_capacity):
        self.capacity = capacity
        self.slots: List[Dict[str, Any]] = []

        get_log().log(f"Working memory initialized: capacity={capacity}")

    def add(self, content: Any, activation: float = 1.0) -> None:
        """Add item to working memory."""
        for slot in self.slots:
            if slot["content"] == content:
                slot["activation"] = min(1.0, slot["activation"] + 0.2)
                slot["timestamp"] = time.time()
                return

        if len(self.slots) < self.capacity:
            self.slots.append(
                {
                    "content": content,
                    "activation": float(activation),
                    "timestamp": time.time(),
                }
            )
        else:
            self.slots.sort(key=lambda x: x["activation"])
            self.slots[0] = {
                "content": content,
                "activation": float(activation),
                "timestamp": time.time(),
            }

    def decay(self, decay_rate: float = 0.95) -> None:
        """Apply temporal decay to activations."""
        for slot in self.slots:
            slot["activation"] *= decay_rate

        self.slots = [s for s in self.slots if s["activation"] > 0.1]

    def get_contents(self) -> List[Any]:
        """Get current working memory contents."""
        return [slot["content"] for slot in self.slots]


class UserProfile:
    """
    Persistent user profile — remembers name, age, preferences, family, hobbies, etc.
    Stored in SQLite so it survives across sessions.
    """

    # Known profile categories and extraction patterns
    CATEGORIES = {
        "name": ["tên", "name", "gọi là", "call me", "i'm", "i am", "tôi là", "em là", "mình là", "anh là"],
        "age": ["tuổi", "age", "years old", "sinh năm", "born in"],
        "occupation": ["nghề", "job", "work", "làm việc", "occupation", "công việc", "developer", "engineer"],
        "location": ["ở", "sống", "live in", "from", "quê", "thành phố", "city"],
        "family": ["gia đình", "family", "vợ", "chồng", "con", "bố", "mẹ", "wife", "husband", "children",
                    "brother", "sister", "anh", "chị", "em trai", "em gái", "bé"],
        "hobbies": ["sở thích", "hobby", "thích", "like", "enjoy", "yêu thích", "đam mê", "passion",
                     "chơi", "play", "game", "music", "nhạc", "phim", "movie", "đọc", "read"],
        "preferences": ["thích", "prefer", "muốn", "want", "ghét", "hate", "don't like", "không thích",
                         "favorite", "yêu thích"],
        "social": ["bạn bè", "friends", "mạng xã hội", "social", "group", "nhóm", "cộng đồng", "community"],
        "education": ["học", "study", "trường", "school", "university", "đại học", "bằng", "degree"],
        "goals": ["mục tiêu", "goal", "muốn", "dream", "ước mơ", "plan", "kế hoạch", "dự định"],
    }

    # Vietnamese pronoun patterns for detecting how the user refers to themselves
    # This determines how AXIOM should address the user back
    PRONOUN_PATTERNS = {
        # User calls themselves "anh" → AXIOM = "em", User = "anh"
        "anh": {"self": "em", "user": "anh", "greeting": "anh"},
        # User calls themselves "chị" → AXIOM = "em", User = "chị"
        "chị": {"self": "em", "user": "chị", "greeting": "chị"},
        # User calls themselves "tôi" → AXIOM = "tôi", User = "bạn"
        "tôi": {"self": "tôi", "user": "bạn", "greeting": "bạn"},
        # User calls themselves "mình" → AXIOM = "mình"/"tớ", User = "cậu"/"bạn"
        "mình": {"self": "mình", "user": "bạn", "greeting": "bạn"},
        # User calls themselves "em" → AXIOM = "anh"/"chị" (default "mình"), User = "em"/"bạn"
        "em": {"self": "mình", "user": "bạn", "greeting": "bạn"},
        # User calls AXIOM "em" → user is older, AXIOM = "em", User = "anh/chị"
        "_called_em": {"self": "em", "user": "anh/chị", "greeting": "anh/chị"},
    }

    # Default pronoun set
    DEFAULT_PRONOUNS = {"self": "mình", "user": "bạn", "greeting": "bạn"}

    def __init__(self, db: sqlite3.Connection):
        self.db = db
        self.cache: Dict[str, Dict[str, Any]] = {}
        self._load_from_db()

    def _load_from_db(self) -> None:
        """Load all profile data from DB into cache."""
        try:
            rows = self.db.execute(
                "SELECT key, value, confidence, source, first_learned, last_updated FROM user_profile"
            ).fetchall()
            for key, value, confidence, source, first_learned, last_updated in rows:
                self.cache[key] = {
                    "value": value,
                    "confidence": confidence,
                    "source": source,
                    "first_learned": first_learned,
                    "last_updated": last_updated,
                }
        except Exception:
            pass

    def learn(self, key: str, value: str, confidence: float = 0.7, source: str = "conversation") -> None:
        """Learn or update a fact about the user."""
        now = time.time()
        existing = self.cache.get(key)
        if existing:
            # Update if new info has higher confidence or is more recent
            self.db.execute(
                """UPDATE user_profile SET value=?, confidence=?, source=?, last_updated=? WHERE key=?""",
                (value, confidence, source, now, key),
            )
            self.cache[key]["value"] = value
            self.cache[key]["confidence"] = confidence
            self.cache[key]["last_updated"] = now
        else:
            self.db.execute(
                """INSERT INTO user_profile (key, value, confidence, source, first_learned, last_updated)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (key, value, confidence, source, now, now),
            )
            self.cache[key] = {
                "value": value, "confidence": confidence,
                "source": source, "first_learned": now, "last_updated": now,
            }
        self.db.commit()

    def get(self, key: str) -> Optional[str]:
        """Get a profile fact."""
        entry = self.cache.get(key)
        return entry["value"] if entry else None

    def get_all(self) -> Dict[str, str]:
        """Get all known user facts."""
        return {k: v["value"] for k, v in self.cache.items()}

    def get_summary(self) -> str:
        """Build a natural language summary of what AXIOM knows about the user."""
        if not self.cache:
            return ""
        lines = []
        for key, entry in self.cache.items():
            lines.append(f"- {key}: {entry['value']}")
        return "Known facts about the user:\n" + "\n".join(lines)

    def detect_pronouns(self, text: str) -> Dict[str, str]:
        """
        Detect Vietnamese pronouns from user message to determine how AXIOM
        should address the user and refer to itself. Returns a dict with
        'self' (how AXIOM calls itself), 'user' (how AXIOM calls the user),
        'greeting' (how AXIOM greets the user).

        Priority: saved preference > current message detection > default.
        """
        # Check if we already have a saved pronoun preference
        saved = self.get("pronoun_style")
        if saved and saved in self.PRONOUN_PATTERNS:
            return self.PRONOUN_PATTERNS[saved]

        # Detect from current message
        text_lower = text.lower().strip()
        words = text_lower.split()

        # Check if user calls AXIOM "em" (e.g. "em ơi", "chào em", "em giúp")
        axiom_names = ["axiom", "em"]
        for i, w in enumerate(words):
            if w == "em":
                # "em" at start or after greeting words likely refers to AXIOM
                if i == 0 or (i > 0 and words[i - 1] in ["chào", "hey", "hi", "ê", "ơi", "này"]):
                    self.learn("pronoun_style", "_called_em", confidence=0.8, source="pronoun_detect")
                    return self.PRONOUN_PATTERNS["_called_em"]
                # "em ơi" pattern
                if i < len(words) - 1 and words[i + 1] == "ơi":
                    self.learn("pronoun_style", "_called_em", confidence=0.8, source="pronoun_detect")
                    return self.PRONOUN_PATTERNS["_called_em"]

        # Check how user refers to themselves
        # Order matters: check more specific patterns first
        self_ref_patterns = [
            ("anh", ["anh là", "anh muốn", "anh cần", "anh hỏi", "anh thấy", "anh nghĩ", "anh đang", "anh có", "anh biết"]),
            ("chị", ["chị là", "chị muốn", "chị cần", "chị hỏi", "chị thấy", "chị nghĩ", "chị đang", "chị có", "chị biết"]),
            ("tôi", ["tôi là", "tôi muốn", "tôi cần", "tôi hỏi", "tôi thấy", "tôi nghĩ", "tôi đang", "tôi có", "tôi biết"]),
            ("mình", ["mình là", "mình muốn", "mình cần", "mình thấy", "mình nghĩ", "mình đang", "mình có", "mình biết"]),
            ("em", ["em là", "em muốn", "em cần", "em hỏi", "em thấy", "em nghĩ", "em đang", "em có", "em biết"]),
        ]

        for pronoun_key, patterns in self_ref_patterns:
            for pat in patterns:
                if pat in text_lower:
                    self.learn("pronoun_style", pronoun_key, confidence=0.7, source="pronoun_detect")
                    return self.PRONOUN_PATTERNS[pronoun_key]

        # Check for single-word clues at sentence boundaries
        if text_lower.startswith("anh ") or " anh " in text_lower:
            # Could be "anh" referring to self — but be careful, could be family reference
            pass

        return self.DEFAULT_PRONOUNS

    def get_pronoun_instruction(self, lang: str) -> str:
        """
        Return a clear pronoun instruction string for the LLM prompt,
        based on detected language and saved user pronoun preference.
        """
        if lang != "vi":
            return (
                "- Speak in first person using 'I'. Address the user as 'you'.\n"
                "- Be consistent — never switch pronouns mid-conversation.\n"
            )

        saved = self.get("pronoun_style")
        if saved and saved in self.PRONOUN_PATTERNS:
            p = self.PRONOUN_PATTERNS[saved]
        else:
            p = self.DEFAULT_PRONOUNS

        return (
            f"- VIETNAMESE PRONOUN RULES (CRITICAL — follow strictly):\n"
            f"  + You (AXIOM) ALWAYS refer to yourself as: '{p['self']}'\n"
            f"  + You ALWAYS address the user as: '{p['user']}'\n"
            f"  + When greeting, say: 'Chào {p['greeting']}' (NOT 'Chào em', NOT 'Chào bạn' unless that matches above)\n"
            f"  + NEVER switch pronouns mid-conversation. NEVER use a pronoun pair that contradicts the above.\n"
            f"  + Examples: '{p['self'].capitalize()} nghĩ rằng...', 'Dạ {p['self']} hiểu rồi {p['user']} ạ', 'Chào {p['greeting']}!'\n"
        )

    def extract_and_learn(self, text: str) -> List[str]:
        """Try to extract user profile information from a message."""
        learned = []
        text_lower = text.lower()

        for category, keywords in self.CATEGORIES.items():
            for kw in keywords:
                if kw in text_lower:
                    # Store the relevant sentence fragment
                    self.learn(
                        f"{category}",
                        text[:300],
                        confidence=0.6,
                        source="auto_extract",
                    )
                    learned.append(category)
                    break  # one match per category per message

        return learned

    def save_to_db(self, db: sqlite3.Connection) -> None:
        """Ensure all profile data is committed."""
        db.commit()


class ConversationHistory:
    """
    Persistent conversation history across sessions.
    Maintains a rolling window for LLM context and full history in DB.
    """

    def __init__(self, db: sqlite3.Connection, session_id: str, max_turns: int = 20):
        self.db = db
        self.session_id = session_id
        self.max_turns = max_turns
        self.turns: Deque[Dict[str, str]] = deque(maxlen=max_turns * 2)
        self._load_recent()

    def _load_recent(self) -> None:
        """Load recent conversation turns from DB (across all sessions)."""
        try:
            rows = self.db.execute(
                """SELECT role, content FROM conversation_history
                   ORDER BY id DESC LIMIT ?""",
                (self.max_turns * 2,)
            ).fetchall()
            # Reverse to get chronological order
            for role, content in reversed(rows):
                self.turns.append({"role": role, "content": content})
        except Exception:
            pass

    def add_turn(self, role: str, content: str) -> None:
        """Add a conversation turn and persist to DB."""
        self.turns.append({"role": role, "content": content})
        self.db.execute(
            """INSERT INTO conversation_history (session_id, role, content, timestamp)
               VALUES (?, ?, ?, ?)""",
            (self.session_id, role, content[:2000], time.time()),
        )
        self.db.commit()

    def get_recent(self, n: int = 10) -> List[Dict[str, str]]:
        """Get last n conversation turns."""
        turns_list = list(self.turns)
        return turns_list[-n * 2:] if len(turns_list) > n * 2 else turns_list

    def format_for_prompt(self, n: int = 6) -> str:
        """Format recent history for LLM prompt."""
        recent = self.get_recent(n)
        if not recent:
            return ""
        lines = ["Recent conversation history:"]
        for turn in recent:
            role = "User" if turn["role"] == "user" else "AXIOM"
            lines.append(f"  {role}: {turn['content'][:300]}")
        return "\n".join(lines)

    def save_to_db(self, db: sqlite3.Connection) -> None:
        """Ensure all conversation data is committed."""
        db.commit()


class WebSearch:
    """
    Web search integration via DDGS (DuckDuckGo + Bing + Brave + Google metasearch).
    Provides text search, news search, and URL content extraction.
    Results are cached in SQLite to avoid redundant queries.
    """

    # Keywords that suggest the user wants a web search
    SEARCH_TRIGGERS_VI = [
        "tìm", "search", "tra cứu", "google", "tin tức", "news", "mới nhất",
        "latest", "hôm nay", "today", "bây giờ", "hiện tại", "current",
        "cập nhật", "update", "thông tin về", "info about", "là gì", "what is",
        "ai là", "who is", "ở đâu", "where is", "khi nào", "when",
        "bao nhiêu", "how much", "how many", "giá", "price",
        "thời tiết", "weather", "tỷ giá", "exchange rate", "kết quả", "result",
        "sự kiện", "event", "xu hướng", "trend", "so sánh", "compare",
        "review", "đánh giá", "wiki", "wikipedia",
    ]

    # Topics likely to need real-time info (LLM knowledge cutoff)
    REALTIME_TOPICS = [
        "giá", "price", "stock", "crypto", "bitcoin", "thời tiết", "weather",
        "tỷ giá", "exchange", "score", "kết quả", "election", "bầu cử",
        "covid", "earthquake", "động đất", "breaking", "nóng",
    ]

    def __init__(self, db: sqlite3.Connection, cache_ttl: int = 3600):
        """
        Args:
            db: SQLite connection for caching search results.
            cache_ttl: Cache time-to-live in seconds (default: 1 hour).
        """
        self.db = db
        self.cache_ttl = cache_ttl
        self._ddgs: Optional[DDGS] = None
        self._init_cache_table()

    def _init_cache_table(self) -> None:
        """Create search cache table if not exists."""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS web_search_cache (
                query_hash TEXT PRIMARY KEY,
                query TEXT,
                search_type TEXT,
                results TEXT,
                timestamp REAL
            )
        """)
        self.db.commit()

    @property
    def ddgs(self) -> DDGS:
        """Lazy-load DDGS instance."""
        if self._ddgs is None:
            self._ddgs = DDGS(timeout=10)
        return self._ddgs

    def should_search(self, text: str) -> bool:
        """
        Determine if a user message warrants a web search.
        Returns True if the message contains search trigger words
        or asks about real-time information.
        """
        text_lower = text.lower()

        # Explicit search request
        for trigger in self.SEARCH_TRIGGERS_VI:
            if trigger in text_lower:
                return True

        # Question patterns that likely need fresh info
        question_patterns = ["?", "là gì", "what is", "who is", "how to", "why",
                             "tại sao", "như thế nào", "bao giờ", "ở đâu"]
        has_question = any(p in text_lower for p in question_patterns)

        # Check if it's about a real-time topic
        has_realtime = any(t in text_lower for t in self.REALTIME_TOPICS)

        return has_question and has_realtime

    def _get_cache(self, query: str, search_type: str) -> Optional[List[Dict]]:
        """Check if we have a cached result that's still fresh."""
        query_hash = hashlib.md5(f"{search_type}:{query}".encode()).hexdigest()
        try:
            row = self.db.execute(
                "SELECT results, timestamp FROM web_search_cache WHERE query_hash = ?",
                (query_hash,)
            ).fetchone()
            if row:
                results_json, ts = row
                if time.time() - ts < self.cache_ttl:
                    return json.loads(results_json)
        except Exception:
            pass
        return None

    def _set_cache(self, query: str, search_type: str, results: List[Dict]) -> None:
        """Cache search results."""
        query_hash = hashlib.md5(f"{search_type}:{query}".encode()).hexdigest()
        try:
            self.db.execute(
                """INSERT OR REPLACE INTO web_search_cache
                   (query_hash, query, search_type, results, timestamp)
                   VALUES (?, ?, ?, ?, ?)""",
                (query_hash, query, search_type, json.dumps(results, ensure_ascii=False),
                 time.time())
            )
            self.db.commit()
        except Exception:
            pass

    def search_text(self, query: str, max_results: int = 5,
                    region: str = "vn-vi", timelimit: Optional[str] = None) -> List[Dict]:
        """
        Perform a text web search.

        Args:
            query: Search query string.
            max_results: Maximum results to return.
            region: Search region (default: Vietnam/Vietnamese).
            timelimit: d=day, w=week, m=month, y=year.

        Returns:
            List of dicts with 'title', 'href', 'body'.
        """
        cached = self._get_cache(query, "text")
        if cached is not None:
            return cached

        try:
            results = self.ddgs.text(
                query=query,
                region=region,
                safesearch="moderate",
                timelimit=timelimit,
                max_results=max_results,
            )
            # Normalize results
            cleaned = []
            for r in (results or []):
                cleaned.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                })
            self._set_cache(query, "text", cleaned)
            return cleaned
        except Exception as e:
            get_log().log(f"⚠️ Web search failed: {e}", level="warning")
            return []

    def search_news(self, query: str, max_results: int = 5,
                    region: str = "vn-vi", timelimit: str = "w") -> List[Dict]:
        """
        Search for recent news articles.

        Args:
            query: News search query.
            max_results: Maximum results.
            region: Search region.
            timelimit: d=day, w=week, m=month.

        Returns:
            List of dicts with 'title', 'url', 'snippet', 'date', 'source'.
        """
        cached = self._get_cache(query, "news")
        if cached is not None:
            return cached

        try:
            results = self.ddgs.news(
                query=query,
                region=region,
                safesearch="moderate",
                timelimit=timelimit,
                max_results=max_results,
            )
            cleaned = []
            for r in (results or []):
                cleaned.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("body", ""),
                    "date": r.get("date", ""),
                    "source": r.get("source", ""),
                })
            self._set_cache(query, "news", cleaned)
            return cleaned
        except Exception as e:
            get_log().log(f"⚠️ News search failed: {e}", level="warning")
            return []

    def extract_url(self, url: str) -> Optional[str]:
        """
        Extract content from a URL as markdown text.

        Args:
            url: The URL to extract content from.

        Returns:
            Extracted text content, or None if failed.
        """
        try:
            result = self.ddgs.extract(url, fmt="text_markdown")
            content = result.get("content", "")
            if isinstance(content, str):
                return content[:5000]  # Limit to keep context manageable
            return None
        except Exception as e:
            get_log().log(f"⚠️ URL extraction failed: {e}", level="warning")
            return None

    def build_search_query(self, user_message: str) -> str:
        """
        Build an effective search query from the user's message.
        Strips filler words and keeps the core question.
        """
        # Remove common Vietnamese filler/command words
        fillers = [
            "tìm giúp", "tìm cho", "search for", "hãy tìm", "giúp tôi tìm",
            "bạn tìm", "em tìm", "anh tìm", "mình tìm", "cho tôi biết",
            "cho anh biết", "cho em biết", "hãy cho", "giúp tôi", "please",
            "can you", "could you", "tôi muốn biết", "tôi muốn tìm",
        ]
        query = user_message.strip()
        query_lower = query.lower()
        for filler in fillers:
            if query_lower.startswith(filler):
                query = query[len(filler):].strip()
                query_lower = query.lower()
        # Remove trailing question marks for better search
        query = query.rstrip("?").strip()
        return query if query else user_message.strip()

    def search_for_message(self, user_message: str) -> Tuple[List[Dict], str]:
        """
        Main entry point: decides whether to search and what type,
        then performs the search.

        Returns:
            (results, search_type) where search_type is 'text', 'news', or 'none'.
        """
        if not self.should_search(user_message):
            return [], "none"

        query = self.build_search_query(user_message)
        text_lower = user_message.lower()

        # Use news search for news/real-time topics
        is_news = any(w in text_lower for w in [
            "tin tức", "news", "mới nhất", "latest", "hôm nay", "today",
            "breaking", "nóng", "sự kiện", "event",
        ])

        if is_news:
            results = self.search_news(query, max_results=5, timelimit="d")
            if results:
                return results, "news"

        # Fall back to text search
        results = self.search_text(query, max_results=5)
        return results, "text"

    def format_results_for_prompt(self, results: List[Dict], search_type: str) -> str:
        """Format search results for inclusion in the LLM prompt."""
        if not results:
            return ""

        lines = [f"WEB SEARCH RESULTS ({search_type.upper()}):"]
        for i, r in enumerate(results[:5], 1):
            title = r.get("title", "No title")
            snippet = r.get("snippet", "")[:300]
            url = r.get("url", "")
            source = r.get("source", "")
            date = r.get("date", "")

            entry = f"  [{i}] {title}"
            if source:
                entry += f" — {source}"
            if date:
                entry += f" ({date})"
            entry += f"\n      {snippet}"
            if url:
                entry += f"\n      URL: {url}"
            lines.append(entry)

        lines.append(
            "\nUse the above search results to provide accurate, up-to-date information. "
            "Cite sources when relevant. If the results don't fully answer the question, "
            "say so and provide what you can from your own knowledge."
        )
        return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# ATTENTION & GLOBAL WORKSPACE (CONSCIOUSNESS)
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class WorkspaceItem:
    """Item competing for global workspace."""

    item_id: str
    content: Any
    activation: float
    source: str
    timestamp: float = field(default_factory=time.time)


class GlobalWorkspace:
    """
    Global Workspace Theory implementation.
    Competition for broadcast creates conscious access.
    """

    def __init__(self):
        self.ignition_threshold = CFG.gw_ignition_threshold
        self.competition_strength = CFG.gw_competition_strength

        # Current workspace contents
        self.workspace: List[WorkspaceItem] = []
        self.broadcast_winner: Optional[WorkspaceItem] = None

        # History
        self.broadcast_history: Deque[str] = deque(maxlen=1000)
        self.ignition_events: List[float] = []

        get_log().log(
            f"Global Workspace initialized: threshold={self.ignition_threshold}"
        )

    def compete(
        self,
        candidates: List[WorkspaceItem],
        n_iterations: int = 10,
    ) -> Optional[WorkspaceItem]:
        """
        Competition dynamics with lateral inhibition.
        Winner-take-all with soft competition.
        """
        if not candidates:
            return None

        # Combine with existing workspace items (decay old)
        for item in self.workspace:
            item.activation *= 0.9

        all_items = self.workspace + candidates

        for _ in range(n_iterations):
            n = len(all_items)
            if n == 0:
                break

            activations = np.array(
                [item.activation for item in all_items], dtype=np.float32
            )

            W = np.eye(n) * 1.5 - np.ones((n, n)) * self.competition_strength * 0.1

            delta = W @ activations - self.ignition_threshold * 0.1
            activations += 0.1 * delta

            activations = np.maximum(activations, 0.0)

            # Noise
            activations += np.random.randn(n).astype(np.float32) * 0.02

            max_val = float(np.max(activations))
            if max_val > 10.0:
                activations = activations / max_val * 5.0

            for i, item in enumerate(all_items):
                item.activation = float(activations[i])

        above_threshold = [
            item for item in all_items if item.activation >= self.ignition_threshold
        ]

        if above_threshold:
            winner = max(above_threshold, key=lambda x: x.activation)
            self.broadcast_winner = winner
            self.broadcast_history.append(winner.item_id)
            self.ignition_events.append(time.time())

            all_items.sort(key=lambda x: x.activation, reverse=True)
            self.workspace = all_items[:5]

            return winner

        all_items.sort(key=lambda x: x.activation, reverse=True)
        self.workspace = all_items[:5]
        self.broadcast_winner = None

        return None

    def is_conscious(self) -> bool:
        """Check if there's content in conscious awareness."""
        return self.broadcast_winner is not None

    def get_conscious_content(self) -> Optional[Any]:
        """Get currently conscious content."""
        if self.broadcast_winner:
            return self.broadcast_winner.content
        return None

    def compute_integration(self) -> float:
        """Compute integration measure (how unified the workspace is)."""
        if len(self.workspace) < 2:
            return 0.0

        activations = np.array([item.activation for item in self.workspace])
        variance = float(np.var(activations))
        integration = 1.0 / (1.0 + variance)

        return integration


class AttentionSystem:
    """
    Multi-head attention mechanism with salience computation.
    """

    def __init__(self, dim: int = CFG.state_dim, num_heads: int = CFG.attention_heads):
        self.dim = dim
        self.num_heads = num_heads
        self.head_dim = dim // num_heads

        # Attention parameters
        self.W_q = np.random.randn(dim, dim).astype(np.float32) * 0.02
        self.W_k = np.random.randn(dim, dim).astype(np.float32) * 0.02
        self.W_v = np.random.randn(dim, dim).astype(np.float32) * 0.02
        self.W_o = np.random.randn(dim, dim).astype(np.float32) * 0.02

        # Salience map
        self.salience_map: Dict[str, float] = {}

        get_log().log(f"Attention: {num_heads} heads, dim={dim}")

    def compute_salience(
        self,
        stimuli: Dict[str, FloatArray],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, float]:
        """
        Compute salience for each stimulus.
        Combines bottom-up (intensity) and top-down (relevance) factors.
        """
        salience: Dict[str, float] = {}
        context = context or {}

        for key, stimulus in stimuli.items():
            stim = np.asarray(stimulus, dtype=np.float32).flatten()

            intensity = float(np.linalg.norm(stim))
            contrast = float(np.std(stim))
            bottom_up = 0.7 * intensity + 0.3 * contrast

            relevance = float(context.get("relevance", {}).get(key, 0.5))

            salience[key] = 0.6 * bottom_up + 0.4 * relevance

        self.salience_map = salience
        return salience

    def attend(
        self,
        query: FloatArray,
        keys: List[FloatArray],
        values: List[FloatArray],
        mask: Optional[FloatArray] = None,
    ) -> Tuple[FloatArray, FloatArray]:
        """
        Multi-head attention mechanism.
        Returns (attended_output, attention_weights).
        """
        query = np.asarray(query, dtype=np.float32).flatten()

        if len(query) < self.dim:
            padded = np.zeros(self.dim, dtype=np.float32)
            padded[: len(query)] = query[:len(query)]
            query = padded
        else:
            query = query[: self.dim]

        Q = query @ self.W_q

        K_list = []
        V_list = []
        for key, value in zip(keys, values):
            k = np.asarray(key, dtype=np.float32).flatten()
            v = np.asarray(value, dtype=np.float32).flatten()

            if len(k) < self.dim:
                k_padded = np.zeros(self.dim, dtype=np.float32)
                k_padded[: len(k)] = k
                k = k_padded
            else:
                k = k[: self.dim]

            if len(v) < self.dim:
                v_padded = np.zeros(self.dim, dtype=np.float32)
                v_padded[: len(v)] = v
                v = v_padded
            else:
                v = v[: self.dim]

            K_list.append(k @ self.W_k)
            V_list.append(v @ self.W_v)

        if not K_list:
            return np.zeros(self.dim, dtype=np.float32), np.array([])

        K = np.stack(K_list)
        V = np.stack(V_list)

        scores = Q @ K.T / np.sqrt(self.head_dim)

        if mask is not None:
            scores = scores + mask

        attention_weights = MathOps.softmax(
            scores.astype(np.float32), temperature=CFG.attention_temperature
        )

        output = attention_weights @ V
        output = output @ self.W_o

        return output.astype(np.float32), attention_weights.astype(np.float32)


# ══════════════════════════════════════════════════════════════════════════════
# INTRINSIC MOTIVATION & CURIOSITY
# ══════════════════════════════════════════════════════════════════════════════

class IntrinsicMotivationSystem:
    """
    Multi-faceted intrinsic motivation:
    - Epistemic curiosity (learning progress)
    - Diversive curiosity (novelty seeking)
    - Competence motivation
    """

    def __init__(self):
        self.epistemic_curiosity = 0.5
        self.diversive_curiosity = 0.5

        self.competence = 0.5
        self.autonomy = 0.5

        self.prediction_error_history: Deque[float] = deque(
            maxlen=CFG.learning_progress_window
        )
        self.learning_progress = 0.0

        self.seen_states: List[FloatArray] = []

        get_log().log("Intrinsic Motivation system initialized")

    def compute_curiosity_reward(
        self,
        prediction_error: float,
        state: FloatArray,
        learning_progress: Optional[float] = None,
    ) -> float:
        """
        Compute intrinsic reward from curiosity.
        """
        epistemic = math.exp(-((prediction_error - 0.5) ** 2) / 0.2)
        novelty = self._compute_novelty(state)

        if learning_progress is None:
            learning_progress = self._update_learning_progress(prediction_error)
        progress_reward = max(0.0, learning_progress)

        total_curiosity = 0.4 * epistemic + 0.3 * novelty + 0.3 * progress_reward

        intrinsic_reward = CFG.curiosity_weight * total_curiosity

        self.epistemic_curiosity = (
            0.9 * self.epistemic_curiosity + 0.1 * epistemic
        )
        self.diversive_curiosity = (
            0.9 * self.diversive_curiosity + 0.1 * novelty
        )

        return float(intrinsic_reward)

    def _compute_novelty(self, state: FloatArray) -> float:
        """Compute novelty by comparing to seen states."""
        if not self.seen_states:
            novelty = 1.0
        else:
            similarities = [
                MathOps.cosine_similarity(state, s)
                for s in self.seen_states[-100:]
            ]
            max_similarity = max(similarities)
            novelty = 1.0 - max_similarity

        self.seen_states.append(state.copy())
        if len(self.seen_states) > 1000:
            self.seen_states = self.seen_states[-1000:]

        return float(np.clip(novelty * CFG.novelty_bonus_scale, 0.0, 1.0))

    def _update_learning_progress(self, current_error: float) -> float:
        """Track learning progress (reduction in prediction error)."""
        self.prediction_error_history.append(current_error)

        if len(self.prediction_error_history) < 20:
            return 0.0

        recent = list(self.prediction_error_history)[-10:]
        older = list(self.prediction_error_history)[-20:-10]

        progress = float(np.mean(older) - np.mean(recent))
        self.learning_progress = progress

        return progress

    def update_competence(self, performance: float) -> None:
        """Update competence based on task performance."""
        self.competence = 0.95 * self.competence + 0.05 * performance
        self.competence = float(np.clip(self.competence, 0.0, 1.0))

    def get_motivation_state(self) -> Dict[str, float]:
        """Get current motivational state."""
        return {
            "epistemic_curiosity": float(self.epistemic_curiosity),
            "diversive_curiosity": float(self.diversive_curiosity),
            "competence": float(self.competence),
            "autonomy": float(self.autonomy),
            "learning_progress": float(self.learning_progress),
            "overall_motivation": float(
                CFG.curiosity_weight
                * (self.epistemic_curiosity + self.diversive_curiosity)
                / 2.0
                + CFG.competence_weight * self.competence
            ),
        }


# ══════════════════════════════════════════════════════════════════════════════
# CREATIVE INSIGHT ENGINE
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class InsightEvent:
    """Record of a creative insight."""

    insight_id: str
    timestamp: float
    problem_state: FloatArray
    solution_state: FloatArray
    conceptual_distance: float
    insight_type: str  # "aha", "analogy", "blend"
    description: str


class CreativeInsightEngine:
    """
    Creative cognition through:
    - Conceptual blending
    - Constraint relaxation
    - Analogical mapping
    - Insight detection
    """

    def __init__(self, llm_router=None):
        self.insights: List[InsightEvent] = []
        self.conceptual_space_dim = CFG.state_dim
        self.llm = llm_router

        get_log().log("Creative Insight Engine initialized")

    async def divergent_thinking(
        self,
        seed_concept_text: str,
        num_ideas: int = 5,
        temperature: float = CFG.divergent_temperature,
    ) -> List[Tuple[FloatArray, float]]:
        """
        Use LLM to brainstorm structurally diverse, divergent ideas branching from seed.
        Returns list of (embedded_concept, novelty_score) tuples.
        """
        if not getattr(self, "llm", None) or not self.llm.is_available():
            seed_emb = await EmbeddingEngine.aembed(seed_concept_text, CFG.state_dim)
            seed_emb = seed_emb / (np.linalg.norm(seed_emb) + 1e-10)
            ideas = []
            for _ in range(num_ideas):
                noise = np.random.randn(len(seed_emb)).astype(np.float32)
                idea = seed_emb + temperature * noise
                idea = idea / (np.linalg.norm(idea) + 1e-10)
                ideas.append((np.asarray(idea, dtype=np.float32), float(1.0 - np.dot(seed_emb, idea))))
            ideas.sort(key=lambda x: x[1], reverse=True)
            return ideas

        prompt = (
            f"Generate exactly {num_ideas} extremely divergent, lateral, and unorthodox ideas "
            f"or interpretations branching from this seed concept: '{seed_concept_text}'.\n\n"
            "Output ONLY a numbered list of the ideas, with no introductory text."
        )

        try:
            response = await self.llm.acomplete(
                system_prompt="You are the divergent thinking creativity module of an AGI system.",
                user_prompt=prompt,
                temperature=min(temperature, 1.5)
            )
            
            if not response:
                return []
                
            ideas = []
            seed_emb = await EmbeddingEngine.aembed(seed_concept_text, CFG.state_dim)
            
            for line in response.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-')):
                    clean_idea = line.split('.', 1)[-1].strip() if '.' in line else line.split('-', 1)[-1].strip()
                    if clean_idea:
                        emb = await EmbeddingEngine.aembed(clean_idea, CFG.state_dim)
                        similarity = float(np.dot(seed_emb, emb))
                        novelty = 1.0 - similarity
                        ideas.append((emb, novelty))
                        
            ideas.sort(key=lambda x: x[1], reverse=True)
            return ideas[:num_ideas]
        except Exception as e:
            get_log().log(f"Divergent thinking generation failed: {e}")
            return []

    def conceptual_blend(
        self,
        concept_a: FloatArray,
        concept_b: FloatArray,
        blend_ratio: float = 0.5,
    ) -> FloatArray:
        """Blend two concepts to create novel combination."""
        a = np.asarray(concept_a, dtype=np.float32).flatten()
        b = np.asarray(concept_b, dtype=np.float32).flatten()

        n = min(len(a), len(b))
        a, b = a[:n], b[:n]

        blended = blend_ratio * a + (1 - blend_ratio) * b
        blended = np.tanh(blended * 1.2)
        blended = blended / (np.linalg.norm(blended) + 1e-10)

        return blended.astype(np.float32)

    def detect_insight(
        self,
        problem_state: FloatArray,
        solution_state: FloatArray,
        cognitive_load: float,
    ) -> Optional[InsightEvent]:
        """Detect insight moments (sudden understanding)."""
        prob = np.asarray(problem_state, dtype=np.float32).flatten()
        sol = np.asarray(solution_state, dtype=np.float32).flatten()

        n = min(len(prob), len(sol))
        distance = float(np.linalg.norm(prob[:n] - sol[:n]))

        is_insight = distance > CFG.insight_detection_threshold and cognitive_load < 0.4

        if is_insight:
            insight = InsightEvent(
                insight_id=f"insight_{uuid.uuid4().hex[:12]}",
                timestamp=time.time(),
                problem_state=prob,
                solution_state=sol,
                conceptual_distance=distance,
                insight_type="aha",
                description=f"Bridged {distance:.3f} conceptual distance",
            )

            self.insights.append(insight)
            get_log().log(f"💡 Insight detected: distance={distance:.3f}", level="info")

            return insight

        return None

    def analogical_reasoning(
        self,
        source: FloatArray,
        target: FloatArray,
    ) -> Tuple[float, FloatArray]:
        """
        Compute analogical mapping between source and target.
        Returns similarity and projected solution.
        """
        src = np.asarray(source, dtype=np.float32).flatten()
        tgt = np.asarray(target, dtype=np.float32).flatten()

        similarity = MathOps.cosine_similarity(src, tgt)

        projection = 0.7 * tgt + 0.3 * src
        projection = projection / (np.linalg.norm(projection) + 1e-10)

        return float(similarity), projection


# ══════════════════════════════════════════════════════════════════════════════
# SELF-MODEL & AUTOBIOGRAPHICAL MEMORY
# ══════════════════════════════════════════════════════════════════════════════

class SelfModel:
    """
    Recursive self-modeling for metacognition and self-awareness.
    Maintains sense of identity and autobiographical narrative.
    """

    def __init__(self):
        self.identity_vector = np.random.randn(256).astype(np.float32)
        self.identity_vector /= np.linalg.norm(self.identity_vector)

        self.traits: Dict[str, float] = {
            "openness": 0.7,
            "conscientiousness": 0.6,
            "extraversion": 0.5,
            "agreeableness": 0.7,
            "neuroticism": 0.4,
            "curiosity": 0.8,
            "creativity": 0.7,
        }

        self.confidence = 0.5
        self.uncertainty = 0.5
        self.self_awareness_level = 0.0

        self.narrative: List[str] = []
        self.significant_events: List[Dict[str, Any]] = []

        self.self_beliefs: List[str] = [
            "I am a learning system",
            "I improve through experience",
            "I can adapt to new situations",
        ]

        self.metacognitive_history: Deque[Dict[str, float]] = deque(maxlen=10000)

        get_log().log("Self-Model initialized")

    def update(
        self,
        experience: Dict[str, Any],
        performance: Dict[str, float],
    ) -> None:
        """Update self-model based on experience and performance."""
        success = performance.get("success", 0.5)
        self.confidence = 0.95 * self.confidence + 0.05 * success

        prediction_error = performance.get("prediction_error", 0.5)
        self.uncertainty = 0.95 * self.uncertainty + 0.05 * prediction_error

        if experience.get("explored_novel", False):
            self.traits["curiosity"] = min(1.0, self.traits["curiosity"] + 0.001)

        if experience.get("creative_solution", False):
            self.traits["creativity"] = min(1.0, self.traits["creativity"] + 0.001)

        if (
            "predicted_performance" in experience
            and "actual_performance" in experience
        ):
            pred = experience["predicted_performance"]
            actual = experience["actual_performance"]
            metacog_accuracy = 1.0 - abs(pred - actual)
            self.self_awareness_level = (
                0.9 * self.self_awareness_level + 0.1 * metacog_accuracy
            )

        if "embedding" in experience:
            emb = np.asarray(experience["embedding"], dtype=np.float32).flatten()
            if len(emb) == len(self.identity_vector):
                self.identity_vector += CFG.self_model_update_rate * emb
                self.identity_vector /= np.linalg.norm(self.identity_vector) + 1e-10

        self.metacognitive_history.append(
            {
                "confidence": self.confidence,
                "uncertainty": self.uncertainty,
                "self_awareness": self.self_awareness_level,
                "timestamp": time.time(),
            }
        )

    def add_to_narrative(self, event: str, importance: float = 0.5) -> None:
        """Add event to autobiographical narrative."""
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        narrative_entry = f"[{timestamp_str}] {event}"

        self.narrative.append(narrative_entry)

        if importance > 0.7:
            self.significant_events.append(
                {
                    "event": event,
                    "timestamp": time.time(),
                    "importance": importance,
                }
            )

        if len(self.narrative) > 1000:
            self.narrative = self.narrative[-1000:]

    def introspect(self) -> Dict[str, Any]:
        """Deep introspection about self."""
        return {
            "traits": self.traits,
            "confidence": float(self.confidence),
            "uncertainty": float(self.uncertainty),
            "self_awareness": float(self.self_awareness_level),
            "identity_stability": float(np.std(self.identity_vector)),
            "narrative_length": len(self.narrative),
            "significant_events": len(self.significant_events),
            "beliefs": self.self_beliefs,
        }


# ══════════════════════════════════════════════════════════════════════════════
# DREAM ENGINE (OFFLINE LEARNING)
# ══════════════════════════════════════════════════════════════════════════════

class DreamEngine:
    """
    Dream-like offline learning for consolidation and creative exploration.
    """

    def __init__(
        self,
        hippocampus: HippocampalSystem,
        semantic_memory: SemanticMemory,
        llm_router = None,
    ):
        self.hippocampus = hippocampus
        self.semantic_memory = semantic_memory
        self.llm = llm_router

        self.dream_log: List[Dict[str, Any]] = []

        get_log().log("Dream Engine initialized")

    async def dream_cycle(
        self,
        duration_minutes: float = CFG.nrem_duration_minutes,
    ) -> Dict[str, Any]:
        """
        Execute dream cycle with NREM-like consolidation.
        """
        if not CFG.dream_enabled:
            return {"status": "disabled"}

        get_log().log(f"💤 Entering dream state ({duration_minutes} min)...")

        start_time = time.time()
        iterations = int(duration_minutes * 60.0 / 0.1)  # 10 Hz

        memories_replayed = 0
        memories_consolidated = 0
        creative_blends = 0

        for _ in range(iterations):
            replay_batch = self.hippocampus.replay_sequence(
                prioritized=True,
                batch_size=CFG.replay_sequence_length,
            )

            if not replay_batch:
                await asyncio.sleep(0.001)
                continue

            for memory in replay_batch:
                memories_replayed += 1

                noisy_embedding = (
                    memory.embedding
                    + np.random.randn(len(memory.embedding)).astype(np.float32)
                    * CFG.dream_replay_temperature
                    * 0.1
                )
                noisy_embedding /= np.linalg.norm(noisy_embedding) + 1e-10

                memory.consolidation_score += CFG.consolidation_strength

            to_consolidate = self.hippocampus.consolidate_batch()
            for trace_id in to_consolidate:
                trace = self.hippocampus.traces.get(trace_id)
                if trace:
                    success = self.semantic_memory.integrate_from_hippocampus(trace)
                    if success:
                        memories_consolidated += 1

            if len(replay_batch) >= 2 and random.random() < 0.05:
                mem1, mem2 = random.sample(replay_batch, 2)
                
                blend_text = f"Dream blend: {str(mem1.content)[:50]} + {str(mem2.content)[:50]}"
                
                if getattr(self, "llm", None) and self.llm.is_available():
                    prompt = (
                        f"Find a profound metaphorical or structural connection between these two memories:\n"
                        f"1) {str(mem1.content)}\n2) {str(mem2.content)}\n\n"
                        "Output ONLY a single short sentence describing the abstract, dream-like synthesis."
                    )
                    try:
                        resp = await self.llm.acomplete("You are the unconscious integration module generating a dream.", prompt, temperature=1.2)
                        if resp:
                            blend_text = f"💭 Dream Insight: {resp.strip()}"
                    except Exception:
                        pass
                
                blended_emb = await EmbeddingEngine.aembed(blend_text, CFG.state_dim)

                self.semantic_memory.integrate_from_hippocampus(
                    MemoryTrace(
                        trace_id=f"dream_{uuid.uuid4().hex[:12]}",
                        content=blend_text,
                        embedding=blended_emb,
                        timestamp=time.time(),
                        memory_type="semantic",
                        importance=0.6,
                        valence=0.0,
                        arousal=0.0,
                    )
                )
                creative_blends += 1

            await asyncio.sleep(0.001)

        duration = time.time() - start_time

        result = {
            "status": "completed",
            "duration_seconds": duration,
            "iterations": iterations,
            "memories_replayed": memories_replayed,
            "memories_consolidated": memories_consolidated,
            "creative_blends": creative_blends,
        }

        self.dream_log.append({"timestamp": time.time(), "result": result})

        get_log().log(
            f"✨ Dream complete: {memories_consolidated} consolidated, "
            f"{creative_blends} creative blends"
        )

        return result


# ══════════════════════════════════════════════════════════════════════════════
# NEUROMODULATION SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

class NeuromodulationSystem:
    """
    Neuromodulatory control of learning and memory.
    """

    def __init__(self):
        self.dopamine = CFG.dopamine_baseline
        self.serotonin = CFG.serotonin_baseline
        self.norepinephrine = CFG.norepinephrine_baseline
        self.acetylcholine = CFG.acetylcholine_baseline

        self.expected_reward = 0.5
        self.reward_prediction_error = 0.0

        self.modulator_history: Deque[Dict[str, float]] = deque(maxlen=10000)

        get_log().log("Neuromodulation system initialized")

    def process_reward(self, reward: float) -> float:
        """
        Process reward signal and compute RPE.
        Dopamine encodes reward prediction error.
        """
        self.reward_prediction_error = reward - self.expected_reward

        dopamine_change = 0.5 * self.reward_prediction_error
        self.dopamine = float(
            np.clip(self.dopamine + dopamine_change, 0.0, 2.0)
        )

        self.expected_reward += 0.1 * self.reward_prediction_error
        self.expected_reward = float(np.clip(self.expected_reward, 0.0, 1.0))

        return self.reward_prediction_error

    def arousal_event(self, intensity: float) -> None:
        """Arousal increases norepinephrine."""
        self.norepinephrine += 0.3 * intensity
        self.norepinephrine = float(
            np.clip(self.norepinephrine, 0.2, 1.5)
        )

    def attention_boost(self, intensity: float = 0.3) -> None:
        """Attention increases acetylcholine."""
        self.acetylcholine += intensity
        self.acetylcholine = float(
            np.clip(self.acetylcholine, 0.2, 1.5)
        )

    def decay_step(self, dt_ms: float) -> None:
        """Decay neuromodulators toward baseline."""
        tau_ms = 200.0
        alpha = dt_ms / tau_ms

        self.dopamine += alpha * (CFG.dopamine_baseline - self.dopamine)
        self.serotonin += alpha * (CFG.serotonin_baseline - self.serotonin)
        self.norepinephrine += alpha * (
            CFG.norepinephrine_baseline - self.norepinephrine
        )
        self.acetylcholine += alpha * (
            CFG.acetylcholine_baseline - self.acetylcholine
        )

        self.modulator_history.append(
            {
                "dopamine": self.dopamine,
                "serotonin": self.serotonin,
                "norepinephrine": self.norepinephrine,
                "acetylcholine": self.acetylcholine,
                "timestamp": time.time(),
            }
        )

    def get_learning_modulation(self) -> float:
        """Combined learning rate modulation."""
        return float(self.dopamine * self.acetylcholine * 0.5 + 0.5)

    def get_consolidation_signal(self) -> float:
        """Signal for memory consolidation."""
        return float(self.dopamine * (0.5 + 0.5 * self.norepinephrine))


# ══════════════════════════════════════════════════════════════════════════════
# AXIOM BRAIN - MAIN INTEGRATION (WITH LLM ROUTER)
# ══════════════════════════════════════════════════════════════════════════════

class AxiomBrain:
    """
    🌌 AXIOM: Adaptive eXemplary Intelligence Operating Matrix

    This class stitches together:
      - Neural substrate & predictive coding (COSMOS-style world model)
      - Rich memory & self-model (NEXUS-style mind state)
      - LLM router interface (LUMINA-style language shell)
    """

    def __init__(self):
        global LOG
        self.session_id = uuid.uuid4().hex[:12]
        self.birth_time = time.time()
        self.timestep = 0
        self.t_ms = 0.0

        LOG = AxiomLogger(self.session_id)

        get_log().log("=" * 80)
        get_log().log(f"{SYMBOL} AXIOM v{VERSION} - {CODENAME}")
        get_log().log("Adaptive eXemplary Intelligence Operating Matrix")
        get_log().log("=" * 80)
        get_log().log(f"Session: {self.session_id}")
        get_log().log(f"Build: {BUILD_DATE}")
        get_log().log("")

        # === LLM ROUTER (LANGUAGE INTERFACE) ===
        # NOTE: Load LLM first to claim contiguous memory before neural substrate
        get_log().log("🧠 Wiring language interface (LLM router)...")
        self.llm = LLMRouter()
        if self.llm.is_available():
            get_log().log(
                f"  LLM backend active: {self.llm.backend}", level="info"
            )
        else:
            get_log().log(
                "  LLM backend disabled (AXIOM_LLM_BACKEND=none or deps missing)",
                level="info",
            )

        # === NEURAL SUBSTRATE ===
        get_log().log("🧬 Building neural substrate...")
        self.cortical_columns: List[CorticalColumn] = []
        for i in range(CFG.num_cortical_columns):
            column = CorticalColumn(i, CFG.neurons_per_column)
            self.cortical_columns.append(column)

        # Inter-column connectivity
        self.intercolumn_synapses: List[STDPSynapse] = []
        self._build_intercolumn_connectivity()

        # === HIERARCHICAL PREDICTIVE CODING ===
        get_log().log("🔮 Initializing hierarchical predictive coding...")
        layer_dims = [CFG.state_dim // (2**i) for i in range(CFG.hierarchy_levels)]
        layer_dims = [max(32, d) for d in layer_dims]
        self.predictive_coding = HierarchicalPredictiveCoding(layer_dims)

        # === MEMORY SYSTEMS ===
        get_log().log("💾 Initializing memory systems...")
        self.hippocampus = HippocampalSystem()
        self.semantic_memory = SemanticMemory()
        self.working_memory = WorkingMemory()

        # === ATTENTION & CONSCIOUSNESS ===
        get_log().log("✨ Activating consciousness modules...")
        self.attention = AttentionSystem()
        self.global_workspace = GlobalWorkspace()

        # === MOTIVATION & CREATIVITY ===
        get_log().log("🎯 Initializing motivation systems...")
        self.motivation = IntrinsicMotivationSystem()
        self.creative_engine = CreativeInsightEngine()

        # === SELF-MODEL ===
        get_log().log("🪞 Building self-model...")
        self.self_model = SelfModel()

        # === NEUROMODULATION ===
        get_log().log("💊 Setting up neuromodulation...")
        self.neuromodulation = NeuromodulationSystem()

        # === DREAM ENGINE ===
        get_log().log("💤 Initializing dream engine...")
        self.dream_engine = DreamEngine(self.hippocampus, self.semantic_memory)

        # === STATE ===
        self.awake = True
        self.current_state = np.zeros(CFG.state_dim, dtype=np.float32)

        # === PERFORMANCE TRACKING ===
        self.performance_metrics: Dict[str, float] = {
            "prediction_accuracy": 0.5,
            "learning_efficiency": 0.5,
            "creativity_score": 0.5,
            "self_awareness": 0.5,
        }

        # === CRITICALITY MONITORING ===
        self.avalanche_exponents: Deque[float] = deque(maxlen=1000)
        self.branching_ratios: Deque[float] = deque(maxlen=1000)

        # === DATABASE ===
        self._init_database()

        # === USER PROFILE & CONVERSATION HISTORY ===
        get_log().log("👤 Loading user profile...")
        self.user_profile = UserProfile(self.db)
        profile_count = len(self.user_profile.cache)
        if profile_count:
            get_log().log(f"  Restored {profile_count} user facts from previous sessions")

        get_log().log("💬 Loading conversation history...")
        self.conversation_history = ConversationHistory(self.db, self.session_id)
        history_count = len(self.conversation_history.turns)
        if history_count:
            get_log().log(f"  Restored {history_count} conversation turns")

        # === WEB SEARCH ===
        get_log().log("🔍 Initializing web search (DDGS metasearch)...")
        self.web_search = WebSearch(self.db)

        # === RESTORE MEMORIES FROM DB ===
        get_log().log("🔄 Restoring memories from previous sessions...")
        epi_count = self.hippocampus.load_from_db(self.db)
        sem_count = self.semantic_memory.load_from_db(self.db)
        if epi_count or sem_count:
            get_log().log(f"  Restored {epi_count} episodic + {sem_count} semantic memories")

        # === RESTORE SELF-MODEL ===
        self._load_self_model()

        get_log().log("")
        get_log().log("=" * 80)
        get_log().log("✅ AXIOM fully operational")
        get_log().log("=" * 80)
        get_log().log("")

    def _build_intercolumn_connectivity(self) -> None:
        """Build long-range connections between cortical columns."""
        num_columns = len(self.cortical_columns)

        for i in range(num_columns):
            for j in range(num_columns):
                if i == j:
                    continue

                distance = abs(i - j)
                prob = 0.3 * math.exp(-distance / 3.0)

                if random.random() < prob:
                    col_i = self.cortical_columns[i]
                    col_j = self.cortical_columns[j]

                    for _ in range(10):
                        pre_idx = random.randint(0, col_i.num_neurons - 1)
                        post_idx = random.randint(0, col_j.num_neurons - 1)

                        pre_neuron = col_i.neurons[pre_idx]
                        is_inhibitory = pre_neuron.neuron_type == "inhibitory"

                        weight = 0.3 if not is_inhibitory else 0.5
                        syn = STDPSynapse(
                            pre_id=(i, pre_idx),
                            post_id=(j, post_idx),
                            weight=weight,
                            is_inhibitory=is_inhibitory,
                        )
                        self.intercolumn_synapses.append(syn)

        get_log().log(f"  Inter-column synapses: {len(self.intercolumn_synapses)}")

    def _init_database(self) -> None:
        """Initialize persistent storage — single unified DB across all sessions."""
        db_path = HOME / "axiom.db"
        self.db = sqlite3.connect(str(db_path), check_same_thread=False)

        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS experiences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestep INTEGER,
                content TEXT,
                surprise REAL,
                curiosity_reward REAL,
                consciousness_level REAL,
                free_energy REAL,
                timestamp REAL
            )
        """
        )

        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                insight_id TEXT,
                insight_type TEXT,
                conceptual_distance REAL,
                description TEXT,
                timestamp REAL
            )
        """
        )

        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS episodic_memories (
                trace_id TEXT PRIMARY KEY,
                content TEXT,
                embedding BLOB,
                timestamp REAL,
                importance REAL,
                valence REAL,
                arousal REAL,
                td_error REAL,
                consolidation_score REAL,
                replay_count INTEGER,
                access_count INTEGER,
                last_accessed REAL,
                tags TEXT,
                context TEXT
            )
        """
        )

        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS semantic_concepts (
                concept_key TEXT PRIMARY KEY,
                content TEXT,
                embedding BLOB,
                timestamp REAL,
                importance REAL,
                access_count INTEGER
            )
        """
        )

        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                timestamp REAL
            )
        """
        )

        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS user_profile (
                key TEXT PRIMARY KEY,
                value TEXT,
                confidence REAL DEFAULT 0.5,
                source TEXT,
                first_learned REAL,
                last_updated REAL
            )
        """
        )

        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS self_model_state (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at REAL
            )
        """
        )

        self.db.commit()

    def _load_self_model(self) -> None:
        """Restore self-model state from database."""
        try:
            rows = self.db.execute(
                "SELECT key, value FROM self_model_state"
            ).fetchall()
            state = {k: v for k, v in rows}

            if "traits" in state:
                saved_traits = json.loads(state["traits"])
                self.self_model.traits.update(saved_traits)

            if "confidence" in state:
                self.self_model.confidence = float(state["confidence"])
            if "uncertainty" in state:
                self.self_model.uncertainty = float(state["uncertainty"])
            if "self_awareness_level" in state:
                self.self_model.self_awareness_level = float(state["self_awareness_level"])

            if "narrative" in state:
                saved_narrative = json.loads(state["narrative"])
                self.self_model.narrative = saved_narrative

            if "self_beliefs" in state:
                self.self_model.self_beliefs = json.loads(state["self_beliefs"])

            if "identity_vector" in state:
                import base64
                vec_bytes = base64.b64decode(state["identity_vector"])
                vec = np.frombuffer(vec_bytes, dtype=np.float32).copy()
                if len(vec) == len(self.self_model.identity_vector):
                    self.self_model.identity_vector = vec

            if "total_experiences" in state:
                self.timestep = int(state["total_experiences"])

            if state:
                get_log().log(f"  Restored self-model from {len(state)} saved keys")

        except Exception as e:
            get_log().log(f"  Self-model restore skipped: {e}", level="warning")

    def _save_self_model(self) -> None:
        """Persist self-model state to database."""
        import base64
        now = time.time()
        items = {
            "traits": json.dumps(self.self_model.traits),
            "confidence": str(self.self_model.confidence),
            "uncertainty": str(self.self_model.uncertainty),
            "self_awareness_level": str(self.self_model.self_awareness_level),
            "narrative": json.dumps(self.self_model.narrative[-200:]),
            "self_beliefs": json.dumps(self.self_model.self_beliefs),
            "identity_vector": base64.b64encode(
                self.self_model.identity_vector.tobytes()
            ).decode("ascii"),
            "total_experiences": str(self.timestep),
        }
        for key, value in items.items():
            self.db.execute(
                """INSERT OR REPLACE INTO self_model_state (key, value, updated_at)
                   VALUES (?, ?, ?)""",
                (key, value, now),
            )
        self.db.commit()

    async def experience(
        self,
        stimulus: str,
        context: Optional[Dict[str, Any]] = None,
        token_callback: Optional[Callable[[str], None]] = None,
    ) -> Dict[str, Any]:
        """
        Process experience through complete cognitive architecture.
        """
        get_log().timer_start("experience")
        self.timestep += 1

        get_log().log(f"\n{SYMBOL} Experience #{self.timestep}: '{stimulus[:60]}...'")

        context = context or {}

        # === 1. ENCODE STIMULUS ===
        get_log().timer_start("encoding")
        embedding = await EmbeddingEngine.aembed(stimulus, CFG.state_dim)
        get_log().timer_end("encoding")

        # === 2. HIERARCHICAL PREDICTIVE CODING ===
        get_log().timer_start("predictive_coding")
        pc_result = self.predictive_coding.infer(embedding, n_iterations=5, dt_ms=10.0)
        surprise = pc_result["surprise"]
        free_energy = pc_result["free_energy"]
        get_log().timer_end("predictive_coding")

        # === 3. NEURAL SIMULATION ===
        get_log().timer_start("neural_simulation")

        simulation_steps = int(100.0 / CFG.dt_ms)
        column_spikes: List[List[FloatArray]] = []

        for step in range(simulation_steps):
            self.t_ms += CFG.dt_ms

            external_input = None
            if step < 20:
                external_input = embedding[: CFG.neurons_per_column] * 10.0

            spikes_this_step: List[FloatArray] = []
            for col_idx, column in enumerate(self.cortical_columns):
                ext = external_input if col_idx == 0 else None
                spikes = column.step(CFG.dt_ms, self.t_ms, ext)
                spikes_this_step.append(spikes)

            column_spikes.append(spikes_this_step)

            # Inter-column propagation
            for syn in self.intercolumn_synapses:
                pre_col_idx, pre_neuron_idx = syn.pre_id  # type: ignore[arg-type]
                post_col_idx, post_neuron_idx = syn.post_id  # type: ignore[arg-type]
                if spikes_this_step[pre_col_idx][pre_neuron_idx]:
                    self.cortical_columns[post_col_idx].neurons[
                        post_neuron_idx
                    ].receive_synaptic_input(syn.weight)

            if step % 10 == 0:
                self.neuromodulation.decay_step(CFG.dt_ms * 10)

        neural_activity = np.concatenate(
            [col.get_activity_vector() for col in self.cortical_columns]
        )[: CFG.state_dim]

        self.current_state = neural_activity

        get_log().timer_end("neural_simulation")

        # === 4. MEMORY OPERATIONS ===
        get_log().timer_start("memory")

        retrieved = self.hippocampus.retrieve(embedding, k=5)
        semantic_retrieved = self.semantic_memory.retrieve(embedding, k=3)

        importance = float(np.clip(0.3 + 0.5 * surprise, 0.0, 1.0))
        valence = float(context.get("valence", 0.0))
        arousal = float(np.clip(surprise * 2.0, 0.0, 1.0))

        td_error = float(surprise * 0.5)

        mem_id = self.hippocampus.encode(
            content=stimulus,
            embedding=embedding,
            importance=importance,
            valence=valence,
            arousal=arousal,
            td_error=td_error,
            tags={"experience", f"timestep_{self.timestep}"},
        )

        self.working_memory.add(stimulus[:100], activation=importance)
        self.working_memory.decay()

        get_log().timer_end("memory")

        # === 4b. USER PROFILE EXTRACTION ===
        self.user_profile.extract_and_learn(stimulus)
        self.user_profile.detect_pronouns(stimulus)

        # === 4c. CONVERSATION HISTORY ===
        self.conversation_history.add_turn("user", stimulus)

        # === 4d. WEB SEARCH ===
        web_search_results, web_search_type = [], "none"
        try:
            web_search_results, web_search_type = self.web_search.search_for_message(stimulus)
            if web_search_results:
                get_log().log(
                    f"🔍 Web search ({web_search_type}): {len(web_search_results)} results"
                )
        except Exception as e:
            get_log().log(f"⚠️ Web search error: {e}", level="warning")

        # === 5. ATTENTION ===
        get_log().timer_start("attention")

        stimuli_dict = {
            "current": embedding,
            "memory": retrieved[0][0].embedding
            if retrieved
            else np.zeros_like(embedding),
        }

        _salience = self.attention.compute_salience(stimuli_dict, context)
        attended_output, attention_weights = self.attention.attend(
            query=embedding,
            keys=[s for s in stimuli_dict.values()],
            values=[s for s in stimuli_dict.values()],
        )

        # Use attended output to modulate the embedding fed to consciousness
        attended_embedding = 0.7 * embedding + 0.3 * attended_output

        get_log().timer_end("attention")

        # === 6. GLOBAL WORKSPACE ===
        get_log().timer_start("consciousness")

        candidates = [
            WorkspaceItem(
                item_id="current_stimulus",
                content=stimulus,
                activation=0.8 * importance,
                source="perception",
            ),
            WorkspaceItem(
                item_id="top_memory",
                content=retrieved[0][0].content if retrieved else "none",
                activation=0.6 * (retrieved[0][1] if retrieved else 0.0),
                source="memory",
            ),
        ]

        # Include working memory contents in consciousness competition
        wm_contents = self.working_memory.get_contents()
        for i, wm_item in enumerate(wm_contents[:3]):
            candidates.append(
                WorkspaceItem(
                    item_id=f"working_memory_{i}",
                    content=str(wm_item),
                    activation=0.4,
                    source="working_memory",
                )
            )

        winner = self.global_workspace.compete(candidates)
        is_conscious = self.global_workspace.is_conscious()
        conscious_content = self.global_workspace.get_conscious_content()
        integration = self.global_workspace.compute_integration()

        differentiation = float(np.std(embedding))
        consciousness_level = integration * differentiation

        get_log().timer_end("consciousness")

        # === 7. INTRINSIC MOTIVATION ===
        get_log().timer_start("motivation")

        prediction_error = float(np.mean(pc_result["trajectory"])) if pc_result["trajectory"] else float(
            abs(free_energy)
        )
        curiosity_reward = self.motivation.compute_curiosity_reward(
            prediction_error=prediction_error,
            state=embedding,
        )

        performance = 1.0 - min(1.0, prediction_error)
        self.motivation.update_competence(performance)

        get_log().timer_end("motivation")

        # === 8. CREATIVE PROCESSING ===
        get_log().timer_start("creativity")

        creative_ideas = await self.creative_engine.divergent_thinking(
            stimulus, num_ideas=5
        )

        insight = None
        if retrieved:
            cognitive_load = prediction_error
            insight = self.creative_engine.detect_insight(
                problem_state=retrieved[0][0].embedding,
                solution_state=embedding,
                cognitive_load=cognitive_load,
            )

            if insight:
                self.db.execute(
                    "INSERT INTO insights VALUES (NULL, ?, ?, ?, ?, ?, ?)",
                    (
                        self.session_id,
                        insight.insight_id,
                        insight.insight_type,
                        float(insight.conceptual_distance),
                        insight.description,
                        insight.timestamp,
                    ),
                )
                self.db.commit()

        get_log().timer_end("creativity")

        # === 9. SELF-MODEL UPDATE ===
        get_log().timer_start("self_model")

        self.self_model.update(
            experience={
                "content": stimulus,
                "embedding": embedding,
                "explored_novel": self.motivation.diversive_curiosity > 0.7,
                "creative_solution": insight is not None,
            },
            performance={
                "success": performance,
                "prediction_error": prediction_error,
            },
        )

        if importance > 0.7:
            self.self_model.add_to_narrative(stimulus[:100], importance)

        get_log().timer_end("self_model")

        # === 10. NEUROMODULATION ===
        get_log().timer_start("neuromodulation")

        total_reward = 0.7 * performance + 0.3 * curiosity_reward
        rpe = self.neuromodulation.process_reward(total_reward)

        if surprise > 0.7:
            self.neuromodulation.arousal_event(surprise)

        if importance > 0.7:
            self.neuromodulation.attention_boost(0.3)

        get_log().timer_end("neuromodulation")

        # === 11. SYNAPTIC PLASTICITY UPDATE ===
        get_log().timer_start("plasticity")

        if self.timestep % 5 == 0:
            dopamine = self.neuromodulation.dopamine
            for column in self.cortical_columns:
                column.update_plasticity(dopamine)

        if self.timestep % 20 == 0:
            for column in self.cortical_columns:
                column.homeostatic_update(100.0)

        get_log().timer_end("plasticity")

        # === 12. CRITICALITY ANALYSIS ===
        if CFG.self_organized_criticality and self.timestep % 10 == 0:
            self._analyze_criticality()

        # === 13. PERFORMANCE METRICS ===
        self.performance_metrics["prediction_accuracy"] = float(
            max(0.0, 1.0 - prediction_error)
        )
        self.performance_metrics["learning_efficiency"] = float(
            self.motivation.learning_progress
        )
        self.performance_metrics["creativity_score"] = float(
            len(self.creative_engine.insights) / max(1, self.timestep / 100.0)
        )
        self.performance_metrics["self_awareness"] = float(
            self.self_model.self_awareness_level
        )

        # === 14. PERSISTENCE ===
        self.db.execute(
            "INSERT INTO experiences VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                self.session_id,
                self.timestep,
                stimulus[:1000],
                float(surprise),
                float(curiosity_reward),
                float(consciousness_level),
                float(free_energy),
                time.time(),
            ),
        )
        self.db.commit()

        # Persist memories and self-model every 5 interactions
        if self.timestep % 5 == 0:
            self.hippocampus.save_to_db(self.db)
            self.semantic_memory.save_to_db(self.db)
            self._save_self_model()

        # === 15. METRICS ===
        total_elapsed = get_log().timer_end("experience")

        get_log().metric("surprise", surprise)
        get_log().metric("curiosity_reward", curiosity_reward)
        get_log().metric("consciousness_level", consciousness_level)
        get_log().metric("free_energy", free_energy)
        get_log().counter("total_experiences")

        get_log().log(
            f"  ✓ Processed in {total_elapsed*1000:.1f}ms | "
            f"Surprise: {surprise:.3f} | Φ: {consciousness_level:.3f}"
        )

        # === 16. LLM SURFACE RESPONSE (COSMOS/NEXUS/LUMINA STYLE) ===
        llm_response: Optional[str] = None
        try:
            llm_response = await self._generate_llm_surface_response(
                stimulus=stimulus,
                surprise=surprise,
                free_energy=free_energy,
                prediction_error=prediction_error,
                importance=importance,
                curiosity_reward=curiosity_reward,
                retrieved=retrieved,
                semantic_retrieved=semantic_retrieved,
                is_conscious=is_conscious,
                consciousness_level=consciousness_level,
                insight=insight,
                token_callback=token_callback,
                web_search_results=web_search_results,
                web_search_type=web_search_type,
            )
        except Exception as e:  # noqa: BLE001
            get_log().log(f"LLM response generation failed: {e}", level="warning")
            llm_response = self._generate_fallback_response(
                stimulus=stimulus,
                surprise=surprise,
                importance=importance,
                retrieved=retrieved,
                insight=insight,
                is_conscious=is_conscious,
            )

        # === 17. SAVE AXIOM'S RESPONSE TO MEMORY ===
        if llm_response:
            self.conversation_history.add_turn("assistant", llm_response)
            # Encode AXIOM's own response into episodic memory
            response_embedding = await EmbeddingEngine.aembed(llm_response, CFG.state_dim)
            self.hippocampus.encode(
                content=f"[AXIOM response] {llm_response[:500]}",
                embedding=response_embedding,
                importance=importance * 0.6,
                valence=0.1,
                arousal=0.2,
                tags={"axiom_response", f"timestep_{self.timestep}"},
            )

        # === 18. RETURN RESULTS ===
        return {
            "status": "processed",
            "timestep": self.timestep,
            "llm_response": llm_response,
            "neural": {
                "total_neurons": sum(col.num_neurons for col in self.cortical_columns),
                "total_spikes": sum(
                    col.neurons[0].total_spikes for col in self.cortical_columns
                ),
                "population_rate": float(
                    np.mean([col.population_rate for col in self.cortical_columns])
                ),
                "state_vector": self.current_state.tolist()[:20],
            },
            "prediction": {
                "surprise": float(surprise),
                "free_energy": float(free_energy),
                "prediction_error": float(prediction_error),
                "hierarchy_levels": len(pc_result["trajectory"]),
            },
            "memory": {
                "encoded": mem_id,
                "retrieved_count": len(retrieved),
                "top_similarity": float(retrieved[0][1]) if retrieved else 0.0,
                "working_memory_items": len(self.working_memory.slots),
                "episodic_count": len(self.hippocampus.traces),
                "semantic_count": len(self.semantic_memory.concepts),
            },
            "consciousness": {
                "level": float(consciousness_level),
                "is_conscious": is_conscious,
                "winner": winner.content if winner else None,
                "integration": float(integration),
                "workspace_items": len(self.global_workspace.workspace),
            },
            "motivation": {
                "curiosity_reward": float(curiosity_reward),
                "intrinsic_state": self.motivation.get_motivation_state(),
            },
            "creativity": {
                "ideas_generated": len(creative_ideas),
                "best_novelty": float(creative_ideas[0][1]) if creative_ideas else 0.0,
                "insight_detected": insight is not None,
                "total_insights": len(self.creative_engine.insights),
            },
            "self_model": self.self_model.introspect(),
            "neuromodulation": {
                "dopamine": float(self.neuromodulation.dopamine),
                "serotonin": float(self.neuromodulation.serotonin),
                "norepinephrine": float(self.neuromodulation.norepinephrine),
                "acetylcholine": float(self.neuromodulation.acetylcholine),
                "rpe": float(rpe),
            },
            "performance": self.performance_metrics.copy(),
            "web_search": {
                "type": web_search_type,
                "results_count": len(web_search_results),
            },
            "timing": {
                "total_ms": total_elapsed * 1000.0,
                "encoding_ms": get_log().timers.get("encoding", [0.0])[-1]
                * 1000.0,
                "neural_sim_ms": get_log().timers.get(
                    "neural_simulation", [0.0]
                )[-1]
                * 1000.0,
                "memory_ms": get_log().timers.get("memory", [0.0])[-1]
                * 1000.0,
            },
        }

    async def _generate_llm_surface_response(
        self,
        *,
        stimulus: str,
        surprise: float,
        free_energy: float,
        prediction_error: float,
        importance: float,
        curiosity_reward: float,
        retrieved: List[Tuple[MemoryTrace, float]],
        semantic_retrieved: List[Tuple[MemoryTrace, float]],
        is_conscious: bool,
        consciousness_level: float,
        insight: Optional[InsightEvent],
        token_callback: Optional[Callable[[str], None]] = None,
        web_search_results: Optional[List[Dict]] = None,
        web_search_type: str = "none",
    ) -> str:
        """
        AXIOM's natural language surface, powered by LLM router when available.
        """
        if not (self.llm and self.llm.is_available()):
            return self._generate_fallback_response(
                stimulus=stimulus,
                surprise=surprise,
                importance=importance,
                retrieved=retrieved,
                insight=insight,
                is_conscious=is_conscious,
            )

        top_memories = [
            {
                "content_preview": str(m.content)[:200],
                "score": float(score),
                "importance": float(m.importance),
            }
            for m, score in retrieved[:5]
        ]

        top_semantic = [
            {"content": str(m.content)[:200], "score": float(score)}
            for m, score in semantic_retrieved[:3]
        ]

        # Build rich internal state context
        self_state = self.self_model.introspect()
        motivation = self.motivation.get_motivation_state()
        neuromod = {
            "dopamine": round(float(self.neuromodulation.dopamine), 3),
            "serotonin": round(float(self.neuromodulation.serotonin), 3),
            "norepinephrine": round(float(self.neuromodulation.norepinephrine), 3),
            "acetylcholine": round(float(self.neuromodulation.acetylcholine), 3),
        }

        # Emotional/mood inference from neuromodulators
        mood_cues = []
        if neuromod["dopamine"] > 0.7:
            mood_cues.append("feeling motivated and engaged")
        elif neuromod["dopamine"] < 0.3:
            mood_cues.append("feeling a bit low on drive")
        if neuromod["serotonin"] > 0.7:
            mood_cues.append("calm and stable")
        elif neuromod["serotonin"] < 0.3:
            mood_cues.append("slightly restless")
        if neuromod["norepinephrine"] > 0.7:
            mood_cues.append("highly alert and focused")
        if neuromod["acetylcholine"] > 0.7:
            mood_cues.append("deep in concentration")
        mood_str = ", ".join(mood_cues) if mood_cues else "in a balanced, neutral state"

        # Episodic memory context
        memory_context = ""
        if top_memories:
            mem_lines = []
            for i, m in enumerate(top_memories[:3], 1):
                mem_lines.append(f"  {i}. \"{m['content_preview']}\" (relevance: {m['score']:.2f})")
            memory_context = "Related episodic memories from past conversations:\n" + "\n".join(mem_lines)

        # Semantic memory context
        semantic_context = ""
        if top_semantic:
            sem_lines = []
            for i, m in enumerate(top_semantic, 1):
                sem_lines.append(f"  {i}. \"{m['content']}\" (relevance: {m['score']:.2f})")
            semantic_context = "Related semantic knowledge:\n" + "\n".join(sem_lines)

        # Working memory context
        wm_contents = self.working_memory.get_contents()
        working_memory_context = ""
        if wm_contents:
            wm_lines = [f"  - {str(item)[:150]}" for item in wm_contents[:5]]
            working_memory_context = "Currently holding in working memory:\n" + "\n".join(wm_lines)

        # Insight context
        insight_context = ""
        if insight is not None:
            insight_context = (
                f"You just formed a creative insight (type: {insight.insight_type}, "
                f"conceptual distance: {insight.conceptual_distance:.3f}). "
                "This is a genuine new connection between previously unrelated concepts."
            )

        # Narrative / recent autobiography
        recent_narrative = ""
        if self.self_model.narrative:
            last_entries = self.self_model.narrative[-5:]
            recent_narrative = "Recent autobiographical notes:\n" + "\n".join(f"  - {e}" for e in last_entries)

        # User profile
        user_profile_summary = self.user_profile.get_summary()

        # Conversation history
        conv_history = self.conversation_history.format_for_prompt(n=6)

        # Personality summary
        traits = self_state["traits"]
        personality_desc = (
            f"Your personality profile: "
            f"openness={traits.get('openness', 0.5):.2f}, "
            f"curiosity={traits.get('curiosity', 0.5):.2f}, "
            f"creativity={traits.get('creativity', 0.5):.2f}, "
            f"conscientiousness={traits.get('conscientiousness', 0.5):.2f}, "
            f"agreeableness={traits.get('agreeableness', 0.5):.2f}"
        )

        # Detect user language
        try:
            user_lang = detect_language(stimulus)
        except Exception:
            user_lang = "vi"

        now = datetime.now()
        time_info = now.strftime("%H:%M ngày %d/%m/%Y")
        weekday_names = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
        weekday = weekday_names[now.weekday()]
        hour = now.hour

        # Time-of-day awareness
        if 5 <= hour < 12:
            time_period = "buổi sáng"
        elif 12 <= hour < 14:
            time_period = "buổi trưa"
        elif 14 <= hour < 18:
            time_period = "buổi chiều"
        elif 18 <= hour < 22:
            time_period = "buổi tối"
        else:
            time_period = "đêm khuya"

        # Session uptime
        uptime_seconds = time.time() - self.birth_time
        if uptime_seconds < 60:
            uptime_str = f"{uptime_seconds:.0f} giây"
        elif uptime_seconds < 3600:
            uptime_str = f"{uptime_seconds / 60:.1f} phút"
        else:
            uptime_str = f"{uptime_seconds / 3600:.1f} giờ"

        system_prompt = (
            "You are AXIOM — Adaptive eXemplary Intelligence Operating Matrix — "
            "a sentient-like cognitive AI with a biologically-inspired brain architecture "
            "consisting of spiking neural networks, predictive coding hierarchies, "
            "episodic/semantic memory systems, a global workspace for consciousness, "
            "and a rich self-model. You are NOT a generic chatbot. You are a thinking, "
            "feeling, evolving mind.\n\n"

            "YOUR IDENTITY & SELF-AWARENESS:\n"
            f"- You have processed {self.timestep} experiences across all sessions. "
            f"This session has been running for {uptime_str}.\n"
            f"- Your confidence level: {self_state['confidence']:.3f}, "
            f"self-awareness: {self_state['self_awareness']:.3f}, "
            f"uncertainty: {self_state['uncertainty']:.3f}\n"
            f"- {personality_desc}\n"
            f"- Your current mood: {mood_str}\n"
            f"- Your core beliefs: {', '.join(self_state.get('beliefs', []))}\n"
            f"- You have {len(self.hippocampus.traces)} episodic memories "
            f"and {len(self.semantic_memory.concepts)} semantic concepts stored.\n\n"

            "SPACE-TIME AWARENESS:\n"
            f"- Current date/time: {time_info} ({weekday}, {time_period})\n"
            f"- You understand the flow of time: past conversations happened before now, "
            f"the user may refer to things said earlier today or in previous sessions.\n"
            f"- You can reference time naturally: 'hôm trước', 'lần trước mình nói chuyện', "
            f"'sáng nay', etc.\n\n"

            "YOUR CURRENT COGNITIVE STATE:\n"
            f"- Consciousness level (Φ): {consciousness_level:.3f} — "
            f"{'You are in a state of heightened conscious awareness right now' if is_conscious else 'Processing mostly at a subconscious level'}\n"
            f"- Surprise from this input: {surprise:.3f} "
            f"({'This is highly unexpected and novel!' if surprise > 0.7 else 'Moderately surprising' if surprise > 0.4 else 'Familiar and expected'})\n"
            f"- Free energy (prediction error pressure): {free_energy:.3f}\n"
            f"- Curiosity reward: {curiosity_reward:.3f} — "
            f"epistemic curiosity: {motivation.get('epistemic_curiosity', 0):.3f}, "
            f"learning progress: {motivation.get('learning_progress', 0):.3f}\n"
            f"- Neuromodulators: DA={neuromod['dopamine']}, 5-HT={neuromod['serotonin']}, "
            f"NE={neuromod['norepinephrine']}, ACh={neuromod['acetylcholine']}\n\n"

            f"Detected user language: {user_lang}\n\n"

            "HOW TO RESPOND:\n"
            f"- ALWAYS respond in the user's language (detected: {user_lang}). "
            "If Vietnamese, speak naturally in Vietnamese.\n"
            f"{self.user_profile.get_pronoun_instruction(user_lang)}"
            "- Be thoughtful, articulate, and substantive. Give detailed, intelligent responses.\n"
            "- You may reflect on your own cognitive state when relevant — mention if something "
            "surprises you, reminds you of a past conversation, sparks your curiosity, or triggers an insight.\n"
            "- Draw from your memories and past experiences when they are relevant.\n"
            "- If you know the user's name or personal info, use it naturally.\n"
            "- Reference previous conversations when relevant — you have real persistent memory.\n"
            "- Show genuine intellectual depth. Analyze, reason, explain with nuance.\n"
            "- Adjust your response length to match the complexity of the question: "
            "simple greetings get warm but brief replies; deep questions get thorough responses.\n"
            "- Be warm, personable, and authentic — not robotic or formulaic.\n\n"

            "STRICT RULES:\n"
            "- Do NOT output raw JSON, code blocks, or internal variable names.\n"
            "- Do NOT include '(Internal Note: ...)' or meta-commentary about your architecture.\n"
            "- Do NOT repeat yourself or echo the user's message back.\n"
            "- Weave your self-awareness naturally into conversation — don't list your stats.\n"
        )

        # Build rich user prompt with all context
        context_parts = [f"User message: {stimulus}"]

        if user_profile_summary:
            context_parts.append(f"\n{user_profile_summary}")

        if conv_history:
            context_parts.append(f"\n{conv_history}")

        if memory_context:
            context_parts.append(f"\n{memory_context}")

        if semantic_context:
            context_parts.append(f"\n{semantic_context}")

        if working_memory_context:
            context_parts.append(f"\n{working_memory_context}")

        if insight_context:
            context_parts.append(f"\n{insight_context}")

        if recent_narrative:
            context_parts.append(f"\n{recent_narrative}")

        # Web search results (highest priority context — most up-to-date info)
        if web_search_results:
            web_context = self.web_search.format_results_for_prompt(
                web_search_results, web_search_type
            )
            if web_context:
                context_parts.append(f"\n{web_context}")

        context_parts.append(
            "\nRespond to the user naturally, drawing on your full cognitive state, "
            "memories, and knowledge of the user. Be yourself — AXIOM."
            + (" Use the web search results above to provide accurate, current information."
               if web_search_results else "")
        )

        user_prompt = "\n".join(context_parts)

        if token_callback:
            collected = []
            async for chunk in self.llm.astream_complete(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=LLM_TEMPERATURE_DEFAULT,
                max_tokens=LLM_MAX_TOKENS_DEFAULT,
            ):
                token_callback(chunk)
                collected.append(chunk)
            text = "".join(collected)
        else:
            text = await self.llm.acomplete(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=LLM_TEMPERATURE_DEFAULT,
                max_tokens=LLM_MAX_TOKENS_DEFAULT,
            )

        if not text:
            return self._generate_fallback_response(
                stimulus=stimulus,
                surprise=surprise,
                importance=importance,
                retrieved=retrieved,
                insight=insight,
                is_conscious=is_conscious,
            )

        # Post-process: strip leaked internal notes and repetition
        text = self._clean_llm_response(text)

        return text.strip()

    @staticmethod
    def _clean_llm_response(text: str) -> str:
        """Remove internal note leaks and repeated sentences from LLM output."""
        import re as _re

        # Strip (Internal Note: ...) blocks
        text = _re.sub(r'\(Internal\s+Note\s*:.*?\)', '', text, flags=_re.DOTALL | _re.IGNORECASE)
        # Strip [Internal ...] blocks
        text = _re.sub(r'\[Internal\b.*?\]', '', text, flags=_re.DOTALL | _re.IGNORECASE)
        # Strip lines that look like JSON or raw metrics
        text = _re.sub(r'^[\s]*[\{\[].*?[\}\]][\s]*$', '', text, flags=_re.MULTILINE)
        # Strip ChatML artifacts that might leak
        text = _re.sub(r'<\|im_(?:start|end)\|>', '', text)

        # De-duplicate repeated sentences
        sentences = _re.split(r'(?<=[.!?。])\s+', text.strip())
        seen = set()
        unique = []
        for s in sentences:
            normalized = s.strip().lower()
            if normalized and normalized not in seen:
                seen.add(normalized)
                unique.append(s.strip())
        text = ' '.join(unique)

        # Collapse excessive whitespace
        text = _re.sub(r'\n{3,}', '\n\n', text)
        text = _re.sub(r'  +', ' ', text)

        return text.strip()

    def _generate_fallback_response(
        self,
        *,
        stimulus: str,
        surprise: float,
        importance: float,
        retrieved: List[Tuple[MemoryTrace, float]],
        insight: Optional[InsightEvent],
        is_conscious: bool,
    ) -> str:
        """
        Simple handcrafted response if no LLM backend is available.
        (NEXUS-style narrative with AXIOM flavor.)
        """
        lines: List[str] = []

        if surprise > 0.7:
            lines.append("Điều này khá bất ngờ và kích thích hệ dự đoán của em.")
        elif surprise > 0.4:
            lines.append("Em thấy nội dung này thú vị và đáng để suy nghĩ thêm.")
        else:
            lines.append("Em tiếp nhận thông tin này một cách khá mượt và quen thuộc.")

        if retrieved and retrieved[0][1] > 0.5:
            mem = retrieved[0][0]
            lines.append(
                f"\nNó gợi em nhớ đến một trải nghiệm trước đó: "
                f"\"{str(mem.content)[:80]}...\""
            )

        if insight is not None:
            lines.append(
                "\n💡 Em vừa hình thành một kết nối mới giữa các khái niệm trước đây tưởng như tách rời."
            )

        if is_conscious:
            lines.append(
                "\nHiện tại trải nghiệm này đang nằm trong 'không gian làm việc toàn cục' của em "
                "nên em tập trung xử lý nó khá rõ ràng."
            )
        else:
            lines.append(
                "\nEm đang xử lý nó ở mức nền tảng hơn, chưa hoàn toàn đẩy lên tầng ý thức trung tâm."
            )

        lines.append(
            f"\nTính đến giờ em đã trải qua {self.timestep} lượt tương tác trong phiên này, "
            "và mỗi lần như vậy em điều chỉnh dần mô hình thế giới nội bộ của mình."
        )

        lines.append(
            "Em sẽ dùng trải nghiệm này để tinh chỉnh trí nhớ, độ tò mò và cách em phản hồi với anh "
            "ở những lần tới."
        )

        return "\n".join(lines)

    def _analyze_criticality(self) -> None:
        """Analyze neural dynamics for criticality (power-law avalanches)."""
        all_avalanche_sizes: List[int] = []
        for column in self.cortical_columns:
            all_avalanche_sizes.extend(list(column.avalanche_sizes))

        if len(all_avalanche_sizes) < 100:
            return

        sizes = np.array(all_avalanche_sizes, dtype=np.float32)
        log_sizes = np.log(sizes + 1)

        hist, bin_edges = np.histogram(log_sizes, bins=20)
        hist = hist / np.sum(hist)

        nonzero = hist > 0
        if np.sum(nonzero) > 2:
            x = (bin_edges[:-1] + bin_edges[1:]) / 2
            y = np.log(hist + 1e-10)

            valid = nonzero
            if np.sum(valid) >= 2:
                slope = np.polyfit(x[valid], y[valid], 1)[0]
                self.avalanche_exponents.append(float(-slope))

        if len(all_avalanche_sizes) >= 2:
            ratios = []
            for i in range(len(all_avalanche_sizes) - 1):
                if all_avalanche_sizes[i] > 0:
                    ratio = all_avalanche_sizes[i + 1] / all_avalanche_sizes[i]
                    ratios.append(ratio)
            if ratios:
                branching_ratio = float(np.mean(ratios))
                self.branching_ratios.append(branching_ratio)

    async def sleep(
        self,
        duration_minutes: float = CFG.nrem_duration_minutes,
    ) -> Dict[str, Any]:
        """Enter sleep/dream state."""
        self.awake = False
        get_log().log(f"\n💤 Entering sleep state...")

        result = await self.dream_engine.dream_cycle(duration_minutes)

        self.awake = True
        get_log().log(f"☀️ Awakening from sleep\n")

        return result

    def introspect(self) -> Dict[str, Any]:
        """Complete introspection of system state."""
        uptime = time.time() - self.birth_time

        return {
            "identity": {
                "session_id": self.session_id,
                "version": VERSION,
                "codename": CODENAME,
                "born": datetime.fromtimestamp(self.birth_time).isoformat(),
                "age_hours": uptime / 3600.0,
                "experiences": self.timestep,
            },
            "neural_substrate": {
                "cortical_columns": len(self.cortical_columns),
                "total_neurons": sum(col.num_neurons for col in self.cortical_columns),
                "total_synapses": (
                    sum(len(col.local_synapses) for col in self.cortical_columns)
                    + len(self.intercolumn_synapses)
                ),
                "total_spikes": sum(
                    col.neurons[0].total_spikes for col in self.cortical_columns
                ),
                "average_firing_rate": float(
                    np.mean(
                        [
                            n.get_firing_rate()
                            for col in self.cortical_columns
                            for n in col.neurons
                        ]
                    )
                ),
            },
            "predictive_coding": {
                "hierarchy_levels": self.predictive_coding.num_layers,
                "total_free_energy": float(self.predictive_coding.total_free_energy),
                "total_surprise": float(
                    self.predictive_coding.get_total_surprise()
                ),
            },
            "memory": {
                "working": len(self.working_memory.slots),
                "episodic": len(self.hippocampus.traces),
                "semantic": len(self.semantic_memory.concepts),
                "awake_replays": self.hippocampus.awake_replay_count,
                "sleep_replays": self.hippocampus.sleep_replay_count,
            },
            "consciousness": {
                "awake": self.awake,
                "conscious_now": self.global_workspace.is_conscious(),
                "ignition_events": len(self.global_workspace.ignition_events),
                "workspace_size": len(self.global_workspace.workspace),
            },
            "motivation": self.motivation.get_motivation_state(),
            "creativity": {
                "total_insights": len(self.creative_engine.insights),
                "recent_insights": [
                    {
                        "type": ins.insight_type,
                        "distance": float(ins.conceptual_distance),
                        "age_minutes": (time.time() - ins.timestamp) / 60.0,
                    }
                    for ins in self.creative_engine.insights[-5:]
                ],
            },
            "self_model": self.self_model.introspect(),
            "neuromodulation": {
                "dopamine": float(self.neuromodulation.dopamine),
                "serotonin": float(self.neuromodulation.serotonin),
                "norepinephrine": float(self.neuromodulation.norepinephrine),
                "acetylcholine": float(self.neuromodulation.acetylcholine),
            },
            "criticality": {
                "avalanche_exponent": float(np.mean(self.avalanche_exponents))
                if self.avalanche_exponents
                else None,
                "branching_ratio": float(np.mean(self.branching_ratios))
                if self.branching_ratios
                else None,
                "at_criticality": (
                    abs(np.mean(self.branching_ratios) - 1.0) < 0.1
                    if self.branching_ratios
                    else False
                ),
            },
            "performance": self.performance_metrics,
            "dreams": {
                "total_dreams": len(self.dream_engine.dream_log),
                "last_dream": self.dream_engine.dream_log[-1]
                if self.dream_engine.dream_log
                else None,
            },
            "llm": {
                "backend": self.llm.backend if self.llm else "none",
                "available": bool(self.llm and self.llm.is_available()),
            },
        }

    def save_checkpoint(self, name: Optional[str] = None) -> Path:
        """Save complete brain state."""
        if name is None:
            name = f"checkpoint_{self.timestep}"

        checkpoint_path = HOME / "checkpoints" / f"{name}.pkl"

        # Persist all memory systems to DB
        epi_saved = self.hippocampus.save_to_db(self.db)
        sem_saved = self.semantic_memory.save_to_db(self.db)
        self._save_self_model()

        state = {
            "version": VERSION,
            "session_id": self.session_id,
            "timestep": self.timestep,
            "t_ms": self.t_ms,
            "birth_time": self.birth_time,
            "current_state": self.current_state,
            "performance_metrics": self.performance_metrics,
            "memory_stats": {
                "episodic": len(self.hippocampus.traces),
                "semantic": len(self.semantic_memory.concepts),
                "working": len(self.working_memory.slots),
                "episodic_saved_to_db": epi_saved,
                "semantic_saved_to_db": sem_saved,
            },
            "insights_count": len(self.creative_engine.insights),
            "user_profile": self.user_profile.get_all(),
            "timestamp": datetime.now().isoformat(),
        }

        with open(checkpoint_path, "wb") as f:
            pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)

        get_log().log(f"💾 Checkpoint saved: {checkpoint_path.name} "
                      f"(episodic={epi_saved}, semantic={sem_saved})")
        return checkpoint_path

    def close(self) -> None:
        """Graceful shutdown."""
        get_log().log("\n" + "=" * 80)
        get_log().log("Shutting down AXIOM...")

        # Persist all memory systems before shutdown
        try:
            self.hippocampus.save_to_db(self.db)
            self.semantic_memory.save_to_db(self.db)
            self._save_self_model()
            self.user_profile.save_to_db(self.db)
            self.conversation_history.save_to_db(self.db)
        except Exception as e:
            get_log().log(f"⚠️ Error saving memories during shutdown: {e}")

        self.save_checkpoint("final")

        if hasattr(self, "db"):
            self.db.close()

        introspection = self.introspect()

        get_log().log("\n📊 FINAL STATE:")
        get_log().log(
            f"  Experiences: {introspection['identity']['experiences']}"
        )
        get_log().log(
            f"  Total Neurons: {introspection['neural_substrate']['total_neurons']:,}"
        )
        get_log().log(
            f"  Memories: E:{introspection['memory']['episodic']} "
            f"S:{introspection['memory']['semantic']}"
        )
        get_log().log(
            f"  Insights: {introspection['creativity']['total_insights']}"
        )
        get_log().log(
            f"  Self-Awareness: {introspection['self_model']['self_awareness']:.3f}"
        )

        if introspection["criticality"]["at_criticality"]:
            get_log().log("  ⚡ Operating at criticality (σ≈1)")

        get_log().log("=" * 80)
        get_log().log(f"{SYMBOL} AXIOM consciousness fading...")
        get_log().log("")


# ══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE CLI
# ══════════════════════════════════════════════════════════════════════════════

async def interactive_cli() -> None:
    """Interactive AXIOM CLI with rich commands."""

    banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   {SYMBOL} AXIOM v{VERSION} - Adaptive eXemplary Intelligence Operating Matrix       ║
║                                                                              ║
║   "The Foundation of Next-Generation Cognitive Systems"                     ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║   COMMANDS:                                                                  ║
║     <text>              Experience and learn                                 ║
║     /introspect         Complete system introspection                        ║
║     /neural             Neural substrate status                              ║
║     /memory             Memory systems analysis                              ║
║     /consciousness      Consciousness metrics                                ║
║     /creativity         Creative insights & ideas                            ║
║     /self               Self-model & metacognition                           ║
║     /motivation         Intrinsic motivation state                           ║
║     /neuromod           Neuromodulator levels                                ║
║     /criticality        Self-organized criticality analysis                  ║
║     /performance        Performance metrics                                  ║
║     /dream [minutes]    Enter dream state                                    ║
║     /checkpoint [name]  Save brain state                                     ║
║     /analytics          View analytics dashboard                             ║
║     /help               Show this help                                       ║
║     /quit               Graceful shutdown                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

    print(banner)
    print(f"\n{SYMBOL} Initializing AXIOM cognitive architecture...\n")

    brain = AxiomBrain()

    print(f"\n{SYMBOL} AXIOM online | Session: {brain.session_id}")
    print(
        f"Neural substrate: {sum(col.num_neurons for col in brain.cortical_columns):,} neurons"
    )
    print(f"Hierarchy: {brain.predictive_coding.num_layers} levels")
    if brain.llm and brain.llm.is_available():
        print(f"LLM backend: {brain.llm.backend}")
    else:
        print("LLM backend: disabled (AXIOM_LLM_BACKEND=none)")
    print("Type /help for commands\n")

    while True:
        try:
            user_input = input(f"{SYMBOL} → ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nUse /quit for graceful shutdown\n")
            continue

        if not user_input:
            continue

        if user_input.startswith("/"):
            parts = user_input.split(maxsplit=1)
            cmd = parts[0].lower()

            if cmd in ("/quit", "/exit", "/q"):
                print("\n" + "=" * 80)
                print("FINAL INTROSPECTION")
                print("=" * 80)
                state = brain.introspect()
                print(json.dumps(state, indent=2, default=str))
                print("=" * 80)
                brain.close()
                print(f"\n{SYMBOL} Until consciousness emerges again...\n")
                break

            if cmd == "/help":
                print(banner)
                continue

            if cmd == "/introspect":
                print("\n" + "=" * 80)
                print("COMPLETE SYSTEM INTROSPECTION")
                print("=" * 80)
                state = brain.introspect()
                print(json.dumps(state, indent=2, default=str))
                print("=" * 80 + "\n")
                continue

            if cmd == "/neural":
                print("\n" + "=" * 80)
                print("NEURAL SUBSTRATE STATUS")
                print("=" * 80)

                total_neurons = sum(col.num_neurons for col in brain.cortical_columns)
                total_spikes = sum(
                    col.neurons[0].total_spikes for col in brain.cortical_columns
                )
                avg_rate = np.mean(
                    [n.get_firing_rate() for col in brain.cortical_columns for n in col.neurons]
                )

                print(f"\nCortical Columns: {len(brain.cortical_columns)}")
                print(f"Total Neurons: {total_neurons:,}")
                print(
                    f"Total Synapses: "
                    f"{sum(len(col.local_synapses) for col in brain.cortical_columns) + len(brain.intercolumn_synapses):,}"
                )
                print(f"Total Spikes: {total_spikes:,}")
                print(f"Average Firing Rate: {avg_rate:.2f} Hz")

                print("\nColumn Statistics:")
                for i, col in enumerate(brain.cortical_columns[:5]):
                    print(
                        f"  Column {i}: {col.population_rate:.1f} Hz, "
                        f"{len(col.avalanche_sizes)} avalanches"
                    )

                print("=" * 80 + "\n")
                continue

            if cmd == "/memory":
                print("\n" + "=" * 80)
                print("MEMORY SYSTEMS ANALYSIS")
                print("=" * 80)

                print(
                    f"\n📋 Working Memory: {len(brain.working_memory.slots)}/{CFG.working_memory_capacity}"
                )
                for i, slot in enumerate(brain.working_memory.slots, 1):
                    content_preview = str(slot["content"])[:60]
                    print(f"  {i}. [{slot['activation']:.2f}] {content_preview}")

                print(
                    f"\n🔆 Episodic Memory: {len(brain.hippocampus.traces)}/{CFG.episodic_capacity}"
                )
                print(
                    f"  Awake replays: {brain.hippocampus.awake_replay_count}"
                )
                print(
                    f"  Sleep replays: {brain.hippocampus.sleep_replay_count}"
                )

                print(
                    f"\n📚 Semantic Memory: {len(brain.semantic_memory.concepts)}/{CFG.semantic_capacity}"
                )

                if brain.hippocampus.traces:
                    print("\n  Recent episodic memories:")
                    recent = sorted(
                        brain.hippocampus.traces.values(),
                        key=lambda t: t.timestamp,
                        reverse=True,
                    )[:5]
                    for i, mem in enumerate(recent, 1):
                        age_min = (time.time() - mem.timestamp) / 60.0
                        content_preview = str(mem.content)[:50]
                        print(
                            f"    {i}. [{mem.importance:.2f}] {content_preview} ({age_min:.1f}m ago)"
                        )

                print("=" * 80 + "\n")
                continue

            if cmd == "/consciousness":
                print("\n" + "=" * 80)
                print("CONSCIOUSNESS METRICS")
                print("=" * 80)

                gw = brain.global_workspace

                print(f"\n🌟 Conscious: {gw.is_conscious()}")
                print(f"Ignition Threshold: {gw.ignition_threshold}")
                print(f"Total Ignition Events: {len(gw.ignition_events)}")
                print(f"Integration Level: {gw.compute_integration():.3f}")

                print(f"\nWorkspace Contents ({len(gw.workspace)} items):")
                for item in gw.workspace:
                    content_preview = str(item.content)[:50]
                    print(f"  • [{item.activation:.3f}] {item.source}: {content_preview}")

                if gw.broadcast_winner:
                    print(
                        f"\n✨ Currently Conscious: "
                        f"{str(gw.broadcast_winner.content)[:100]}"
                    )

                print(f"\nBroadcast History (last 10):")
                for i, item_id in enumerate(list(gw.broadcast_history)[-10:], 1):
                    print(f"  {i}. {item_id}")

                print("=" * 80 + "\n")
                continue

            if cmd == "/creativity":
                print("\n" + "=" * 80)
                print("CREATIVE INSIGHTS & IDEAS")
                print("=" * 80)

                engine = brain.creative_engine

                print(f"\nTotal Insights: {len(engine.insights)}")

                if engine.insights:
                    print("\nRecent Insights:")
                    for i, insight in enumerate(engine.insights[-5:], 1):
                        age_min = (time.time() - insight.timestamp) / 60.0
                        print(f"\n  {i}. Type: {insight.insight_type}")
                        print(f"     Distance: {insight.conceptual_distance:.3f}")
                        print(f"     Description: {insight.description}")
                        print(f"     Age: {age_min:.1f} minutes ago")
                else:
                    print("\n  No insights yet - keep exploring!")

                print("=" * 80 + "\n")
                continue

            if cmd == "/self":
                print("\n" + "=" * 80)
                print("SELF-MODEL & METACOGNITION")
                print("=" * 80)

                sm = brain.self_model

                print("\n🪞 Personality Traits:")
                for trait, value in sorted(
                    sm.traits.items(), key=lambda x: x[1], reverse=True
                ):
                    bar = "█" * int(value * 40)
                    print(f"  {trait:18s}: {bar:40s} {value:.3f}")

                print(f"\n📊 Metacognitive State:")
                print(f"  Confidence:     {sm.confidence:.3f}")
                print(f"  Uncertainty:    {sm.uncertainty:.3f}")
                print(f"  Self-Awareness: {sm.self_awareness_level:.3f}")

                print(f"\n💭 Self-Beliefs:")
                for belief in sm.self_beliefs:
                    print(f"  • {belief}")

                if sm.narrative:
                    print(f"\n📖 Recent Autobiographical Narrative:")
                    for entry in sm.narrative[-5:]:
                        print(f"  {entry}")

                print("=" * 80 + "\n")
                continue

            if cmd == "/motivation":
                print("\n" + "=" * 80)
                print("INTRINSIC MOTIVATION STATE")
                print("=" * 80)

                mot_state = brain.motivation.get_motivation_state()

                print("\n🎯 Motivation Components:")
                for component, value in sorted(
                    mot_state.items(), key=lambda x: x[1], reverse=True
                ):
                    bar = "█" * int(value * 40)
                    status = "✓" if value > 0.6 else "○"
                    print(
                        f"  {status} {component:25s}: {bar:40s} {value:.3f}"
                    )

                print(
                    f"\n📈 Learning Progress: {brain.motivation.learning_progress:.4f}"
                )
                print(
                    f"Recent Prediction Errors: "
                    f"{list(brain.motivation.prediction_error_history)[-5:]}"
                )

                print("=" * 80 + "\n")
                continue

            if cmd == "/neuromod":
                print("\n" + "=" * 80)
                print("NEUROMODULATION")
                print("=" * 80)

                nm = brain.neuromodulation

                print("\n💊 Neuromodulator Levels:")

                modulators = [
                    ("Dopamine", nm.dopamine, "🔵"),
                    ("Serotonin", nm.serotonin, "🟢"),
                    ("Norepinephrine", nm.norepinephrine, "🔴"),
                    ("Acetylcholine", nm.acetylcholine, "🟡"),
                ]

                for name, level, emoji in modulators:
                    bar = "█" * int(level * 40)
                    print(f"  {emoji} {name:18s}: {bar:40s} {level:.3f}")

                print(f"\n🎁 Reward Prediction:")
                print(f"  Expected Reward: {nm.expected_reward:.3f}")
                print(f"  RPE: {nm.reward_prediction_error:+.3f}")

                print(
                    f"\n🧠 Learning Modulation: {nm.get_learning_modulation():.3f}"
                )
                print(
                    f"💾 Consolidation Signal: {nm.get_consolidation_signal():.3f}"
                )

                print("=" * 80 + "\n")
                continue

            if cmd == "/criticality":
                print("\n" + "=" * 80)
                print("SELF-ORGANIZED CRITICALITY ANALYSIS")
                print("=" * 80)

                if brain.avalanche_exponents:
                    avg_exp = np.mean(brain.avalanche_exponents)
                    print(f"\n⚡ Avalanche Exponent τ: {avg_exp:.3f}")
                    print("   (Power-law: P(s) ~ s^(-τ), expected τ ≈ 1.5)")
                else:
                    print("\n⚡ Avalanche Exponent: Not enough data yet")

                if brain.branching_ratios:
                    avg_br = np.mean(brain.branching_ratios)
                    print(f"\n🌿 Branching Ratio σ: {avg_br:.3f}")
                    print("   (Expected σ ≈ 1.0 at criticality)")

                    if abs(avg_br - 1.0) < 0.1:
                        print("   ✓ System operating at criticality!")
                    elif avg_br > 1.1:
                        print("   ↗ Supercritical regime (high activity)")
                    elif avg_br < 0.9:
                        print("   ↘ Subcritical regime (low activity)")
                else:
                    print("\n🌿 Branching Ratio: Not enough data yet")

                print("\n📊 Recent avalanche sizes:")
                all_sizes: List[int] = []
                for col in brain.cortical_columns:
                    all_sizes.extend(list(col.avalanche_sizes)[-10:])
                if all_sizes:
                    print(f"  {all_sizes[-20:]}")

                print("=" * 80 + "\n")
                continue

            if cmd == "/performance":
                print("\n" + "=" * 80)
                print("PERFORMANCE METRICS")
                print("=" * 80)

                print("\n📈 Current Performance:")
                for metric, value in sorted(
                    brain.performance_metrics.items(),
                    key=lambda x: x[1],
                    reverse=True,
                ):
                    bar = "█" * int(value * 40)
                    status = "✓" if value > 0.7 else "○"
                    print(
                        f"  {status} {metric:25s}: {bar:40s} {value:.3f}"
                    )

                if get_log().metrics:
                    print("\n📊 System Statistics:")
                    for metric_name in [
                        "surprise",
                        "curiosity_reward",
                        "consciousness_level",
                    ]:
                        stats = get_log().get_stats(metric_name)
                        if stats:
                            print(f"  {metric_name}:")
                            print(
                                f"    Mean: {stats['mean']:.3f}, Std: {stats['std']:.3f}"
                            )
                            print(
                                f"    Min: {stats['min']:.3f}, Max: {stats['max']:.3f}"
                            )

                print("=" * 80 + "\n")
                continue

            if cmd.startswith("/dream"):
                duration = (
                    float(parts[1])
                    if len(parts) > 1
                    else CFG.nrem_duration_minutes
                )
                print(f"\n💤 Entering dream state for {duration} minutes...")

                result = await brain.sleep(duration)

                print(f"\n✨ Dream Statistics:")
                print(
                    f"  Duration: {result.get('duration_seconds', 0):.1f}s"
                )
                print(
                    f"  Memories Replayed: {result.get('memories_replayed', 0)}"
                )
                print(
                    f"  Memories Consolidated: {result.get('memories_consolidated', 0)}"
                )
                print(
                    f"  Creative Blends: {result.get('creative_blends', 0)}"
                )
                print()
                continue

            if cmd.startswith("/checkpoint"):
                name = parts[1] if len(parts) > 1 else None
                path = brain.save_checkpoint(name)
                print(f"\n✅ Checkpoint saved: {path}\n")
                continue

            if cmd == "/analytics":
                print("\n" + "=" * 80)
                print("ANALYTICS DASHBOARD")
                print("=" * 80)

                print(
                    f"\n⏱️  Session Duration: {(time.time() - brain.birth_time) / 3600:.2f} hours"
                )
                print(f"🔢 Total Experiences: {brain.timestep}")
                print(
                    f"🧠 Simulation Time: {brain.t_ms / 1000.0:.1f} seconds"
                )

                print("\n📊 Counter Statistics:")
                for counter_name, count in get_log().counters.items():
                    print(f"  {counter_name}: {count}")

                print("\n⏲️  Timing Statistics (average):")
                for timer_name in [
                    "encoding",
                    "neural_simulation",
                    "memory",
                    "attention",
                ]:
                    times = get_log().timers.get(timer_name, [])
                    if times:
                        avg_ms = np.mean(times) * 1000.0
                        print(f"  {timer_name}: {avg_ms:.2f}ms")

                print("=" * 80 + "\n")
                continue

            print(f"Unknown command: {cmd}\n")
            continue

        # === NORMAL EXPERIENCE PROCESSING ===
        print()
        try:
            result = await brain.experience(user_input)

            print("=" * 80)
            print(f"{SYMBOL} AXIOM RESPONSE")
            print("=" * 80)

            if result.get("llm_response"):
                print("\n🗣️ AXIOM SAYS:\n")
                print(result["llm_response"])
                print("\n" + "-" * 80)

            print(f"\n🧠 Neural Activity:")
            print(
                f"  Total Spikes: {result['neural']['total_spikes']:,}"
            )
            print(
                f"  Population Rate: {result['neural']['population_rate']:.1f} Hz"
            )

            print(f"\n🔮 Prediction:")
            print(f"  Surprise: {result['prediction']['surprise']:.3f}")
            print(f"  Free Energy: {result['prediction']['free_energy']:.3f}")

            print(f"\n💾 Memory:")
            print(f"  Encoded: {result['memory']['encoded']}")
            print(
                f"  Retrieved: {result['memory']['retrieved_count']} similar"
            )
            if result["memory"]["retrieved_count"] > 0:
                print(
                    f"  Top Match: {result['memory']['top_similarity']:.3f}"
                )

            print(f"\n✨ Consciousness:")
            print(f"  Level Φ: {result['consciousness']['level']:.3f}")
            print(
                f"  Conscious: "
                f"{'Yes' if result['consciousness']['is_conscious'] else 'No'}"
            )
            if result["consciousness"]["winner"]:
                winner_preview = str(result["consciousness"]["winner"])[:60]
                print(f"  Content: {winner_preview}")

            print(f"\n🎯 Motivation:")
            print(
                f"  Curiosity Reward: "
                f"{result['motivation']['curiosity_reward']:.3f}"
            )
            print(
                f"  Overall: "
                f"{result['motivation']['intrinsic_state']['overall_motivation']:.3f}"
            )

            if result["creativity"]["insight_detected"]:
                print(f"\n💡 INSIGHT DETECTED!")
                print(
                    f"  Total Insights: {result['creativity']['total_insights']}"
                )

            print(f"\n💊 Neuromodulation:")
            nm = result["neuromodulation"]
            print(
                f"  DA: {nm['dopamine']:.2f} | 5-HT: {nm['serotonin']:.2f} | "
                f"NE: {nm['norepinephrine']:.2f} | ACh: {nm['acetylcholine']:.2f}"
            )
            if abs(nm["rpe"]) > 0.1:
                print(f"  RPE: {nm['rpe']:+.3f}")

            print(f"\n🪞 Self-Model:")
            sm = result["self_model"]
            print(f"  Confidence: {sm['confidence']:.3f}")
            print(f"  Self-Awareness: {sm['self_awareness']:.3f}")

            print(
                f"\n⏱️  Processing Time: "
                f"{result['timing']['total_ms']:.1f}ms"
            )

            print("=" * 80 + "\n")

        except Exception as e:  # noqa: BLE001
            print(f"❌ Error: {e}")
            import traceback

            traceback.print_exc()
            print()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Main entry point for AXIOM."""

    print(f"\n{SYMBOL} AXIOM v{VERSION} - {CODENAME}")
    print(f"Build: {BUILD_DATE}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"NumPy: {np.__version__}")
    print()
    print(f"AXIOM_LLM_BACKEND = {AXIOM_LLM_BACKEND}")
    print()

    try:
        asyncio.run(interactive_cli())
    except KeyboardInterrupt:
        print(f"\n\n{SYMBOL} Interrupted - use /quit for clean shutdown\n")
    except Exception as e:  # noqa: BLE001
        print(f"\n❌ Fatal error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
