# codex-skills

面向 Codex 的技能合集，涵盖软件工程、机器人遥操作、科研实验、数据可视化、文档制作与界面设计。

收录 32 项可复制安装的技能源码，并为 35 项外部技能保留官方安装入口。安装器支持批量或单项安装、文件完整性校验、冲突备份和失败恢复；来源、许可证与恢复方式记录在 `manifest.json` 中。

## 快速安装

要求：Bash 和 Python 3.8+，适用于 macOS、Linux 和 Windows 的 WSL 环境。安装过程可离线运行；技能所需的科学计算库、Herdr、Codex 工具或插件连接需另行配置。

克隆或下载本仓库，进入仓库目录后执行：

```bash
git clone https://github.com/C1TRuSovo831/codex-skills.git
cd codex-skills
bash install.sh
```

默认安装 `skills/` 下的 28 项普通技能到 `${CODEX_HOME:-$HOME/.codex}/skills`。若设置了 `CODEX_HOME`，脚本自动使用它；也可用 `--dest` 指定 skills 目录。安装后开始新对话，让 Codex 发现新文件。

```bash
# 查看全部技能及默认安装状态
bash install.sh --list

# 先检查文件并预览，不写目标目录
bash install.sh --dry-run

# 只安装一项，或选择多项
bash install.sh --skill experimental-design
bash install.sh --skill scientific-visualization --skill scientific-writing

# 指定目标 skills 目录
bash install.sh --dest /path/to/skills

# 冲突时先备份旧版本，再替换
bash install.sh --skill scientific-writing --force

# 可选：安装仓库内全部 32 项技能文件（含 4 项系统技能）
bash install.sh --all --dest /path/to/isolated-skills
```

`--all` 仅安装仓库内的技能源码，包括 `bundled/system/` 中的 4 项系统技能。它们需要兼容的 Codex 工具；与应用已提供的同名技能同时安装时可能出现重复，建议先使用隔离目录。

插件、模板及另外 2 项系统技能通过 Codex 官方入口安装，本仓库不复制其源码或资源。查看 [外部技能安装指引](external-skills.md)，或执行 `bash install.sh --recovery plugin-presentations`。对于外部条目，`--skill` 也只显示手动安装指引，不会联网或安装插件。

## 安装结果与失败恢复

- `[OK]`：逐文件 SHA-256 和可执行权限校验通过，已安装。
- `[SKIP]`：目标已有完全相同的内容和可执行权限。
- `[EXTERNAL]`：已显示官方安装入口，仍需在 Codex 中操作；不计为已安装。
- `[FAIL] 技能ID: 原因`：该项失败，其他技能继续；随后打印该项官方/公开上游命令、来源链接和本地单项重试命令。
- 默认不覆盖不同的文件或软链接；`--force` 会先把旧目录/软链接移动到目标父目录的 `.codex-skills-backups/`，再发布新副本。发布失败时尝试恢复旧版本，回滚失败会明确报告旧副本位置。
- 退出码：`0` 本次文件安装、预览或指引展示完成（外部插件仍需手动安装），`1` 至少一个技能失败，`2` 参数、清单、Python 或目标目录等初始化错误。

随时查询某项的恢复方式：

```bash
bash install.sh --recovery experimental-design
bash install.sh --recovery herdr-requirements-grill
bash install.sh --recovery plugin-presentations
```

例如 `experimental-design` 的公开上游安装命令：

```bash
npx skills add K-Dense-AI/scientific-agent-skills --skill experimental-design --agent codex --global
```

上游安装命令仅供手动执行，脚本不会自动联网安装。上游版本可能与仓库收录版本不同；需要使用仓库中的版本时，可通过 `--skill` 单项安装。仓库文件损坏时，请重新下载完整仓库；目标权限不足时，选择有写权限的 `--dest`。

自定义技能没有独立公开安装命令时，脚本提供本仓库的单项重试方式。外部插件提供 `codex plugin add 插件ID@目录`，需要目标 Codex 提供对应插件目录和账号权限；目录不可用时，请通过桌面应用的插件入口查看。系统能力没有独立安装命令时，会明确给出应用安装或更新入口。

## 包含哪些 skills

表格中的名称也是 `--skill` / `--recovery` 接受的 ID。源码条目链接到 `SKILL.md`；外部条目链接到官方安装指引。用途是简述，实际条件以对应技能或插件说明为准。

### 普通 skills：默认安装已启用项

| Skill ID | 用途 | 默认安装 |
|---|---|---|
| [brand](skills/brand/SKILL.md) | 品牌语气、视觉识别和品牌一致性 | 是 |
| [code-review](skills/code-review/SKILL.md) | 按代码规范与需求分别审查变更 | 是 |
| [codebase-design](skills/codebase-design/SKILL.md) | 模块边界、接口与深模块设计 | 是 |
| [design-system](skills/design-system/SKILL.md) | 设计令牌、组件规范与一致的视觉系统 | 是 |
| [dex-ik-design-debug](skills/dex-ik-design-debug/SKILL.md) | 遥操作 IK、雅可比、约束和轨迹连续性设计调试 | 是 |
| [dex-retargeting-debug](skills/dex-retargeting-debug/SKILL.md) | MANUS/Wuji 等灵巧手重定向、标定和捏合调试 | 是 |
| [dex-robotics-engineering](skills/dex-robotics-engineering/SKILL.md) | 为遥操作、重定向和阻抗问题选择工程工作流 | 是 |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | 通过证据与假设迭代定位故障和性能回退 | 是 |
| [domain-modeling](skills/domain-modeling/SKILL.md) | 梳理项目术语、领域模型与架构决策 | 是 |
| [experimental-design](skills/experimental-design/SKILL.md) | 实验对照、随机化、区组、重复测量和多因素设计 | 是 |
| [find-skills](skills/find-skills/SKILL.md) | 搜索、评估和发现可安装的 skills | 是 |
| [handoff](skills/handoff/SKILL.md) | 将当前任务整理成供下一位 agent 使用的交接文档 | 是 |
| [herdr](skills/herdr/SKILL.md) | 控制 Herdr 的终端、工作区和 agents；需要 Herdr 环境 | 是 |
| [herdr-requirements-grill](skills/herdr-requirements-grill/SKILL.md) | 在 Herdr Planner 角色下澄清高影响需求缺口 | 是 |
| [impedance-gain-tuning](skills/impedance-gain-tuning/SKILL.md) | 机器人 kp/kd、阻抗、振荡和阶跃响应调参 | 是 |
| [receiving-code-review](skills/receiving-code-review/SKILL.md) | 核实代码审查意见后再采取修改 | 是 |
| [research](skills/research/SKILL.md) | 依据可信一手来源调查问题并记录证据 | 是 |
| [scientific-visualization](skills/scientific-visualization/SKILL.md) | 科研数据绘图、误差表达、配色与导出检查 | 是 |
| [scientific-writing](skills/scientific-writing/SKILL.md) | 科研结果、论文段落、图注与证据一致性检查 | 是 |
| [setup-matt-pocock-skills](skills/setup-matt-pocock-skills/SKILL.md) | 配置工程 skills 所用的议题和文档约定 | 是 |
| [slides](skills/slides/SKILL.md) | 用 HTML 和 Chart.js 制作演示文稿 | 是 |
| [statistical-power](skills/statistical-power/SKILL.md) | 样本量、可检测差异和统计功效规划 | 是 |
| [tdd](skills/tdd/SKILL.md) | 按测试先行的方式实现功能与修复问题 | 是 |
| [teleop-hil-review](skills/teleop-hil-review/SKILL.md) | 在指定审查角色下核查遥操作 HIL 与安全证据 | 是 |
| [ui-styling](skills/ui-styling/SKILL.md) | 用 Tailwind/shadcn 等实现界面样式 | 是 |
| [ui-ux-pro-max](skills/ui-ux-pro-max/SKILL.md) | 检索 UI/UX 风格、配色、字体、图表与实现指南 | 是 |
| [verification-before-completion](skills/verification-before-completion/SKILL.md) | 在宣布完成前运行相关验证并检查结果 | 是 |
| [writing-for-agents](skills/writing-for-agents/SKILL.md) | 编写 agent 可执行的技能、规则与项目说明 | 是 |

### Codex 系统技能：4 项源码与 2 项官方入口

| Skill ID | 用途 |
|---|---|
| [system-imagegen](bundled/system/imagegen/SKILL.md) | 生成、编辑与变换栅格图像 |
| [system-openai-docs](bundled/system/openai-docs/SKILL.md) | 核实 OpenAI、Codex 与 API 的官方资料 |
| [system-plugin-creator](external-skills.md#system-plugin-creator) | 创建和打包 Codex 插件 |
| [system-review-agent](external-skills.md#system-review-agent) | 以缺陷为重点进行只读代码审查 |
| [system-skill-creator](bundled/system/skill-creator/SKILL.md) | 创建或修改 Codex skill |
| [system-skill-installer](bundled/system/skill-installer/SKILL.md) | 从官方列表或 GitHub 安装 skills |

### 插件附带技能和模板：通过 Codex 官方入口安装

| Skill ID | 用途 | 所属插件 |
|---|---|---|
| [plugin-documents](external-skills.md#plugin-documents) | 制作和编辑 Word 文档并检查渲染 | documents |
| [plugin-pdf](external-skills.md#plugin-pdf) | 读取、生成和检查 PDF | pdf |
| [plugin-excel-live-control](external-skills.md#plugin-excel-live-control) | 控制已连接的 Excel 实时会话 | spreadsheets |
| [plugin-spreadsheets](external-skills.md#plugin-spreadsheets) | 处理工作簿、公式、数据表和图表 | spreadsheets |
| [plugin-presentations](external-skills.md#plugin-presentations) | 制作、编辑和验证 PowerPoint/Google Slides 演示稿 | presentations |
| [plugin-template-creator](external-skills.md#plugin-template-creator) | 从参考成品建立可复用的个人模板 | template-creator |
| [plugin-sites-building](external-skills.md#plugin-sites-building) | 使用 Sites 创建网站和内部工具 | sites |
| [plugin-sites-hosting](external-skills.md#plugin-sites-hosting) | 使用 Sites 发布和管理网站托管 | sites |
| [plugin-computer-history](external-skills.md#plugin-computer-history) | 检索本机活动历史；依赖 Computer History 工具 | computer-history |
| [plugin-visualize](external-skills.md#plugin-visualize) | 在对话中制作交互可视化与解释工具 | visualize |
| [plugin-exa-search](external-skills.md#plugin-exa-search) | 使用 Exa 进行多轮网络检索与资料搜集 | Exa Search |
| [plugin-plugin-management](external-skills.md#plugin-plugin-management) | 发现插件并管理连接、依赖和权限 | plugin-management |
| [plugin-artifact-template-analytics-dashboard](external-skills.md#plugin-artifact-template-analytics-dashboard) | 获客、留存、营收等指标仪表盘表格模板 | openai-templates |
| [plugin-artifact-template-business-review](external-skills.md#plugin-artifact-template-business-review) | 业务复盘与决策汇报 PPT 模板 | openai-templates |
| [plugin-artifact-template-design-report](external-skills.md#plugin-artifact-template-design-report) | 设计报告 Word 模板 | openai-templates |
| [plugin-artifact-template-experiment-analysis](external-skills.md#plugin-artifact-template-experiment-analysis) | 假设、方法、结果及局限性的实验分析报告模板 | openai-templates |
| [plugin-artifact-template-financial-budget](external-skills.md#plugin-artifact-template-financial-budget) | 预算、情景预测和现金规划表格模板 | openai-templates |
| [plugin-artifact-template-investment-committee-memo](external-skills.md#plugin-artifact-template-investment-committee-memo) | 投资委员会备忘录模板 | openai-templates |
| [plugin-artifact-template-legal-memorandum](external-skills.md#plugin-artifact-template-legal-memorandum) | 法律问题分析备忘录模板 | openai-templates |
| [plugin-artifact-template-market-trends-report](external-skills.md#plugin-artifact-template-market-trends-report) | 市场与行业趋势 PPT 模板 | openai-templates |
| [plugin-artifact-template-minimal-letterhead](external-skills.md#plugin-artifact-template-minimal-letterhead) | 简洁信头与商务信函模板 | openai-templates |
| [plugin-artifact-template-operating-calendar](external-skills.md#plugin-artifact-template-operating-calendar) | 年度与月度运营日历表格模板 | openai-templates |
| [plugin-artifact-template-operating-review](external-skills.md#plugin-artifact-template-operating-review) | 周度运营复盘 PPT 模板 | openai-templates |
| [plugin-artifact-template-project-kickoff](external-skills.md#plugin-artifact-template-project-kickoff) | 项目启动和职责对齐 PPT 模板 | openai-templates |
| [plugin-artifact-template-project-tracker](external-skills.md#plugin-artifact-template-project-tracker) | 任务、负责人、日期与甘特图跟踪表格模板 | openai-templates |
| [plugin-artifact-template-sales-pipeline](external-skills.md#plugin-artifact-template-sales-pipeline) | 销售机会与预测表格模板 | openai-templates |
| [plugin-artifact-template-simple-dark-mode](external-skills.md#plugin-artifact-template-simple-dark-mode) | 简洁深色 PPT 模板 | openai-templates |
| [plugin-artifact-template-simple-light-mode](external-skills.md#plugin-artifact-template-simple-light-mode) | 简洁浅色 PPT 模板 | openai-templates |
| [plugin-artifact-template-strategy-memorandum](external-skills.md#plugin-artifact-template-strategy-memorandum) | 战略选择与建议备忘录模板 | openai-templates |
| [plugin-artifact-template-system-design](external-skills.md#plugin-artifact-template-system-design) | 架构、组件、数据流与取舍的系统设计文档模板 | openai-templates |
| [plugin-artifact-template-team-alignment](external-skills.md#plugin-artifact-template-team-alignment) | 团队目标、优先级与行动计划 PPT 模板 | openai-templates |
| [plugin-artifact-template-three-statement-forecast](external-skills.md#plugin-artifact-template-three-statement-forecast) | 三大财务报表联动预测模板 | openai-templates |
| [plugin-deep-research](external-skills.md#plugin-deep-research) | 进行深入研究并交付有来源的研究成果 | deep-research-work |

## 目录结构与依赖

```text
skills/                  默认安装的普通技能
bundled/system/          4 项携带开源许可证的系统技能
external-skills.md       插件、模板及其他系统技能的官方安装入口
manifest.json            来源、启用状态、单项恢复命令、SHA-256 与执行位
provenance/              上游许可证和逐项来源依据
THIRD_PARTY_NOTICES.md   许可归属与第三方声明
install.sh               安装入口
scripts/install.py       安装、校验、备份与逐项错误处理
readme.md                本说明
```

- 源码条目包含 `SKILL.md`、许可证，以及该技能使用的脚本、参考资料或 UI 元数据。外部条目仅包含名称、简述和官方入口。
- 安装器只安装技能文件。科研技能需要各自声明的 Python 依赖；Herdr 和机器人技能需要相应项目或环境；系统技能需要兼容的 Codex 版本和工具；插件通过 Codex 安装后使用。
- 账号授权、插件连接、Python 环境和运行时由使用者配置。安装器不修改 Codex 的 `config.toml`。
- 技能中的项目路径、工具名称和运行条件，应按实际工作环境核对。

添加或更新技能文件时，需同步更新 `manifest.json` 中的技能信息、文件校验值和可执行权限记录，否则安装器会报告内容不匹配。

## 来源与许可

仓库维护者编写的安装器、文档及自定义技能采用根目录的 [MIT 许可证](LICENSE)。第三方技能保留各自的 MIT、Apache-2.0 等许可证，每个可安装目录携带相应许可文件；根目录许可证不替代第三方条款。

逐项归属见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 和 `provenance/redistribution.json`，公开上游许可证的来源与校验值见 `provenance/license-index.json`。外部条目不包含技能指令、代码、模板或其他插件资源，也不授予对这些材料的复制权。

## 验证安装器

```bash
python3 -B -m unittest discover -s tests -v
```

测试在临时目录执行，覆盖完整安装、内容与权限、重复安装、失败继续、备份与回滚、含空格的路径、目录边界，以及外部入口查询和混合选择。测试不会执行技能代码或网络恢复命令；它验证的是安装器，不证明每个技能的专业建议或外部工具已可用。

安装机制参考：[OpenAI skills 文档](https://learn.chatgpt.com/docs/build-skills)、[OpenAI 插件文档](https://learn.chatgpt.com/docs/plugins)、[Skills CLI](https://github.com/vercel-labs/skills)。
