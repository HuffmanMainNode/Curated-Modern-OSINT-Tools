# Submodule Integrity and Trust Boundaries

This repository uses Git submodules to point to third-party projects at specific commits. A submodule pointer is a version reference, not a security assessment.

## Audit

Run:

    python scripts/audit_submodules.py --root .
    python -m unittest discover -s tests -p 'test_*.py' -v

The audit compares Git tree entries with .gitmodules, validates relative paths and canonical HTTPS GitHub URLs, and reports upstream URLs reused across categories.

## Interpreting results

- Missing or unmatched mappings and malformed URLs are errors.
- Reusing one upstream repository in multiple categories is a warning. It may be intentional and is not automatically removed.
- The audit does not clone, execute, scan, or contact upstream repositories.
- Pinned commits improve reproducibility, but do not prove that the pinned code is benign or maintained.

## Safe updates

Update one submodule at a time:

    bash scripts/update_submodules.sh tools/popular/sherlock

The script displays the upstream URL and current pinned commit, asks for explicit confirmation, updates only the named submodule, and prints the pointer diff. It does not commit changes. Review the upstream commit range, license, install scripts, dependencies, permissions, and tests before staging the new pointer.

Do not use bulk remote updates. Do not execute newly retrieved code until it has been reviewed and isolated appropriately.

## Badge count

The README badge is a count of Git submodule entries, not a validation score. After intentionally adding or removing entries, update it locally with:

    python scripts/update_badges.py

The workflow does not need write access to keep this badge synchronized.

## Curation status

The directory currently contains 232 Git submodule entries. That count describes the Git tree only. It does not mean 232 projects have passed security review, license review, maintenance checks, or safe-execution testing.

The selection rationale includes historical star counts and descriptions. Treat those as dated snapshots, not live metrics. Verify current upstream metadata before relying on them.
