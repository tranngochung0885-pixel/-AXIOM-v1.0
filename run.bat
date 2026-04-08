@echo off
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
title AXIOM v1.0

:: ── Activate venv ────────────────────────────────────────────
if not exist .venv\Scripts\activate.bat (
    echo ERROR: Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat

:: ══════════════════════════════════════════════════════════════
::  LLM MODEL CONFIGURATION
::  Priority: model_config.bat (auto-detected) > manual override below
::  To reconfigure:  python auto_model.py --rescan
:: ══════════════════════════════════════════════════════════════

:: Load auto-detected config if available
if exist model_config.bat (
    call model_config.bat
    goto :run
)

:: ── Manual override (uncomment ONE section if no model_config.bat) ──

:: Option 0: No LLM (pure cognitive simulation)
:: set AXIOM_LLM_BACKEND=none

:: Option 1: Local llama.cpp (GGUF model on CPU) [ACTIVE]
set AXIOM_LLM_BACKEND=local_llama
set AXIOM_LLAMA_MODEL_PATH=D:\models\Qwen2.5-7B-Instruct-Q4_K_M.gguf
set AXIOM_LLM_CTX_WINDOW=4096
set AXIOM_LLM_MAX_TOKENS=512

:: Option 2: OpenAI API
:: set AXIOM_LLM_BACKEND=openai_http
:: set OPENAI_API_KEY=sk-your-key-here
:: set AXIOM_OPENAI_MODEL=gpt-4.1-mini

:: Option 3: Anthropic API
:: set AXIOM_LLM_BACKEND=anthropic_http
:: set ANTHROPIC_API_KEY=sk-ant-your-key-here
:: set AXIOM_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

:: Option 4: HuggingFace Transformers (needs GPU or lots of RAM)
:: set AXIOM_LLM_BACKEND=transformers_local
:: set AXIOM_TRANSFORMERS_MODEL=Qwen/Qwen2.5-3B-Instruct

:run
:: ══════════════════════════════════════════════════════════════
::  RUN AXIOM
:: ══════════════════════════════════════════════════════════════
echo.
echo Starting AXIOM v1.0...
echo LLM Backend: %AXIOM_LLM_BACKEND%
if defined AXIOM_LLAMA_MODEL_PATH echo Model: %AXIOM_LLAMA_MODEL_PATH%
if defined AXIOM_TRANSFORMERS_MODEL echo Model: %AXIOM_TRANSFORMERS_MODEL%
echo.

python axiom_v1.py

echo.
pause
