# codex-skills

面向 Codex 的技能合集，涵盖软件工程、科研写作、机器人遥操作和界面设计。可以按任务选择技能，也可以批量安装。

[开始使用](#开始使用) · [技能目录](#技能目录) · [使用提示](#使用提示) · [维护与许可](#维护与许可)

## 开始使用

需要 Bash 和 Python 3.8+，支持 macOS、Linux 和 Windows WSL。

```bash
git clone https://github.com/C1TRuSovo831/codex-skills.git
cd codex-skills
```

根据下方技能目录选择安装入口：

| 命令 | 安装范围 |
|---|---|
| `bash install.sh` | 安装仓库内的常用技能，可离线运行 |
| `bash download-research-skills.sh` | 安装目录中标为「下载」的技能，需要联网 |

不带参数时，各入口安装自己支持的全部常用技能。默认目录是 `~/.codex/skills`；设置了 `CODEX_HOME` 时使用 `$CODEX_HOME/skills`。安装后开启新的 Codex 对话，可用 `$技能名` 显式调用。

两个入口都支持以下选项：

| 选项 | 用途 |
|---|---|
| `--list` | 查看该入口支持的技能 |
| `--skill 名称` | 只安装指定技能，可重复使用 |
| `--dry-run` | 预览安装，不联网、不写入文件 |
| `--dest 路径` | 指定安装目录 |
| `--force` | 备份已有的不同版本后替换 |

例如，选择安装或先预览：

```bash
bash install.sh --skill scientific-writing --skill scientific-visualization
bash download-research-skills.sh --skill citation-management
bash install.sh --dry-run
```

安装只复制技能文件，不运行技能附带的脚本，也不会安装运行依赖、配置密钥或上传资料。

## 技能目录

以下四类技能按用途排列，点击名称查看使用说明。未标注的技能通过 `install.sh` 安装；标为「下载」的技能通过 `download-research-skills.sh` 安装。名称也可直接用作对应入口的 `--skill` 参数。

### 软件工程与协作

| Skill | 用途 |
|---|---|
| [codebase-design](skills/codebase-design/SKILL.md) | 设计模块边界与接口 |
| [domain-modeling](skills/domain-modeling/SKILL.md) | 梳理项目术语、领域模型与架构决策 |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | 用证据定位故障和性能回退 |
| [tdd](skills/tdd/SKILL.md) | 通过测试先行实现功能与修复问题 |
| [code-review](skills/code-review/SKILL.md) | 按代码规范与需求审查变更 |
| [receiving-code-review](skills/receiving-code-review/SKILL.md) | 核实审查意见并落实修改 |
| [verification-before-completion](skills/verification-before-completion/SKILL.md) | 在宣布完成前检查验证结果 |
| [handoff](skills/handoff/SKILL.md) | 为下一位 agent 整理任务交接文档 |
| [writing-for-agents](skills/writing-for-agents/SKILL.md) | 编写技能、协作规则和项目说明 |
| [setup-matt-pocock-skills](skills/setup-matt-pocock-skills/SKILL.md) | 配置工程技能使用的议题和文档约定 |
| [find-skills](skills/find-skills/SKILL.md) | 搜索和评估可安装的技能 |

### 科研与论文

| Skill | 用途 |
|---|---|
| [research](skills/research/SKILL.md) | 依据可信的一手来源调查问题并记录证据 |
| [experimental-design](skills/experimental-design/SKILL.md) | 规划实验对照、随机化、区组和重复测量 |
| [statistical-power](skills/statistical-power/SKILL.md) | 规划样本量、可检测差异和统计功效 |
| [scientific-visualization](skills/scientific-visualization/SKILL.md) | 绘制科研图表，检查误差表达、配色与导出 |
| [scientific-writing](skills/scientific-writing/SKILL.md) | 撰写和修订科研文本，核查论述与证据的一致性 |
| [ai-research-writing-skill](https://github.com/jin-s13/ai-research-writing-skill)（下载） | 从项目材料组织 AI/ML 论文，支持写作、修订和投稿准备 |
| [citation-management](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/citation-management)（下载） | 检索文献、核实引用信息并生成 BibTeX |
| [peer-review](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/peer-review)（下载） | 检查研究方法、证据与可复现性，起草审稿意见 |

### 机器人与遥操作

| Skill | 用途 |
|---|---|
| [dex-robotics-engineering](skills/dex-robotics-engineering/SKILL.md) | 沿感知、标定、重定向、IK、控制与执行定位故障层 |
| [dex-ik-design-debug](skills/dex-ik-design-debug/SKILL.md) | 分析正运动学、雅可比、约束求解与解连续性 |
| [dex-retargeting-debug](skills/dex-retargeting-debug/SKILL.md) | 诊断运动重定向、坐标约定、形态差异与标定 |
| [impedance-gain-tuning](skills/impedance-gain-tuning/SKILL.md) | 诊断 PD/PID 和阻抗控制响应，调整增益 |
| [teleop-hil-review](skills/teleop-hil-review/SKILL.md) | 在指定审查角色下核查遥操作 HIL 与安全证据 |
| [herdr](skills/herdr/SKILL.md) | 在 Herdr 环境中控制终端、工作区和 agents |
| [herdr-requirements-grill](skills/herdr-requirements-grill/SKILL.md) | 为 Herdr Planner 澄清关键需求与验收条件 |

### 设计与展示

| Skill | 用途 |
|---|---|
| [brand](skills/brand/SKILL.md) | 定义品牌语气与视觉识别，检查品牌一致性 |
| [design-system](skills/design-system/SKILL.md) | 建立设计令牌、组件规范与视觉系统 |
| [ui-styling](skills/ui-styling/SKILL.md) | 用 Tailwind、shadcn 等实现界面样式 |
| [ui-ux-pro-max](skills/ui-ux-pro-max/SKILL.md) | 检索 UI/UX 风格、配色、字体与实现指南 |
| [slides](skills/slides/SKILL.md) | 用 HTML 和 Chart.js 制作演示文稿 |

### 系统技能与插件

系统技能通常由 Codex 提供。仓库另保留了 [imagegen](bundled/system/imagegen/SKILL.md)、[openai-docs](bundled/system/openai-docs/SKILL.md)、[skill-creator](bundled/system/skill-creator/SKILL.md) 和 [skill-installer](bundled/system/skill-installer/SKILL.md) 的副本，使用 `bash install.sh --all` 可一并安装；建议先指定隔离目录，避免与应用自带版本重复。

Word、PDF、表格、PowerPoint、Sites、交互可视化、Exa 搜索及各类文档模板通过 Codex 插件入口安装。完整列表和安装方式见 [外部技能安装指引](external-skills.md)。

## 使用提示

### 更新与安装冲突

重新运行安装命令会跳过内容相同的技能。遇到不同版本时默认保留原目录；确认替换后加 `--force`，旧副本会保存到安装目录旁的 `.codex-skills-backups/`。

```bash
bash install.sh --skill scientific-writing --force
```

安装失败时先查看终端中的具体原因。仓库文件不完整可重新下载仓库；目标目录不可写可用 `--dest` 换一个目录。仓库内技能及外部插件的恢复指引可按名称查询：

```bash
bash install.sh --recovery experimental-design
bash install.sh --recovery plugin-presentations
```

外部插件显示安装指引后，仍需在 Codex 中完成安装。

### 运行环境

文件安装成功不代表相关功能已经运行验证。具体依赖以各技能说明为准：论文编译需要 LaTeX 工具链，文献检索可能需要 `requests`、`scholarly` 和网络连接，部分审稿脚本需要 Python 3.11+；Herdr、机器人和插件技能需要相应工具与环境。

当前下载的写作技能有一项已知问题：OpenAlex API key 可能随查询 URL 写入引用记录或错误信息。使用带密钥的查询前应先修复，详见[检查记录](provenance/research-downloads-2026-10-27.json)。

### 机器人技能的配套安装

机器人领域技能引用 `dex-robotics-engineering` 中的共享文档，建议一起安装到同一目录：

```bash
bash install.sh \
  --skill dex-robotics-engineering \
  --skill dex-ik-design-debug \
  --skill dex-retargeting-debug \
  --skill impedance-gain-tuning
```

故障层不明确时使用 `dex-robotics-engineering`；已经明确时直接使用对应领域技能。

## 维护与许可

- [AGENTS.md](AGENTS.md)：仓库协作约定；[任务模板](prompts/task-templates.md)：常用任务的提示词。
- [安装清单](manifest.json)与[下载清单](provenance/research-skills-lock.json)：技能来源和安装所需的文件记录。更新技能时需同步维护。
- [方案历史](docs/approach-history.md)与[来源记录](provenance/)：维护决策、变更依据和验证结果。
- [MIT 许可证](LICENSE)与[第三方声明](THIRD_PARTY_NOTICES.md)：仓库自有内容和第三方技能分别遵循各自许可证。

修改安装器后运行：

```bash
python3 -B -m unittest discover -s tests -v
```

测试覆盖文件安装、冲突处理、备份与恢复，不执行技能代码。下载器测试使用模拟网络，产生的测试资料带有 `REMOVABLE.txt` 标记，保留待确认后清理。
