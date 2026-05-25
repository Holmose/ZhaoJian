# TianJi 天机推演系统

> 东方象数增强型多智能体推演系统：融合现实数据、易经八卦、五行、四柱八字、奇门遁甲与 Multi-Agent Simulation，用于过去反推，未来分支预测与决策推演。

TianJi is an oriental philosophy enhanced multi-agent simulation system for causal reconstruction, future branching, and decision strategy.

## 当前状态

当前版本为 **V0.5.0 / V1-V5 Prototype Completed**，已完成五层核心能力与完整工程体系：

- **V1 语义推演底座**：现实解析、八卦象意、五行动力、本地多 Agent 推演、因果回溯、未来三路径、Markdown / JSON 报告、CLI、HTTP API `/api/tianji/run`
- **V2 四柱人物长期结构模型**：出生时间输入、近似四柱、日主、可见十神、五行比例、人物倾向、风险模式、Agent 参数
- **V3 奇门事件局势引擎**：事件时间/地点输入、语义阴阳遁局、九宫、八门、九星、八神、主客关系、时机提示、风险提示、行动提示
- **V4 易经 64 卦趋势演化引擎**：完整 64 卦语义数据、本卦/变卦、变爻阶段提示、趋势转化、阶段风险、行动提示
- **V5 示例与测试体系**：3 个领域样例输入、`sample_reports/` 完整报告、4 个单元测试、`npm run test` / `npm run samples`

当前系统已经形成完整推演链路：

```
现实解析
  ↓
八卦/五行状态象意
  ↓
易经64卦趋势演化
  ↓
四柱人物长期结构
  ↓
奇门事件时机局势
  ↓
多 Agent 争论收敛
  ↓
过去反推 + 未来三路径 + 行动建议
```

快速体验完整链路（包含全部 V1-V4 模块）：

```bash
cd backend
PYTHONPATH=. python scripts/tianji_cli.py \
  "这个天机推演系统还没完全成熟，未来适不适合继续扩张和公开发布？" \
  --domain strategy \
  --goal "判断项目发布与扩张路线" \
  --event-time "2026-05-26 22:10" \
  --location "Guangzhou" \
  --birth-datetime "1998-06-15 14:30" \
  --gender male \
  --out reports/tianji
```

运行测试：

```bash
npm run test
```

生成样例报告：

```bash
npm run samples
```

## API

```http
POST /api/tianji/run
```

请求示例：

```json
{
  "question": "我现在想做一个东方哲学增强型推演系统，未来这个项目能不能做大？",
  "domain": "strategy",
  "goal": "判断项目路线",
  "event_time": "2026-05-26 22:10",
  "location": "Guangzhou",
  "birth_datetime": "1998-06-15 14:30",
  "gender": "male",
  "rounds": 3,
  "save_report": true
}
```

## 文档

- [TianJi 详细说明](./README_TIANJI.md)
- [系统架构文档](./docs/TIANJI_ARCHITECTURE.md)
- [API 文档](./docs/API.md)
- [Roadmap](./docs/ROADMAP.md)
- [Examples](./examples/README.md)
- [Sample Reports](./sample_reports/README.md)
- [Contributing](./CONTRIBUTING.md)
- [Changelog](./CHANGELOG.md)

## 路线图

### V1：语义推演版

- 八卦象意映射
- 五行动力模型
- 易经语义趋势库
- 本地多 Agent 推演适配
- 因果回溯
- 未来三路径
- 报告生成

### V2：四柱人物模型版

- 干支基础数据
- 十神映射数据
- 出生时间输入
- 近似年/月/日/时柱计算
- 日主识别
- 可见天干十神分析
- 五行比例计算
- 人物长期倾向、风险模式、Agent 参数
- 与 TianJi 报告集成

注意：V2 当前采用公历近似计算，月柱尚未按节气修正，大运/流年/用神分析将在后续版本增强。

### V3：奇门事件局势版

- 事件时间/地点输入
- 语义阳遁/阴遁与局数
- 九宫语义模型
- 八门行动模型
- 九星事件能量模型
- 八神隐性变量模型
- 主客关系判断
- 时机提示、风险提示、行动提示

注意：V3 当前是语义奇门局势引擎，尚不是完整传统奇门排盘；节气、阴阳遁精确起局、天地盘、用神定位将在后续版本增强。

### V4：完整 64 卦易经趋势引擎

- 完整 64 卦语义数据集
- 本卦/变卦趋势模型
- 变爻阶段提示
- 趋势转化说明
- 阶段风险与行动提示
- 与多 Agent 推演报告集成

### V5：示例与测试体系

- 3 个领域样例输入
- `sample_reports/` 完整 Markdown / JSON 报告
- 4 个单元测试覆盖 IChing / Bazi / Qimen / Orchestrator
- `npm run test` / `npm run samples`

### V6：深度推理增强

计划接入更复杂的多步推理能力，增强模拟适配器。

## 使用原则

1. 现实优先，象数辅助。
2. 多路径输出，不做绝对断言。
3. 每个判断尽量标注来源：现实证据 / 象数标签 / Agent 共识。
4. 必须保留反方质疑。
5. 结果必须可复盘、可回填、可迭代。
6. 高风险领域如投资、医疗、法律，只做辅助推演，不替用户决策。

## License & Attribution

This prototype is rebuilt on top of the MiroFish codebase and follows the original AGPL-3.0 license. See [LICENSE](./LICENSE) and [NOTICE.md](./NOTICE.md).
