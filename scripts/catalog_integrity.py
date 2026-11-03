#!/usr/bin/env python3
"""Validate Git submodule metadata without cloning or executing upstream tools."""
from __future__ import annotations
import argparse, configparser, json, subprocess, sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

def read_gitlink_paths(root: Path) -> set[str]:
    result = subprocess.run(["git", "ls-files", "--stage"], cwd=root, check=True, capture_output=True, text=True)
    paths=set()
    for line in result.stdout.splitlines():
        try:
            metadata,path=line.split("\t",1)
            if metadata.split()[0]=="160000": paths.add(path)
        except ValueError: continue
    return paths

def audit_submodules(root: str | Path, gitlink_paths: set[str] | None = None) -> dict:
    root=Path(root); modules_file=root/".gitmodules"
    parser=configparser.ConfigParser(interpolation=None, strict=False)
    errors=[]; warnings=[]; records=[]
    if not modules_file.is_file():
        return {"schema_version":"1.0.0","submodule_count":0,"errors":["missing .gitmodules"],"warnings":[],"duplicate_url_groups":[],"records":[]}
    try: parser.read(modules_file,encoding="utf-8")
    except (OSError,configparser.Error) as error:
        return {"schema_version":"1.0.0","submodule_count":0,"errors":[f"cannot parse .gitmodules: {type(error).__name__}"],"warnings":[],"duplicate_url_groups":[],"records":[]}
    paths_seen={}; urls_seen=defaultdict(list)
    for section in parser.sections():
        path=parser.get(section,"path",fallback="").strip()
        url=parser.get(section,"url",fallback="").strip()
        if not path: errors.append(f"{section}: missing path")
        elif path in paths_seen: errors.append(f"duplicate submodule path: {path}")
        else: paths_seen[path]=section
        parsed=urlsplit(url)
        try: port_ok=parsed.port in (None,443)
        except ValueError: port_ok=False
        parts=[part for part in parsed.path.strip("/").split("/") if part]
        valid=(parsed.scheme=="https" and parsed.hostname=="github.com" and parsed.username is None and parsed.password is None and port_ok and not parsed.query and not parsed.fragment and len(parts)==2)
        if not valid: errors.append(f"{section}: URL must be HTTPS github.com/owner/repository")
        else: urls_seen[("https://github.com/"+parsed.path.strip("/").removesuffix(".git").lower())].append(path)
        if path and (path.startswith("/") or ".." in Path(path).parts or not path.startswith("tools/")):
            errors.append(f"{section}: unsafe or unexpected submodule path: {path}")
        records.append({"name":section,"path":path,"url":url})
    duplicates=[{"url":url,"paths":sorted(paths)} for url,paths in sorted(urls_seen.items()) if len(paths)>1]
    for group in duplicates: warnings.append(f"upstream appears in multiple categories: {group['url']} ({len(group['paths'])} paths)")
    if gitlink_paths is not None:
        configured={r["path"] for r in records if r["path"]}
        for path in sorted(configured-gitlink_paths): errors.append(f".gitmodules path has no tracked gitlink: {path}")
        for path in sorted(gitlink_paths-configured): errors.append(f"tracked gitlink has no .gitmodules entry: {path}")
    return {"schema_version":"1.0.0","submodule_count":len(records),"unique_upstream_count":len(urls_seen),"duplicate_url_group_count":len(duplicates),"errors":errors,"warnings":warnings,"duplicate_url_groups":duplicates,"records":sorted(records,key=lambda x:x["path"]),"interpretation":{"duplicate_urls":"May be intentional multi-category indexing; review rather than delete.","validation_scope":"Metadata and Git index consistency only. No upstream code, license, maintenance, safety, or security review is performed."}}

def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--root",default="."); parser.add_argument("--output"); args=parser.parse_args(argv)
    try:
        root=Path(args.root); report=audit_submodules(root,read_gitlink_paths(root))
    except (OSError,subprocess.CalledProcessError) as error:
        print(f"Catalog validation failed: {type(error).__name__}",file=sys.stderr); return 2
    rendered=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if args.output:
        output=Path(args.output); output.parent.mkdir(parents=True,exist_ok=True); output.write_text(rendered,encoding="utf-8")
    else: print(rendered,end="")
    return 1 if report["errors"] else 0

if __name__=="__main__": raise SystemExit(main())
