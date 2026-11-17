<h1 align="center">travel-guide-planner</h1>

<p align="center">
  <em>A visual-first, concise travel itinerary & A4 lookbook PDF agent skill</em>
</p>

<p align="center">
  <a href="../VERSION"><img src="https://img.shields.io/badge/version-1.0.0-245C68?style=flat-square" alt="Version"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/license-MIT-3E6B5C?style=flat-square" alt="License: MIT"></a>
  <a href="../SKILL.md"><img src="https://img.shields.io/badge/works%20with-Agent%20Skills%20%2F%20Antigravity%20%2F%20Claude%20Code%20%2F%20Codex-B43B2A?style=flat-square" alt="Agent Skills"></a>
</p>

<p align="center">
  <a href="../README.md">简体中文</a> | English
</p>

**travel-guide-planner** turns trip ideas into concise, practical, visual-first itineraries and print-ready 4-page A4 PDF lookbooks. It collects traveler constraints before planning (never assuming a fixed departure city), checks schedule/stamina/budget conflicts, designs zero-backtracking transit routes, embeds local specialty food guides with prices, and validates rendered PDF pages automatically.

## Showcase (4-Page Visual PDF Output)

<table>
  <tr>
    <td align="center" width="50%"><img src="../assets/demo_page_1.png" alt="Page 1 Cover and Budget" width="100%"><br><sub><b>Page 1</b>: Hero cover, KPI badges, weather outfit & proportional budget bars</sub></td>
    <td align="center" width="50%"><img src="../assets/demo_page_2.png" alt="Page 2 Scenic Highlights" width="100%"><br><sub><b>Page 2</b>: 2×2 landmark photo cards & 1×3 neighborhood anchors</sub></td>
  </tr>
  <tr>
    <td align="center" width="50%"><img src="../assets/demo_page_3.png" alt="Page 3 SVG Route and Timeline" width="100%"><br><sub><b>Page 3</b>: Embedded SVG metro map, two-column timeline & Plan B fallbacks</sub></td>
    <td align="center" width="50%"><img src="../assets/demo_page_4.png" alt="Page 4 Food Prices and Checklist" width="100%"><br><sub><b>Page 4</b>: Local food photo banners, 6-card price matrix & quick checklist</sub></td>
  </tr>
</table>

## Key Capabilities

- **Pre-Inquiry Gate (No Hardcoded Origin)**: Always collects or confirms departure city, destination, exact arrival/departure windows, discount eligibility (student/senior IDs), dietary/spice tolerance, budget scope, and stamina rules (such as cable-car / shuttle routes for no-hiking travelers).
- **Concise & Visual-First**: Compresses verbose itineraries into a scannable 4-page layout (`~1,800–2,600` non-whitespace CJK characters) led by photos, price badges, proportional budget bars, and SVG transit diagrams.
- **Route-Integrated Local Cuisine**: Covers sit-down local restaurants, breakfast dishes, street snacks/drinks, and night markets with real dish recommendations, price ranges, spice notes, and queue alternatives.
- **Automated PDF Export & Visual QA**: Includes [`scripts/export_pdf.py`](../scripts/export_pdf.py) using headless Edge/Chrome + `PyMuPDF` to verify page counts, character density, and per-page PNG renders.

## Quick Install

```bash
npx skills add CJG0712/travel-guide-planner -g
```

Or clone directly into your agent's skills directory (e.g., `~/.gemini/config/skills/travel-guide-planner` for Antigravity or `~/.claude/skills/travel-guide-planner` for Claude Code).

## License

MIT License. See [`LICENSE`](../LICENSE). Note that optional `PyMuPDF` is licensed under AGPL-3.0 (see [`requirements.txt`](../requirements.txt)).
