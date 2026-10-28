# 2026-10-23历史26项仓库参考

这是项目已有调研的精简索引，属于历史选型结论；本次没有逐库重跑。分支、依赖、许可证及维护状态执行前查上游，不把旧快照当当前事实。没有把这里的第三方源码打进技能包。

| 项目 | 当时提炼的用途与限制 |
|---|---|
| [blender/blender](https://github.com/blender/blender) | 已实际使用的FBX/GLB检查、Decimate和参数化平台；Planar polygon减少需重三角化验数 |
| [Whinarn/UnityMeshSimplifier](https://github.com/Whinarn/UnityMeshSimplifier) | 原生Unity QEM候选；明确配置边界/UV保护和属性输出，不默认全部保护 |
| [cnr-isti-vclab/PyMeshLab](https://github.com/cnr-isti-vclab/PyMeshLab) | Python过滤器、带贴图QEM及距离检查；不是Unity业务资产适配器 |
| [cnr-isti-vclab/meshlab](https://github.com/cnr-isti-vclab/meshlab) | 同一路线的界面/底层实现，不额外算一种独立算法 |
| [zeux/meshoptimizer](https://github.com/zeux/meshoptimizer) | 项目实际使用；属性简化+完整流重映射/压紧、缓存/fetch重排 |
| [donmccurdy/glTF-Transform](https://github.com/donmccurdy/glTF-Transform) | GLB weld/simplify/prune；不是FBX/GUID教学工程替换器 |
| [RamType0/Meshia.MeshSimplification](https://github.com/RamType0/Meshia.MeshSimplification) | Jobs/Burst调度候选；并行实现本身不证明更快、更保形 |
| [touma-tw/Meshia.MeshSimplification](https://github.com/touma-tw/Meshia.MeshSimplification) | UV属性误差和材质约束参考；偏特定应用，先做工业件小样 |
| [pyvista/fast-simplification](https://github.com/pyvista/fast-simplification) | 纯几何QEM/折叠序列对照；target_reduction为删去比例，不能反用 |
| [sp4cerat/Fast-Quadric-Mesh-Simplification](https://github.com/sp4cerat/Fast-Quadric-Mesh-Simplification) | 简洁QEM实现；薄截面和完整多零件属性不是其简单命令行强项 |
| [mikedh/trimesh](https://github.com/mikedh/trimesh) | 分组、采样、距离与外围检查；简化可能调用同源依赖，不重复算算法 |
| [gradientspace/geometry3Sharp](https://github.com/gradientspace/geometry3Sharp) | C#约束/投影简化实现参考；需独立恢复材质属性 |
| [libigl/libigl](https://github.com/libigl/libigl) | 自定义折叠回调；C++适配成本和逐组件许可证需检查 |
| [CGAL/cgal](https://github.com/CGAL/cgal) | 策略/法线变化过滤器参考；模块许可与编译前提不可略过 |
| [isl-org/Open3D](https://github.com/isl-org/Open3D) | 点云/纯几何基线；历史所读简化路径对三角UV有限制，不当带贴图首选 |
| [wjakob/instant-meshes](https://github.com/wjakob/instant-meshes) | 重拓扑/重烘焙路线；不能默认继承原UV与零件绑定 |
| [valette/ACVD](https://github.com/valette/ACVD) | CVD/特征重网格参考；VTK依赖及属性恢复成本较大 |
| [Unity-Technologies/AutoLOD](https://github.com/Unity-Technologies/AutoLOD) | LOD导入架构参考；历史实验性质，LOD不替代基础模型减面 |
| [Unity-Technologies/UnityMeshSimplifier](https://github.com/Unity-Technologies/UnityMeshSimplifier) | 同源旧版本，不因组织名就优先，不与上游当两个算法 |
| [manaporkun/Automatic-LOD-Generator](https://github.com/manaporkun/Automatic-LOD-Generator) | 编辑器、保存/撤销流程参考；依赖简化器，不必先装整套LOD |
| [refiaa/MeshOptimizer.Unity](https://github.com/refiaa/MeshOptimizer.Unity) | 历史所读截短索引和重算法线路径有缺面/外观风险；不是zeux绑定 |
| [TLDR-Electronics/Batch-Planar-Decimate-Blender-Add-On](https://github.com/TLDR-Electronics/Batch-Planar-Decimate-Blender-Add-On) | 选中物体遍历/计数骨架；默认直接应用修改器不充分保护硬缝 |
| [ufbx/ufbx](https://github.com/ufbx/ufbx) | FBX层级/属性读取器参考，不是减面器或完整FBX导出器 |
| [assimp/assimp](https://github.com/assimp/assimp) | 多格式适配与清理；OptimizeMeshes等标志不是高保真QEM验收 |
| [Unity-Technologies/com.unity.formats.fbx](https://github.com/Unity-Technologies/com.unity.formats.fbx) | 需要Unity→Blender往返时参考导出流程；不是简化算法 |
| [google/draco](https://github.com/google/draco) | 几何压缩与解码；文件变小不代表面数变少，需解码支持 |

与后续结构重建/诊断相关的CadQuery、KiCad StepUp、RenderDoc、AssetRipper和REA见tool-references.md；它们不混入这次历史26项数量。许可证不从仓库名或GitHub自动标签推断，按实际使用组件和文件核对。
