# Contributing

## Maintainers

**Thomas** and **Colin**

## Prerequisites

Contributors should be comfortable with:
- Python and OpenCV
- Computer vision concepts (camera calibration, affine transforms)
- Linux environments (Ubuntu, Jetson)

## How to Contribute

1. Contact the maintainers first — we'll point you to what needs doing
2. Fork the repo and create a feature branch
3. Make focused, small changes
4. Run `ruff check .` and fix any issues
5. Open a Pull Request against `main`

## Linting

We use **ruff** as our only linter. Run it before submitting PRs:

```bash
pip install ruff
ruff check .
```

## On Using AI Tools

We welcome contributors who use Claude Code, Cursor, Copilot, or other AI tools — but please write your own commit messages and PR descriptions.

Why? It forces you to slow down and understand what you're actually contributing.

## What We Don't Want

- **Giant PRs** that change everything at once — keep changes small and focused
- **LLM conversation dumps** pasted into PRs or code
- Unrelated changes bundled together

Keep PRs readable and human-understandable.
