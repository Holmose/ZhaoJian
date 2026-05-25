from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime
from collections import Counter

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class BaziEngine:
    """V2 basic Bazi natal pattern engine.

    This engine provides an approximate solar-calendar Four Pillars model.
    It is designed as a long-term personality/cycle parameter provider for
    TianJi agents, not as deterministic fate prediction.

    V2 scope:
    - approximate year/month/day/hour pillars
    - day master
    - ten gods for visible stems
    - five element balance
    - personality/risk/action parameters

    Future improvements:
    - solar term based month pillar
    - precise calendar conversion
    - luck cycles
    - strength/weakness and useful god analysis
    """

    def __init__(self) -> None:
        base = json.loads((DATA_DIR / "tiangan_dizhi.json").read_text(encoding="utf-8"))
        self.stems = base["stems_order"]
        self.branches = base["branches_order"]
        self.stem_info = base["heavenly_stems"]
        self.branch_info = base["earthly_branches"]
        self.ten_gods = json.loads((DATA_DIR / "ten_gods.json").read_text(encoding="utf-8"))

    def analyze(self, birth_datetime: str | None = None, gender: str | None = None, location: str | None = None) -> dict:
        if not birth_datetime:
            return {"status": "missing_birth_datetime", "role": "人物长期结构模型，需要 birth_datetime 才能计算", "required_format": "YYYY-MM-DD HH:MM"}
        dt = self._parse_dt(birth_datetime)
        year = self._year_pillar(dt.year)
        month = self._month_pillar(dt.year, dt.month)
        day = self._day_pillar(dt)
        hour = self._hour_pillar(day[0], dt.hour)
        pillars = {"year": year, "month": month, "day": day, "hour": hour}
        day_master = day[0]
        elements = self._element_balance(pillars)
        visible_ten_gods = self._visible_ten_gods(day_master, pillars)
        return {
            "status": "ok",
            "note": "V2 uses approximate solar-calendar pillars; month pillar is not yet solar-term corrected.",
            "birth_datetime": birth_datetime,
            "gender": gender,
            "location": location,
            "pillars": pillars,
            "day_master": {"stem": day_master, **self.stem_info[day_master]},
            "ten_gods": visible_ten_gods,
            "five_element_balance": elements,
            "dominant_elements": self._dominant(elements),
            "personality_bias": self._personality(day_master, elements, visible_ten_gods),
            "risk_pattern": self._risks(day_master, elements, visible_ten_gods),
            "agent_parameters": self._agent_params(day_master, elements, visible_ten_gods),
            "v3_needed": ["solar_terms", "luck_cycles", "strength_analysis", "useful_god"]
        }

    def _parse_dt(self, value: str) -> datetime:
        for fmt in ["%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                pass
        raise ValueError("birth_datetime must be YYYY-MM-DD or YYYY-MM-DD HH:MM")

    def _year_pillar(self, year: int) -> str:
        # 1984 is JiaZi year. Approximate: no LiChun correction in V2.
        idx = (year - 1984) % 60
        return self.stems[idx % 10] + self.branches[idx % 12]

    def _month_pillar(self, year: int, month: int) -> str:
        # Approximate month branch: 寅 starts around February. No solar-term correction.
        month_branches = ["丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子"]
        branch = month_branches[month - 1]
        year_stem_idx = (year - 1984) % 10
        first_month_stem_idx = ((year_stem_idx % 5) * 2 + 2) % 10
        stem = self.stems[(first_month_stem_idx + month - 1) % 10]
        return stem + branch

    def _day_pillar(self, dt: datetime) -> str:
        # Known reference: 2000-01-01 approximated as 戊辰 in common calendars.
        ref = datetime(2000, 1, 1)
        ref_idx = self._jiazi_index("戊辰")
        idx = (ref_idx + (dt.date() - ref.date()).days) % 60
        return self.stems[idx % 10] + self.branches[idx % 12]

    def _hour_pillar(self, day_stem: str, hour: int) -> str:
        branch_idx = ((hour + 1) // 2) % 12
        day_stem_idx = self.stems.index(day_stem)
        first_hour_stem_idx = (day_stem_idx % 5) * 2 % 10
        stem = self.stems[(first_hour_stem_idx + branch_idx) % 10]
        return stem + self.branches[branch_idx]

    def _jiazi_index(self, pillar: str) -> int:
        for i in range(60):
            if self.stems[i % 10] + self.branches[i % 12] == pillar:
                return i
        raise ValueError(pillar)

    def _element_balance(self, pillars: dict) -> dict:
        c = Counter()
        for p in pillars.values():
            stem, branch = p[0], p[1]
            c[self.stem_info[stem]["element"]] += 1.0
            c[self.branch_info[branch]["element"]] += 1.0
            for hs in self.branch_info[branch].get("hidden_stems", []):
                c[self.stem_info[hs]["element"]] += 0.25
        total = sum(c.values()) or 1
        return {e: round(c[e] / total, 3) for e in ["木", "火", "土", "金", "水"]}

    def _visible_ten_gods(self, day_master: str, pillars: dict) -> dict:
        return {k: self.ten_gods[day_master][v[0]] for k, v in pillars.items() if k != "day"}

    def _dominant(self, elements: dict) -> list[str]:
        return [k for k, _ in sorted(elements.items(), key=lambda x: x[1], reverse=True)[:2]]

    def _personality(self, dm: str, elements: dict, gods: dict) -> list[str]:
        element = self.stem_info[dm]["element"]
        bias = {
            "木": "重成长与规划，喜欢开新枝，但需要稳定落地",
            "火": "重表达与影响，容易被反馈点燃，也要防情绪过载",
            "土": "重承载与现实，适合做长期盘，但要防迟滞",
            "金": "重规则与决断，适合切问题，但要防过硬",
            "水": "重信息与流动，擅长观察变化，但要防犹疑"
        }[element]
        result = [bias]
        if "正官" in gods.values() or "七杀" in gods.values(): result.append("对规则、压力或竞争环境敏感")
        if "正财" in gods.values() or "偏财" in gods.values(): result.append("资源、结果和交换价值会明显影响决策")
        if "食神" in gods.values() or "伤官" in gods.values(): result.append("表达、创造和输出欲望较强")
        if "正印" in gods.values() or "偏印" in gods.values(): result.append("学习、认知和安全感需求较高")
        return result

    def _risks(self, dm: str, elements: dict, gods: dict) -> list[str]:
        risks = []
        high = max(elements, key=elements.get)
        low = min(elements, key=elements.get)
        risks.append(f"{high}偏旺时容易路径依赖，{low}偏弱处是补课方向")
        if "伤官" in gods.values(): risks.append("表达锋利时容易挑战规则，需要控制输出边界")
        if "七杀" in gods.values(): risks.append("压力驱动强，但高压下容易走极端动作")
        if not risks: risks.append("信息不足，暂不做过度人格推断")
        return risks

    def _agent_params(self, dm: str, elements: dict, gods: dict) -> dict:
        return {
            "decision_style": self._personality(dm, elements, gods)[0],
            "resource_sensitivity": "正财" in gods.values() or "偏财" in gods.values(),
            "rule_pressure_sensitivity": "正官" in gods.values() or "七杀" in gods.values(),
            "expression_drive": "食神" in gods.values() or "伤官" in gods.values(),
            "learning_security_need": "正印" in gods.values() or "偏印" in gods.values()
        }
