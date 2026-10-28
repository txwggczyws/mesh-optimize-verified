# 工具路由、现有skill复用与上游参考

优先读当前工程、可读源码与冻结证据。根据输入选工具，不为凑齐清单安装所有工具。以下链接是上游资料，不是作者对我们模型效果的保证；实际API/版本以执行时安装版本为准。

| 工具/项目 | 何时使用 | 边界与项目状态 |
|---|---|---|
| [Blender](https://github.com/blender/blender) / [Decimate文档](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/decimate.html) | 离线FBX/GLB、局部小样、参数化与实际重开 | 本项目实际使用；工具自动选择/材质转换及硬边仍需检查；本次网页版Decimate文档抓取失败，使用本机5.2.1接口实测，不称其当前网页已核对成功 |
| [meshoptimizer](https://github.com/zeux/meshoptimizer) | 属性感知简化、完整流去重/压紧、缓存与fetch优化 | 本项目实际使用JS/WASM离线路径；不代表向Unity加入WASM/DLL；输入适配与属性接缝影响可达面数 |
| [UnityMeshSimplifier](https://github.com/Whinarn/UnityMeshSimplifier) | Unity原生静态网格QEM小样 | 已调研候选，不声称已在全部PCB上使用；边界与UV保护选项不是全自动 |
| [PyMeshLab](https://github.com/cnr-isti-vclab/PyMeshLab) / [MeshLab](https://github.com/cnr-isti-vclab/meshlab) | 清理、QEM、纹理简化与独立距离评估 | 同一路线的接口/应用，不算两个独立算法证明；不会直接理解Unity业务引用 |
| [glTF Transform simplify](https://gltf-transform.dev/modules/functions/functions/simplify) | 现有glTF/GLB的简化管线 | 与压缩、重排、去重区别对待；保持scene实例、材质与扩展兼容 |
| [CGAL Surface Mesh Simplification](https://doc.cgal.org/latest/Surface_mesh_simplification/index.html) | 明确需要拓扑/约束方法时小试 | 计划/依赖存在不等于PCB实际解决；编译、许可证与输入前提另核对 |
| [CadQuery](https://github.com/CadQuery/cadquery) / [KiCad StepUp](https://github.com/easyw/kicadStepUpMod) | 有尺寸/截面或可用CAD来源时重建 | 项目历史为资料/条件性路线，不能写成已完成CAD恢复 |
| [Unity应用性能分析](https://docs.unity3d.com/2022.3/Documentation/Manual/profiler-profiling-applications.html) | 构建版/目标设备测量 | 最终需要实际运行；Editor或同步离屏不代替全部屏幕/XR |
| [D3D11缓冲区](https://learn.microsoft.com/en-us/windows/win32/direct3d11/overviews-direct3d-11-resources-buffers-intro) | shader表容量、常量buffer规划 | 单buffer约束不等于程序所有buffer总容量；本项目仅对特定D3D11实现讨论 |
| [RenderDoc](https://renderdoc.org/) | 已有可重现GPU异常，需要draw/覆盖证据 | 条件性工具；不默认安装，不称本项目已用其证实唯一瓶颈 |
| [AssetRipper](https://github.com/AssetRipper/AssetRipper) | 只有Player/Bundle且授权读取资源时 | 有源码/可读prefab就先读；不为普通减面默认逆向商业编辑器 |

本次创建时在线读取确认：Agent Skills规格、meshoptimizer README、Unity2022.3应用性能文档、UnityMeshSimplifier仓库及glTF Transform simplify页。其余是原项目调研保留入口，执行前核对；没有逐个重新安装/运行。历史调研有26项仓库审查、51份文档/源码保存，不代表全部工具都已跑过。

26项历史仓库与取舍完整保留在[历史参考索引](historical-repository-index.md)，用于找回选型经验，不必每次全部读取。两个值得单独保留的坑：fast-simplification的`target_reduction`是**删除比例**，与保留比例相反；名为MeshOptimizer.Unity的封装不等于zeux/meshoptimizer绑定，原项目读到的索引截短路径可能直接造成缺面，不应为达目标强截索引数组。gltfpack默认可能合并/裁剪节点，使用命名节点保留选项也需验证教学语义。

## 合理复用已有skill

本包是自包含技能；以下是本项目环境中的可选能力，其他AI没有这些skill时按等价工具完成，不应因此停止。

- **skill-creator / writing-skills**：制作可发现入口、按需引用、确定性脚本与独立使用测试。不要把阅读本包当作训练模型权重；不把A/B里本来就会的回答称为skill增益。
- **Lux3D**：用户要求新建/处理资产且该能力适合时，使用其真实报价、任务跟踪与交付验证；本次仅参考其保原件/真实验证规范，没有调用付费生成。现有CAD精确减面优先本地几何工具，生成模型不能代替尺寸保真。
- **systematic-debugging / verification-before-completion**：先定位异常和做对照，再改动；保存运行证据后才称成功。
- **reverse-engineer-anything（REA）**：仅现有可读源码不足且确有授权目标时，针对资源/运行时问题取证；不要因资源来自Unity就默认逆向。
- **data-quality / statistics类skill**：有复杂实验/统计需求时检查样本、百分位、范围和缺失值；不凭空制造显著性或独立复测。
- **computer-use / playwright**：确需真实打开、截图或界面审查时使用；有本地/API工具可用就优先工具。文件成功保存不等于真实窗口已打开。
- **Git/GitHub能力**：仅用户要求发布时才上传；当前打包供DeepSeek测试，不包含自动推送或发送消息。

不需要与几何任务无关的论文、旅游、网页、视频等skill。复用方法与边界即可，不把已有skill全文或其第三方实现复制进本包。

Agent Skills目录规范参见[官方规格](https://agentskills.io/specification)。本包SKILL.md与相对引用可被文件型代理加载；具体AI产品是否自动识别取决于其宿主功能。
