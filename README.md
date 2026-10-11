# Chat with Cao

A small demo built for a school career fair ("Forum des Métiers") talk by **Cao Tri DO** (PhD in AI, data expert, musician). It shows students one idea: **a system prompt gives an LLM a personality**. The same model answers very differently depending on the instructions it receives before the conversation starts.

All chatbots call [Groq](https://groq.com/) with streaming enabled.

## Features

- **Streamlit web UI** where the audience picks a persona (8 styles, 4 in French and 4 in English) and chats live.
- **Model picker** populated from the models available to the API key you enter.
- **Terminal chat** variants driven by a system prompt stored in a text file.
- **Prompt-secret demo**: a system prompt that hides a "magic number" and deflects follow-up questions, to illustrate prompt injection and secrets in prompts.

## Project structure

```
.
├── app/
│   └── app.py                 # Streamlit web app (main demo)
├── scripts/
│   ├── main.py                # Terminal chat, API key hardcoded in the file
│   └── main_protected.py      # Terminal chat, API key read from .env
├── config/
│   └── system_prompt.txt      # System prompt for the terminal scripts (secret demo)
├── .devcontainer/             # Dev container / Codespaces config
├── .env.template              # Template for the .env file
├── Makefile                   # Shortcuts for common commands
├── pyproject.toml             # Project metadata and dependencies
└── uv.lock
```

## Requirements

- Python **3.12+**
- [uv](https://docs.astral.sh/uv/) for dependency management
- A free [Groq API key](https://console.groq.com/keys)

Dependencies (see [pyproject.toml](pyproject.toml)): `groq`, `python-dotenv`, `streamlit`.

## Setup

```bash
git clone <repo-url>
cd Chat-with-cao
make install        # or: uv sync
```

## Usage

A [Makefile](Makefile) wraps the commands. Run `make help` to list them.

| Command | Description |
|---|---|
| `make install` | Install dependencies (`uv sync`) |
| `make run` | Start the Streamlit web UI |
| `make protected` | Terminal chat, API key read from `.env` |
| `make chat` | Terminal chat, API key hardcoded in `scripts/main.py` |
| `make clean` | Remove `__pycache__` and `.mypy_cache` directories |

### Web app (main demo)

```bash
make run
# equivalent: uv run streamlit run app/app.py
```

Then open <http://localhost:8501> and, in the sidebar:

1. Paste your **Groq API key** (it is only kept in the browser session; no environment variable is used).
2. Choose a **model**. The list is fetched from Groq for your key, and a Llama 70B model is selected by default when available.
3. Choose an **AI style** (persona).
4. Chat. Use **Réinitialiser la discussion** to clear the history.

The UI text is in French.

#### Available personas

| French | English |
|---|---|
| Cool & Grand Frère | Cool & Big Brother (English) |
| Futuriste 2077 | Futurist 2077 (English) |
| Coach de Super-Héros | Superhero Coach (English) |
| Mario (It's-a me!) | Mario (It's-a me!) (English) |

Each persona mentions Cao Tri as both a PhD in AI and a musician. The personas are defined in the `PROMPT_STYLES` dictionary at the top of [app/app.py](app/app.py); add an entry there to create a new one.

### Terminal chat

Both scripts use `llama-3.3-70b-versatile`, stream the answer token by token, and keep the conversation history. Type `exit` or `quit` (or press Ctrl+C) to leave.

**With a `.env` file (recommended):**

```bash
cp .env.template .env
# edit .env and set GROQ_API_KEY=your_key
make protected
```

**With a hardcoded key:** set `API_KEY_PASSWORD` at the top of [scripts/main.py](scripts/main.py), then run `make chat`. Never commit the key.

Both scripts load the system prompt from `system_prompt.txt`, resolved relative to the current working directory (see [Known issues](#known-issues)).

## How it works

Every request to the model is a list of messages:

```
[ system prompt ] + [ user / assistant history ]
```

- In the web app, the selected persona's prompt is re-prepended as the `system` message on every request, so switching style changes the personality immediately. History is stored in `st.session_state.messages`.
- In the terminal scripts, the system prompt is read once at startup from the text file.
- Responses are streamed (`stream=True`) and rendered progressively.

The web app uses `temperature=0.7` and `max_tokens=1024`.

## Security notes

- Keep your Groq API key out of version control. [.env.template](.env.template) is the tracked template; copy it to `.env` for real keys.
- `.env` is **not** currently listed in [.gitignore](.gitignore). Add it before putting a real key in it, and if it was ever tracked, run `git rm --cached .env`.
- Never commit a key written into `API_KEY_PASSWORD` in `scripts/main.py`.

## Dev container / Codespaces

[.devcontainer/devcontainer.json](.devcontainer/devcontainer.json) provides a Python container that forwards port 8501 for Streamlit. It still references the old `app.py` path (see below).

## Known issues

- **System prompt path:** the terminal scripts open `system_prompt.txt` relative to the working directory, but the file now lives in `config/`. Running `make protected` or `make chat` from the repo root fails with "'system_prompt.txt' not found" until the path is updated to `config/system_prompt.txt`.
- **Dev container paths:** `devcontainer.json` still runs `streamlit run app.py` and opens `app.py`; update them to `app/app.py`.
- **Dev container Python:** the container image uses Python 3.11, while the project requires 3.12+.
- The streaming/chat loop is duplicated across the scripts; there is no shared module.
- There are no tests, linter, or build step.

## Author

Cao Tri DO: PhD in AI, data & AI expert, and musician.
