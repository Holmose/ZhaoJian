from __future__ import annotations

import json
from pathlib import Path
from collections import Counter

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class SymbolicEngine:
    """V1 semantic symbolic engine.

    This is intentionally not a fortune-telling oracle. It maps facts into
    reusable oriental symbolic tags so the multi-agent engine can reason with
    them under reality constraints.
    """

    def __init__(self) -> None:
        self.bagua = json.loads((DATA_DIR / "bagua.json").read_text(encoding="utf-8"))
        self.wuxing = json.loads((DATA_DIR / "wuxing.json").read_text(encoding="utf-8"))
        self.iching = json.loads((DATA_DIR / "iching_seed.json").read_text(encoding="utf-8"))

    def analyze(self, text: str, domain: str = "unknown") -> dict:
        bagua_scores = self._score_bagua(text, domain)
        main_gua = bagua_scores.most_common(1)[0][0]
        element = self.bagua[main_gua]["element"]
        hexagram = self._pick_hexagram(main_gua, text)
        return {
            "bagua": {
                "main": main_gua,
                "element": element,
                "keywords": self.bagua[main_gua]["keywords"],
                "action_hint": self.bagua[main_gua]["action_hint"],
                "scores": dict(bagua_scores.most_common())
            },
            "wuxing": {
                "main": element,
                "keywords": self.wuxing[element]["keywords"],
                "risk": self.wuxing[element]["risk"]
            },
            "iching": hexagram,
            "bazi": {"status": "V2 planned", "role": "人物长期结构模型，需要出生年月日时"},
            "qimen": {"status": "V3 planned", "role": "具体事件局势与行动时机，需要起局时间地点"}
        }

    def _score_bagua(self, text: str, domain: str) -> Counter:
        rules = {
            "乾": ["目标", "主动", "领导", "权力", "项目", "战略", "父", "老板"],
            "坤": ["稳定", "承接", "资源", "家庭", "母", "长期", "土地", "基础"],
            "震": ["开始", "启动", "突然", "变化", "冲突", "惊", "爆发", "行动"],
            "巽": ["传播", "关系", "渗透", "影响", "沟通", "进入", "合作"],
            "坎": ["风险", "隐情", "冷", "困难", "不确定", "担心", "失败", "陷"],
            "离": ["内容", "曝光", "表达", "情绪", "美", "视频", "朋友圈", "品牌"],
            "艮": ["停止", "卡", "边界", "阻碍", "沉淀", "复盘", "暂停"],
            "兑": ["销售", "成交", "聊天", "社交", "说服", "钱", "愉悦", "暧昧"]
        }
        c = Counter({k: 1 for k in rules})
        for gua, words in rules.items():
            for w in words:
                if w in text:
                    c[gua] += 3
        if domain == "business": c["乾"] += 2; c["兑"] += 2
        if domain == "content": c["离"] += 3; c["巽"] += 1
        if domain == "relationship": c["兑"] += 2; c["巽"] += 1
        if domain == "strategy": c["乾"] += 2; c["坎"] += 1
        return c

    def _pick_hexagram(self, main_gua: str, text: str) -> dict:
        if any(x in text for x in ["复盘", "回来", "恢复", "重新"]): name = "地雷复"
        elif any(x in text for x in ["完成", "已经", "成了"]): name = "水火既济"
        elif any(x in text for x in ["卡", "不懂", "信息不足"]): name = "山水蒙"
        elif any(x in text for x in ["决断", "切割", "止损"]): name = "泽天夬"
        elif main_gua == "乾": name = "乾为天"
        elif main_gua == "坤": name = "坤为地"
        elif main_gua == "巽": name = "风火家人"
        else: name = "火水未济"
        data = dict(self.iching[name])
        data["name"] = name
        return data
