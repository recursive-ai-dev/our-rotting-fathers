# v1.0 Release Plan

## Purpose
This plan defines the work needed to ship a stable, reproducible, and documented `v1.0` of the AI Human Generator codebase.

## Snapshot Of Current State
- Core sprite generation, batch generation, animation generation, and swarm modules are implemented.
- A critical runtime bug exists in swarm batch generation: `time` is used but not imported in `generator/swarm_generator.py`.
- Deterministic seed handling is inconsistent: `seed=0` is ignored in `generator/pure_generator.py` (`if seed:` pattern).
- Animation alignment is incomplete: animated hair and face currently do not follow head offsets in `generator/animation_generator.py`.
- CLI is interactive-only and includes an explicitly unimplemented memory query path in `ai_human_generator.py`.
- No automated tests, CI, packaging metadata (`pyproject.toml`), or release governance files (`LICENSE`, `CONTRIBUTING`, etc.) are present.
- Docs make strong claims that are not yet backed by repeatable tests/benchmarks in-repo.

## v1.0 Release Goals
- Reliable generation flows (pure, mass, animation, swarm) with no known runtime crash paths.
- Reproducible results for fixed seeds across supported generation modes.
- Clear user interface for scripted and interactive usage.
- Automated test coverage and CI quality gates.
- Documentation that accurately matches implemented behavior and measured results.
- Installable and distributable package with standard project governance files.

## Out Of Scope For v1.0
- New model families or major architecture rewrites.
- Non-essential UI applications (web/desktop frontends).
- Advanced distributed generation infrastructure.

## Milestones

## M0 - Scope Freeze And Baseline (0.5-1 day)
### Tasks
- Define supported runtime matrix (recommended: Python 3.10-3.12).
- Freeze v1.0 scope to stabilization + packaging + documentation correctness.
- Add a `scripts/smoke_test.sh` (or Python equivalent) for quick local validation.

### Exit Criteria
- Scope approved and documented.
- Baseline smoke script runs all primary modes with small sample counts.

## M1 - Critical Stabilization (P0) (1-2 days)
### Tasks
- Fix `NameError` in swarm batch by importing `time` in `generator/swarm_generator.py`.
- Normalize seed checks from `if seed:` to `if seed is not None:` in relevant code paths.
- Ensure deterministic behavior in swarm completion path (remove uncontrolled random fallback or seed all fallback randomness deterministically).
- Fix animated head/face/hair alignment so offsets are applied consistently.
- Verify `SwarmCharacterGenerator.__init__` passes `canvas_size` directly to parent init.

### Exit Criteria
- No runtime crashes in:
  - `MassCharacterGenerator.generate_massive_batch(...)`
  - `AnimationGenerator.generate_animation(...)`
  - `SwarmCharacterGenerator.generate_swarm_batch(...)`
- Fixed seed reproducibility test passes including `seed=0`.
- Visual sanity checks pass for walk/run/jump frame alignment.

## M2 - CLI/Product Interface Completion (P1) (1-2 days)
### Tasks
- Add non-interactive CLI interface (`argparse`) with subcommands:
  - `generate-batch`
  - `generate-animation`
  - `generate-swarm`
  - `query-memory` (or explicitly remove from CLI scope for v1.0 and document API-only)
- Keep current interactive menu as optional mode.
- Standardize output directory naming and metadata schema between modes.
- Add explicit exit codes and clear error messages.

### Exit Criteria
- All primary flows can run from command line without prompts.
- CLI help text is complete and accurate.
- Memory query behavior is either implemented or intentionally excluded and documented.

## M3 - Tests And CI (P0) (2-4 days)
### Tasks
- Introduce `pytest` test suite with focused invariants:
  - Determinism with fixed seed (including `0`).
  - Uniqueness constraints for batch generation at small N.
  - Swarm batch smoke test.
  - Animation frame count and alignment checks.
  - Metadata schema validation.
- Add CI workflow (recommended: GitHub Actions) to run tests on supported Python versions.
- Add linting/type baseline (recommended: `ruff`; optional `mypy` in strict subset).

### Exit Criteria
- CI is green on all supported Python versions.
- Regressions in P0 paths are prevented by automated tests.

## M4 - Documentation Integrity And Claims Calibration (P0) (1-2 days)
### Tasks
- Update `README.md` and `SWARM_README.md` so claims match measured behavior.
- Add a "Reproducibility" section with exact commands and expected outputs.
- Mark experimental components clearly (if any swarm learning behavior remains heuristic).
- Add troubleshooting section for common runtime issues and platform notes.

### Exit Criteria
- Documentation contains no unverified claim presented as guaranteed fact.
- A new user can reproduce sample outputs from docs alone.

## M5 - Packaging And Governance (P1) (1-2 days)
### Tasks
- Add `pyproject.toml` with project metadata and console entry point.
- Add semantic version source of truth (`__version__` + package metadata consistency).
- Add standard project files:
  - `LICENSE`
  - `CONTRIBUTING.md`
  - `CODE_OF_CONDUCT.md` (optional but recommended)
  - `SECURITY.md` (recommended)
  - `CHANGELOG.md`

### Exit Criteria
- Project installs via `pip` in a clean environment.
- Console command works after install.
- Release/legal/governance files exist and are linked from `README.md`.

## M6 - Performance And Release Validation (P1) (1-2 days)
### Tasks
- Add repeatable benchmark script for representative sizes/counts (for example: 32/64, N=100 and N=1000).
- Record benchmark outputs in docs with hardware notes.
- Validate disk output structure and metadata consistency across all modes.
- Run end-to-end release candidate checklist.

### Exit Criteria
- Benchmark and resource expectations are documented.
- Release candidate passes full smoke + test suite.

## M7 - v1.0 Release (0.5 day)
### Tasks
- Tag release `v1.0.0`.
- Publish release notes with:
  - Known limitations
  - Compatibility matrix
  - Upgrade notes
- Archive canonical sample outputs and metadata for reproducibility.

### Exit Criteria
- Tagged release and published notes.
- Reproducible installation and command examples validated post-tag.

## Prioritized Backlog (Condensed)
- P0: Swarm `time` import crash fix.
- P0: Seed determinism correctness including `seed=0`.
- P0: Animation head/hair/face offset consistency.
- P0: Automated tests + CI.
- P0: Documentation claim calibration.
- P1: Non-interactive CLI subcommands.
- P1: Packaging and governance docs.
- P1: Benchmarking and performance reporting.

## Suggested Definition Of Done For v1.0
- All P0 items complete.
- CI green and reproducible locally.
- Documentation and product behavior are aligned.
- Install + run path verified from a clean environment.
- No known crash in primary generation modes.

## Recommended Execution Order
1. M0-M1 stabilization first.
2. M3 tests/CI immediately after core fixes.
3. M2 CLI completion in parallel with M4 docs cleanup.
4. M5 packaging/governance.
5. M6 validation and M7 release tag.

