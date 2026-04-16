# Snowflake Semantic View Best Practices: A Complete Guide

*A comprehensive guide to building accurate, scalable semantic layers for Cortex Analyst and Snowflake Intelligence*

---

Snowflake semantic views are the bridge between your raw data and AI-powered analytics. They translate natural language questions into accurate SQL queries, enabling self-service analytics for everyone — no SQL knowledge required.

This guide covers everything from creation to optimization, drawing from internal best practices, the semantic-view Cortex Code skill, and real-world production experience.

## Table of Contents

1. [What Are Semantic Views?](#section-1)
2. [Using the semantic-view Skill in Cortex Code](#section-2)
3. [YAML Anatomy &mdash; Structure of a Semantic View](#section-3)
4. [Key Concepts &mdash; What You Can & Cannot Do](#section-4)
5. [Creation Workflow](#section-5)
6. [Sizing & Architecture](#section-6)
7. [Descriptions & Metadata &mdash; The Biggest Accuracy Lever](#section-7)
8. [Metrics, Filters & Relationships](#section-8)
9. [Verified Queries (VQRs) &mdash; 40-60% Accuracy Boost](#section-9)
10. [Custom Instructions &mdash; Last Resort](#section-10)
11. [Audit & Quality Assurance](#section-11)
12. [Debug Workflow &mdash; Fixing SQL Generation Issues](#section-12)
13. [Improvement & Optimization Loop](#section-13)
14. [Common Pitfalls & Anti-Patterns](#section-14)

---

<a name="section-1"></a>

## What Are Semantic Views?

![Introduction - What Are Semantic Views?](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/snowflake_semantic_layer_infographic_56141960bdd845a2b9771285415db160.png)

### The Semantic Layer for Cortex Analyst & Snowflake Intelligence

A Semantic View is a YAML-based metadata layer that sits between your raw Snowflake tables and Cortex Analyst — Snowflake's natural-language-to-SQL engine that powers Snowflake Intelligence.

Semantic views fix the mismatch between how business users describe data ("revenue by region") and how it's actually stored in database schemas (`TBL_SALES.AMT_TOTAL`). They define the business meaning of your data by providing:

Cortex Analyst uses these semantic views to generate accurate SQL from natural language questions. Instead of guessing column names and join paths, it understands your business concepts and generates reliable queries.

Snowflake Intelligence brings it all together: a Cortex Agent orchestrates multiple tools (Cortex Analyst for structured data, Cortex Search for documents, custom tools) to deliver end-to-end natural-language analytics inside Snowflake.

- Business context — Descriptions that explain what each table and column represents in business terms
- Relationships — How tables connect to each other through joins
- Metrics — Pre-defined calculations like Net Revenue = SUM(gross_revenue * (1 - discount))
- Filters — Common data slices like "active customers" or "last quarter"
- Examples — Sample question-answer pairs (Verified Queries) that guide the AI

> ℹ️ **Note**: What is Snowflake Intelligence? Snowflake Intelligence is Snowflake's conversational AI platform powered by Cortex Agents. It enables business users to ask questions in natural language and get instant answers from their data. Cortex Analyst is the core engine that translates these questions into SQL queries using semantic views as its guide.

> ℹ️ **Note**: OSI Standard Alignment: Snowflake semantic views follow the Open Semantic Initiative (OSI) v1.0 standard, which defines a common specification for semantic layers across the data industry. This ensures portability, interoperability, and future-proofing as the standard evolves.

### Key Benefits & Added Value

Business users query data in natural language without SQL knowledge or understanding complex schemas. Break down technical barriers and empower true self-service.

Semantic views provide the business context LLMs need to answer real-world questions reliably. Essential for Cortex Analyst and Snowflake Intelligence to generate accurate SQL.

Define metrics and business rules once in Snowflake, reuse everywhere. Eliminate "multiple versions of truth" where revenue means different things in different reports.

Native Snowflake objects inherit role-based access control, sharing, and lineage automatically. No separate semantic server to secure.

Avoid separate semantic servers, sync jobs, and duplicated logic. Change once in Snowflake, propagate everywhere—fewer moving parts, lower ops overhead.

New BI tools and AI agents plug into existing semantic views immediately. Autopilot and visual editor accelerate modeling from raw data to business-ready.

Shared contract between business and data teams. Names, definitions, and relationships are explicit and documented in one place.

BI-tool agnostic—works with Sigma, Omni, Honeydew, Power BI, and more. Standardize semantics without locking into a single tool.

**🎯 Self-Service Analytics for Everyone**

Business users query data in natural language without SQL knowledge or understanding complex schemas. Break down technical barriers and empower true self-service.

**🤖 Foundation for AI & Agentic Analytics**

Semantic views provide the business context LLMs need to answer real-world questions reliably. Essential for Cortex Analyst and Snowflake Intelligence to generate accurate SQL.

**🎓 Single Source of Truth**

Define metrics and business rules once in Snowflake, reuse everywhere. Eliminate "multiple versions of truth" where revenue means different things in different reports.

**🔒 Built-in Governance & Security**

Native Snowflake objects inherit role-based access control, sharing, and lineage automatically. No separate semantic server to secure.

**💰 Lower TCO vs External Semantic Layers**

Avoid separate semantic servers, sync jobs, and duplicated logic. Change once in Snowflake, propagate everywhere—fewer moving parts, lower ops overhead.

**🚀 Faster Time-to-Value**

New BI tools and AI agents plug into existing semantic views immediately. Autopilot and visual editor accelerate modeling from raw data to business-ready.

**🤝 Better Team Collaboration**

Shared contract between business and data teams. Names, definitions, and relationships are explicit and documented in one place.

---

<a name="section-2"></a>

## Using the semantic-view Skill in Cortex Code

![Using the semantic-view Skill](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/semantic_view_skill_use_2561f37308464a1daaa6c7b54b4e5548.png)

### What Is the semantic-view Skill?

The semantic-view skill is a bundled skill available in both Cortex Code environments:

It is the single entry point for all semantic view operations &mdash; creation, optimization, auditing, debugging, VQR generation, and more. Every best practice described in this guide is implemented as a workflow inside this skill.

- Cortex Code in Snowsight &mdash; AI assistant integrated directly into the Snowflake web UI
- Cortex Code CLI &mdash; Command-line AI assistant for local development workflows

> ℹ️ **Note**: You do not need to install anything. The skill ships with Cortex Code and is automatically invoked when you mention semantic views in your prompt.

### Getting Started with Cortex Code

**📱 Cortex Code in Snowsight**

Use Cortex Code directly in your browser within Snowflake's web UI. No installation required.

📚 Documentation: [Cortex Code in Snowsight](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-snowsight)

**💻 Cortex Code CLI**

Install the command-line version for terminal-based workflows and local development.

📚 Documentation: [Cortex Code CLI](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-cli)

### How to Invoke the Skill

Simply describe what you want in natural language. The skill triggers automatically on keywords like create, optimize, debug, audit, improve, suggest VQRs, suggest metrics, or import Tableau.

### Skill Workflow Routing

After initialization, the skill automatically routes to the right workflow based on your intent:

| Intent | Workflow | What Happens |
| Create new SV | Creation Mode | FastGen API generates YAML from your tables and SQL queries, then validates |
| Import Tableau file | Tableau Import | Analyzes .twb/.twbx/.tds/.tdsx, exports to semantic view YAML |
| Audit / check quality | Audit Mode | VQR testing, best practices verification, inconsistency & duplicate detection |
| Fix SQL generation | Debug Mode | Diagnosis &rarr; Root Cause Analysis &rarr; Apply targeted optimizations |
| Suggest VQRs | VQR Suggestions | Mines CA request history + query history in parallel, returns ranked suggestions |
| Suggest metrics / filters | Filters & Metrics Suggestions | Uses SYSTEM$CORTEX_ANALYST_SVA_TOOL to suggest metrics, filters, and computed facts from real usage |


### Prerequisites

- Cortex Code CLI installed and connected to Snowflake
- Fully qualified semantic view name for existing views: DATABASE.SCHEMA.VIEW_NAME
- Python managed via uv &mdash; the skill uses uv run python for all scripts
- Dependencies: tomli, urllib3, requests, pyyaml, snowflake-connector-python (auto-managed by uv)

---

<a name="section-3"></a>

## YAML Anatomy &mdash; Structure of a Semantic View

![YAML Anatomy](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/snowflake_yaml_anatomy_infographic_cca0da462c04490ba3352fe06abf47ad.png)

---

<a name="section-4"></a>

## Key Concepts &mdash; What You Can & Cannot Do

![Key Concepts](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/snowflake_physical_computed_infographic_a9cdffac899c40adba2cf5ac7d3b38dc.png)

### Physical vs Computed Elements

| Category | Elements | Can Add New? | Can Enhance? |
| Physical | Dimensions, Facts, Time Dimensions | No &mdash; mapped to real columns | Yes &mdash; descriptions, synonyms, sample_values |
| Computed | Metrics, Filters, Relationships, Custom Instructions | Yes | Yes |

### Logical vs Physical Table Names

> ℹ️ **Note**: Key insight: Cortex Analyst always generates SQL with physical base_table references, never logical names. This is expected and correct behavior.

---

<a name="section-5"></a>

## Creation Workflow

![Creation Workflow](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/semantic_view_creation_workflow_header_9236b474cac941da92409972ce3fcf1c.png)

### Step-by-Step Process

- Name: simple identifier or FQN (DATABASE.SCHEMA.NAME)
- Target: database + schema for the semantic view
- Context: SQL queries, table references, and business context &mdash; all in one request

> ℹ️ **Note**: FastGen API (Automated) Extracts metadata, infers PKs and relationships, generates dimensions/facts/metrics/VQRs automatically. Recommended for most use cases.

> ℹ️ **Note**: Manual Creation Hand-craft the YAML using DESCRIBE TABLE results and business knowledge. Fallback when FastGen fails.


### Deployment Options

CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML( 'DATABASE.SCHEMA', '<yaml_content>', FALSE -- FALSE = create ); Creates a managed Snowflake object. No stage needed.

CREATE STAGE IF NOT EXISTS my_stage; PUT file://model.yaml @my_stage/; Reference via stage path: @my_stage/model.yaml

**Option 1: Database Object (Recommended)**

CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML( 'DATABASE.SCHEMA', '<yaml_content>', FALSE -- FALSE = create ); Creates a managed Snowflake object. No stage needed.

---

<a name="section-6"></a>

## Sizing & Architecture

![Sizing and Architecture](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/snowflake_sizing_architecture_infographic_9cb4aa43ef614e7380b4c05810ca6661.png)

### Size Limits

---

<a name="section-7"></a>

## Descriptions & Metadata &mdash; The Biggest Accuracy Lever

![Descriptions and Metadata](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/snowflake_descriptions_metadata_banner_d27aa8dc46e64568a25217d359c1f7c4.png)

### Descriptions Have the Biggest Impact

Rich, contextual descriptions are the single most impactful thing you can do for accuracy. They outperform synonyms for English-language environments.

- name: ACCOUNT_ID description: "Account ID" expr: account_id data_type: NUMBER Minimal &mdash; just repeats the column name. Gives the LLM nothing to work with.

- name: ACCOUNT_ID description: "Unique identifier for Snowflake accounts. Used to track usage and link with customer information." expr: account_id data_type: NUMBER unique: true Rich context: what it is, how it's used, business relationships. Plus unique: true to prevent unnecessary DISTINCT.

### Description Best Practices

Every description should cover:

- What the column represents
- How it's commonly used in queries
- Relationships to other data (foreign keys, hierarchies)
- Business context (what domain it belongs to)

### Sample Values & Cortex Search

> ℹ️ **Note**: Tip: For boolean/enum-like columns, also set sample_values to help the LLM generate correct filter values.

| Distinct Values | Approach | Example |
| Fewer than 10 | Use sample_values | sample_values: ["NA", "EMEA", "APAC"] |
| More than 10 | Use Cortex Search | Auto-updating, low cost, scales to thousands |

---

<a name="section-8"></a>

## Metrics, Filters & Relationships

![Metrics, Filters and Relationships](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/snowflake_metrics_filters_relationships_banner_f7346f9e13c648b994ae67e2f7668734.png)

### Optimization Priority

When fixing SQL generation issues, apply fixes in this order:

### Metrics

Facts are raw numeric columns. Metrics are computed aggregations you can add.

### Filters

Named WHERE clauses that must be nested under the table they apply to.

tables: - name: CUSTOMERS filters: - name: ACTIVE_CUSTOMERS description: "Customers with active status and recent purchases" expr: status = 'ACTIVE' AND last_purchase_date >= DATEADD(month, -6, CURRENT_DATE()) - name: LAST_30_DAYS description: "Records from the last 30 days" expr: created_date >= DATEADD(day, -30, CURRENT_DATE()) Filters nested under tables

Simple WHERE-style expressions

Clear descriptions of when to use

Filters at the top level

HAVING clauses (use metrics instead)

Aggregation-dependent filters

---

<a name="section-9"></a>

## Verified Queries (VQRs) &mdash; 40-60% Accuracy Boost

![Verified Queries](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/snowflake_vqrs_infographic_004e6ea2bcd449c9b47d6976bf9bf44f.png)

### What Are VQRs?

Verified Query Results are question + SQL pairs that serve as few-shot examples for Cortex Analyst. When a user asks a question, the system finds the most similar VQR via cosine similarity and uses it as a template.

> ℹ️ **Note**: VQRs are excluded from the 32K token limit. You can add many VQRs without hitting size constraints.

### VQR Format & Naming

---

<a name="section-10"></a>

## Custom Instructions &mdash; Last Resort

![Custom Instructions](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/snowflake_custom_instructions_infographic_1776294873.png)

### When to Use Custom Instructions

Custom instructions are natural language guidance for the LLM. Only use them after trying all other optimization levers:


### Two Types

Targeted guidance for specific pipeline components.

module_custom_instructions: sql_generation: | Use table aliases for readability. For fiscal quarters, add 11 months before extracting quarter. question_categorization: | Treat trend questions as UNAMBIGUOUS_SQL. Legacy custom_instructions General instructions for SQL generation.

> ℹ️ **Note**: If starting fresh, prefer module_custom_instructions. If the SV already has custom_instructions, keep using that pattern for consistency.

**Recommended module_custom_instructions**

Targeted guidance for specific pipeline components.

---

<a name="section-11"></a>

## Audit & Quality Assurance

![Audit and Quality Assurance](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/snowflake_audit_quality_banner_b1ff9a2e9cb34a47b7e88e4b4e52dcb6.png)

### Three Audit Types

Test each VQR without hints. Identifies which queries fail to measure completeness.

Documentation, naming, metadata, type safety, inconsistencies, duplicates, missing relationships.

User-defined validation rules for domain-specific requirements.

### Best Practices Checks

| Check Category | What It Verifies | Severity |
| Documentation | All tables and columns have descriptions; quality/clarity | HIGH |
| Naming | No special characters; consistent conventions | MEDIUM |
| Metadata | Data types defined; synonyms used appropriately | MEDIUM |
| Type Safety | Correct dimension vs fact classification; time dimension types | HIGH |

### Inconsistency Detection

| Type | Example | Severity |
| Conflicting descriptions | order_date described differently across tables | MEDIUM |
| Data type mismatch | customer_id is NUMBER in one table, VARCHAR in another | CRITICAL |
| Orphaned relationships | Relationship references non-existent table or column | CRITICAL |
| Circular dependencies | Table A &rarr; B &rarr; C &rarr; A | HIGH |
| Contradictory filters | Filter requires both status = 'active' AND status = 'inactive' | CRITICAL |

### Duplicate Detection

Identifies when custom instructions redundantly repeat information already in model elements:

> ℹ️ **Note**: Keep information in its natural location: Descriptions in descriptions, filter logic in filters, metric logic in metrics. Custom instructions should only contain unique guidance not already in the model.

| Duplicate Type | Match Level | Resolution |
| Exact duplicate | 100% | Remove from instructions |
| High similarity | >85% | Remove from instructions |
| Partial overlap | 50-85% | Review and consolidate |

---

<a name="section-12"></a>

## Debug Workflow &mdash; Fixing SQL Generation Issues

![Debug Workflow](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/debug_workflow_infographic_4ce985a4d45c4d85b9f5e4d0e0c3b96f.png)

### Three-Step Debug Process

- Get the problematic natural language question from the user
- Generate SQL using Cortex Analyst with the current semantic view
- Execute the SQL and present results

- Compare generated SQL against expected output
- Identify gaps in the semantic model
- Present findings and recommended fixes
- Wait for user approval before applying changes

- Apply approved fixes using the optimization priority order
- Validate with reflect_semantic_model
- Re-test the problematic question
- Exact match required &mdash; no "close enough"


---

<a name="section-13"></a>

## Improvement & Optimization Loop

![Improvement and Optimization Loop](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/improvement_loop_infographic_ea8ef05c2bc24c02ad48bc1c6ce2085d.png)

### Three Improvement Approaches

AI-generated verified query suggestions based on usage patterns. Modes: ca_requests_based or query_history_based.

Automated AI analysis. Runs async (minutes). Suggests VQRs, descriptions, and structural changes.

Test existing VQRs, identify failures, fix iteratively with the debug workflow.

### Agentic Optimization Workflow


### Iterative Improvement Cycle

> ℹ️ **Note**: Small incremental changes are better than bulk updates. After each change: validate &rarr; test &rarr; verify. This makes it easy to identify which change caused a regression.


---

<a name="section-14"></a>

## Common Pitfalls & Anti-Patterns

![Common Pitfalls and Anti-Patterns](https://raw.githubusercontent.com/sfc-gh-pmanowiecki/semantic-view-best-practices/main/slides/snowflake_pitfalls_maturity_model_5bc4f2adfe8d4fea8f480f975220e391.png)

### Top 10 Mistakes to Avoid

| # | Pitfall | Impact | Fix |
| 1 | Too many columns (>100) | Performance degrades, token limit exceeded | Split by domain, keep 50-100 per SV |
| 2 | No VQRs | Missing 40-60% accuracy gain | Add VQRs for complex/ambiguous questions |
| 3 | Missing relationships in multi-table SVs | JOINs not generated, data incomplete | Add relationships with verified PKs |
| 4 | Duplicate instructions | Confusion, conflicting guidance, wasted tokens | Keep info in its natural location; audit for dupes |
| 5 | Deprecated fields (measures, default_aggregation) | Validation errors or silent failures | Use facts and metrics instead |
| 6 | Minimal descriptions | LLM can't understand column purpose | Write rich descriptions with business context |
| 7 | Custom instructions as first resort | Brittle, hard to maintain, limited to ~10 | Follow priority order: descriptions &rarr; metrics &rarr; filters &rarr; relationships &rarr; instructions |
| 8 | NOT IN conditions in generated SQL | Unexpected NULL handling | Use explicit filters or custom instructions to guide SQL patterns |
| 9 | No testing before deployment | Broken queries in production | Always validate + run VQR testing audit |
| 10 | Timestamp filtering bugs | Wrong date ranges in results | Use explicit time_dimensions; add date filters with DATEADD |

### The Semantic View Maturity Model

- IT-driven creation
- Minimal descriptions
- No VQRs
- Manual deployment

- Rich metadata
- VQRs from usage patterns
- Regular audits
- Git-based version control

- Business teams maintain SVs
- CI/CD pipelines
- Automated testing
- Agentic optimization

---

## Want More?

📊 **Interactive version**: Check out the [live presentation](https://sfc-gh-pmanowiecki.github.io/semantic-view-best-practices/semantic_view_best_practices.html) with full visual styling and navigation.

💡 **Cortex Code skill**: Use the `semantic-view` skill in Cortex Code CLI or Snowsight to automate semantic view creation, auditing, and optimization.

🔖 **Tags**: #snowflake #data-engineering #ai

