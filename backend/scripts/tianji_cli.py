from __future__ import annotations

import argparse
from pathlib import Path
from app.tianji.orchestrator import TianJiOrchestrator
from app.tianji.report_generator import TianJiReportGenerator


def main() -> None:
    p = argparse.ArgumentParser(description="TianJi oriental philosophy enhanced simulation CLI")
    p.add_argument("question", help="要推演的问题/背景")
    p.add_argument("--domain", default="unknown", help="relationship/business/content/personal/strategy/unknown")
    p.add_argument("--goal", default="", help="用户目标")
    p.add_argument("--event-time", default=None, help="事件时间，可选")
    p.add_argument("--location", default=None, help="地点，可选")
    p.add_argument("--rounds", type=int, default=3, help="推演轮次，V1本地适配器默认3")
    p.add_argument("--out", default="reports/tianji", help="输出目录")
    args = p.parse_args()

    state = TianJiOrchestrator().run(args.question, args.domain, args.goal, args.event_time, args.location, args.rounds)
    paths = TianJiReportGenerator().save(state, Path(args.out))
    print(paths["markdown"])
    print(paths["json"])

if __name__ == "__main__":
    main()
