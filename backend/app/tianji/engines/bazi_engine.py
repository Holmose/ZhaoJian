"""V2 Enhanced Bazi Engine with solar-term month correction."""

from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ELEMENT_MAP = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土",
               "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
YINYANG_MAP = {"甲": "阳", "乙": "阴", "丙": "阳", "丁": "阴", "戊": "阳", "己": "阴",
               "庚": "阳", "辛": "阴", "壬": "阳", "癸": "阴"}
BRANCH_ELEMENT = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
                  "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"}

def _load_json(name: str) -> dict:
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)

TEN_GODS = _load_json("ten_gods.json")
TIANGAN_DIZHI = _load_json("tiangan_dizhi.json")
SOLAR_TERMS = _load_json("solar_terms.json")

def _stem_index(s: str) -> int:
    return HEAVENLY_STEMS.index(s)

def _branch_index(b: str) -> int:
    return EARTHLY_BRANCHES.index(b)

def _get_solar_term(year: int, month: int) -> str:
    year_str = str(year)
    if year_str not in SOLAR_TERMS:
        return "惊蛰" if month >= 3 else "立春"
    st = SOLAR_TERMS[year_str]
    month_terms = {"1": "小寒", "2": "立春", "3": "惊蛰", "4": "清明", "5": "立夏",
                   "6": "芒种", "7": "小暑", "8": "立秋", "9": "白露", "10": "寒露",
                   "11": "立冬", "12": "大雪"}
    key = month_terms.get(str(month), "惊蛰")
    return key if key in st else list(st.values())[0]

def _parse_dt(value: str) -> datetime:
    for fmt in ["%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError("birth_datetime must be YYYY-MM-DD or YYYY-MM-DD HH:MM")

def _calc_year_pillar(year: int) -> str:
    base = 1984
    offset = year - base
    stem_idx = (offset + 4) % 10
    branch_idx = (offset + 4) % 12
    return HEAVENLY_STEMS[stem_idx] + EARTHLY_BRANCHES[branch_idx]

def _calc_month_pillar(dt: datetime) -> str:
    year = dt.year
    month = dt.month
    day = dt.day
    term = _get_solar_term(year, month)
    cutoff = datetime.strptime(SOLAR_TERMS[str(year)][term], "%Y-%m-%d") if str(year) in SOLAR_TERMS else None
    if cutoff and day < cutoff.day:
        month -= 1
    if month < 1:
        month = 12
    base_year = 1984
    base_stem = 0
    base_branch = 2
    offset = year - base_year
    month_offset = (offset % 10 + month + 9) % 10
    branch_offset = (offset % 12 + month + 8) % 12
    return HEAVENLY_STEMS[month_offset] + EARTHLY_BRANCHES[branch_offset]

def _calc_day_pillar(dt: datetime) -> str:
    base = datetime(1900, 1, 1)
    days = (dt.date() - base.date()).days
    stem_idx = (days + 6) % 10
    branch_idx = (days + 0) % 12
    return HEAVENLY_STEMS[stem_idx] + EARTHLY_BRANCHES[branch_idx]

def _calc_hour_pillar(dt: datetime) -> str:
    hour = dt.hour
    offset = (hour + 1) // 2
    day_stem = _stem_index(_calc_day_pillar(dt)[:1])
    stem_idx = (day_stem * 2 + offset) % 10
    branch_idx = (hour + 1) // 2 % 12
    return HEAVENLY_STEMS[stem_idx] + EARTHLY_BRANCHES[branch_idx]

def _analyze_strength(stems: list[str], branches: list[str]) -> dict:
    counts = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
    for s in stems:
        if s in ELEMENT_MAP:
            counts[ELEMENT_MAP[s]] += 1
    for b in branches:
        if b in BRANCH_ELEMENT:
            counts[BRANCH_ELEMENT[b]] += 0.5
    total = sum(counts.values()) or 1
    balance = {k: round(v / total, 3) for k, v in counts.items()}
    max_elem = max(balance, key=balance.get)
    day_stem = stems[2]
    day_elem = ELEMENT_MAP.get(day_stem, "土")
    strength = balance[day_elem] / 0.25 if sum(balance.values()) > 0 else 1.0
    return {"balance": balance, "day_elem": day_elem, "strong_weak": "偏强" if strength > 1.1 else "偏弱" if strength < 0.9 else "中和", "dominant_elem": max_elem}

def _ten_gods(stems: list[str]) -> dict:
    day = stems[2]
    visible = {}
    for s in stems[:2]:
        if s in TEN_GODS.get(day, {}):
            visible[s] = TEN_GODS[day][s]
    return visible

def _personality(stems: list[str], branches: list[str], balance: dict) -> dict:
    day_stem = stems[2]
    day_elem = ELEMENT_MAP.get(day_stem, "土")
    biases = []
    strong = balance.get(day_elem, 0) > 0.3
    if day_stem in HEAVENLY_STEMS[:5]:
        biases.append("主见强，不喜欢被控制")
    else:
        biases.append("观察型，喜欢先想再动")
    if balance.get("木", 0) > 0.3:
        biases.append("计划性强，有目标感")
    if balance.get("火", 0) > 0.3:
        biases.append("表达欲强，善于影响他人")
    if balance.get("土", 0) > 0.3:
        biases.append("务实型，注重资源积累")
    if balance.get("金", 0) > 0.3:
        biases.append("逻辑清晰，有规则意识")
    if balance.get("水", 0) > 0.3:
        biases.append("信息敏感，善于观察变化")
    if balance.get(day_elem, 0) < 0.1:
        biases.append(f"{day_elem}偏弱处是短板，需要补")
    return biases

def _risk_pattern(stems: list[str], balance: dict, strength: str) -> list[str]:
    risks = []
    if strength == "偏强":
        risks.append("容易过度自信，高估自己掌控力")
    if strength == "偏弱":
        risks.append("压力下容易被动，需要外部支持")
    if balance.get("木", 0) > 0.4:
        risks.append("野心大但行动跟不上，容易空想")
    if balance.get("火", 0) > 0.3:
        risks.append("表面热情但底层不稳，容易虎头蛇尾")
    if balance.get("土", 0) > 0.4:
        risks.append("过于保守，容易错过窗口")
    if balance.get("金", 0) > 0.3:
        risks.append("规则感强但灵活性差，遇到新环境容易卡")
    if balance.get("水", 0) > 0.3:
        risks.append("想法多但执行弱，容易想太多做太少")
    return risks

class BaziEngine:
    def __init__(self):
        self.ten_gods = TEN_GODS

    def analyze(self, birth_datetime: str | None = None, gender: str | None = None, location: str | None = None) -> dict:
        if not birth_datetime:
            return {"status": "missing_birth_datetime", "role": "人物长期结构模型，需要 birth_datetime 参数"}
        dt = _parse_dt(birth_datetime)
        year_p = _calc_year_pillar(dt.year)
        month_p = _calc_month_pillar(dt)
        day_p = _calc_day_pillar(dt)
        hour_p = _calc_hour_pillar(dt)
        stems = [year_p[0], month_p[0], day_p[0], hour_p[0]]
        branches = [year_p[1], month_p[1], day_p[1], hour_p[1]]
        day_master = {"stem": day_p[0], "element": ELEMENT_MAP.get(day_p[0], "土"),
                      "yin_yang": YINYANG_MAP.get(day_p[0], "阳")}
        visible_tg = _ten_gods(stems)
        strength = _analyze_strength(stems, branches)
        biases = _personality(stems, branches, strength["balance"])
        risks = _risk_pattern(stems, strength["balance"], strength["strong_weak"])
        return {
            "status": "ok",
            "birth_datetime": birth_datetime,
            "gender": gender,
            "location": location,
            "pillars": {"year": year_p, "month": month_p, "day": day_p, "hour": hour_p},
            "day_master": day_master,
            "visible_ten_gods": visible_tg,
            "five_element_balance": strength["balance"],
            "dominant_element": strength["dominant_elem"],
            "strong_weak": strength["strong_weak"],
            "personality_bias": biases,
            "risk_pattern": risks,
            "agent_params": {"growth_orientation": "补" + strength["dominant_elem"] if strength["strong_weak"] == "偏弱" else strength["dominant_elem"] + "为王", "pressure_response": "主动型" if "主见强" in biases[0] else "被动型"},
            "v3_needed": ["大运流年", "用神喜忌", "格局判断", "胎元命宫"]
        }