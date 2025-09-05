# AI Code Assistant (Gemini Function-Calling)

A small command-line AI coding agent that uses Google's Gemini models with function calling to safely inspect and manipulate a sandboxed project directory. The agent can:

- List files and directories within a configured working directory
- Read file contents (with size limits)
- Run Python files with optional arguments
- Write or overwrite files (creating directories as needed)

All tool operations are constrained to the configured working directory to prevent access outside the sandbox.

## Demo

- Video: [Watch the demo](aiagent-demo.mp4)

## Requirements

- Python 3.13+
- A Google Gemini API key

Python dependencies are managed via `pyproject.toml` and installed using your preferred tool (e.g., `uv`, `pip`).

## Installation

Using `uv` (recommended):

```bash
# From the project root
uv sync
```

## Configuration

Environment variables are loaded via `.env` (using `python-dotenv`). Create a `.env` file in the project root containing:

```bash
GEMINI_API_KEY=your_api_key_here
```

Other runtime configuration lives in `config.py`:

- `WORKING_DIR`: sandboxed directory for all tool calls (default: `./calculator`)
- `MAX_CHARS`: max characters returned when reading files (default: 10000)
- `MAX_ITERS`: safety limit for agent turns (default: 20)

## Usage

From the project root:

```bash
python main.py "Your request here" [--verbose]
```

Examples:

```bash
python main.py "List files in the project"
python main.py "Open calculator/main.py and explain the bug" --verbose
python main.py "Run calculator/tests.py"
```

- `--verbose` prints token usage, tool invocations, and intermediate outputs.

## How it works

Entry point: `main.py`

- Loads `.env`
- Builds a conversation with your user prompt
- Calls Gemini (`gemini-2.0-flash-001`) with a system instruction (`prompts.py`) and tool declarations
- Handles model tool calls via `dispatcher/call_function.py`
- Continues until the model returns a final text response or `MAX_ITERS` is reached

### System instruction

`prompts.py` defines the agent’s capabilities and constraints for tool usage.

### Tools (Functions)

Declared in `dispatcher/call_function.py` and implemented under `functions/`:

- `get_files_info(directory='.')`

  - Lists files in a directory within `WORKING_DIR`, returning name, size, and is_dir.
  - Enforced sandbox: prevents escaping the working directory.

- `get_file_content(file_path)`

  - Reads a file within `WORKING_DIR` up to 10,000 characters; truncates if larger.

- `run_python_file(file_path, args=[])`

  - Executes a Python script inside `WORKING_DIR` with optional args.
  - Captures stdout/stderr; reports non-zero exit codes.

- `write_file(file_path, content)`
  - Writes text to a file inside `WORKING_DIR`; creates parent dirs as needed.

## Development

- Adjust `WORKING_DIR` in `config.py` to target a different sandbox.
- Extend tools by adding new functions in `functions/` and wiring their schemas into `dispatcher/call_function.py`.
- Keep I/O constrained to `WORKING_DIR` to maintain safety.
