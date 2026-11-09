#!/usr/bin/env node

/**
 * cua_driver_acceleration CLI
 * Fast, deterministic desktop automation skill installer for AI agents.
 * 
 * Works with Antigravity, Claude Code, Cursor, Codex, and shell-capable agents.
 * Usage:
 *   npx github:pratikforge/cua_driver_acceleration
 *   npx cua_driver_acceleration [options]
 */

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const VERSION = '1.0.0';

// ANSI styling helpers (safe fallback for non-TTY)
const useColor = process.stdout.isTTY && !process.env.NO_COLOR;
const color = {
  cyan: (s) => (useColor ? `\x1b[36m${s}\x1b[0m` : s),
  green: (s) => (useColor ? `\x1b[32m${s}\x1b[0m` : s),
  yellow: (s) => (useColor ? `\x1b[33m${s}\x1b[0m` : s),
  bold: (s) => (useColor ? `\x1b[1m${s}\x1b[0m` : s),
  dim: (s) => (useColor ? `\x1b[2m${s}\x1b[0m` : s),
  red: (s) => (useColor ? `\x1b[31m${s}\x1b[0m` : s),
};

function printBanner() {
  console.log(`
${color.bold(color.cyan('⚡ CUA Driver Acceleration'))} ${color.dim(`v${VERSION}`)}
${color.dim('Deterministic, sub-200ms desktop automation skill for AI agents.')}
`);
}

function printHelp() {
  printBanner();
  console.log(`Usage:
  npx cua_driver_acceleration [options]
  npx github:pratikforge/cua_driver_acceleration [options]

Options:
  --check                 Run read-only system audit for cua-driver and agent-desktop
  --target <agent>        Install specifically for: antigravity, claude, cursor, or all
  --path <directory>      Install into a custom directory
  -v, --version           Print version information
  -h, --help              Show this help message

Examples:
  npx cua_driver_acceleration               # Auto-detects agent environments and installs
  npx cua_driver_acceleration --check       # Checks installed drivers without writing files
  npx cua_driver_acceleration --target all  # Installs into all detected agent platforms
`);
}

function runCheck() {
  printBanner();
  console.log(color.bold('Running environment audit...\n'));
  const isWin = os.platform() === 'win32';
  try {
    if (isWin) {
      const script = path.join(ROOT_DIR, 'scripts', 'check-setup.ps1');
      execSync(`powershell -ExecutionPolicy Bypass -File "${script}"`, { stdio: 'inherit' });
    } else {
      const script = path.join(ROOT_DIR, 'scripts', 'check-setup.sh');
      execSync(`bash "${script}"`, { stdio: 'inherit' });
    }
  } catch (err) {
    console.error(color.red('Error running check script:'), err.message);
    process.exit(1);
  }
}

function copyDirectory(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirectory(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function installSkillInto(targetDir, agentName) {
  const dest = path.join(targetDir, 'cua_driver_acceleration');
  console.log(`Installing skill into ${color.bold(agentName)}:`);
  console.log(color.dim(`  Destination: ${dest}`));

  fs.mkdirSync(dest, { recursive: true });

  // Copy SKILL.md
  const skillFile = path.join(ROOT_DIR, 'SKILL.md');
  if (fs.existsSync(skillFile)) {
    fs.copyFileSync(skillFile, path.join(dest, 'SKILL.md'));
  }

  // Copy references directory
  const refDir = path.join(ROOT_DIR, 'references');
  if (fs.existsSync(refDir)) {
    copyDirectory(refDir, path.join(dest, 'references'));
  }

  // Copy scripts directory
  const scriptsDir = path.join(ROOT_DIR, 'scripts');
  if (fs.existsSync(scriptsDir)) {
    copyDirectory(scriptsDir, path.join(dest, 'scripts'));
  }

  console.log(`  ${color.green('✔')} Successfully installed into ${agentName}\n`);
}

function detectTargets() {
  const home = os.homedir();
  const cwd = process.cwd();
  const targets = [];

  // 1. Antigravity Global Skills
  const antigravityPath = path.join(home, '.gemini', 'config', 'skills');
  if (fs.existsSync(path.join(home, '.gemini', 'config')) || fs.existsSync(antigravityPath)) {
    targets.push({ name: 'Antigravity (Global)', path: antigravityPath });
  }

  // 2. Claude Code Global Skills
  const claudeGlobalPath = path.join(home, '.claude', 'skills');
  if (fs.existsSync(path.join(home, '.claude')) || fs.existsSync(claudeGlobalPath)) {
    targets.push({ name: 'Claude Code (Global)', path: claudeGlobalPath });
  }

  // 3. Claude Code Project Skills (if current workspace has .claude)
  const claudeLocalPath = path.join(cwd, '.claude', 'skills');
  if (fs.existsSync(path.join(cwd, '.claude'))) {
    targets.push({ name: 'Claude Code (Local Project)', path: claudeLocalPath });
  }

  return targets;
}

function main() {
  const args = process.argv.slice(2);

  if (args.includes('-h') || args.includes('--help')) {
    printHelp();
    return;
  }

  if (args.includes('-v') || args.includes('--version')) {
    console.log(VERSION);
    return;
  }

  if (args.includes('--check')) {
    runCheck();
    return;
  }

  printBanner();

  let customPath = null;
  const pathIdx = args.indexOf('--path');
  if (pathIdx !== -1 && args[pathIdx + 1]) {
    customPath = path.resolve(args[pathIdx + 1]);
  }

  let specificTarget = null;
  const targetIdx = args.indexOf('--target');
  if (targetIdx !== -1 && args[targetIdx + 1]) {
    specificTarget = args[targetIdx + 1].toLowerCase();
  }

  // Handle custom path
  if (customPath) {
    installSkillInto(customPath, `Custom Path (${customPath})`);
    console.log(color.green('✔ Done! Skill installed successfully.'));
    return;
  }

  // Detect available agents
  const detected = detectTargets();

  if (specificTarget) {
    const home = os.homedir();
    if (specificTarget === 'antigravity') {
      installSkillInto(path.join(home, '.gemini', 'config', 'skills'), 'Antigravity');
    } else if (specificTarget === 'claude') {
      installSkillInto(path.join(home, '.claude', 'skills'), 'Claude Code');
    } else if (specificTarget === 'cursor') {
      installSkillInto(path.join(process.cwd(), '.cursor', 'skills'), 'Cursor');
    } else if (specificTarget === 'all') {
      if (detected.length === 0) {
        // Fallback default
        installSkillInto(path.join(home, '.gemini', 'config', 'skills'), 'Antigravity');
        installSkillInto(path.join(home, '.claude', 'skills'), 'Claude Code');
      } else {
        for (const t of detected) {
          installSkillInto(t.path, t.name);
        }
      }
    } else {
      console.log(color.red(`Unknown target: ${specificTarget}`));
      console.log('Supported targets: antigravity, claude, cursor, all');
      process.exit(1);
    }
    console.log(color.green('✔ Installation complete.'));
    return;
  }

  // Automatic install into all detected environments
  if (detected.length > 0) {
    console.log(color.bold(`Detected ${detected.length} agent environment(s):\n`));
    for (const t of detected) {
      installSkillInto(t.path, t.name);
    }
  } else {
    // No existing config directory found, install in local project .skills directory
    const fallbackPath = path.join(process.cwd(), '.skills');
    console.log(color.yellow('No existing ~/.gemini/config/skills or ~/.claude/skills found.'));
    console.log(`Installing into local project directory: ${fallbackPath}\n`);
    installSkillInto(fallbackPath, 'Local Project Skills');
  }

  console.log(color.bold(color.green('✔ Skill installed and ready to use!\n')));
  console.log(color.dim('Next steps:'));
  console.log(color.dim('  1. Ask your agent any computer-use or desktop automation task.'));
  console.log(color.dim('  2. The agent will read cua_driver_acceleration/SKILL.md and run direct, sub-200ms actions.'));
  console.log(color.dim('  3. Run `npx cua_driver_acceleration --check` anytime to audit your driver status.\n'));
}

main();
