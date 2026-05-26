from __future__ import annotations

import argparse
from pathlib import Path
from app.zhaojian.orchestrator import ZhaoJianOrchestrator
from app.zhaojian.report_generator import ZhaoJianReportGenerator


def main() -> None:
    p = argparse.ArgumentParser(description="ZhaoJian oriental philosophy enhanced simulation CLI")
    p.add_argument("question", help="要推演的问题/背景")
    p.add_argument("--domain", default="unknown", help="relationship/business/content/personal/strategy/unknown")
    p.add_argument("--goal", default="", help="用户目标")
    p.add_argument("--event-time", default=None, help="事件时间，可选")
    p.add_argument("--location", default=None, help="地点，可选")
    p.add_argument("--birth-datetime", default=None, help="出生时间，用于V2四柱人物结构：YYYY-MM-DD HH:MM")
    p.add_argument("--gender", default=None, help="性别，可选，用于后续大运方向等扩展")
    p.add_argument("--rounds", type=int, default=3, help="推演轮次，V1本地适配器默认3")
    p.add_argument("--out", default="reports/zhaojian", help="输出目录")
    args = p.parse_args()

    state = ZhaoJianOrchestrator().run(args.question, args.domain, args.goal, args.event_time, args.location, args.rounds, args.birth_datetime, args.gender)
    paths = ZhaoJianReportGenerator().save(state, Path(args.out))
    print(paths["markdown"])
    print(paths["json"])

if __name__ == "__main__":
    main()
