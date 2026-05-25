# Changelog

All notable changes to TianJi will be documented in this file.

## [0.1.0] - 2026-05-26

### Added

- Initial TianJi V1 prototype based on MiroFish codebase.
- Added independent `backend/app/tianji` module.
- Added TianJi state model.
- Added Reality Parser.
- Added Bagua semantic dataset.
- Added Wuxing dynamics dataset.
- Added IChing semantic seed dataset.
- Added Symbolic Engine.
- Added Local Simulation Adapter with 10 agent roles:
  - Reality Agent
  - Causal Agent
  - Risk Agent
  - Strategy Agent
  - Bazi Agent
  - Qimen Agent
  - IChing Agent
  - Wuxing Agent
  - Skeptic Agent
  - Synthesizer Agent
- Added TianJi Orchestrator.
- Added Markdown/JSON Report Generator.
- Added CLI entry: `backend/scripts/tianji_cli.py`.
- Added HTTP API:
  - `GET /api/tianji/health`
  - `POST /api/tianji/run`
- Added `README_TIANJI.md`.
- Added `docs/TIANJI_ARCHITECTURE.md`.
- Added `docs/API.md`.
- Added `docs/ROADMAP.md`.
- Added `CONTRIBUTING.md`.
- Added `NOTICE.md` attribution file.

### Changed

- Updated root `README.md` for TianJi project identity.
- Updated root `package.json` name and description.
- Registered TianJi Flask blueprint.

### Removed

- Removed inherited GitHub workflow from original codebase to avoid token workflow-scope push issue.
