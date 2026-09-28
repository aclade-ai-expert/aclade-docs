# CLI reference (npm `aclade` / `aclade-agent`)

Two packages, one command:

- **`aclade`** — the front door humans type. Banner quickstart, `status`, `stop`, `--version`; everything else is delegated verbatim to the connector.
- **`aclade-agent`** — the local connector daemon: config, background process, outbound polling to `aclade.com`.

`aclade` depends on `aclade-agent` and forwards to it, so the two can never drift out of sync. Run `aclade --version` to see both: `aclade 1.0.0 (aclade-agent 1.2.1)`.

## Install

```bash
# one-off, no install:
npx aclade

# or globally:
npm install -g aclade

# machines without Node: the site's installer provisions a local runtime
curl -fsSL https://aclade.com/install.sh | bash
```

Requirements: Node.js 18+ (LTS recommended), macOS / Linux / Windows.

## Commands

### `aclade` (no arguments) or `aclade --help`

Prints the banner: what Aclade is, a three-step quickstart (get token → `aclade connect --token <TOKEN>` → `aclade status`), and the command list.

### `aclade --version` / `-v`

```
aclade 1.0.0 (aclade-agent 1.2.1)
```

### `aclade connect --token <TOKEN> [flags]`

Starts (or **replaces**) the local agent in the background. Safe to run from a laptop you close afterwards — the daemon detaches.

| Flag | Meaning |
|---|---|
| `--token <T>` | Connection token from the portal (Settings → Local Agent). Valid 12 hours. |
| `--host <url>` | Platform base URL. Defaults to `https://aclade.com`. |
| `--workspace <path>` | Root directory the agent may act on for file-based work. |

On `aclade-agent` ≥ 1.2.1, if a previous daemon is running it is **stopped first** (pid file, with a pid-reuse guard) — rotating your 12-hour token never strands an orphaned process.

### `aclade status`

Reports, top to bottom:

1. **Local agent** — configured or not (host, workspace root).
2. **Daemon** — running (pid) / not running / stale pid file.
3. **Last log lines** — tail of `~/.aclade-agent.log`.
4. **Fleet on aclade.com** — installs and online agents for your workspace, each with hostname, platform, version, tasks executed, last-seen. If the token expired you'll see `token rejected (401)` with a reissue hint instead of a crash.

### `aclade stop`

Sends SIGTERM to the daemon from its pid file, waits up to 3 s, escalates to SIGKILL if needed, and cleans up stale pid files. Prints `Agent stopped (pid N).`

### Anything else

Passed **straight through** to `aclade-agent` with the same stdout/stderr and exit code. So every flag the connector documents works via the wrapper: `aclade connect …`, `aclade-agent` subcommands, etc.

## Files on your machine

| Path | Contents |
|---|---|
| `~/.aclade-agent.json` | `{ "token", "host", "workspaceRoot" }` — also read automatically by the [Python SDK](python-sdk.md) |
| `~/.aclade-agent.log` | Daemon log (connect/heartbeats/errors) |
| `~/.aclade-agent.pid` | Daemon pid (written since `aclade-agent` 1.2.1) |

The token is the only secret at rest. Remove the connector completely with `aclade stop && rm ~/.aclade-agent.json ~/.aclade-agent.log ~/.aclade-agent.pid`.

## Exit codes

- `0` — success
- `1` — error (missing token, connector failure); `status` degrades gracefully instead of failing on an expired fleet token
- passthrough commands exit with the connector's own code

## Python?

The npm CLI manages the local machine; the PyPI SDK drives the platform from scripts. They complement each other — see the [Python SDK reference](python-sdk.md) and the [getting started](getting-started.md) note on the shared `aclade` command name.
