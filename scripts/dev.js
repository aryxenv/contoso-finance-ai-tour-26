#!/usr/bin/env node

/**
 * Starts PostgreSQL via Docker, waits for it to be healthy,
 * runs Alembic migrations, then launches Turborepo dev.
 */

const { execSync, spawn } = require("child_process");
const { resolve } = require("path");

const ROOT = resolve(__dirname, "..");
const SERVER = resolve(ROOT, "apps", "server");
const COMPOSE_FILE = resolve(ROOT, "docker", "docker-compose.yml");

function run(cmd, opts = {}) {
  console.log(`\x1b[36m$ ${cmd}\x1b[0m`);
  execSync(cmd, { stdio: "inherit", ...opts });
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function waitForPostgres(maxRetries = 30) {
  for (let i = 1; i <= maxRetries; i++) {
    try {
      execSync(
        `docker compose -f "${COMPOSE_FILE}" exec -T postgres pg_isready -U postgres`,
        { stdio: "ignore" }
      );
      return;
    } catch {
      if (i === maxRetries) throw new Error("PostgreSQL did not become ready");
      process.stdout.write(
        `\x1b[33mWaiting for PostgreSQL... (${i}/${maxRetries})\x1b[0m\r`
      );
      await sleep(1000);
    }
  }
}

async function main() {
  console.log("\n\x1b[1m🐘 Starting PostgreSQL...\x1b[0m\n");
  run(`docker compose -f "${COMPOSE_FILE}" up -d postgres`);

  console.log("\n\x1b[1m⏳ Waiting for PostgreSQL to be ready...\x1b[0m\n");
  await waitForPostgres();
  console.log("\x1b[32m✓ PostgreSQL is ready\x1b[0m\n");

  console.log("\x1b[1m🔄 Running database migrations...\x1b[0m\n");
  run("uv run alembic upgrade head", {
    cwd: SERVER,
    env: { ...process.env, PYTHONPATH: resolve(SERVER, "src") },
  });
  console.log("\n\x1b[32m✓ Migrations complete\x1b[0m\n");

  console.log("\x1b[1m🚀 Starting dev servers...\x1b[0m\n");
  const turbo = spawn("npx", ["turbo", "dev"], {
    cwd: ROOT,
    stdio: "inherit",
    shell: true,
  });

  let cleaning = false;
  function cleanup() {
    if (cleaning) return;
    cleaning = true;
    console.log("\n\x1b[1m🐘 Stopping PostgreSQL...\x1b[0m\n");
    try {
      execSync(`docker compose -f "${COMPOSE_FILE}" down`, {
        stdio: "inherit",
      });
    } catch {
      // ignore errors during cleanup
    }
    console.log("\n\x1b[32m✓ All stopped. Press Enter to exit.\x1b[0m");
    process.stdin.once("data", () => process.exit(0));
    process.stdin.resume();
  }

  turbo.on("exit", () => cleanup());
  process.on("SIGINT", () => {
    try {
      turbo.kill();
    } catch {
      /* already dead */
    }
    cleanup();
  });
}

main().catch((err) => {
  console.error(`\n\x1b[31m✗ ${err.message}\x1b[0m\n`);
  process.exit(1);
});
