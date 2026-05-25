"""High-precision Bazi Precision Engine v2."""
from __future__ import annotations

TIANGAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
TG_INDEX = {k:i for i,k in enumerate(TIANGAN)}
TG_WUXING = ["木","木","火","火","土","土","金","金","水","水"]

DIZHI = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
DZ_INDEX = {k:i for i,k in enumerate(DIZHI)}
DZ_WUXING = ["水","土","木","木","土","火","火","土","金","金","土","水"]

JIAZI = [f"{TIANGAN[i%10]}{DIZHI[j%12]}" for i,j in zip(range(60),range(60))]

CANGGAN = {
    "子":[TG_INDEX["癸"]],
    "丑":[TG_INDEX["己"],TG_INDEX["癸"],TG_INDEX["辛"]],
    "寅":[TG_INDEX["甲"],TG_INDEX["丙"],TG_INDEX["戊"]],
    "卯":[TG_INDEX["乙"]],
    "辰":[TG_INDEX["戊"],TG_INDEX["乙"],TG_INDEX["癸"]],
    "巳":[TG_INDEX["丙"],TG_INDEX["庚"],TG_INDEX["戊"]],
    "午":[TG_INDEX["丁"],TG_INDEX["己"]],
    "未":[TG_INDEX["己"],TG_INDEX["丁"],TG_INDEX["乙"]],
    "申":[TG_INDEX["庚"],TG_INDEX["壬"],TG_INDEX["戊"]],
    "酉":[TG_INDEX["辛"]],
    "戌":[TG_INDEX["戊"],TG_INDEX["辛"],TG_INDEX["丁"]],
    "亥":[TG_INDEX["壬"],TG_INDEX["甲"]]
}

YUELING_MONTH = {
    "寅":["立春","惊蛰"],"卯":["惊蛰","清明"],"辰":["清明","立夏"],
    "巳":["立夏","芒种"],"午":["芒种","小暑"],"未":["小暑","立秋"],
    "申":["立秋","白露"],"酉":["白露","寒露"],"戌":["寒露","立冬"],
    "亥":["立冬","大雪"],"子":["大雪","小寒"],"丑":["小寒","立春"]
}

ST_2026 = {
    "小寒":"01-05","大寒":"01-20","立春":"02-04","雨水":"02-18",
    "惊蛰":"03-05","春分":"03-20","清明":"04-04","谷雨":"04-20",
    "立夏":"05-05","小满":"05-21","芒种":"06-05","夏至":"06-21",
    "小暑":"07-07","大暑":"07-22","立秋":"08-07","处暑":"08-23",
    "白露":"09-07","秋分":"09-23","寒露":"10-08","霜降":"10-23",
    "立冬":"11-07","小雪":"11-22","大雪":"12-07","冬至":"12-21"
}
ST_2027 = {
    "小寒":"01-05","大寒":"01-20","立春":"02-04","雨水":"02-18",
    "惊蛰":"03-05","春分":"03-20","清明":"04-04","谷雨":"04-20",
    "立夏":"05-05","小满":"05-21","芒种":"06-06","夏至":"06-21",
    "小暑":"07-07","大暑":"07-22","立秋":"08-07","处暑":"08-23",
    "白露":"09-08","秋分":"09-23","寒露":"10-08","霜降":"10-23",
    "立冬":"11-07","小雪":"11-22","大雪":"12-07","冬至":"12-22"
}

NEED_ELEM = {"木":"金","火":"水","土":"木","金":"火","水":"土"}
CONTROL_ELEM = {"木":"金","火":"水","土":"木","金":"火","土":"土"}
SUPPORT_ELEM = {"木":"水","火":"木","土":"火","金":"土","水":"金"}

def _ten_god(ds: int, os: int) -> str:
    if ds == os: return "比肩"
    diff = (os - ds) % 10
    return ["劫财","食神","伤官","偏财","正财","偏官","正官","偏印","正印","比肩"][diff]

def _branch_stem(year: int, month: int, day: int, hour: int) -> dict:
    # 六十甲子年柱
    year_ja = JIAZI[(year - 4) % 60]
    year_stem = year_ja[0]; year_branch = year_ja[1]
    yi = DZ_INDEX[year_branch]; ysi = TG_INDEX[year_stem]
    # 月柱
    month_branch_list = ["寅","卯","辰","巳","午","未","申","酉","戌","亥","子","丑"]
    mz = month_branch_list[(month + 1) % 12]
    msi = (ysi * 2 + yi) % 10
    ms = TIANGAN[msi % 10]
    # 日柱：简化用儒略日近似
    from datetime import date
    d0 = date(1900,1,1); d1 = date(year,month,day)
    days = (d1 - d0).days
    di = (days + 40) % 60
    day_ja = JIAZI[di]
    ds = day_ja[0]; db = day_ja[1]
    dsi = TG_INDEX[ds]; dbi = DZ_INDEX[db]
    # 时柱
    hsi = (dsi * 2) % 10
    hbi = (dbi + 1) % 12
    hs = TIANGAN[hsi % 10]; hb = DIZHI[hbi]
    return {
        "year": f"{year_stem}{year_branch}",
        "month": f"{ms}{mz}",
        "day": f"{ds}{db}",
        "hour": f"{hs}{hb}",
        "day_stem_idx": dsi, "day_branch_idx": dbi,
        "year_stem_idx": TG_INDEX[year_stem],
        "month_stem_idx": msi % 10,
        "hour_stem_idx": hsi % 10
    }

def _solar_term_month(dt_str: str) -> str:
    from datetime import datetime
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except:
        try:
            dt = datetime.strptime(dt_str.split()[0], "%Y-%m-%d")
        except:
            return "未知月令"
    st = ST_2026 if dt.year == 2026 else ST_2027
    prev = None
    for name, md in sorted(st.items(), key=lambda x: x[1]):
        md_dt = datetime.strptime(f"{dt.year}-{md}", "%Y-%m-%d")
        if md_dt <= dt:
            prev = (name, md_dt)
        else:
            break
    if not prev:
        prev = list(sorted(st.items(), key=lambda x: x[1]))[-1]
    term_name, term_dt = prev
    for yz, (s,e) in YUELING_MONTH.items():
        s_dt = datetime.strptime(f"{dt.year}-{st[s]}", "%Y-%m-%d")
        e_dt = datetime.strptime(f"{dt.year}-{st[e]}", "%Y-%m-%d")
        if s_dt <= dt < e_dt:
            return f"{term_name}({yz}月)"
    return f"{term_name}"

def _calc_balance(pillars: dict, dm: dict) -> dict:
    dsi = TG_INDEX[dm["stem"]]
    dbi = DZ_INDEX[pillars["day"][1]]
    branches = [pillars["year"][1], pillars["month"][1], pillars["day"][1], pillars["hour"][1]]
    visible = []
    for b in branches:
        stem = (dsi * 2 + DZ_INDEX[b]) % 10
        visible.append(stem)
    all_elem = [TG_WUXING[dsi]]
    for b in branches:
        if b in CANGGAN:
            all_elem.append(TG_WUXING[CANGGAN[b][0]])
    wc = {}
    for e in all_elem:
        wc[e] = wc.get(e,0) + 1
    total = sum(wc.values()) or 1
    dmc = wc.get(dm["element"], 0)
    label = "中和"
    if dmc >= 3 and dmc > wc.get(NEED_ELEM.get(dm["element"],""),0)+1:
        label = "偏强"
    if dmc <= 1 and wc.get(NEED_ELEM.get(dm["element"],""),0) >= dmc + 2:
        label = "偏弱"
    ratio = dmc / total
    if ratio >= 0.3: label = "身强"
    if ratio <= 0.1: label = "身弱"
    dom = max(wc, key=wc.get)
    bal = {k: round(wc.get(k,0)/total, 3) for k in ["木","火","土","金","水"]}
    return label, dom, bal, wc

def _calc_useful(dsi: int, dbi: int, ratio: float, wc: dict) -> dict:
    dm_elem = TG_WUXING[dsi]
    # element to stem mapping (first occurrence)
    elem_to_stem = {}
    for i, e in enumerate(TG_WUXING):
        if e not in elem_to_stem:
            elem_to_stem[e] = i
    # what this element needs to control
    need_elem = NEED_ELEM.get(dm_elem, dm_elem)
    ctrl_elem = CONTROL_ELEM.get(dm_elem, dm_elem)
    supp_elem = SUPPORT_ELEM.get(dm_elem, dm_elem)
    need_stem = elem_to_stem.get(need_elem, dsi)
    ctrl_stem = elem_to_stem.get(ctrl_elem, (dsi+5)%10)
    supp_stem = elem_to_stem.get(supp_elem, dsi)
    if ratio > 0.25:
        useful = [TIANGAN[need_stem], TIANGAN[ctrl_stem]]
        note = "身强宜用财官抑身"
    else:
        useful = [TIANGAN[supp_stem], TIANGAN[need_stem]]
        note = "身弱宜用印比生扶"
    return {"stems": useful, "note": note}

def _calc_forbidden(dsi: int, dbi: int, ratio: float) -> dict:
    dm_elem = TG_WUXING[dsi]
    same_elem_stems = [i for i in range(10) if TG_WUXING[i] == dm_elem]
    if ratio > 0.25:
        forbidden = [TIANGAN[i] for i in same_elem_stems]
        note = "比劫过旺则争宜收敛"
    else:
        forbidden = [TIANGAN[dsi]]
        note = "身弱忌再泄宜补印比"
    return {"stems": forbidden, "note": note}

def _growth(dm_elem: str) -> str:
    cycle = {"木":"火土金","火":"土金水","土":"金水木","金":"水木火","水":"木火土"}
    return cycle.get(dm_elem, "木火土金水")

class BaziPrecisionEngine:
    def analyze(self, pillars: dict, day_master: dict, strength: str, dominant_element: str, five_element_balance: dict) -> dict:
        dsi = TG_INDEX[day_master["stem"]]
        dbi = DZ_INDEX[pillars["day"][1]]
        dm_elem = day_master["element"]
        branches = [pillars["year"][1], pillars["month"][1], pillars["day"][1], pillars["hour"][1]]
        visible = []
        ten_gods = {}
        hidden = {}
        for p, b in [("年",branches[0]),("月",branches[1]),("日",branches[2]),("时",branches[3])]:
            s2 = (dsi * 2 + DZ_INDEX[b]) % 10
            visible.append(s2)
            tg = _ten_god(dsi, s2)
            ten_gods[p] = {
                "branch": b,
                "stem": TIANGAN[s2],
                "ten_god": tg,
                "stem_element": TG_WUXING[s2],
                "canggan": [TIANGAN[c] for c in CANGGAN.get(b, [])]
            }
            hidden[p] = [TIANGAN[c] for c in CANGGAN.get(b, [])]
        mc = _solar_term_month(pillars.get("_dt", "2026-06-15"))
        label, dom, bal, wc = _calc_balance(pillars, day_master)
        ratio = wc.get(dm_elem, 2) / max(sum(wc.values()), 1)
        useful = _calc_useful(dsi, dbi, ratio, wc)
        forbidden = _calc_forbidden(dsi, dbi, ratio)
        elem_str = {k:{"count":wc.get(k,0),"ratio":round(wc.get(k,0)/max(sum(wc.values()),1),3)} for k in ["木","火","土","金","水"]}
        growth = _growth(dm_elem)
        agent = {
            "emotional_pattern": f"{dm_elem}主人在{label}时高压下易{'走极端' if ratio>0.25 else '缺乏主动'}",
            "useful_action": f"宜用{useful['stems']}引导方向",
            "forbidden_action": f"忌用{forbidden['stems']}硬推",
            "growth_direction": f"学习{growth}补{dm_elem}短板",
            "dominant_behavior": f"主{dom}性五行，{wc.get(dom,0)}项能量占优"
        }
        return {
            "useful_god": useful,
            "forbidden_god": forbidden,
            "hidden_stems": hidden,
            "ten_gods_detail": ten_gods,
            "month_correction": mc,
            "element_strength": elem_str,
            "balance_analysis": {"label": label, "dominant": dom, "day_ratio": round(ratio,3), "wuxing_count": wc},
            "agent_params": agent,
            "v4_needed": ["大运起运年龄","流年叠加","调候用神","格局判断","真太阳时"]
        }