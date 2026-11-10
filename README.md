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

<!-- # Strict Anti-Generic AI Design -->
## Supported Agent Harnesses

The installer auto-detects and installs into both global user directories and project-local workspaces:

| Agent Harness | Supported Location | Detection Target | Integration Status |
|---|---|---|---|
| **Antigravity** | `~/.gemini/config/skills/cua_driver_acceleration/` | Global config & project `.gemini/` | **Verified** |
| **Claude Code** | `~/.claude/skills/` or `./.claude/skills/` | Global & Workspace | **Verified** |
| **OpenAI Codex** | `~/.codex/skills/` or `./.codex/skills/` | `$CODEX_HOME` & Workspace | **Verified** |
| **Cursor** | `./.cursor/skills/` or `.cursorrules` | Project Workspace | **Verified** |
| **OpenCode** | `~/.config/opencode/skills/` or `./.opencode/skills/` | Global & Workspace | **Supported** |
| **Windsurf (Codeium)** | `~/.codeium/windsurf/skills/` or `./.windsurf/skills/` | Global & Workspace | **Supported** |
| **Roo Code / Cline** | `./.roo/skills/` or `./.cline/skills/` | Project Workspace | **Supported** |
| **Universal Standard** | `~/.agents/skills/` or `./.agents/skills/` | Universal Agent Spec | **Supported** |

---

## The Problem

Most computer-use agents suffer from massive latency—often taking 20 to 60 seconds per routine multi-step workflow. This lag is almost never caused by the operating system, but by predictable agent failure modes:

1. **Ad-Hoc Wrapper Script Inflation:** Authoring throwaway 30-line Python scripts (`subprocess`, `pyautogui`) for a single click.
2. **Coordinate Guesswork:** Taking a screenshot and waiting 3-5 seconds for a multimodal vision model to guess `(x, y)` pixels (which often drifts with DPI scaling).
3. **Multi-Turn Roundtrips:** Decomposing routine tasks into 14–16 turns of `click -> screenshot -> think -> click` loops.
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

## Supported Backends

Both backends interface directly with operating system accessibility APIs (Windows UI Automation; macOS AX and Linux AT-SPI supported by upstream engines) to provide sub-200ms DOM-style interaction without pixel guessing:

- **[Vercel agent-desktop](https://github.com/vercel-labs/agent-desktop)**: Open-source Rust CLI from Vercel Labs. Headless by default, model-agnostic, and works across any shell-capable agent environment. Recommended default (`npm i -g agent-desktop`).
- **[cua-driver](https://cua.ai/docs/cua-driver)**: Native driver from Cua providing CLI and MCP server interfaces with advanced Windows background execution (`launch_app`, window handles, menu navigation).

---

## Setup & Reference Guides

Comprehensive reference documentation is included directly in the repository:

- 📖 **[Backend Setup & Permissions (`references/setup.md`)](references/setup.md)**: Step-by-step installation, permissions configuration (macOS Accessibility, Linux AT-SPI, Windows UIA), and environment verification for both backends.
- ⚡ **[CLI Cheat-Sheet (`references/backends.md`)](references/backends.md)**: Side-by-side command syntax for inspecting state (DOM tree snapshots, window lists) and dispatching actions (clicks, text input, hotkeys) across `agent-desktop` and `cua-driver`.
- 🔗 **[Native OS Shortcuts (`references/native-shortcuts.md`)](references/native-shortcuts.md)**: Index of Windows URI schemes (`ms-settings:`), deep links, and OS-level shortcuts to navigate directly to target settings without analog GUI clicking.
- 🛡️ **[Skill Definition (`SKILL.md`)](SKILL.md)**: The operational invariants, single-turn batch chaining instructions, and deterministic fallback recovery rules loaded into agent runtimes.

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

<!-- # Strict Anti-Generic AI Design -->
```text
cua_driver_acceleration/
├── bin/
│   └── cli.js                   # Zero-dependency NPX skill installer
├── docs/
│   └── CUA_Acceleration_Technical_Report.pdf  # 7-page empirical technical report
├── assets/
│   └── benchmark-comparison.png # Comparative evaluation graphic
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
    ├── benchmark-harness.py     # Task definitions, prompt schemas & validation harness
    ├── data/
    │   ├── benchmark-data.json  # Reproducible empirical dataset & timings
    │   └── raw-trials.json      # Raw trial-by-trial execution records (N=25)
    ├── generate-report-pdf.py   # Publication-grade technical report PDF generator
    ├── render-benchmark.py      # Benchmark evaluation infographic generator
    └── verify-benchmark-data.py # Automated dataset arithmetic verification harness
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
