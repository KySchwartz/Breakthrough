# CONTRIBUTING

This document describes how students should work in this repository for CS591 Project 2 (Group 1).

## Goals
- Keep instructor-provided starter code (baseline) separated from student work.
- Provide a single integration branch `main-from-baseline` where reviewed student contributions are merged.
- Enforce simple branch naming and PR rules so grading/overlap checks are reproducible.

## Branches
- `baseline` — an archival record of the instructor's original starter files (read-only).
- `main-from-baseline` — the integration branch. Students should branch from here and open PRs targeting this branch. Only instructors or reviewers should directly merge into this branch.
- `main` — the repo default branch (may be kept protected). Do not push student work directly to `main`.

## Branch naming (students)
Create personal branches using the pattern:
```
student/<your-name>-<task>
```
Example:
```
student/mandy-minimax
```

## How to start (copy/paste)
```powershell
git clone https://github.com/KySchwartz/Breakthrough.git
cd Breakthrough
git fetch origin
git checkout -b student/<your-name>-<task> origin/main-from-baseline
```

## Work → PR → Merge
1. Work locally on your `student/*` branch. Commit small, descriptive changes.
2. Push your branch:
```
git push -u origin student/<your-name>-<task>
```
3. Create a Pull Request on GitHub with base branch `main-from-baseline` and head `student/<your-name>-<task>`.
4. Assign a reviewer (or the instructor). Wait for approvals and address review comments.
5. Once approved, a reviewer (instructor or designated TA) will merge the PR into `main-from-baseline`.

Do NOT merge student PRs directly into `main` unless instructed by the instructor.

## PR checklist (use this when opening a PR)
- [ ] Branch name follows `student/<your-name>-<task>` pattern
- [ ] PR title is descriptive (short summary)
- [ ] PR description explains the change and references any issues
- [ ] Code runs and primary functionality tested locally
- [ ] No large binary files added

## How instructors/maintainers should handle merges
- Require at least 1 approving review before merging.
- If there are many students, merge one student PR at a time and verify that the integration build (if any) is OK.
- Prefer fast-forward or regular merge to preserve individual commits, or use squash if you want a single commit per PR — be consistent.

## Overlap / Baseline checking (for grading)
To estimate overlap with the instructor baseline, use:
```powershell
# show numeric diff summary between baseline (main-from-baseline) and a student's branch
git fetch origin
git diff --numstat origin/main-from-baseline origin/student/<your-name>-<task>
```
This lists files changed and added/removed lines which can help compute overlap percentages.

## Notes & contact
- `BASELINE.md` documents how the instructor baseline was recorded.
- If you are unsure which branch to target, ask the instructor or open an issue.

Thank you — follow these steps and we will keep instructor and student work clearly separated.
