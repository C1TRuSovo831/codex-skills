# 第三方许可与来源

安装器、仓库文档及维护者自定义技能使用根目录 [MIT 许可证](LICENSE)。以下第三方技能沿用对应文件的许可与版权声明。安装时会复制技能目录内的许可文件。

仓库保存收录版本，不承诺与当前上游完全相同。`manifest.json` 中的 `upstream` 字段保留已核实的固定公开来源；早期差异可能来自上游版本或既有定制，不能全部归为维护者修改。

2026-09-14，维护者同步了 27 项技能的指令优化：缩短触发描述、按场景拆分参考说明、明确完成与验证边界，并调整技能默认任务提示词。Herdr 和 ui-styling 的改动文件另附 Apache-2.0 要求的修改声明；UI 搜索示例按实际技能安装目录解析路径。原许可证、版权声明、脚本、数据与安装选择保持不变。逐项修改前后校验值及历史上游比较记录见 [provenance/instruction-updates.json](provenance/instruction-updates.json)；历史相似度不代表优化后文本与上游的相似度。

| Skill ID | 许可 | 随技能提供的许可文件 |
|---|---|---|
| brand | MIT | [许可文件](skills/brand/LICENSE) |
| code-review | MIT | [许可文件](skills/code-review/LICENSE) |
| codebase-design | MIT | [许可文件](skills/codebase-design/LICENSE) |
| design-system | MIT | [许可文件](skills/design-system/LICENSE) |
| dex-ik-design-debug | MIT | [许可文件](skills/dex-ik-design-debug/LICENSE) |
| dex-retargeting-debug | MIT | [许可文件](skills/dex-retargeting-debug/LICENSE) |
| dex-robotics-engineering | MIT | [许可文件](skills/dex-robotics-engineering/LICENSE) |
| diagnosing-bugs | MIT | [许可文件](skills/diagnosing-bugs/LICENSE) |
| domain-modeling | MIT | [许可文件](skills/domain-modeling/LICENSE) |
| experimental-design | MIT | [许可文件](skills/experimental-design/LICENSE) |
| find-skills | MIT | [许可文件](skills/find-skills/LICENSE) |
| handoff | MIT | [许可文件](skills/handoff/LICENSE) |
| herdr | Apache-2.0 | [许可文件](skills/herdr/LICENSE) |
| herdr-requirements-grill | MIT | [许可文件](skills/herdr-requirements-grill/LICENSE) |
| impedance-gain-tuning | MIT | [许可文件](skills/impedance-gain-tuning/LICENSE) |
| receiving-code-review | MIT | [许可文件](skills/receiving-code-review/LICENSE) |
| research | MIT | [许可文件](skills/research/LICENSE) |
| scientific-visualization | MIT | [许可文件](skills/scientific-visualization/LICENSE) |
| scientific-writing | MIT | [许可文件](skills/scientific-writing/LICENSE) |
| setup-matt-pocock-skills | MIT | [许可文件](skills/setup-matt-pocock-skills/LICENSE) |
| slides | MIT | [许可文件](skills/slides/LICENSE) |
| statistical-power | MIT | [许可文件](skills/statistical-power/LICENSE) |
| tdd | MIT | [许可文件](skills/tdd/LICENSE) |
| teleop-hil-review | MIT | [许可文件](skills/teleop-hil-review/LICENSE) |
| ui-styling | Apache-2.0 | [许可文件](skills/ui-styling/LICENSE.txt)；[上游 MIT 声明](skills/ui-styling/UPSTREAM-LICENSE-MIT.txt) |
| ui-ux-pro-max | MIT | [许可文件](skills/ui-ux-pro-max/LICENSE) |
| verification-before-completion | MIT | [许可文件](skills/verification-before-completion/LICENSE) |
| writing-for-agents | MIT | [许可文件](skills/writing-for-agents/LICENSE) |
| system-imagegen | Apache-2.0 | [许可文件](bundled/system/imagegen/LICENSE.txt) |
| system-openai-docs | Apache-2.0 | [许可文件](bundled/system/openai-docs/LICENSE.txt) |
| system-skill-creator | Apache-2.0 | [许可文件](bundled/system/skill-creator/license.txt) |
| system-skill-installer | Apache-2.0 | [许可文件](bundled/system/skill-installer/LICENSE.txt) |

`ui-styling` 的目录许可证为 Apache-2.0，上游元数据和仓库另有 MIT 声明；两者均保留，未用根目录 MIT 替换该技能的具体许可证。

逐项许可依据见 [provenance/redistribution.json](provenance/redistribution.json)，公开上游许可原件与固定来源见 [provenance/license-index.json](provenance/license-index.json)。

插件及未确认本机副本许可的系统技能不提供源码；[外部技能安装指引](external-skills.md)仅用于从官方入口安装，不构成对外部材料的再许可。
