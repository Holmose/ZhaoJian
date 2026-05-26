from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.zhaojian.orchestrator import ZhaoJianOrchestrator
from app.zhaojian.report_generator import ZhaoJianReportGenerator


def main() -> None:
    examples_dir = ROOT / "examples"
    out_dir = ROOT / "sample_reports"
    out_dir.mkdir(exist_ok=True)
    orch = ZhaoJianOrchestrator()
    gen = ZhaoJianReportGenerator()
    for path in sorted(examples_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        state = orch.run(
            question=data["question"],
            domain=data.get("domain", "unknown"),
            goal=data.get("goal", ""),
            event_time=data.get("event_time"),
            location=data.get("location"),
            rounds=int(data.get("rounds", 3)),
            birth_datetime=data.get("birth_datetime"),
            gender=data.get("gender"),
        )
        stem = path.stem
        md = out_dir / f"{stem}.md"
        js = out_dir / f"{stem}.json"
        md.write_text(gen.render_markdown(state), encoding="utf-8")
        js.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        print(md)
        print(js)

if __name__ == "__main__":
    main()
