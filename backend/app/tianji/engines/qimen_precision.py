"""Qimen Precision Engine v2: precise value-fu/shi, heaven/earth plates, horse/empty."""
from __future__ import annotations
import json
from pathlib import Path

TIANGAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
TG_IDX = {k:i for i,k in enumerate(TIANGAN)}
DIZHI = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
DZ_IDX = {k:i for i,k in enumerate(DIZHI)}

YANG_JU = {
    "冬至":1,"小寒":1,"大寒":1,"立春":8,"雨水":8,"惊蛰":8,
    "春分":3,"清明":3,"谷雨":3,"立夏":4,"小满":4,"芒种":4,
    "夏至":9,"小暑":9,"大暑":9,"立秋":2,"处暑":2,"白露":2,
    "秋分":7,"寒露":7,"霜降":7,"立冬":6,"小雪":6,"大雪":6
}
YIN_JU = {k:(v%3+1) for k,v in YANG_JU.items()}

ST_2026 = {"小寒":"01-05","大寒":"01-20","立春":"02-04","雨水":"02-18","惊蛰":"03-05","春分":"03-20","清明":"04-04","谷雨":"04-20","立夏":"05-05","小满":"05-21","芒种":"06-06","夏至":"06-21","小暑":"07-07","大暑":"07-22","立秋":"08-07","处暑":"08-23","白露":"09-07","秋分":"09-23","寒露":"10-08","霜降":"10-23","立冬":"11-07","小雪":"11-22","大雪":"12-07","冬至":"12-21"}
ST_2025 = {"小寒":"01-05","大寒":"01-20","立春":"02-03","雨水":"02-18","惊蛰":"03-05","春分":"03-20","清明":"04-04","谷雨":"04-20","立夏":"05-05","小满":"05-21","芒种":"06-05","夏至":"06-21","小暑":"07-07","大暑":"07-22","立秋":"08-07","处暑":"08-23","白露":"09-07","秋分":"09-23","寒露":"10-08","霜降":"10-23","立冬":"11-07","小雪":"11-22","大雪":"12-07","冬至":"12-21"}
ST_2027 = {"小寒":"01-05","大寒":"01-20","立春":"02-04","雨水":"02-18","惊蛰":"03-05","春分":"03-20","清明":"04-04","谷雨":"04-20","立夏":"05-05","小满":"05-21","芒种":"06-05","夏至":"06-21","小暑":"07-07","大暑":"07-22","立秋":"08-07","处暑":"08-23","白露":"09-08","秋分":"09-23","寒露":"10-08","霜降":"10-23","立冬":"11-07","小雪":"11-22","大雪":"12-07","冬至":"12-22"}

def _find_solar_term(dt):
    from datetime import datetime
    yr = dt.year
    terms = ST_2026 if yr==2026 else ST_2027 if yr==2027 else ST_2025
    prev = None
    for n,m in sorted(terms.items(), key=lambda x:x[1]):
        md = datetime.strptime(f"{yr}-{m}","%Y-%m-%d")
        if md<=dt: prev=(n,md)
        else: break
    return prev[0] if prev else "冬至"

def _calc_yin_yang(dt):
    t=_find_solar_term(dt)
    return "阳遁" if t in ["冬至","小寒","大寒","立春","雨水","惊蛰","春分","清明","谷雨","立夏","小满","芒种"] else "阴遁"

def _build_precise_board(ju, dun):
    PALACE=["坎一宫","坤二宫","震三宫","巽四宫","中五宫","乾六宫","兑七宫","艮八宫","离九宫"]
    STEM=["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
    BRANCH=["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
    ju_m=(ju-1)%9+1
    board={}
    for i,p in enumerate(PALACE):
        n=i+1
        s_idx=(ju_m+n-1)%10 if dun=="阳遁" else (10-(ju_m+n-1)%10)%10
        board[p]={"stem":STEM[s_idx],"branch":BRANCH[n%12],"board_pos":n}
    return board

def _vf_via_stem(board, hour_stem):
    for p,d in board.items():
        if d["stem"]==hour_stem: return p
    return "中五宫"

def _vs_via_branch(board, hour_branch):
    PALACE=["坎一宫","坤二宫","震三宫","巽四宫","中五宫","乾六宫","兑七宫","艮八宫","离九宫"]
    idx=DZ_IDX.get(hour_branch,0)%9
    return PALACE[idx]

def _horse(branch):
    m={"亥":"申","子":"申","寅":"亥","午":"亥","卯":"酉","未":"丑"}
    return m.get(branch,"无马星")

def _empty(branch):
    m={"子":["亥","子"],"丑":["亥","子"],"寅":["戌","亥"],"卯":["戌","亥"],
       "辰":["酉","戌"],"巳":["酉","戌"],"午":["未","申"],"未":["未","申"],
       "申":["午","未"],"酉":["午","未"],"戌":["巳","午"],"亥":["巳","午"]}
    return m.get(branch,[])

def _earth_plate():
    PALACE=["坎一宫","坤二宫","震三宫","巽四宫","中五宫","乾六宫","兑七宫","艮八宫","离九宫"]
    EP=["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
    return {p:EP[i%10] for i,p in enumerate(PALACE)}

class QimenPrecisionEngine:
    def analyze(self, bureau, board, domain, question):
        dun=bureau["dun"]; ju=bureau["ju_number"]
        sb=bureau.get("stem_branch_hour","甲子")
        hs=sb[0]; hb=sb[1] if len(sb)>1 else "子"
        pboard=_build_precise_board(ju,dun)
        vp=_vf_via_stem(pboard,hs)
        vs=_vs_via_branch(pboard,hb)
        hp=_horse(hb); ep=_empty(hb)
        domain_hint={"strategy":"值符主战略布局，值使主执行落地",
                     "relationship":"值符主主动方，值使主被动方",
                     "business":"值符主商机，值使主风险",
                     "personal":"值符主内因，值使主外应",
                     "content":"值符主内容，值使主传播","unknown":"综合判断"}
        agent = f"{vp}值符主战略，{vs}值使主落地；{domain_hint.get(domain,'综合判断')}；{hp}；空亡{ep[:2] if ep else '无'}"
        # 合并board中的stem/branch到主结果
        combined_board={}
        for p,d in board.items():
            pb=pboard.get(p,{})
            combined_board[p]={**d,"stem":pb.get("stem",""),"branch":pb.get("branch","")}
        return {
            "value_fu":{"palace":vp,"note":f"时干{hs}所在宫"},
            "value_shi":{"palace":vs,"note":f"时支{hb}对应宫"},
            "heaven_plate":{p:d["stem"] for p,d in pboard.items()},
            "earth_plate":_earth_plate(),
            "horse_star":hp,
            "empty_palaces":ep,
            "board_with_stems":combined_board,
            "agent_hint":agent,
            "v4_needed":["值符值使逐宫飞布","八门飞宫","九星飞宫","逐字爻辞"]
        }
