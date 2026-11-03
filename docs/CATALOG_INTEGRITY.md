# Catalog Integrity and Safe Use

This repository is a directory of third-party Git submodules. A listed repository is a discovery lead, not an endorsement, security review, license grant, or guarantee that the upstream project is maintained.

## Validate the index

The local validator checks that each configured submodule has a path and HTTPS GitHub owner/repository URL, paths remain inside tools/, and configured paths match tracked Git gitlinks. Duplicate upstream URLs are reported for review without deleting multi-category listings.

Run without fetching upstream repositories:

    python -m unittest discover -s tests -p 'test_*.py' -v
    python scripts/catalog_integrity.py --root .

The validator does not clone submodules, execute their code, inspect dependencies, determine license suitability, or verify current security or maintenance status.

## Safe submodule workflow

- Clone with recursive submodules only when you intend to retrieve third-party code.
- Review the upstream repository, pinned commit, license, release history, issue activity, dependencies, install scripts, and required privileges before running anything.
- Do not run tools against systems or accounts without explicit authorization.
- Prefer isolated VMs or disposable containers for unknown code. A container alone is not a complete security boundary.
- Do not provide credentials, browser profiles, personal datasets, or production access to unreviewed tools.
- Treat upstream code, README instructions, issue content, and generated output as untrusted.
- Preserve source attribution and each upstream project's license and terms.

## Responsible OSINT scope

Use public information proportionately and lawfully. Do not use this directory to facilitate stalking, doxxing, credential theft, unauthorized access, harassment, mass collection of sensitive personal data, or targeting people based on protected or sensitive traits. Minimize collection, retain source context, document uncertainty, and provide a correction/removal path for demonstrably inaccurate entries.

## Curation status vocabulary

- Listed: repository URL and pinned submodule commit are present.
- Metadata-valid: local Git metadata and Git index agree.
- Upstream-reviewed: a dated human review examined the upstream project.
- Security-reviewed: a scoped review was performed and limitations are documented.

Only the first two states are measured by the automated validator.
