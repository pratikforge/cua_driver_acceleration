#!/usr/bin/env node

/**
 * cua_driver_acceleration CLI
 * Fast, deterministic desktop automation skill installer for AI agents.
 * 
 * Works with Antigravity, Claude Code, OpenAI Codex, OpenCode, Cursor, Windsurf, Roo Code, and more.
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

const VERSION = '1.2.0';

// ANSI styling helpers (safe fallback for non-TTY)
const useColor = process.stdout.isTTY && !process.env.NO_COLOR;
const color = {
  cyan: (s) => (useColor ? `\x1b[36m${s}\x1b[0m` : s),
  green: (s) => (useColor ? `\x1b[32m${s}\x1b[0m` : s),
  yellow: (s) => (useColor ? `\x1b[33m${s}\x1b[0m` : s),
  bold: (s) => (useColor ? `\x1b[1m${s}\x1b[0m` : s),
  dim: (s) => (useColor ? `\x1b[2m${s}\x1b[0m` : s),
  red: (s) => (useColor ? `\x1b[31m${s}\x1b[0m` : s),
  magenta: (s) => (useColor ? `\x1b[35m${s}\x1b[0m` : s),
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
  --target <harness>      Install specifically for:
                          antigravity, claude, codex, opencode, cursor, windsurf, roo, or all
  --path <directory>      Install into a custom directory
  -v, --version           Print version information
  -h, --help              Show this help message

Supported Agent Harnesses:
  • Antigravity           ~/.gemini/config/skills/
  • Claude Code           ~/.claude/skills/ or ./.claude/skills/
  • OpenAI Codex          ~/.codex/skills/ or ./.codex/skills/
  • OpenCode              ~/.config/opencode/skills/ or ./.opencode/skills/
  • Cursor                ./.cursor/skills/
  • Windsurf (Codeium)    ~/.codeium/windsurf/skills/ or ./.windsurf/skills/
  • Roo Code / Cline      ./.roo/skills/ or ./.cline/skills/
  • Universal Agent Std   ~/.agents/skills/

Examples:
  npx cua_driver_acceleration               # Auto-detects agent environments and installs
  npx cua_driver_acceleration --check       # Checks installed drivers without writing files
  npx cua_driver_acceleration --target codex # Installs for OpenAI Codex
  npx cua_driver_acceleration --target opencode # Installs for OpenCode
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

  // Copy runtime environment check scripts (omit report/benchmark generators from skill)
  const scriptsDir = path.join(ROOT_DIR, 'scripts');
  if (fs.existsSync(scriptsDir)) {
    const destScripts = path.join(dest, 'scripts');
    fs.mkdirSync(destScripts, { recursive: true });
    for (const file of fs.readdirSync(scriptsDir)) {
      if (file.startsWith('check-setup')) {
        fs.copyFileSync(path.join(scriptsDir, file), path.join(destScripts, file));
      }
    }
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

  // 3. Claude Code Project Skills
  const claudeLocalPath = path.join(cwd, '.claude', 'skills');
  if (fs.existsSync(path.join(cwd, '.claude'))) {
    targets.push({ name: 'Claude Code (Local Workspace)', path: claudeLocalPath });
  }

  // 4. OpenAI Codex Global Skills
  const codexHome = process.env.CODEX_HOME || path.join(home, '.codex');
  const codexGlobalPath = path.join(codexHome, 'skills');
  if (fs.existsSync(codexHome) || fs.existsSync(codexGlobalPath)) {
    targets.push({ name: 'OpenAI Codex (Global)', path: codexGlobalPath });
  }

  // 5. OpenAI Codex Local Workspace Skills
  const codexLocalPath = path.join(cwd, '.codex', 'skills');
  if (fs.existsSync(path.join(cwd, '.codex'))) {
    targets.push({ name: 'OpenAI Codex (Local Workspace)', path: codexLocalPath });
  }

  // 6. OpenCode Global Skills (~/.config/opencode/skills)
  const opencodeGlobalPath = path.join(home, '.config', 'opencode', 'skills');
  if (fs.existsSync(path.join(home, '.config', 'opencode')) || fs.existsSync(opencodeGlobalPath)) {
    targets.push({ name: 'OpenCode (Global)', path: opencodeGlobalPath });
  }

  // 7. OpenCode Local Workspace Skills (.opencode/skills)
  const opencodeLocalPath = path.join(cwd, '.opencode', 'skills');
  if (fs.existsSync(path.join(cwd, '.opencode'))) {
    targets.push({ name: 'OpenCode (Local Workspace)', path: opencodeLocalPath });
  }

  // 8. Cursor Local Skills
  const cursorLocalPath = path.join(cwd, '.cursor', 'skills');
  if (fs.existsSync(path.join(cwd, '.cursor'))) {
    targets.push({ name: 'Cursor (Local Workspace)', path: cursorLocalPath });
  }

  // 9. Windsurf (Codeium) Skills
  const windsurfGlobalPath = path.join(home, '.codeium', 'windsurf', 'skills');
  const windsurfLocalPath = path.join(cwd, '.windsurf', 'skills');
  if (fs.existsSync(path.join(home, '.codeium', 'windsurf')) || fs.existsSync(windsurfGlobalPath)) {
    targets.push({ name: 'Windsurf (Global)', path: windsurfGlobalPath });
  }
  if (fs.existsSync(path.join(cwd, '.windsurf'))) {
    targets.push({ name: 'Windsurf (Local Workspace)', path: windsurfLocalPath });
  }

  // 10. Roo Code / Cline Skills
  const rooLocalPath = path.join(cwd, '.roo', 'skills');
  if (fs.existsSync(path.join(cwd, '.roo'))) {
    targets.push({ name: 'Roo Code (Local Workspace)', path: rooLocalPath });
  }

  // 11. Universal Agent Skills (~/.agents/skills)
  const universalPath = path.join(home, '.agents', 'skills');
  if (fs.existsSync(path.join(home, '.agents')) || fs.existsSync(universalPath)) {
    targets.push({ name: 'Universal Agent Standard (~/.agents/skills)', path: universalPath });
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
  const home = os.homedir();
  const cwd = process.cwd();

  if (specificTarget) {
    if (specificTarget === 'antigravity') {
      installSkillInto(path.join(home, '.gemini', 'config', 'skills'), 'Antigravity');
    } else if (specificTarget === 'claude') {
      installSkillInto(path.join(home, '.claude', 'skills'), 'Claude Code');
    } else if (specificTarget === 'codex') {
      const codexPath = process.env.CODEX_HOME ? path.join(process.env.CODEX_HOME, 'skills') : path.join(home, '.codex', 'skills');
      installSkillInto(codexPath, 'OpenAI Codex');
    } else if (specificTarget === 'opencode') {
      installSkillInto(path.join(home, '.config', 'opencode', 'skills'), 'OpenCode');
    } else if (specificTarget === 'cursor') {
      installSkillInto(path.join(cwd, '.cursor', 'skills'), 'Cursor');
    } else if (specificTarget === 'windsurf') {
      installSkillInto(path.join(home, '.codeium', 'windsurf', 'skills'), 'Windsurf');
    } else if (specificTarget === 'roo' || specificTarget === 'cline') {
      installSkillInto(path.join(cwd, '.roo', 'skills'), 'Roo Code');
    } else if (specificTarget === 'universal') {
      installSkillInto(path.join(home, '.agents', 'skills'), 'Universal Agent Standard');
    } else if (specificTarget === 'all') {
      if (detected.length === 0) {
        // Fallback: install to standard locations
        installSkillInto(path.join(home, '.gemini', 'config', 'skills'), 'Antigravity');
        installSkillInto(path.join(home, '.claude', 'skills'), 'Claude Code');
        installSkillInto(path.join(home, '.config', 'opencode', 'skills'), 'OpenCode');
        installSkillInto(path.join(home, '.codex', 'skills'), 'OpenAI Codex');
        installSkillInto(path.join(home, '.agents', 'skills'), 'Universal Agent Standard');
      } else {
        for (const t of detected) {
          installSkillInto(t.path, t.name);
        }
      }
    } else {
      console.log(color.red(`Unknown target: ${specificTarget}`));
      console.log('Supported targets: antigravity, claude, codex, opencode, cursor, windsurf, roo, universal, all');
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
    // No specific agent directory found; install to universal ~/.agents/skills and local .skills
    const universalPath = path.join(home, '.agents', 'skills');
    console.log(color.yellow('No pre-configured agent directory detected.'));
    console.log(`Installing into Universal Agent Standard directory: ${universalPath}\n`);
    installSkillInto(universalPath, 'Universal Agent Standard (~/.agents/skills)');
  }

  console.log(color.bold(color.green('✔ Skill installed and ready to use!\n')));
  console.log(color.dim('Next steps:'));
  console.log(color.dim('  1. Ask your agent any computer-use or desktop automation task.'));
  console.log(color.dim('  2. The agent will read cua_driver_acceleration/SKILL.md and run direct, sub-200ms actions.'));
  console.log(color.dim('  3. Run `npx cua_driver_acceleration --check` anytime to audit your driver status.\n'));
}

main();
