# Source-based feature parity map

Baseline: AgentSociety2 `670c94fff7c64c4f79b632125f2ccf968155e746`; MatrAIx `3633d8dab149a9482a71b024418a49ae828cc941`.

**Status on 2026-09-14:** all hosted capabilities below are pending implementation. Source existence was inspected; upstream execution and hosted end-to-end operation were not certified in this checkpoint. These are feature families, not a claim that endpoint count equals product completeness. The generated `source_inventory.json` lists additional static entry points and authoring surfaces so they can be expanded into acceptance cases.

## Persona Lab

Paths in this table are relative to the pinned MatrAIx repository.

| ID | Capability family | Observed source | Required hosted surface |
| --- | --- | --- | --- |
| M01 | Persona schema and rich record inspection | `persona/schema/dimensions.json`; `application/playground/backend/api/app.py` persona-pool and persona-detail routes | Browse/search full records and labels; preserve all 1,290 schema dimensions. |
| M02 | Dataset discovery and saved populations | `application/playground/backend/service/persona_pool_service.py` | Import/populate dataset storage, list datasets, save pools and cohorts, reopen them. |
| M03 | Filtered and stratified sampling | `application/playground/backend/service/persona_pool_service.py` (`sample_pool`) | Expose filters, allocation, sizes, seeds and cohort persistence. |
| M04 | Synthetic population generation | `src/matraix/persona_generator.py`; `application/playground/backend/service/persona_pool_service.py` (`generate_synthetic_pool`) | Run the DAG generation path, show progress, preserve generated records and settings. |
| M05 | Contrast populations, overlays and task-aware selection | `application/playground/backend/api/app.py` contrast/attribute-match/persona-strategy routes; `application/playground/backend/service/persona_pool_service.py` | Configure comparison arms and attributes, inspect selected populations, preserve strategies. |
| M06 | Grounding, extraction and curation pipelines | `persona/human_extraction/scripts/run_extraction_api.py`; `persona/curation/existing_data/scripts/run_pipeline.py`; `persona/existing_data_curation/scripts/` | Managed file/code workflow with explicit data inputs, provider settings, outputs and evidence. |
| M07 | Persona quality/consistency validation and reports | `persona/synthesis/scripts/audit_quality.py`; `persona/synthesis/scripts/audit_consistency.py`; `persona/validation/scripts/` | Run chosen checks and matrices, inspect failures, export reports. |
| M08 | Survey evaluation | `environment/agents/matraix/agents/persona/json_survey.py`; `application/tasks/example-survey_product-feedback/` | Author/import questionnaire task, choose cohort/model, run real batch, inspect response and verifier outputs. |
| M09 | Chatbot evaluation | `environment/agents/matraix/agents/persona/user_sim.py`; `application/tasks/example-chat-api_support_chatbot/` | Configure chatbot target/task and sidecars, run conversations, view transcripts, debrief and scores. |
| M10 | Website evaluation | `environment/agents/matraix/agents/persona/browser_use.py`; `environment/agents/matraix/agents/persona/cocoa.py`; `application/tasks/example-web-playwright_quote-choice/` | Browser-backed tasks with target/task authoring, trajectories, screenshots and native artifacts. |
| M11 | Linux desktop application tasks | `environment/agents/matraix/agents/persona/computer_1.py`; `application/tasks/example-computer-use-linux_note-to-csv/` | Run the Linux computer-use environment and expose screenshots, recordings and verification. |
| M12 | macOS/iOS application tasks | `environment/agents/matraix/agents/persona/computer_1.py`; `environment/runtime/harbor/environments/use_computer.py` | Configure the supported external environment and agent dependencies; retain platform-specific submission behavior. |
| M13 | Task authoring and verification | `application/tasks/`; `application/task-spec/`; `environment/runtime/harbor/cli/tasks.py` | Edit/import task.toml, instructions, inputs, verifiers, task persona strategies and environment files. |
| M14 | Job recipes, batch execution and failed-trial retry | `src/matraix/cli.py`; `application/scripts/generate_application_job.py`; `application/playground/backend/service/harbor_job_service.py` | Recipe/config workflow, background execution, progress, failure detail, failed-trial retry and lifecycle supervision. |
| M15 | Live and completed run inspection | `application/playground/backend/api/app.py` Harbor job/trial routes | Job/trial detail, live status, traces, events, screenshots, recordings, instructions and debrief. |
| M16 | Aggregate findings and exports | `src/matraix/job_results.py`; `application/playground/backend/service/report_pdf.py` | Aggregate/subgroup results, native artifacts, JSON/CSV outputs, trial and batch PDFs. |
| M17 | Agent/model and runtime configuration | `environment/agents/`; `packages/playground/src/playground/remote_runner/`; `environment/runtime/harbor/environments/`; `pyproject.toml` extras | Preserve supported agents/providers and local/remote/cloud runtime options, with explicit dependency checks. |
| M18 | Advanced Harbor operations and viewer | `environment/runtime/harbor/cli/main.py`; `environment/runtime/harbor/cli/`; `apps/viewer/` | Managed access to task/dataset/job/trial tools, adapters, sweeps, checks, analysis, trace tools, cache and supported registry integrations. |

## Society Lab

Paths in this table are relative to the pinned AgentSociety repository. Scope is AgentSociety2, not the legacy v1 package.

| ID | Capability family | Observed source | Required hosted surface |
| --- | --- | --- | --- |
| S01 | Research workspace and file lifecycle | `extension/src/`; `packages/agentsociety2/agentsociety2/society/workspace.py`; `extension/package.json` | Projects, research files, JSON/YAML/CSV/Markdown editors/viewers, workspace import/export. |
| S02 | Agent population configuration | `packages/agentsociety2/agentsociety2/society/models.py`; `packages/agentsociety2/agentsociety2/agent/person.py` | Agents/profile/config editing with canonical rich-persona selection, ID validation and saved inputs. |
| S03 | Environment modules | `packages/agentsociety2/agentsociety2/contrib/env/`; `packages/agentsociety2/agentsociety2/backend/routers/modules.py` | Discover and configure social, economic, mobility, event, information and experimental environments. |
| S04 | Reasoning routers | `packages/agentsociety2/agentsociety2/env/__init__.py`; router implementations in that directory | Support CodeGen, ReAct, PlanExecute, TwoTierReAct, TwoTierPlanExecute and SearchTool through appropriate SDK/runner paths. |
| S05 | Run, ask, intervention and questionnaires | `packages/agentsociety2/agentsociety2/society/models.py`; `packages/agentsociety2/agentsociety2/society/cli.py` | Timeline/config authoring and real background execution, answer/intervention/questionnaire artifacts. |
| S06 | Resume, workspaces and agent persistence | `packages/agentsociety2/agentsociety2/society/cli.py`; `packages/agentsociety2/agentsociety2/society/society.py`; `packages/agentsociety2/agentsociety2/agent/person.py` | Preserve native state and checkpoints; certify restart/resume semantics with actual engine runs. |
| S07 | Replay, datasets, agent and timeline inspection | `packages/agentsociety2/agentsociety2/backend/routers/replay.py`; `extension/src/webview/replay/ReplayApp.tsx` | Port v2 replay webviews to browser transport, preserving dataset-driven views. |
| S08 | Native artifacts, traces and analysis access | `packages/agentsociety2/agentsociety2/backend/routers/experiments.py`; `packages/agentsociety2/agentsociety2/trace/`; `packages/agentsociety2/agentsociety2/storage/` | Browse/download raw outputs and query the current replay/trace formats. |
| S09 | Agent skills | `packages/agentsociety2/agentsociety2/backend/routers/agent_skills.py`; `packages/agentsociety2/agentsociety2/agent/skills/` | List, create, import, upload and configure skills with persistent skill files/state. |
| S10 | Custom agents and environment modules | `packages/agentsociety2/agentsociety2/backend/routers/custom.py`; `packages/agentsociety2/agentsociety2/registry/` | Author/import Python modules, scan/register/test them, inspect errors, run them in the owner's worker boundary. |
| S11 | Literature, hypotheses and experiment design | `extension/skills/agentsociety-literature-search/`; `extension/skills/agentsociety-hypothesis/`; `extension/skills/agentsociety-experiment-config/`; `extension/skills/agentsociety-research-pipeline/` | Browser equivalents of research workflows backed by their real tools and workspace files. |
| S12 | Agent, dataset and environment authoring workflows | `extension/skills/agentsociety-create-agent/`; `extension/skills/agentsociety-create-dataset/`; `extension/skills/agentsociety-use-dataset/`; `extension/skills/agentsociety-create-env-module/` | Make assisted and manual authoring available; execute and preserve generated work. |
| S13 | Analysis harness and reports | `packages/agentsociety2/agentsociety2/skills/analysis/harness/`; `extension/src/analysisHarnessStatusViewer.ts`; `extension/skills/agentsociety-analysis/` | Run the analysis phases/tools, show validation state, and expose charts/report bundles. |
| S14 | Model, service and research-tool integrations | `packages/agentsociety2/agentsociety2/config/`; `extension/src/webview/configPage/`; `extension/skills/agentsociety-paper-review/` | Default/coder/embedding roles, research tool configuration, and supported external plugin workflows. Verify external tools separately. |

The environment inventory currently finds 16 direct built-in `EnvBase` subclasses. This is a source count, not a tested capacity or an exhaustive list of extensions. All six exported router types are in scope, although the standard CLI initializes CodeGenRouter; supporting the others requires an SDK execution path or a deliberate runner change.

## Shared and cross-engine features

| ID | Capability | Completion requirement |
| --- | --- | --- |
| P01 | Single-owner account | Login, session lifecycle, persistent profile, one-owner provisioning. |
| P02 | Billing and usage | Credits/subscription, durable usage ledger, idempotent payment events, reservation/settlement, failed/interrupted-run handling. |
| P03 | Durable jobs and storage | Server-side execution, logs/events, inputs/outputs, disconnect tolerance, cancellation/termination handling, tested recovery. |
| P04 | Rich-persona bridge | Canonical record/ID/schema/hash preservation, task-aware context, current PersonAgent integration, memory and state round-trip. |
| P05 | Hosted authoring and export | Guided controls plus advanced files/code/SDK access, custom dependency environments, native export and restore. |

Implementation must split these families into individual acceptance cases as needed. Features discovered later in the pinned source inventory remain in scope; this family-level table is not permission to omit them.
