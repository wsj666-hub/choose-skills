#!/usr/bin/env python3
"""Catalog locally installed Codex-compatible skills."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOTS = [
    ("codex", Path.home() / ".codex" / "skills"),
    ("agents", Path.home() / ".agents" / "skills"),
]


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}

    data: dict[str, str] = {}
    lines = match.group(1).splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue

        if stripped.startswith("name:"):
            data["name"] = stripped.split(":", 1)[1].strip().strip("\"'")
            i += 1
            continue

        if stripped.startswith("description:"):
            value = stripped.split(":", 1)[1].strip()
            if value in {"|", ">"}:
                i += 1
                block: list[str] = []
                while i < len(lines):
                    next_line = lines[i]
                    if next_line.startswith("  ") or next_line.startswith("\t"):
                        block.append(next_line.strip())
                        i += 1
                        continue
                    if not next_line.strip():
                        i += 1
                        continue
                    break
                data["description"] = " ".join(part for part in block if part)
                continue

            data["description"] = value.strip("\"'")
            i += 1
            continue

        i += 1

    return data


def fallback_summary(text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    body = text[match.end() :] if match else text
    for line in body.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped
    return ""


def priority(item: dict[str, str]) -> tuple[int, int, str]:
    source_rank = 0 if item["source"] == "codex" else 1
    backup_penalty = 1 if ".backup" in item["path"] else 0
    return (source_rank, backup_penalty, item["path"])


def collect_skills() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for source, root in ROOTS:
        if not root.exists():
            continue
        for skill_md in sorted(root.glob("*/SKILL.md")):
            text = skill_md.read_text(encoding="utf-8")
            meta = parse_frontmatter(text)
            name = meta.get("name") or skill_md.parent.name
            description = meta.get("description") or fallback_summary(text)
            entries.append(
                {
                    "name": name,
                    "description": description,
                    "source": source,
                    "path": str(skill_md.parent),
                }
            )

    deduped: dict[str, dict[str, str]] = {}
    for entry in sorted(entries, key=priority):
        deduped.setdefault(entry["name"], entry)

    return sorted(
        deduped.values(),
        key=lambda item: (0 if item["source"] == "codex" else 1, item["name"]),
    )


def main() -> None:
    print(json.dumps(collect_skills(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
