# Roadmap

This roadmap records the strategic direction of the independently owned XP & Progression Skill. GitHub Issues should remain the operational task tracker; this file documents outcomes, scope and milestone intent.

## Product direction

Progression is a portable GamerHQ-compatible Skill that owns XP rules, levels, achievements, rewards, Skill-owned state and generic management contracts.

The Skill should remain host-neutral. Host-specific Discord observation, event lifecycle logic and production deployment stay outside this repository.

## Current release

### 0.1.0 — Standalone baseline

**Status:** Ready for publication

Completed outcomes:
- standalone Python package and `gamerhq.skills` entry point
- stable Skill ID `progression`
- Runtime API `1`
- SDK compatibility `>=0.1,<0.2`
- stable storage keys `config.v1` and `member.v1:<member-id>`
- configurable XP sources, level curve, achievements, rewards and announcements
- Management APIs and Management UI Schema
- activity deduplication and daily XP caps
- role ownership safety for pre-existing Discord roles
- Python 3.12 / 3.14 CI
- independent release-artifact workflow

Remaining publication step:
- create immutable tag `v0.1.0`
- publish the GitHub Release
- verify the tag-triggered artifact workflow on the real release tag

## Milestone 1 — Publish the baseline

**Status:** In progress  
**Priority:** P0 / P1

### Objective
Turn the reviewed 0.1.0 baseline into an actual immutable public release.

### User / business value
Creates a stable version that Hosts and third-party developers can reference without depending on a moving commit.

### Acceptance criteria
- `v0.1.0` exists and points to the reviewed release commit
- GitHub Release exists
- wheel, source distribution and SHA-256 checksums are produced successfully
- public entry point and manifest identity pass release validation

## Milestone 2 — Contract & behavior consistency

**Status:** Planned  
**Priority:** P1

### Objective
Make every configurable field either enforce real Skill behavior or clearly document that the Host owns the policy.

### Committed review targets
- decide and document `repeatable` achievement semantics
- resolve the gap for default achievements such as `server-booster` and `first-game`
- define ownership of chat cooldown enforcement
- define ownership of voice eligibility rules such as `requiresOtherHuman` and `excludeAfk`
- eliminate stale documentation that understates current runtime behavior
- make the release workflow version-neutral for future releases

### Acceptance criteria
- no configuration field implies behavior that is silently ignored
- Host-vs-Skill responsibility is explicit
- compatible behavior remains stable for Runtime API 1
- tests cover each resolved contract

## Milestone 3 — Productized progression rules

**Status:** Proposed  
**Priority:** P1 / P2

### Objective
Reduce hard-coded GamerHQ-specific achievement logic and make progression rules reusable across compatible Hosts.

### Proposed direction
A declarative rule model may describe:
- metric or normalized source/event
- comparison
- threshold
- repeatability
- reward linkage

This is proposed scope, not yet an approved implementation contract.

### Acceptance criteria
To be defined only after the rule model is explicitly approved.

## Milestone 4 — External developer readiness

**Status:** Planned  
**Priority:** P2

### Objective
Make the repository understandable and maintainable without prior chat context.

### Candidate deliverables
- concise `CONTRIBUTING.md`
- concise `SECURITY.md`
- example configuration
- explicit compatibility/release guidance
- GitHub Issues and Milestones used for substantial work

## Future opportunities

Only pursue with demonstrated user value:
- leaderboards
- seasons or prestige
- configuration presets
- richer analytics
- Marketplace metadata
- optional public cross-Skill event consumption

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

When a missing upstream contract blocks Progression, create a handoff rather than changing another repository directly.
