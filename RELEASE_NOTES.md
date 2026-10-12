# Release Notes — v0.2.0

## Summary

Progression 0.2.0 extends the standalone XP & Progression Skill with host-neutral external progression signals and explicit safe repeatable-achievement semantics.

The Skill still releases independently from GamerHQ Host. A Host may adopt the new public signal contract separately.

## Public identity

- Distribution: `gamerhq-skill-xp-progression`
- Skill ID: `progression`
- Version: `0.2.0`
- Runtime API: `1`
- SDK compatibility: `>=0.1,<0.2`

## New public contract

### `progression.record-signal.v1`

Purpose: ingest bounded external facts that Progression cannot observe itself.

Payload:

- `memberId` — positive integer
- `provider` — bounded lowercase identifier
- `signal` — bounded lowercase identifier
- `dedupeKey` — required stable replay-safe key, max 160 chars
- `occurredAt` — optional bounded Unix timestamp

The contract does not accept arbitrary XP, arbitrary metrics, role grants or reward payloads.

## Default external achievement mappings

- `server-booster` → provider `discord`, signal `server_boosted`
- `first-game` → provider `profile`, signal `first_game_added`

Unknown valid signal pairs are safely returned as `unhandled`.

## Repeatable achievements

### Metric conditions

A repeatable `metric_at_least` achievement requires `repeatEvery`.

Occurrences happen at:

- `threshold`
- `threshold + repeatEvery`
- `threshold + 2 * repeatEvery`
- and so on

A condition merely remaining true does not award again.

At most 100 crossed repeat intervals are reconciled in one activity call.

### External-signal conditions

A repeatable external-signal achievement awards once for each unique matching deduplicated signal event.

## Reward safety

Achievement XP may repeat, but configured reward bundles remain one-time through existing `claimedRewards` semantics.

## Member-state compatibility

Storage namespaces remain:

- `config.v1`
- `member.v1:<discord-member-id>`

0.2.0 adds member-state fields additively:

- `seenSignals`
- `achievementCounts`

Older partial member records continue to receive safe in-memory defaults and read-only normalization remains non-destructive.

No destructive migration is required.

## Public Management APIs

- `progression.status.v1`
- `progression.get-config.v1`
- `progression.update-config.v1`
- `progression.preview-level.v1`
- `progression.record-activity.v1`
- `progression.record-signal.v1`
- `progression.member-status.v1`

## Capabilities

Unchanged:

- `storage.skill`
- `audit.write`
- `discord.messages.send`
- `discord.channels.read`
- `discord.members.read`
- `discord.roles.manage`

No scheduler capability is requested.

## Architecture boundary

Progression consumes external facts through a public contract and still does not import Discord.py, GamerHQ Host internals or another Skill implementation.

The optional GamerHQ adoption request is documented in `docs/HANDOFF_GAMERHQ_SIGNALS.md`.

## Release boundary

Publishing 0.2.0 does not imply GamerHQ Host adoption, production deployment or a server update.
