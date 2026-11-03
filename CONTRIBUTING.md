# Contributing

Thank you for improving this directory. Contributions should make the catalogue more accurate, traceable, and safe to use.

## Add or update a listing

1. Confirm the canonical upstream repository URL.
2. Review the upstream README, license, release/commit history, installation steps, dependencies, and required privileges.
3. Record a short factual description without unsupported security or capability claims.
4. Add the repository as a Git submodule under the most relevant tools/ category.
5. Update docs/SELECTION_RATIONALE.md with purpose, review date, license status, known operational risks, and reason for inclusion.
6. Run the local metadata tests and validator.
7. Explain any duplicate category placement in the pull request.

## Safety expectations

- Do not commit API keys, credentials, personal datasets, or downloaded private information.
- Do not claim a tool has been security-reviewed unless the review and scope are documented.
- Do not add tools whose primary purpose is unauthorized access, credential theft, harassment, or invasive collection of private data.
- Keep third-party code as submodules; do not copy it into this repository without checking its license.
- Use least-privilege CI and do not execute unreviewed submodule code in CI.
