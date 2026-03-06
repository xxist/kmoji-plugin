#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const readline = require("readline");
const { execSync } = require("child_process");

// ── Colors (ANSI) ──────────────────────────────────────────────
const PINK = "\x1b[38;5;205m";
const GREEN = "\x1b[32m";
const DIM = "\x1b[2m";
const BOLD = "\x1b[1m";
const RESET = "\x1b[0m";
const CLEAR = "\x1b[2J\x1b[H";
const HIDE_CURSOR = "\x1b[?25l";
const SHOW_CURSOR = "\x1b[?25h";

// ── ASCII Logo ─────────────────────────────────────────────────
const LOGO = `
${PINK}╔═══════════════════════════════════════════╗
║  ██╗  ██╗███╗   ███╗ ██████╗    ████╗██╗  ║
║  ██║ ██╔╝████╗ ████║██╔═══██╗     ██║██║  ║
║  █████╔╝ ██╔████╔██║██║   ██║     ██║██║  ║
║  ██╔═██╗ ██║╚██╔╝██║██║   ██║     ██║██║  ║
║  ██║  ██╗██║ ╚═╝ ██║╚██████╔╝███████╗██║  ║
║  ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝  ║
╚═══════════════════════════════════════════╝${RESET}`;

// ── Animation Frames ───────────────────────────────────────────
const TICKER_MOJIS = [
  "ᒋि ᗝ🝏ᗝິ ॏᘃ",
  "⎛⎝𓌹 🝦ㅈ🝦 𓌺⎠⎞",
  "/╲/\\╭⚇人⚇╮/\\╱\\",
  "૮(ᓱ◯ㅈ◯ᓴ)ა",
  "⦤╭ˆ⊛◡⊛ˆ╮⦥",
];

const LOADING_STEPS = [
  "INITIALIZING GENERATOR...",
  "RENDERING TRAITS...",
  "INSERTING EYES...",
  "ADDING MOUTH...",
  "EXECUTING NECROMANCER SCRIPT...",
  "SUMMONING KOAMOJI...",
];

// ── Paths ──────────────────────────────────────────────────────
const KMOJI_ROOT = path.resolve(__dirname, "..");
const PLUGIN_DIR = path.join(KMOJI_ROOT, "plugins", "kmoji");
const SKILLS_DIR = path.join(PLUGIN_DIR, "skills");
const TEMPLATES_DIR = path.join(KMOJI_ROOT, "templates");
const GENERATOR_SCRIPT = path.join(
  SKILLS_DIR,
  "kmoji",
  "scripts",
  "generate.py"
);

function getHomePath() {
  return process.env.HOME || process.env.USERPROFILE || process.env.HOMEPATH;
}

function getClaudeMdPath(scope) {
  if (scope === "global") {
    return path.join(getHomePath(), ".claude", "CLAUDE.md");
  }
  return path.join(process.cwd(), ".claude", "CLAUDE.md");
}

function getSettingsPath(scope) {
  if (scope === "global") {
    return path.join(getHomePath(), ".claude", "settings.json");
  }
  return path.join(process.cwd(), ".claude", "settings.json");
}

function getInstalledPluginsPath() {
  return path.join(getHomePath(), ".claude", "plugins", "installed_plugins.json");
}

// ── Terminal Helpers ───────────────────────────────────────────
function centerText(text, width) {
  const lines = text.split("\n");
  const termWidth = width || process.stdout.columns || 80;
  return lines
    .map((line) => {
      const stripped = line.replace(/\x1b\[[0-9;]*m/g, "");
      const pad = Math.max(0, Math.floor((termWidth - stripped.length) / 2));
      return " ".repeat(pad) + line;
    })
    .join("\n");
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

// ── Splash Screen with Animation ──────────────────────────────
function buildTickerBar() {
  const inner = TICKER_MOJIS.join(`  ${DIM}│${RESET}${PINK}  `);
  const content = `${PINK}  ${inner}  ${RESET}`;
  const stripped = content.replace(/\x1b\[[0-9;]*m/g, "");
  const width = stripped.length;
  const topBorder = `${PINK}${"═".repeat(width)}${RESET}`;
  const bottomBorder = `${PINK}${"═".repeat(width)}${RESET}`;
  return { topBorder, content, bottomBorder };
}

async function showSplash() {
  process.stdout.write(HIDE_CURSOR);
  process.stdout.write(CLEAR);

  const ticker = buildTickerBar();
  console.log(ticker.topBorder);
  console.log(ticker.content);
  console.log(ticker.bottomBorder);
  console.log();
  console.log(LOGO);
  console.log();
  console.log(`${PINK}${BOLD}KAOMOJI GENERATOR v1.0${RESET}`);
  console.log(`${DIM}Vibe coding plugin for Claude Code${RESET}`);
  console.log();
}

// ── Loading Animation ─────────────────────────────────────────
async function showLoading(message) {
  const frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];
  let i = 0;
  const interval = setInterval(() => {
    process.stdout.write(
      `\r${PINK}${frames[i % frames.length]}${RESET} ${message}`
    );
    i++;
  }, 80);
  return () => {
    clearInterval(interval);
    process.stdout.write(`\r${PINK}✓${RESET} ${message}\n`);
  };
}

async function showInstallAnimation() {
  for (const step of LOADING_STEPS) {
    const stop = await showLoading(step);
    await sleep(600);
    stop();
  }
}

// ── Interactive Menu ──────────────────────────────────────────
function createRL() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
}

async function ask(rl, question, options) {
  return new Promise((resolve) => {
    console.log();
    console.log(`${PINK}${BOLD}${question}${RESET}`);
    if (options) {
      options.forEach((opt, i) => {
        console.log(`  ${PINK}${i + 1}${RESET}) ${opt.label}`);
      });
    }
    rl.question(`\n${PINK}>${RESET} `, (answer) => {
      resolve(answer.trim());
    });
  });
}

// ── Plugin Registration ───────────────────────────────────────
function registerPlugin() {
  const pluginsPath = getInstalledPluginsPath();
  const pluginsDir = path.dirname(pluginsPath);

  if (!fs.existsSync(pluginsDir)) {
    fs.mkdirSync(pluginsDir, { recursive: true });
  }

  let data = { version: 2, plugins: {} };
  if (fs.existsSync(pluginsPath)) {
    try {
      data = JSON.parse(fs.readFileSync(pluginsPath, "utf-8"));
    } catch {
      // corrupted file, start fresh
    }
  }
  if (!data.plugins) data.plugins = {};

  data.plugins["kmoji@kmoji"] = [
    {
      scope: "user",
      installPath: KMOJI_ROOT,
      version: "1.0.0",
      installedAt: new Date().toISOString(),
      lastUpdated: new Date().toISOString(),
    },
  ];

  fs.writeFileSync(pluginsPath, JSON.stringify(data, null, 2), "utf-8");
  return true;
}

function unregisterPlugin() {
  const pluginsPath = getInstalledPluginsPath();
  if (!fs.existsSync(pluginsPath)) return false;

  try {
    const data = JSON.parse(fs.readFileSync(pluginsPath, "utf-8"));
    if (!data.plugins || !data.plugins["kmoji@kmoji"]) return false;

    delete data.plugins["kmoji@kmoji"];
    fs.writeFileSync(pluginsPath, JSON.stringify(data, null, 2), "utf-8");
    return true;
  } catch {
    return false;
  }
}

function enablePlugin() {
  const settingsPath = path.join(getHomePath(), ".claude", "settings.json");
  let settings = {};
  if (fs.existsSync(settingsPath)) {
    try {
      settings = JSON.parse(fs.readFileSync(settingsPath, "utf-8"));
    } catch {
      // start fresh
    }
  }

  if (!settings.enabledPlugins) settings.enabledPlugins = {};
  settings.enabledPlugins["kmoji@kmoji"] = true;

  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2), "utf-8");
}

function disablePlugin() {
  const settingsPath = path.join(getHomePath(), ".claude", "settings.json");
  if (!fs.existsSync(settingsPath)) return false;

  try {
    const settings = JSON.parse(fs.readFileSync(settingsPath, "utf-8"));
    if (!settings.enabledPlugins || !settings.enabledPlugins["kmoji@kmoji"]) return false;

    delete settings.enabledPlugins["kmoji@kmoji"];
    fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2), "utf-8");
    return true;
  } catch {
    return false;
  }
}

// ── CLAUDE.md Install Logic ───────────────────────────────────
function getVibeTemplate() {
  const raw = fs.readFileSync(
    path.join(TEMPLATES_DIR, "vibe-kmoji.md"),
    "utf-8"
  );
  return raw.replace(/KMOJI_GENERATOR_PATH/g, GENERATOR_SCRIPT.replace(/\\/g, "/"));
}

function getPRTemplate() {
  const raw = fs.readFileSync(
    path.join(TEMPLATES_DIR, "pr-signature.md"),
    "utf-8"
  );
  return raw.replace(/KMOJI_GENERATOR_PATH/g, GENERATOR_SCRIPT.replace(/\\/g, "/"));
}

const KMOJI_START_MARKER = "<!-- KMOJI:START -->";
const KMOJI_END_MARKER = "<!-- KMOJI:END -->";

function injectIntoCLAUDEmd(claudeMdPath, content) {
  const dir = path.dirname(claudeMdPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  let existing = "";
  if (fs.existsSync(claudeMdPath)) {
    existing = fs.readFileSync(claudeMdPath, "utf-8");
  }

  // Remove any existing KMOJI block
  const startIdx = existing.indexOf(KMOJI_START_MARKER);
  const endIdx = existing.indexOf(KMOJI_END_MARKER);
  if (startIdx !== -1 && endIdx !== -1) {
    existing =
      existing.substring(0, startIdx) +
      existing.substring(endIdx + KMOJI_END_MARKER.length);
    existing = existing.replace(/\n{3,}/g, "\n\n").trim();
  }

  const block = `\n\n${KMOJI_START_MARKER}\n${content}\n${KMOJI_END_MARKER}\n`;
  fs.writeFileSync(claudeMdPath, existing + block, "utf-8");
}

function removeFromCLAUDEmd(claudeMdPath) {
  if (!fs.existsSync(claudeMdPath)) return false;

  let content = fs.readFileSync(claudeMdPath, "utf-8");
  const startIdx = content.indexOf(KMOJI_START_MARKER);
  const endIdx = content.indexOf(KMOJI_END_MARKER);

  if (startIdx === -1 || endIdx === -1) return false;

  content =
    content.substring(0, startIdx) +
    content.substring(endIdx + KMOJI_END_MARKER.length);
  content = content.replace(/\n{3,}/g, "\n\n").trim();

  fs.writeFileSync(claudeMdPath, content + "\n", "utf-8");
  return true;
}

function installHook(settingsPath) {
  const dir = path.dirname(settingsPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  let settings = {};
  if (fs.existsSync(settingsPath)) {
    settings = JSON.parse(fs.readFileSync(settingsPath, "utf-8"));
  }

  if (!settings.hooks) settings.hooks = {};

  settings.hooks["kmoji-vibe"] = {
    description: "KMOJI: Generate a contextual kaomoji on tool failure",
    event: "on_tool_error",
    command: `python "${GENERATOR_SCRIPT.replace(/\\/g, "/")}" sad 1`,
  };

  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2), "utf-8");
}

function removeHook(settingsPath) {
  if (!fs.existsSync(settingsPath)) return false;

  const settings = JSON.parse(fs.readFileSync(settingsPath, "utf-8"));
  if (!settings.hooks || !settings.hooks["kmoji-vibe"]) return false;

  delete settings.hooks["kmoji-vibe"];
  if (Object.keys(settings.hooks).length === 0) delete settings.hooks;

  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2), "utf-8");
  return true;
}

// ── Commands ──────────────────────────────────────────────────
async function runInstall() {
  await showSplash();

  const rl = createRL();

  // Install method
  const method = await ask(rl, "How do you want to install KMOJI?", [
    { label: `Plugin ${DIM}-- adds /kmoji slash command + vibe-kmoji background skill${RESET}` },
    { label: `CLAUDE.md ${DIM}-- injects kaomoji instructions into CLAUDE.md${RESET}` },
    { label: `Both ${DIM}-- plugin + CLAUDE.md templates${RESET}` },
  ]);
  const installPlugin = method === "1" || method === "3";
  const installClaudeMd = method === "2" || method === "3";

  let selectedScope = "global";
  let claudeMdFeatures = null;

  if (installClaudeMd) {
    // Scope selection
    const scope = await ask(rl, "Where should the CLAUDE.md config go?", [
      { label: "Global (all projects)" },
      { label: "This project only" },
    ]);
    selectedScope = scope === "1" ? "global" : "project";

    // Feature selection
    claudeMdFeatures = await ask(rl, "What CLAUDE.md features do you want?", [
      { label: "Vibe Kaomojis -- auto-reactions to success, errors, debugging" },
      { label: "PR Signatures -- kaomoji signatures on PRs and commits" },
      { label: "All of the above" },
    ]);
  }

  console.log();
  await showInstallAnimation();
  console.log();

  const results = [];

  // Plugin registration
  if (installPlugin) {
    registerPlugin();
    enablePlugin();
    results.push(`${GREEN}✓${RESET} Plugin registered ${DIM}(/kmoji slash command + vibe-kmoji)${RESET}`);
    results.push(`  ${DIM}Registered in: ${getInstalledPluginsPath()}${RESET}`);
    results.push(`  ${DIM}Plugin source: ${KMOJI_ROOT}${RESET}`);
  }

  // CLAUDE.md injection
  if (installClaudeMd) {
    const claudeMdPath = getClaudeMdPath(selectedScope);
    const settingsPath = getSettingsPath(selectedScope);
    let template = "";

    if (claudeMdFeatures === "1" || claudeMdFeatures === "3") {
      template += getVibeTemplate() + "\n\n";
      installHook(settingsPath);
      results.push(`${GREEN}✓${RESET} Vibe kaomojis added to CLAUDE.md`);
      results.push(`${GREEN}✓${RESET} Error hook installed`);
    }

    if (claudeMdFeatures === "2" || claudeMdFeatures === "3") {
      template += getPRTemplate();
      results.push(`${GREEN}✓${RESET} PR signatures added to CLAUDE.md`);
    }

    if (template) {
      injectIntoCLAUDEmd(claudeMdPath, template.trim());
      results.push(`  ${DIM}CLAUDE.md: ${claudeMdPath}${RESET}`);
    }
  }

  // Generate a celebratory kaomoji
  let celebrationMoji = "(^ᗜ^)";
  try {
    celebrationMoji = execSync(`python "${GENERATOR_SCRIPT}" happy 1`, {
      encoding: "utf-8",
    }).trim();
  } catch {
    // fallback to static one
  }

  console.log(
    centerText(
      `${PINK}${BOLD}KMOJI INSTALLED SUCCESSFULLY ${celebrationMoji}${RESET}`,
      process.stdout.columns
    )
  );
  console.log();

  for (const line of results) {
    console.log(`  ${line}`);
  }

  console.log();

  if (installPlugin) {
    console.log(`  ${PINK}${BOLD}Restart Claude Code${RESET} to activate the /kmoji slash command.`);
    console.log();
  }

  console.log(
    centerText(
      `${PINK}Run ${BOLD}npx kmoji remove${RESET}${PINK} to uninstall${RESET}`,
      process.stdout.columns
    )
  );

  process.stdout.write(SHOW_CURSOR);
  rl.close();
}

async function runRemove() {
  process.stdout.write(HIDE_CURSOR);
  console.log(LOGO);
  console.log();

  const rl = createRL();

  const what = await ask(rl, "What do you want to remove?", [
    { label: "Everything (plugin + CLAUDE.md + hooks)" },
    { label: "Plugin only (keep CLAUDE.md templates)" },
    { label: "CLAUDE.md templates only (keep plugin)" },
  ]);

  const removePluginReg = what === "1" || what === "2";
  const removeClaudeMdReg = what === "1" || what === "3";

  const results = [];

  if (removePluginReg) {
    const unreg = unregisterPlugin();
    const disabled = disablePlugin();
    if (unreg || disabled) {
      results.push(`${GREEN}✓${RESET} Plugin unregistered`);
    } else {
      results.push(`${DIM}  No plugin registration found${RESET}`);
    }
  }

  if (removeClaudeMdReg) {
    const scope = await ask(rl, "Remove CLAUDE.md config from where?", [
      { label: "Global" },
      { label: "This project" },
      { label: "Both" },
    ]);

    const scopes = [];
    if (scope === "1" || scope === "3") scopes.push("global");
    if (scope === "2" || scope === "3") scopes.push("project");

    for (const s of scopes) {
      const claudeMdPath = getClaudeMdPath(s);
      const settingsPath = getSettingsPath(s);

      const removedMd = removeFromCLAUDEmd(claudeMdPath);
      const removedHook = removeHook(settingsPath);

      if (removedMd || removedHook) {
        results.push(`${GREEN}✓${RESET} Removed from ${s} (${claudeMdPath})`);
      } else {
        results.push(`${DIM}  No KMOJI config found in ${s}${RESET}`);
      }
    }
  }

  let sadMoji = "(╥﹏╥)";
  try {
    sadMoji = execSync(`python "${GENERATOR_SCRIPT}" sad 1`, {
      encoding: "utf-8",
    }).trim();
  } catch {
    // fallback
  }

  console.log();
  for (const line of results) {
    console.log(`  ${line}`);
  }
  console.log();
  console.log(`${PINK}KMOJI removed ${sadMoji}${RESET}`);

  if (removePluginReg) {
    console.log(`${DIM}Restart Claude Code to complete plugin removal.${RESET}`);
  }

  console.log(`${DIM}Run npx kmoji to reinstall anytime${RESET}`);

  process.stdout.write(SHOW_CURSOR);
  rl.close();
}

async function runGenerate() {
  const args = process.argv.slice(3);
  try {
    const result = execSync(
      `python "${GENERATOR_SCRIPT}" ${args.join(" ")}`,
      { encoding: "utf-8" }
    );
    console.log(result.trim());
  } catch (err) {
    console.error(`${PINK}Error:${RESET} Could not run generator.`);
    console.error(`Make sure Python 3.6+ is installed.`);
    process.exit(1);
  }
}

async function runStatus() {
  console.log(`${PINK}${BOLD}KMOJI Status${RESET}`);
  console.log();

  // Check plugin registration
  const pluginsPath = getInstalledPluginsPath();
  let pluginInstalled = false;
  if (fs.existsSync(pluginsPath)) {
    try {
      const data = JSON.parse(fs.readFileSync(pluginsPath, "utf-8"));
      pluginInstalled = !!(data.plugins && data.plugins["kmoji@kmoji"]);
    } catch {}
  }
  console.log(`  Plugin:       ${pluginInstalled ? `${GREEN}installed${RESET}` : `${DIM}not installed${RESET}`}`);

  // Check plugin enabled
  const settingsPath = path.join(getHomePath(), ".claude", "settings.json");
  let pluginEnabled = false;
  if (fs.existsSync(settingsPath)) {
    try {
      const settings = JSON.parse(fs.readFileSync(settingsPath, "utf-8"));
      pluginEnabled = !!(settings.enabledPlugins && settings.enabledPlugins["kmoji@kmoji"]);
    } catch {}
  }
  console.log(`  Enabled:      ${pluginEnabled ? `${GREEN}yes${RESET}` : `${DIM}no${RESET}`}`);

  // Check CLAUDE.md (global)
  const globalClaudeMd = getClaudeMdPath("global");
  let globalMd = false;
  if (fs.existsSync(globalClaudeMd)) {
    const content = fs.readFileSync(globalClaudeMd, "utf-8");
    globalMd = content.includes(KMOJI_START_MARKER);
  }
  console.log(`  CLAUDE.md:    ${globalMd ? `${GREEN}global${RESET}` : `${DIM}not in global${RESET}`}`);

  // Check CLAUDE.md (project)
  const projectClaudeMd = getClaudeMdPath("project");
  let projectMd = false;
  if (fs.existsSync(projectClaudeMd) && projectClaudeMd !== globalClaudeMd) {
    const content = fs.readFileSync(projectClaudeMd, "utf-8");
    projectMd = content.includes(KMOJI_START_MARKER);
  }
  if (projectMd) {
    console.log(`                ${GREEN}project${RESET}`);
  }

  // Check hook
  let hookInstalled = false;
  if (fs.existsSync(settingsPath)) {
    try {
      const settings = JSON.parse(fs.readFileSync(settingsPath, "utf-8"));
      hookInstalled = !!(settings.hooks && settings.hooks["kmoji-vibe"]);
    } catch {}
  }
  console.log(`  Error hook:   ${hookInstalled ? `${GREEN}installed${RESET}` : `${DIM}not installed${RESET}`}`);

  console.log();
  console.log(`  ${DIM}Plugin source: ${KMOJI_ROOT}${RESET}`);
}

// ── Entry Point ───────────────────────────────────────────────
async function main() {
  const command = process.argv[2];

  // Cleanup cursor on exit
  process.on("exit", () => process.stdout.write(SHOW_CURSOR));
  process.on("SIGINT", () => {
    process.stdout.write(SHOW_CURSOR);
    process.exit(0);
  });

  switch (command) {
    case "remove":
    case "uninstall":
      await runRemove();
      break;
    case "generate":
    case "gen":
      await runGenerate();
      break;
    case "status":
      await runStatus();
      break;
    case "install":
    case undefined:
      await runInstall();
      break;
    default:
      console.log(LOGO);
      console.log();
      console.log(`${PINK}Usage:${RESET}`);
      console.log(`  npx kmoji              Install KMOJI (interactive)`);
      console.log(`  npx kmoji remove       Uninstall KMOJI`);
      console.log(`  npx kmoji status       Check installation status`);
      console.log(`  npx kmoji generate     Generate kaomojis`);
      console.log(`  npx kmoji gen happy 5  Generate 5 happy kaomojis`);
      break;
  }
}

main().catch((err) => {
  console.error(err);
  process.stdout.write(SHOW_CURSOR);
  process.exit(1);
});
