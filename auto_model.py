"""
AXIOM v1.0 - Auto Model Finder & Configurator
Detects system specs, searches for LLM models (GGUF / HuggingFace),
recommends the best fit, and optionally downloads one.

Usage:
    python auto_model.py            Interactive mode
    python auto_model.py --auto     Non-interactive (picks best available)
    python auto_model.py --rescan   Force re-scan even if model_config.bat exists
"""

import ctypes
import datetime
import glob
import os
import platform
import struct
import sys

# ── Recommended GGUF models (HuggingFace repos) ────────────────────────────
RECOMMENDED_GGUF = [
    {
        "label": "Qwen2.5-7B-Instruct-Q4_K_M",
        "repo_id": "Qwen/Qwen2.5-7B-Instruct-GGUF",
        "filename": "qwen2.5-7b-instruct-q4_k_m.gguf",
        "size_gb": 4.4,
        "min_ram_gb": 10,
        "quality": 3,
        "desc": "7B Q4_K_M  — best quality for 16 GB+ RAM",
    },
    {
        "label": "Qwen2.5-3B-Instruct-Q4_K_M",
        "repo_id": "Qwen/Qwen2.5-3B-Instruct-GGUF",
        "filename": "qwen2.5-3b-instruct-q4_k_m.gguf",
        "size_gb": 2.0,
        "min_ram_gb": 6,
        "quality": 2,
        "desc": "3B Q4_K_M  — good balance for 8 GB+ RAM",
    },
    {
        "label": "Qwen2.5-1.5B-Instruct-Q4_K_M",
        "repo_id": "Qwen/Qwen2.5-1.5B-Instruct-GGUF",
        "filename": "qwen2.5-1.5b-instruct-q4_k_m.gguf",
        "size_gb": 1.0,
        "min_ram_gb": 4,
        "quality": 1,
        "desc": "1.5B Q4_K_M — lightweight, fits 4 GB+ RAM",
    },
]

RECOMMENDED_HF = [
    {
        "label": "Qwen/Qwen2.5-3B-Instruct",
        "model_id": "Qwen/Qwen2.5-3B-Instruct",
        "size_gb": 6.5,
        "min_vram_gb": 6,
        "quality": 2,
        "desc": "3B GPU  — needs 6 GB+ VRAM (CUDA)",
    },
    {
        "label": "Qwen/Qwen2.5-1.5B-Instruct",
        "model_id": "Qwen/Qwen2.5-1.5B-Instruct",
        "size_gb": 3.2,
        "min_vram_gb": 4,
        "quality": 1,
        "desc": "1.5B GPU — needs 4 GB+ VRAM (CUDA)",
    },
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "model_config.bat")


# ── System detection ────────────────────────────────────────────────────────

def get_ram_gb():
    """Return total physical RAM in GB (Windows)."""
    try:
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]
        stat = MEMORYSTATUSEX(dwLength=ctypes.sizeof(MEMORYSTATUSEX))
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
        return round(stat.ullTotalPhys / (1024 ** 3), 1)
    except Exception:
        return 0.0


def get_gpu_info():
    """Return (has_cuda, gpu_name, vram_gb)."""
    try:
        import torch
        if torch.cuda.is_available():
            name = torch.cuda.get_device_name(0)
            vram = round(torch.cuda.get_device_properties(0).total_mem / (1024 ** 3), 1)
            return True, name, vram
    except Exception:
        pass
    return False, None, 0.0


def get_system_info():
    info = {
        "cpu": platform.processor() or "Unknown CPU",
        "cores": os.cpu_count() or 4,
        "ram_gb": get_ram_gb(),
        "has_cuda": False,
        "gpu_name": None,
        "vram_gb": 0.0,
    }
    info["has_cuda"], info["gpu_name"], info["vram_gb"] = get_gpu_info()
    return info


# ── Model search ────────────────────────────────────────────────────────────

def _candidate_dirs():
    """Return a list of directories to search for .gguf files."""
    dirs = [
        os.path.join(SCRIPT_DIR, "models"),
        SCRIPT_DIR,
    ]
    home = os.path.expanduser("~")
    dirs.append(os.path.join(home, "models"))
    dirs.append(os.path.join(home, ".cache", "llama.cpp"))

    # Check common drive roots on Windows
    if platform.system() == "Windows":
        for drive in "CDEFGH":
            d = f"{drive}:\\models"
            if os.path.isdir(d):
                dirs.append(d)

    return [d for d in dirs if os.path.isdir(d)]


def search_gguf_models():
    """Search for .gguf files in common locations."""
    found = []
    seen = set()
    for d in _candidate_dirs():
        for path in glob.glob(os.path.join(d, "**", "*.gguf"), recursive=True):
            real = os.path.realpath(path)
            if real not in seen:
                seen.add(real)
                try:
                    size_gb = round(os.path.getsize(real) / (1024 ** 3), 2)
                except OSError:
                    continue
                found.append({
                    "name": os.path.basename(real),
                    "path": real,
                    "size_gb": size_gb,
                })
    return sorted(found, key=lambda m: -m["size_gb"])


def search_hf_cached_models():
    """Search for HuggingFace cached models."""
    cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
    if not os.path.isdir(cache_dir):
        return []

    models = []
    for entry in os.listdir(cache_dir):
        if not entry.startswith("models--"):
            continue
        model_name = entry.replace("models--", "").replace("--", "/")
        model_path = os.path.join(cache_dir, entry)
        total = 0
        for root, _dirs, files in os.walk(model_path):
            for f in files:
                try:
                    total += os.path.getsize(os.path.join(root, f))
                except OSError:
                    pass
        size_gb = round(total / (1024 ** 3), 2)
        if size_gb >= 0.5:
            models.append({"name": model_name, "path": model_path, "size_gb": size_gb})
    return sorted(models, key=lambda m: -m["size_gb"])


def check_package(name):
    """Check if a Python package is importable."""
    try:
        __import__(name)
        return True
    except ImportError:
        return False


# ── Recommendation ──────────────────────────────────────────────────────────

def get_recommendations(ram_gb, has_cuda, vram_gb):
    """Return (gguf_recs, hf_recs) that fit the user's hardware."""
    has_llama = check_package("llama_cpp")
    has_transformers = check_package("transformers") and check_package("torch")

    gguf_recs = []
    if has_llama:
        usable_ram = ram_gb * 0.6
        for m in RECOMMENDED_GGUF:
            if usable_ram >= m["min_ram_gb"]:
                gguf_recs.append(m)

    hf_recs = []
    if has_transformers and has_cuda:
        for m in RECOMMENDED_HF:
            if vram_gb >= m["min_vram_gb"]:
                hf_recs.append(m)

    return gguf_recs, hf_recs


# ── Download ────────────────────────────────────────────────────────────────

def download_gguf(repo_id, filename, dest_dir):
    """Download a GGUF model file. Returns local path or None."""
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, filename)

    if os.path.isfile(dest_path):
        print(f"    Already exists: {dest_path}")
        return dest_path

    # Prefer huggingface_hub (supports resume, progress)
    try:
        from huggingface_hub import hf_hub_download
        print(f"    Downloading {filename} from {repo_id} ...")
        print(f"    Destination: {dest_dir}")
        print(f"    (this may take several minutes)")
        path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=dest_dir,
        )
        return path
    except ImportError:
        pass

    # Fallback: raw urllib download
    url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
    print(f"    Downloading from {url}")
    print(f"    Destination: {dest_path}")
    print(f"    (this may take several minutes)")
    try:
        import urllib.request

        def _progress(block, block_size, total):
            done = block * block_size
            if total > 0:
                pct = min(100.0, done / total * 100)
                print(f"\r    [{pct:5.1f}%] {done / 1e6:.0f} / {total / 1e6:.0f} MB",
                      end="", flush=True)

        urllib.request.urlretrieve(url, dest_path, reporthook=_progress)
        print()
        return dest_path
    except Exception as exc:
        print(f"\n    Download failed: {exc}")
        if os.path.isfile(dest_path):
            os.remove(dest_path)
        return None


# ── Config writer ───────────────────────────────────────────────────────────

def write_config(backend, model_path=None, model_name=None,
                 ctx_window=4096, max_tokens=512):
    """Write model_config.bat used by run.bat / run_ui.bat."""
    lines = [
        "@echo off",
        f":: Auto-generated by auto_model.py on "
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f":: Re-run:  python auto_model.py --rescan",
        "",
        f"set AXIOM_LLM_BACKEND={backend}",
    ]
    if backend == "local_llama" and model_path:
        lines.append(f"set AXIOM_LLAMA_MODEL_PATH={model_path}")
        lines.append(f"set AXIOM_LLM_CTX_WINDOW={ctx_window}")
        lines.append(f"set AXIOM_LLM_MAX_TOKENS={max_tokens}")
    elif backend == "transformers_local" and model_name:
        lines.append(f"set AXIOM_TRANSFORMERS_MODEL={model_name}")
        lines.append(f"set AXIOM_LLM_MAX_TOKENS={max_tokens}")

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\n  Config saved: {CONFIG_FILE}")


# ── Interactive menu ────────────────────────────────────────────────────────

def _print_header():
    print()
    print("=" * 62)
    print("  AXIOM v1.0 — Auto Model Finder & Configurator")
    print("=" * 62)


def run_interactive(info, gguf_found, hf_found, gguf_recs, hf_recs):
    """Present choices and let user pick."""
    # Build unified option list
    options = []  # (label, action_fn)

    # --- Existing models on disk ---
    if gguf_found:
        print(f"\n  Found {len(gguf_found)} GGUF model(s) on disk:")
        for m in gguf_found:
            idx = len(options) + 1
            print(f"    [{idx}] USE  {m['name']}  ({m['size_gb']} GB)")
            print(f"         {m['path']}")
            options.append(("gguf_local", m))

    if hf_found:
        print(f"\n  Found {len(hf_found)} HuggingFace cached model(s):")
        for m in hf_found:
            idx = len(options) + 1
            print(f"    [{idx}] USE  {m['name']}  ({m['size_gb']} GB)")
            options.append(("hf_local", m))

    # --- Downloadable models ---
    # Filter out models that are already found on disk
    found_names = {m["name"].lower() for m in gguf_found}
    download_recs = [r for r in gguf_recs
                     if r["filename"].lower() not in found_names]

    if download_recs:
        print(f"\n  Recommended downloads (for {info['ram_gb']} GB RAM):")
        for rec in download_recs:
            idx = len(options) + 1
            print(f"    [{idx}] DOWNLOAD  {rec['label']}  ({rec['size_gb']} GB)")
            print(f"         {rec['desc']}")
            options.append(("download_gguf", rec))

    found_hf_names = {m["name"].lower() for m in hf_found}
    hf_dl_recs = [r for r in hf_recs
                  if r["model_id"].lower() not in found_hf_names]
    if hf_dl_recs:
        print(f"\n  HuggingFace GPU models (auto-download at runtime):")
        for rec in hf_dl_recs:
            idx = len(options) + 1
            print(f"    [{idx}] SELECT  {rec['label']}  — {rec['desc']}")
            options.append(("select_hf", rec))

    print(f"\n    [0] No LLM (pure cognitive simulation)")

    if not options:
        print("\n  No models found and no downloads available.")
        print("  AXIOM will run in pure simulation mode.")
        write_config("none")
        return

    print()
    default = "1"
    try:
        choice = input(f"  Choose [{default}]: ").strip() or default
    except (EOFError, KeyboardInterrupt):
        choice = "0"

    if choice == "0":
        write_config("none")
        print("  AXIOM will run in pure simulation mode (no LLM).")
        return

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
        print("  Invalid choice — defaulting to [1].")
        choice = "1"

    action, data = options[int(choice) - 1]

    if action == "gguf_local":
        write_config("local_llama", model_path=data["path"])
    elif action == "hf_local":
        write_config("transformers_local", model_name=data["name"])
    elif action == "download_gguf":
        models_dir = os.path.join(SCRIPT_DIR, "models")
        path = download_gguf(data["repo_id"], data["filename"], models_dir)
        if path:
            write_config("local_llama", model_path=path)
        else:
            print("  Download failed. You can retry later: python auto_model.py")
            write_config("none")
    elif action == "select_hf":
        write_config("transformers_local", model_name=data["model_id"])
        print(f"  Model will be downloaded automatically on first run.")


def run_auto(info, gguf_found, hf_found, gguf_recs, hf_recs):
    """Non-interactive: pick best model automatically."""
    # Prefer existing GGUF on disk (biggest = best quality)
    if gguf_found:
        best = gguf_found[0]
        print(f"\n  Auto-selected: {best['name']} ({best['size_gb']} GB)")
        write_config("local_llama", model_path=best["path"])
        return

    # Prefer existing HF cached model
    if hf_found and info["has_cuda"]:
        best = hf_found[0]
        print(f"\n  Auto-selected: {best['name']} ({best['size_gb']} GB)")
        write_config("transformers_local", model_name=best["name"])
        return

    # Download best fitting GGUF
    if gguf_recs:
        rec = gguf_recs[0]  # highest quality that fits
        print(f"\n  Auto-downloading: {rec['label']} ({rec['size_gb']} GB)")
        models_dir = os.path.join(SCRIPT_DIR, "models")
        path = download_gguf(rec["repo_id"], rec["filename"], models_dir)
        if path:
            write_config("local_llama", model_path=path)
            return

    # Select HF model (will download at runtime)
    if hf_recs:
        rec = hf_recs[0]
        print(f"\n  Auto-selected HF model: {rec['model_id']}")
        write_config("transformers_local", model_name=rec["model_id"])
        return

    print("\n  No suitable model found. Running in pure simulation mode.")
    write_config("none")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    auto_mode = "--auto" in sys.argv
    rescan = "--rescan" in sys.argv

    # Skip if config already exists (unless --rescan)
    if os.path.isfile(CONFIG_FILE) and not rescan and not auto_mode:
        print(f"\n  model_config.bat already exists.")
        try:
            ans = input("  Reconfigure? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            ans = "n"
        if ans != "y":
            print("  Keeping existing config. Use --rescan to force.")
            return

    _print_header()

    # Step 1: System info
    print("\n  [1/4] Detecting system specs...")
    info = get_system_info()
    print(f"    CPU:   {info['cpu']}  ({info['cores']} cores)")
    print(f"    RAM:   {info['ram_gb']} GB")
    if info["has_cuda"]:
        print(f"    GPU:   {info['gpu_name']}  ({info['vram_gb']} GB VRAM, CUDA)")
    else:
        print(f"    GPU:   No CUDA detected — will use CPU inference")

    # Step 2: Search GGUF
    print("\n  [2/4] Searching for GGUF models...")
    gguf_found = search_gguf_models()
    if not gguf_found:
        print("    (none found)")

    # Step 3: Search HF cache
    print("\n  [3/4] Searching HuggingFace cache...")
    hf_found = search_hf_cached_models()
    if not hf_found:
        print("    (none found)")

    # Step 4: Recommendations
    print("\n  [4/4] Generating recommendations...")
    gguf_recs, hf_recs = get_recommendations(
        info["ram_gb"], info["has_cuda"], info["vram_gb"]
    )

    # Choose
    if auto_mode:
        run_auto(info, gguf_found, hf_found, gguf_recs, hf_recs)
    else:
        run_interactive(info, gguf_found, hf_found, gguf_recs, hf_recs)

    print()
    print("=" * 62)
    print("  Done! Run AXIOM with:  run.bat  or  run_ui.bat")
    print("=" * 62)
    print()


if __name__ == "__main__":
    main()
