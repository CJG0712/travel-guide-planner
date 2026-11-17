#!/usr/bin/env python3
"""Validate travel-guide-planner skill package structure, metadata, and links."""

from __future__ import annotations

import py_compile
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/workflows/validate.yml",
    ".gitignore",
    "LICENSE",
    "README.md",
    "SKILL.md",
    "VERSION",
    "agents/openai.yaml",
    "assets/demo_page_1.png",
    "assets/demo_page_2.png",
    "assets/demo_page_3.png",
    "assets/demo_page_4.png",
    "examples/lookbook-template.html",
    "readmes/README.en.md",
    "references/itinerary-template.md",
    "references/visual-pdf-blueprint.md",
    "requirements.txt",
    "scripts/export_pdf.py",
    "scripts/validate_skill.py",
]

MARKDOWN_FILES_FOR_LINK_CHECK = [
    "SKILL.md",
    "README.md",
    "readmes/README.en.md",
    "references/itinerary-template.md",
    "references/visual-pdf-blueprint.md",
]

LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)#\s]+)(?:#[^)\s]*)?\)")


def validate_required_files() -> None:
    missing = [rel for rel in REQUIRED_FILES if not (ROOT / rel).is_file()]
    if missing:
        raise AssertionError(f"Missing required files: {missing}")


def validate_skill_frontmatter() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError("SKILL.md must start with YAML frontmatter '---'")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise AssertionError("SKILL.md frontmatter closing '---' not found")
    fm = yaml.safe_load(parts[1])
    if not isinstance(fm, dict) or set(fm.keys()) != {"name", "description"}:
        raise AssertionError(f"SKILL.md frontmatter must contain only name and description, got: {fm}")
    if fm["name"] != "travel-guide-planner":
        raise AssertionError(f"Unexpected skill name: {fm['name']}")
    if not isinstance(fm["description"], str) or len(fm["description"].strip()) < 20:
        raise AssertionError("SKILL.md description is missing or too short")


def validate_version_and_agents() -> str:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise AssertionError(f"VERSION must follow semver X.Y.Z, got: {version!r}")

    openai_cfg = yaml.safe_load((ROOT / "agents/openai.yaml").read_text(encoding="utf-8"))
    iface = openai_cfg.get("interface", {})
    for key in ("display_name", "short_description", "default_prompt"):
        if not iface.get(key):
            raise AssertionError(f"agents/openai.yaml missing interface.{key}")
    if "$travel-guide-planner" not in iface["default_prompt"]:
        raise AssertionError("agents/openai.yaml default_prompt must mention $travel-guide-planner")
    return version


def validate_markdown_links() -> None:
    broken: list[str] = []
    for rel in MARKDOWN_FILES_FOR_LINK_CHECK:
        md_path = ROOT / rel
        content = md_path.read_text(encoding="utf-8")
        for target in LINK_PATTERN.findall(content):
            if target.startswith(("http://", "https://", "mailto:", "file://")):
                continue
            resolved = (md_path.parent / target).resolve()
            if not resolved.exists():
                broken.append(f"{rel} -> {target}")
    if broken:
        raise AssertionError(f"Broken relative links found: {broken}")


def validate_scripts_and_templates() -> None:
    for py_rel in ("scripts/export_pdf.py", "scripts/validate_skill.py"):
        py_compile.compile(str(ROOT / py_rel), doraise=True)

    html = (ROOT / "examples/lookbook-template.html").read_text(encoding="utf-8")
    for token in ("@page", "size: A4 portrait", "print-color-adjust: exact", "svg-leg"):
        if token not in html:
            raise AssertionError(f"examples/lookbook-template.html missing expected pattern: {token}")


def main() -> int:
    try:
        validate_required_files()
        validate_skill_frontmatter()
        version = validate_version_and_agents()
        validate_markdown_links()
        validate_scripts_and_templates()
    except Exception as exc:
        print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        return 1

    print(f"validation ok: travel-guide-planner v{version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
