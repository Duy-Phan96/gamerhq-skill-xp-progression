# Release Checklist — 0.1.0

This checklist determines whether **this Skill** is ready for its own release. Downstream Host installation/pinning is not a release gate.

- [x] Python 3.12 CI passes.
- [x] Python 3.14 CI passes.
- [x] Package builds successfully.
- [x] Built wheel installs successfully.
- [x] `pip check` passes.
- [x] Full standalone pytest suite passes.
- [x] Source portability audit is clean.
- [x] Factory/lifecycle SDK conformance passes.
- [x] Static `[tool.gamerhq]` metadata is valid.
- [x] Static capabilities exactly match `SkillManifest.permissions`.
- [x] Entry-point name equals manifest Skill ID `progression`.
- [x] Runtime API / SDK compatibility is explicitly documented.
- [x] CI uses a reviewed immutable compatibility input rather than a moving upstream branch.
- [x] Public Management API compatibility has been reviewed.
- [x] Storage keys and migration behavior have been reviewed.
- [x] Partial/legacy member state remains compatible without normalization writes.
- [x] Capability/security set has been explicitly reviewed.
- [x] CHANGELOG reflects this Skill release.
- [x] Package version is `0.1.0`.
- [x] Rollback/upgrade compatibility for Skill-owned state is understood.
- [x] No missing upstream contract currently blocks this release.

## Release status

**READY FOR RELEASE**

Final publication requires an immutable release tag/artifact for the reviewed `main` commit.

## Downstream adoption

After publication, GamerHQ or another compatible Host may independently choose whether and when to install or pin this Skill. Their CI, release candidate, production acceptance and deployment remain outside this repository.
