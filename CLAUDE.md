# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Small demo project ("cyberchat") for a school career-fair talk by Cao Tri DO: chatbots that show how a system prompt gives an LLM a personality. All three entry points call Groq's `llama-3.3-70b-versatile` with streaming. Python >=3.12, managed with `uv`. There are no tests, linter, or build step.

## Commands

```bash
uv sync                          # install deps
uv run streamlit run app.py      # web UI (main demo)
uv run python main_protected.py  # terminal chat, key from .env
uv run python main.py            # terminal chat, key hardcoded in API_KEY_PASSWORD
```

## Architecture

Three independent scripts, no shared module (the streaming/chat loop is duplicated):

- [app.py](app.py): Streamlit app. The persona is chosen in the sidebar from the `PROMPT_STYLES` dict (4 French + 4 English styles, each mentioning "Cao Tri" as PhD in AI and musician). The user pastes their own Groq API key in the sidebar; no env var is used. Chat history lives in `st.session_state.messages`, and the selected style's prompt is re-prepended as the system message on every request. UI strings are in French.
- [main_protected.py](main_protected.py): terminal chat that reads `GROQ_API_KEY` from `.env` via `python-dotenv` and loads the system prompt from [system_prompt.txt](system_prompt.txt).
- [main.py](main.py): same as above, but the key is a hardcoded `API_KEY_PASSWORD` constant (left empty; fill it locally, never commit it).

[system_prompt.txt](system_prompt.txt) is a prompt-injection/"secret" demo: the bot reveals a "magic number" for the cybersecurity course only on a specific question, deflects further questions as classified, and otherwise plays Super Mario. It is used only by the terminal scripts, not by `app.py`.

## Gotchas

- `.env` is tracked in git and is not listed in [.gitignore](.gitignore), so a real `GROQ_API_KEY` would be committed. Add `.env` to `.gitignore` and `git rm --cached .env` before putting a real key in it.
- [README.md](README.md) is empty.
