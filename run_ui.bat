@echo off
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
title AXIOM v1.0 - Web UI

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

:: ── Manual override (same options as run.bat) ────────────────
:: set AXIOM_LLM_BACKEND=none

:: Option 1: Local llama.cpp [ACTIVE]
set AXIOM_LLM_BACKEND=local_llama
set AXIOM_LLAMA_MODEL_PATH=D:\models\Qwen2.5-7B-Instruct-Q4_K_M.gguf
set AXIOM_LLM_CTX_WINDOW=4096
set AXIOM_LLM_MAX_TOKENS=512

:run
:: ══════════════════════════════════════════════════════════════
::  RUN AXIOM WEB UI
:: ══════════════════════════════════════════════════════════════
echo.
echo Starting AXIOM v1.0 Web UI...
echo LLM Backend: %AXIOM_LLM_BACKEND%
if defined AXIOM_LLAMA_MODEL_PATH echo Model: %AXIOM_LLAMA_MODEL_PATH%
if defined AXIOM_TRANSFORMERS_MODEL echo Model: %AXIOM_TRANSFORMERS_MODEL%
echo Web UI will open at: http://localhost:7860
echo.

python axiom_ui.py

echo.
pause
