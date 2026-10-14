# Roadmap

This roadmap records the strategic direction of the independently owned XP & Progression Skill. GitHub Issues remain the operational task tracker; this file documents outcomes, scope and milestone intent.

## Product direction

Progression is a portable GamerHQ-compatible Skill that owns XP rules, levels, achievements, rewards, Skill-owned state and generic management contracts.

The Skill remains host-neutral. Host-specific Discord observation, event lifecycle logic and production deployment stay outside this repository.

## Released baseline

### v0.1.0 — Standalone baseline

**Status:** RELEASED  
**Release commit:** `f32d27815b52a5a3cb94c4632904fd5692d3ffd4`

Delivered:
- standalone Python package and `gamerhq.skills` entry point
- stable Skill ID `progression`
- Runtime API `1`
- SDK compatibility `>=0.1,<0.2`
- stable storage keys `config.v1` and `member.v1:<member-id>`
- configurable XP sources, levels, achievements, rewards and announcements
- declarative local achievement rules
- chat cooldown enforcement and explicit Host voice-observation boundary
- validated reward grants and role-backed channel access semantics
- generic Management UI Schema
- bounded activity deduplication and daily XP caps
- Python 3.12 / 3.14 CI
- release artifacts, source distribution and SHA-256 checksums
- contributor and security guidance

## Milestone 1 — Standalone baseline

**Status:** Completed

### Outcome

Progression is independently versioned, released and consumable by a compatible Host without depending on a moving branch.

## Milestone 2 — Progression interoperability & rule completeness

**Status:** Completed  
**Priority:** P1

### Objective

Complete the rule model for progression events that cannot currently be inferred from Progression-owned local metrics.

### Current gaps

- public external signals are implemented through `progression.record-signal.v1`;
- `server-booster` maps to `discord/server_boosted`;
- `first-game` maps to `profile/first_game_added`;
- repeatable achievements have explicit safe semantics;
- GamerHQ `develop` now emits the public signals through the reviewed Host adapter.

### Completed design work

- dedicated `progression.record-signal.v1` contract;
- bounded provider/signal identifiers;
- required replay-safe dedupe keys;
- explicit external-signal achievement conditions;
- explicit metric `repeatEvery` semantics;
- repeatable external signals once per unique deduplicated event.

### Downstream adoption

GamerHQ adopted the released 0.2 contract through PR #148, merged to `develop` as `f2c237dd76133484e9a2f70ea8161c8a573b2100`.

The Host:
- pins Progression v0.2.0 immutably;
- emits `discord/server_boosted`;
- emits `profile/first_game_added`;
- preserves replay-safe dedupe keys;
- treats missing/disabled Progression as non-fatal.

This verifies the public contract against the reference Host. Production deployment remains a separate GamerHQ release decision.

### Acceptance criteria

- [x] external achievement triggers do not depend on private Host knowledge;
- [x] replay-safe/idempotent signal semantics are defined;
- [x] Runtime API 1 and storage compatibility are preserved;
- [x] repeatability is bounded and explicit;
- [x] tests cover approved public behavior;
- [x] downstream Host adoption is verified in GamerHQ `develop`.

### 0.2.0 — Interoperability & repeatability

**Status:** RELEASED / reference Host integration verified

Scope:
- public external signal API;
- booster and first-game external achievement mappings;
- replay-safe signal dedupe;
- safe repeatable metric and external-signal achievements;
- additive occurrence tracking;
- optional GamerHQ Host adoption handoff.

Downstream Host adoption is not a release gate.

## Milestone 3 — Developer and operator usability

**Status:** Planned  
**Priority:** P2

### Objective

Make configuration easier to understand, validate and adopt for third-party operators.

### Candidate outcomes

- example configurations for common community setups;
- clearer management schema descriptions for achievement conditions and rewards;
- compatibility examples for Host integrators;
- release upgrade notes when 0.2.0 is prepared.

## Future opportunities

Only pursue with demonstrated user value:
- leaderboards
- seasons or prestige
- configuration presets
- richer analytics
- Marketplace metadata
- additional public cross-Skill events

These are not committed requirements.

## Out of scope

This repository does not own:
- GamerHQ Host internals
- Discord Gateway observation
- event lifecycle implementation
- gamerhq-web
- Marketplace backend
- Skill installation infrastructure
- production VPS deployment
- Runtime / SDK implementation owned by another repository

When another repository must change, Progression defines the public requirement and creates a handoff rather than modifying that repository directly.
