# mesh-optimize-verified

版本 **0.2.0** · MIT · 通用三维资产降面、减点与验证技能。

供任何使用者及能读取指令的助手复用，不绑定特定应用、资产来源或助手提供商。适用于静态网格、带贴图资产、硬表面装配、角色动画、扫描网格、场景与 LOD；点云提供独立选路和验证方法。具体可执行能力取决于实际工具、格式和资产特征。

目标是在约定预算下保留需要的形状、外观、属性与功能，并验证目标环境的帧表现。它是知识、决策流程和工具包，不是训练权重，也不承诺任意输入都能达到任意比例或任意设备绝不掉帧。

## 使用

下载当前仓库完整目录，使用支持技能的宿主自身的加载方式；不支持时，让执行者先读取 `SKILL.md`，再按链接读取必要文件。只有文本能力时可做分析与操作指导；真实修改、导出、图像检查和性能测量需要相应软件、执行权限或人工返回实际结果。

可直接使用以下请求：

> 请读取 SKILL.md，分析我提供的三维资产及实际工具，按适合的路线降面和减点。沿用我已给出的输出格式、预算、观察尺度和目标环境；保留原件，先测无优化往返，再做代表性局部试验。交付新候选、重导入计数、外观与功能检查和真实运行性能证据。没有执行的写未验证；不能用减少面数代替帧率测量。

## 能力边界

| 层级 | 提供内容 | 边界 |
|---|---|---|
| 通用流程 | 按资产选路、预算组合、属性/语义保护、验证与交付 | 不要求固定工具；不能由文档保证所有输入可行 |
| 静态网格候选脚本 | Blender 下读取 .blend/.glb/.fbx，指定对象做 Collapse Decimate，导出 blend/GLB | 目标有修改器、骨骼权重、形态键或链接数据等时拒绝；不是所有格式的转换器 |
| GLB 审计 | JSON 声明与普通节点计数 | 不解码压缩几何，不展开 GPU 实例扩展，不代替验证器和真实导入 |
| 帧数据分析 | 线性百分位、长帧、分组对照 | 不采集帧，不确认画面、采集器真实性或场景覆盖 |

角色、扫描、建筑场景和点云等路线需使用[资产路线](references/asset-routes.md)中的适配工具；不可强行套用静态比例脚本。

## 可运行工具

Python 工具使用标准库，需 Python 3.10+。候选脚本需 Blender；集成测试记录具体版本，不推定其他版本已通过。命令从技能根目录运行；示例路径、预算和容差需按任务填写，输出目录/文件应为新路径。

```text
python -m unittest discover -s tests -v
python tests/blender_smoke.py --blender /path/to/blender
blender --background --factory-startup --python-exit-code 9 --python scripts/blender_candidate.py -- --input /models/source.blend --output-dir /experiments/candidate-001 --objects Body --ratio 0.5
python scripts/audit_glb.py /experiments/candidate-001/candidate.glb --out /experiments/count-001.json
python scripts/analyze_frames.py tests/fixtures/frames-synthetic.json --out /experiments/frames-001.json --threshold-ms 16.67 --relative-allowance 0.05 --absolute-allowance-ms 0.2
```

Shell 的可执行文件路径引用方式按所在系统调整。`ratio` 是请求保留比例，不是保证达到的输出比例或误差上界。例中的帧数据是合成测试，数值不是通用验收线。

## 验证和参考

[评估协议](references/evaluation.md)给出工具测试、不同类别未见资产实操及有/无技能对照方法。[上游参考](references/tool-references.md)列出方法依据、适用范围及限制；在线查阅不等于已集成或实测所有工具。

当前验证记录见 [validation/current.json](validation/current.json)。旧版本的验证只属于旧版本；当前包不依赖历史工程、私有模型或本机实验缓存。所有新效果结论需绑定实际输入、导出文件、工具版本与目标设备。

本包代码与文档采用 [MIT](LICENSE)。第三方工具遵循各自许可，未将第三方源码、模型或私有工程打包。当前默认分支是最新技能；下载时注意版本，历史标签保留原始记录。
