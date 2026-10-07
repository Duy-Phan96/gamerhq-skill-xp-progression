# XP & Progression Skill repository instructions

This package is a portable GamerHQ Skill.

Hard rules:

- Keep Skill ID `progression` stable.
- Keep version `0.1.0` during the extraction baseline unless a reviewed release change requires otherwise.
- Preserve `config.v1` and `member.v1:<member-id>`.
- Preserve all public `progression.*.v1` Management API IDs.
- Do not import Discord.py or GamerHQ bot/cogs/services/database/hosts/config.
- Use only public `skill_runtime` contracts and explicitly reviewed Skill-owned dependencies.
- Keep static `[tool.gamerhq]` capabilities exactly equal to manifest permissions.
- Do not add `scheduler.jobs`; Progression does not own scheduler jobs.
- Keep tests offline and token-free.
- Keep host observation/adapters in GamerHQ.
- Do not deploy production from this repository.


## GamerHQ cross-project release boundary

This repository participates in the wider GamerHQ ecosystem.

A green PR/release in this repository means the work can be **ready for GamerHQ integration**. It does **not** independently mean the production GamerHQ server should update.

Every meaningful handoff must report:

- repository, branch, PR and immutable merge/package commit;
- public contract impact;
- storage/data migration impact;
- Runtime/API/capability impact where relevant;
- deployment/config/secret impact;
- whether this work should be included in the next GamerHQ server release snapshot.

Production deployment is decided only from one immutable GamerHQ Host release candidate and its Server Release Snapshot. Never recommend deploying a moving `develop`/latest branch merely because this repository's CI is green.

### Host-only server update rule

All GamerHQ production server updates are owned and executed from the main Host repository:

`Duy-Phan96/GamerHQ`

Standalone Skill repositories must never execute, initiate, or provide the operational server-update step themselves. They may only report their immutable reviewed package/commit and whether they are ready to be included in the next GamerHQ Host release candidate.

The Host repository is responsible for release-candidate creation, Server Release Snapshot, promotion to `main`, deployment readiness, and the owner-run VPS update procedure. If a Skill change requires a server update, hand that requirement back to GamerHQ instead of running deployment from the Skill project.

Canonical rules live in the GamerHQ Host repository:

- `docs/development/GAMERHQ_ECOSYSTEM_WORKING_RULES.md`
- `docs/development/SERVER_RELEASE_SNAPSHOT.md`

Production deployment, restart, DB mutation and production secret changes remain explicit owner actions.
