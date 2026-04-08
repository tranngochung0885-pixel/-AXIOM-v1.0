# 🌌 AXIOM v1.0 - Adaptive eXemplary Intelligence Operating Matrix

> "The Foundation of Next-Generation Cognitive Systems"

## Yêu cầu hệ thống

| Thành phần | Tối thiểu | Máy bạn |
|---|---|---|
| OS | Windows 10/11 64-bit | ✅ Windows 64-bit |
| Python | 3.11+ | Cần cài đặt |
| RAM | 8 GB | ✅ 16 GB |
| CPU | 4 cores | ✅ AMD Ryzen 5 7535HS |
| GPU | Không bắt buộc | AMD Radeon 4GB (dùng CPU mode) |

> **Lưu ý:** AMD Radeon trên Windows không hỗ trợ CUDA nên PyTorch sẽ chạy ở chế độ CPU.
> Với 16GB RAM, hệ thống vẫn chạy tốt các model local nhỏ (3B-7B quantized).

---

## Cài đặt nhanh

### Bước 1: Cài Python 3.11+

Nếu chưa có Python, tải từ: https://www.python.org/downloads/

⚠️ **Quan trọng:** Khi cài đặt, tick vào **"Add Python to PATH"**.

### Bước 2: Chạy Setup

```
Double-click: setup.bat
```

Script sẽ tự động:
- Tạo virtual environment (`.venv`)
- Cài PyTorch (CPU version)
- Cài tất cả dependencies (numpy, openai, anthropic, transformers, llama-cpp-python)

### Bước 3: Chạy AXIOM

Có 2 chế độ:

```
Double-click: run.bat        ← CLI (terminal)
Double-click: run_ui.bat     ← Web UI (mở trình duyệt tại http://localhost:7860)
```

**Khuyến nghị dùng Web UI** (`run_ui.bat`) để có trải nghiệm trực quan hơn với các panel theo dõi real-time.

---

## Cấu hình LLM Backend

AXIOM hỗ trợ 5 chế độ LLM. Chỉnh sửa trong `run.bat` hoặc `run_ui.bat`:

### 🔹 Option 0: Không dùng LLM (mặc định)

```bat
set AXIOM_LLM_BACKEND=none
```

AXIOM chạy ở chế độ **cognitive simulation thuần** — không cần tải model nào.

### 🔹 Option 1: Local llama.cpp (khuyên dùng cho máy bạn)

**Bước 1:** Tải model GGUF (khuyên dùng cho 16GB RAM):

| Model | Size | Link |
|---|---|---|
| Qwen2.5-3B-Instruct-Q4_K_M | ~2 GB | [HuggingFace](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF) |
| Qwen2.5-7B-Instruct-Q4_K_M | ~4.5 GB | [HuggingFace](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF) |

**Bước 2:** Đặt file `.gguf` vào thư mục, ví dụ `D:\models\`

**Bước 3:** Sửa `run.bat`, bỏ comment (xóa `::`) các dòng Option 1:

```bat
set AXIOM_LLM_BACKEND=local_llama
set AXIOM_LLAMA_MODEL_PATH=D:\models\Qwen2.5-3B-Instruct-Q4_K_M.gguf
set AXIOM_LLM_CTX_WINDOW=2048
set AXIOM_LLM_MAX_TOKENS=512
```

### 🔹 Option 2: OpenAI API

```bat
set AXIOM_LLM_BACKEND=openai_http
set OPENAI_API_KEY=sk-your-key-here
set AXIOM_OPENAI_MODEL=gpt-4.1-mini
```

### 🔹 Option 3: Anthropic API

```bat
set AXIOM_LLM_BACKEND=anthropic_http
set ANTHROPIC_API_KEY=sk-ant-your-key-here
set AXIOM_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### 🔹 Option 4: HuggingFace Transformers (local)

```bat
set AXIOM_LLM_BACKEND=transformers_local
set AXIOM_TRANSFORMERS_MODEL=Qwen/Qwen2.5-3B-Instruct
```

> ⚠️ Option 4 sẽ tải model về từ HuggingFace (~6-14 GB) và load vào RAM.
> Với 16GB RAM, chỉ nên dùng model 3B.

---

## Web UI (Gradio)

Chạy `run_ui.bat` hoặc:

```bash
python axiom_ui.py
```

Mở trình duyệt tại **http://localhost:7860**

### Giao diện gồm:

**Bên trái:** Chat với AXIOM (hỗ trợ tất cả slash commands + nhập text tự do)

**Bên phải:** 9 panel theo dõi real-time:

| Tab | Nội dung |
|-----|----------|
| 📊 System | Version, session, uptime, LLM backend |
| 🧬 Neural | Cortical columns, neurons, synapses, spikes, predictive coding, criticality |
| 💾 Memory | Working/Episodic/Semantic memory, replay counts |
| ✨ Consciousness | Global workspace, ignition events, conscious state |
| 🎯 Motivation | Curiosity, competence, novelty, learning progress |
| 🎨 Creativity | Insight detection, conceptual distances |
| 🪞 Self-Model | Personality traits, confidence, self-awareness, narrative |
| 💊 Neuromod | Dopamine, Serotonin, Norepinephrine, Acetylcholine |
| 📈 Performance | Prediction accuracy, learning efficiency, creativity score, dreams |

**Nút bấm:** Save checkpoint, Dream (nhập số phút), Xoá chat

---

## Các lệnh trong AXIOM CLI

| Lệnh | Mô tả |
|---|---|
| `<text>` | Nhập text để hệ thống xử lý và học |
| `/introspect` | Xem toàn bộ trạng thái hệ thống |
| `/neural` | Trạng thái neural substrate |
| `/memory` | Phân tích hệ thống bộ nhớ |
| `/consciousness` | Metrics về consciousness |
| `/creativity` | Creative insights & ideas |
| `/self` | Self-model & metacognition |
| `/motivation` | Trạng thái intrinsic motivation |
| `/neuromod` | Mức neuromodulator |
| `/criticality` | Phân tích self-organized criticality |
| `/performance` | Performance metrics |
| `/dream [minutes]` | Vào trạng thái dream |
| `/checkpoint [name]` | Lưu brain state |
| `/analytics` | Xem analytics dashboard |
| `/quit` | Tắt hệ thống |

---

## Cấu trúc thư mục

```
AXIOM v1/
├── axiom_v1.py          # Source code chính (cognitive engine)
├── axiom_ui.py          # Gradio Web UI
├── requirements.txt     # Dependencies
├── setup.bat            # Script cài đặt tự động
├── run.bat              # Script chạy AXIOM (CLI)
├── run_ui.bat           # Script chạy Web UI
├── README.md            # File này
└── .venv/               # Virtual environment (tạo bởi setup.bat)
```

AXIOM lưu dữ liệu tại `~/.axiom/` (thư mục user home):

```
~/.axiom/
├── logs/           # Log files
├── memories/       # Memory storage
├── dreams/         # Dream states
├── insights/       # Generated insights
├── checkpoints/    # Brain state snapshots
└── analytics/      # Analytics data
```

---

## Troubleshooting

### "Python not found"
→ Cài Python 3.11+ và tick "Add Python to PATH". Restart terminal sau khi cài.

### "pip install torch bị lỗi"
→ PyTorch CPU version khá lớn (~200MB). Đảm bảo có kết nối internet ổn định.

### "llama-cpp-python cài lỗi"
→ Cần có C++ Build Tools. Cài từ: https://visualstudio.microsoft.com/visual-cpp-build-tools/
→ Chọn "Desktop development with C++" workload.

### "AXIOM chạy chậm khi dùng LLM"
→ Bình thường khi chạy model local trên CPU. Model 3B sẽ nhanh hơn 7B.
→ Giảm `AXIOM_LLM_CTX_WINDOW` và `AXIOM_LLM_MAX_TOKENS` để tăng tốc.

### "Không đủ RAM khi load model"
→ Dùng model nhỏ hơn (3B thay vì 7B) hoặc chạy ở chế độ `none`.

---

## License

MIT
