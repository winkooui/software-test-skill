# 工具名称映射表
# Tool Name Mapping Reference
# 版本: v1.0
# 各平台适配器使用此表进行工具名称转换

---

## 通用能力 → 各平台工具名

| 通用能力 | SOLO | Claude Code | Trae / Qoder | Codex |
|---------|------|-------------|-------------|-------|
| 读取文件 | `Read` | `Read` | 文件读取 | 文件读取 |
| 写入文件 | `Write` | `Write` | 文件写入 | 文件写入 |
| 编辑文件 | `SearchReplace` | `Write` | 文件编辑 | — |
| 列出目录 | `LS` / `Glob` | `LS` / `Glob` | 目录浏览 | 目录浏览 |
| 执行命令(阻塞) | `RunCommand` (blocking=true) | `Bash` | 终端执行 | — |
| 执行命令(非阻塞) | `RunCommand` (blocking=false) | `Bash` (后台) | 终端执行(后台) | — |
| 检查命令状态 | `CheckCommandStatus` | `Bash` (ps) | 进程检查 | — |
| 搜索网页 | `WebSearch` | `WebSearch` | 网络搜索 | 搜索 |
| 获取网页 | `WebFetch` | `WebFetch` | 网页获取 | 网页获取 |
| 用户交互 | `AskUserQuestion` | 自然语言 | 对话交互 | 对话 |
| 代码搜索 | `Grep` / `SearchCodebase` | `Grep` | 代码搜索 | 代码搜索 |
| 任务跟踪 | `TodoWrite` | Markdown 列表 | Markdown 列表 | Markdown 列表 |
| 子Skill调用 | `Skill` | 内联引用 | 内联引用 | — |
| 生成Excel | Python openpyxl | Python openpyxl | Python openpyxl | — (降级CSV) |
| 生成图表 | matplotlib + openpyxl | matplotlib + openpyxl | matplotlib + openpyxl | — (降级ASCII) |

---

## 路径变量映射

| 通用变量 | SOLO | Claude Code | Trae / Qoder | Codex |
|---------|------|-------------|-------------|-------|
| `{PROJECT_ROOT}` | `/sessions/{id}/workspace` | `{cwd}` | `{project_root}` | `{upload_dir}` |
| `{WORKSPACE_DIR}` | `/sessions/{id}/workspace` | `{cwd}/test-output` | `{project_root}/test-output` | `{upload_dir}` |
| `{TEMP_DIR}` | `/sessions/{id}/work` | `{cwd}/.temp` | `{project_root}/.temp` | `/tmp` |
| `{SESSION_ID}` | 环境推断 | `N/A` | `N/A` | `N/A` |

---

## 用户交互降级策略

| 平台 | 有无专用工具 | 交互方式 |
|------|------------|---------|
| SOLO | ✅ AskUserQuestion | 多选UI，每次最多4个问题 |
| Claude Code | ❌ | 自然语言提问，用户文本回复，一次性所有问题 |
| Trae / Qoder | ❌ | 对话交互，分段提问 |
| Codex | ❌ | 对话交互 |

### 通用格式（无专用工具时）
```
请逐一回复以下问题（格式：1-A, 2-是, 3-补充内容）：

1. 本次测试涉及哪些环境？
   A. 沙箱+SIT+UAT  B. 全部(含生产)  C. 仅沙箱和SIT

2. 是否需要覆盖性能测试？
   ...
```

---

## 能力检测命令

| 检测项 | 命令 | 成功输出 |
|--------|------|---------|
| Python 可用 | `python3 --version` | Python 3.x.x |
| openpyxl 可用 | `python3 -c "import openpyxl; print('OK')"` | OK |
| matplotlib 可用 | `python3 -c "import matplotlib; print('OK')"` | OK |
| pandas 可用 | `python3 -c "import pandas; print('OK')"` | OK |
| 全部就绪 | `python3 -c "import openpyxl, matplotlib, pandas; print('ALL OK')"` | ALL OK |

---

## 平台检测方法

| 平台 | 检测特征 |
|------|---------|
| SOLO | `AskUserQuestion` 和 `TodoWrite` 工具可用；路径含 `/sessions/` |
| Claude Code | `.claude/skills/` 目录存在；`CLAUDE_CODE_VERSION` 环境变量 |
| Trae | `TRAE_VERSION` 环境变量；Skills 面板 UI |
| Qoder | `QODER_VERSION` 环境变量；Skills 面板 UI |
| Codex | 不支持 Bash；仅能访问上传文件；`OPENAI_API_KEY` 环境变量 |

---

*版本: v1.0 | 最后更新: 2026-05-25*
