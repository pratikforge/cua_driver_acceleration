# fast-computer-use: read-only environment check (Windows).
# Reports which computer-use backend is available. Never installs anything.

$ErrorActionPreference = 'SilentlyContinue'

function Test-Bin($name) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source } else { return $null }
}

Write-Host "fast-computer-use environment check"
Write-Host "OS: Windows $([System.Environment]::OSVersion.Version)"
Write-Host ""

$cua  = Test-Bin 'cua-driver'
$ad   = Test-Bin 'agent-desktop'
$node = Test-Bin 'node'
$npm  = Test-Bin 'npm'

if ($cua) {
    $v = (& cua-driver --version 2>$null | Select-Object -First 1)
    Write-Host "[found]   cua-driver     $cua  $v"
} else {
    Write-Host "[missing] cua-driver"
}

if ($ad) {
    Write-Host "[found]   agent-desktop  $ad"
    & agent-desktop status 2>$null | Select-Object -First 5 | ForEach-Object { Write-Host "          $_" }
} else {
    Write-Host "[missing] agent-desktop"
}

if ($node) {
    $nv = (& node --version 2>$null)
    Write-Host "[found]   node           $nv"
} else {
    Write-Host "[missing] node (needed only for the npm install of agent-desktop)"
}

Write-Host ""

if ($cua) {
    Write-Host "BACKEND=cua-driver"
} elseif ($ad) {
    Write-Host "BACKEND=agent-desktop"
} else {
    Write-Host "BACKEND=none"
    Write-Host ""
    Write-Host "No backend installed. Ask the user to approve ONE of these:"
    if ($npm) {
        Write-Host "  Recommended: npm install -g agent-desktop"
        Write-Host "  Alternative: irm https://cua.ai/driver/install.ps1 | iex"
    } else {
        Write-Host "  Recommended: irm https://cua.ai/driver/install.ps1 | iex"
        Write-Host "  Alternative: install Node.js 18+, then: npm install -g agent-desktop"
    }
    Write-Host ""
    Write-Host "After install, open a new terminal so PATH refreshes, then re-run this check."
}
