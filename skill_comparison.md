# Comparison: `semantic_view_optimization_skill` vs `semantic-view` (Cortex Code)

## Overview

| Aspect | `semantic_view_optimization_skill` (Desktop bundled) | `semantic-view` (Cortex Code CLI) |
|--------|------|------|
| **Location** | `snowflake-coco-desktop/resources/snowflake/skills/` | `Documents/skills/semantic-view/` |
| **File structure** | Nested directories (`audit/`, `debug/`, `optimization/`, etc.) | Flat files with `_` prefix naming (`audit_SKILL.md`, `debug_SKILL.md`, etc.) |
| **Total doc files** | 30 | 42 |
| **Total scripts** | 17 | 18 |
| **Skill name** | `semantic-view-optimization` | `semantic-view` |

---

## Workflow Routing

| Workflow | `semantic_view_optimization_skill` | `semantic-view` |
|----------|------|------|
| **Entry routing** | NEW vs EXISTING (Audit/Debug) | NEW vs IMPORT vs EXISTING vs VQR SUGGESTIONS vs FILTERS & METRICS |
| **Creation** | Yes (FastGen + fallback) | Yes (FastGen + fallback) |
| **Audit** | Yes (VQR testing, Best Practices, Custom Criteria) | Yes (same 3 types + SVA VQR compile check) |
| **Debug** | Yes (Diagnosis, Root Cause, Optimization) | Yes (same 3 steps) |
| **VQR Suggestions** | No dedicated workflow | Yes - `vqr_suggestions_SKILL.md` (dedicated parallel script) |
| **Filters & Metrics Suggestions** | No | Yes - `filters_and_metrics_suggestions_SKILL.md` (via `SYSTEM$CORTEX_ANALYST_SVA_TOOL`) |
| **Tableau Import** | No | Yes - `import_tableau_SKILL.md` (.twb/.twbx/.tds/.tdsx) |
| **SVA VQR Compile Check** | No | Yes - `reference_sva_validate_verified_queries.md` (bulk + inline modes) |
| **SVA Expand/Truncate SQL** | No | Yes - `reference_sva_expand_truncate_verified_query.md` |

---

## Sub-Skills & Documents

### Creation

| Document | `semantic_view_optimization_skill` | `semantic-view` |
|----------|------|------|
| `creation/SKILL.md` | Yes | Yes |
| `creation/fastgen_workflow.md` | Yes | Yes |
| `creation/fallback_creation.md` | Yes | Yes |
| `creation/primary_keys_and_relationships.md` | Yes | Yes |
| `creation/fastgen_request_spec.md` | No | Yes (added) |

### Audit

| Document | `semantic_view_optimization_skill` | `semantic-view` |
|----------|------|------|
| `audit/SKILL.md` | Yes | Yes |
| `audit/vqr_testing/SKILL.md` | Yes | Yes |
| `audit/vqr_testing/vqr_evaluation.md` | Yes | Yes |
| `audit/vqr_testing/vqr_extraction.md` | Yes | Yes |
| `audit/vqr_testing/results_formatting.md` | Yes | Yes |
| `audit/best_practices/SKILL.md` | Yes | Yes |
| `audit/best_practices/inconsistencies.md` | Yes | Yes |
| `audit/best_practices/duplicates.md` | Yes | Yes |
| `audit/best_practices/missing_relationships.md` | Yes | Yes |
| `audit/best_practices/results_formatting.md` | Yes | Yes |
| `audit/custom_criteria/SKILL.md` | Yes | Yes |
| `audit/custom_criteria/results_formatting.md` | Yes | Yes |

### Debug

| Document | `semantic_view_optimization_skill` | `semantic-view` |
|----------|------|------|
| `debug/SKILL.md` | Yes | Yes |
| `debug/issue_diagnosis.md` | Yes | Yes |
| `debug/root_cause_analysis.md` | Yes | Yes |
| `debug/optimization_application.md` | Yes | Yes |

### Optimization Patterns

| Document | `semantic_view_optimization_skill` | `semantic-view` |
|----------|------|------|
| `optimization/SKILL.md` | Yes | Yes |
| `optimization/dimension_optimization.md` | Yes | Yes |
| `optimization/metric_optimization.md` | Yes | Yes |
| `optimization/filter_optimization.md` | Yes | Yes |
| `optimization/relationship_optimization.md` | Yes | Yes |
| `optimization/custom_instructions.md` | Yes | Yes |

### Reference

| Document | `semantic_view_optimization_skill` | `semantic-view` |
|----------|------|------|
| `reference/semantic_view_concepts.md` | Yes | Yes |
| `reference/semantic_view_get.md` | Yes | Yes |
| `reference/semantic_view_set.md` | Yes | Yes |
| `reference/sql_comparison.md` | Yes | Yes |
| `reference/eval_sql_pair.md` | Yes | Yes |
| `reference/get_cortex_analyst_events.md` | Yes | Yes |
| `reference/get_vqr_suggestions.md` | Yes | Yes |
| `reference/sva_validate_verified_queries.md` | No | Yes (added) |
| `reference/sva_expand_truncate_verified_query.md` | No | Yes (added) |
| `reference/tableau_tool_reference.md` | No | Yes (added) |

### Other

| Document | `semantic_view_optimization_skill` | `semantic-view` |
|----------|------|------|
| `setup/SKILL.md` | Yes | Yes |
| `validation/SKILL.md` | Yes | Yes |
| `upload/SKILL.md` | Yes | Yes |
| `time_tracking/SKILL.md` | Yes | Yes |
| `time_tracking/agent_tracking_pattern.md` | Yes | Yes |
| `vqr_suggestions/SKILL.md` | No | Yes (added) |
| `filters_and_metrics_suggestions/SKILL.md` | No | Yes (added) |
| `import_tableau/SKILL.md` | No | Yes (added) |

---

## Scripts

| Script | `semantic_view_optimization_skill` | `semantic-view` |
|--------|------|------|
| `semantic_view_get.py` | Yes | Yes |
| `semantic_view_set.py` | Yes | Yes |
| `semantic_view_sql_utils.py` | Yes | Yes |
| `sf_connection_utils.py` | Yes | Yes |
| `download_semantic_view_yaml.py` | Yes | Yes |
| `upload_semantic_view_yaml.py` | Yes | Yes |
| `eval_sql_pair.py` | Yes | Yes |
| `extract_table_metadata.py` | Yes | Yes |
| `extract_vqrs.py` | Yes | Yes |
| `generate_semantic_model_fastgen.py` | Yes | Yes |
| `get_cortex_analyst_events.py` | Yes | Yes |
| `get_vqr_suggestions.py` | Yes | Yes |
| `infer_primary_keys.py` | Yes | Yes |
| `relationship_creation.py` | Yes | Yes |
| `remove_vqrs.py` | Yes | Yes |
| `time_tracker.py` | Yes | Yes |
| `track_agent_task.py` | Yes | Yes |
| `tableau_export_yaml.py` | No | Yes (added) |

---

## Setup & Initialization Differences

| Aspect | `semantic_view_optimization_skill` | `semantic-view` |
|--------|------|------|
| **Prerequisites** | Load `semantic_view_concepts.md` + `semantic_view_get.md` | Same |
| **Environment checks** | Not explicit | Explicit: checks `uv`, Python packages, Snowflake config |
| **Directory naming** | `semantic_view_optimization_{TIMESTAMP}/` | `semantic_view_{TIMESTAMP}/` |
| **Variables tracked** | `WORKING_DIR` | `SKILL_BASE_DIR`, `BASE_WORKING_DIR`, `WORKING_DIR` |

---

## SKILL.md Description Scope

| Aspect | `semantic_view_optimization_skill` | `semantic-view` |
|--------|------|------|
| **Trigger keywords** | create, build, debug, fix, troubleshoot, optimize, improve, analyze | Same + VQR suggestions, verified queries, seeding queries, suggesting metrics/filters, enriching |
| **Self-description** | "Entry point for all semantic view workflows" | "REQUIRED entry point" for all SV requests including VQR + metric/filter suggestions |

---

## Summary of Unique Features

### Only in `semantic-view` (Cortex Code CLI)

| Feature | Description |
|---------|-------------|
| **VQR Suggestions workflow** | Dedicated skill with parallel `ca_requests_based` + `query_history_based` modes, `fast`/`slow` speed options |
| **Filters & Metrics Suggestions** | Mines query history via `SYSTEM$CORTEX_ANALYST_SVA_TOOL` to suggest metrics, filters, and computed facts |
| **Tableau Import** | Full import pipeline for `.twb`/`.twbx`/`.tds`/`.tdsx` with published datasource support, custom SQL handling, worksheet filtering |
| **SVA VQR Compile Check** | Bulk and inline `validate_verified_queries` via `SYSTEM$CORTEX_ANALYST_SVA_TOOL` |
| **SVA Expand/Truncate SQL** | Convert between semantic (logical) and physical SQL for verified queries |
| **FastGen Request Spec** | Detailed JSON schema documentation for `SYSTEM$CORTEX_ANALYST_FAST_GENERATION` |
| **`tableau_export_yaml.py`** | Script for exporting Tableau files to semantic view YAML |
| **Explicit environment checks** | Setup verifies `uv`, Python packages, and Snowflake config before proceeding |

### Only in `semantic_view_optimization_skill` (Desktop)

| Feature | Description |
|---------|-------------|
| (None unique) | All capabilities are a subset of `semantic-view` |
