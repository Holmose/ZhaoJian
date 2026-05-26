"""V5 Relationship Scene Engine · 人间关系推演引擎

场景：关系瓶颈、关系抉择、磨合诊断
输入：双方描述 + 冲突/核心矛盾 + 时间
输出：泰卦解读 + "应/敌"判断 + 接受度诊断 + 三路径

核心逻辑：
- 关系卦象映射：问题类型 → 对应易经卦象
- "应"判断：根据输入判断对方是"应"还是"敌"
- 接受度诊断：让步 vs 接受 的分界
- 天玑铭文：车辙比喻 + 命盘铭文化输出
"""
from __future__ import annotations
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class RelationshipEngine:
    """V5 人间关系推演引擎"""

    # 问题类型 → 卦象映射
    HEXAGRAM_MAP = {
        "性格冲突": {"primary": "泽山咸", "secondary": "雷泽归妹", "reason": "咸卦主感应，归妹主错位"},
        "磨合困难": {"primary": "地天泰", "secondary": "天泽履", "reason": "泰卦主交泰通达，履卦主分寸礼法"},
        "沟通障碍": {"primary": "风山渐", "secondary": "风地观", "reason": "渐卦主渐进节奏，观卦主观察审视"},
        "信任危机": {"primary": "地风升", "secondary": "山天大畜", "reason": "升卦主积累信任，大畜主蓄能待发"},
        "关系抉择": {"primary": "地天泰", "secondary": "天泽履", "reason": "泰卦通达，履卦分寸"},
        "冷淡冷却": {"primary": "风水涣", "secondary": "风山渐", "reason": "涣卦主离散，渐卦主修复节律"},
        "暧昧升温": {"primary": "泽山咸", "secondary": "天泽履", "reason": "咸卦主感应吸引，履卦主建立边界"},
        "分手边缘": {"primary": "雷泽归妹", "secondary": "水天需", "reason": "归妹主错位，需卦主等待时机"},
    }

    # "应"的信号（对方能接住）
    YING_SIGNALS = [
        "她愿意陪你快两步",
        "她愿意慢下来等你",
        "她能接住你的情绪",
        "你急的时候她愿意配合",
        "你停下来她愿意等你",
        "她能看到你的不同背后的价值",
        "她愿意往你方向走一步",
    ]

    # "敌"的信号（对方接不住）
    DI_SIGNALS = [
        "你好好说她却说你急",
        "她总是否定你的感受",
        "她不接你的话茬",
        "你退一步她进一步",
        "她把你的付出当理所当然",
        "她只顾自己方向不管你",
        "你说她在听但从不改",
    ]

    def __init__(self):
        with open(DATA_DIR / "iching_64_hexagrams.json") as f:
            self.iching_data = json.load(f)
        with open(DATA_DIR / "relationship_hexagrams.json", encoding="utf-8") as f:
            self.rel_data = json.load(f)

    def analyze(
        self,
        question: str,
        conflict_type: str,
        party_a_desc: str,
        party_b_desc: str,
        conflict_event: str,
        duration: str,
    ) -> dict:
        """主分析入口"""
        # 1. 判断问题类型 → 卦象
        hexagram_key = self._match_hexagram_key(conflict_type, question)
        primary_key = self.HEXAGRAM_MAP.get(hexagram_key, {}).get("primary", "地天泰")
        primary_hex = self._get_hexagram(primary_key)
        secondary_key = self.HEXAGRAM_MAP.get(hexagram_key, {}).get("secondary", "地天泰")
        secondary_hex = self._get_hexagram(secondary_key)

        # 2. "应"vs"敌" 判断
        ying_di = self._judge_ying_di(question, party_a_desc, party_b_desc, conflict_event)

        # 3. 接受度诊断
        acceptance = self._judge_acceptance(ying_di, conflict_event)

        # 4. 方向一致性
        direction = self._judge_direction(party_a_desc, party_b_desc)

        # 5. 三路径（基于卦象+判断）
        paths = self._generate_paths(primary_hex, ying_di, direction, acceptance)

        # 6. 天玑铭文（诗化输出）
        inscription = self._generate_inscription(
            primary_hex, ying_di, direction, acceptance, party_a_desc, party_b_desc
        )

        # 7. 核心判词
        verdict = self._generate_verdict(primary_hex, ying_di, acceptance, direction)

        return {
            "status": "ok",
            "engine": "RelationshipEngine V5.0",
            "conflict_type": conflict_type,
            "hexagram_key": hexagram_key,
            "primary_hexagram": primary_hex,
            "secondary_hexagram": secondary_hex,
            "ying_di": ying_di,
            "acceptance": acceptance,
            "direction": direction,
            "paths": paths,
            "inscription": inscription,
            "verdict": verdict,
            "mapping_reason": self.HEXAGRAM_MAP.get(hexagram_key, {}).get("reason", ""),
        }

    def _match_hexagram_key(self, conflict_type: str, question: str) -> str:
        """匹配问题类型到卦象关键字"""
        conflict_lower = conflict_type.lower()
        question_lower = question.lower()

        for key in self.HEXAGRAM_MAP:
            if key in conflict_lower or key in question_lower:
                return key

        if any(k in conflict_lower or k in question_lower for k in ["性格", "急性子", "慢性子", "磨合"]):
            return "性格冲突"
        if any(k in conflict_lower or k in question_lower for k in ["沟通", "说话", "不理", "冷战"]):
            return "沟通障碍"
        if any(k in conflict_lower or k in question_lower for k in ["信任", "怀疑", "不诚实"]):
            return "信任危机"
        if any(k in conflict_lower or k in question_lower for k in ["冷淡", "冷", "不回", "不主动"]):
            return "冷淡冷却"
        if any(k in conflict_lower or k in question_lower for k in ["升温", "暧昧", "上头", "表白"]):
            return "暧昧升温"
        if any(k in conflict_lower or k in question_lower for k in ["分手", "离婚", "断"]):
            return "分手边缘"

        return "磨合困难"

    def _get_hexagram(self, key: str) -> dict:
        """从易经数据获取卦象（基础字段）"""
        base = self.iching_data.get(key, {})
        enhanced = self.rel_data.get(key, {})
        merged = {**base, **enhanced}
        # 确保有 name 字段
        if "name" not in merged:
            merged["name"] = key
        return merged

    def _judge_ying_di(
        self, question: str, party_a: str, party_b: str, event: str
    ) -> dict:
        """判断应或敌"""
        combined = f"{question} {party_a} {party_b} {event}".lower()

        # 统计命中
        ying_count = sum(1 for s in self.YING_SIGNALS if s in combined)
        di_count = sum(1 for s in self.DI_SIGNALS if s in combined)

        # 关键词命中
        ying_kw = ["愿意", "配合", "接住", "等我", "理解", "回应", "在乎", "愿意陪", "慢下来"]
        di_kw = ["否定", "不听", "只顾", "理所当然", "说你急", "不接", "翻旧账", "冷战"]
        ying_hits = sum(1 for kw in ying_kw if kw in combined)
        di_hits = sum(1 for kw in di_kw if kw in combined)

        total_ying = ying_count + ying_hits
        total_di = di_count + di_hits

        if total_ying > total_di + 1:
            label = "应"
            desc = "她能接住你，你发出去她愿意回应"
            prob = round(total_ying / (total_ying + total_di + 1), 2)
        elif total_di > total_ying + 1:
            label = "敌"
            desc = "她在拒绝接住你，你发出去她接不住"
            prob = round(total_di / (total_ying + total_di + 1), 2)
        else:
            label = "待观察"
            desc = "信号不明确，需要更多现实反馈来判断"
            prob = 0.5

        return {
            "label": label,
            "description": desc,
            "ying_score": total_ying,
            "di_score": total_di,
            "confidence": prob,
            "signals_ying": ying_hits,
            "signals_di": di_hits,
        }

    def _judge_acceptance(self, ying_di: dict, event: str) -> dict:
        """判断接受度：让步 vs 接受"""
        event_lower = event.lower()

        # 让步信号（记账式隐忍）
        compromise_kw = ["让步", "算了", "我不计较", "我又忍了", "每次都是我让", "我忍了很久", "翻旧账", "我图什么", "不公平"]
        # 接受信号（自然绕开不记账）
        accept_kw = ["接受", "理解", "我知道她", "她就是这样", "正常", "自然", "不抱怨", "绕开"]

        compromise_count = sum(1 for kw in compromise_kw if kw in event_lower)
        accept_count = sum(1 for kw in accept_kw if kw in event_lower)

        if ying_di["label"] == "敌":
            level = "低（对方是敌，接受也是徒劳）"
            score = 0.2
        elif compromise_count > accept_count:
            level = "低（你在让步，不是在接受）"
            score = 0.3
        elif accept_count > compromise_count:
            level = "高（你是在真正接受）"
            score = 0.8
        else:
            level = "中（接受和让步混在一起）"
            score = 0.5

        return {
            "level": level,
            "score": score,
            "compromise_signals": compromise_count,
            "accept_signals": accept_count,
        }

    def _judge_direction(self, party_a: str, party_b: str) -> dict:
        """判断方向一致性"""
        combined = f"{party_a} {party_b}".lower()

        same_direction_kw = ["同一个方向", "目标一致", "都想要", "一起", "共同努力", "一起走", "方向相同"]
        diff_direction_kw = ["各走各的", "方向不同", "他要她不要", "矛盾", "冲突", "不一致"]

        same_hits = sum(1 for kw in same_direction_kw if kw in combined)
        diff_hits = sum(1 for kw in diff_direction_kw if kw in combined)

        if same_hits > diff_hits:
            status = "一致"
            desc = "方向一致，脚步不同，可以磨合"
        elif diff_hits > same_hits:
            status = "不一致"
            desc = "方向不一致，接受也没用，该收就收"
        else:
            status = "待验证"
            desc = "方向是否一致需要更多现实反馈"

        return {"status": status, "description": desc}

    def _generate_paths(self, primary_hex: dict, ying_di: dict, direction: dict, acceptance: dict) -> list:
        """生成三路径"""
        name = primary_hex.get("name", "地天泰")
        trend = primary_hex.get("trend", "")

        # 基础概率调整
        if ying_di["label"] == "应":
            a_prob = 0.50
            b_prob = 0.30
            c_prob = 0.20
        elif ying_di["label"] == "敌":
            a_prob = 0.20
            b_prob = 0.35
            c_prob = 0.45
        else:
            a_prob = 0.40
            b_prob = 0.35
            c_prob = 0.25

        # 如果方向不一致，降低A路径
        if direction["status"] == "不一致":
            a_prob, b_prob, c_prob = 0.15, 0.40, 0.45

        # 如果接受度低且对方是敌，降低A
        if ying_di["label"] == "敌" and acceptance["score"] < 0.4:
            a_prob, b_prob, c_prob = 0.10, 0.35, 0.55

        return [
            {
                "name": "A 顺势磨合",
                "probability": a_prob,
                "condition": f"{name}·{trend}",
                "action": "继续当前节奏，在小事上验证对方是否真的愿意配合，不要强推",
                "risks": ["把对方的配合当成理所当然", "在大事上才发现方向不一致"],
                "天意": "天恩示现，吉象显化，顺势而动，见好就收",
            },
            {
                "name": "B 调整边界",
                "probability": b_prob,
                "condition": "接受和让步混在一起，或方向有分歧",
                "action": "明确你自己的边界：哪些可以接受，哪些不能再让；用行动而非语言表达",
                "risks": ["边界模糊导致反复拉锯", "说了边界但不守"],
                "天意": "风云待变，隐忍待机，守住边界，静观其变",
            },
            {
                "name": "C 止损转身",
                "probability": c_prob,
                "condition": "对方持续是敌，方向持续不一致，接受度持续低",
                "action": "不是认输，是看清楚后做选择；减少投入，降低期待，把精力收回",
                "risks": ["不甘心导致反复回头", "止损不彻底"],
                "天意": "天机逆转，祸福相依，以退为进，断舍离生",
            },
        ]

    def _generate_inscription(
        self,
        primary_hex: dict,
        ying_di: dict,
        direction: dict,
        acceptance: dict,
        party_a: str,
        party_b: str,
    ) -> dict:
        """生成天玑命盘铭文（诗化）"""
        name = primary_hex.get("name", "地天泰")
        gua = primary_hex.get("gua", "泰")

        # 车辙比喻铭文
        cart_note = (
            "老路上的车辙，左边深右边浅，却谁也离不开谁。"
            "没有深浅，就无处可依，甚至陷进泥里。"
            "你们的关系也是如此，接受对方的「不一样」，才能走得长远。"
        )

        # 泰卦专属铭文
        if name == "地天泰":
            tai_inscription = (
                "地在上，天在下，本是错位，却因交合而万物通泰。"
                "你往下走一步，她往上迈一步，就能契合。"
                "若你站在原地等她过来，她永远也到不了。"
            )
        elif name == "泽山咸":
            tai_inscription = (
                "泽山咸，感应之道，咸者，感也。"
                "心心相印，不期而至；情感情应，不勉而中。"
                "关系的关键不在相似或互补，在于你发出去，她能不能接住。"
            )
        else:
            tai_inscription = (
                f"{name}，{gua}者，变也。"
                "天地交泰，阴阳相感，关系之道，不在形而在神。"
            )

        # 命盘铭文
        if ying_di["label"] == "应":
            fate = "应命——她能接住你，你发出去她愿回应，值得磨合"
            fate_style = "通泰之命，感应相随"
        elif ying_di["label"] == "敌":
            fate = "敌命——她在拒绝接住你，继续投入需谨慎"
            fate_style = "错位之命，方向有违"
        else:
            fate = "待定命——信号不明确，需要更多现实反馈"
            fate_style = "待观之命，静待天机"

        return {
            "hexagram_inscription": tai_inscription,
            "cart_metaphor": cart_note,
            "fate_label": fate,
            "fate_style": fate_style,
            "acceptance_judge": (
                f"接受度{acceptance['level']}。"
                f"真正的接受是像水遇石自然绕开，不存抱怨。"
                f"若让步时心里记着账，那不是接受，是隐忍。"
            ),
            "direction_judge": (
                f"方向{direction['status']}：{direction['description']}"
            ),
        }

    def _generate_verdict(
        self, primary_hex: dict, ying_di: dict, acceptance: dict, direction: dict
    ) -> dict:
        """生成天玑判词"""
        name = primary_hex.get("name", "地天泰")
        gua = primary_hex.get("gua", "泰")

        if ying_di["label"] == "应" and direction["status"] == "一致":
            core = "应命通泰，值得磨合，顺势而动"
            style = "吉"
        elif ying_di["label"] == "敌":
            core = "敌命错位，接受无效，该收就收"
            style = "平"
        elif direction["status"] == "不一致":
            core = "方向有违，接受也是徒劳，明智止损"
            style = "平"
        else:
            core = "待观之命，需要现实反馈来判断方向"
            style = "待定"

        return {
            "title": f"{name}·{ying_di['label']}命",
            "core": core,
            "style": style,
            "hexagram_judgment": f"{gua}卦：{primary_hex.get('trend', '')}，关键在{personal_key_point(ying_di)}",
            "one_liner": f"{'她能接住你' if ying_di['label'] == '应' else '她在拒绝接住你'}，"
            f"{'方向一致' if direction['status'] == '一致' else '方向有分歧'}，"
            f"{acceptance['level']}。",
        }


def personal_key_point(ying_di: dict) -> str:
    if ying_di["label"] == "应":
        return "上下相交与顺势的平衡"
    elif ying_di["label"] == "敌":
        return "看清后做选择，不再徒劳投入"
    else:
        return "等待更多现实反馈"