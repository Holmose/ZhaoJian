# Examples

This directory contains ready-to-run TianJi simulation inputs.

## Run an example through CLI

```bash
cd backend
PYTHONPATH=. python scripts/tianji_cli.py \
  "这个天机推演系统还没完全成熟，未来适不适合继续扩张和公开发布？" \
  --domain strategy \
  --goal "判断项目发布与扩张路线" \
  --event-time "2026-05-26 22:10" \
  --location "Guangzhou" \
  --birth-datetime "1998-06-15 14:30" \
  --gender male \
  --out reports/tianji
```

## Generate sample reports

From repository root:

```bash
python3 scripts/generate_sample_reports.py
```

Generated reports are written to:

```text
sample_reports/
```

## Included examples

- `strategy_project_launch.json`: project launch / expansion strategy.
- `personal_long_term_path.json`: long-term personal path and structure fit.
- `business_customer_decision.json`: business customer conversion decision.
