# Software Test Skill Suite · 软件测试 Skill 套件

[![Version](https://img.shields.io/badge/version-2.4-blue)](https://github.com/winkooui/software-test-skill)
[![CI](https://github.com/winkooui/software-test-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/winkooui/software-test-skill/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Platforms](https://img.shields.io/badge/platforms-4-orange)](#supported-platforms)

把 PRD、变更说明或测试执行记录交给 AI 助手，生成结构化测试用例、回归范围、Prod 上线门禁和测试报告。

适合 QA、测试负责人、研发团队和需要把“需求 -> 测试设计 -> 执行报告”流程标准化的 AI Agent 工作流。

## Why This Skill

| 常见痛点 | 本 Skill 提供 |
|----------|---------------|
| PRD 写完后测试点容易漏 | 22 项可测试性检查 + 9 类测试类型覆盖 |
| 回归范围靠经验拍脑袋 | 代码/数据/API/业务/UI 五维相近度模型 |
| 只生成普通功能用例 | 新手探索、非预期路径、直觉偏差三类用户视角用例 |
| 上线前风险说不清 | P0、缺陷严重度、阻塞项、灰度/回滚因子合成上线就绪度 |
| AI 输出格式不稳定 | JSON Schema、Excel 模板、示例 CSV 和可执行脚本约束输出 |

## 60 秒试跑

不依赖网络，不需要 LLM。脚本会基于示例 PRD 和执行记录生成可预览的 CSV/Markdown；如本机安装了 `openpyxl`，会额外生成 `.xlsx`。

```bash
python scripts/generate_test_cases.py \
  --input examples/prd-login.md \
  --out-dir test-output

python scripts/generate_report.py \
  --input examples/execution-records.csv \
  --out-dir test-output

python scripts/validate_schema.py --root .
python scripts/evaluate_quality.py --input examples/sample-test-cases.csv --min-score 75
python -m unittest discover -s tests -v
```

生成结果：

```text
test-output/
├── login-test-cases.csv
├── login-test-cases.md
├── login-report-summary.csv
└── login-test-report.md
```

示例文件：

- [示例 PRD](./examples/prd-login.md)
- [示例测试用例 CSV](./examples/sample-test-cases.csv)
- [示例执行记录 CSV](./examples/execution-records.csv)
- [示例测试报告](./examples/sample-report.md)
- [登录场景 Benchmark](./benchmarks/login/evaluation.md)

## Core Capabilities

### 1. 测试用例生成

从 PRD/需求文档生成结构化测试用例和回归交付物：

| 阶段 | 名称 | 核心动作 |
|------|------|----------|
| 0 | 测试左移 | 可测试性评估，22 项检查点，低于 6 分先反馈需求方 |
| 1 | 需求获取 | 提取产品目标、功能、业务流程、非功能要求和约束 |
| 2 | 产品分析 | 功能树、测试边界、变更影响链路、相近度计算 |
| 3 | 交互确认 | 针对范围、环境、数据、回归策略提出反问 |
| 4 | 用例生成 | 标准用例、回归用例、环境分层、用户视角、Prod 门禁 |
| 5 | 自我审查 | 覆盖率、端到端串联、类型覆盖、数据完备性、遗漏风险 |
| 6 | 交付 | CSV/Markdown/Excel 测试用例、相近度报表、回归确认单 |

### 2. 测试报告生成

从测试执行记录生成统计、风险和上线建议：

| 步骤 | 名称 | 核心动作 |
|------|------|----------|
| 1 | 接收解析 | 读取 CSV/JSON/文本/Excel，识别列结构 |
| 2 | 数据清洗 | 状态标准化、缺失值检查、合理性校验 |
| 3 | 多维统计 | 整体、优先级、模块、类型、覆盖率、缺陷、效率 |
| 4 | 图表生成 | 有 matplotlib 时输出图表，无图表能力时降级文本 |
| 5 | 风险评估 | 10 条风险规则 + 上线就绪度评分 |
| 6 | 报告输出 | Dashboard、执行明细、缺陷分析、风险评估 |

## Key Models

### 相近度模型

```text
综合相近度 = 代码 x 0.30 + 数据 x 0.25 + API x 0.20 + 业务 x 0.15 + UI x 0.10
```

| 等级 | 分数 | 回归深度 | 覆盖建议 |
|------|------|----------|----------|
| 高相近 | >= 4.0 | 深度回归 | 100% |
| 中相近 | 2.0-3.9 | 重点回归 | >= 70% |
| 低相近 | 1.0-1.9 | 冒烟回归 | >= 50% |
| 微相近 | 0.1-0.9 | 极简回归 | 采样 |
| 无关 | 0.0 | 核心冒烟 | 关键路径 |

### 上线就绪度评分

```text
基础 100 分
- P0 未通过: -3/个
- 致命缺陷: -10/个
- 严重缺陷: -3/个
- 阻塞用例: -2/个
+ 回归全通过: +5
+ 灰度方案: +3
+ 回滚方案: +3

评级: A >= 90 | B >= 75 | C >= 60 | D < 60
```

## Supported Platforms

| 平台 | 适配器 | Excel | 图表 | 命令执行 | Skill 嵌套 |
|------|--------|-------|------|----------|------------|
| SOLO / WorkBuddy | ✅ | ✅ | ✅ | ✅ | ✅ |
| Claude Code | ✅ | ✅ | ✅ | ✅ | 内联 |
| Trae / Qoder | ✅ | ✅ | ✅ | ✅ | 内联 |
| Codex | ✅ | 降级 CSV | 降级文本 | 视环境而定 | 内联 |

## Installation

### Claude Code

```bash
mkdir -p .claude/skills/software-test-skill
cp -R SKILL.md core adapters scripts agents .claude/skills/software-test-skill/
```

### Codex

把本仓库作为 skill 目录安装，或复制 `SKILL.md`、`core/`、`scripts/` 到你的 Codex skills 目录。`agents/openai.yaml` 已包含展示名和默认提示。

### Trae / Qoder

参考 [adapters/trae-qoder/adapter-config.yaml](./adapters/trae-qoder/adapter-config.yaml) 中的导入方式和工具映射。

### SOLO / WorkBuddy

参考 [adapters/solo/adapter-config.yaml](./adapters/solo/adapter-config.yaml)。若环境需要 Excel 和图表，安装依赖：

```bash
pip install -r scripts/requirements.txt
```

## Repository Structure

```text
software-test-skill/
├── SKILL.md
├── agents/openai.yaml
├── core/
│   ├── prompts/
│   ├── workflows/
│   ├── frameworks/
│   ├── schemas/
│   ├── templates/
│   └── capability-contract.yaml
├── adapters/
├── examples/
├── scripts/
├── tests/
└── .github/workflows/ci.yml
```

## Roadmap

See [ROADMAP.md](./ROADMAP.md) for the full roadmap.

- 增加真实项目脱敏案例和输出截图。
- 增加完整 `.xlsx` 示例产物。
- 增加更多平台的安装脚本。
- 增加更严格的 JSON Schema 运行时校验。
- 增加缺陷趋势图和报告截图生成脚本。

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) and [CHANGELOG.md](./CHANGELOG.md).

欢迎提交 PR，尤其是：

- 新平台适配器。
- 更真实的 PRD / 执行记录示例。
- 测试设计规则补充。
- Excel 模板和图表模板优化。
- 脚本化生成能力增强。

## License

MIT License

Version: 2.4 | Author: [@winkooui](https://github.com/winkooui)
