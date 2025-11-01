# BreakthroughGame

## Requirements

- Python 3.8+ (or a compatible Python 3.x)
- pygame

Install pygame:
```
pip install pygame
```

## Project

Breakthrough is an abstract strategy board game invented by Dan Troyka in 2000. This repository contains an implementation of Breakthrough and two AI agents (minimax and alpha-beta). The project was created for CS591 at Southeast Missouri State University.

## Goals

Implement agents capable of playing Breakthrough. Features considered include "important pieces", "connected pairs of pieces", and configurable parameters to make agents more aggressive or defensive.

## Student workflow (CS591 - Group 1)

This repository preserves the instructor-provided starter code on a baseline branch and provides a clean integration branch `main-from-baseline` for student work.

- Baseline: Instructor-provided starter files are recorded on the `baseline` branch.
- Integration: `main-from-baseline` is a clean branch created from the baseline and contains the shared game board helper (`The_game_board.py`) and the baseline materials.

Student branches: Create personal branches from `main-from-baseline` using the pattern:
`student/<your-name>-<task>` (example: `student/mandy-minimax`)

Example student commands:
```
git fetch origin
git checkout -b student/<your-name>-<task> origin/main-from-baseline
# make changes, then:
git add .
git commit -m "Short descriptive message"
git push -u origin student/<your-name>-<task>
```

See `BASELINE.md` in the repository root for details on how the baseline is recorded and how to estimate overlap (for example, using `git diff --numstat`).
