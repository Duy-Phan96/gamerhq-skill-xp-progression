# Release Checklist — 0.2.0

This checklist determines whether **this Skill** is ready for its own 0.2.0 release. Downstream Host adoption is not a release gate.

- [ ] Python 3.12 release-branch CI passes.
- [ ] Python 3.14 release-branch CI passes.
- [ ] Package builds successfully.
- [ ] Built wheel installs successfully.
- [ ] `pip check` passes.
- [ ] Full standalone pytest suite passes.
- [x] Source portability boundary remains intact.
- [x] Skill ID remains `progression`.
- [x] Runtime API remains `1`.
- [x] SDK compatibility remains `>=0.1,<0.2`.
- [x] Existing storage keys remain unchanged.
- [x] New member state is additive only.
- [x] Public Management API addition `progression.record-signal.v1` is documented and tested.
- [x] External signals cannot inject arbitrary XP/rewards.
- [x] Signal dedupe/replay behavior is documented and tested.
- [x] Repeatable metric achievement semantics are explicit and tested.
- [x] Repeatable external-signal semantics are explicit and tested.
- [x] Existing non-repeatable achievement behavior remains compatible.
- [x] Reward bundles remain one-time unless separately redesigned.
- [x] Capability set is unchanged and reviewed.
- [x] CHANGELOG reflects 0.2.0.
- [x] RELEASE_NOTES reflect 0.2.0.
- [x] Package/manifest version is `0.2.0`.
- [x] Optional GamerHQ Host adoption is separated via handoff.
- [x] No downstream Host implementation blocks this independent release.

## Release status

**RELEASE CANDIDATE — CI PENDING**

After this release branch is fully green, update this checklist to READY FOR RELEASE and merge the final release PR. The resulting reviewed `main` commit becomes the intended target for tag `v0.2.0`.

## Downstream adoption

GamerHQ or another Host may independently adopt `progression.record-signal.v1`. Host CI, release candidates, production acceptance and deployment remain outside this repository.
