#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌌 AXIOM v1.0 — Gradio Web UI
Giao diện web cho hệ thống cognitive AXIOM.
Chạy: python axiom_ui.py
"""

import asyncio
import json
import os
import sys
import time
import threading
import queue
from datetime import datetime
from pathlib import Path

import gradio as gr

# ---------------------------------------------------------------------------
# Import AXIOM core (same folder)
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))

from axiom_v1 import (
    AxiomBrain,
    AxiomConfig,
    CFG,
    HOME,
    VERSION,
    CODENAME,
    BUILD_DATE,
    SYMBOL,
    DEPS,
)

# ---------------------------------------------------------------------------
# Global AXIOM instance (singleton)
# ---------------------------------------------------------------------------
_axiom: AxiomBrain | None = None


def get_axiom() -> AxiomBrain:
    """Lazy-init AXIOM singleton."""
    global _axiom
    if _axiom is None:
        _axiom = AxiomBrain()
    return _axiom


# ═══════════════════════════════════════════════════════════════════════════
# CHAT HANDLER
# ═══════════════════════════════════════════════════════════════════════════

def chat_respond(user_message: str, history: list):
    """Process a user message through AXIOM and return the response."""
    if not user_message.strip():
        yield history, ""
        return

    axiom = get_axiom()
    cmd = user_message.strip().lower()

    # ── Slash commands ──

    if cmd == "/introspect":
        data = axiom.introspect()
        bot_msg = f"```json\n{json.dumps(data, indent=2, default=str)}\n```"
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_msg})
        yield history, ""
        return

    if cmd == "/neural":
        info = axiom.introspect()
        ns = info["neural_substrate"]
        bot_msg = (
            "**🧬 Neural Substrate**\n\n"
            f"| Metric | Value |\n|--------|-------|\n"
            f"| Cortical Columns | {ns['cortical_columns']} |\n"
            f"| Total Neurons | {ns['total_neurons']:,} |\n"
            f"| Total Synapses | {ns['total_synapses']:,} |\n"
            f"| Total Spikes | {ns['total_spikes']:,} |\n"
            f"| Avg Firing Rate | {ns['average_firing_rate']:.2f} Hz |"
        )
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_msg})
        yield history, ""
        return

    if cmd == "/memory":
        info = axiom.introspect()
        mem = info["memory"]
        bot_msg = (
            "**💾 Memory Systems**\n\n"
            f"| Type | Count |\n|------|-------|\n"
            f"| Working Memory | {mem['working']}/{CFG.working_memory_capacity} |\n"
            f"| Episodic (Hippocampus) | {mem['episodic']:,} |\n"
            f"| Semantic | {mem['semantic']:,} |\n"
            f"| Awake Replays | {mem['awake_replays']:,} |\n"
            f"| Sleep Replays | {mem['sleep_replays']:,} |"
        )
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_msg})
        yield history, ""
        return

    if cmd == "/consciousness":
        info = axiom.introspect()
        c = info["consciousness"]
        bot_msg = (
            "**✨ Consciousness**\n\n"
            f"| Metric | Value |\n|--------|-------|\n"
            f"| Awake | {'✓' if c['awake'] else '✗'} |\n"
            f"| Conscious Now | {'✓' if c['conscious_now'] else '✗'} |\n"
            f"| Ignition Events | {c['ignition_events']} |\n"
            f"| Workspace Size | {c['workspace_size']} |"
        )
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_msg})
        yield history, ""
        return

    if cmd == "/creativity":
        info = axiom.introspect()
        cr = info["creativity"]
        lines = [
            "**🎨 Creativity & Insights**\n",
            f"**Total Insights:** {cr['total_insights']}",
        ]
        if cr["recent_insights"]:
            lines.append("\n| Type | Distance | Age (min) |")
            lines.append("|------|----------|-----------|")
            for ins in cr["recent_insights"]:
                lines.append(
                    f"| {ins['type']} | {ins['distance']:.3f} | {ins['age_minutes']:.1f} |"
                )
        else:
            lines.append("\n*No insights detected yet.*")
        bot_msg = "\n".join(lines)
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_msg})
        yield history, ""
        return

    if cmd == "/self":
        info = axiom.introspect()
        sm = info["self_model"]
        traits = sm.get("traits", {})
        lines = [
            "**🪞 Self-Model & Metacognition**\n",
            f"**Confidence:** {sm.get('confidence', 0):.3f}",
            f"**Self-Awareness:** {sm.get('self_awareness', 0):.3f}",
            f"**Uncertainty:** {sm.get('uncertainty', 0):.3f}",
            "\n**Personality Traits:**\n",
            "| Trait | Value |",
            "|-------|-------|",
        ]
        for trait_name, trait_val in traits.items():
            bar_filled = int(trait_val * 10)
            bar = "█" * bar_filled + "░" * (10 - bar_filled)
            lines.append(f"| {trait_name} | `{bar}` {trait_val:.2f} |")
        bot_msg = "\n".join(lines)
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_msg})
        yield history, ""
        return

    if cmd == "/motivation":
        info = axiom.introspect()
        mot = info["motivation"]
        lines = [
            "**🎯 Intrinsic Motivation**\n",
            "| Component | Value |",
            "|-----------|-------|",
        ]
        for k, v in mot.items():
            if isinstance(v, (int, float)):
                bar_filled = int(min(1.0, max(0.0, float(v))) * 10)
                bar = "█" * bar_filled + "░" * (10 - bar_filled)
                lines.append(f"| {k} | `{bar}` {float(v):.3f} |")
        bot_msg = "\n".join(lines)
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_msg})
        yield history, ""
        return

    if cmd == "/neuromod":
        info = axiom.introspect()
        nm = info["neuromodulation"]
        lines = [
            "**💊 Neuromodulation**\n",
            "| Modulator | Level |",
            "|-----------|-------|",
        ]
        labels = {
            "dopamine": "Dopamine (DA)",
            "serotonin": "Serotonin (5-HT)",
            "norepinephrine": "Norepinephrine (NE)",
            "acetylcholine": "Acetylcholine (ACh)",
        }
        for key, label in labels.items():
            val = nm.get(key, 0.0)
            bar_filled = int(min(1.0, val) * 10)
            bar = "█" * bar_filled + "░" * (10 - bar_filled)
            lines.append(f"| {label} | `{bar}` {val:.3f} |")
        bot_msg = "\n".join(lines)
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_msg})
        yield history, ""
        return

    if cmd == "/criticality":
        info = axiom.introspect()
        crit = info["criticality"]
        ae = crit.get("avalanche_exponent")
        br = crit.get("branching_ratio")
        at_c = crit.get("at_criticality", False)
        bot_msg = (
            "**⚡ Self-Organized Criticality**\n\n"
            f"| Metric | Value |\n|--------|-------|\n"
            f"| Avalanche Exponent | {f'{ae:.3f}' if ae else 'N/A'} |\n"
            f"| Branching Ratio | {f'{br:.3f}' if br else 'N/A'} |\n"
            f"| At Criticality (σ≈1) | {'⚡ Yes' if at_c else 'No'} |"
        )
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_msg})
        yield history, ""
        return

    if cmd == "/performance":
        info = axiom.introspect()
        perf = info["performance"]
        lines = [
            "**📊 Performance Metrics**\n",
            "| Metric | Value |",
            "|--------|-------|",
        ]
        for k, v in perf.items():
            bar_filled = int(min(1.0, max(0.0, float(v))) * 10)
            bar = "█" * bar_filled + "░" * (10 - bar_filled)
            lines.append(f"| {k.replace('_', ' ').title()} | `{bar}` {float(v):.3f} |")
        bot_msg = "\n".join(lines)
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_msg})
        yield history, ""
        return

    if cmd.startswith("/dream"):
        parts = user_message.strip().split()
        minutes = float(parts[1]) if len(parts) > 1 else CFG.nrem_duration_minutes
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": f"💤 Entering dream state for {minutes:.1f} minutes..."})
        yield history, ""

        loop = asyncio.new_event_loop()
        try:
            result = loop.run_until_complete(axiom.sleep(minutes))
            bot_msg = (
                f"☀️ **Awakened from dream**\n\n"
                f"```json\n{json.dumps(result, indent=2, default=str)}\n```"
            )
        except Exception as e:
            bot_msg = f"❌ Dream cycle error: {e}"
        finally:
            loop.close()

        history[-1] = {"role": "assistant", "content": bot_msg}
        yield history, ""
        return

    if cmd.startswith("/checkpoint"):
        parts = user_message.strip().split(maxsplit=1)
        name = parts[1] if len(parts) > 1 else None
        path = axiom.save_checkpoint(name)
        bot_msg = f"💾 Checkpoint saved: `{path}`"
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_msg})
        yield history, ""
        return

    if cmd == "/analytics":
        from axiom_v1 import get_log
        log = get_log()
        uptime = time.time() - axiom.birth_time
        lines = [
            "**📈 Analytics Dashboard**\n",
            f"**Session:** `{axiom.session_id}`",
            f"**Uptime:** {uptime / 3600:.2f} hours",
            f"**Total Experiences:** {axiom.timestep}",
            "",
            "**Counters:**\n",
            "| Counter | Value |",
            "|---------|-------|",
        ]
        for name, val in sorted(log.counters.items()):
            lines.append(f"| {name} | {val:,} |")
        if log.timers:
            lines.append("\n**Average Timings:**\n")
            lines.append("| Operation | Avg (ms) |")
            lines.append("|-----------|----------|")
            for name, vals in sorted(log.timers.items()):
                if not name.endswith("_start") and vals:
                    import numpy as np
                    avg_ms = float(np.mean(vals)) * 1000
                    lines.append(f"| {name} | {avg_ms:.1f} |")
        bot_msg = "\n".join(lines)
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_msg})
        yield history, ""
        return

    if cmd == "/help":
        bot_msg = (
            "**📋 AXIOM Commands**\n\n"
            "| Command | Description |\n|---------|-------------|\n"
            "| `<text>` | Experience and learn |\n"
            "| `/introspect` | Complete system introspection (JSON) |\n"
            "| `/neural` | Neural substrate status |\n"
            "| `/memory` | Memory systems analysis |\n"
            "| `/consciousness` | Consciousness metrics |\n"
            "| `/creativity` | Creative insights & ideas |\n"
            "| `/self` | Self-model & metacognition |\n"
            "| `/motivation` | Intrinsic motivation state |\n"
            "| `/neuromod` | Neuromodulator levels |\n"
            "| `/criticality` | Self-organized criticality |\n"
            "| `/performance` | Performance metrics |\n"
            "| `/dream [minutes]` | Enter dream state |\n"
            "| `/checkpoint [name]` | Save brain state |\n"
            "| `/analytics` | View analytics dashboard |\n"
            "| `/help` | Show this help |"
        )
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_msg})
        yield history, ""
        return

    # ── Normal chat: process through AXIOM cognitive cycle ──
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": "⏳ Processing through cognitive architecture..."})
    yield history, ""

    try:
        result_holder = [None]
        error_holder = [None]
        token_queue = queue.Queue()

        def _bg_experience():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result_holder[0] = loop.run_until_complete(
                    axiom.experience(
                        user_message,
                        token_callback=lambda tok: token_queue.put(tok),
                    )
                )
            except Exception as e:
                error_holder[0] = e
            finally:
                token_queue.put(None)  # sentinel
                loop.close()

        bg_thread = threading.Thread(target=_bg_experience, daemon=True)
        bg_thread.start()

        # Stream tokens as they arrive
        partial_text = ""
        streaming_started = False
        while True:
            try:
                token = token_queue.get(timeout=0.15)
            except queue.Empty:
                if not bg_thread.is_alive():
                    break
                continue
            if token is None:
                break
            if not streaming_started:
                streaming_started = True
                partial_text = ""
            partial_text += token
            history[-1] = {"role": "assistant", "content": partial_text}
            yield history, ""

        bg_thread.join(timeout=600)

        if error_holder[0]:
            raise error_holder[0]

        if result_holder[0] is None:
            raise TimeoutError("Processing timed out after 10 minutes.")

        result = result_holder[0]

        # Use the streamed text if we got it, otherwise use the result
        llm_response = partial_text if streaming_started else (result.get("llm_response") or "")
        bot_msg = llm_response + "\n\n"

        # Metadata footer
        pred = result["prediction"]
        mem = result["memory"]
        cons = result["consciousness"]
        timing = result["timing"]

        bot_msg += (
            f"---\n"
            f"🔮 **Surprise:** {pred['surprise']:.3f} · "
            f"**Free Energy:** {pred['free_energy']:.3f}\n"
            f"💾 **Memory:** Retrieved {mem['retrieved_count']} · "
            f"Working {mem['working_memory_items']}/{CFG.working_memory_capacity} · "
            f"Episodic {mem['episodic_count']:,}\n"
            f"✨ **Consciousness (Φ):** {cons['level']:.3f} · "
            f"{'Conscious' if cons['is_conscious'] else 'Subconscious'}\n"
            f"⏱️ **Time:** {timing['total_ms']:.0f}ms"
        )

        if result["creativity"]["insight_detected"]:
            bot_msg += f" · 💡 **Insight detected!**"

    except Exception as e:
        bot_msg = f"❌ **Error:** {str(e)}"

    history[-1] = {"role": "assistant", "content": bot_msg}
    yield history, ""


# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR / PANEL REFRESH FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def refresh_system_info():
    axiom = get_axiom()
    info = axiom.introspect()
    ident = info["identity"]
    llm = info["llm"]
    lines = [
        f"**Version:** {ident['version']} ({ident['codename']})",
        f"**Session:** `{ident['session_id']}`",
        f"**Uptime:** {ident['age_hours']:.2f}h",
        f"**Experiences:** {ident['experiences']:,}",
        f"**LLM Backend:** {llm['backend']} ({'✓' if llm['available'] else '✗'})",
    ]
    return "\n\n".join(lines)


def refresh_neural_panel():
    axiom = get_axiom()
    info = axiom.introspect()
    ns = info["neural_substrate"]
    pc = info["predictive_coding"]
    crit = info["criticality"]
    ae = crit.get('avalanche_exponent')
    br = crit.get('branching_ratio')
    ae_str = f"{ae:.3f}" if ae is not None else "N/A"
    br_str = f"{br:.3f}" if br is not None else "N/A"
    return (
        f"### 🧬 Neural Substrate\n\n"
        f"| Metric | Value |\n|--------|-------|\n"
        f"| Columns | {ns['cortical_columns']} |\n"
        f"| Neurons | {ns['total_neurons']:,} |\n"
        f"| Synapses | {ns['total_synapses']:,} |\n"
        f"| Spikes | {ns['total_spikes']:,} |\n"
        f"| Avg Firing Rate | {ns['average_firing_rate']:.2f} Hz |\n"
        f"\n### 🔮 Predictive Coding\n\n"
        f"| Metric | Value |\n|--------|-------|\n"
        f"| Hierarchy Levels | {pc['hierarchy_levels']} |\n"
        f"| Free Energy | {pc['total_free_energy']:.4f} |\n"
        f"| Surprise | {pc['total_surprise']:.4f} |\n"
        f"\n### ⚡ Criticality\n\n"
        f"| Metric | Value |\n|--------|-------|\n"
        f"| Avalanche Exp. | {ae_str} |\n"
        f"| Branching Ratio | {br_str} |\n"
        f"| At Criticality | {'⚡ Yes' if crit['at_criticality'] else 'No'} |"
    )


def refresh_memory_panel():
    axiom = get_axiom()
    info = axiom.introspect()
    mem = info["memory"]
    return (
        f"| Type | Count |\n|------|-------|\n"
        f"| Working Memory | {mem['working']}/{CFG.working_memory_capacity} |\n"
        f"| Episodic | {mem['episodic']:,} |\n"
        f"| Semantic | {mem['semantic']:,} |\n"
        f"| Awake Replays | {mem['awake_replays']:,} |\n"
        f"| Sleep Replays | {mem['sleep_replays']:,} |"
    )


def refresh_consciousness_panel():
    axiom = get_axiom()
    info = axiom.introspect()
    c = info["consciousness"]
    return (
        f"| Metric | Value |\n|--------|-------|\n"
        f"| Awake | {'✓ Yes' if c['awake'] else '✗ No'} |\n"
        f"| Conscious Now | {'✓ Yes' if c['conscious_now'] else '✗ No'} |\n"
        f"| Ignition Events | {c['ignition_events']} |\n"
        f"| Workspace Size | {c['workspace_size']} |"
    )


def refresh_motivation_panel():
    axiom = get_axiom()
    info = axiom.introspect()
    mot = info["motivation"]
    lines = ["| Component | Value |", "|-----------|-------|"]
    for k, v in mot.items():
        if isinstance(v, (int, float)):
            val = min(1.0, max(0.0, float(v)))
            bar_filled = int(val * 10)
            bar = "█" * bar_filled + "░" * (10 - bar_filled)
            lines.append(f"| {k} | `{bar}` {float(v):.3f} |")
    return "\n".join(lines)


def refresh_creativity_panel():
    axiom = get_axiom()
    info = axiom.introspect()
    cr = info["creativity"]
    lines = [f"**Total Insights:** {cr['total_insights']}\n"]
    if cr["recent_insights"]:
        lines.append("| Type | Distance | Age (min) |")
        lines.append("|------|----------|-----------|")
        for ins in cr["recent_insights"]:
            lines.append(
                f"| {ins['type']} | {ins['distance']:.3f} | {ins['age_minutes']:.1f} |"
            )
    else:
        lines.append("*No insights detected yet. Keep interacting!*")
    return "\n".join(lines)


def refresh_self_model_panel():
    axiom = get_axiom()
    info = axiom.introspect()
    sm = info["self_model"]
    traits = sm.get("traits", {})

    lines = [
        f"**Confidence:** {sm.get('confidence', 0):.3f}",
        f"**Self-Awareness:** {sm.get('self_awareness', 0):.3f}",
        f"**Uncertainty:** {sm.get('uncertainty', 0):.3f}",
        "",
        "### Personality Traits\n",
        "| Trait | Value |",
        "|-------|-------|",
    ]
    for trait_name, trait_val in traits.items():
        bar_filled = int(min(1.0, float(trait_val)) * 10)
        bar = "█" * bar_filled + "░" * (10 - bar_filled)
        lines.append(f"| {trait_name.title()} | `{bar}` {trait_val:.2f} |")

    # Narrative
    narrative = sm.get("narrative_length", 0)
    sig_events = sm.get("significant_events", 0)
    lines.append(f"\n**Narrative entries:** {narrative}")
    lines.append(f"**Significant events:** {sig_events}")

    return "\n".join(lines)


def refresh_neuromod_panel():
    axiom = get_axiom()
    info = axiom.introspect()
    nm = info["neuromodulation"]
    labels = {
        "dopamine": "Dopamine (DA)",
        "serotonin": "Serotonin (5-HT)",
        "norepinephrine": "Norepinephrine (NE)",
        "acetylcholine": "Acetylcholine (ACh)",
    }
    lines = ["| Modulator | Level |", "|-----------|-------|"]
    for key, label in labels.items():
        val = nm.get(key, 0.0)
        bar_filled = int(min(1.0, val) * 10)
        bar = "█" * bar_filled + "░" * (10 - bar_filled)
        lines.append(f"| {label} | `{bar}` {val:.3f} |")
    return "\n".join(lines)


def refresh_performance_panel():
    axiom = get_axiom()
    info = axiom.introspect()
    perf = info["performance"]
    dreams = info["dreams"]
    lines = [
        "### 📊 Performance\n",
        "| Metric | Value |",
        "|--------|-------|",
    ]
    for k, v in perf.items():
        bar_filled = int(min(1.0, max(0.0, float(v))) * 10)
        bar = "█" * bar_filled + "░" * (10 - bar_filled)
        lines.append(f"| {k.replace('_', ' ').title()} | `{bar}` {float(v):.3f} |")

    lines.append(f"\n### 💤 Dreams\n")
    lines.append(f"**Total Dreams:** {dreams['total_dreams']}")
    if dreams["last_dream"]:
        lines.append(f"\n**Last Dream:**\n```json\n{json.dumps(dreams['last_dream'], indent=2, default=str)}\n```")

    return "\n".join(lines)


def do_save_checkpoint():
    axiom = get_axiom()
    try:
        path = axiom.save_checkpoint()
        return f"✅ Saved: `{path}`"
    except Exception as e:
        return f"❌ Failed: {e}"


def do_dream(minutes_str: str):
    """Trigger a dream cycle."""
    axiom = get_axiom()
    try:
        minutes = float(minutes_str) if minutes_str.strip() else CFG.nrem_duration_minutes
    except ValueError:
        minutes = CFG.nrem_duration_minutes

    loop = asyncio.new_event_loop()
    try:
        result = loop.run_until_complete(axiom.sleep(minutes))
        return f"☀️ **Dream complete!**\n\n```json\n{json.dumps(result, indent=2, default=str)}\n```"
    except Exception as e:
        return f"❌ Dream error: {e}"
    finally:
        loop.close()


# ═══════════════════════════════════════════════════════════════════════════
# BUILD GRADIO INTERFACE
# ═══════════════════════════════════════════════════════════════════════════

def build_ui() -> gr.Blocks:
    # Dependency status
    deps_items = []
    for name, key in [
        ("NumPy", "numpy"),
        ("PyTorch", "torch"),
        ("Transformers", "transformers"),
        ("OpenAI", "openai"),
        ("Anthropic", "anthropic"),
        ("llama.cpp", "llama_cpp"),
    ]:
        ok = DEPS.get(key, False)
        deps_items.append(f"{'✓' if ok else '✗'} {name}")
    deps_str = "  ·  ".join(deps_items)

    with gr.Blocks(
        title=f"🌌 AXIOM v{VERSION}",
    ) as app:
        # ── Header ──
        gr.Markdown(
            f"""
            <div class="main-header">
            <h1>🌌 AXIOM v{VERSION}</h1>
            <p><em>Adaptive eXemplary Intelligence Operating Matrix</em></p>
            <p style="font-size:0.85em; opacity:0.7;">{deps_str}  ·  Data: <code>{HOME}</code></p>
            </div>
            """,
        )

        with gr.Row():
            # ════════════════════ LEFT: Chat ════════════════════
            with gr.Column(scale=4):
                chatbot = gr.Chatbot(
                    label="AXIOM Chat",
                    height=650,
                    placeholder="Nhập câu hỏi hoặc /help để xem commands…",
                )

                with gr.Row():
                    msg_input = gr.Textbox(
                        placeholder="Hỏi AXIOM bất cứ điều gì… (Enter để gửi)",
                        show_label=False,
                        scale=5,
                        lines=1,
                        max_lines=3,
                    )
                    send_btn = gr.Button("Gửi 🌌", variant="primary", scale=1)

                with gr.Row():
                    clear_btn = gr.Button("🗑 Xoá chat", size="sm")
                    save_btn = gr.Button("💾 Save checkpoint", size="sm")
                    dream_minutes = gr.Textbox(
                        value="5",
                        label="",
                        show_label=False,
                        scale=0,
                        max_lines=1,
                        placeholder="min",
                        elem_classes=["dream-input"],
                    )
                    dream_btn = gr.Button("💤 Dream", size="sm")

                save_status = gr.Markdown("")

            # ════════════════════ RIGHT: Panels ════════════════════
            with gr.Column(scale=2):
                with gr.Tabs():
                    with gr.Tab("📊 System"):
                        system_md = gr.Markdown("*Loading…*")
                        refresh_sys_btn = gr.Button("🔄 Refresh", size="sm")

                    with gr.Tab("🧬 Neural"):
                        neural_md = gr.Markdown("*Loading…*")
                        refresh_neural_btn = gr.Button("🔄 Refresh", size="sm")

                    with gr.Tab("💾 Memory"):
                        memory_md = gr.Markdown("*Loading…*")
                        refresh_mem_btn = gr.Button("🔄 Refresh", size="sm")

                    with gr.Tab("✨ Consciousness"):
                        consciousness_md = gr.Markdown("*Loading…*")
                        refresh_cons_btn = gr.Button("🔄 Refresh", size="sm")

                    with gr.Tab("🎯 Motivation"):
                        motivation_md = gr.Markdown("*Loading…*")
                        refresh_mot_btn = gr.Button("🔄 Refresh", size="sm")

                    with gr.Tab("🎨 Creativity"):
                        creativity_md = gr.Markdown("*Loading…*")
                        refresh_cre_btn = gr.Button("🔄 Refresh", size="sm")

                    with gr.Tab("🪞 Self-Model"):
                        self_model_md = gr.Markdown("*Loading…*")
                        refresh_self_btn = gr.Button("🔄 Refresh", size="sm")

                    with gr.Tab("💊 Neuromod"):
                        neuromod_md = gr.Markdown("*Loading…*")
                        refresh_nm_btn = gr.Button("🔄 Refresh", size="sm")

                    with gr.Tab("📈 Performance"):
                        performance_md = gr.Markdown("*Loading…*")
                        refresh_perf_btn = gr.Button("🔄 Refresh", size="sm")

        # ── Footer ──
        gr.Markdown(
            f"<p style='text-align:center; opacity:0.5; font-size:0.8em;'>"
            f"🌌 AXIOM {VERSION} · {CODENAME} · Build {BUILD_DATE} · "
            f"\"The Foundation of Next-Generation Cognitive Systems\"</p>"
        )

        # ────────────────── Event bindings ──────────────────

        # Chat
        msg_input.submit(chat_respond, [msg_input, chatbot], [chatbot, msg_input])
        send_btn.click(chat_respond, [msg_input, chatbot], [chatbot, msg_input])
        clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg_input])

        # Save & Dream
        save_btn.click(do_save_checkpoint, outputs=[save_status])
        dream_btn.click(do_dream, inputs=[dream_minutes], outputs=[save_status])

        # Panel refreshes
        refresh_sys_btn.click(refresh_system_info, outputs=[system_md])
        refresh_neural_btn.click(refresh_neural_panel, outputs=[neural_md])
        refresh_mem_btn.click(refresh_memory_panel, outputs=[memory_md])
        refresh_cons_btn.click(refresh_consciousness_panel, outputs=[consciousness_md])
        refresh_mot_btn.click(refresh_motivation_panel, outputs=[motivation_md])
        refresh_cre_btn.click(refresh_creativity_panel, outputs=[creativity_md])
        refresh_self_btn.click(refresh_self_model_panel, outputs=[self_model_md])
        refresh_nm_btn.click(refresh_neuromod_panel, outputs=[neuromod_md])
        refresh_perf_btn.click(refresh_performance_panel, outputs=[performance_md])

        # Auto-refresh panels on page load
        app.load(refresh_system_info, outputs=[system_md])
        app.load(refresh_neural_panel, outputs=[neural_md])
        app.load(refresh_memory_panel, outputs=[memory_md])
        app.load(refresh_consciousness_panel, outputs=[consciousness_md])
        app.load(refresh_motivation_panel, outputs=[motivation_md])
        app.load(refresh_creativity_panel, outputs=[creativity_md])
        app.load(refresh_self_model_panel, outputs=[self_model_md])
        app.load(refresh_neuromod_panel, outputs=[neuromod_md])
        app.load(refresh_performance_panel, outputs=[performance_md])

    return app


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print(f"\n{SYMBOL} AXIOM v{VERSION} — Web UI")
    print(f"Data: {HOME}\n")

    # Pre-init AXIOM so neural substrate builds before UI opens
    print("Loading AXIOM cognitive architecture (this may take a moment)…")
    get_axiom()
    print("✓ AXIOM ready!\n")

    app = build_ui()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        inbrowser=True,
        show_error=True,
        share=False,
        theme=gr.themes.Soft(
            primary_hue="indigo",
            secondary_hue="purple",
            neutral_hue="slate",
            font=["Inter", "system-ui", "sans-serif"],
        ),
        css="""
        .main-header { text-align: center; margin-bottom: 0.5em; }
        .panel-title { font-size: 1.1em; font-weight: 600; margin-bottom: 0.3em; }
        footer { display: none !important; }
        .gradio-container { max-width: 100% !important; padding: 0 1em !important; }
        """,
    )


if __name__ == "__main__":
    main()
