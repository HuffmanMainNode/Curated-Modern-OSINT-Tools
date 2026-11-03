# Submodule Integrity and Trust Boundaries

This repository uses Git submodules to point to third-party projects at specific commits. A submodule pointer is a version reference, not a security assessment.

## Audit

Run:

```bash
python scripts/audit_submodules.py --root .
python -m unittest discover -s tests -p 'test_*.py' -v
```

The audit compares Git tree entries with `.gitmodules`, validates that paths are safe relative paths, checks that URLs use the canonical HTTPS GitHub host, and reports upstream URLs reused across categories.

## Interpreting results

- Missing or unmatched mappings and malformed URLs are errors.
- Reusing one upstream repository in multiple categories is a warning. It may be intentional and is not automatically removed.
- The audit does not clone, execute, scan, or contact upstream repositories.
- Pinned commits improve reproducibility, but do not prove that the pinned code is benign or maintained.

## Safe use

1. Review the upstream repository and pinned commit before initializing a submodule.
2. Read its license, security policy, installation instructions, dependencies, and permission requirements.
3. Use a disposable VM/container or other isolation appropriate to the tool's risk.
4. Do not supply credentials, personal data, or production access to an unreviewed tool.
5. Update one submodule at a time, inspect the pointer diff and upstream changes, then record the review date and rationale.

## Curation status

The directory currently contains 232 Git submodule entries. That count describes the Git tree only. It does not mean 232 projects have passed security review, license review, maintenance checks, or safe-execution testing.

The selection rationale includes historical star counts and descriptions. Treat those as dated snapshots, not live metrics. Verify current upstream metadata before relying on them.
