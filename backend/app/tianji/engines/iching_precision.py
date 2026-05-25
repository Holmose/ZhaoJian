"""IChing Precision Engine v2: nuclear hexagram, cuo/geng, liu qin, stage analysis."""
from __future__ import annotations
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
ICH = json.load(open(DATA / "iching_64_hexagrams.json", encoding="utf-8"))

CUO = {
    "乾为天":"坤为地","坤为地":"乾为天","水雷屯":"火风鼎","山水蒙":"泽雷随",
    "水天需":"天火讼","天水讼":"水天需","地水师":"水地比","水地比":"地水师",
    "风天小畜":"天泽履","天泽履":"风天小畜","地天泰":"天地否","天地否":"地天泰",
    "天火同人":"火天大有","火天大有":"天火同人","地山谦":"泽山咸","雷山小过":"雷泽归妹",
    "水火既济":"火水未济","火水未济":"水火既济",
    "风火家人":"雷水解","雷水解":"风火家人","天雷无妄":"地雷复",
    "山雷颐":"泽风大过","山天大畜":"地风升","水风井":"火风鼎",
}
ALL_H = list(ICH.keys())
for i, h in enumerate(ALL_H):
    if h not in CUO:
        CUO[h] = ALL_H[(i + 32) % 64]

DM_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
DM_ELEM = ["木","木","火","火","土","土","金","金","水","水"]

def _line_meaning(val):
    if val == 6: return {"label":"老阴", "symbol":"-- --", "change":True}
    if val == 7: return {"label":"少阳", "symbol":"━━━", "change":False}
    if val == 8: return {"label":"少阴", "symbol":"-- --", "change":False}
    if val == 9: return {"label":"老阳", "symbol":"━━━", "change":True}
    return {"label":"未知", "symbol":"?", "change":False}

def _liu_qin(stems):
    rel_map = {0:"兄弟",1:"子孙",2:"妻财",3:"官鬼",4:"父母",5:"兄弟",6:"子孙",7:"妻财",8:"官鬼",9:"父母"}
    elem_map = {0:"木",1:"木",2:"火",3:"火",4:"土",5:"土",6:"金",7:"金",8:"水",9:"水"}
    return [{"position":["初","二","三","四","五","六"][i],"stem":DM_STEMS[stems[i]%10],"stem_element":DM_ELEM[stems[i]%10],"relation":rel_map[stems[i]%10]} for i in range(6)]

def _select_primary(question, domain):
    kw = {
        "strategy": ["乾为天","天泽履","地天泰","火天大有","水天需","天火同人"],
        "relationship": ["风火家人","雷水解","水火既济","泽山咸","雷山小过","地山谦"],
        "business": ["天火同人","地水师","水地比","乾为天","雷水解","天泽履"],
        "personal": ["地山谦","水雷屯","山水蒙","雷山小过","风天小畜","地天泰"],
        "content": ["火水未济","天火同人","风天小畜","风火家人","水天需"]
    }
    pool = kw.get(domain, kw["strategy"])
    q = question.lower()
    if any(w in q for w in ["扩张","发布","布局","做成","做大","公开"]): pool = kw["strategy"]
    if any(w in q for w in ["情感","关系","她","暧昧","追","复合","窗口","推","升温"]): pool = kw["relationship"]
    if any(w in q for w in ["客户","成交","商业","合作","项目","销售"]): pool = kw["business"]
    if any(w in q for w in ["个人","成长","职业","发展","方向"]): pool = kw["personal"]
    import hashlib
    h = int(hashlib.md5(q.encode()).hexdigest()[:8], 16)
    return pool[h % len(pool)]

class IChingPrecisionEngine:
    def analyze(self, primary_hexagram, changing_lines, changed_hexagram, domain, question):
        hx = list(ICH.keys())
        p = primary_hexagram if primary_hexagram in hx else hx[0]
        c = changed_hexagram if changed_hexagram in hx else hx[32]
        cl = changing_lines if changing_lines and len(changing_lines)==6 else [8,7,8,7,8,7]
        # 错卦
        cuo_name = CUO.get(p, hx[(hx.index(p)+32)%64])
        # 互卦（简化：取第2/3/4/5爻）
        mid_section = cl[1:5]
        nuclear_idx = sum((1 if v in [8,9] else 0)*2**(4-i) for i,v in enumerate(mid_section))
        nuclear = hx[nuclear_idx % 64]
        # 逐爻分析
        line_details = [{"position":["初爻","二爻","三爻","四爻","五爻","上爻"][i], **_line_meaning(cl[i])} for i in range(6)]
        # 六亲
        liu_qin = _liu_qin([cl[i] % 10 for i in range(6)])
        # 阶段分析
        chg_pos = [i for i,v in enumerate(cl) if v in [6,9]]
        stage_warn = []
        if chg_pos:
            last = max(chg_pos)
            stage_warn.append(f"变爻在{['初爻','二爻','三爻','四爻','五爻','上爻'][last]}，{['前段需布局','前段渐明','中段转折','后段关键','后段收尾','结果已定'][last]}")
            if last >= 4: stage_warn.append("后半段变爻，注意结果收口、名实匹配")
        p_d = ICH.get(p, {})
        c_d = ICH.get(c, {})
        cuo_d = ICH.get(cuo_name, {})
        nuc_d = ICH.get(nuclear, {})
        transition = f"本卦{p}趋势{p_d.get('trend','')}；变卦{c}趋势{c_d.get('trend','')}"
        action = f"{p_d.get('strategy','')}；参照{c_d.get('strategy','')}"
        # Agent
        dm_stem_idx = sum(cl) % 10
        dm_elem = DM_ELEM[dm_stem_idx]
        rel_elements = [DM_ELEM[cl[i]%10] for i in range(6)]
        p_elem = sum(1 for e in rel_elements if e == dm_elem)
        if p_elem >= 4: emo_tone = "进取强势"
        elif p_elem <= 1: emo_tone = "柔和内敛"
        else: emo_tone = "平衡灵活"
        agent = {
            "hex_type": p, "transition_type": "变卦主导" if chg_pos and max(chg_pos)>=4 else "本卦主导" if chg_pos and max(chg_pos)<=2 else "本变交替",
            "stage_focus": "开局布局" if not chg_pos else "收尾验证" if max(chg_pos)>=4 else "中段推进",
            "emotional_tone": emo_tone,
            "action_keyword": p_d.get("strategy",""),
            "risk_keyword": c_d.get("risk","")
        }
        return {
            "primary_detail": p_d,
            "changed_detail": c_d,
            "错卦_cuo": {"name": cuo_name, "trend": cuo_d.get("trend",""), "strategy": cuo_d.get("strategy","")},
            "互卦_nuclear": {"name": nuclear, "trend": nuc_d.get("trend","")},
            "changing_line_detail": line_details,
            "liu_qin": liu_qin,
            "stage_warning": stage_warn,
            "transition": transition,
            "action_hint": action,
            "agent_params": agent,
            "v4_needed": []
        }