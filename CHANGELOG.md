# Changelog

## 2026-09-28 — first public release

### npm `aclade` 1.0.0

- First release. The CLI front door for the Aclade local connector:
  - first-run banner with a three-step quickstart
  - `aclade status` — local daemon state, last log lines, and the live fleet as seen by aclade.com (with graceful handling of expired 12-hour tokens)
  - `aclade stop` — clean daemon shutdown (SIGTERM, SIGKILL fallback after 3 s, stale-pid cleanup)
  - `aclade --version` — reports both the wrapper and the underlying `aclade-agent` versions
  - every other argument is delegated verbatim to `aclade-agent` (including `connect`), so the wrapper can never drift from connector behaviour
- `curl -fsSL https://aclade.com/install.sh | bash` now launches `npx aclade` (a bundled Node runtime is provisioned on machines without one).

### PyPI `aclade` 0.1.0

- First release. A stdlib-only client for the Aclade platform — zero third-party dependencies, Python 3.8+.
- `aclade.Aclade` client: token auto-load (`$ACLADE_TOKEN` → `~/.aclade-agent.json` → `~/.aclade/token`), `workspace()`, `members()`, `experts()`, `expert(name_or_id)`, `delegate(expert, task, answers, attachments)`, `pending_tasks()`, `connector_status()`.
- `aclade` console CLI: `whoami`, `experts`, `run <expert> <task> [--answers <json>]`, `tasks`, `agent`.
- Documents the three delegation outcomes: `completed` (report), `needs-input` (questions → re-call with answers), `needs-approval` (human approval by email for high-risk steps).

### npm `aclade-agent` 1.2.1

- Daemon lifecycle fix: the agent now writes `~/.aclade-agent.pid`, and re-running `connect` stops any previous daemon first (with a pid-reuse guard). Rotating a 12-hour token no longer strands an orphaned daemon.
- `aclade stop` (npm `aclade`) uses the same pid file for a clean shutdown.
