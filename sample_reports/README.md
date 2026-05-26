# Sample Reports

This directory contains generated ZhaoJian reports from `examples/*.json`.

Each example has two outputs:

- Markdown report: human-readable ZhaoJian analysis.
- JSON report: structured `ZhaoJianState` output for API/testing integration.

## Files

- `strategy_project_launch.md/json`
- `personal_long_term_path.md/json`
- `business_customer_decision.md/json`

Regenerate:

```bash
python3 scripts/generate_sample_reports.py
```
