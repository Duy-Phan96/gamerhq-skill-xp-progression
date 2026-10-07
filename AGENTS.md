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
