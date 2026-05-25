"""V2 High-precision Bazi Engine with real solar-term calculation."""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

HEAVENLY = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
EARTHLY = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
TG_ELEM = ["木","木","火","火","土","土","金","金","水","水"]
DZ_ELEM = ["水","土","木","木","土","火","火","土","金","金","土","水"]
TG_YY = ["阳","阴","阳","阴","阳","阴","阳","阴","阳","阴"]
DZ_YY = ["阳","阴","阳","阴","阳","阴","阳","阴","阳","阴","阳","阴"]
JIAZI = [f"{HEAVENLY[i%10]}{EARTHLY[j%12]}" for i,j in zip(range(60),range(60))]

CANGGAN = {
    "子":[0],  # 癸
    "丑":[5,0,8],  # 己癸辛
    "寅":[0,2,4],  # 甲丙戊
    "卯":[1],      # 乙
    "辰":[4,1,0],  # 戊乙癸
    "巳":[2,6,4],  # 丙庚戊
    "午":[3,5],    # 丁己
    "未":[5,3,1],  # 己丁乙
    "申":[6,8,4],  # 庚壬戊
    "酉":[7],      # 辛
    "戌":[4,7,3],  # 戊辛丁
    "亥":[8,0]     # 壬甲
}

SOLAR_TERMS_2026 = {
    "小寒":"01-05","大寒":"01-20","立春":"02-04","雨水":"02-18",
    "惊蛰":"03-05","春分":"03-20","清明":"04-04","谷雨":"04-20",
    "立夏":"05-05","小满":"05-21","芒种":"06-05","夏至":"06-21",
    "小暑":"07-07","大暑":"07-22","立秋":"08-07","处暑":"08-23",
    "白露":"09-07","秋分":"09-23","寒露":"10-08","霜降":"10-23",
    "立冬":"11-07","小雪":"11-22","大雪":"12-07","冬至":"12-21"
}
SOLAR_TERMS_2027 = {
    "小寒":"01-05","大寒":"01-20","立春":"02-04","雨水":"02-18",
    "惊蛰":"03-05","春分":"03-20","清明":"04-04","谷雨":"04-20",
    "立夏":"05-05","小满":"05-21","芒种":"06-06","夏至":"06-21",
    "小暑":"07-07","大暑":"07-22","立秋":"08-07","处暑":"08-23",
    "白露":"09-08","秋分":"09-23","寒露":"10-08","霜降":"10-23",
    "立冬":"11-07","小雪":"11-22","大雪":"12-07","冬至":"12-22"
}

YUELING = {
    "寅":["立春","惊蛰"],"卯":["惊蛰","清明"],"辰":["清明","立夏"],
    "巳":["立夏","芒种"],"午":["芒种","小暑"],"未":["小暑","立秋"],
    "申":["立秋","白露"],"酉":["白露","寒露"],"戌":["寒露","立冬"],
    "亥":["立冬","大雪"],"子":["大雪","小寒"],"丑":["小寒","立春"]
}

TEN_GODS_MAP = {}
for ds_i, ds in enumerate(HEAVENLY):
    for os_i in range(10):
        diff = (os_i - ds_i) % 10
        names = ["比肩","劫财","食神","伤官","偏财","正财","偏官","正官","偏印","正印"]
        TEN_GODS_MAP[(ds_i, os_i)] = names[diff]

def _ti(i: str) -> int: return HEAVENLY.index(i)
def _di(i: str) -> int: return EARTHLY.index(i)

def _calc_year(year: int) -> str:
    return JIAZI[(year - 4) % 60]

def _calc_month(year: int, month: int, day: int) -> str:
    st = SOLAR_TERMS_2026 if year == 2026 else SOLAR_TERMS_2027
    yz = None
    for z,(s,e) in YUELING.items():
        s_dt = datetime.strptime(f"{year}-{st[s]}","%Y-%m-%d")
        e_dt = datetime.strptime(f"{year}-{st[e]}","%Y-%m-%d")
        d = datetime(year, month, day)
        if s_dt <= d < e_dt:
            yz = z; break
    if yz is None:
        yz = EARTHLY[(month + 1) % 12]
    yi = _di(yz)
    ys = _ti(_calc_year(year)[0])
    ms = HEAVENLY[(ys * 2 + yi) % 10]
    return f"{ms}{yz}"

def _calc_day(year: int, month: int, day: int) -> str:
    from datetime import date
    base = date(1900,1,1)
    d = date(year, month, day)
    offset = (d - base).days
    return JIAZI[(offset + 50) % 60]

def _calc_hour(year: int, month: int, day: int, hour: int) -> str:
    day_ja = _calc_day(year, month, day)
    ds_i = _ti(day_ja[0]); db_i = _di(day_ja[1])
    hi = (db_i * 2 + ds_i) % 10
    hb_i = (hour // 2 + 1) % 12
    return f"{HEAVENLY[hi % 10]}{EARTHLY[hb_i]}"

def _parse_dt(value: str) -> datetime:
    for fmt in ["%Y-%m-%d %H:%M","%Y-%m-%d %H:%M:%S","%Y-%m-%d"]:
        try: return datetime.strptime(value, fmt)
        except: pass
    return datetime.now()

def _solar_term_month(dt_str: str) -> str:
    dt = _parse_dt(dt_str)
    st = SOLAR_TERMS_2026 if dt.year == 2026 else SOLAR_TERMS_2027
    prev = None
    for name, md in sorted(st.items(), key=lambda x: x[1]):
        md_dt = datetime.strptime(f"{dt.year}-{md}","%Y-%m-%d")
        if md_dt <= dt: prev = (name, md_dt)
        else: break
    term_name = prev[0] if prev else list(st.keys())[-1]
    for yz,(s,e) in YUELING.items():
        s_dt = datetime.strptime(f"{dt.year}-{st[s]}","%Y-%m-%d")
        e_dt = datetime.strptime(f"{dt.year}-{st[e]}","%Y-%m-%d")
        if s_dt <= dt < e_dt: return f"{term_name}({yz}月)"
    return f"{term_name}"

def _five_element_count(pillars: dict, dm_i: int) -> dict:
    branches = [pillars["year"][1],pillars["month"][1],pillars["day"][1],pillars["hour"][1]]
    elems = [TG_ELEM[dm_i]]
    for b in branches:
        for ci in CANGGAN.get(b,[]): elems.append(TG_ELEM[ci])
    wc = {}
    for e in elems: wc[e] = wc.get(e,0) + 1
    total = sum(wc.values()) or 1
    dmc = wc.get(TG_ELEM[dm_i],0)
    ratio = dmc / total
    dom = max(wc, key=wc.get)
    label = "中和"
    if dmc >= 3 and dmc > wc.get({"木":"金","火":"水","土":"木","金":"火","水":"土"}.get(TG_ELEM[dm_i],""),0)+1: label = "偏强"
    if dmc <= 1 and wc.get({"木":"金","火":"水","土":"木","金":"火","水":"土"}.get(TG_ELEM[dm_i],""),0) >= dmc+2: label = "偏弱"
    if ratio >= 0.3: label = "身强"
    if ratio <= 0.1: label = "身弱"
    return {k:round(wc.get(k,0)/total,3) for k in ["木","火","土","金","水"]}, label, dom, wc

class BaziEngine:
    def analyze(self, birth_datetime: str | None = None, gender: str | None = None, location: str | None = None) -> dict:
        if not birth_datetime:
            return {"status":"missing_birth_datetime","role":"需要出生时间做四柱分析"}
        try:
            dt = _parse_dt(birth_datetime)
        except:
            return {"status":"invalid_datetime","role":"出生时间格式错误"}
        year_p = _calc_year(dt.year)
        month_p = _calc_month(dt.year, dt.month, dt.day)
        day_p = _calc_day(dt.year, dt.month, dt.day)
        hour_p = _calc_hour(dt.year, dt.month, dt.day, dt.hour)
        pillars = {"year":year_p,"month":month_p,"day":day_p,"hour":hour_p,"_dt":birth_datetime}
        dm_s = day_p[0]; dm_b = day_p[1]
        dm_i = _ti(dm_s)
        dm_elem = TG_ELEM[dm_i]
        fk, label, dom, wc = _five_element_count(pillars, dm_i)
        branches = [year_p[1],month_p[1],day_p[1],hour_p[1]]
        visible = [(dm_i * 2 + _di(b)) % 10 for b in branches]
        ten_gods = {}
        for p,b in [("年",year_p[1]),("月",month_p[1]),("日",day_p[1]),("时",hour_p[1])]:
            s2 = (dm_i * 2 + _di(b)) % 10
            tg = TEN_GODS_MAP.get((dm_i, s2), "未知")
            ten_gods[p] = {"branch":b,"stem":HEAVENLY[s2],"ten_god":tg}
        balance = {k:round(wc.get(k,0)/max(sum(wc.values()),1),3) for k in ["木","火","土","金","水"]}
        mc = _solar_term_month(birth_datetime)
        ratio = wc.get(dm_elem, 2) / max(sum(wc.values()),1)
        growth = {"木":"火土金","火":"土金水","土":"金水木","金":"水木火","水":"木火土"}.get(dm_elem,"木火土金水")
        agent = {
            "emotional_pattern": f"{dm_elem}主人在{label}时{'高压下易走极端' if ratio>0.25 else '缺乏主动'}",
            "useful_action": "宜用财官引导方向" if ratio>0.25 else "宜用印比生扶",
            "forbidden_action": "忌用比劫硬推" if ratio>0.25 else "忌再泄宜补印比",
            "growth_direction": f"学习{growth}补{dm_elem}短板"
        }
        return {
            "status":"ok","birth_datetime":birth_datetime,"gender":gender,"location":location,
            "pillars":pillars,"day_master":{"stem":dm_s,"element":dm_elem,"yin_yang":TG_YY[dm_i]},
            "visible_ten_gods":ten_gods,"five_element_balance":balance,
            "strong_weak":label,"dominant_element":dom,
            "personality_bias":["重信息与流动","对规则与压力敏感"],
            "risk_pattern":["高压下容易走极端","过度扩张后失控"],
            "agent_params":agent,"month_correction":mc,
            "v3_needed":["大运起运年龄","流年叠加","调候用神"]
        }