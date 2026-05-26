# ZhaoJian 照见系统

**东方象数推演引擎**

融合八卦、五行、四柱、奇门、易经，预测路径、复盘节点、给出行动建议。

---

## 引擎

| 引擎 | 能力 |
|------|------|
| 四柱 | 六十甲子 · 节气月令 · 十神藏干 · 用神忌神 |
| 奇门 | 九宫飞布 · 八门九星八神 · 主客判断 · 三冲分析 |
| 易经 | 64卦 · 本卦错卦互卦 · 动爻阶段 |
| 人间关系 | 性格冲突 · 关系危机 · 边界困扰 · 情感困惑 |
| 通俗解读 | 术语 → 人话 + 可执行动作 |

---

## 快速开始

```bash
cd backend
pip install -r requirements.txt

# 命令行
PYTHONPATH=. python scripts/zhaojian_cli.py \
  "我想追这个女生，后续怎么推进？" \
  --domain relationship \
  --birth-datetime "1998-06-15 14:30"

# API
curl -X POST http://localhost:5000/api/zhaojian/run \
  -H "Content-Type: application/json" \
  -d '{
    "question": "这个项目适不适合发布？",
    "domain": "strategy",
    "event_time": "2026-05-26 22:00"
  }'
```

---

## 报告结构

```
1. 现实解析    事实清单 + 时间线 + 已知/未知变量
2. 因果时序    过去节点反推
3. 概率分支    未来三条路径（A/B/C）
4. 行动建议    最佳动作 + 禁忌 + 观察信号
5. 四柱分析    六十甲子 + 十神 + 用神忌神
6. 奇门分析    九宫飞布 + 八门/九星/八神
7. 易经分析    主卦 + 错卦 + 互卦 + 动爻
8. 通俗解读    一句话说结论 + 分层行动建议
```

---

## 技术栈

- 后端：Python + Flask
- 前端：Vue 3 + Vite + Pinia
- 象数引擎：纯 Python，无外部易学依赖

---

## License

基于 [MiroFish](https://github.com/666ghj/MiroFish) 源码重建，AGPL-3.0