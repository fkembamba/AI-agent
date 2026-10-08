# GitHub Setup Guide

## Project board

Create one GitHub Project for the study with these fields:

| Field | Type |
|---|---|
| Status | Single select |
| Priority | Single select |
| Work Package | Single select |
| Milestone | Single select |
| Area | Single select |
| Owner | Assignee or single select |
| Evidence | Text |
| Target Date | Date |
| Percent Complete | Number |

Recommended Status values: `Backlog`, `Ready`, `In Progress`, `Blocked`, `Technical Review`, `Done`.

## Milestones

Create milestones M1 through M10 using the definitions in `docs/PROJECT_MANAGEMENT.md`.

## Labels

Create the area, priority, and type labels listed in the project-management document.

## Issue creation

Start with the ten Immediate Next Actions in `docs/PROJECT_MANAGEMENT.md`. Create one issue per action and assign it to the responsible team member(s).

## Branching

A simple research-project convention is sufficient:

- `main` — approved baseline
- `feature/<issue>-<short-name>` — implementation work
- `experiment/<id>` — experiment-specific changes only when needed

## Releases/tags

Tag every reproducible experimental baseline. Record the exact Git SHA or tag in every run manifest.
