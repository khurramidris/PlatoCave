# PlatoCave

The main project repository for a single-owner hosted platform that provides the capabilities of both selected engine forks through two separate product sections.

| Section (working name) | Engine | Purpose |
| --- | --- | --- |
| Persona Lab | MatrAIx | Build populations and evaluate surveys, chatbots, websites, and applications with persona agents. |
| Society Lab | AgentSociety2 | Create and run societies, experiments, interventions, questionnaires, and research workflows. |

The product target is functional parity with using both repositories locally, including advanced configuration, custom tasks, code, and exports. One account owns each deployment. Profile, login, credits/subscription, usage, and saved history are shared across the two sections. Society simulations use MatrAIx rich personas while preserving AgentSociety2's runtime and extensibility.

## Current status

The repository was empty when inspected on 2026-09-14. This initial checkpoint contains the verified product scope, a source-based feature map, pinned engine versions, and source acquisition/inventory tooling. **It does not yet contain an implemented SaaS or a deployed service.** Source inspection is not an end-to-end execution test.

- [Product scope and acceptance criteria](docs/PRODUCT_SCOPE.md)
- [Feature parity map](docs/FEATURE_PARITY.md)
- [Code findings and implementation sequence](docs/SOURCE_FINDINGS.md)
- [Pinned engine versions](engines.lock.json)
- [Machine-readable source inventory](docs/source_inventory.json)

## Reproduce the source baseline

Python 3.11+ and Git are sufficient for these inspection commands. They do not install the engine dependencies or start model/compute jobs.

```bash
python tools/engine_sources.py sync
python tools/engine_sources.py verify
python tools/engine_sources.py inventory --output docs/source_inventory.json
```

Engine source checkouts live under `engines/` and are ignored by Git. Their exact revisions are preserved in `engines.lock.json`. The two engines will have separate runtime environments; source checkout alone does not make their services operational.

Future implementation must update the parity map with real execution evidence before describing any feature as available online.
