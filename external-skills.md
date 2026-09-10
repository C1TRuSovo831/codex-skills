# 外部技能安装指引

本页只记录技能名称、所属插件与官方安装入口，不包含技能源码、模板或运行时。

在 Codex 桌面应用的插件目录中查找相应插件；CLI 可输入 `/plugins` 浏览已配置的目录。安装、完成所需连接后，开始新会话。入口说明见 [官方插件文档](https://learn.chatgpt.com/zh-Hans/docs/plugins)。

以下 `codex plugin add` 命令使用 Codex CLI 支持的 `PLUGIN@MARKETPLACE` 语法，供手动执行。目录、账号权限和应用版本决定具体插件是否可用；目录不可用时，请使用桌面应用提供的插件入口，不能假设每台电脑都能运行所有命令。

安装器的 `--skill` 和 `--recovery` 对这些条目均只展示指引，不运行命令，也不代表插件已安装。

## system-plugin-creator

创建和打包 Codex 插件。

优先使用 Codex 随附的 plugin-creator。此命令安装已核实的公开上游版本，不恢复本机差异版；本仓库不包含该系统技能源码。

[官方入口](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/plugin-creator/SKILL.md)

```bash
npx skills add https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/plugin-creator --skill plugin-creator --agent codex --global
```

## system-review-agent

以缺陷为重点进行只读代码审查。

此系统能力由兼容的 Codex 应用提供；请通过官方入口安装或更新 Codex。未核实独立技能安装命令，也不能保证每个版本都提供同名技能。

[官方入口](https://developers.openai.com/codex/app/)

## documents@openai-primary-runtime

```bash
codex plugin add documents@openai-primary-runtime
```

- <a id="plugin-documents"></a> **plugin-documents**（documents）：制作和编辑 Word 文档并检查渲染。

[官方安装入口与操作说明](https://learn.chatgpt.com/zh-Hans/docs/plugins)

## pdf@openai-primary-runtime

```bash
codex plugin add pdf@openai-primary-runtime
```

- <a id="plugin-pdf"></a> **plugin-pdf**（pdf）：读取、生成和检查 PDF。

[官方安装入口与操作说明](https://learn.chatgpt.com/zh-Hans/docs/plugins)

## spreadsheets@openai-primary-runtime

```bash
codex plugin add spreadsheets@openai-primary-runtime
```

- <a id="plugin-excel-live-control"></a> **plugin-excel-live-control**（excel-live-control）：控制已连接的 Excel 实时会话。
- <a id="plugin-spreadsheets"></a> **plugin-spreadsheets**（Spreadsheets）：处理工作簿、公式、数据表和图表。

[官方安装入口与操作说明](https://learn.chatgpt.com/zh-Hans/docs/plugins)

## presentations@openai-primary-runtime

```bash
codex plugin add presentations@openai-primary-runtime
```

- <a id="plugin-presentations"></a> **plugin-presentations**（Presentations）：制作、编辑和验证 PowerPoint/Google Slides 演示稿。

[官方安装入口与操作说明](https://learn.chatgpt.com/zh-Hans/docs/plugins)

## template-creator@openai-primary-runtime

```bash
codex plugin add template-creator@openai-primary-runtime
```

- <a id="plugin-template-creator"></a> **plugin-template-creator**（template-creator）：从参考成品建立可复用的个人模板。

[官方安装入口与操作说明](https://learn.chatgpt.com/zh-Hans/docs/plugins)

## sites@openai-bundled

```bash
codex plugin add sites@openai-bundled
```

- <a id="plugin-sites-building"></a> **plugin-sites-building**（sites-building）：使用 Sites 创建网站和内部工具。
- <a id="plugin-sites-hosting"></a> **plugin-sites-hosting**（sites-hosting）：使用 Sites 发布和管理网站托管。

[官方安装入口与操作说明](https://learn.chatgpt.com/zh-Hans/docs/plugins)

## computer-history@openai-bundled

```bash
codex plugin add computer-history@openai-bundled
```

- <a id="plugin-computer-history"></a> **plugin-computer-history**（computer-history）：检索本机活动历史；依赖 Computer History 工具。

[官方安装入口与操作说明](https://learn.chatgpt.com/zh-Hans/docs/plugins)

## visualize@openai-bundled

```bash
codex plugin add visualize@openai-bundled
```

- <a id="plugin-visualize"></a> **plugin-visualize**（visualize）：在对话中制作交互可视化与解释工具。

[官方安装入口与操作说明](https://learn.chatgpt.com/zh-Hans/docs/plugins)

## app-69ea4ed2cf7c8191b742ef3622479ddd@openai-curated-remote

```bash
codex plugin add app-69ea4ed2cf7c8191b742ef3622479ddd@openai-curated-remote
```

- <a id="plugin-exa-search"></a> **plugin-exa-search**（Search）：使用 Exa 进行多轮网络检索与资料搜集。

[官方安装入口与操作说明](https://learn.chatgpt.com/zh-Hans/docs/plugins)

## plugin-management@openai-curated-remote

```bash
codex plugin add plugin-management@openai-curated-remote
```

- <a id="plugin-plugin-management"></a> **plugin-plugin-management**（plugin-management）：发现插件并管理连接、依赖和权限。

[官方安装入口与操作说明](https://learn.chatgpt.com/zh-Hans/docs/plugins)

## openai-templates@openai-curated-remote

```bash
codex plugin add openai-templates@openai-curated-remote
```

- <a id="plugin-artifact-template-analytics-dashboard"></a> **plugin-artifact-template-analytics-dashboard**（artifact-template-analytics-dashboard）：获客、留存、营收等指标仪表盘表格模板。
- <a id="plugin-artifact-template-business-review"></a> **plugin-artifact-template-business-review**（artifact-template-business-review）：业务复盘与决策汇报 PPT 模板。
- <a id="plugin-artifact-template-design-report"></a> **plugin-artifact-template-design-report**（artifact-template-design-report）：设计报告 Word 模板。
- <a id="plugin-artifact-template-experiment-analysis"></a> **plugin-artifact-template-experiment-analysis**（artifact-template-experiment-analysis）：假设、方法、结果及局限性的实验分析报告模板。
- <a id="plugin-artifact-template-financial-budget"></a> **plugin-artifact-template-financial-budget**（artifact-template-financial-budget）：预算、情景预测和现金规划表格模板。
- <a id="plugin-artifact-template-investment-committee-memo"></a> **plugin-artifact-template-investment-committee-memo**（artifact-template-investment-committee-memo）：投资委员会备忘录模板。
- <a id="plugin-artifact-template-legal-memorandum"></a> **plugin-artifact-template-legal-memorandum**（artifact-template-legal-memorandum）：法律问题分析备忘录模板。
- <a id="plugin-artifact-template-market-trends-report"></a> **plugin-artifact-template-market-trends-report**（artifact-template-market-trends-report）：市场与行业趋势 PPT 模板。
- <a id="plugin-artifact-template-minimal-letterhead"></a> **plugin-artifact-template-minimal-letterhead**（artifact-template-minimal-letterhead）：简洁信头与商务信函模板。
- <a id="plugin-artifact-template-operating-calendar"></a> **plugin-artifact-template-operating-calendar**（artifact-template-operating-calendar）：年度与月度运营日历表格模板。
- <a id="plugin-artifact-template-operating-review"></a> **plugin-artifact-template-operating-review**（artifact-template-operating-review）：周度运营复盘 PPT 模板。
- <a id="plugin-artifact-template-project-kickoff"></a> **plugin-artifact-template-project-kickoff**（artifact-template-project-kickoff）：项目启动和职责对齐 PPT 模板。
- <a id="plugin-artifact-template-project-tracker"></a> **plugin-artifact-template-project-tracker**（artifact-template-project-tracker）：任务、负责人、日期与甘特图跟踪表格模板。
- <a id="plugin-artifact-template-sales-pipeline"></a> **plugin-artifact-template-sales-pipeline**（artifact-template-sales-pipeline）：销售机会与预测表格模板。
- <a id="plugin-artifact-template-simple-dark-mode"></a> **plugin-artifact-template-simple-dark-mode**（artifact-template-simple-dark-mode）：简洁深色 PPT 模板。
- <a id="plugin-artifact-template-simple-light-mode"></a> **plugin-artifact-template-simple-light-mode**（artifact-template-simple-light-mode）：简洁浅色 PPT 模板。
- <a id="plugin-artifact-template-strategy-memorandum"></a> **plugin-artifact-template-strategy-memorandum**（artifact-template-strategy-memorandum）：战略选择与建议备忘录模板。
- <a id="plugin-artifact-template-system-design"></a> **plugin-artifact-template-system-design**（artifact-template-system-design）：架构、组件、数据流与取舍的系统设计文档模板。
- <a id="plugin-artifact-template-team-alignment"></a> **plugin-artifact-template-team-alignment**（artifact-template-team-alignment）：团队目标、优先级与行动计划 PPT 模板。
- <a id="plugin-artifact-template-three-statement-forecast"></a> **plugin-artifact-template-three-statement-forecast**（artifact-template-three-statement-forecast）：三大财务报表联动预测模板。

[官方安装入口与操作说明](https://learn.chatgpt.com/zh-Hans/docs/plugins)

## deep-research-work@openai-curated-remote

```bash
codex plugin add deep-research-work@openai-curated-remote
```

- <a id="plugin-deep-research"></a> **plugin-deep-research**（deep-research）：进行深入研究并交付有来源的研究成果。

[官方安装入口与操作说明](https://learn.chatgpt.com/zh-Hans/docs/plugins)
