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

**Status:** Active planning  
**Priority:** P1

### Objective

Complete the rule model for progression events that cannot currently be inferred from Progression-owned local metrics.

### Current gaps

- `server-booster` has no local automatic unlock source.
- `first-game` has no local automatic unlock source.
- `repeatable: true` is compatibility-reserved but intentionally has no repeated-award semantics.
- cross-Skill / Host-originated progression signals need a stable host-neutral contract before they can drive achievements safely.

### Planned design work

- define a bounded public external progression-signal contract;
- decide whether it belongs in an existing Management API or a new versioned API;
- define idempotency / dedupe requirements;
- define which signal types are Progression-owned versus external-provider-owned;
- define explicit repeatable-achievement semantics before enabling repeated XP.

No external repository may be modified from this project. If a compatible Host needs to emit a new public signal, create a handoff after the Progression-side contract is defined.

### Acceptance criteria

- external achievement triggers no longer depend on private Host knowledge;
- replay-safe/idempotent signal semantics are defined;
- existing Runtime API 1 and storage compatibility are preserved where practical;
- repeatability cannot create ambiguous or uncontrolled repeated XP;
- tests cover all approved public behavior.

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
