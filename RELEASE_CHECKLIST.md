# Release Checklist

This checklist determines whether **this Skill** is ready for its own release. Downstream GamerHQ installation/pinning is not a release gate for this repository.

- [ ] Python 3.12 CI passes.
- [ ] Python 3.14 CI passes.
- [ ] Package builds successfully.
- [ ] Built wheel installs successfully.
- [ ] `pip check` passes.
- [ ] Full standalone pytest suite passes.
- [ ] Source portability audit is clean.
- [ ] Factory/lifecycle SDK conformance passes.
- [ ] Static `[tool.gamerhq]` metadata is valid.
- [ ] Static capabilities exactly match `SkillManifest.permissions`.
- [ ] Entry-point name equals manifest Skill ID `progression`.
- [ ] Runtime API / SDK compatibility is explicitly documented.
- [ ] CI uses released/public contracts or a reviewed immutable compatibility commit, never a moving upstream branch.
- [ ] Public Management API compatibility has been reviewed.
- [ ] Storage keys and migration behavior have been reviewed.
- [ ] Partial/legacy member state remains compatible where required.
- [ ] Capability/security changes, if any, received explicit review.
- [ ] CHANGELOG reflects this Skill release.
- [ ] Package version is correct for the intended release.
- [ ] Release points to an immutable reviewed commit/artifact.
- [ ] Rollback/upgrade compatibility for Skill-owned state is understood.
- [ ] Any missing upstream contract is represented by a handoff rather than a cross-repository implementation.

## Downstream adoption

After a Skill release, GamerHQ or another compatible Host may independently choose to install or pin it. Their CI, release candidate, production acceptance and deployment are owned by those repositories and are not prerequisites for declaring this Skill `READY FOR RELEASE` or `RELEASED`.
