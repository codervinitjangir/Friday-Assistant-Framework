# F.R.I.D.A.Y. Assistant - Public Showcase

Welcome to the public showcase repository for the **F.R.I.D.A.Y. AI Assistant** project.

This repository contains the **User Interface (UI)**, configuration templates, and setup scripts for the assistant. The core AI processing logic and backend systems are kept in a separate, private repository to protect the proprietary logic.

## What's Included in This Repository?

This showcase repository features the modern, futuristic frontend and utility scripts that power the Friday experience.

### 🎨 User Interface

- **`src/friday/ui/hud.py`**: The main Heads-Up Display (HUD) built with PyQt6. This file handles the floating, transparent UI, dynamic animations, and visual feedback for the user.

### 🛠️ Configuration & Dependencies

- **`requirements.txt`**: The python dependencies handling GUI, animations, and system packages required to run the interface portion.

## System Architecture Overview

While the core source code is private, the complete F.R.I.D.A.Y. architecture consists of:

- **Core Orchestrator**: The central event loop processing commands.
- **Skill Engine**: A modular plugin system enabling system control, memory retrieval, and web capabilities.
- **Memory Module**: SQLite vectorized long-term memory.
- **Audio IO**: Wake-word detection, STT (Speech-to-Text) and Edge TTS.
- **HUD Engine**: The open-source `hud.py` visual interface.

### 🏃‍♂️ Running the UI Standalone

Since the core engine is private and hidden, this UI can be tested or modified independently:

1. **Setup Environment**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run HUD Code**
   ```bash
   python src/friday/ui/hud.py
   ```
   _(Note: To integrate this UI into your own assistant, you will need to build your own engine connecting it to LLMs and Voice IO)._

## License

MIT License (Applicable to the files in this public repository).
