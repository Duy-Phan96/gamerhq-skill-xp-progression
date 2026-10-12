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
- [x] Achievement rule semantics are documented and tested.
- [x] Activity policy ownership is documented and tested.
- [x] Reward grant payloads are validated at config time.
- [x] Channel-access semantics are documented and tested.
- [x] Capability/security set has been explicitly reviewed.
- [x] CHANGELOG reflects the final 0.1.0 scope.
- [x] RELEASE_NOTES reflect the final 0.1.0 scope.
- [x] Package version is `0.1.0`.
- [x] Release workflow is version-neutral.
- [x] Rollback/upgrade compatibility for Skill-owned state is understood.
- [x] No missing upstream contract blocks publication.

## Release status

**READY FOR FINAL RELEASE PR**

After this final release-preparation PR is merged and CI is green, its merge commit becomes the immutable publication target for tag `v0.1.0`.

## Downstream adoption

After publication, GamerHQ or another compatible Host may independently choose whether and when to install or pin this Skill. Their CI, release candidate, production acceptance and deployment remain outside this repository.
