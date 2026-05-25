"""Bazi Precision Engine v4: Fixed element balance + canggan counting."""
from __future__ import annotations

TIANGAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
TG_IDX = {k:i for i,k in enumerate(TIANGAN)}
TG_WUXING = ["木","木","火","火","土","土","金","金","水","水"]
DIZHI = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
DZ_IDX = {k:i for i,k in enumerate(DIZHI)}
DZ_WUXING = ["水","土","木","木","土","火","火","土","金","金","土","水"]

CANGGAN = {
    "子":[9], "丑":[5,9,7], "寅":[0,2,4], "卯":[1],
    "辰":[4,1,9], "巳":[2,5,4], "午":[3,5], "未":[5,3,1],
    "申":[6,8,4], "酉":[7], "戌":[4,7,3], "亥":[8,0]
}

YUELING = {
    "寅":["立春","惊蛰"],"卯":["惊蛰","清明"],"辰":["清明","立夏"],
    "巳":["立夏","芒种"],"午":["芒种","小暑"],"未":["小暑","立秋"],
    "申":["立秋","白露"],"酉":["白露","寒露"],"戌":["寒露","立冬"],
    "亥":["立冬","大雪"],"子":["大雪","小寒"],"丑":["小寒","立春"]
}

ST2026 = {
    "小寒":"01-05","大寒":"01-20","立春":"02-04","雨水":"02-18",
    "惊蛰":"03-05","春分":"03-20","清明":"04-04","谷雨":"04-20",
    "立夏":"05-05","小满":"05-21","芒种":"06-06","夏至":"06-21",
    "小暑":"07-07","大暑":"07-22","立秋":"08-07","处暑":"08-23",
    "白露":"09-07","秋分":"09-23","寒露":"10-08","霜降":"10-23",
    "立冬":"11-07","小雪":"11-22","大雪":"12-07","冬至":"12-21"
}
ST2025 = {
    "小寒":"01-05","大寒":"01-20","立春":"02-03","雨水":"02-18",
    "惊蛰":"03-05","春分":"03-20","清明":"04-04","谷雨":"04-20",
    "立夏":"05-05","小满":"05-21","芒种":"06-05","夏至":"06-21",
    "小暑":"07-07","大暑":"07-22","立秋":"08-07","处暑":"08-23",
    "白露":"09-07","秋分":"09-23","寒露":"10-08","霜降":"10-23",
    "立冬":"11-07","小雪":"11-22","大雪":"12-07","冬至":"12-21"
}

def _solar(dt_str):
    from datetime import datetime
    try:
        dt = datetime.strptime(dt_str[:16],"%Y-%m-%d %H:%M")
    except:
        try:
            dt = datetime.strptime(dt_str[:10],"%Y-%m-%d")
        except:
            return "未知"
    terms = ST2026 if dt.year == 2026 else ST2025
    prev = None
    for n,m in sorted(terms.items(), key=lambda x:x[1]):
        t = datetime.strptime(f"{dt.year}-{m}","%Y-%m-%d")
        if t <= dt: prev = (n,t)
        else: break
    return prev[0] if prev else list(terms.items())[-1][0]

def _month_branch(dt_str):
    term = _solar(dt_str)
    for z,(s,e) in YUELING.items():
        if term == s: return z
    return None

def _ten_god(ds, os):
    diff = (os - ds) % 10
    return ["比肩","劫财","食神","伤官","偏财","正财","偏官","正官","偏印","正印"][diff]

def _balance(wc, ds):
    dm_elem = TG_WUXING[ds]
    total = sum(wc.values()) or 1
    de_cnt = wc.get(dm_elem, 0)
    ratio = de_cnt / total
    dom = max(wc, key=wc.get) if wc else dm_elem
    sup_map = {"木":"水","火":"木","土":"火","金":"土","水":"金"}
    ctrl_map = {"木":"金","火":"水","土":"木","金":"火","水":"土"}
    sup_v = wc.get(sup_map.get(dm_elem,dm_elem), 0)
    ctrl_v = wc.get(ctrl_map.get(dm_elem,dm_elem), 0)
    if ratio > 0.35: label = "身强"
    elif ratio < 0.12: label = "身弱"
    elif de_cnt >= sup_v + 2 and de_cnt >= ctrl_v + 2: label = "偏强"
    elif de_cnt <= 1 and sup_v <= 1 and ctrl_v >= 3: label = "偏弱"
    else: label = "中和"
    bal = {k:round(wc.get(k,0)/total, 3) for k in ["木","火","土","金","水"]}
    return label, dom, bal, wc

def _useful(ds, wc):
    dm_elem = TG_WUXING[ds]
    total = sum(wc.values()) or 1
    ratio = wc.get(dm_elem, 0) / total
    e2s = {}
    for i,e in enumerate(TG_WUXING):
        if e not in e2s: e2s[e] = i
    need_map = {"木":"金","火":"水","土":"木","金":"火","水":"土"}
    ctrl_map = {"木":"金","火":"水","土":"木","金":"火","水":"土"}
    sup_map = {"木":"水","火":"木","土":"火","金":"土","水":"金"}
    if ratio > 0.25:
        cnd = [need_map.get(dm_elem,dm_elem), ctrl_map.get(dm_elem,dm_elem)]
        note = "身强宜用财官抑身"
    else:
        cnd = [sup_map.get(dm_elem,dm_elem), need_map.get(dm_elem,dm_elem)]
        note = "身弱宜用印比生扶"
    stems = [TIANGAN[e2s.get(c,c)] for c in cnd if c in e2s]
    return {"stems": stems, "note": note}

class BaziPrecisionEngine:
    def analyze(self, pillars, day_master, strength, dominant_element, five_element_balance):
        ds = TG_IDX[day_master["stem"]]
        dm_elem = TG_WUXING[ds]
        year_b = pillars.get("_year_branch", pillars["year"][1])
        month_b = pillars.get("_month_branch", pillars["month"][1])
        day_b = pillars["day"][1]
        hour_b = pillars["hour"][1]
        hs = {}
        tg_details = {}
        all_vis = []
        for p, b in [("年",year_b),("月",month_b),("日",day_b),("时",hour_b)]:
            cg = CANGGAN.get(b, [])
            s2 = (ds * 2 + DZ_IDX[b]) % 10
            tg = _ten_god(ds, s2)
            hs[p] = [TIANGAN[c] for c in cg]
            tg_details[p] = {"branch": b, "stem": TIANGAN[s2], "ten_god": tg,
                            "ten_god_element": TG_WUXING[s2], "canggan": hs[p]}
            all_vis.append(s2)
        mc = _month_branch(pillars.get("_dt","2026-06-15 12:00"))
        # 五行计数：可见4柱天干 + 藏干（五行全息），不额外加日主
        wc = {}
        for s2 in all_vis:
            e = TG_WUXING[s2]; wc[e] = wc.get(e,0) + 1
        for p_cg in hs.values():
            for c in p_cg:
                e = TG_WUXING[TG_IDX[c]]
                wc[e] = wc.get(e, 0) + 1
        label, dom, bal, wc = _balance(wc, ds)
        useful = _useful(ds, wc)
        # 忌神：与日主同五行者（可见柱 + 藏干）
        fr_stems = [s for s in all_vis if TG_WUXING[s] == dm_elem]
        for p_cg in hs.values():
            for c in p_cg:
                if TG_WUXING[TG_IDX[c]] == dm_elem:
                    fr_stems.append(c)
        fr_stems_dedup = list(dict.fromkeys(fr_stems))
        fr = [TIANGAN[ds]] + fr_stems_dedup
        note = "比劫过旺则争宜收敛" if len(fr_stems_dedup) > 1 else "身弱忌再泄宜补印比"
        growth = {"木":"火土金","火":"水金","土":"金水","金":"木水","水":"木火"}.get(dm_elem,"木")
        agent = {
            "emotional_pattern": "偏强则高压下易走极端，身弱则缺乏主动",
            "useful_action": "宜用{}引导方向".format(useful["stems"]),
            "forbidden_action": "忌用{}硬推".format(fr),
            "growth_direction": "学习{}短板".format(growth),
            "dominant_behavior": "主{}性，倾向{}项驱动".format(dm_elem, wc.get(dm_elem, 0))
        }
        return {
            "useful_god": useful,
            "forbidden_god": {"stems": fr, "note": note},
            "hidden_stems": hs,
            "ten_gods_detail": tg_details,
            "month_correction": mc,
            "element_strength": {k:{"count":wc.get(k,0),"ratio":bal.get(k,0)} for k in ["木","火","土","金","水"]},
            "balance_analysis": {"label": label, "dominant": dom, "day_ratio": bal.get(dm_elem,0), "wuxing_count": wc},
            "agent_params": agent,
            "v4_needed": []
        }