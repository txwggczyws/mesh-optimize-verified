# mesh-optimize-verified

版本0.1.1（公开测试版，MIT许可）。将物联网模型优化项目从资源盘点、Blender小样，到PCB V2/V3、V4系列及2026-10-28 ZR候选的可复用经验整理为Agent Skill。包含实际可运行的候选生成、GLB计数、逐帧分析工具，以及独立测试协议。

这属于知识与流程蒸馏，没有微调DeepSeek或其他模型权重。支持读取文件与执行工具的AI可直接使用；只有聊天能力的AI可以阅读并生成操作方案，但不能代替软件真正修改模型、检查图像或测帧。

## 当前发布与验证

项目地址：[txwggczyws/mesh-optimize-verified](https://github.com/txwggczyws/mesh-optimize-verified)。
下载：[GitHub Releases](https://github.com/txwggczyws/mesh-optimize-verified/releases)。

0.1.1在已复核0.1.0的基础上补充MIT许可、脱敏DeepSeek复核记录和发布说明；三个优化/审计/统计脚本逐字节不变。原始0.1.0归档仍保留其原SHA256，不能把旧包的复核改称对新文档版本的独立复核。

- DeepSeek已对**0.1.0压缩包**完成工具复跑与溯源核对：[复核报告](validation/deepseek-review-0.1.0.md)、[机器可读结果](validation/deepseek-review-0.1.0.json)。报告内本机路径已换成占位符。
- 发布版验证见[发布记录](validation/publication-0.1.1.json)。原单测、Blender真实导出/重导入及保护拒绝检查会在发布目录重新运行。
- 尚未完成DeepSeek有/无skill增益盲测、未见真实模型和目标Unity Player/设备验收；不承诺任意模型或设备绝不掉帧。

原始实验的来源索引用于历史追溯；相关老师模型和私有实验目录未公开。使用本skill不需要访问那些目录，随包测试和快照可独立运行。首次使用请先在模型副本上做小试验，并按目标格式重新导入验数。

## 给任意AI的最短用法

把整个文件夹交给AI，发送：

> 请先读取 mesh-optimize-verified/SKILL.md，再按需读取其引用文件。对我提供的模型做可验证的降面与减点。先核对已给出的预算、格式、外观尺度与目标设备；保留原件，从一个代表性局部试验开始。执行你实际具备的工具，交付新候选、重新导入后的计数、外观/几何检查和目标设备帧数据；没有测到的明确写未验证。不要把减少面数当作不掉帧的证明。

支持Agent Skills的工具：将本文件夹放入该产品支持的skills目录。Codex可复制到 `~/.codex/skills/mesh-optimize-verified`；是否立即发现以客户端当前会话为准。其他AI应使用自己的技能加载机制；不要求安装Codex、Lux3D、REA或MCP。

DeepSeek网页版：上传本文件夹相关文本/代码；若界面不支持目录，先贴SKILL.md，再按它的路由附上需要的引用。完整实操需要本地代理或由人执行命令并返回原始结果。不能说模型“内置学会了”这个skill。

## 本地工具

Python脚本只使用标准库，需Python3.10+。Blender工具需本地Blender，当前集成测试为5.2.1；其他版本需重测。所有命令在skill根目录运行；将占位路径替换为真实路径。

```powershell
python -m unittest discover -s tests -v
python tests/blender_smoke.py --blender 'X:/tools/blender.exe'

# 必须经Blender执行；仅Body允许修改，其他网格受保护。输出目录必须不存在。
& 'X:/tools/blender.exe' --background --factory-startup --python-exit-code 9 --python scripts/blender_candidate.py -- --input 'X:/models/source.blend' --output-dir 'X:/experiments/candidate-001' --objects Body --ratio 0.5

python scripts/audit_glb.py 'X:/experiments/candidate-001/candidate.glb' --out 'X:/experiments/glb-audit-001.json'

# 下面数值只是项目选项示例，不是所有项目的默认验收线。
python scripts/analyze_frames.py tests/fixtures/frames-synthetic.json --out 'X:/experiments/frame-analysis-001.json' --threshold-ms 16.67 --relative-allowance 0.05 --absolute-allowance-ms 0.2
```

Blender工具只做指定静态网格的Collapse Decimate小样；有修改器、骨骼权重、形态键或链接库的目标会拒绝处理。复杂CAD、薄壁、硬缝、教学交互及Unity自定义shader不由一个比例自动保护。输出blend、GLB与报告，状态固定为`UNVALIDATED_CANDIDATE`。导出的标准材质还需检查。

## 包的内容与发布

`references/`包含工作流、几何方法、性能、项目案例、工具参考和DeepSeek测试。`tests/`包含算法检查、Blender真实导出重导入小样、合成帧数据。`provenance/source-index.json`记录提炼来源的相对路径与哈希；它是追溯索引，不是所有原工程文件的副本。`provenance/project-snapshot.json`是本次读取到的ZR状态精简快照。

不附老师模型、商业资源、私有参考工程、密钥、本机账号目录或第三方源码。旧项目算法脚本依赖冻结缓存、Unity宿主和本机路径，不能伪装为通用即用工具；其方法已转写为引用文档。包内没有自动上传或联网调用。

准备上传GitHub时，提交整个skill目录及随包验证结果；README中保留候选与未验证范围。本包代码和文档采用[MIT许可证](LICENSE)；引用库仍遵守各自许可证，未包含其源码或模型。尚未完成DeepSeek盲测和真实新模型目标设备实测时，不能写“对所有AI/模型有效”或“绝不失帧”。
