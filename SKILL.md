---
name: mesh-optimize-verified
license: MIT
description: Use when reducing polygon or vertex counts in FBX, GLB, Blender or Unity models, especially CAD/PCB assemblies with holes, thin pins, hard normals, part interactions, tight resource budgets or frame-time regressions. 适用于模型降面、减点、保形与帧率验证。
metadata:
  version: "0.1.1"
---

# Verified mesh optimization / 可验证的模型降面减点

Optimize an isolated copy to the user's actual geometry, appearance, runtime and format requirements. A smaller file or fewer triangles does not establish preserved appearance or stable frame delivery. This is a portable instruction/tool package, not trained model weights or a universal zero-drop guarantee.

## Start with the actual contract

Inspect available assets, existing approvals and target importer. Record units, transform/pivot, required formats, render pipeline/device, interaction parts, budgets and viewing distance. Reuse explicit choices; ask only for essential missing decisions. Continue offline inspection if the final teaching/XR project is unavailable. Read [workflow](references/workflow.md) for counting, preservation, tool choice and delivery.

Freeze source/dependency hashes. Separate input, experiments and reviewed releases; never overwrite the original or a frozen candidate. Run an unchanged import/export roundtrip before attributing reductions to optimization. Count source control points, rendering vertices, triangles, unique assets, scene instances and primitive references separately.

## Select a small, measurable experiment

Read [geometry and representation](references/geometry.md). Classify planar bodies, curved shells, thin pins, holes, embossed labels and interaction boundaries. Use constrained simplification for suitable surfaces; rebuild structural cross-sections when QEM loses a feature. Retain attributes at shared positions. Account for the full assembly budget before integrating a local repair.

For an opt-in Blender baseline, use `scripts/blender_candidate.py --help` **through Blender**, with exact permitted object names. It produces an unvalidated candidate; it is not the advanced PCB pipeline. For native Unity assets use the engine's mesh streams, not the generic Blender helper. Geometry-replacing shader techniques require independent closeup, depth, shadow, platform and performance checks and separate standard-format exports.

## Validate the candidate you actually deliver

Use fixed whole-object and feature closeups at matched camera/light/material settings; inspect silhouette, holes, thickness, pins, normals, contacts and required interaction. Distinguish sampling diagnostics, user acceptance and untested coverage. Use `python scripts/audit_glb.py MODEL.glb --out NEW.json` for **declared** GLB counts, then reimport to validate actual streams. It does not decode compressed geometry or prove GLB validity.

Read [performance](references/performance.md) before collecting or interpreting frames. Profile both full assembly and critical closeups on the target Player/device. Keep every timed spike; compare each session/view, preserve block boundaries. `python scripts/analyze_frames.py --help` analyzes supplied raw blocks; it does not collect frames or verify that rendering happened.

## Report the evidence, including gaps

Output: candidate paths/hash and representation; per-format counts/budget headroom; geometry/image evidence; performance measurement type/settings/raw samples/results; fresh-import dependencies; remaining gaps/next bounded experiment. Use [acceptance record](assets/acceptance-record.json) for machine-readable status. `null` means unknown. A diagnostic failure is not automatically user rejection; a diagnostic pass is not automatically full acceptance. Do not invent teacher thresholds, universal feasibility proofs or completed tests.

For transferable PCB lessons and historical results read [project casebook](references/project-casebook.md). For external libraries and optional existing skills read [tool references](references/tool-references.md). For independent DeepSeek A/B, tool and unseen-model tests read [evaluation](references/evaluation.md). Start-up and copying into other AI products: [README](README.md).
