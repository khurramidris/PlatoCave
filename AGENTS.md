# PlatoCave project instructions

## Product contract

- Treat this repository as the authoritative application repository.
- Read `docs/PRODUCT_SCOPE.md`, `docs/FEATURE_PARITY.md`, and `docs/SOURCE_FINDINGS.md` before implementation. Check current code and Git history; documentation is not proof of functionality.
- Preserve two separate product sections and all functional capabilities in the pinned MatrAIx and AgentSociety2 forks, including advanced authoring and SDK/CLI workflows.
- Initial deployment has one human owner with login, profile, credits/subscription, usage, and history. Team and organization administration are outside this scope. This restriction does not limit the number of simulated agents.
- Society simulations use MatrAIx rich persona records while retaining AgentSociety2 memory, skills, actions, environments, clock, Ray execution, persistence, and replay. Keep custom agent/module authoring available.
- Follow the current AgentSociety2 code. The root AgentSociety frontend contains legacy API clients and is not a complete v2 frontend.
- Keep upstream repositories at explicit reviewed commits. Implement integration in PlatoCave through adapters or tracked patches; do not silently change the referenced forks.
- Do not expose raw upstream development servers publicly as a completed SaaS. All user paths, workers, files, and provider access belong to the authenticated owner's deployment.
- Keep native inputs, results, and error details available. Mock, oracle, replay-only, and genuine provider runs must remain distinguishable.

## Reporting and persistence

- State precisely which capabilities were implemented and which were exercised with real dependencies.
- A source file, successful import, unit test, or visible button is not evidence of a successful end-to-end feature.
- Commit concrete work checkpoints in this repository. Keep secrets, generated runtime data, downloaded populations, and engine dependency environments out of Git.
- Preserve source notices and attribution when adapting upstream code.
