# Changelog

All notable changes to ZhaoJian will be documented in this file.

## [0.6.0] - 2026-05-26

### Added

- Added ZhaoJian frontend page: `frontend/src/views/ZhaoJianView.vue` with form-based simulation interface.
- Added ZhaoJian navigation link in Home navbar.
- Added ZhaoJian routes: `/zhaojian` page.
- Added ZhaoJian review/feedback system: `backend/app/api/zhaojian_review.py`.
- Added review API endpoints:
  - `POST /api/zhaojian-review/reviews/<report_id>` — save feedback
  - `GET /api/zhaojian-review/reviews/<report_id>` — get feedback
  - `DELETE /api/zhaojian-review/reviews/<report_id>` — delete feedback
  - `GET /api/zhaojian-review/reviews` — list all reviews
  - `GET /api/zhaojian-review/stats` — review statistics and accuracy
- Added review UI in ZhaoJian frontend page.

## [0.5.0] - 2026-05-26

### Added

- Added V5 examples and test suite.
- Added `examples/` with strategy, personal path, and business decision inputs.
- Added `sample_reports/` with generated Markdown and JSON reports.
- Added `scripts/generate_sample_reports.py`.
- Added tests for IChing, Bazi, Qimen, and full ZhaoJian Orchestrator chain.
- Added npm scripts: `test` and `samples`.

## [0.4.0] - 2026-05-26

### Added

- Added V4 I Ching Transition Engine.
- Added full 64-hexagram semantic dataset: `iching_64_hexagrams.json`.
- Added `backend/app/zhaojian/engines/iching_engine.py`.
- Added primary hexagram and changed hexagram trend modeling.
- Added changing-line based stage warnings.
- Integrated I Ching transition output into reports.
- Integrated I Ching action hints into local simulation adapter.

### Notes

- V4 is a semantic trend engine, not deterministic divination.
- Nuclear hexagram and line-by-line traditional texts are planned for future versions.

## [0.3.0] - 2026-05-26

### Added

- Added V3 Qimen Situation Engine.
- Added `backend/app/zhaojian/engines/qimen_engine.py`.
- Added Qimen semantic datasets:
  - `jiugong.json`
  - `bamen.json`
  - `jiuxing.json`
  - `bashen.json`
- Integrated event-time based Qimen semantic situation analysis into Orchestrator.
- Integrated Qimen layout rendering into Markdown reports.
- Enhanced local simulation adapter with Qimen timing hints.

### Notes

- V3 uses semantic Qimen layout, not yet full traditional solar-term Qimen calculation.
- Solar terms, Yin/Yang Dun precision, Ju number, heaven/earth plates, and useful god selection are planned for future versions.

## [0.2.0] - 2026-05-26

### Added

- Added V2 Bazi Natal Pattern Engine.
- Added `backend/app/zhaojian/engines/bazi_engine.py`.
- Added Heavenly Stems and Earthly Branches data: `tiangan_dizhi.json`.
- Added Ten Gods mapping data: `ten_gods.json`.
- Added birth datetime support in CLI.
- Added birth datetime and gender support in API.
- Integrated Bazi output into ZhaoJian Orchestrator.
- Integrated Bazi result rendering into Markdown reports.
- Updated API docs and roadmap for V2.

### Notes

- V2 uses approximate solar-calendar pillar calculation.
- Month pillar is not yet corrected by solar terms.
- Luck cycles, useful god, and strength analysis are planned for future versions.

## [0.1.0] - 2026-05-26

### Added

- Initial ZhaoJian V1 prototype based on MiroFish codebase.
- Added independent `backend/app/zhaojian` module.
- Added ZhaoJian state model.
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
- Added ZhaoJian Orchestrator.
- Added Markdown/JSON Report Generator.
- Added CLI entry: `backend/scripts/zhaojian_cli.py`.
- Added HTTP API:
  - `GET /api/zhaojian/health`
  - `POST /api/zhaojian/run`
- Added `README_ZHAOJIAN.md`.
- Added `docs/ZHAOJIAN_ARCHITECTURE.md`.
- Added `docs/API.md`.
- Added `docs/ROADMAP.md`.
- Added `CONTRIBUTING.md`.
- Added `NOTICE.md` attribution file.

### Changed

- Updated root `README.md` for ZhaoJian project identity.
- Updated root `package.json` name and description.
- Registered ZhaoJian Flask blueprint.

### Removed

- Removed inherited GitHub workflow from original codebase to avoid token workflow-scope push issue.
