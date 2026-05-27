# AGENTS.md

## Project overview

This repository hosts the image containing the Open Source Vulnerability (OSV) database used by MintMaker. The image is built and pushed periodically using Konflux CI to ensure the database contains the latest vulnerability data.

## Architecture

- `Dockerfile`: The image containing the OSV database.
- `cleanup.py`: Script that prunes old image tags from Quay.
- `.github/workflows/clean-osv-db-repo.yaml`: Runs `cleanup.py`.
- `.github/workflows/trigger-osv-db-build.yaml`: Triggers rebuild via empty commit.

## Agent Directives

- **Commits**: Do NOT commit unless asked. Use conventional commits (e.g., `feat:`, `fix:`, `chore:`).
- **Secrets**: NEVER commit credentials or tokens.
- **Style**: Match the existing style in `cleanup.py`.
- **Prohibitions**: Do NOT modify `.github/workflows/`, `.tekton/` or `CODEOWNERS` unless explicitly commanded.
