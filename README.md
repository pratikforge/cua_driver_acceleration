# cua_driver_acceleration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![npx](https://img.shields.io/badge/npx-cua__driver__acceleration-000000?logo=npm&logoColor=white)](https://github.com/pratikforge/cua_driver_acceleration)
[![Platform](https://img.shields.io/badge/platform-Windows%2011%20(tested)%20%7C%20Cross--Platform%20CLI-lightgrey.svg)](https://github.com/pratikforge/cua_driver_acceleration)
[![Accessibility-First](https://img.shields.io/badge/DOM%2FAccessibility-Sub--200ms-brightgreen.svg)](https://github.com/pratikforge/cua_driver_acceleration)

A high-performance agent skill and one-command CLI that accelerates desktop automation (computer use / CUA) by eliminating multi-second agent latency.

---

## Quickstart (Zero Clone Required)

Run directly in your terminal via `npx` to auto-detect your AI agent environments (Antigravity, Claude Code, Cursor, Codex) and install the skill instantly:

```bash
npx github:pratikforge/cua_driver_acceleration
```

*Or via the npm package:*

```bash
npx cua_driver_acceleration
```

### CLI Options & Targeting

```bash
# Check installed drivers (read-only audit without writing files)
npx github:pratikforge/cua_driver_acceleration --check

# Auto-detect all active agent harnesses and install
npx github:pratikforge/cua_driver_acceleration

# Target specific agent harnesses
npx github:pratikforge/cua_driver_acceleration --target antigravity
npx github:pratikforge/cua_driver_acceleration --target claude
npx github:pratikforge/cua_driver_acceleration --target codex
npx github:pratikforge/cua_driver_acceleration --target opencode
npx github:pratikforge/cua_driver_acceleration --target cursor
npx github:pratikforge/cua_driver_acceleration --target windsurf
npx github:pratikforge/cua_driver_acceleration --target roo
npx github:pratikforge/cua_driver_acceleration --target universal

# Install into a custom directory
npx github:pratikforge/cua_driver_acceleration --path ./my-agent/skills
```

---

## Supported Agent Harnesses

The installer auto-detects and installs into both global user directories and project-local workspaces:

| Agent Harness | Supported Location | Detection Target |
|---|---|---|
| **Antigravity** | `~/.gemini/config/skills/cua_driver_acceleration/` | Global config |
| **Claude Code** | `~/.claude/skills/` or `./.claude/skills/` | Global & Workspace |
| **OpenAI Codex** | `~/.codex/skills/` or `./.codex/skills/` | `$CODEX_HOME` & Workspace |
| **OpenCode** | `~/.config/opencode/skills/` or `./.opencode/skills/` | Global & Workspace |
| **Cursor** | `./.cursor/skills/` or `.cursorrules` | Project Workspace |
| **Windsurf (Codeium)** | `~/.codeium/windsurf/skills/` or `./.windsurf/skills/` | Global & Workspace |
| **Roo Code / Cline** | `./.roo/skills/` or `./.cline/skills/` | Project Workspace |
| **Universal Standard** | `~/.agents/skills/` or `./.agents/skills/` | Universal Agent Spec |

---

## The Problem

Most computer-use agents suffer from massive latency—often taking 20 to 60 seconds for simple actions. This lag is almost never caused by the operating system, but by predictable agent failure modes:

1. **Ad-Hoc Wrapper Script Inflation:** Authoring throwaway 30-line Python scripts (`subprocess`, `pyautogui`) for a single click.
2. **Coordinate Guesswork:** Taking a screenshot and waiting 3-5 seconds for a multimodal vision model to guess `(x, y)` pixels (which often drifts with DPI scaling).
3. **Multi-Turn Roundtrips:** Decomposing simple 3-step tasks into 15-20 turns of `click -> screenshot -> think -> click` loops.
4. **Analog Navigation:** Clicking through menus when native deep links (e.g. `ms-settings:display`) exist.

---

## Core Invariants

| Legacy Agent Pattern | Accelerated Invariant |
|---|---|
| Ad-hoc Python wrapper scripts | One-line direct backend CLI calls |
| Screenshot + pixel guessing | Accessibility-tree snapshot + element refs (50-200 ms) |
| Multi-turn micro-loops | Single-turn synchronous task execution |
| Manual GUI menu navigation | Native deep links, URI schemes, CLIs, and direct config edits |
| Screenshot after every step | Read JSON exit state; capture only at completion or unrecoverable error |

---

## Empirical Benchmarks: Pre-Acceleration vs. Post-Acceleration

Evaluation conducted across standardized operating system navigation, UIAutomation trace logs, OSWorld desktop automation subsets, and latency profiling on Windows 11 Pro (x64):

<p align="center">
  <img src="assets/benchmark-comparison.png" alt="CUA Driver Acceleration Benchmark Comparison: Pre-Acceleration vs. Post-Acceleration" width="100%" />
</p>

> **Methodology:** Evaluated on Windows 11 Pro 24H2 (Intel Core i7-13700H, 32GB RAM, UIA Provider v3) across standardized desktop navigation, UIAutomation trace logs, OSWorld desktop automation subsets, and latency profiling. Pre-acceleration measures legacy agent loops relying on multimodal screenshots, Python wrapper scripts (`pyautogui`/`subprocess`), and coordinate guessing. Post-acceleration measures direct accessibility tree snapshots, native stdin pipe dispatch, and OS URI deep links. (Note: Only Windows 11 Pro was empirically benchmarked; macOS and Linux driver backends exist in the underlying engine architectures but were not measured in this dataset).

> 📄 **Technical Report (PDF):** For the complete empirical research whitepaper covering experimental setup, latency dissections, token economics, ablation studies, and qualitative trace logs, download the [CUA Acceleration Technical Report (PDF)](docs/CUA_Acceleration_Technical_Report.pdf).

---

## Supported Backends

Both backends interface directly with operating system accessibility APIs (Windows UI Automation; macOS AX and Linux AT-SPI supported by upstream engines) to provide sub-200ms DOM-style interaction without pixel guessing:

- **[Vercel agent-desktop](https://github.com/vercel-labs/agent-desktop)**: Open-source Rust CLI from Vercel Labs. Headless by default, model-agnostic, and works across any shell-capable agent environment. Recommended default (`npm i -g agent-desktop`).
- **[cua-driver](https://cua.ai/docs/cua-driver)**: Native driver from Cua providing CLI and MCP server interfaces with advanced Windows background execution (`launch_app`, window handles, menu navigation).

---

## Alternative Manual Installation

If you prefer cloning manually into your agent's skills directory:

```bash
git clone https://github.com/pratikforge/cua_driver_acceleration.git
```

| Agent Platform | Global Skills Location |
|---|---|
| **Antigravity** | `~/.gemini/config/skills/cua_driver_acceleration/` |
| **Claude Code** | `~/.claude/skills/cua_driver_acceleration/` (or project `.claude/skills/`) |
| **Cursor / Codex / Windsurf** | Add to project skills directory or copy `SKILL.md` into `.cursorrules` / instructions |

---

## Repository Structure

```text
cua_driver_acceleration/
├── bin/
│   └── cli.js                   # Zero-dependency NPX skill installer
├── docs/
│   └── CUA_Acceleration_Technical_Report.pdf  # 6-page empirical research whitepaper
├── assets/
│   └── benchmark-comparison.png # High-resolution DeepMind-style evaluation graphic
├── SKILL.md                     # Agent operational rules & invariants
├── LICENSE                      # Full MIT License text
├── README.md                    # Overview, quickstart & documentation
├── package.json                 # NPX executable & npm package definition
├── references/
│   ├── setup.md                 # Backend installation, permissions & troubleshooting
│   ├── backends.md              # cua-driver vs agent-desktop command reference
│   └── native-shortcuts.md      # OS URI schemes, deep links & CLI shortcuts
└── scripts/
    ├── check-setup.ps1          # Read-only environment check (Windows)
    ├── check-setup.sh           # Read-only environment check (macOS / Linux)
    ├── generate-report-pdf.py   # Publication-grade technical report PDF generator
    └── render-benchmark.py      # Benchmark evaluation infographic generator
```

---

## Security & Safety Guarantees

- **Read-Only Audit:** The `--check` command and setup scripts inspect only environment paths and binary availability; they perform zero network requests or disk modifications.
- **Explicit Consent:** Remote installer scripts (`curl | bash`, `irm | iex`) are never executed autonomously without explicit user confirmation.
- **Zero Telemetry:** The skill and CLI contain no tracking, analytics, or external phone-home mechanisms.

---

## License & Legal

This project is licensed under the terms of the **MIT License**.

```text
MIT License

Copyright (c) 2026 pratikforge

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Rights & Permissions Summary

- **Commercial Use:** Permitted for both personal and enterprise production environments.
- **Modification:** Permitted to fork, edit, and adapt invariants for custom agent architectures.
- **Distribution:** Permitted to bundle and distribute with other agent frameworks.
- **Private Use:** Permitted to use without disclosing source modifications.
- **Disclaimer:** The software is provided "as is", without warranty of any kind. Automated computer actions executed by AI agents remain under the operator's supervision.

For complete legal terms, review the full [LICENSE](LICENSE) file.
