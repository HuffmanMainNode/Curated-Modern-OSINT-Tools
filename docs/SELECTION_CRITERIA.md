# OSINT Tool Selection Criteria

This directory is a discovery catalogue, not a certification programme. Inclusion does not mean a tool is safe, trustworthy, maintained, legally suitable, or appropriate for every investigation.

## Listing criteria

1. Clear purpose: the upstream project should have an identifiable use case and source repository.
2. Source transparency: source and maintainer identity should be inspectable where available. Public source does not prove the absence of malicious behavior.
3. Lifecycle evidence: record the date of the last observed upstream activity. Recent commits are a signal, not proof of quality; older stable projects may remain useful.
4. License clarity: record the upstream license and note when it is absent, unclear, or incompatible with the intended use.
5. Operational risk: document permissions, credentials, data sent to third parties, scraping behavior, and potentially intrusive functions.
6. Provenance: keep the canonical upstream URL, pinned commit, category, review date, and reviewer notes.

## Review outcomes

Use explicit states rather than a blanket "Passed" badge:

- Listed: URL and pinned gitlink are present.
- Metadata-valid: Git submodule metadata matches the Git index.
- Upstream-reviewed: a dated human review inspected the upstream repository.
- Security-reviewed: a scoped security review was completed and documented.

Do not infer any higher state from popularity, stars, forks, commit recency, or public source availability.

## Category rationales

Category placement is navigational only. A project may appear in more than one category. Duplicate URLs should be disclosed and reviewed, not automatically removed.
