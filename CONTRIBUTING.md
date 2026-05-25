# Contributing to TianJi

Thank you for your interest in TianJi.

TianJi is an oriental philosophy enhanced multi-agent simulation system. Contributions should respect the project's core principle:

> Reality first, symbolic systems second, multi-path reasoning always.

## Development Setup

```bash
git clone https://github.com/Holmose/TianJi.git
cd TianJi
npm run setup
```

Backend only:

```bash
cd backend
uv sync
```

Run backend:

```bash
cd backend
uv run python run.py
```

Run TianJi CLI:

```bash
cd backend
PYTHONPATH=. python scripts/tianji_cli.py "你的问题" --domain strategy --goal "你的目标" --out reports/tianji
```

## Contribution Areas

### 1. Symbolic Datasets

- Full 64 IChing hexagram dataset.
- Bagua semantic extensions.
- Wuxing relationship rules.
- Heavenly stems and earthly branches.
- Ten gods.
- Qimen symbols.

### 2. Engines

- Bazi engine.
- Qimen engine.
- IChing transition engine.
- Causal timeline engine.
- Future branch engine.
- Confidence calibration engine.

### 3. Multi-Agent Integration

- Replace local adapter with full Hermes/MiroFish simulation.
- Add TianJi-specific agent profiles.
- Add Skeptic Agent and Synthesizer Agent prompts.
- Add report agent improvements.

### 4. Frontend

- TianJi simulation page.
- Report viewer.
- Symbolic state visualization.
- Future branch graph.
- Past causal timeline graph.

### 5. Tests

- Unit tests for symbolic mapping.
- CLI snapshot tests.
- API tests.
- Regression tests for report structure.

## Pull Request Rules

1. Keep TianJi output probabilistic and evidence-aware.
2. Do not introduce deterministic fortune-telling claims.
3. Add documentation for new engines or data formats.
4. Keep output JSON backward compatible when possible.
5. Include sample input/output when changing report behavior.
6. Avoid hardcoding API keys, tokens, or credentials.

## Coding Style

- Python 3.10+
- Prefer small modules with clear contracts.
- Keep engine outputs JSON-serializable.
- Do not mix frontend and backend changes unless necessary.

## Safety Boundaries

TianJi may assist with strategic analysis, but it must not replace professional advice in:

- medical decisions
- legal decisions
- financial/investment decisions
- emergency or safety-critical decisions

## License

TianJi is currently based on MiroFish codebase and follows AGPL-3.0. See `LICENSE` and `NOTICE.md`.
