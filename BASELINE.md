# Baseline (Instructor-provided) and Student Work

This repository follows course CS591 — Advanced Artificial Intelligence (Project 2-Group 1) workflow. Instructor-provided starter code and images (the "baseline") are recorded so student work can be developed separately and overlap can be measured if parts of the baseline are used.

- **Baseline**: The instructor-provided files live on the `baseline` branch (or optionally in `reference/` on `main`). This branch or folder contains the original starter files and is intentionally preserved unchanged so provenance is clear.
- **Main**: `main` is the integration branch used for merged student work. `main` can be created from `baseline` so it starts from the same baseline state.
- **Student branches**: Each student or task should be developed on its own branch using the naming pattern:
  - `student/<your-name>-<task>` or `student/<yourname>/<task>` (pick one convention and use it consistently).
  - Examples: `student/mandy-minimax` or `student/mandy/minimax`.
- **Attribution**: In commits and PR descriptions, note which code files, snippets, or images are adapted from the baseline (a short "Derived from" line is enough). Replace any placeholder commit hash (e.g., `abc123`) with the actual baseline commit hash.

## Derived from (example)

- Instructor baseline: commit `abc123` on branch `baseline`. Student work lives in `src/`. The main differences are:
  - new agent implementation in `src/minimax_agent.py`
  - revised evaluation function in `src/eval.py`
  - tests in `tests/`

## How to measure overlap

- Use Git to compute added/removed lines per file between `baseline` and a student branch:
  - `git diff --numstat origin/baseline..origin/student/branch`
  - The output shows added and removed line counts per file (format: `added<TAB>removed<TAB>filename`).
- Count baseline lines (PowerShell example) and compute overlap percent:
  - Sum baseline lines, then use the removed lines from the diff to estimate how many baseline lines were changed or removed.
- If the course requires a specific tool or metric, use that tool; otherwise `git diff --numstat` plus line counts is a reasonable line-count estimate.

---

## Notes for this repo

- The instructor's original `README.md` will remain unaltered in the repository root (it documents the original project and demo instructions). This file (`BASELINE.md`) will be placed alongside `README.md` so reviewers and graders can easily find baseline documentation.
- If there is a code file already added by a group member intended for everyone to use (the game board helper), that file will be added to `main` so the whole team can build on it.
