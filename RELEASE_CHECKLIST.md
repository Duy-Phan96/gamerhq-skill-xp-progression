# Release Checklist — 0.1.0 extracted baseline

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
- [x] Public Management API IDs are unchanged.
- [x] Storage keys remain `config.v1` and `member.v1:<member-id>`.
- [x] Partial/legacy member state remains read-compatible without normalization writes.
- [x] Capability set reviewed; no extraction-time escalation added.
- [x] Release points to immutable reviewed commit `565ee8379cdd22cb00c18db188eeaddd058e626d`.
- [x] GamerHQ integration pins that reviewed commit.
- [x] GamerHQ full CI passed after externalization.
- [x] Rollback preserves the same Skill ID and storage namespace.
- [x] Production deployment remains outside this repository and is owned by the GamerHQ Host release process.

## Handoff state

**READY FOR GAMERHQ INTEGRATION**

This checklist records the standalone Skill release state only. It is not a GamerHQ production deployment approval.
