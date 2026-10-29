# 上游方法与工具选择

2026-10-29 在线查阅上游 README 后整理。以下为选型依据及本技能的适配建议；不是所有工具已安装、集成或跑过的声明。执行前核对实际版本、API、输入前提和许可证，记录版本或 commit；不依赖网络才可阅读本技能。

| 上游 | 方法用途 | 适配限制与验证 |
|---|---|---|
| [meshoptimizer](https://github.com/zeux/meshoptimizer/blob/master/README.md) | 简化、属性感知、索引/缓存/fetch、量化及压缩 | 区分只输出索引与更新顶点的接口；最终索引确定后压紧所有流。属性缝、骨骼和边界约束需明确；不能据数量推断外观或帧率 |
| [glTF Transform](https://github.com/donmccurdy/glTF-Transform/blob/main/README.md) | glTF/GLB 读写、去重、裁剪、简化、动画与压缩管线 | 变换是否保真取决于具体操作；注册所需扩展/解码器；避免 prune/合并移除业务节点，实际重导入 |
| [PyMeshLab](https://github.com/cnr-isti-vclab/PyMeshLab/blob/main/README.md) | MeshLab 过滤器的 Python 接口，清理与网格处理 | 从实际版本过滤器列表确认 QEM/纹理及度量选项，不编造函数名；不会自动保留业务绑定 |
| [Open3D](https://github.com/isl-org/Open3D/blob/main/README.md) | 点云、表面、采样与三维数据处理路线 | 点云减点独立检查覆盖与属性；网格处理先查 UV/材料/动画支持，不能仅因能读取就假定能保真往返 |
| [UnityMeshSimplifier](https://github.com/Whinarn/UnityMeshSimplifier/blob/master/README.md) | C# QEM 与引擎网格、LOD 接入参考 | 上游说明基于 Fast Quadric 路线；smart linking 与保护参数仍需验证，维护与兼容情况按实际版本确认 |
| [Instant Meshes](https://github.com/wjakob/instant-meshes/blob/master/README.md) | 场对齐重拓扑，可作扫描/雕刻重网格选路 | 重新生成拓扑后，原 UV、材质、权重、形态键与索引绑定不能假定保留；需转移/重烘焙和独立检查 |

Blender 是随包静态候选工具的执行宿主。使用其他 DCC 或运行时的原生工具同样可遵循该工作流；不需要为套用脚本转换所有资产。第三方工具的许可证不随本包 MIT 改变。

实际选型顺序：先看资产与现有工具，再核对属性能力、保护约束、导出与目标运行时，最后比较候选质量和运行成本。不要把同一算法的多个封装当独立算法证据。压缩改变传输/存储，不自动改变三角面；LOD 降低特定视距的工作量，可能增加总资源量。

已有配套技能可用于文献/源码查阅、工具执行、统计、调试或界面检查；存在时按需复用，不存在时使用等价方法，不设置特定助手或付费服务为前置条件。
