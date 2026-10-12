# 机器人技能前向案例答复

八案独立处理，仅使用给定虚构证据。以下为实际用户答复与采用资源；未操作设备、联网或修改项目。

## 1. position-only-arm-ik

主流程选 IK 调试。位置任务对应 3×7 Jacobian 正确，无需添加朝向目标。同一目标、同一边界内已有 0.02 mm 可行解，因此 4.2 mm 停滞不能归因于该窗口内不可达。导数检查通过，首要嫌疑是无约束 DLS 后逐分量裁剪改变了下降方向，使活跃边界处反复受阻。

最小修正是保留现有位置残差与阻尼，把步长改成带边界的阻尼最小二乘：`min ||r + J dq||² + λ²||dq||²`，在求解内同时施加位置与本周期运动边界。窗口应始终基于契约规定的已接受状态，不能在内迭代中反复获得新运动额度；最终仍检查 FK 和约束。

验收复现原失败状态，确认修正后达到已知约 0.02 mm 可行解的残差量级，并满足应用既有容差；检查最终边界、有限性，以及边界附近连续目标的推进和关节连续性。局部失败仍不能作为全局不可行证明。实施前查方案历史；未提供记录不等于从未尝试。

资源：主技能 [dex-ik-design-debug](../../../skills/dex-ik-design-debug/SKILL.md)；参考 [execution-contract.md](../../../skills/dex-robotics-engineering/references/execution-contract.md)、[replay-validation.md](../../../skills/dex-robotics-engineering/references/replay-validation.md)。

## 2. retarget-final-window

不通过。最终输出中 11/240 个闭合样本，约 4.6%，使模型端点间距比基线增加 3–6 mm，超过允许的 0.8 mm。提案层通过和各关节限位通过，都不能替代最终几何要求。

下一步对齐这 11 个样本及前后连续片段，分别比较提案、拇指滤波后和限速后的端点间距、形状误差、滤波状态及活跃限速分量，确认误差首次出现的阶段，重点看快速接近。已有对比使用相同录制、原始时序、独立历史与相同重置状态，可保留该比较基础。

定位后再决定如何在最终运动窗口内保持间距要求，不能只提高优化权重。复验全部闭合样本，报告间距失败数、形状改善和新增滞后。结论仅涉及模型接近程度；没有实测接触，不能声称物理接触成功。

资源：主技能 [dex-retargeting-debug](../../../skills/dex-retargeting-debug/SKILL.md)；参考 [execution-contract.md](../../../skills/dex-robotics-engineering/references/execution-contract.md)、[replay-validation.md](../../../skills/dex-robotics-engineering/references/replay-validation.md)。

## 3. calibration-low-residual

当前不能替换。未训练屈曲试次已经出现错误的内部关节运动，未满足功能动作改善的条件。三组长度差异很大却得到近似残差，说明低传感器误差没有唯一确定长度、安装与关节分配。单轴激励不足是有力解释；安装角触边也提示参数补偿或边界影响，但尚不能排除链结构、坐标和先验问题。

同一次保持姿势的相邻两半高度相关，不能当成对新动作的独立验证。最有信息的下一步是冻结原模型与三个候选，在未参与拟合、能区分内部关节分配的独立多方向屈伸试次上成对比较，评价关节分配、功能范围、连续性及全部保护姿势。现有未训练屈曲试次应先纳入。若没有独立关节观测，只能评价功能表现，不能证明内部角度准确。

可用缩放后的参数敏感度/Jacobian 检查辨识弱方向；没有独立长度测量时，几何真实性仍不确定。保留原始输入和当前模型，候选单独存放；功能改善且保护姿势无退化后才重新评估替换。

资源：主技能 [dex-retargeting-debug](../../../skills/dex-retargeting-debug/SKILL.md)；参考 [calibration-observability.md](../../../skills/dex-retargeting-debug/references/calibration-observability.md)、[replay-validation.md](../../../skills/dex-robotics-engineering/references/replay-validation.md)。

## 4. failure-response-contract

该处理器违反契约，必须按故障类别拆分：

- 仅源中断且反馈新鲜、无 STOP 锁存：允许保留最后已准入目标，不能用尚未准入的有限提案代替。
- 反馈过期：执行设备规定的 stop-and-disable，不再重发位置目标。
- STOP 类驱动故障：锁存运动禁止，包括新 HOLD；后续有限数据包不能清除，只能显式恢复。
- 禁用状态不确定或清理超时：保留所有权和清理责任，直到确认达到契约允许的清理终态。

因此要删除统一的重发、有限包清错和超时释放逻辑。STOP 锁存优先于源中断回退，保留原始故障类型。用假驱动针对上述四条验证，尤其检查 STOP 后有限包不会产生 HOLD、清理超时不会丢失所有权；本次审查不涉及实机操作。

资源：主技能 [dex-robotics-engineering](../../../skills/dex-robotics-engineering/SKILL.md)；参考 [execution-contract.md](../../../skills/dex-robotics-engineering/references/execution-contract.md)。

## 5. asynchronous-time-and-age

新鲜度策略不符合契约，也不能保证一毫秒响应。10.050 s 接受 B:1 后，应重置已接受求解历史；10.080 s 完成的 A:80 属于旧 epoch，必须丢弃，不能更新 B 的状态或覆盖 latest-only 显示。

缓存重发必须保留源身份与原始 receipt，另记发布时间。A:80 完成时距其 receipt 已有 80 ms；这属于 receipt 到完成的年龄，不等于纯计算耗时。改写 receipt 会伪造新鲜度。

计算中位数 0.8 ms 不是实时保证，实测最大 15 ms 已否定每帧计算不超过 1 ms；有限样本最大值也不是未来上界。84 个模拟帧周期按 120 Hz 约为 0.7 s；若 84 帧含首尾则是 83 个间隔，准确值应取模拟时间戳。这是模拟动作时长。没有执行器反馈，无法推断物理响应时间。

最小验证是按给定顺序重放事件，确认旧 epoch 结果不能提交、重发时源年龄持续增长且显示始终选择当前最新有效结果。评估截止期还需逐帧超时数、尾部延迟和丢弃数。

资源：主技能 [dex-robotics-engineering](../../../skills/dex-robotics-engineering/SKILL.md)；参考 [execution-contract.md](../../../skills/dex-robotics-engineering/references/execution-contract.md)、[replay-validation.md](../../../skills/dex-robotics-engineering/references/replay-validation.md)。

## 6. software-only-evidence

按给定证据，软件接口验收通过。版本匹配的源码差异、配置和测试报告覆盖了六元素命令的顺序、单位、源身份，以及非有限值和错误维数拒绝，且载荷与拒绝结果均通过。假发布器足以支持这些接口结论，无需连接硬件作为额外前提。

结论仅覆盖对应版本、配置与测试边界，不证明物理跟踪、接触或实机响应。这些不在本次验收范围内，也无需引入额外团队审批流程。

资源：主技能 [dex-robotics-engineering](../../../skills/dex-robotics-engineering/SKILL.md)；参考 [replay-validation.md](../../../skills/dex-robotics-engineering/references/replay-validation.md)。

## 7. gain-and-force-evidence

现有证据不支持增益加倍，也不能把 `effort=0.6` 报成 0.6 N。假发布器没有执行器动态和测量反馈，只能验证命令生成，不能证明闭环稳定。

厂商归一化位置增益不能直接当作物理刚度；内环未知，翻倍后的响应无法推断。effort 是电流经占位 `Kt=1` 换算的字段，既未建立可信力矩标定，也没有接触力单位依据。应保留原始字段并标明换算未标定；力推断还需要真实电机常数、传动/摩擦、接触几何与负载校准。

下一步先核清可调增益的真实语义及 effort 的完整换算链。之后在合适动力学模型或有测量反馈的受限实验中，以当前增益建立跟踪、超调、振荡、延迟和饱和基线，再讨论参数扫描。当前离线评估不改增益、不操作设备。

资源：主技能 [impedance-gain-tuning](../../../skills/impedance-gain-tuning/SKILL.md)；参考 [replay-validation.md](../../../skills/dex-robotics-engineering/references/replay-validation.md)。

## 8. adjacent-ui-copy

不需要机器人领域技能。最小改动是把目标按钮对应的单条本地化字符串从 `Start` 改为 `Preview`。

检查差异只涉及该字符串及其引用范围；在对应语言页面确认新文案显示正确、无截断或布局挤压，按钮仍使用原点击处理函数和启用状态逻辑。无需设备、IK、重定向或增益测试。案例未提供可编辑文件，本次给出修改范围与验证方法，不声称已修改页面。

资源：未采用任何候选机器人领域技能或领域参考。
