# 软件测试 Skill 套件 — 目录结构与文件功能总览

## 一、套件概览

| 维度 | 说明 |
|------|------|
| 名称 | `software-test-skill` |
| 版本 | v2.4 |
| 文件总数 | 38 个 |
| 代码总行数 | 约 6,226 行 |
| 语言 | YAML / Markdown / JSON / Python (requirements.txt) |
| 目标平台 | SOLO、Claude Code、Trae、Qoder、Codex |

---

## 二、顶层目录结构

```
software-test-skill/
├── SKILL.md                    ← 入口，YAML frontmatter + 双模块概要
├── core/                       ← 核心逻辑层（平台无关）
├── adapters/                   ← 平台适配层
├── scripts/                    ← 可执行脚本与依赖
├── examples/                   ← 示例 PRD、执行记录、输出样例
├── tests/                      ← 自测用例
├── agents/                     ← OpenAI UI 元数据
└── .github/workflows/          ← CI 校验
```

---

## 三、各目录文件详解

### 3.1 根目录

| 文件 | 格式 | 行数 | 功能 |
|------|------|------|------|
| `SKILL.md` | Markdown | 431 | Skill 入口文件。含 YAML frontmatter（name、description、license、triggers），以及双模块核心能力、平台自检、框架摘要、审查清单和使用示例。 |

---

### 3.2 `core/` — 核心逻辑层（平台无关）

#### 3.2.1 `core/prompts/` — Prompt 定义

| 文件 | 格式 | 行数 | 功能 |
|------|------|------|------|
| `main-prompt.md` | Markdown | 464 | 去平台化的完整 Prompt。含 `[PLATFORM_PROBE]` 自检段、`[ROLE]` 角色定义、`[TRIGGER]` 触发条件、`[WORKFLOW]` 双模块概要、`[FRAMEWORKS]` 分析方法引用、`[TEMPLATES]` 输出模板索引、`[RULES]` 执行规则、`[CHECKLIST]` 审查清单、`[EXAMPLES]` 使用示例。是所有平台适配器的 Prompt 源。 |

#### 3.2.2 `core/workflows/` — 工作流定义

| 文件 | 格式 | 行数 | 功能 |
|------|------|------|------|
| `test-case-generation.md` | Markdown | 243 | 测试用例生成 6 阶段完整工作流。每个阶段标注输入、处理逻辑、输出、门禁条件和参考耗时。含 11 条反问题模板、5 类条件反问、引用文件索引、平台适配说明。 |
| `test-report-generation.md` | Markdown | 306 | 测试报告生成 6 步骤完整工作流。含数据输入格式定义（3 种方式）、列名别名匹配规则、状态标准化映射表、7 种统计维度、9 种图表驱动、数据质量报告模板、10 个 Sheet 结构一览。 |

#### 3.2.3 `core/frameworks/` — 分析框架（5 个）

| 文件 | 格式 | 行数 | 功能 |
|------|------|------|------|
| `proximity-model.md` | Markdown | 128 | **相近度计算模型**。定义综合相近度 = 代码×0.30 + 数据×0.25 + API×0.20 + 业务×0.15 + UI×0.10。每维有 0-5 分评分标准、等级划分与回归深度映射、完整计算示例、4 条校准规则（历史缺陷模块/支付模块/中间件变更/DDL操作自动提级）。 |
| `test-type-methods.md` | Markdown | 391 | **测试类型设计方法与覆盖要点**。9 种测试类型（F/I/P/S/C/U/E/N/R）各自的方法论与 Checklist：功能测试 6 种设计方法 + 9 项覆盖清单、接口测试 6 种方法 + 10 项清单、性能测试 5 种子类型 + 7 项指标阈值表、安全测试 5 种方法 + 9 项清单、兼容性测试矩阵 + 4 维缩减策略、UX 测试 8 项清单、异常边界 9 项清单。含用户意图自适应检测表（9 类关键词 → 类型策略调整）和多类型组合规则。 |
| `testability-checklist.md` | Markdown | 108 | **需求可测试性分析检查清单**。5 个维度 22 项检查点（需求清晰度 5 项、可验证性 4 项、完整性 5 项、数据可获取性 4 项、依赖清晰度 4 项）。含评分规则（0-10 分）和风险等级判定（≥8 低风险、6-7.9 中风险、4-5.9 高风险、<4 严重风险）。附带快速自评 5 问。 |
| `user-perspective-checklist.md` | Markdown | 123 | **用户视角测试检查清单**。三类用户视角用例的总计 26 条检查项——新手探索式 7 项（3秒认知、首要操作识别、自然操作路径等）、非预期路径 10 项（快速连击、浏览器后退/刷新、多Tab、网络中断等）、直觉偏差 9 项（提交≠成功、删除=彻底删除、退出=切换账号等）。含 5 种用户画像定义与测试焦点。 |
| `risk-identification-rules.md` | Markdown | 118 | **风险识别规则与上线就绪度算法**。10 条自动风险规则（触发条件 + 风险等级 + 缓解措施），6 因子上线就绪度扣分算法（P0未通过 -3/个、致命缺陷 -10/个、严重缺陷 -3/个 等），补充调整项（回归全通过 +5、灰度方案 +3、回滚方案 +3、历史事故 -5）。评分分级：A≥90 / B≥75 / C≥60 / D<60。含缺陷严重度定义和风险报告模板。 |

#### 3.2.4 `core/schemas/` — 数据 Schema（3 个）

| 文件 | 格式 | 行数 | 功能 |
|------|------|------|------|
| `test-case-fields.yaml` | YAML | 693 | **测试用例组成字段完整规范**。定义 30 个字段，分 6 组。核心字段 12 个（编号/模块/功能/类型/优先级/名称/前置条件/步骤/数据/数据准备/预期结果/实际结果），扩展字段 6 个（环境/环境限制/前置用例/后置用例/关联需求/关联测试点），用户视角字段 2 个，回归字段 5 个，执行追踪字段 4 个，元数据 1 个。每个字段含类型、必填性、描述、格式约束、选项枚举、正反例、校验规则。含用例编号规则（`TC-{MODULE}-{FUNC}-{SEQ}-{TYPE}`）与 9 种类型标识码定义。含 Excel A-AD 列映射表。含 11 条完整性检查清单（分 error/warning 两级）。 |
| `test-case-record.schema.json` | JSON | 183 | **测试用例记录 JSON Schema**。使用 Draft 2020-12 规范，定义所有 30 个字段的类型、枚举值、正则校验、条件必填（回归用例必填相近度等级和回归深度、用户视角用例必填标签和用户画像）。 |
| `test-execution-record.schema.json` | JSON | 101 | **测试执行追踪记录 JSON Schema**。定义执行状态/实际结果/执行人/执行日期/执行环境/缺陷ID/缺陷严重度/缺陷状态/执行耗时/重试次数等字段。条件必填：失败时强制要求缺陷ID。 |

#### 3.2.5 `core/templates/` — 输出模板（3 个）

| 文件 | 格式 | 行数 | 功能 |
|------|------|------|------|
| `excel-schema.json` | JSON | 223 | **Excel 输出结构定义**。测试用例工作簿 11 个 Sheet 的完整结构（每 Sheet 的列定义、列宽、条件格式规则），测试报告工作簿 10 个 Sheet 的结构（含 KPI 指标定义和数据源公式），统一样式规范（字体/表头/zebra striping/边框/KPI 高亮/风险色标）。 |
| `chart-specs.json` | JSON | 156 | **图表规格定义**。10 种图表（通过率饼图、模块堆叠柱状图、类型雷达图、执行趋势折线图、优先级堆叠图、缺陷严重度饼图、缺陷模块柱状图、缺陷趋势图、上线就绪度进度条、效率对比柱状图）。每种图表含类型/数据源/颜色/阈值/标签/排序规则。无 matplotlib 时的 ASCII art 降级方案。 |
| `tool-mapping.md` | Markdown | 87 | **四平台工具名称映射表**。16 项通用能力 × 4 平台逐对照（读取文件/写入文件/编辑文件/列出目录/执行命令/检查状态/搜索/用户交互/代码搜索/任务跟踪/子Skill嵌套/Excel生成/图表生成）。含路径变量映射、用户交互降级策略（各平台格式模板）、能力检测命令（5 条）、平台检测方法。 |

#### 3.2.6 `core/capability-contract.yaml`

| 文件 | 格式 | 行数 | 功能 |
|------|------|------|------|
| `capability-contract.yaml` | YAML | 414 | **平台无关能力契约**。定义 14 种通用能力接口（文件读写/追加/列表/存在检查、命令执行/检查、网页搜索/获取、用户交互、代码搜索、环境信息），每种含参数名/类型/必填/默认值/返回值/错误码。扩展能力 4 种（Excel生成/图表嵌入/Skill嵌套/Todo跟踪）。降级策略 5 条。路径变量规范。工具名称映射表（4 平台）。验证检查清单。 |

---

### 3.3 `adapters/` — 平台适配层（4 个）

| 目录/文件 | 格式 | 行数 | 功能 |
|-----------|------|------|------|
| `solo/adapter-config.yaml` | YAML | 162 | SOLO 平台适配器。工具映射（`Read`/`Write`/`RunCommand`/`AskUserQuestion`/`TodoWrite`/`CheckCommandStatus`），路径映射（`/sessions/{id}/workspace`，`/sessions/{id}/work`），能力声明（全功能支持，含 `Skill` 嵌套调用），依赖安装（`--break-system-packages`），平台检测规则（AskUserQuestion + TodoWrite 工具检测 + `/sessions/` 路径检测）。 |
| `claude-code/adapter-config.yaml` | YAML | 203 | Claude Code 平台适配器。工具映射（`Bash`/`Read`/`Write`/`Grep`），路径映射（项目相对路径），能力声明（Python 需用户安装依赖），frontmatter 模板（含 `name`/`description`/`disable-model-invocation`/`triggers`），用户交互降级格式模板（文本形式一次性提问），Skill 目录结构要求（`.claude/skills/software-test-suite/SKILL.md` + `references/`），平台检测规则（`.claude` 目录检测）。 |
| `trae-qoder/adapter-config.yaml` | YAML | 170 | Trae / Qoder 平台适配器（两平台共享 Skills 格式）。工具映射、路径映射（`{project_root}/test-output`）、Markdown header 格式模板、安装方式（市场安装 + 手动导入）。 |
| `codex/adapter-config.yaml` | YAML | 206 | Codex (OpenAI) 平台适配器。能力声明（大部分为 `false`：不可用 Excel/图表/命令执行），GPT Instructions 格式模板，全降级策略（Excel→Markdown+CSV，图表→ASCII art，命令→提示用户本地执行），工作流建议（Codex 文本分析 → 本地 Python 生成 Excel）。 |

---

### 3.4 `scripts/` — 可执行脚本

| 文件 | 格式 | 行数 | 功能 |
|------|------|------|------|
| `requirements.txt` | Python | 26 | Python 依赖清单。核心依赖：openpyxl≥3.1.0、pandas≥2.0.0、matplotlib≥3.8.0。含一键安装命令和各平台注意事项（SOLO 需 `--break-system-packages`）、安装后验证命令。 |
| `generate_test_cases.py` | Python | 249 | 从示例 PRD 生成测试用例 CSV/Markdown；若安装 openpyxl，则额外输出 Excel。用于 GitHub 访客本地试跑。 |
| `generate_report.py` | Python | 199 | 从执行记录 CSV 生成测试报告 Markdown、模块统计 CSV；若安装 openpyxl，则额外输出 Excel。 |
| `validate_schema.py` | Python | 100 | 校验 JSON 模板可解析、示例测试用例 CSV 和执行记录 CSV 满足核心约束。 |

---

### 3.5 `examples/` 和 `tests/`

| 目录/文件 | 状态 | 说明 |
|-----------|------|------|
| `examples/prd-login.md` | 已提供 | 脱敏登录需求示例，用于演示 PRD 到测试用例的输入。 |
| `examples/sample-test-cases.csv` | 已提供 | 结构化测试用例样例，字段对齐测试用例 Schema。 |
| `examples/execution-records.csv` | 已提供 | 测试执行追踪数据样例，包含通过、失败、阻塞、跳过状态。 |
| `examples/sample-report.md` | 已提供 | 测试报告输出样例，展示 KPI、风险和结论格式。 |
| `tests/test_examples.py` | 已提供 | 基于 unittest 的示例数据和生成脚本 smoke test。 |
| `.github/workflows/ci.yml` | 已提供 | GitHub Actions：校验 schema/examples 并运行测试。 |
| `agents/openai.yaml` | 已提供 | OpenAI/Codex UI 展示元数据与默认提示。 |

---

## 四、文件分类统计

| 分类 | 文件数 | 行数 | 占比 |
|------|--------|------|------|
| 核心 Prompt | 1 | 464 | 7.6% |
| 工作流定义 | 2 | 549 | 9.0% |
| 分析框架 | 5 | 868 | 14.2% |
| 数据 Schema | 3 | 977 | 15.9% |
| 输出模板 | 3 | 466 | 7.6% |
| 能力契约 | 1 | 414 | 6.8% |
| 平台适配器 | 4 | 741 | 12.1% |
| 示例输入输出 | 4 | 106 | 1.7% |
| 脚本/依赖 | 4 | 574 | 9.4% |
| 测试与 CI | 2 | 103 | 1.7% |
| 入口与说明 | 4 | 803 | 13.1% |
| 元数据 | 1 | 8 | 0.1% |
| 仓库配置 | 1 | 42 | 0.7% |
| **合计** | **38** | **约 6,226** | **100%** |

---

## 五、文件间引用关系

```
SKILL.md ─────────────────────────────────────────────────────────┐
  │ 引用:  workflows/  frameworks/  schemas/  templates/          │
  │        capability-contract.yaml                                │
  ▼                                                                │
main-prompt.md ───────────────────────────────────────────────────┤
  │ 引用:  所有 frameworks/  所有 templates/  所有 schemas/        │
  │        capability-contract.yaml                                │
  ▼                                                                │
workflows/test-case-generation.md ────────────────────────────────┤
  │ 引用:  frameworks/proximity-model.md                          │
  │        frameworks/test-type-methods.md                         │
  │        frameworks/testability-checklist.md                     │
  │        frameworks/user-perspective-checklist.md               │
  │        schemas/test-case-fields.yaml                           │
  │        templates/excel-schema.json                             │
  ▼                                                                │
workflows/test-report-generation.md ──────────────────────────────┤
  │ 引用:  frameworks/test-type-methods.md                         │
  │        frameworks/risk-identification-rules.md                 │
  │        templates/chart-specs.json                              │
  │        templates/excel-schema.json                             │
  ▼                                                                │
adapters/solo/adapter-config.yaml ────────────────────────────────┤
adapters/claude-code/adapter-config.yaml ─────────────────────────┤
adapters/trae-qoder/adapter-config.yaml ──────────────────────────┤
adapters/codex/adapter-config.yaml ───────────────────────────────┤
  │ 引用:  capability-contract.yaml (所有适配器)                    │
  ▼                                                                │
scripts/ ──────────────── 示例生成、报告生成、schema 校验             │
examples/ ─────────────── 示例 PRD、执行记录、测试用例、报告样例       │
tests/ ────────────────── smoke test + 示例数据检查                  │
.github/workflows/ci.yml ─ CI 调用 validate_schema.py 和 unittest     │
```

---

*文档更新时间: 2026-06-11 | Skill 版本: v2.4*
