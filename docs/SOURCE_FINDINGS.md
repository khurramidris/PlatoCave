# Source findings and delivery sequence

Inspection date: 2026-09-14. The selected fork commits are in `engines.lock.json`.

## Verified current state

PlatoCave had no commits or files at inspection. Both engine forks were cloned and their checked-out commits verified. This checkpoint creates the product contract and reproducible source baseline; the hosted application, billing, integration workers, and persona bridge have not been implemented here.

Inspection covered actual API route registration/handlers, CLI execution steps, persona generation service, computer-use dispatch, remote worker dispatch, agent lifecycle, frontend API consumers, extension commands/webviews, and research/advanced source entry points. It was not an exhaustive line-by-line audit or a runtime certification.

## Findings that change implementation

### 1. AgentSociety's root frontend is not a complete v2 SaaS frontend

The root frontend includes pages that call `/api/run-experiments`, `/api/llm-configs`, `/api/agent-configs` and other legacy endpoints. The v2 backend registers a different, narrower set of routes for experiment information/artifacts, replay, modules, skills, custom modules and prefill parameters. The v2 experiment router does not supply a run-creation endpoint.

Evidence:

- `frontend/src/pages/Experiment/CreateExperiment.tsx`
- `frontend/src/pages/Console/index.tsx`
- `packages/agentsociety2/agentsociety2/backend/app.py`
- `packages/agentsociety2/agentsociety2/backend/routers/experiments.py`
- `extension/src/webview/replay/ReplayApp.tsx`

Consequence: create PlatoCave's v2 execution interface and adapt the actual v2 extension webviews. Hosting the existing root frontend against the v2 backend would leave core controls unconnected.

### 2. AgentSociety2 capability extends beyond its HTTP API

The CLI executes `run`, `ask`, `intervene`, and `questionnaire` steps. The SDK exposes multiple router implementations; the standard CLI constructs the CodeGen environment-router actor. Research workflows and file/editor operations are also distributed across the extension and its skills.

Evidence:

- `packages/agentsociety2/agentsociety2/society/cli.py`
- `packages/agentsociety2/agentsociety2/society/models.py`
- `packages/agentsociety2/agentsociety2/env/__init__.py`
- `extension/package.json`
- `extension/skills/`

Consequence: an HTTP reverse proxy alone cannot deliver all v2 capabilities. Add durable CLI/SDK execution and browser authoring/research interfaces.

### 3. MatrAIx Playground is a substantial starting point, but does not cover the whole repository

The Playground API exposes dataset/persona/cohort operations, generation/sampling/contrast, task catalogs, job execution/retry and rich trial/result views. The source also contains task authoring, extraction/curation/validation scripts, Harbor operations, environment providers, and an additional viewer.

Evidence:

- `application/playground/backend/api/app.py`
- `application/playground/backend/service/persona_pool_service.py`
- `src/matraix/cli.py`
- `environment/runtime/harbor/cli/main.py`
- `persona/`

Consequence: reuse the working surfaces through adapters, and expose the remaining source-level workflows in an advanced browser workbench. Catalog examples alone are insufficient; users must be able to bring their own tasks.

### 4. Runtime parity requires the corresponding execution environments

`computer_1.py` selects Docker computer-use, use.computer desktop, or iOS agents according to the environment. Optional extras install these integrations. Ray remains part of AgentSociety2. These are runtime dependencies that must be provisioned and tested.

Evidence:

- MatrAIx `environment/agents/matraix/agents/persona/computer_1.py`
- MatrAIx `environment/runtime/harbor/environments/use_computer.py`
- MatrAIx `pyproject.toml`
- AgentSociety2 `packages/agentsociety2/agentsociety2/society/cli.py`
- AgentSociety2 `packages/agentsociety2/agentsociety2/agent/runner.py`

Consequence: maintain a feature-to-runtime readiness matrix. An unconfigured dependency is a blocked feature, not a successful simulation. Native macOS/iOS support is not established by a Linux Docker smoke test.

### 5. Engine job state and spend controls are not sufficient SaaS accounting

MatrAIx's product CLI documents its `MATRIX_MAX_COST_USD` gate for the host Survey/Chat paths; this does not establish a global prepaid budget enforcement mechanism across every execution backend. Its Harbor job service uses process-local tracking/executor state alongside native files. The legacy remote web path can return deterministic mock artifacts if no command is configured; the general `harbor_job` path dispatches differently.

Evidence:

- `src/matraix/cli.py`
- `application/playground/backend/service/harbor_job_service.py`
- `packages/playground/src/playground/remote_runner/server.py`

Consequence: PlatoCave must own durable job identity, status reconciliation, ledger entries, and worker supervision. Preserve native run semantics; never count a legacy mock response as real website execution. Cancellation, recovery and accounting require execution tests, not just inspection of status fields.

### 6. The rich-persona bridge must match the current agent lifecycle

The inspected `PersonAgent` is workspace-backed and restores itself with an injected service proxy. It inherits generic tools/skills/workspace behavior from `AgentBase`, and builds a separate person memory runtime. A bridge built against an older long-lived actor design would not match this code.

Evidence:

- `packages/agentsociety2/agentsociety2/agent/person.py`
- `packages/agentsociety2/agentsociety2/agent/base/`
- `packages/agentsociety2/agentsociety2/agent/runner.py`
- `packages/agentsociety2/agentsociety2/society/society.py`

Consequence: retain the current lifecycle and introduce canonical persona loading/context selection at its supported extension points. Test save/reconstruction and mutable memory separately from persona identity.

## Implementation sequence

These are future implementation milestones, not completed work.

| Order | Deliverable | Required evidence |
| --- | --- | --- |
| 1 | Single-owner platform application, sessions, projects, persistent files and durable job records; separate engine runtime builds pinned to this baseline. | Owner can sign in, save/reopen a project; runtimes start and expose accurate dependency readiness; persistence survives restart. |
| 2 | Real MatrAIx cohort and survey flow; real AgentSociety2 run/ask/intervene/questionnaire flow; native results and v2 replay. | Execute both through the browser using real providers and retrieve their native outputs. |
| 3 | Rich-persona bridge and shared cohort selection. | One saved cohort becomes society agents with preserved identity, persona context, memory and restart/replay behavior. |
| 4 | Remaining MatrAIx chat/web/Linux/macOS/iOS paths, tasks/recipes, cohort generation/contrast, and result views. | Real end-to-end case per supported runtime, plus custom task authoring and exports. |
| 5 | Complete Society Lab environment/router/skill/module controls and browser research workflow. | All built-in environment/router families have execution coverage; custom module/skill and research cases complete. |
| 6 | Full advanced workbench for source-level persona, Harbor, SDK/CLI, dataset and authoring workflows. | An owner can perform the documented local reference tasks online and export equivalent inputs/artifacts. |
| 7 | Payment integration, ledger/budget enforcement across runtimes, operational recovery and deployment packaging. | Payment retry/idempotency, interrupted run reconciliation, backup/restore, and clean deployment acceptance cases pass. |
| 8 | Feature-by-feature release review. | Every required acceptance case has real evidence or a clearly identified unresolved dependency. Full parity is claimed only after all required cases pass. |

Billing/accounting architecture and recovery behavior must be designed at milestone 1, then exercised and completed as execution backends and payments are connected. Milestone order does not permit retrofitting ownership or usage semantics after the runners are built.

## Validation performed for this checkpoint

- GitHub confirmed the application repository was empty and both engine fork heads were accessible.
- Local Git checkouts matched the pinned commit hashes.
- Static source inspection and reproducible inventory generation were performed without installing or executing engine services.
- No model calls, paid compute jobs, hosted application tests or payment flows were run.
- No hosted capability is marked complete.

An existing `feat/allegory-micro-society-v0.1` branch was observed in the AgentSociety fork. GitHub reports it diverged from the selected main revision (26 commits ahead, 12 behind), with micro-society example/UI additions. It was not merged, treated as a completed SaaS, or used as the baseline for this contract.
