# RGT

QwenRGT 训练与评测展示网页：LIBERO-Plus、LIBERO-PRO、VLABench，四类泛化与三种机制分析。

静态网页入口：`index.html`。GitHub Pages 从 `main` 分支根目录发布。

机制热力图、曲线与因果干预分布为示意，不是实验结果。样例图片为官方演示静帧，训练任务参考不等于已核实的训练集 episode。

仓库仅包含网页与配图，不包含模型、训练日志、数据集或访问凭据。

## 第三方图像来源

- `media-pro-original.png`、`media-pro-shift.png`：LIBERO-PRO 官方网页 `static/videos/position-original.mp4` 与 `position-x-0-2.mp4` 的首帧。https://zxy-mllab.github.io/LIBERO-PRO-Webpage/
- `media-plus-bg.png`：LIBERO-Plus 官方环境扰动演示中 alphabet soup 任务的首帧。https://sylvestf.github.io/LIBERO-plus/
- `media-vla-base.png`、`media-vla-semantic.png`：VLABench 官方 `media-primitive_task/select_fruit/base.mp4` 与 `semantic.mp4` 的首帧。https://vlabench.github.io/

第三方素材权利归原作者；本仓库不为其重新授予许可。

## 2026-11-03 · Explore 分类扩展

01 展示 Plus 七类、Pro 1.0 五维、Pro 2.0 六维（22 静态 / 20 动态）、VLABench 六类能力与六个评测 tracks。简短例子是中文机制释义，不冒充实际训练 episode。官方定义来源链接内嵌各卡片。

`media/pro2-d07-rollout.mp4` 与 `media/pro2-d07-initial.png` 是本项目 QwenFAST MoT6 30k 的 Pro 2.0 D07 接入检查（2026-11-03，Spatial task 0，seed 7，init 0）。第 34 步真实触发相机偏移；视频仅展示机制，不是全量 benchmark 成绩。原始证据位于协调工作区 `artifacts/libero_robustness_20261103/pro2_smoke`。

Pro 1.0 官方定义含 Environment；当前固定资产版本接入仅四类，网页明确保留此差异。VLABench Track 5 的训练／测试任务划分由实验者指定。

## 2026-11-03 · 两套域内泛化入口

02 对应 `libero-generalization` 与 `vlabench-generalization`，分别使用各自数据训练的 checkpoint，不包含跨数据集零样本任务。

当前 FAST30k 训练清单 40 任务；LIBERO-90 去除 3 个重叠指令后保留 87 个任务。完整 LIBERO CPU 计划为 25,405 次执行，尚未进行新全量策略评测。VLABench 评测代码已实现，仍待仿真资产、相机映射及域内 checkpoint 的闭环核验；动作留出任务没有官方固定切分，不虚构覆盖。

统一结果：逐任务成功率、视频、四类能力；缺失为 N/A。代码和运行说明：
https://github.com/huaihailv/starVLA-RGT/blob/musa/examples/RobustnessEval/GENERALIZATION.md


## 2026-11-05 · 每个 subset 一个真实任务

Explore 保留第一行五个 benchmark 标签，第二行按 subset 切换。PLUS 的七类在宽屏上同排，窄屏横向滚动；PRO 1.0 五类、CF 四主类及 Focused 对照、VLABench 六个 tracks 各有独立入口。PRO 2.0 六个维度下可选择全部22静态/20动态扰动（不含已删除D19），每种扰动一例。

`media/subsets/cases.json` 与同目录62张PNG是实际任务素材：PLUS7、PRO1四类、PRO2共42、CF主类4、VLABench5。PLUS/PRO图片取自本项目已完成Qwen+OFT评测视频的第一帧；CF来自50任务CPU环境检查；VLABench来自T1/2/3/4/6的add_condiment固定案例环境检查。CF和VLABench图像不是模型闭环成绩；动态PRO2图片为干预前初始观察，触发步另行说明。未挑选成功轨迹来暗示模型表现。

仍缺真实素材的三组明确保留说明：PRO1 Environment（当前固定资产版本缺配套任务）、CF Spatial-Focused（尚未采样）、VLABench T5（未指定训练/留出清单）。不以其他subset图片冒充。原有02部分标注为2026-11-03历史快照，不作为当前运行进度。

任务元数据与图片来源：LIBERO-Plus、LIBERO-PRO、LIBERO-Pro2.0、VLA-CF、VLABench的官方仿真器与本项目观测；第三方模型/纹理/场景权利归原作者。图片只是输入示例，不是新的成功率结果。

编辑数据/分类后运行 `python3 scripts/build-explore.py` 生成01静态HTML；交互位于 `benchmark-tabs.js`。支持键盘左右箭头/Home/End、subset深链接和PRO2具体案例深链接，无额外前端依赖。
