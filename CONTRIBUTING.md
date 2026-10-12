# Contributing

Thanks for contributing to the Progression Skill.

## Repository ownership

This repository owns only the standalone XP & Progression Skill.
Do not modify GamerHQ Host, gamerhq-web, another Skill repository, or production infrastructure from this project. If a missing public contract blocks work, create a handoff that describes the required public outcome and acceptance criteria.

## Development flow

1. Start from `main`.
2. Create a focused branch such as `feat/...`, `fix/...`, `docs/...`, `test/...`, or `chore/...`.
3. Keep changes scoped to one coherent outcome.
4. Add or update tests for behavior changes.
5. Open a focused pull request.
6. Merge only after CI is green and compatibility impact is reviewed.

## Required validation

Normal CI validates Python 3.12 and 3.14, package build, wheel installation, `pip check`, and the standalone pytest suite.

## Public contract compatibility

Treat Skill ID `progression`, Runtime API `1`, `config.v1`, `member.v1:<member-id>`, public `progression.*.v1` Management APIs, and declared capabilities as compatibility surfaces.

## Versioning and releases

Use semantic versioning. Update release metadata, review `RELEASE_CHECKLIST.md`, require green CI, create an immutable version tag, and verify the release-artifact workflow. See `RELEASES.md`.

## Architecture rules

- No Discord.py imports.
- No GamerHQ private Host imports.
- Use public Runtime/SDK contracts only.
- Keep Skill-owned storage backward-compatible where practical.
- Do not add capabilities without explicit review.
- Keep Host observation and production deployment outside this repository.

Use GitHub Issues for substantial work and `ROADMAP.md` for milestone direction.