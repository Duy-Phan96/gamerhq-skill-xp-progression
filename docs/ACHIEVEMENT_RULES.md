# Achievement Rules

This document defines the approved host-neutral achievement rule model for the next Progression compatibility slice.

## Goals

- remove hidden dependence on hard-coded achievement IDs;
- keep Runtime API `1`;
- preserve `config.v1` and `member.v1:<member-id>`;
- keep Host-specific observation outside this repository;
- make configuration semantics explicit and testable.

## Rule V1

Locally evaluable achievements use a declarative condition:

```json
{
  "condition": {
    "type": "metric_at_least",
    "metric": "voiceMinutes",
    "threshold": 300
  }
}
```

Supported V1 condition type:

### `metric_at_least`

Fields:

- `metric` — stable member metric key owned by Progression;
- `threshold` — positive integer threshold.

An achievement unlocks when the stored metric is greater than or equal to the threshold.

Initial stable metric keys:

- `voiceMinutes`
- `lfgParticipations`
- `eventsHosted`

New metric keys require an explicit Progression-owned design change or a public upstream signal contract. Do not infer private Host state.

## Existing defaults

The current hard-coded defaults map to rules as follows:

| Achievement | Condition |
| --- | --- |
| `first-mate` | `lfgParticipations >= 1` |
| `event-regular` | `lfgParticipations >= 10` |
| `community-host` | `eventsHosted >= 10` |
| `voice-rookie` | `voiceMinutes >= 300` |
| `voice-regular` | `voiceMinutes >= 1500` |
| `voice-veteran` | `voiceMinutes >= 6000` |

These become configuration data rather than Python ID switches.

## External-signal achievements

`server-booster` and `first-game` depend on state that this repository does not observe.

For V1:

- they remain valid achievement definitions;
- they do not receive a fake local metric rule;
- Progression does not inspect GamerHQ Host internals;
- automatic unlocking remains unavailable until a suitable public event/API signal exists.

If automatic support is required, create a HANDOFF for a public contract. Do not modify the Host from this repository.

## Repeatable semantics

`repeatable: false` means the achievement can unlock only once per member.

`repeatable: true` is supported with explicit, condition-specific semantics:

### Metric conditions

A repeatable `metric_at_least` achievement must define `repeatEvery`.

- first occurrence: when `metric >= threshold`;
- second occurrence: when `metric >= threshold + repeatEvery`;
- third occurrence: when `metric >= threshold + 2 * repeatEvery`;
- and so on.

A true condition that has not crossed another interval does not award again. Up to 100 crossed occurrences may be reconciled in one activity call.

### External-signal conditions

A repeatable `external_signal` achievement awards once for each unique matching signal event. The required signal `dedupeKey` provides replay safety.

### Rewards

Repeatable achievement XP may repeat, but configured rewards remain one-time through existing `claimedRewards` semantics. Repeatable rewards would require a separate explicit design.

### State

`achievementCounts` stores occurrence counts additively per achievement. The existing `achievements` list continues to mean “unlocked at least once”, preserving member-state compatibility.

## Storage compatibility

No storage-key migration is required.

Existing member records continue to use:

- `achievements` as the set/list of unlocked non-repeatable achievement IDs;
- existing metrics under `metrics`.

No normalization write occurs during reads.

## Configuration compatibility

Achievements without `condition` remain valid. They are treated as externally-triggered/inert from the local metric evaluator.

This preserves existing definitions such as `server-booster` and `first-game`.

## Security / trust boundary

The Skill evaluates only data already present in its Skill-owned member state.

It does not:
- query Discord.py objects directly;
- inspect Host databases;
- infer booster/game state;
- trust arbitrary metric names without validation.

## Acceptance criteria

- hard-coded achievement threshold table is removed;
- local default achievements declare equivalent conditions;
- config validation rejects unsupported condition types/metrics/thresholds;
- achievements without conditions remain valid and are not auto-unlocked;
- existing non-repeatable member state remains compatible;
- current unlock behavior for first-mate, event-regular, community-host and voice milestones remains unchanged;
- tests prove custom metric-threshold achievements can unlock without code changes.
