> 公开副本：原始报告针对0.1.0归档；个人绝对路径仅替换为占位符，其余结论保留。0.1.1是作者的许可/文档发布整理，未冒称DeepSeek重新审计。

# mesh-optimize-verified 0.1.0 独立复核记录（DeepSeek Harness）

- 日期：2026-10-28
- 对象：`deliverables/mesh-optimize-verified-0.1.0.zip`（sha256 `20667859cba4fb47b433281613acb0bfa7def20e65d8881ae7a8a0402ead158c`，119,503 B）
- 机器可读结果：`reports/mesh-skill-deepseek-verification-20261028.json`
- 结论先行：在本次可执行的桌面环境内，包的身份、清单、工具、溯源链与文档声明均核实通过，**未发现阻断性缺陷**；但这不是无/有 skill 的 A/B 盲测，也没有未见真实模型 + Unity Player/目标设备实测，因此不能据此宣称 skill 对未见模型有效或“绝不失帧”。

## 1. 产物身份与可移植性

| 检查 | 方法/证据 | 结果 |
|---|---|---|
| 外置 SHA256 与 zip 一致 | 与 `*.zip.sha256` 比对 | PASS |
| ZIP CRC | Python `zipfile.testzip()` | PASS（无坏文件） |
| 根目录结构 | 27 个条目，全部在 `mesh-optimize-verified/` 下，无路径穿越 | PASS |
| 逐文件清单 | `SHA256SUMS.json` 26 条；实际 payload 26 个；无缺失/多余/不匹配 | PASS |
| 源码目录 = zip payload | 26/26 文件哈希一致（`__pycache__` 未入包） | PASS |
| 已安装副本 | `<INSTALLED_SKILL>` 26/26 哈希一致，清单一致 | PASS |
| 清单自指 | `SHA256SUMS.json` 不含自身哈希（惯例，非缺陷） | 说明 |

## 2. 执行环境与实际复跑

- Windows；Blender **5.2.1 LTS**（build 2026-08-25）位于 `<BLENDER_EXECUTABLE>`。
- Python **3.10.11**（系统）与 **3.12.14**（DSH 自带）各跑一遍；**无 Unity / Player / 目标设备**。
- 所有复跑均在换目录解压副本 `<DEEPSEEK_AUDIT_ROOT>/extracted/mesh-optimize-verified` 中进行，未修改源目录与 zip。

| # | 检查 | 结果 |
|---|---|---|
| 1 | `quick_validate.py`（skill-creator） | **PASS — “Skill is valid!”** |
| 2 | `python -m unittest discover -s tests -v` | **15/15 通过**（Python 3.10 与 3.12 均通过） |
| 3 | `tests/blender_smoke.py --blender <BLENDER_EXECUTABLE>` | **PASS**：Body 1106V/2208T → 333V/662T；Rim/Pin 属性摘要相同；源文件 SHA 不变；blend+GLB 实际重导入；linked Mesh 明确拒绝；重复输出目录拒绝 |
| 4 | `blender_candidate.py --help` 经 Blender 执行 | PASS（退出 0，帮助正常） |
| 5 | 真实 GLB 输入（独立测试候选） | PASS：Body 1986V/662T → 1853V/529T（ratio 0.8）；Rim/Pin 不变；源 SHA 不变；报告 `UNVALIDATED_CANDIDATE` |
| 6 | `audit_glb.py` 真实候选 GLB | PASS：声明 3594V/1474T、3 mesh 节点；`decoded_geometry_validated=false`；重复输出退出 2 |
| 7 | `analyze_frames.py` 合成 fixture | 正确保留 detail 回归；`all_measured_comparisons_pass=false`、`full_acceptance_proven=false`（符合预期语义） |
| 8 | `analyze_frames.py` 对真实 ZR 快照（25ms/5%/0.2ms） | 6144 帧、6 组比较；三视角全部 pass；仍 `full_acceptance_proven=false`；重复输出退出 2 |
| 9 | 文档/结构 | 9/9 相对链接可解析；frontmatter name 22 字符、description 236 字符、version 0.1.0，均符合校验器 |

## 3. 溯源链独立复算（关键项）

原始证据位于 `deliverables/PCB_FeatureReview_V4ZR_ReviewCandidate/Evidence/`，均与本包记录互相印证：

| 链路 | 结果 |
|---|---|
| `ordinary_screen_raw.json`（220,956 B，sha256 `99afa3721717230d57eceebdfde4cf359cad7f4d7ab52410d321b17826ec4d77`） | 与 `provenance/zr-screen-frames.json` 的 `environment.source_raw_sha256` **一致** |
| `state.json`（4,448 B，sha256 `824ac6f2bd97cb2b25dc42a4c304f1bee7b4039ffea296ea2a4210f173ecfd83`） | 与 `provenance/project-snapshot.json` 的 `source_state_sha256` **一致** |
| 原始 12 行 / 6144 帧 → 快照 12 行 / 6144 帧 | **逐帧 0 差异**；仅字段改名（`frameMs→frame_ms`、`leg→block`、`optimized→candidate`）与环境字段映射 |
| `state.json` → `project-snapshot.json` | 25 个共享字段 **0 不匹配**（含 Unity 计数、headroom、图像通过/失败数、strict 标志、人工/教学/GLB 未验收标志） |
| `ordinary_screen_analysis.json` → 快照 `ordinaryScreenSummary` | 6/6 行，frames/meanFPS/p50/p99/max/>25ms/>33.33ms 全部精确相等 |
| 包内 analyzer 重算 `zr-frame-reanalysis.json` | P50/P95/P99/max/长帧计数精确相等；`mean_fps` 仅浮点末位差（最大 `5e-14`，求和顺序所致） |
| `provenance/source-index.json` | 816 条：**816/816 文件存在、字节与 SHA256 全部匹配**；无绝对路径；groups 合计 816 |
| 独立前向测试报告 | `REPORT.md` sha256 = `c00d0f24…e1207`，与 `validation/independent-forward-test.json` 记录一致；其 `zr-screen-analysis.json` 与包内 validation 文件字节相同 |

## 4. 卫生与合规扫描

- 未发现个人绝对路径、邮箱、API key/私钥、口令字面量；scripts 仅标准库（Blender 助手依赖 `bpy`），**无网络/上传调用**；包内无第三方源码、老师模型或商业资源。
- 版本号一致：zip 名、SKILL metadata、acceptance schema 均为 0.1.0。
- 包内文字明确保留：DeepSeek 未实测、未见真实模型未验证、标准 GLB 未新导出、人工外观未验收、不承诺永不掉帧；未发现夸大表述。

## 5. 发现（均非阻断）

1. `validation/zr-frame-reanalysis.json` 用当前包内 analyzer 复跑时，`mean_fps` 有末位浮点差（≤5e-14）；P50/P95/P99/max/长帧计数完全一致，文档“重算与原记录一致”在数值上成立。若追求逐位可复现，可用当前脚本重生成该 JSON（会改动包哈希与 zip，需作者决定）。
2. linked-library 拒绝仅覆盖“本地 Object 引用 linked Mesh”这一已修复回归；object override / linked collection 未被 smoke 覆盖，属残余未验边界。
3. 无 LICENSE 文件；README 已写明由权利人决定许可证。公开发布前需补许可证或明确保留权利。
4. 父目录 git 仓库尚无提交、无远端；上传 GitHub 仍需用户选择仓库与许可证，并只提交 skill 目录及验证结果。

## 6. 仍未验证（不得写成已通过）

- DeepSeek 无/有 skill 的 A/B 盲测与实际增益；T5“未见真实模型 + 目标 Unity Player/设备”实操。
- ZR 标准 GLB/blend 新导出与重导入；Unity 目标场景逐帧（本次无 Unity/Player）。
- 人工常规观看尺度外观验收、完整教学/XR 验收。
- Blender 5.2.1 以外版本；FBX 输入路径（本次实测 .blend 与 .glb）；大型真实 CAD/薄壁模型。
- 因此：本次可支持“包可运行、数据可追溯、已测范围内工具行为符合说明”，**不支持**“对任意 AI/模型有效”“绝不掉帧”“全面验收通过”。

## 7. 结论

该 0.1.0 zip 在本次桌面环境复跑中通过身份/清单/安装/单测/Blender smoke/CLI/溯源复算与卫生检查，未发现阻断性缺陷或与文档相悖的声明。可以进入用户决定的上传准备：选择许可证、提交 skill 目录与验证结果、保留未验证范围说明；如要对外宣称“有效”，还需按其自带的 `tests/evaluation-tasks.md` 完成 A/B 盲测和未见模型 + 目标设备实测。

> 本次复核未修改 skill 源目录、zip 或已安装副本；临时产物与命令输出位于 `<DEEPSEEK_AUDIT_ROOT>/`。