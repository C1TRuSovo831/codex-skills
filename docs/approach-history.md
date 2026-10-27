# 方案历史

已有 [2026-09-14 指令更新记录](../provenance/instruction-updates.json) 保留历史校验值。本文件补充后续方案与验证条件，不覆盖该记录；此前未记录的尝试未知。

## S01 — 通用机器人技能与既有验证的发布（2026-10-12）

- 原理：按实际失效阶段路由；任务维数、模型、坐标、控制接口和故障动作从当前合同确定。通过共享执行与连续回放参考、标定可辨识性诊断，去除品牌、固定关节数和特定工程链路假设。
- 适用条件：[skills/dex-robotics-engineering](../skills/dex-robotics-engineering/SKILL.md)、[IK](../skills/dex-ik-design-debug/SKILL.md)、[retargeting](../skills/dex-retargeting-debug/SKILL.md) 和 [impedance](../skills/impedance-gain-tuning/SKILL.md)。本次发布此前已验证的四项内容，保持调用名；其他技能不属本轮范围。
- 状态：技能通用化及一次离线行为评估已完成。本次复用既有结果并移植可审查证据；提交和推送状态以 Git 记录为准。
- 验收标准：发布的 19 个技能文件与受评候选 SHA-256 一致；资源链接可在仓库内解析；元数据与实际适用范围一致；八个虚构任务按预定 23 条标准评估。结构检查、分析行为和物理验证分别报告。
- 实际结果：候选文件 19/19 匹配；公开答复中的 18 个资源链接解析通过。已有独立 agent 在不含对话历史、不读取评分标准的条件下完成八案，随后逐案语义评分，8/8 案通过、23 条标准均检查通过。本次只归一化链接与候选路径、更新答复哈希，未重跑行为评估。单次分析样本不构成求解器性能测试、实机结果或未来行为的统计保证。
- 本仓库打包验证：34 项既有安装器测试通过；四项 dry-run 与隔离安装通过，安装后的 19 个文件内容/权限和 16 个相对引用均匹配。安装器测试不运行技能行为或设备。命令与结果摘要见 [本轮来源记录](../provenance/robotics-updates-2026-10-12.json)。
- 证据：[实际答复](validation/2026-10-12/forward-responses-001.md)、[评分](validation/2026-10-12/behavior-assessment-001.json)、[候选指纹](validation/2026-10-12/candidate-manifest-001.json)、[发布归一化与检查](validation/2026-10-12/publication-normalization.json)。[可复用案例、方法与评分入口](../skills/dex-robotics-engineering/tests/forward-evaluation.md)留在技能内。
- 重试条件：仅在新增模型或接口合同、实际误路由、行为回归或候选内容改变时追加证据；针对受影响案例复验并关联本条，不以同条件重复测试替代新证据。打包修复与必要链接检查不算算法路线重试。

## S02 — 三项科研技能的固定版本下载（2026-10-27）

- 原理：新增显式联网入口，调用 Codex 的 skill-installer 下载固定 commit；按文件白名单与 SHA-256 验证整批来源，复用现有 `scripts/install.py` 的发布、权限、冲突备份和回滚代码。
- 适用条件：仅 `ai-research-writing-skill`、`citation-management`、`peer-review`。不改变 28 项默认离线技能、4 项可选系统技能及 35 项外部入口。
- 既有证据及复用：S01 记录既有安装器的 34 项测试及隔离安装通过，本次复用其发布机制。2026-10-27 的实际安装已校验三个来源共 112 个上游文件，下载 commit 与 SHA-256 保存在 [锁定清单](../provenance/research-skills-lock.json)。未将缺少其他历史记录解释为未曾尝试。
- 状态：实现与文件安装验证完成；提交和推送状态以 Git 记录为准。
- 验收标准：固定完整 commit；根目录技能使用正确目录名且只选择所需资源；仅下载指定的两个 K-Dense 技能；哈希/名称异常阻止发布；已有目录默认保留；dry-run 无联网和写入；支持自定义目的目录；不执行下载技能、不安装依赖、不配置密钥。
- 实际结果：14 项新增离线测试、34 项既有安装器测试通过。使用当前 Codex 内置安装器实际下载并隔离安装 3 项技能，112 个上游文件及 3 份来源记录通过内容、权限和清单检查；当前已安装技能的 112 个上游文件保持不变。上游写作技能的 OpenAlex 密钥入 URL/记录问题保留并明确告知；功能脚本未运行。
- 下载边界修正：检查内置 Git 实现发现，其默认分支浅克隆可能无法取得未来的旧 commit；增加同 commit、同文件白名单的 HTTPS 回退。离线测试模拟该失败条件，真实 HTTPS 回退下载的 46 个 K-Dense 文件全部校验通过。未改用主分支或扩大安装范围。
- 证据位置：[下载锁定清单](../provenance/research-skills-lock.json)、[本轮验证记录](../provenance/research-downloads-2026-10-27.json)、[离线测试](../tests/test_download_research_skills.py)。
- 重试条件：上游 commit、文件清单、下载器行为或接口变化，或发现下载/校验/发布失败时追加验证；既有成功的安装机制继续复用。网络服务与技能科研功能未验证，不据此声明功能可用。
