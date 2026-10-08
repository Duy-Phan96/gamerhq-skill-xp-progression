# Releases

This repository releases the XP & Progression Skill independently from GamerHQ Host and other repositories.

## Release process

1. Prepare and merge a focused release PR.
2. Confirm the package version in `pyproject.toml` and `CHANGELOG.md`.
3. Confirm normal CI is green on the reviewed release commit.
4. Create an immutable Git tag using the package version, for example `v0.1.0`.
5. The `Release artifacts` workflow verifies that the tag matches `project.version`.
6. The workflow builds both wheel and source distribution, installs the wheel, runs `pip check`, verifies the public `gamerhq.skills` entry point and uploads SHA-256 checksums with the artifacts.
7. Publish the GitHub Release using `RELEASE_NOTES.md`.

## Release artifacts

Each tag produces one GitHub Actions artifact containing:

- `gamerhq_skill_xp_progression-<version>-py3-none-any.whl`
- source distribution
- `SHA256SUMS.txt`

Artifacts are release evidence for this repository. They do not deploy GamerHQ or another Host.

## Compatibility

Every release must document:

- Skill ID
- package version
- Runtime API
- SDK compatibility range
- capabilities
- public Management API impact
- storage/migration impact

## Security

Release workflows are token-free beyond GitHub's default workflow token and do not publish to PyPI or another package registry automatically. Registry publication can be added later as a separate reviewed change.
