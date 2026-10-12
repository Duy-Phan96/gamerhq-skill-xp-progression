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

## Achievement rule model

The approved local rule model is documented in [docs/ACHIEVEMENT_RULES.md](docs/ACHIEVEMENT_RULES.md). Locally measurable achievements use declarative metric thresholds. Achievements that depend on external Host state remain inert until a public signal contract exists; the Skill does not inspect Host internals.

## Activity policy ownership

Progression owns deterministic XP economics that can be evaluated from its own payload/state. In Runtime API 1:

- `enabled`, `xp` and `dailyCap` are enforced by Progression;
- `chat.cooldownMinutes` is enforced by Progression using the supplied `occurredAt` timestamp and additive member state;
- `voice.windowMinutes` converts trusted voice activity units into Progression-owned `voiceMinutes` metrics;
- `voice.requiresOtherHuman` and `voice.excludeAfk` are observation requirements for the Host because this package does not receive raw Discord voice-state context.

The Host must submit voice activity only after applying those configured observation requirements. Progression must not inspect Discord.py or Host databases to enforce them.

If a future generic Host cannot consume these observation requirements through an existing public contract, this repository must create a HANDOFF rather than reaching into Host internals.

## Channel access reward semantics

In Runtime API 1, `channel_access` is intentionally a **role-backed access grant**, not a direct Discord channel-permission mutation.

Contract:
- the grant uses `roleId`;
- Progression calls the public role-grant adapter;
- the Host remains responsible for mapping that role to channel permissions;
- Progression tracks ownership only when it actually added the role;
- a pre-existing member role is never claimed as Progression-owned;
- disabling or removing the reward does not automatically revoke pre-existing access.

This keeps the Skill inside the existing `discord.roles.manage` capability and avoids inventing a new channel-permission capability. If future product requirements need direct per-member channel overrides, that would require a separate public Host capability and a HANDOFF rather than private Host access.
