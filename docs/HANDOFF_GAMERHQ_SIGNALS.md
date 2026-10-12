# HANDOFF REQUIRED — GamerHQ Host Signal Emission

FROM REPOSITORY:
`Duy-Phan96/gamerhq-skill-xp-progression`

TARGET REPOSITORY:
`Duy-Phan96/GamerHQ`

## Problem

Progression now exposes the public host-neutral contract:

`progression.record-signal.v1`

The Skill can consume external facts safely, but it does not observe Discord Gateway state or GamerHQ profile internals itself.

Default external achievements:

- `server-booster` → provider `discord`, signal `server_boosted`
- `first-game` → provider `profile`, signal `first_game_added`

Without a Host adapter emitting these public signals, those achievements will not unlock automatically in GamerHQ.

## Why this belongs to GamerHQ Host

The Host owns Discord/member observation, profile/game observation, Runtime routing and integration lifecycle.

Progression must not import GamerHQ private services, cogs, database code, Discord.py objects or profile internals.

## Requested outcome

Add Host-side adapters that call `progression.record-signal.v1` when the corresponding event is proven.

### Server booster

```json
{
  "memberId": 123456789,
  "provider": "discord",
  "signal": "server_boosted",
  "dedupeKey": "discord:server_boosted:<guild-id>:<member-id>:<stable-occurrence-id>",
  "occurredAt": 1791800000
}
```

### First game

```json
{
  "memberId": 123456789,
  "provider": "profile",
  "signal": "first_game_added",
  "dedupeKey": "profile:first_game_added:<guild-id>:<member-id>:<stable-occurrence-id>",
  "occurredAt": 1791800000
}
```

## Current contract / version

Progression:
- package `gamerhq-skill-xp-progression`
- Skill ID `progression`
- released baseline `v0.1.0`
- Runtime API `1`

New post-v0.1 public API:
- `progression.record-signal.v1`

Payload:
- `memberId`: positive integer
- `provider`: bounded lowercase identifier
- `signal`: bounded lowercase identifier
- `dedupeKey`: required stable key, max 160 chars
- `occurredAt`: optional bounded Unix timestamp

## Acceptance criteria

- Host uses only the public Runtime/Management contract.
- `discord/server_boosted` is emitted only for a real qualifying boost transition.
- `profile/first_game_added` is emitted only when the first-game condition is genuinely satisfied.
- Every event has a stable replay-safe `dedupeKey`.
- Retries reuse the same dedupe key.
- Host does not inject arbitrary XP, metrics or reward payloads.
- Missing/unavailable Progression Skill is handled safely according to Host conventions.
- Tests cover observation, payload construction, retry/dedupe and routing.
- Production deployment remains a separate GamerHQ release decision.

## Compatibility / migration

- Runtime API remains `1`.
- Progression storage keys remain unchanged.
- No direct Progression DB migration is required.
- Host must not depend on Progression private implementation symbols.

## Security / capability impact

No new Progression capability is required.

The Host should validate its own observed event before calling the public contract. Do not expose arbitrary user-controlled provider/signal payloads directly.

## Non-goals

- Do not modify Progression from the Host unless a real public-contract incompatibility is discovered.
- Do not add arbitrary XP injection.
- Do not couple Progression to Discord.py.
- Do not deploy production as part of this handoff.

## Source project status

Progression-side implementation is complete on current main:

- external signal contract implemented
- validation implemented
- dedupe/replay safety implemented
- booster and first-game conditions configured
- repeatable external signals supported
- Python 3.12 / 3.14 CI green

## When complete

Return with:
- GamerHQ PR / commit
- adapter behavior implemented
- tests/CI result
- any compatibility blocker discovered

Progression may then document GamerHQ as a verified consumer.
