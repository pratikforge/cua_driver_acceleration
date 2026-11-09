#!/usr/bin/env bash
# fast-computer-use: read-only environment check (macOS / Linux).
# Reports which computer-use backend is available. Never installs anything.

set -u

have() { command -v "$1" >/dev/null 2>&1; }

OS="$(uname -s)"
echo "fast-computer-use environment check"
echo "OS: $OS $(uname -r)"
echo

if have cua-driver; then
  echo "[found]   cua-driver     $(command -v cua-driver)  $(cua-driver --version 2>/dev/null | head -n1)"
else
  echo "[missing] cua-driver"
fi

if have agent-desktop; then
  echo "[found]   agent-desktop  $(command -v agent-desktop)"
  agent-desktop status 2>/dev/null | head -n5 | sed 's/^/          /'
else
  echo "[missing] agent-desktop"
fi

if have node; then
  echo "[found]   node           $(node --version 2>/dev/null)"
else
  echo "[missing] node (needed only for the npm install of agent-desktop)"
fi

if [ "$OS" = "Linux" ] && have gsettings; then
  A11Y="$(gsettings get org.gnome.desktop.interface toolkit-accessibility 2>/dev/null || echo unknown)"
  echo "[info]    GNOME toolkit-accessibility: $A11Y"
fi

echo

if have cua-driver; then
  echo "BACKEND=cua-driver"
elif have agent-desktop; then
  echo "BACKEND=agent-desktop"
else
  echo "BACKEND=none"
  echo
  echo "No backend installed. Ask the user to approve ONE of these:"
  if have npm; then
    echo "  Recommended: npm install -g agent-desktop"
  elif have brew; then
    echo "  Recommended: brew install agent-desktop"
  fi
  echo "  Alternative: /bin/bash -c \"\$(curl -fsSL https://cua.ai/driver/install.sh)\""
  echo
  if [ "$OS" = "Darwin" ]; then
    echo "macOS: after install, grant Accessibility in System Settings > Privacy & Security."
  fi
  echo "Open a new terminal so PATH refreshes, then re-run this check."
fi
