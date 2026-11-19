## title
Picard 与 Newton · 地下水迭代实验室

## page_title
Picard 与 Newton 实验室

## s1
01 · 从水量平衡到迭代

## s2
02 · 理想化三单元模型

## s3
03 · 十一个单元：更复杂的系统

## preset
建议预设

## locked_preset_help
Mehl（2006）案例采用原文的含水层和蒸散发设置。若要启用一般模型设置中的这些开关，请在建议预设中选择三个可编辑的承压或潜水案例之一。

## et_preset
潜水 · 含蒸散发

## left
左侧给定水头（m）

## right
右侧给定水头（m）

## kl
K，左单元（m/s）

## kc
K，中央单元（m/s）

## kr
K，右单元（m/s）

## initial
中央初始水头（m）

## unconfined
潜水含水层

## et_enable
启用中央单元的蒸散发

## et_surface
ET 表面高程（m）

## et_depth
ET 极限深度（m）

## et_max
最大 ET 速率（mm/year）

## recharge
均匀补给（mm/year）

## omega
阻尼系数 ω

## omega_help
1 = 完整步长。较小的值减小建议修正，但不保证收敛。

## reset
重置

## reset_notice
模型设置已改变：迭代历史已重新开始。

## ready
初始估计

## running
迭代中

## converged
已收敛

## singular
线性系统奇异；请重置或改变初始水头

## dry
步骤被拒绝：水头位于含水层底板或以下

## cycle
检测到两步循环；请重置或改变初始水头

## limit
已达到迭代次数上限

## diverged
建议水头不是有限值或过大

## status
{method}：{status} · 已接受步数：{steps}

## reference
参考水头 · 解析解比较

## no_reference
尚未独立验证这些设置存在非干涸解。请检查参数。

## maps
点击查看蛛网图的补充说明

## scalar_caption
在横轴上读取当前水头。细橙色点线连接输入与迭代构造；橙色实线段显示 Picard 蛛网路径或 Newton 切线。Picard 把每个已接受更新转移至对角线。当前 Picard 水头处的实线竖段从上方或下方到达函数值，表示当前评价，不接受额外更新。Newton 沿残差切线到达零点。未启用缩放时坐标轴固定；缩放仅改变视图。

## coupled_caption
十一单元 Picard 面板在本步完整系统的水头函数上显示最近接受的构造。该函数随其他水头变化；历史图保留所有已接受水头。此模型的 Newton 约化流量残差固定，可显示所有已接受切线。

## residuals
收敛：水头变化与流量残差

## residual_caption
绿色 = Picard；蓝色 = Newton。方块 = 流量残差（右侧紫色轴及阈值）；圆点 = 水头变化（左侧赭色轴及阈值）。两对数轴固定在 1E-12–100。必须同时满足 max|Δh| < {head_tol:.0e} m 和 max|F| < {flow_tol:.0e} m³/s。k = 0 时无水头变化值。边缘三角形标示低于窗口的值（▼，包括零）或高于窗口的值（▲）。窗口外的阈值仍适用。这些指标不是相对参考水头的误差。

## head_history
单元 {cell} 的水头历史

## head_history_caption
每次接受更新后的实际水头；k = 0 为初始估计。独立参考水头仅用于视觉比较，不作为迭代停止标准。k 计数的是已接受更新，不是时间步。

## off
无 ET

## linear
ET 线性区间

## maximum
最大 ET

## gradient
增大梯度 · 右水头降至 0.5 m

## heterogeneous
加入三个渗透系数分区

## zone1
区域 1 · 单元 1–5 · K（m/s）

## zone2
区域 2 · 单元 6 · K（m/s）

## zone3
区域 3 · 单元 7–11 · K（m/s）

## cell
选择研究单元（内部单元 2–10）

## initial_mode
初始水头分布

## initial_linear
边界间线性分布

## initial_uniform
内部水头均一

## uniform_value
均一内部初始水头（m）

## assess
检查理解程度

## assessment_info
请选择所有正确陈述（一项或多项）。本实验室仅对选中的正确选项计分，每项一分。未选项及错误选项均不计分，也不扣分。完全正确要求选中全部正确选项且不选任何错误选项。本课程使用的 OPAL/ONYX 计分方案，还会对正确地不选错误选项给予一分。

## check
检查答案

## score
选中正确选项得分：{score}/{total}

## answer_full
完全正确

## answer_partial
部分正确

## answer_wrong
不正确

## assessment_details
已选错误选项：{incorrect}。尚未选中的正确选项：{missing}。分数本身不能证明答案完全正确。

## theory_quiz
基本原理

## three_quiz
三单元平衡与迭代

## references
参考文献与模型适用范围

## confined_preset
承压 · 无蒸散发

## unconfined_preset
潜水 · 无蒸散发

## learn_theory
进一步学习 · 推导 Picard 和 Newton

## notes_three
进一步学习 · 假设与建议实验

## notes_grid
进一步学习 · 完整模型与耦合更新

## learn_three
探索 · 三单元模型与蒸散发

## learn_grid
探索 · 十一个单元与复杂性增加

## language_proxy
内容提供英语、德语、法语、西班牙语、意大利语、印地语、阿拉伯语和简体中文。缺失译文时使用英语。

## closure
收敛标准

## head_closure
最大水头变化阈值（m）

## flow_closure
最大流量残差阈值（m³/s）

## closure_help
两项检查都必须通过。默认水头变化阈值为 1E-4 m，流量残差阈值为 1E-6 m³/s。在 Mehl (2006) 的小流量案例中，水头尚未稳定时流量检查可能已通过。改变阈值会重新评价保存的迭代状态，并可能允许继续运行。

## sync
同步

## sync_help
默认关闭：各按钮只推进自己的方法。开启后，两按钮置于同一框内；任一活动按钮推进两种可用方法。已收敛或已停止的方法保持不变。

## to_closure
运行至收敛

## to_closure_help
选择完整运行而不是单次更新，再按活动运行按钮。开关本身不会运行或重置模型。同步开启时，两种可用方法都运行至收敛或已诊断的停止条件。

## play_method
▶ {method}

## converged_method
✓ {method}

## stopped_method
■ {method}

## play_help
尝试对 {methods} 执行一次更新。

## run_help
继续 {methods}，直到收敛或已诊断的停止条件。

## stopped_help
{method}：{status}。

## outside_view
{method}：当前水头 {head:.3f} m 超出本视图，其数值仍保留在历史中。

## advanced
高级选项 · 阻尼

## advanced_help
阻尼将建议修正乘以 ω。小于 1 时采用较短数值步长，可能帮助收敛，但不保证收敛。

## conductivity_help
每个数量级选择 1 或 5：10⁻⁶、5×10⁻⁶、…、10⁻³ m/s。

## fig_cell
单元 {cell}

## fig_cell_number
单元编号

## fig_specified
给定水头

## fig_final
参考水头

## fig_top
含水层顶板：{top:g} m

## fig_bottom
底板：{bottom:g} m

## conductance_heading
1 · 从水头差计算流量

## balance_heading
2 · 建立水量平衡

## picard_heading
3 · 为 Picard 重排平衡方程

## newton_heading
4 · 为 Newton 线性化平衡方程

## compare_heading
Mehl（2006）的计算示例

## convergence_heading
判断何时停止

## fig_optional_et
可选 ET

## fig_recharge
补给

## current_head
当前水头：**{head:.3f} m**

## zoom
自动缩放

## zoom_auto
自动缩放

## zoom_manual
手动缩放

## zoom_help
将函数与对角线（Picard）或零线（Newton）的交点居中。初次设定时，当前水头位于中心至近侧边缘距离的三分之二处。直到距中心小于半宽的 25 % 才缩小范围；若水头超出窗口则扩大。最小完整宽度为 0.001 m。关闭自动缩放恢复完整视图，或使用 − 缩放 / + 缩放选择手动范围。改变模型输入或初始水头会恢复完整视图。缩放从不改变计算水头。

## zoom_in
+ 缩放

## zoom_out
− 缩放

## zoom_in_help
手动放大：从 1、0.1、0.01、0.001、1E-4、1E-5 m 中选择下一个更小的完整范围。关闭自动模式，并在迭代间保持范围，函数交点保持居中。改变模型输入或初始水头后恢复完整视图。

## zoom_out_help
手动缩小：从 1E-5、1E-4、0.001、0.01、0.1、1 m 中选择下一个更大的完整范围。关闭自动模式，并在迭代间保持范围，函数交点保持居中。改变模型输入或初始水头后恢复完整视图。

## general_settings
一般模型设置

## initial_boundary
初始条件与边界条件

## aquifer_parameters
含水层与 ET 参数

## uniform_k
均一 K（m/s）

## grid_quiz
耦合迭代与非线性

## paper_case
Mehl（2006）图组

## paper_smooth
光滑潜水平衡 · 图 2 和图 3

## paper_et
含 ET 的分段平衡 · 图 5 和图 6

## true_head_column
参考 h（m）

## hydraulic_parameters
含水层参数

## mehl_smooth_preset
Mehl（2006）· 潜水，无 ET · 图 2 和图 3

## mehl_et_preset
Mehl（2006）· 潜水，含 ET · 图 5 和图 6

## use_paper_case
在第 2 节使用此 Mehl（2006）案例

## initial_picard
中央初始水头 · Picard（m）

## initial_newton
中央初始水头 · Newton（m）

## mehl_conductivity
| 单元 | K（等效 m/day） |
|:--|--:|
| 1 | {kl:g} |
| 2 | {kc:g} |
| 3 | {kr:g} |

## mehl_k_help
与第 1 节相同，这里将原文的渗透系数数值解释为 m/day，并在内部换算为 m/s。

## fig_display_top
显示上限：{top:g} m

## model_preview
模型预览

## head_check_wait
水头变化检查：第一次更新后可用。

## head_check
最大 |Δh| = {value:.2e} m；阈值 {threshold:.0e} m — {result}。

## flow_check
最大 |F| = {value:.2e} m³/s；阈值 {threshold:.0e} m³/s — {result}。

## criterion_met
✓ 已满足

## criterion_unmet
尚未满足

## fig_residual_method
{method} · 流量残差

## fig_change_method
{method} · 水头变化

## fig_head_method
{method} · 水头

## fig_true_head_history
参考水头（{head:.3f} m）

## fig_flow_closure
流量阈值（{value:.0e} m³/s）

## fig_head_closure
水头阈值（{value:.0e} m）

## fig_head_axis
单元 {cell} 水头（m）

## slider_input
使用滑块设置初始水头

## iteration_summary
**h = {head:.3f} m** · k = {steps} · {status}

## analytical_head_column
解析 h（m）

## analytical_difference_column
参考 − 解析（m）

## analytical_unavailable
非均质渗透系数或含 ET 的情形不提供均质解析解比较。

## coupled_map_help
蓝色 Newton 曲线显示选定单元的流量不平衡，条件是每个试算水头下，其余八个内部单元都达到平衡。因此，对选定单元和设置得到一条固定曲线。橙色点标示当前估计。每条切线到达完整 Newton 建议水头，阻尼可缩短实际接受的步骤。收敛图使用实际九个水头处的流量不平衡。

Picard 面板显示最近接受的完整九水头更新。绿色曲线及其对角线交点可随其他水头改变。选定水头几乎不变时，曲线固定其他输入水头。历史图保留所有已接受水头。

## fig_step_fraction
步长比例 α

## fig_iteration_axis
迭代 k

## fig_head_detail
参考值附近 · < 1 cm

## postprocessing
后处理选项

## side_by_side
并排显示图形

## fig_zoom_range
{mode} · 水头范围 {width:.3g} m

## foundations_quiz
为什么需要迭代

## conductance_quiz
连接传导系数与达西流

## balance_quiz
水量平衡与非线性

## et_quiz
地下水蒸散发

## picard_quiz
Picard 迭代

## newton_quiz
Newton 迭代

## mehl_quiz
理解 Mehl (2006) 的示例

## author_credit
开发：**Thomas Reimann**（2026）· TUD Dresden University of Technology · The Groundwater Project · 基于 [Mehl (2006)](https://doi.org/10.1111/j.1745-6584.2006.00207.x)
