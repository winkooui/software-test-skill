---
name: software-test-skill
description: "软件测试全生命周期 Skill 套件。支持测试用例生成（含左移/变更影响分析/相近度报表/用户视角/回归策略/环境分层/自我审查8层）和测试报告生成（含KPI仪表盘/7种图表/上线就绪度评分）。当用户需要根据PRD生成测试用例，或根据执行追踪数据生成测试报告时触发。"
license: MIT
---

# 软件测试 Skill 套件 v2.3

## 平台自检（最先执行）
判断平台(SOLO/Claude Code/Trae/Qoder/Codex) → 检查 Python + openpyxl + matplotlib → 确定降级策略

## 模块一：测试用例生成
从 PRD 到 Excel 的 6 阶段流程：

**阶段0 测试左移** → 按 `frameworks/testability-checklist.md` 评估可测试性，评分<6则反馈需求方
**阶段1 需求获取** → 提取产品目标、功能列表、业务流程、非功能需求、已知约束  
**阶段2 产品分析** → 架构分析 + 功能树 + **变更影响五层追溯** + **相近度计算**(引用 `frameworks/proximity-model.md`) + 环境策略 + 数据策略
**阶段3 交互确认** → 展示相近度报表，反问11个问题(每次≤4个)，含回归范围确认
**阶段4 用例生成** → 标准业务用例(按 `frameworks/test-type-methods.md` 自适应类型策略) + 回归分层(高/中/低/微) + 环境分层(沙箱/SIT/UAT/生产) + 用户视角三类(引用 `frameworks/user-perspective-checklist.md`) + Prod门禁集
**阶段5 8层审查** → 功能点覆盖率≥95% + 串联分析 + 类型覆盖≥3 + 环境覆盖 + 用户视角≥2/模块 + 回归覆盖(高100%/中≥70%/低≥50%) + 数据完备≥90% + 遗漏识别
**阶段6 交付** → 11Sheet Excel(引用 `templates/excel-schema.json`) + 相近度报表 + 回归确认单 + Prod门禁单

### 相近度模型
`综合 = 代码×0.30 + 数据×0.25 + API×0.20 + 业务×0.15 + UI×0.10`，每维0-5分，≥4.0高/2.0-3.9中/1.0-1.9低/0.1-0.9微/0无关

### 用户视角三类
新手探索式(零基础直觉) / 非预期路径(快速连击/后退/多Tab) / 直觉偏差(用户理解≠设计)

### 用例字段规范
30个字段分6组，引用 `schemas/test-case-fields.yaml`，含编号规则 `TC-{MODULE}-{FUNC}-{SEQ}-{TYPE}` + 9种类型标识(F/I/P/S/C/U/E/N/R)

## 模块二：测试报告生成
从测试追踪数据到 Excel 报告的 6 步骤：

**步骤1 接收解析** → pandas读取，自动识别列结构，提取元数据
**步骤2 数据清洗** → 完整性/状态标准化/合理性校验，输出数据质量报告
**步骤3 多维统计** → 整体/按优先级/按模块/按类型/覆盖率/缺陷/效率 7维度
**步骤4 图表生成** → 9种图表(引用 `templates/chart-specs.json`)，无matplotlib时降级为ASCII art
**步骤5 风险评估** → 按 `frameworks/risk-identification-rules.md` 的10条规则自动识别 → 6因子上线就绪度评分 → 结论建议
**步骤6 交付** → 10Sheet Excel(引用 `templates/excel-schema.json`)含KPI卡片+图表+条件格式

### 风险规则
P0未全通过(🔴) / 整体<85%(🔴) / 致命遗留(🔴) / 严重>3(🟠) / 阻塞>5%(🟠) / 修复<60%(🟠) / 回归<90%(🟠) / 趋势上扬(🟡)

### 上线就绪度
基础100分 - 扣分项(P0未通过-3/个 etc.) + 加分项(灰度+3 etc.) → A≥90/B≥75/C≥60/D<60

## 文件结构引用
- 工作流: `workflows/test-case-generation.md` / `workflows/test-report-generation.md`
- 框架: `frameworks/proximity-model.md` / `testability-checklist.md` / `test-type-methods.md` / `user-perspective-checklist.md` / `risk-identification-rules.md`
- Schema: `schemas/test-case-fields.yaml` / `test-case-record.schema.json` / `test-execution-record.schema.json`
- 模板: `templates/excel-schema.json` / `chart-specs.json` / `tool-mapping.md`
- 能力契约: `capability-contract.yaml`
- 平台适配: `adapters/solo/` / `adapters/claude-code/` / `adapters/trae-qoder/` / `adapters/codex/`
