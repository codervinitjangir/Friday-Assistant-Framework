# F.R.I.D.A.Y. Assistant

A modular, extensible personal AI assistant inspired by the MCU. Built with Python, it handles voice commands, executes system actions, and provides a futuristic HUD.

## Features

- **Voice Interaction**: Wake-word activation ("Friday") and natural speech commands.
- **LLM Intelligence**: Powered by OpenAI (adaptable to local LLMs).
- **System Control**: Open apps, manage volume, take screenshots.
- **Memory**: Remembers user details and past interactions via SQLite.
- **GUI**: A floating HUD built with PyQt6.
- **Safe**: Confirms destructive actions before execution.

## Quickstart

### Prerequisites

- Python 3.10+
- A working microphone and speakers.
- (Optional) Docker

### Installation

1. **Clone and Setup**

   ```bash
   # Create a virtual environment
   python -m venv .venv

   # Activate it
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

   _Note: On Windows, you may need to install [PyAudio wheel](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) manually if pip fails._

2. **Configuration**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your `OPENAI_API_KEY`.

3. **Run**

   ```bash
   # Launch with GUI
   python src/main.py --gui

   # Launch headless (terminal only)
   python src/main.py --headless
   ```

## Architecture

- **`src/friday/core`**: The central orchestrator loop.
- **`src/friday/skills`**: Plugin system for capabilities.
- **`src/friday/ui`**: PyQt6 interface.
- **`src/friday/memory`**: SQLite context storage.

## Extending

To add a new skill, create a file in `src/friday/skills/` and use the `@skill` decorator. See `docs/developer_guide.md`.

## License

MIT
