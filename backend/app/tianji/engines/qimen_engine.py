from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class QimenEngine:
    """V3 semantic Qimen situation engine.

    V3 scope:
    - event time based deterministic symbolic layout
    - nine palaces / eight doors / nine stars / eight gods semantic mapping
    - host/guest hints
    - timing and risk suggestions

    This is not a complete traditional Qimen Dunjia calendar engine yet.
    It is a situation-modeling layer for TianJi agents.
    """

    def __init__(self) -> None:
        self.palaces = json.loads((DATA_DIR / "jiugong.json").read_text(encoding="utf-8"))
        self.doors = json.loads((DATA_DIR / "bamen.json").read_text(encoding="utf-8"))
        self.stars = json.loads((DATA_DIR / "jiuxing.json").read_text(encoding="utf-8"))
        self.gods = json.loads((DATA_DIR / "bashen.json").read_text(encoding="utf-8"))
        self.palace_order = list(self.palaces.keys())
        self.door_order = list(self.doors.keys())
        self.star_order = list(self.stars.keys())
        self.god_order = list(self.gods.keys())

    def analyze(self, event_time: str | None = None, location: str | None = None, question: str = "", domain: str = "unknown") -> dict:
        if not event_time:
            return {"status": "missing_event_time", "role": "具体事件局势与行动时机，需要 event_time 才能起语义局"}
        dt = self._parse_dt(event_time)
        seed = self._seed(dt, question, domain)
        palace = self.palace_order[seed % len(self.palace_order)]
        door = self.door_order[(seed + dt.hour) % len(self.door_order)]
        star = self.star_order[(seed + dt.day) % len(self.star_order)]
        god = self.god_order[(seed + dt.month) % len(self.god_order)]
        bureau = self._bureau(dt)
        host_guest = self._host_guest(door, god, domain)
        return {
            "status": "ok",
            "note": "V3 uses semantic Qimen layout, not yet full traditional solar-term Qimen calculation.",
            "event_time": event_time,
            "location": location,
            "bureau": bureau,
            "main_palace": {"name": palace, **self.palaces[palace]},
            "door": {"name": door, **self.doors[door]},
            "star": {"name": star, **self.stars[star]},
            "god": {"name": god, **self.gods[god]},
            "host_guest": host_guest,
            "situation_signal": self._signals(palace, door, star, god),
            "timing_hint": self._timing_hint(door, star, god),
            "risk_hint": self._risk_hint(door, star, god),
            "action_hint": self._action_hint(door, god),
            "v4_needed": ["solar_terms", "yin_yang_dun", "ju_number", "heaven_earth_plate", "useful_god_selection"]
        }

    def _parse_dt(self, value: str) -> datetime:
        for fmt in ["%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                pass
        raise ValueError("event_time must be YYYY-MM-DD or YYYY-MM-DD HH:MM")

    def _seed(self, dt: datetime, question: str, domain: str) -> int:
        return dt.year + dt.month * 3 + dt.day * 5 + dt.hour * 7 + len(question) + len(domain)

    def _bureau(self, dt: datetime) -> dict:
        yang = dt.month in [1, 2, 3, 4, 5, 6]
        ju = ((dt.month + dt.day + dt.hour) % 9) + 1
        return {"dun": "阳遁" if yang else "阴遁", "ju": ju, "label": f"{'阳遁' if yang else '阴遁'}{ju}局"}

    def _host_guest(self, door: str, god: str, domain: str) -> dict:
        active_doors = ["开门", "生门", "景门", "伤门"]
        relation_gods = ["六合", "太阴", "九地"]
        posture = "主动方占优" if door in active_doors else "被动方/环境约束较强"
        relation = "适合协商整合" if god in relation_gods else "需先处理权力、风险或信息问题"
        return {"posture": posture, "relation": relation, "domain": domain}

    def _signals(self, palace: str, door: str, star: str, god: str) -> list[str]:
        return [
            f"主宫{palace}：{'、'.join(self.palaces[palace]['keywords'])}",
            f"主门{door}：{'、'.join(self.doors[door]['keywords'])}",
            f"主星{star}：{'、'.join(self.stars[star]['keywords'])}",
            f"主神{god}：{'、'.join(self.gods[god]['keywords'])}"
        ]

    def _timing_hint(self, door: str, star: str, god: str) -> str:
        quality = self.doors[door]["quality"]
        if "吉" in quality and god in ["六合", "九天", "值符"]:
            return "窗口偏开，可小步推进并观察反馈"
        if "凶" in quality:
            return "窗口不稳，先控风险或等待新信号"
        return "窗口中性，适合试探、验证、低成本行动"

    def _risk_hint(self, door: str, star: str, god: str) -> list[str]:
        risks = [self.doors[door]["action_hint"], self.stars[star]["risk"], self.gods[god]["hint"]]
        return risks

    def _action_hint(self, door: str, god: str) -> str:
        return f"{self.doors[door]['action_hint']}；{self.gods[god]['hint']}"
