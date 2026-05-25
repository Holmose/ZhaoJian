"""Interpretation Engine: 把象数结果翻译成用户能看懂的大白话。

L1 术语翻译：专业术语 → 通俗解释
L2 象意整合：多维度信号 → 一个核心信息
L3 行动建议：关键词罗列 → 一句话行动指南
"""
from __future__ import annotations


class InterpretationEngine:
    """解读引擎 v1.0"""

    # ── L1: 四柱术语翻译 ──────────────────────────────────────────────────────
    def _interpret_bazi(self, bazi: dict) -> dict:
        dm = bazi.get("day_master", {})
        dm_stem = dm.get("stem", "")
        dm_elem = dm.get("element", "")
        p = bazi.get("v3_precision", {})
        label = p.get("balance_analysis", {}).get("label", bazi.get("strong_weak", ""))
        useful = p.get("useful_god", {})
        forbidden = p.get("forbidden_god", {})
        hidden = p.get("hidden_stems", {})
        month_corr = p.get("month_correction", "")

        # 五行性格通俗描述
        elem_nature = {
            "木": "有想法、爱规划，但容易想得多做得少",
            "火": "表达力强、情绪外露，但容易三分钟热度",
            "土": "稳重踏实、靠谱，但容易保守拖延",
            "金": "直接果断、逻辑强，但容易冷硬不近人情",
            "水": "灵活变通、信息敏感，但容易犹豫不决"
        }
        elem_plain = elem_nature.get(dm_elem, "混合特质")

        # 身强身弱通俗解释
        strength_plain = {
            "身强": "你目前底气比较足，有能量去推动事情",
            "身弱": "你目前状态偏弱，底气不足，不适合强推",
            "偏强": "你目前能量偏强，但还不稳定，容易用力过猛",
            "偏弱": "你目前能量偏弱，需要借力而不是硬撑",
            "中和": "你状态比较平衡，可以灵活选择推进或观望"
        }
        strength_note = strength_plain.get(label, label)

        # 用神忌神通俗翻译
        useful_stems = useful.get("stems", [])
        useful_stems_plain = self._stem_meaning(useful_stems)

        forbidden_stems = forbidden.get("stems", [])
        forbidden_stems_plain = self._stem_meaning(forbidden_stems)

        useful_note = useful.get("note", "")
        forbidden_note = forbidden.get("note", "")

        # 藏干翻译
        hidden_lines = []
        for pillar, stems in hidden.items():
            meanings = [self._stem_plain(s) for s in stems]
            hidden_lines.append(f"{pillar}藏{''.join(stems)}（{','.join(meanings)}）")

        return {
            "personality": (
                f"日主{dm_stem}，{dm_elem}属性。{elem_plain}。"
                f"月令{month_corr}月。"
            ),
            "strength": strength_note,
            "useful": {
                "what": f"天干{','.join(useful_stems)}适合你",
                "why": useful_note,
                "how": self._useful_how(dm_elem, label, useful_stems)
            },
            "forbidden": {
                "what": f"天干{','.join(forbidden_stems)}对你不利",
                "why": forbidden_note
            },
            "hidden": hidden_lines,
            "summary": (
                f"你{dm_elem}属性偏重，{strength_note}。"
                f"当前用{''.join(useful_stems)}引导方向，忌用{''.join(forbidden_stems)}硬推。"
            )
        }

    def _stem_meaning(self, stems: list[str]) -> list[str]:
        """天干 → 通俗含义"""
        meanings = {
            "甲": "甲木",
            "乙": "乙木",
            "丙": "丙火",
            "丁": "丁火",
            "戊": "戊土",
            "己": "己土",
            "庚": "庚金",
            "辛": "辛金",
            "壬": "壬水",
            "癸": "癸水"
        }
        return [meanings.get(s, s) for s in stems]

    def _stem_plain(self, stem: str) -> str:
        plain = {
            "甲": "开创力",
            "乙": "柔和适应力",
            "丙": "爆发力",
            "丁": "内敛热度",
            "戊": "承载力",
            "己": "细腻务实",
            "庚": "果断决断",
            "辛": "精致敏感",
            "壬": "流动变化",
            "癸": "内省智慧"
        }
        return plain.get(stem, stem)

    def _useful_how(self, dm_elem: str, label: str, stems: list[str]) -> str:
        """用神怎么用"""
        if "印" in stems or "庚" in stems or "戊" in stems:
            return "用温和的沟通方式，给自己和对方留空间，不要急"
        if "比" in stems or "劫" in stems:
            return "借助他人力量，找信任的人帮你推动"
        if "财" in stems or "官" in stems:
            return "用实际利益或规则来推进，靠结果说话"
        return "顺势而为，不要逆着来"

    # ── L1: 奇门术语翻译 ──────────────────────────────────────────────────────
    def _interpret_qimen(self, qimen: dict) -> dict:
        bureau = qimen.get("bureau", {})
        main = qimen.get("main_palace", {})
        door = qimen.get("door", {})
        star = qimen.get("star", {})
        god = qimen.get("god", {})
        vp = qimen.get("v3_precision", {})
        empty = vp.get("empty_palaces", [])

        ju_label = bureau.get("label", "")
        palace_name = main.get("name", "")
        door_name = door.get("name", "")
        star_name = star.get("name", "")
        god_name = god.get("name", "")

        # 宫位含义
        palace_plain = self._palace_plain(palace_name)
        # 门含义
        door_plain = self._door_plain(door_name)
        # 星含义
        star_plain = self._star_plain(star_name)
        # 神含义
        god_plain = self._god_plain(god_name)
        # 空亡通俗
        empty_plain = ""
        if empty:
            empty_plain = f"（注：{','.join(empty)}宫空亡，存在虚假信号，不要过度解读）"

        return {
            "ju": ju_label,
            "palace": {
                "name": palace_name,
                "plain": palace_plain
            },
            "door": {
                "name": door_name,
                "quality": door.get("quality", ""),
                "plain": door_plain
            },
            "star": {
                "name": star_name,
                "keywords": star.get("keywords", []),
                "plain": star_plain
            },
            "god": {
                "name": god_name,
                "plain": god_plain
            },
            "empty_note": empty_plain,
            "core_signal": (
                f"当前局势{ju_label}，主{palace_name}，{door_plain}。"
                f"主星{star_plain}，主神助{god_plain}。"
                f"{empty_plain}"
            ),
            "summary": (
                f"奇门局{ju_label}，{door.get('quality','')}门{door_name}当令。"
                f"整体局势：{self._situation_tone(palace_name, door.get('quality',''))}。"
                f"{empty_plain}"
            )
        }

    def _palace_plain(self, name: str) -> str:
        map_ = {
            "坎一宫": "风险和隐情较多，要谨慎",
            "坤二宫": "柔顺承载，适合配合和积蓄",
            "震三宫": "变动和启动，节奏加快",
            "巽四宫": "渗透和传播，适合软性影响",
            "中五宫": "核心枢纽，需要统合资源",
            "乾六宫": "领导力展示，适合明确规则",
            "兑七宫": "沟通和交易，适合谈合作",
            "艮八宫": "停止和观望，适合守势",
            "离九宫": "曝光和表达，适合展示"
        }
        return map_.get(name, f"主{name}")

    def _door_plain(self, name: str) -> str:
        map_ = {
            "开门": "大开，机会现，适合行动",
            "休门": "休息恢复，缓冲期，不宜强推",
            "生门": "生机出现，有收益，适合推进",
            "伤门": "损伤风险，冲突高，慎行动",
            "杜门": "阻断封闭，适合保密不公开",
            "景门": "曝光展示，适合表达但防虚",
            "死门": "停滞死局，适合止损复盘",
            "惊门": "动荡口舌，适合提醒曝光风险"
        }
        return map_.get(name, f"{name}门")

    def _star_plain(self, name: str) -> str:
        map_ = {
            "天蓬": "冒险和欲望，有风险但也有机会",
            "天任": "承担和稳定，进展慢但扎实",
            "天冲": "冲动和行动，容易急进冲突",
            "天辅": "辅助和学习，依赖外部支持",
            "天英": "声量和表现，容易虚火过旺",
            "天芮": "问题和病灶，隐藏问题暴露",
            "天柱": "规则和口舌，制度和沟通压力",
            "天心": "决策和修正，需要精准判断",
            "天禽": "中枢和统合，核心节点压力集中"
        }
        return map_.get(name, f"{name}星")

    def _god_plain(self, name: str) -> str:
        map_ = {
            "值符": "有权威力量主导",
            "腾蛇": "有缠绕和不确定，要防误判",
            "太阴": "有隐藏变量，注意幕后力量",
            "六合": "有合作和撮合机会",
            "白虎": "有冲突和硬碰风险",
            "玄武": "有隐瞒和信息不透明",
            "九地": "有守势和稳定力量",
            "九天": "有高举和声势力量"
        }
        # handle name like "蛇" or "太阴" or "值符"
        for k, v in map_.items():
            if k in name or name in k:
                return v
        return f"主{name}神"

    def _situation_tone(self, palace: str, quality: str) -> str:
        if "吉" in quality and "坎" in palace:
            return "有隐忧的开局，需要谨慎推进"
        if "吉" in quality:
            return "整体有利，可以顺势推进"
        if "凶" in quality:
            return "整体偏风险，建议控节奏"
        return "中性局势，边走边看"

    # ── L1: 易经术语翻译 ──────────────────────────────────────────────────────
    def _interpret_iching(self, iching: dict) -> dict:
        primary = iching.get("primary_hexagram", {})
        changed = iching.get("changed_hexagram", {})
        transition = iching.get("transition", "")
        warnings = iching.get("stage_warning", [])

        gua_name = primary.get("name", primary.get("gua", ""))
        trend = primary.get("trend", "")
        strategy = primary.get("strategy", "")
        risk = primary.get("risk", "")
        changed_name = changed.get("name", "")

        stage_hint = primary.get("stage_hint", "")[:40]
        warning_plain = self._warnings_plain(warnings)

        return {
            "gua": gua_name,
            "trend": trend,
            "strategy": strategy,
            "risk": risk,
            "changed": changed_name,
            "stage_hint": stage_hint,
            "warning": warning_plain,
            "summary": (
                f"当前主卦{gua_name}。"
                f"趋势：{trend}。"
                f"建议：{strategy}。"
                f"风险：{risk}。"
                f"若变化，趋向{changed_name}。"
            )
        }

    def _warnings_plain(self, warnings: list[str]) -> list[str]:
        plain = []
        for w in warnings:
            if "早期" in w:
                plain.append("先稳基础，不要急于放大投入")
            elif "中段" in w:
                plain.append("重点看执行过程和外部反馈")
            elif "风险" in w:
                plain.append(w.replace("本卦", "").replace("变卦", "变卦"))
            else:
                plain.append(w)
        return plain

    # ── L2: 象意整合 ─────────────────────────────────────────────────────────
    def _integrate(self, bazi_in: dict, qimen_in: dict, iching_in: dict,
                   bagua_in: dict, domain: str) -> dict:
        """把四个维度的信号整合成一个核心信息"""

        bazi = self._interpret_bazi(bazi_in)
        qimen = self._interpret_qimen(qimen_in)
        iching = self._interpret_iching(iching_in)

        # 核心主题提取
        themes = []

        # 从奇门提取主调
        door = qimen.get("door", {})
        star = qimen.get("star", {})
        if "吉" in door.get("quality", ""):
            themes.append("机会现")
        elif "凶" in door.get("quality", ""):
            themes.append("风险高")

        if star.get("name") in ["天英", "天冲"]:
            themes.append("信号强")
        if star.get("name") in ["天蓬", "天芮"]:
            themes.append("需谨慎")

        # 从易经提取方向
        if "明夷" in iching.get("changed", "") or "无妄" in iching.get("changed", ""):
            themes.append("防受伤")
        if "泰" in iching.get("changed", ""):
            themes.append("向好")

        # 从四柱提取基调
        strength = bazi.get("strength", "")
        if "弱" in strength:
            themes.append("宜守")
        elif "强" in strength:
            themes.append("可攻")

        core_theme = "、".join(themes) if themes else "中性观望"

        # 关系域特殊处理
        if domain == "relationship":
            if "吉" in door.get("quality", "") and "坎" in qimen.get("palace", {}).get("name", ""):
                tone = "有机会但有隐情，需要试探验证"
            elif "吉" in door.get("quality", ""):
                tone = "整体有利，可以顺势推进关系"
            elif "凶" in door.get("quality", ""):
                tone = "当前风险偏高，建议收敛等待"
            else:
                tone = "中性局势，边聊边观察"
        else:
            tone = qimen.get("summary", {}).get("core_signal", "")

        return {
            "core_theme": core_theme,
            "tone": tone,
            "bazi_summary": bazi.get("summary", ""),
            "qimen_summary": qimen.get("summary", ""),
            "iching_summary": iching.get("summary", ""),
            "integrated": f"{core_theme}。{tone}。{bazi.get('strength','')}。"
        }

    # ── L3: 行动建议 ─────────────────────────────────────────────────────────
    def _action(self, report: dict) -> dict:
        """把三路径和信号收敛成一个可执行的一句话动作"""
        branches = report.get("future", {}).get("branches", [])
        best_action = report.get("strategy", {}).get("best_action", "")

        if not branches:
            return {"one_liner": best_action or "顺势而为", "paths": []}

        # 路径翻译
        path_plain = []
        for b in branches:
            name = b["name"]
            prob = b["probability"]
            triggers = b.get("trigger_conditions", [])
            triggers_plain = [self._trigger_plain(t) for t in triggers[:2]]
            domain = report.get("query", {}).get("domain", "unknown")
            path_plain.append({
                "name": name,
                "prob": f"{prob*100:.0f}%",
                "triggers": triggers_plain,
                "action": self._path_action(name, domain)
            })

        # 一句话行动
        top_path = path_plain[0] if path_plain else {}
        one_liner = self._build_one_liner(report, top_path, domain)
        watch = report.get("strategy", {}).get("watch_signals", [])
        return {
            "one_liner": one_liner,
            "paths": path_plain,
            "watch_signals": [self._trigger_plain(t) for t in watch[:3]]
        }

    def _trigger_plain(self, trigger: str) -> str:
        map_ = {
            "现实反馈持续增强": "对方回应变积极",
            "关键风险未触发": "没有出意外",
            "信息不足继续扩大": "对方依然冷淡",
            "外部变量介入": "有新变量出现",
            "执行动作过急或过慢": "节奏失调",
            "隐藏变量暴露": "对方暴露真实意图",
            "时间窗口变化": "时机窗口错过",
            "关键人物态度突变": "对方态度突然变化",
            "对方/市场/环境是否持续反馈": "看对方是否持续回应",
            "关键时间节点是否出现新变量": "看关键节点是否有变化",
            "风险信号是否从隐性变显性": "看风险是否变明显"
        }
        return map_.get(trigger, trigger)

    def _path_action(self, name: str, domain: str) -> str:
        if "顺势" in name:
            return "继续当前节奏，观察反馈" if domain != "relationship" else "继续聊天节奏，保持自然"
        if "受阻" in name:
            return "收敛等待，不宜强推" if domain != "relationship" else "减少主动，观望等待"
        if "反转" in name:
            return "准备PLAN B，重新评估" if domain != "relationship" else "准备撤退或调整策略"
        return "保持当前策略"

    def _build_one_liner(self, report: dict, top_path: dict, domain: str) -> str:
        bazi_in = report.get("symbolic", {}).get("bazi", {})
        qimen_in = report.get("symbolic", {}).get("qimen", {})
        bazi = self._interpret_bazi(bazi_in)
        qimen = self._interpret_qimen(qimen_in)
        door_name = qimen_in.get("door", {}).get("name", "")
        door_quality = qimen_in.get("door", {}).get("quality", "")

        strength_note = bazi.get("strength", "")
        useful_how = bazi.get("useful", {}).get("how", "")

        # 根据门和路径组合
        if "凶" in door_quality:
            if domain == "relationship":
                return f"{strength_note}。{useful_how}。奇门{door_name}当令，不宜强聊，先缓一缓。"
            return f"{strength_note}。{useful_how}。当前风险偏高，先控节奏。"

        if "开门" in door_name or "生门" in door_name:
            if domain == "relationship":
                return f"{strength_note}。{useful_how}。奇门开门有势，可以主动一点，但要看反馈。"
            return f"{strength_note}。{useful_how}。有机会，可以顺势推进。"

        if "休门" in door_name or "杜门" in door_name:
            if domain == "relationship":
                return f"{strength_note}。{useful_how}。奇门偏静，不宜高频打扰，保持低频沟通。"
            return f"{strength_note}。{useful_how}。当前偏保守，适合蓄势。"

        return f"{strength_note}。{useful_how}。看情况推进，注意反馈。"

    # ── 主入口 ────────────────────────────────────────────────────────────────
    def interpret(self, report: dict) -> dict:
        """把完整报告翻译成用户能看懂的结构化解读"""
        bazi = report.get("symbolic", {}).get("bazi", {})
        qimen = report.get("symbolic", {}).get("qimen", {})
        iching = report.get("symbolic", {}).get("iching", {})
        bagua = report.get("symbolic", {}).get("bagua", {})
        strategy = report.get("strategy", {})
        domain = report.get("query", {}).get("domain", "unknown")

        bazi_int = self._interpret_bazi(bazi)
        qimen_int = self._interpret_qimen(qimen)
        iching_int = self._interpret_iching(iching)
        integrated = self._integrate(bazi, qimen, iching, bagua, domain)
        action = self._action(report)

        return {
            "version": "1.0",
            "bazi": bazi_int,
            "qimen": qimen_int,
            "iching": iching_int,
            "integrated": integrated,
            "action": action,
            "plain_title": self._build_title(bazi, qimen, domain),
            "plain_summary": self._build_summary(integrated, action)
        }

    def _build_title(self, bazi: dict, qimen: dict, domain: str) -> str:
        dm = bazi.get("day_master", {}).get("stem", "")
        label = bazi.get("v3_precision", {}).get("balance_analysis", {}).get("label", "")
        door = qimen.get("door", {}).get("name", "")
        quality = qimen.get("door", {}).get("quality", "")

        if domain == "relationship":
            return f"{dm}{label} · 奇门{door}{quality} · 局势解读"
        return f"{dm}{label} · 奇门{door} · 局势解读"

    def _build_summary(self, integrated: dict, action: dict) -> str:
        parts = []
        tone = integrated.get("tone", "")
        if tone:
            parts.append(tone)
        one_liner = action.get("one_liner", "")
        if one_liner:
            parts.append(one_liner)
        return "。".join(parts)