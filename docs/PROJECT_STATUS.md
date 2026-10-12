# Project Status

**Snapshot date:** 2026-10-12  
**Repository:** `Duy-Phan96/gamerhq-skill-xp-progression`  
**Released version:** `v0.1.0`  
**Release commit:** `f32d27815b52a5a3cb94c4632904fd5692d3ffd4`  
**Maturity:** Released Alpha / stable standalone baseline

## Executive status

The standalone Progression extraction is complete and `v0.1.0` is officially released.

Verified release state:
- annotated tag `v0.1.0` points to the approved release commit;
- GitHub Release exists;
- wheel is published;
- source distribution is published;
- `SHA256SUMS.txt` is published;
- release issue #13 is completed.

The repository can now move into 0.2.0 development without changing the immutable 0.1.0 baseline.

## Verified implementation

Implemented and covered by code/tests:
- deterministic level curve and level previews
- source-based XP awards
- per-source totals
- daily XP caps
- bounded activity deduplication
- member metrics
- declarative `metric_at_least` achievement rules
- level / XP / achievement reward triggers
- badge, title, XP bonus and role-based grants
- role-backed channel-access rewards
- safe ownership tracking for role grants
- Skill-owned chat cooldown enforcement
- explicit Host ownership of raw voice eligibility observation
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
- released version: `0.1.0`
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

Release baseline CI:
- Python 3.12: 41 tests passed, 5 subtests passed
- Python 3.14: 41 tests passed, 5 subtests passed
- package build: pass
- wheel install: pass
- `pip check`: pass

No code-coverage percentage is currently measured; do not infer one.

## Remaining product gaps

- `repeatable: true` remains compatibility-reserved and has no repeated-award semantics yet.
- `server-booster` depends on an external signal.
- `first-game` depends on an external signal.
- public external progression-signal semantics are not yet defined.
- no automatic Host integration should be assumed merely because the Skill release exists.

## Current strategy

Next focus:
1. define external progression-signal semantics;
2. define safe repeatable-achievement semantics;
3. preserve 0.1.0 compatibility while preparing 0.2.0;
4. defer broad growth features until those contracts are stable.

## Repository ownership

This repository owns only the Progression Skill and its release lifecycle.

External changes use handoffs. The repository must not directly modify GamerHQ Host, gamerhq-web, another Skill or production infrastructure.

## Current release status

**RELEASED — v0.1.0**

No production/server deployment is implied by this release.
