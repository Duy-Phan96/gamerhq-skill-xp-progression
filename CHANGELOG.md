# Changelog

## 0.2.0 - 2026-10-12

- Added public host-neutral external progression signals through `progression.record-signal.v1`.
- Added replay-safe required signal dedupe keys and bounded provider/signal identifiers.
- Wired `server-booster` to `discord/server_boosted` and `first-game` to `profile/first_game_added`.
- Prevented external signals from injecting arbitrary XP, metrics or reward payloads; configured Progression rules remain authoritative.
- Added safe repeatable achievement semantics:
  - metric achievements use explicit `repeatEvery` intervals;
  - external-signal achievements repeat only for unique deduplicated events.
- Added additive `achievementCounts` and `seenSignals` member state while preserving existing storage keys.
- Kept reward bundles one-time through existing `claimedRewards` semantics even when achievement XP is repeatable.
- Added GamerHQ Host adoption handoff documentation without coupling this repository to Host internals.
- Preserved Skill ID `progression`, Runtime API `1`, existing capabilities and storage namespaces.

## 0.1.0 - 2026-10-12

- Extracted the existing GamerHQ Progression & Achievements implementation into its standalone package.
- Preserved Skill ID `progression`, Runtime API 1, Management API IDs and storage keys.
- Added configurable XP sources, deterministic levels, achievements, rewards, announcements and generic Management UI behavior.
- Added daily XP caps, bounded activity deduplication and revision-safe configuration updates.
- Added declarative `metric_at_least` achievement rules for Progression-owned metrics.
- Added Skill-owned chat cooldown enforcement while keeping raw voice-eligibility observation at the Host boundary.
- Added validated reward grant configuration and explicit role-backed `channel_access` semantics.
- Added independent package metadata, tests, contributor/security documentation and release automation.
- Added Python 3.12 / 3.14 CI and immutable SDK compatibility validation.
