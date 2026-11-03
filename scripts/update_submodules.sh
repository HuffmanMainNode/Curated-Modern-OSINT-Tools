#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <submodule-path>" >&2
  echo "Updates exactly one configured submodule after interactive confirmation." >&2
}

if [[ $# -ne 1 ]]; then
  usage
  exit 2
fi

target=$1
if [[ "$target" == /* || "$target" == *".."* || "$target" != tools/* ]]; then
  echo "Refusing unsafe submodule path: $target" >&2
  exit 2
fi

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Run this script from inside a Git working tree." >&2
  exit 2
fi

section=$(
  git config -f .gitmodules --get-regexp '^submodule\..*\.path$' |
    awk -v target="$target" '$2 == target { sub(/\.path$/, "", $1); print $1 }'
) || true

if [[ -z "$section" ]]; then
  echo "No .gitmodules entry matches: $target" >&2
  exit 2
fi

matches=$(printf '%s\n' "$section" | wc -l | tr -d ' ')
if [[ "$matches" != "1" ]]; then
  echo "Path must map to exactly one submodule entry: $target" >&2
  exit 2
fi

url=$(git config -f .gitmodules --get "$section.url")
case "$url" in
  https://github.com/*/*|https://github.com/*/*.git) ;;
  *)
    echo "Refusing non-canonical upstream URL: $url" >&2
    exit 2
    ;;
esac

current=$(git ls-tree HEAD -- "$target" | awk '{print $3}')
echo "Submodule: $target"
echo "Upstream:  $url"
echo "Pinned:    ${current:-unknown}"
echo "This fetches the configured upstream branch for this one submodule."
read -r -p "Continue? Type 'yes' to proceed: " confirmation
if [[ "$confirmation" != "yes" ]]; then
  echo "No changes made."
  exit 0
fi

git submodule update --init --remote --checkout -- "$target"
echo
echo "Review the pointer change before committing:"
git diff --submodule=log -- "$target"
echo
echo "No commit was created. Inspect upstream changes and tests before staging the new pointer."
