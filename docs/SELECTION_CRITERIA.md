# OSINT Tool Selection Criteria

This document describes the directory's intended curation criteria. It is not evidence that every listed project has passed every check.

## Discovery and inclusion

A candidate may be included when it has a clear OSINT, digital investigation, public-interest research, defensive security, or data-analysis use case. Popularity is a discovery signal only. Low-star projects may be included when they offer a distinct capability, but they receive no implied quality endorsement.

## Review dimensions

For each candidate, reviewers should record what is known and what remains unknown:

1. **Identity and provenance:** canonical upstream URL, repository owner, project name, and pinned commit.
2. **Maintenance:** latest upstream commit/release observed and whether the project is archived. A recent commit does not prove security or quality.
3. **License:** explicit upstream license and whether it covers the code or data being used. Missing or unclear license means rights are unresolved.
4. **Security posture:** available security policy, dependency practices, permissions, network behavior, secret handling, and known advisories. A public source tree is not proof of harmlessness.
5. **Data practices:** sources collected, personal-data exposure, retention, telemetry, and third-party service requirements.
6. **Operational safety:** install steps, privilege requirements, destructive actions, and whether testing can be done in an isolated environment.
7. **Use limitations:** platform/API restrictions, rate limits, terms of service, jurisdictional constraints, and possible false positives.

## Status vocabulary

- **Catalogued:** a repository URL and pinned submodule commit are present.
- **Metadata reviewed:** identity, maintenance, and license fields have been checked on a recorded date.
- **Security reviewed:** a documented, scoped review was performed. State the scope and date.
- **Needs review:** information is missing, stale, ambiguous, or contradictory.
- **Archived/upstream unavailable:** the upstream project is archived or cannot currently be reached.

Never label a project "passed", "safe", "verified", or "zero-trust validated" unless a defined, reproducible review supports that exact claim.

## Refresh cadence

A quarterly review is a reasonable target for metadata triage, with urgent review when a security advisory or upstream compromise is reported. This is a target, not an automated guarantee. Record review dates and preserve historical findings rather than silently rewriting them.
