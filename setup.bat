@echo off
chcp 65001 >nul 2>&1
title AXIOM v1.0 - Setup
echo.
echo ══════════════════════════════════════════════════════════════
echo   AXIOM v1.0 - Automated Setup
echo ══════════════════════════════════════════════════════════════
echo.

:: ── 1. Check Python ──────────────────────────────────────────
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.11+ from https://www.python.org
    echo        Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo       Found Python %PYVER%

:: ── 2. Create virtual environment ────────────────────────────
echo.
echo [2/7] Creating virtual environment (.venv)...
if exist .venv (
    echo       .venv already exists, skipping.
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo       Created.
)

:: ── 3. Activate venv ─────────────────────────────────────────
echo.
echo [3/7] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo       Activated.

:: ── 4. Upgrade pip ───────────────────────────────────────────
echo.
echo [4/7] Upgrading pip...
python -m pip install --upgrade pip --quiet

:: ── 5. Install PyTorch (auto-detect CUDA vs CPU) ─────────────
echo.
echo [5/7] Installing PyTorch...
python -c "import torch; print(torch.cuda.is_available())" 2>nul | findstr /i "True" >nul 2>&1
if %errorlevel%==0 (
    echo       CUDA detected — installing GPU version...
    pip install torch torchvision torchaudio --quiet
) else (
    echo       No CUDA detected — installing CPU version...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --quiet
)
if errorlevel 1 (
    echo WARNING: PyTorch install failed. Neural simulation may be limited.
)

:: ── 6. Install dependencies from requirements.txt ────────────
echo.
echo [6/7] Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo WARNING: Some packages may have failed.
    echo          AXIOM can still run in simulation mode (no LLM).
)

:: ── 7. Auto-detect / configure LLM model ─────────────────────
echo.
echo [7/7] Configuring LLM model...
echo       Scanning for GGUF / HuggingFace models on your system...
echo.
python auto_model.py

:: ── Done ─────────────────────────────────────────────────────
echo.
echo ══════════════════════════════════════════════════════════════
echo   Setup complete!
echo ══════════════════════════════════════════════════════════════
echo.
echo   Run AXIOM:
echo     run.bat          CLI mode
echo     run_ui.bat       Web UI (opens browser at localhost:7860)
echo.
echo   Reconfigure model later:
echo     python auto_model.py
echo.
pause
