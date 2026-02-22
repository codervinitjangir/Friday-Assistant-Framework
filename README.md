# F.R.I.D.A.Y. Assistant - Public Showcase

Welcome to the public showcase repository for the **F.R.I.D.A.Y. AI Assistant** project.

This repository contains the **User Interface (UI)**, configuration templates, and setup scripts for the assistant. The core AI processing logic and backend systems are kept in a separate, private repository to protect the proprietary logic.

## What's Included in This Repository?

This showcase repository features the modern, futuristic frontend and utility scripts that power the Friday experience.

### 🎨 User Interface

- **`src/friday/ui/hud.py`**: The main Heads-Up Display (HUD) built with PyQt6. This file handles the floating, transparent UI, dynamic animations, and visual feedback for the user.

### 🛠️ Configuration & Setup

- **`.env.example`**: A template for the environment variables required to run the assistant, demonstrating the required core APIs (like OpenAI for LLMs).
- **`Dockerfile`**: Containerization setup for the modular application.
- **`requirements.txt` / `pyproject.toml`**: The python dependencies handling GUI, AI, Voice, and System integrations.

### 🏃‍♂️ Running & Utilities

- **`Run Friday.bat`**: A convenient Windows batch script for setting up the environment and launching the assistant.
- **`check_gpu.py`**: Utility script to verify GPU acceleration capabilities for faster local processing.
- **`list_models.py` / `list_voices.py`**: Scripts to query and manage available TTS voices and LLM models.
- **`setup_model.py`**: Handles initialization for any local AI models used by the assistant.

## System Architecture Overview

While the core source code is private, the complete F.R.I.D.A.Y. architecture consists of:

- **Core Orchestrator**: The central event loop processing commands.
- **Skill Engine**: A modular plugin system enabling system control, memory retrieval, and web capabilities.
- **Memory Module**: SQLite vectorized long-term memory.
- **Audio IO**: Wake-word detection, STT (Speech-to-Text) and Edge TTS.
- **HUD Engine**: The open-source `hud.py` visual interface.

## Quickstart

If you clone this showcase and wish to build your own engine behind the HUD:

1. **Setup Environment**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Variables**

   ```bash
   cp .env.example .env
   # Add your API keys to the .env file
   ```

3. **Launch the Core (Requires private engine)**
   ```bash
   Run Friday.bat
   ```

## License

MIT License (Applicable to the files in this public repository).
