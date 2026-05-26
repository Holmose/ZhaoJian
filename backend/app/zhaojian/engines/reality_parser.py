from __future__ import annotations

import re

DOMAIN_HINTS = {
    "relationship": ["女生", "男生", "恋爱", "复合", "暧昧", "关系", "她", "他", "约会"],
    "business": ["客户", "成交", "销售", "项目", "合作", "产品", "商业", "投资"],
    "content": ["作品", "视频", "抖音", "小红书", "朋友圈", "流量", "爆", "人设"],
    "personal": ["人生", "职业", "阶段", "状态", "选择", "未来", "过去"],
    "strategy": ["战略", "系统", "路线", "布局", "长期", "竞争"]
}

class RealityParser:
    def parse(self, text: str, domain: str = "unknown", goal: str = "") -> dict:
        if domain == "unknown":
            domain = self.detect_domain(text)
        sentences = [s.strip() for s in re.split(r"[。！？\n；;]+", text) if s.strip()]
        facts = sentences[:12]
        unknowns = []
        if any(x in text for x in ["会不会", "能不能", "是不是", "为什么", "未来", "后面"]):
            unknowns.append("结果走向仍未验证，需要用多路径而非单结论处理")
        if "时间" not in text and "什么时候" not in text:
            unknowns.append("缺少明确时间节点，奇门/周期判断仅能做语义级参考")
        people = []
        for p in ["我", "她", "他", "客户", "团队", "合作方", "用户", "对手"]:
            if p in text: people.append(p)
        return {
            "domain": domain,
            "facts": facts or [text],
            "timeline": [s for s in sentences if any(t in s for t in ["之前", "现在", "后来", "今天", "明天", "昨天", "去年", "今年"])],
            "people": people,
            "known_variables": self.extract_variables(text),
            "unknown_variables": unknowns,
            "constraints": ["现实证据优先", "象数只作建模语言", "输出必须保留概率分支和盲区"]
        }

    def detect_domain(self, text: str) -> str:
        scores = {d: 0 for d in DOMAIN_HINTS}
        for d, words in DOMAIN_HINTS.items():
            for w in words:
                if w in text: scores[d] += 1
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "unknown"

    def extract_variables(self, text: str) -> list[str]:
        vars = []
        if any(x in text for x in ["钱", "价格", "成交", "预算"]): vars.append("利益/资源变量")
        if any(x in text for x in ["情绪", "冷", "热", "主动", "暧昧"]): vars.append("情绪/关系变量")
        if any(x in text for x in ["时间", "周期", "今晚", "明天", "今年"]): vars.append("时间窗口变量")
        if any(x in text for x in ["曝光", "流量", "传播", "内容"]): vars.append("传播/认知变量")
        if any(x in text for x in ["风险", "失败", "担心", "不确定"]): vars.append("风险变量")
        return vars or ["目标变量", "信息完整度变量", "执行变量"]
