# Setup

Pick **one** backend. Both read the OS accessibility tree (Windows UI Automation, macOS AX, Linux AT-SPI), so both avoid screenshot-based guessing.

> The agent shows these commands to the user and waits for approval before running any of them.

---

## Option A — Vercel agent-desktop (recommended for most agents)

Open-source Rust CLI from Vercel Labs. Works with any agent that can run shell commands (Claude Code, Cursor, Codex, Gemini CLI, Antigravity, custom harnesses). Headless by default: it does not move the real cursor or steal focus.

Repo: https://github.com/vercel-labs/agent-desktop
Docs: https://agent-browser.dev/desktop/

**Prerequisite:** Node.js 18+ (for the npm route).

| Platform | Install |
|---|---|
| Any (npm) | `npm install -g agent-desktop` |
| macOS / Linux (Homebrew) | `brew install agent-desktop` |
| From source | `git clone https://github.com/vercel-labs/agent-desktop && cd agent-desktop && cargo build --release -p agent-desktop` |

**Verify:**

```bash
agent-desktop status
agent-desktop --help
```

**Permissions:**

```bash
agent-desktop permissions --guide
```

- macOS: grant Accessibility to the terminal / agent host app in System Settings → Privacy & Security → Accessibility.
- Linux: AT-SPI must be enabled (on by default in GNOME/KDE; check `gsettings get org.gnome.desktop.interface toolkit-accessibility`).
- Windows: no extra permissions for normal user-level apps. Elevated (admin) windows need an elevated agent process.

---

## Option B — cua-driver

Native driver from Cua with a CLI and an MCP server. Ships with Antigravity setups and has extra Windows features (focus-safe `launch_app`, menu paths, recording).

Docs: https://cua.ai/docs/cua-driver

| Platform | Install |
|---|---|
| macOS / Linux | `/bin/bash -c "$(curl -fsSL https://cua.ai/driver/install.sh)"` |
| Windows (PowerShell) | `irm https://cua.ai/driver/install.ps1 \| iex` |

**Verify:**

```bash
cua-driver --version
cua-driver --help
```

**Optional:** install cua-driver's own detailed skill alongside this one:

```bash
cua-driver skills install
```

**Permissions:**

- macOS: grant Accessibility **and** Screen Recording to `CuaDriver.app`.
- Windows: first run may trigger SmartScreen; choose "More info → Run anyway" if the user trusts it.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `command not found` after install | Open a new terminal so PATH refreshes. npm global bin must be on PATH (`npm config get prefix`). |
| Snapshot returns empty tree (macOS) | Accessibility permission missing for the host process. Re-grant and restart the host app. |
| Clicks do nothing on an admin window (Windows) | Target runs elevated; the agent must run elevated too. |
| `STALE_REF` (agent-desktop) | UI changed since the snapshot. Take a new snapshot and use the new ref. |
| App has no tree (game, canvas, remote desktop) | Fall back to coordinate clicks for that app only. |
