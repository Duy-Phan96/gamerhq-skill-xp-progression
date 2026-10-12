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

`repeatable: true` is reserved but **not enabled in Rule V1** because a single `metric_at_least` condition does not define a safe repeat interval. Existing configurations continue to parse the field for compatibility, but a repeatable achievement without an explicit future repeat rule must not produce repeated XP.

A later compatible extension may introduce an explicit repeat model such as `every` or a distinct repeat condition. That requires separate review and tests.

This deliberately avoids inventing ambiguous semantics such as awarding repeatedly on every subsequent activity after a threshold is crossed.

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
