# Hosted product contract

Recorded 2026-09-14 from the owner's stated goal and inspection of the selected forks. Product section names below are working labels.

## Objective

A user can open the platform online and perform the work they could perform by installing the selected MatrAIx and AgentSociety2 repositories locally. The platform operates the software and infrastructure for them. It exposes two separate product sections with a shared account, saved work, usage, and payment experience.

Functional parity includes the engines' user workflows and their advanced configuration/extension surfaces. It does not imply identical desktop menus or identical stochastic outputs. A browser editor or managed workbench may supply an equivalent authoring workflow where upstream expects Python, YAML, task files, terminal commands, or a VS Code extension. Those workflows remain part of the product scope.

## Initial account model

- One human owner per isolated deployment, consistent with the earlier single-user deployment decision.
- Owner login, persistent profile, saved projects, settings, provider configuration, usage ledger, credit balance or subscription entitlement, and complete run history.
- No team invitations, organization hierarchy, shared workspaces, or role administration in this first version.
- Many simulated agents, many saved projects, and resource-limited background runs are supported. Human account count and simulation population size are different settings.
- Subsequent customers can receive separate deployments. A shared multi-tenant application is outside the initial scope.

## Product sections

| Area | User outcomes |
| --- | --- |
| Persona Lab — populations | Import/browse persona datasets; inspect rich records; filter, sample, stratify, generate, contrast, and save cohorts; use the schema and available grounding/curation/validation pipelines. |
| Persona Lab — evaluations | Author or import surveys, chatbot tasks, website tasks, and supported native app tasks; choose cohorts and models; launch batches; inspect individual and aggregate outcomes. |
| Persona Lab — advanced work | Edit task definitions, instructions, inputs, verifiers, sidecars, recipes, agent configuration, adapters, and runtime options; access supported Harbor tools; export native results and reports. |
| Society Lab — societies | Configure populations, agent classes and skills, environments, reasoning routers, model roles, simulated time, and experiments; run/ask/intervene/questionnaire workflows. |
| Society Lab — research | Manage research files, literature, hypotheses, experiment configuration, datasets, analysis, and report artifacts; bring the available extension/CLI research workflows online. |
| Society Lab — inspection and extension | Inspect agents, memory, traces, replay datasets, timelines, environment data, and artifacts; develop custom skills, agents, and environment modules in the managed workspace. |
| Shared platform | Account, projects, uploads/downloads, jobs, logs, costs, billing, history, retention, export, backup, and recovery. |

## Rich-persona integration

Retain the earlier requirement that Society Lab uses rich MatrAIx personas.

1. Preserve each canonical MatrAIx record, schema version, source dataset, ID, and content hash.
2. Map persona IDs to AgentSociety2 integer agent IDs without losing the original identity.
3. Keep canonical persona traits separate from changing simulation state and event memory.
4. Adapt the current workspace-backed `PersonAgent` contract. Preserve its service proxy, memory runtime, skills, tool loop, Ray task execution, and workspace reconstruction.
5. Render relevant persona context for the current task and retain access to the full record. Do not put all schema fields into every prompt by default.
6. Round-trip identity, selected traits, memory, and simulation state through save/restart/replay.
7. Keep AgentSociety2's custom agent and environment extension mechanisms available. Rich-persona support must not silently remove other upstream capabilities.

This is an additional cross-engine feature. The bridge is not evidence that either complete product section already exists.

## Runtime design

PlatoCave owns the web application, authenticated API, durable job records, storage references, entitlement/usage accounting, and orchestration. The engines retain separate installed runtime environments and native data formats.

| Component | Responsibility |
| --- | --- |
| Web application | Two product sections, guided workflows, advanced editor/workbench, live status, results, account and billing. |
| Platform API and database | Owner/session, projects, file metadata, job state, idempotency, usage/credits, provider configuration. |
| MatrAIx adapter and worker | Calls the real installed MatrAIx/Playground/Harbor paths and collects native artifacts; routes tasks to the required compute environment. |
| AgentSociety2 adapter and worker | Launches and supervises real CLI/SDK jobs, implements browser equivalents of extension workflows, and serves v2 inspection/replay. |
| Persona bridge | Resolves canonical cohorts into workspace-backed society agents. |
| Persistent storage | Original inputs, population snapshots, tasks, workspaces, results, traces, checkpoints, and export bundles. |

Use server-side execution so closing the browser does not interrupt a job. Run source-authored code and task environments within the owner's worker boundary, separated from platform credentials and billing state. Model calls, subprocesses, Ray tasks, containers, and external environments must all be covered by job lifecycle and resource accounting.

MatrAIx has platform-specific compute paths. Web/Linux desktop tasks need the appropriate browser/container environments; macOS/iOS computer-use paths depend on the configured `use.computer` integration in the pinned code. The platform must provide those dependencies to claim that capability online. A generic Linux process alone does not cover every app target.

External provider credentials, datasets, model services, and optional research plugins remain explicit dependencies, just as they are in local usage. The platform must provision them or show a concrete missing-dependency status; it must not silently substitute an unrelated feature.

## Definition of feature completion

Each feature row requires all of the following before it is marked available online:

1. **Inputs:** the owner can provide the same meaningful inputs/configuration, including custom files/code when the engine requires them.
2. **Execution:** the real engine or equivalent supported interface executes that work with its required dependencies.
3. **Operations:** progress and failures are visible; supported stop/retry/resume behavior is correctly implemented. Resume is advertised only where state restoration is demonstrated.
4. **Outputs:** native results, relevant traces/screenshots/replay, and exports are accessible and persistent.
5. **Recovery:** browser disconnects and service restarts have tested outcomes, with interrupted work and partial artifacts represented accurately.
6. **Accounting:** usage and credit/subscription changes are durable and do not double-charge on retries or duplicate payment events.
7. **Evidence:** an end-to-end acceptance case records inputs, engine revision, environment, run ID, outcome, and artifact locations. A mock/oracle case is labeled as such and cannot certify real execution.

For each applicable workflow, compare a local reference execution with the hosted path using the same engine commit, input artifact hashes, model configuration, and seeds where supported. Compare capability and output contracts; do not require byte-identical stochastic responses.

## Initial acceptance journey

An owner signs in, creates a cohort, runs a real survey, inspects answers and cost, uses that saved cohort in a real society experiment, runs a questionnaire and intervention, opens replay, downloads the native results, signs out, and returns to the same saved history. Restarting the platform preserves the work and accounting.

This first complete journey is an implementation milestone. Full parity additionally requires every feature family in `FEATURE_PARITY.md`, including Web/app compute, custom authoring, advanced routers, research workflows, and external dependency paths. The platform is not full-parity or launch-ready merely because the first journey works.
