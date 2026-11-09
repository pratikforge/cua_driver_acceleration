# Backend Cheat-Sheet

Common actions side by side. Flags can change between releases, so run `--help` once per session to confirm.

## Observe

| Action | cua-driver | agent-desktop |
|---|---|---|
| Health check | `cua-driver --version` | `agent-desktop status` |
| List apps / windows | `cua-driver call list_windows` | `agent-desktop --help` (see app listing command for your version) |
| Read accessibility tree | `'{"pid":P,"window_id":W}' \| cua-driver call get_window_state` | `agent-desktop snapshot --app "App" -i` |

`-i` on agent-desktop limits output to interactive elements, which keeps the JSON small.

## Act

| Action | cua-driver | agent-desktop |
|---|---|---|
| Click element | `'{"pid":P,"element_token":"T"}' \| cua-driver call click` | `agent-desktop click @<snap>:<el>` |
| Type into element | `'{"pid":P,"element_token":"T","text":"hello"}' \| cua-driver call type_text` | `agent-desktop type @<snap>:<el> "hello"` |
| Launch app without stealing focus | `'{"name":"App"}' \| cua-driver call launch_app` | launch via OS (`open -a`, `start`, `xdg-open`) then snapshot |
| Hotkey | `'{"pid":P,"keys":["ctrl","s"]}' \| cua-driver call hotkey` | see `agent-desktop --help` |

## Reference formats

- **cua-driver:** `element_token` from the latest `get_window_state` (preferred; carries index + snapshot id). Raw `element_index` also works but must be sent with its matching `snapshot_id`. Tokens go stale once a newer snapshot exists.
- **agent-desktop:** `@<snapshot_id>:<element_id>`, e.g. `@s8f3k2p9:e8`. Bare refs like `@e8` are rejected on purpose so you can't act on an old snapshot.

## Output

Both return JSON. Read `ok` / error fields from the JSON instead of taking a screenshot to see what happened.

## Windows quoting tip (cua-driver)

Pipe JSON on stdin. PowerShell 5.1 mangles arguments that contain both quotes and spaces:

```powershell
'{"pid":1234,"text":"hello world"}' | cua-driver call type_text
```
