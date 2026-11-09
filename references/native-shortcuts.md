# Native Shortcuts

Skip the GUI when the OS already exposes a direct route.

## Windows

| Target | Command |
|---|---|
| Any Settings page | `start ms-settings:<page>` — e.g. `display`, `bluetooth`, `appsfeatures`, `windowsupdate`, `network-wifi`, `sound`, `privacy-microphone` |
| Microsoft Store search | `start "ms-windows-store://search/?query=<term>"` |
| Store product page | `start "ms-windows-store://pdp/?productid=<id>"` |
| Open URL in default browser | `start https://example.com` |
| Open folder in Explorer | `explorer.exe C:\path\to\folder` |
| Control Panel applet | `control printers`, `control mmsys.cpl` (sound), `ncpa.cpl` (network adapters) |
| Installed apps (scriptable) | `winget list`, `winget install <id>` |
| Processes | `Get-Process`, `Stop-Process -Name <name>` |

## macOS *(OS reference; empirical benchmarks conducted on Windows 11)*

| Target | Command |
|---|---|
| System Settings pane | `open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"` |
| Open app | `open -a "App Name"` |
| Open URL | `open https://example.com` |
| Reveal file in Finder | `open -R /path/to/file` |
| App Store search | `open "macappstore://search.itunes.apple.com/WebObjects/MZSearch.woa/wa/search?q=<term>"` |
| Defaults / prefs | `defaults read <domain>`, `defaults write <domain> <key> <value>` |
| Scriptable apps | `osascript -e 'tell application "Music" to play'` |

## Linux

| Target | Command |
|---|---|
| Open URL / file with default app | `xdg-open <url-or-path>` |
| GNOME settings panel | `gnome-control-center <panel>` — e.g. `display`, `network`, `sound` |
| GNOME setting value | `gsettings set <schema> <key> <value>` |
| Packages | `apt`, `dnf`, `pacman`, `flatpak` |

## Cross-platform developer tools

| Target | Command |
|---|---|
| Open file in VS Code | `code <file>` / `code -g <file>:<line>` |
| Git hosting | `gh pr create`, `gh issue list` |
| Browser automation | Prefer a browser-automation tool (Playwright, agent-browser, DevTools MCP) over clicking the browser's address bar |
