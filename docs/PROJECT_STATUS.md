# Project Status

**Snapshot date:** 2026-10-12  
**Repository:** `Duy-Phan96/gamerhq-skill-xp-progression`  
**Released version:** `v0.2.0`  
**Release commit:** `b8226977adad5ea966f77805f6a4c0f56b78be17`  
**Maturity:** Released Alpha / verified GamerHQ develop integration

## Executive status

The standalone Progression Skill is released as `v0.2.0`, and GamerHQ `develop` now consumes that immutable release through the public signal contract.

Verified release state:
- annotated tag `v0.2.0` points to `b8226977adad5ea966f77805f6a4c0f56b78be17`;
- GitHub Release exists;
- wheel, source distribution and `SHA256SUMS.txt` are published;
- release issue #30 is completed.

Verified downstream adoption:
- GamerHQ PR #148 merged into `develop`;
- GamerHQ merge commit `f2c237dd76133484e9a2f70ea8161c8a573b2100`;
- GamerHQ emits the booster and first-game public signals;
- GamerHQ CI is green on Python 3.12 and 3.14.

This does not mean GamerHQ production has been deployed.

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
- seven public Management API contracts
- additive reads of partial legacy member state

## Current public contracts

### Identity
- Skill ID: `progression`
- Runtime API: `1`
- released version: `0.2.0`
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

The 0.2 interoperability milestone is complete for the Progression Skill and verified against GamerHQ `develop`.

Remaining work is product evolution rather than a contract blocker:
- broader operator examples/presets;
- post-0.2 usability improvements;
- future features such as leaderboards/seasons only when justified by usage.

GamerHQ production adoption remains pending its normal Host release/deployment lifecycle.

## Current strategy

Next focus:
1. preserve the released 0.2 public compatibility guarantees;
2. improve developer/operator usability and examples;
3. evaluate the next product milestone using real user value;
4. keep GamerHQ production rollout independent from Skill development.

## Repository ownership

This repository owns only the Progression Skill and its release lifecycle.

External changes use handoffs. The repository must not directly modify GamerHQ Host, gamerhq-web, another Skill or production infrastructure.

## Current release status

**v0.2.0 — RELEASED**  
**GamerHQ `develop` integration — VERIFIED**  
**GamerHQ production deployment — NOT PERFORMED**

The immutable v0.1.0 release remains available as the previous baseline.
