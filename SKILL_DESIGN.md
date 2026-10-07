# Skill Design — Progression & Achievements

## Identity

- Distribution: `gamerhq-skill-xp-progression`
- Python package: `gamerhq_skill_xp_progression`
- Display name: Progression & Achievements
- Skill ID: `progression`
- Version: `0.1.0`
- Runtime API: `1`

The repository/distribution name may describe XP explicitly. The runtime Skill ID is frozen and must not change.

## Boundary

The package owns XP rules, level calculations, achievements, rewards, Skill-owned storage, configuration, Management APIs and the Management UI Schema.

The host owns Discord voice/activity observation, completed-event observation and other GamerHQ-specific adapters. The host calls public Runtime contracts and never imports private implementation symbols from this package.

## Storage schema

### `config.v1`
Stores validated Progression configuration including XP sources, level curve, achievements, rewards, announcements and revision.

### `member.v1:<discord-member-id>`
Stores member progression state. Reads are additive: older partial records receive safe in-memory defaults for `sourceXp`, `dailyXp`, `metrics`, `achievements`, `seenActivity`, `badges`, `titles`, `claimedRewards` and `ownedRoleGrants`.

Read-only normalization must not rewrite storage. `disable()` is non-destructive.

## Migrations

Repository extraction does not change guild ID, Skill ID or storage keys and therefore does not require a data migration. Future schema changes must be deterministic, reviewed and backward-compatible.

## Management APIs

- `progression.status.v1`
- `progression.get-config.v1`
- `progression.update-config.v1`
- `progression.preview-level.v1`
- `progression.record-activity.v1`
- `progression.member-status.v1`

Payloads are host-neutral and bounded. The host routes calls through the Skill Runtime.

## Management UI Schema

The manifest declares a generic schema covering XP sources, level curve, achievements, rewards and announcements. Generic host/web management surfaces can render configuration without a custom Progression page.

## Capabilities and rationale

- `storage.skill`: configuration and member progression state.
- `audit.write`: auditable configuration changes.
- `discord.messages.send`: configured announcements.
- `discord.channels.read`: validate/read configured announcement/channel access targets.
- `discord.members.read`: member display/context required by rewards/announcements.
- `discord.roles.manage`: reviewed role reward grants.

No scheduler capability is required; Progression does not own scheduler jobs.

## Dedupe

Host activity may provide a bounded `dedupeKey`. Seen keys are tracked in member state so a repeated host signal does not award XP twice.

## Reward ownership

When a role grant is newly created by Progression, ownership is tracked. If the member already had the role, Progression must not claim ownership of that pre-existing role.

## Announcements

Announcements are configurable by enablement, destination channel, event type and template. Rendering uses safe allowed-mentions behavior. Status/read operations never emit announcements.

## Security and privacy

The Skill uses only public Runtime capabilities and Skill-scoped storage. It does not access tokens, environment secrets, raw production databases, Discord.py objects or arbitrary filesystem/network execution.

## Failure and retry behavior

Configuration writes use revision checks to reject stale edits. Activity dedupe makes retried host signals safe when a stable dedupe key is supplied. Host-side signal collection remains responsible for retrying transient observation/Runtime failures.
