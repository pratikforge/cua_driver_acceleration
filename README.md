# fast-computer-use

An agent skill that makes desktop automation (computer use / CUA) much faster by changing **how the agent works**, not which driver it uses.

## The problem

Give an agent a computer-use tool and it usually:

- writes a throwaway Python script to send a single click,
- takes a screenshot and guesses pixel coordinates,
- spends 15â€“20 turns on click â†’ screenshot â†’ think loops,
- clicks through Settings menus when `ms-settings:display` would open the page directly.

Every one of those adds seconds. Together they turn a 2-second task into a 2-minute one.

## What the skill does

| Habit | Replaced with |
|---|---|
| Wrapper scripts per action | One-line direct backend calls |
| Screenshot + pixel guessing | Accessibility-tree snapshot + element refs (50â€“200 ms) |
| Multi-turn micro-loops | One turn per routine task |
| GUI menu navigation | Deep links, URI schemes, CLIs, config files |
| Screenshot after every step | Read the JSON result; screenshot only at the end or on error |

It also bootstraps itself: on first use the agent runs a read-only check, finds which backend is installed, and if none is, shows you the install command and waits for your approval.

## Supported backends

Both use native OS accessibility APIs (Windows UI Automation, macOS AX, Linux AT-SPI):

- **[Vercel agent-desktop](https://github.com/vercel-labs/agent-desktop)**: open-source Rust CLI, works with any shell-capable agent, headless, `npm i -g agent-desktop`. Recommended default.
- **[cua-driver](https://cua.ai/docs/cua-driver)**: native driver with CLI + MCP server, strong Windows support (focus-safe app launch, menu paths, recording).

## Install the skill

Clone into your agent's skills directory:

```bash
git clone https://github.com/pratikforge/fast-computer-use
```

| Agent | Location |
|---|---|
| Antigravity | `~/.gemini/config/skills/fast-computer-use/` |
| Claude Code | `~/.claude/skills/fast-computer-use/` (or `.claude/skills/` in a project) |
| Codex / others with skill support | the agent's skills folder |
| Agents without skill support | paste `SKILL.md` into your rules / system prompt file (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`) |

Then just ask for a desktop task. The agent loads the skill, runs the setup check, and goes from there.

## Repository layout

```
fast-computer-use/
â”œâ”€â”€ SKILL.md                     # Rules the agent follows
â”œâ”€â”€ references/
â”‚   â”œâ”€â”€ setup.md                 # Backend install + permissions + troubleshooting
â”‚   â”œâ”€â”€ backends.md              # cua-driver vs agent-desktop command cheat-sheet
â”‚   â””â”€â”€ native-shortcuts.md      # Deep links / URIs / CLIs per OS
â””â”€â”€ scripts/
    â”œâ”€â”€ check-setup.ps1          # Read-only environment check (Windows)
    â””â”€â”€ check-setup.sh           # Read-only environment check (macOS / Linux)
```

## Safety

- The check scripts only read the environment. They never install or change anything.
- The skill tells the agent to get your approval before running any installer, especially remote ones (`curl | bash`, `irm | iex`).
- OS permission prompts (macOS Accessibility, Screen Recording) are left to you.

## License

MIT
