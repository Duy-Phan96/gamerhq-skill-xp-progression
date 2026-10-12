# Release Notes — v0.1.0

## Summary

First standalone release of the GamerHQ-compatible XP & Progression Skill.

This release is the reviewed baseline for independent installation by a compatible Host. It does not deploy or update GamerHQ production.

## Public identity

- Distribution: `gamerhq-skill-xp-progression`
- Skill ID: `progression`
- Version: `0.1.0`
- Runtime API: `1`
- SDK compatibility: `>=0.1,<0.2`

## Core features

- configurable XP sources and daily caps
- deterministic level calculation and previews
- per-member XP totals and source totals
- activity metrics
- bounded activity deduplication
- chat cooldown enforcement
- declarative metric-threshold achievements
- level / achievement / total-XP rewards
- badge, title, XP bonus, role and role-backed channel-access rewards
- configurable milestone announcements
- generic Management UI Schema
- revision-safe configuration updates
- additive compatibility for partial legacy member state

## Achievement rule model

Locally measurable achievements may use:

```json
{
  "condition": {
    "type": "metric_at_least",
    "metric": "voiceMinutes",
    "threshold": 300
  }
}
```

Stable local metrics in this release:

- `voiceMinutes`
- `lfgParticipations`
- `eventsHosted`

Achievements that depend on external Host state, such as `server-booster` and `first-game`, remain valid definitions but are not inferred from private Host internals.

`repeatable: true` remains compatibility-reserved in Rule V1; repeated awards require a future explicit repeat model.

## Activity policy ownership

Progression enforces:

- source enablement
- XP amounts
- daily caps
- chat cooldowns
- conversion of trusted voice units into `voiceMinutes`

The Host observer remains responsible for voice eligibility requiring raw Discord context, including:

- `requiresOtherHuman`
- `excludeAfk`

## Reward semantics

Supported reward grant types:

- `badge`
- `title`
- `xp_bonus`
- `role`
- `channel_access`
- `announcement`

`channel_access` is role-backed in Runtime API 1. The Host maps the configured role to channel permissions.

Progression never claims ownership of a role that the member already had.

## Public Management APIs

- `progression.status.v1`
- `progression.get-config.v1`
- `progression.update-config.v1`
- `progression.preview-level.v1`
- `progression.record-activity.v1`
- `progression.member-status.v1`

## Storage compatibility

- `config.v1`
- `member.v1:<discord-member-id>`

The standalone extraction preserves Skill ID and storage identity. Member-state additions remain additive. No release-specific destructive migration is required.

## Capabilities

- `storage.skill`
- `audit.write`
- `discord.messages.send`
- `discord.channels.read`
- `discord.members.read`
- `discord.roles.manage`

The Skill does not request `scheduler.jobs`.

## Quality evidence

Latest reviewed CI before final release preparation:

- Python 3.12: 41 tests passed, 5 subtests passed
- Python 3.14: 41 tests passed, 5 subtests passed
- package build: PASS
- built wheel installation: PASS
- `pip check`: PASS

The final release PR must pass the same repository CI before tagging.

## Release artifacts

Creating tag `v0.1.0` triggers the repository-owned release workflow, which verifies tag/version identity and builds:

- wheel
- source distribution
- SHA-256 checksums

## Architecture boundary

Host-specific Discord observation remains outside this package. The Skill consumes public Runtime/SDK contracts and does not import Discord.py or GamerHQ Host internals.

## Release boundary

This repository releases independently. A compatible Host may choose whether and when to install or pin this release.
