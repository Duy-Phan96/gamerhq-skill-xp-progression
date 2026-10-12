# Project Status

**Snapshot date:** 2026-10-12  
**Repository:** `Duy-Phan96/gamerhq-skill-xp-progression`  
**Current package version:** `0.1.0`  
**Maturity:** Alpha / release-ready baseline  
**Current main:** `f0d589136854d2f62c11ca1e0a01d0126bc893a6`

## Executive status

The standalone extraction is complete and technically healthy. The repository has a stable public identity, independent CI, tests and release tooling. The major remaining baseline task is publication of the first immutable release.

The next development phase should focus on contract/behavior consistency before adding broad new features.

## Verified implementation

Implemented and covered by code/tests:
- deterministic level curve and level previews
- source-based XP awards
- per-source totals
- daily XP caps
- bounded activity deduplication
- member metrics
- achievement unlocks for current hard-coded metric thresholds
- level / XP / achievement reward triggers
- badge, title, XP bonus and role-based grants
- safe ownership tracking for role grants
- configurable announcements with suppressed Discord mentions
- revision-safe configuration updates
- Skill health check
- generic Management UI Schema
- six public Management API contracts
- additive reads of partial legacy member state

## Current public contracts

### Identity
- Skill ID: `progression`
- Runtime API: `1`
- SDK: `>=0.1,<0.2`

### Storage
- `config.v1`
- `member.v1:<discord-member-id>`

### Management APIs
- `progression.status.v1`
- `progression.get-config.v1`
- `progression.update-config.v1`
- `progression.preview-level.v1`
- `progression.record-activity.v1`
- `progression.member-status.v1`

### Capabilities
- `storage.skill`
- `audit.write`
- `discord.messages.send`
- `discord.channels.read`
- `discord.members.read`
- `discord.roles.manage`

## Quality evidence

Latest reviewed CI evidence:
- Python 3.12: 31 tests passed
- Python 3.14: 31 tests passed
- package build: pass
- wheel install: pass
- `pip check`: pass

No code-coverage percentage is currently measured; do not infer one.

## Important known gaps

### Product / contract gaps
- achievement `repeatable: true` remains compatibility-reserved; Rule V1 deliberately does not invent repeated-award semantics without an explicit repeat interval/condition
- default achievements `server-booster` and `first-game` have definitions but no local automatic unlock path
- chat `cooldownMinutes` is Skill-owned and enforced by `record_activity()` using `occurredAt` plus additive member state
- voice `requiresOtherHuman` and `excludeAfk` are explicitly Host observation requirements because raw Discord voice-state context is outside this repository
- locally measurable achievements now use validated declarative `metric_at_least` conditions instead of a hard-coded achievement-ID threshold table
- `channel_access` is explicitly defined as a role-backed access grant in Runtime API 1; direct channel-permission mutation is out of scope without a future public Host capability
- reward grant payloads are now validated at configuration time instead of deferring malformed IDs/XP values until reward execution

### Documentation / release gaps
- no Git tag or GitHub Release exists yet for 0.1.0
- the tag release workflow still contains a fixed `0.1.0` manifest-version assertion and must become version-neutral before the next version
- no formal Issue backlog existed at the time of this snapshot

## Product strategy

Near-term priority:
1. publish 0.1.0
2. align configuration with real runtime semantics
3. make achievement/rule behavior more generic only after the contract is approved
4. improve contributor/security documentation
5. defer growth features until real usage justifies them

Avoid adding broad feature scope before the existing contract is internally consistent.

## Repository ownership

This repository owns only the Progression Skill and its release lifecycle.

External changes use handoffs. The repository must not directly modify GamerHQ Host, gamerhq-web, another Skill or production infrastructure.

## Current release status

**READY FOR RELEASE — 0.1.0**

This means the Skill is technically ready for its own publication. It does not imply that any Host should deploy or update.
