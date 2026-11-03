#!/usr/bin/env python3
"""Audit Git submodule entries against .gitmodules without fetching upstream code."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

SAFE_PATH = re.compile(r"^(?!/)(?!.*(?:^|/)\.\.(?:/|$))[A-Za-z0-9._/-]+$")


class AuditError(RuntimeError):
    pass


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise AuditError(result.stderr.strip() or "git command failed")
    return result.stdout


def read_gitlinks(root: Path) -> list[dict]:
    output = git(root, "ls-tree", "-r", "HEAD")
    records = []
    for line in output.splitlines():
        metadata, separator, path = line.partition("\t")
        if not separator:
            continue
        fields = metadata.split()
        if len(fields) == 3 and fields[0] == "160000" and fields[1] == "commit":
            records.append({"path": path, "commit": fields[2]})
    return records


def read_mappings(root: Path) -> list[dict]:
    modules = root / ".gitmodules"
    if not modules.is_file():
        return []
    output = git(root, "config", "-f", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$")
    mappings = []
    for line in output.splitlines():
        key, _, path = line.partition(" ")
        section = key[:-5] if key.endswith(".path") else ""
        url = git(root, "config", "-f", ".gitmodules", "--get", f"{section}.url").strip()
        mappings.append({"path": path.strip(), "url": url, "section": section})
    return mappings


def validate_url(value: str) -> bool:
    parsed = urlsplit(value)
    try:
        port_ok = parsed.port in (None, 443)
    except ValueError:
        return False
    return (
        parsed.scheme == "https"
        and parsed.hostname == "github.com"
        and parsed.username is None
        and parsed.password is None
        and port_ok
        and not parsed.query
        and not parsed.fragment
        and bool(re.fullmatch(r"/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?/?", parsed.path))
    )


def audit(root: str | Path) -> dict:
    root = Path(root).resolve()
    gitlinks = read_gitlinks(root)
    mappings = read_mappings(root)
    errors = []
    warnings = []
    gitlink_paths = [item["path"] for item in gitlinks]
    mapping_paths = [item["path"] for item in mappings]

    for path in gitlink_paths:
        if path not in mapping_paths:
            errors.append({"code": "gitlink_missing_mapping", "path": path})
    for path in mapping_paths:
        if path not in gitlink_paths:
            errors.append({"code": "mapping_missing_gitlink", "path": path})
    for path in mapping_paths:
        if not SAFE_PATH.fullmatch(path):
            errors.append({"code": "unsafe_submodule_path", "path": path})

    duplicate_paths = sorted(path for path, count in _counts(mapping_paths).items() if count > 1)
    for path in duplicate_paths:
        errors.append({"code": "duplicate_mapping_path", "path": path})

    for item in mappings:
        if not validate_url(item["url"]):
            errors.append({"code": "untrusted_or_malformed_url", "path": item["path"]})
    by_url = defaultdict(list)
    for item in mappings:
        by_url[item["url"]].append(item["path"])
    duplicate_urls = [
        {"url": url, "paths": sorted(paths)}
        for url, paths in sorted(by_url.items()) if len(paths) > 1
    ]
    for group in duplicate_urls:
        warnings.append({"code": "upstream_reused_across_categories", **group})

    return {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gitlink_count": len(gitlinks),
        "mapping_count": len(mappings),
        "matched_count": len(set(gitlink_paths) & set(mapping_paths)),
        "duplicate_upstream_url_groups": duplicate_urls,
        "errors": errors,
        "warnings": warnings,
        "gitlinks": gitlinks,
        "mappings": [{"path": item["path"], "url": item["url"]} for item in mappings],
        "limitations": [
            "No upstream network requests or submodule checkout are performed.",
            "A valid URL and pinned commit do not establish upstream safety, maintenance, license rights, or code quality.",
            "Duplicate upstream URLs may be intentional cross-category indexing and are reported as warnings.",
            "The audit validates the current Git tree and .gitmodules, not the full Git history.",
        ],
    }


def _counts(values):
    result = defaultdict(int)
    for value in values:
        result[value] += 1
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        report = audit(args.root)
    except (AuditError, OSError) as error:
        print(f"Submodule audit failed: {error}", file=sys.stderr)
        return 2
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
