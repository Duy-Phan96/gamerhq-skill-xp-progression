# XP & Progression Skill repository instructions

This package is a portable, independently owned GamerHQ-compatible Skill.

## Hard rules

- Keep Skill ID `progression` stable.
- Preserve `config.v1` and `member.v1:<member-id>`.
- Preserve public `progression.*.v1` Management API IDs across compatible releases.
- Do not import Discord.py or GamerHQ bot/cogs/services/database/hosts/config.
- Use only public `skill_runtime` contracts and explicitly reviewed Skill-owned dependencies.
- Keep static `[tool.gamerhq]` capabilities exactly equal to manifest permissions.
- Do not add `scheduler.jobs` unless Progression itself gains scheduler-owned behavior through an explicit reviewed change.
- Keep tests offline and token-free.
- Keep host observation/adapters outside this repository.
- Never deploy or operate a GamerHQ production server from this repository.

## Repository ownership

Repository: `Duy-Phan96/gamerhq-skill-xp-progression`

This project owns:

- XP rules and level calculations;
- achievements and rewards;
- Progression configuration;
- Skill-owned storage schemas and compatibility;
- Progression Management APIs and Management UI Schema;
- package metadata and entry point;
- tests and CI;
- Skill documentation;
- Skill versioning, changelog and releases;
- internal implementation decisions for this package.

This project does NOT own:

- `Duy-Phan96/GamerHQ` Host/Runtime/SDK implementation;
- GamerHQ production deployment or infrastructure;
- `gamerhq-web`;
- another `gamerhq-skill-*` repository;
- another developer's private implementation.

Read-only inspection of public external repositories is allowed when needed to understand public contracts, released versions, immutable commits, package metadata or compatibility requirements. Inspection never grants write ownership.

## Public dependencies

Current compatibility:

- Runtime API: `1`
- SDK compatibility: `>=0.1,<0.2`
- host capabilities:
  - `storage.skill`
  - `audit.write`
  - `discord.messages.send`
  - `discord.channels.read`
  - `discord.members.read`
  - `discord.roles.manage`

Consume public/released contracts or reviewed immutable compatibility commits. Do not test or release against a moving upstream branch such as `develop`.

## Independent releases

This repository versions and releases Progression independently.

Valid status language includes:

- `READY FOR REVIEW`
- `READY FOR RELEASE`
- `RELEASED`
- `BLOCKED BY HANDOFF`
- `WAITING FOR PUBLIC CONTRACT`
- `COMPATIBLE WITH RUNTIME API 1`

A green Skill release does not imply a GamerHQ server update. GamerHQ or another compatible Host may independently decide whether and when to install or pin a released Progression version.

## Handoffs

If work requires a change in another repository, stop at the ownership boundary. Finish all possible local work and provide:

```text
HANDOFF REQUIRED

FROM REPOSITORY:
Duy-Phan96/gamerhq-skill-xp-progression

TARGET REPOSITORY:
<owner/repository>

PROBLEM:
<missing public behavior/contract>

WHY THIS BELONGS TO THE TARGET:
<ownership reason>

REQUESTED OUTCOME:
<public behavior/contract needed>

CURRENT CONTRACT / VERSION:
<Runtime API / SDK / Management API / Skill version>

ACCEPTANCE CRITERIA:
- ...

COMPATIBILITY / MIGRATION CONSTRAINTS:
- ...

SECURITY / CAPABILITY IMPACT:
- ...

NON-GOALS:
- ...

SOURCE PROJECT STATUS:
<complete/blocked local work>

WHEN COMPLETE:
<released version / immutable commit / public API this project should consume>
```

Describe what is needed. Do not dictate another repository's private implementation unless a public compatibility constraint requires it.

## Skill-to-Skill communication

Never import another Skill's private implementation. Cross-Skill behavior must use public Events or public Skill APIs. Optional providers must remain optional unless explicitly declared as required dependencies.

## Reporting

At meaningful milestones report:

```text
COMPLETED

REPOSITORY
BRANCH
PR
VERSION / MERGE COMMIT

TESTS / CI

PUBLIC CONTRACT IMPACT

STORAGE / MIGRATION IMPACT

SECURITY / CAPABILITY IMPACT

RELEASE STATUS

DEPENDENCIES

HANDOFFS REQUIRED

PROPOSED FOLLOW-UPS
```
