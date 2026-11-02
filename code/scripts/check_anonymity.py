#!/usr/bin/env python3
"""Conservative identity and machine-path scan for the anonymous artifact."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", ".venv", "outputs"}
TEXT_SUFFIXES = {
    "", ".cfg", ".csv", ".ini", ".json", ".jsonl", ".md", ".py", ".sh", ".toml", ".txt", ".yaml", ".yml"
}
PATTERNS = {
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "absolute user or cluster path": re.compile(r"/(?:home|Users|gpfs|nfs|scratch)/[^\s'\"`]+"),
    "scheduler account": re.compile(r"(?:SBATCH\s+--account|--account=)", re.I),
    "possible ORCID": re.compile(r"\b\d{4}-\d{4}-\d{4}-\d{3}[\dX]\b"),
}


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        if path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"binary or non-UTF8 text-like file: {path.relative_to(root)}")
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            for label, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append(f"{path.relative_to(root)}:{line_number}: {label}")
    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    findings = scan(args.root.resolve())
    if findings:
        print("Anonymization scan failed:")
        print("\n".join(f"- {finding}" for finding in findings))
        raise SystemExit(1)
    print("Anonymization scan passed: no configured identity or machine-path patterns found.")


if __name__ == "__main__":
    main()
