---
name: fast-computer-use
description: Low-latency desktop automation for AI agents. Use whenever the task involves operating a native GUI app, clicking, typing, opening apps or settings, or any computer-use / CUA work on macOS, Windows, or Linux. Enforces accessibility-tree targeting over screenshots and pixel guessing, bans throwaway wrapper scripts, prefers deep links and CLIs over GUI navigation, and self-bootstraps a backend (cua-driver or Vercel agent-desktop) on first use.
version: 1.0.0
license: MIT
metadata:
  requires:
    anyBins:
      - cua-driver
      - agent-desktop
  homepage: https://github.com/pratikforge/fast-computer-use
---

# Fast Computer Use

Most computer-use latency comes from agent habits, not from the driver. The four usual culprits:

1. Writing a 30-line Python wrapper to send one click.
2. Taking a screenshot and guessing `(x, y)` pixel coordinates.
3. Splitting a 3-step task into 20 click â†’ screenshot â†’ think turns.
4. Clicking through menus when a deep link or CLI flag already does the job.

This skill removes all four. Follow the sections in order.

---

## Step 0 â€” Bootstrap (first use only)

Run the read-only environment check once per machine:

- Windows: `powershell -ExecutionPolicy Bypass -File <skill_dir>/scripts/check-setup.ps1`
- macOS / Linux: `bash <skill_dir>/scripts/check-setup.sh`

It reports which backend is installed and prints the exact install command for anything missing. It never installs anything by itself.

**Pick a backend:**

| Situation | Backend |
|---|---|
| `cua-driver` already on PATH | Use **cua-driver** |
| Only `agent-desktop` on PATH | Use **agent-desktop** |
| Neither installed, Node.js available | Recommend **agent-desktop** (`npm i -g agent-desktop`) |
| Neither installed, no Node.js | Recommend **cua-driver** (one-line installer) |

**Installing is a user decision.** Show the user the install command from [references/setup.md](references/setup.md) and wait for approval. Remote installers (`curl | bash`, `irm | iex`) are never run without explicit consent. On macOS, the user must also grant Accessibility (and Screen Recording for cua-driver) in System Settings; the agent cannot do that itself.

After install, verify:

- cua-driver: `cua-driver --version`
- agent-desktop: `agent-desktop status`

Then check the live command list once (`cua-driver --help` / `agent-desktop --help`), because flags change between versions. The cheat-sheet in [references/backends.md](references/backends.md) covers the common commands.

---

## Rule 1 â€” Shortest path first

Before touching the mouse, check whether a non-GUI path exists. Use the first one that works:

1. **CLI or API** â€” `git`, `code <file>`, `gh`, `npm`, app-specific CLIs.
2. **Deep link / URI scheme** â€” `ms-settings:display`, `x-apple.systempreferences:`, `ms-windows-store://search/?query=...`, plain `https://` URLs.
3. **Config file edit** â€” e.g. `settings.json` instead of the settings UI.
4. **Accessibility-tree action** via the backend (Rule 3).
5. **Pixel coordinates** â€” last resort, only for canvases with no accessibility tree (games, remote desktops, some Electron/WebGL surfaces).

Deep links per OS: [references/native-shortcuts.md](references/native-shortcuts.md).

**Launching visible apps:** on Windows with cua-driver, use `launch_app` rather than `Start-Process` or `&`. Those raise the window and steal the user's focus; `launch_app` does not.

---

## Rule 2 â€” No wrapper scripts for actions

Do **not** write Python, Node, or shell wrapper files (and no `python -c "import subprocess..."`) to perform clicks, keystrokes, window lookups, or coordinate searches.

Call the backend directly, one line per action:

```powershell
# cua-driver (Windows: pipe JSON on stdin to avoid PowerShell quoting bugs)
'{"pid":1234,"element_token":"<token-from-get_window_state>"}' | cua-driver call click
```

```bash
# agent-desktop
agent-desktop click @s8f3k2p9:e8
```

Exception: a script is fine when the deliverable itself is a script (the user asked for an automation file), or for non-GUI data processing.

---

## Rule 3 â€” Target elements, not pixels

1. **Snapshot once.** Read the accessibility tree of the target window.
   - cua-driver: `'{"pid":<pid>,"window_id":<wid>}' | cua-driver call get_window_state`
   - agent-desktop: `agent-desktop snapshot --app "<App Name>" -i`
2. **Act by reference.** Use the `element_token` from the latest snapshot (cua-driver; it bundles the element index and snapshot id) or the snapshot-qualified ref like `@s8f3k2p9:e8` (agent-desktop).
3. **Re-snapshot only when the UI changed** (new window, navigation, dialog). Refs from an old snapshot are stale; agent-desktop returns `STALE_REF` instead of misclicking.

Never compute bounding-box centres, scan pixel colours, or estimate positions from screenshots when the tree has the element.

---

## Rule 4 â€” One turn per task

- A routine task (open app â†’ find control â†’ act) should finish in **one turn**, two at most if a final check is needed.
- Chain dependent commands in a single shell call where the shell allows it.
- No screenshot between every step. Screenshot only when:
  - the user asked for one,
  - a command returned an error you cannot read from the JSON, or
  - presenting the final result.
- Use a long enough synchronous wait on GUI commands (about 10 s) so the result arrives in the same turn instead of polling.
- No blind `sleep N`. If you must wait, wait on a condition (window exists, element present).

---

## Rule 5 â€” Trust the event dispatch

On Windows, synthetic input through the global input queue often returns `"effect": "unverifiable"`. That means the event was dispatched. Do not loop on screenshots just because of that flag; verify once from a fresh snapshot if the outcome matters.

---

## Rule 6 â€” Screenshots for the user

When presenting a capture, use a unique filename (`snip_<timestamp>_<id>.png`) so viewers never show a cached older image. Don't overwrite earlier captures.

---

## Quick self-check before each action

- Is there a CLI, deep link, or config path? â†’ use it.
- Am I about to write a wrapper file? â†’ stop, call the backend directly.
- Am I about to guess coordinates? â†’ snapshot and use a ref.
- Am I about to take a screenshot "just to see"? â†’ read the JSON result instead.
