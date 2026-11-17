#!/usr/bin/env python3
"""Compile a visual travel guide HTML file to A4 PDF and render per-page PNG previews.

Uses Microsoft Edge or Chrome/Chromium headless printing for exact CSS fidelity,
then uses PyMuPDF (if installed) to report character/page metrics and export
per-page PNG screenshots for visual QA.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


BROWSER_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "msedge",
    "microsoft-edge",
    "google-chrome",
    "chromium",
    "chromium-browser",
]


def find_browser(explicit_path: str | None = None) -> str:
    """Locate a headless Chromium-based browser executable."""
    if explicit_path:
        resolved = shutil.which(explicit_path) or (explicit_path if os.path.isfile(explicit_path) else None)
        if not resolved:
            raise FileNotFoundError(f"Browser executable not found: {explicit_path}")
        return resolved

    for candidate in BROWSER_CANDIDATES:
        if os.path.isfile(candidate):
            return candidate
        which_hit = shutil.which(candidate)
        if which_hit:
            return which_hit

    raise FileNotFoundError(
        "No Edge/Chrome/Chromium binary found. Pass --browser <path> explicitly."
    )


def render_pdf(browser_exe: str, html_path: Path, out_pdf: Path) -> None:
    """Print HTML file to PDF via headless browser."""
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    html_uri = html_path.resolve().as_uri()
    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={out_pdf.resolve()}",
        html_uri,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0 or not out_pdf.is_file():
        raise RuntimeError(
            f"Headless PDF export failed (code {result.returncode}): {result.stderr.strip()}"
        )


def inspect_and_export_previews(out_pdf: Path, preview_dir: Path | None, dpi: int) -> None:
    """Inspect generated PDF metrics via PyMuPDF and optionally export PNG previews."""
    try:
        import pymupdf
    except ImportError:
        size_kb = out_pdf.stat().st_size / 1024
        print(f"Generated PDF: {out_pdf} | Size: {size_kb:.1f} KB")
        print("Note: PyMuPDF is not installed; skipping char count and PNG preview rendering.")
        return

    doc = pymupdf.open(out_pdf)
    page_chars = [len("".join(page.get_text().split())) for page in doc]
    total_chars = sum(page_chars)
    rect = doc[0].rect if len(doc) > 0 else None
    dims_mm = f"{rect.width * 25.4 / 72:.1f}x{rect.height * 25.4 / 72:.1f}mm" if rect else "n/a"
    size_kb = out_pdf.stat().st_size / 1024

    print(
        f"Generated PDF: {out_pdf} | Pages: {len(doc)} ({dims_mm}) | "
        f"Non-ws chars: {total_chars} {page_chars} | Size: {size_kb:.1f} KB"
    )
    if len(doc) > 1 and page_chars[-1] < 180:
        print(
            f"WARNING: Trailing page {len(doc)} has only {page_chars[-1]} non-ws chars; "
            "consider tightening margins/spacing to eliminate overflow."
        )

    if preview_dir:
        preview_dir.mkdir(parents=True, exist_ok=True)
        for idx, page in enumerate(doc, start=1):
            out_png = preview_dir / f"pdf_page_{idx}.png"
            page.get_pixmap(dpi=dpi).save(out_png)
            print(f"Rendered page {idx} -> {out_png}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export travel lookbook HTML to A4 PDF with PNG QA.")
    parser.add_argument("--html", required=True, help="Path to source HTML file.")
    parser.add_argument("--out", required=True, help="Destination PDF file path.")
    parser.add_argument("--preview-dir", default="", help="Optional directory to write pdf_page_*.png.")
    parser.add_argument("--dpi", type=int, default=160, help="PNG preview render DPI (default: 160).")
    parser.add_argument("--browser", default="", help="Optional path to Edge/Chrome executable.")
    args = parser.parse_args()

    html_path = Path(args.html)
    if not html_path.is_file():
        print(f"Error: HTML file not found: {html_path}", file=sys.stderr)
        return 1

    browser_exe = find_browser(args.browser or None)
    out_pdf = Path(args.out)
    preview_dir = Path(args.preview_dir) if args.preview_dir else None

    render_pdf(browser_exe, html_path, out_pdf)
    inspect_and_export_previews(out_pdf, preview_dir, args.dpi)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
