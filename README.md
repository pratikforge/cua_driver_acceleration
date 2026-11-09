# fast-computer-use

An agent skill that makes desktop automation (computer use / CUA) significantly faster by optimizing **how the agent operates**, regardless of the underlying driver.

## The Problem

Standard computer-use agents often default to high-latency habits:

- Writing throwaway 30-line Python scripts to execute a single click.
- Taking screenshots and guessing `(x, y)` pixel coordinates.
- Decomposing simple 3-step tasks into 15-20 turns of click -> screenshot -> think loops.
- Navigating nested GUI menus when native deep links (e.g. `ms-settings:display`) exist.

Each unneeded layer introduces multi-second overhead. This skill eliminates those bottlenecks.

## Core Invariants

| Inefficient Pattern | Fast Invariant |
|---|---|
| Ad-hoc Python wrapper scripts | One-line direct backend CLI calls |
| Screenshot + pixel guessing | Accessibility-tree snapshot + element refs (50-200 ms) |
| Multi-turn micro-loops | Single-turn synchronous task execution |
| Manual GUI menu navigation | Native deep links, URI schemes, CLIs, and direct config edits |
| Screenshot after every step | Read JSON exit state; capture only at completion or unrecoverable error |

## Self-Bootstrapping Workflow

On first use, the agent runs a read-only environment check (`scripts/check-setup.ps1` or `scripts/check-setup.sh`) to detect available drivers. If no driver is present, it recommends the optimal installer and waits for explicit user approval before proceeding.

## Supported Backends

Both backends interact directly with native operating system accessibility APIs (Windows UI Automation, macOS AX, Linux AT-SPI) to provide sub-200ms DOM-style interaction without pixel guessing:

- **[Vercel agent-desktop](https://github.com/vercel-labs/agent-desktop)**: Open-source Rust CLI from Vercel Labs. Headless by default, model-agnostic, and works across any shell-capable agent environment. Recommended default (`npm i -g agent-desktop`).
- **[cua-driver](https://cua.ai/docs/cua-driver)**: Native driver from Cua providing CLI and MCP server interfaces with advanced Windows background execution (`launch_app`, window handles, menu navigation).

## Installation

Clone the repository into your agent's skills directory:

```bash
git clone https://github.com/pratikforge/fast-computer-use
```

| Agent Platform | Installation Path |
|---|---|
| **Antigravity** | `~/.gemini/config/skills/fast-computer-use/` |
| **Claude Code** | `~/.claude/skills/fast-computer-use/` (or project `.claude/skills/`) |
| **Cursor / Codex / Windsurf** | Add repository to project skills or paste `SKILL.md` into `.cursorrules` / instructions |

Once installed, simply request any desktop automation task. The agent automatically activates the skill and runs the fast-path loop.

## Repository Structure

```text
fast-computer-use/
├── SKILL.md                     # Agent operational rules & invariants
├── LICENSE                      # MIT License
├── README.md                    # Overview and setup guide
├── references/
│   ├── setup.md                 # Backend installation, permissions & troubleshooting
│   ├── backends.md              # cua-driver vs agent-desktop command reference
│   └── native-shortcuts.md      # OS URI schemes, deep links & CLI shortcuts
└── scripts/
    ├── check-setup.ps1          # Read-only environment check (Windows)
    └── check-setup.sh           # Read-only environment check (macOS / Linux)
```

## Security & Privacy

- Environment check scripts are strictly read-only and perform zero network requests or disk alterations.
- Remote installer scripts (`curl | bash`, `irm | iex`) are never executed autonomously without explicit user confirmation.
- OS accessibility permissions must be granted directly by the user on platforms enforcing security boundaries (macOS Privacy & Security).

## License

[MIT](LICENSE) © 2026 pratikforge
