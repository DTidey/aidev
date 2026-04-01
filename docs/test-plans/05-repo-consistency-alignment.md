# Test Plan: repo-consistency-alignment

Path: `docs/test-plans/05-repo-consistency-alignment.md`

## What changed
- Tightened docs-only detection so human-authored dependency and tooling changes require the normal spec-first packet.
- Backfilled older packet artifacts so the repository history matches the current workflow rules.
- Added tests that pin both the stricter validator behavior and the required historical packet sections.

## Acceptance criteria coverage
- AC1: Verify validator tests reject docs-only classification for dependency manifests, `Makefile`, and pre-commit config, while still allowing `README.md` and `CHANGELOG.md`.
- AC2: Verify packet `00` has a matching PR draft and a `Security considerations` section in the spec.
- AC3: Verify older PR drafts include required security review context and expected validation state.
- AC4: Verify static tests cover the historical artifacts and run `make lint`, `make test`, and `make security`.

## Edge cases
- From spec:
  - `CHANGELOG.md` should stay docs-only.
  - Dependabot dependency-only PRs should still qualify for the existing bypass.
  - Historical artifact updates should not introduce new behavior.
- Additional adversarial cases:
  - A future validator edit re-classifies `pyproject.toml` as docs-only again.
  - A future cleanup removes packet `00`'s PR draft because it is "historical."
  - A historical PR draft omits the security review disposition even though the repository requires it.

## Notes
- Flaky risks: None expected; coverage is static content plus pure validator unit tests.
- Determinism considerations: Prefer direct file-content assertions over narrative review.
