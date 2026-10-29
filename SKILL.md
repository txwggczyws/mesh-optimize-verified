---
name: mesh-optimize-verified
license: MIT
description: Reduce polygon and vertex counts in 3D assets with verified geometry, appearance, attributes, export and runtime performance. Use for static or animated meshes, textured assets, scans, assemblies, scenes, LOD and point-cloud reduction, choosing tools according to the asset and target environment. 适用于通用三维资产降面、减点、保形及性能验证。
metadata:
  version: "0.2.0"
---

# 通用三维资产降面与减点 / Verified mesh optimization

Apply this workflow to the supplied asset and its intended use. It is independent of assistant provider, owner and application domain. Use available equivalent tools; the bundled scripts cover only the explicitly documented subset. A workflow is portable; successful optimization of every possible asset and zero dropped frames on every device are not guaranteed.

## Establish the asset contract

Inspect the input and available tools. Reuse requirements already supplied; ask only about essential unknowns. Record source/dependency hashes, format, units, transforms, hierarchy, materials, animation and interaction constraints, viewing scale, count/error budgets and target environment. Distinguish mesh vertices, render vertices, point-cloud samples, polygons, final triangles and instance totals. Read [workflow](references/workflow.md).

Keep originals immutable. Use a new candidate directory and run an unchanged import/export roundtrip first. Attribute losses caused by conversion must not be counted as simplification success. Work offline on geometry when a runtime is unavailable; mark runtime validation pending.

## Choose the route by asset and bottleneck

Read the relevant row of [asset routes](references/asset-routes.md), then [geometry](references/geometry.md). Use attribute-aware simplification for suitable surfaces, structural reconstruction for important thin or analytic features, retopology and rebaking for suitable scans, and deformation-aware tools for animated assets. Point clouds require sampling and coverage checks rather than triangle decimation. Preserve selection, collision, assembly and animation semantics when required.

Optimize representative difficult regions first, then integrate under the total budget. Sweep a small number of error/ratio choices and retain the best feasible quality/cost tradeoff. Do not reach a count by discarding required parts or truncating index arrays. If constraints conflict, report measured tradeoffs and a bounded next experiment rather than silently relaxing them.

For tool selection read [upstream references](references/tool-references.md). Do not install every listed tool. `scripts/blender_candidate.py` is an opt-in static-mesh Collapse Decimate baseline for .blend/.glb/.fbx through Blender; use exact permitted object names. It rejects unsupported targets and emits an unvalidated candidate. It does not implement animation, point-cloud sampling, universal CAD reconstruction or engine asset replacement.

## Verify the actual exported candidate

Check silhouette, thickness, boundaries, contacts and local error; test UVs, materials, normals, tangents, skin/morph deformation and application semantics where applicable. Compare matched whole-object views and critical closeups. Use independent samples and holdout views; sampling maxima are not strict geometric bounds. Read [transferable lessons](references/transferable-lessons.md) when interpreting failures.

Export every required format, reimport it into a clean target environment, render it and count its actual streams. `scripts/audit_glb.py` reports declared GLB counts, not decoded compressed geometry, full validity or a vertex deduplication result. Compression, sharing, LOD and triangle reduction have distinct outcomes.

Read [performance](references/performance.md) for target runtime measurement. Record original and candidate in matched, visibly rendered conditions; retain all timed spikes and critical views. `scripts/analyze_frames.py` analyzes supplied blocks; it does not collect frames. Missing device evidence remains unverified.

## Deliver evidence and scope

Deliver candidate files/hashes, counts under explicit definitions, budgets, quality checks, runtime measurements, dependencies and unverified requirements. Use [acceptance record](assets/acceptance-record.json); null means unknown. A diagnostic pass is not full acceptance and a stricter optional diagnostic is not automatically a user rejection. Only claim acceptance for requirements supported by evidence.

For independent tool tests, unseen-asset tests and optional with/without-skill comparison read [evaluation](references/evaluation.md). For loading and command examples read [README](README.md). No particular assistant product or optional companion skill is required.
