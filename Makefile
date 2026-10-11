.PHONY: help install app protected chat clean

help: ## Show available commands
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-10s %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

run: ## Run the Streamlit web UI (main demo)
	uv run streamlit run app/app.py

protected: ## Run terminal chat, key from .env
	uv run scripts/main_protected.py

chat: ## Run terminal chat, key hardcoded in main.py
	uv run scripts/main.py

clean: ## Remove Python and tool caches
	find . -type d \( -name __pycache__ -o -name .mypy_cache \) -not -path './.venv/*' -prune -exec rm -rf {} +
