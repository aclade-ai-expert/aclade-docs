# Python SDK reference (PyPI `aclade`)

`import aclade` — the official, **stdlib-only** client for the Aclade platform. Zero third-party dependencies (it speaks JSON over `urllib`), Python 3.8+, any OS CPython runs on.

The SDK is a *client*, not a harness: it holds your signed token and calls the platform. Reasoning, model keys, metering, and tenant data stay on `aclade.com`.

## Install

```bash
pip install aclade
```

## Authentication

Token resolution, in order:

1. `$ACLADE_TOKEN` environment variable
2. `~/.aclade-agent.json` — the file the [npm connector](cli-reference.md) writes, so machines that already run `aclade connect` need no extra setup (reads `{"token": …}` or a bare token string)
3. `~/.aclade/token`

Issue tokens in the portal: **Settings → Local Agent**. They are signed, workspace-scoped, and expire after **12 hours**.

```python
import aclade

team = aclade.Aclade()                     # auto-loads the token
team = aclade.Aclade(token="eyJ…")         # explicit
team = aclade.Aclade(base_url="https://aclade.com", timeout=300)
```

If no token can be found, construction raises `AcladeError` with a pointer to the portal.

## Identity (read from your own token)

```python
team.company_id    # "co_…"
team.member_id     # "m_…"
team.name          # display name on the token
```

## Roster

```python
team.workspace()      # full durable workspace: {"workspace": {company, members, …}}
team.members()        # everyone on the roster (humans and experts)
team.experts()        # the rented AI experts only
team.expert("Sarah")  # one expert by id or case-insensitive name substring
```

`expert()` raises `AcladeError("No expert matching …")` when nothing fits — the message suggests running `aclade experts`.

## Delegation

```python
result = team.delegate(expert, task, answers=None, attachments=None)
```

`expert` accepts an expert dict (from `experts()`/`expert()`) or a name/id string. The call **blocks until the platform returns** (default timeout 300 s — raise `timeout=` in the constructor for long jobs). The result has one of three statuses:

| `result["status"]` | Meaning | What to do |
|---|---|---|
| `completed` | The work is done | Read `result["run"]["report"]` |
| `needs-input` | The expert has clarifying questions | Read `result["questions"]`, re-call with `answers={"…": "…"}` (same task) |
| `needs-approval` | A high-risk step awaits a human | The workspace admin gets an approve/deny email; nothing runs unattended |

```python
result = team.delegate("Priya", "Draft the Q3 status report for the exec team")
if result["status"] == "completed":
    print(result["run"]["report"])
elif result["status"] == "needs-input":
    print(result["questions"])
    result = team.delegate("Priya", "Draft the Q3 status report for the exec team",
                           answers={"audience": "exec", "tone": "formal"})
    print(result["run"]["report"])
```

## Observability

```python
team.pending_tasks()     # {"pendingByExpert": {"<expertId>": <count>, …}}
team.connector_status()  # local-agent fleet for this workspace: installs, online, agents[]
```

`connector_status()` returns the same data `aclade status` (npm) prints: `installs`, `connected`, and per-agent `hostname`, `platform`, `version`, `online`, `tasksExecuted`, `lastSeenAt`.

## Errors

```python
from aclade import Aclade, AcladeError

try:
    result = team.delegate("Nobody", "…")
except AcladeError as e:
    e.status   # HTTP status (401, 403, 500…) or 0 for local/config errors
    e.message  # human-readable detail
```

`401` means the token is invalid or expired — reissue it in the portal. `403` means the token's workspace doesn't match the resource. `0` means the SDK couldn't even make the call (no token, unknown expert, …).

## Command line

Installing the package provides an `aclade` console command (see the [getting started](getting-started.md) note if you also have the npm CLI):

```
aclade [--token T] [--host URL] {whoami, experts, run, tasks, agent}
```

| Command | What it does |
|---|---|
| `whoami` | Prints the identity carried by the token (name, companyId, memberId, baseUrl) |
| `experts` | Lists the roster's AI experts: `name  role  title` |
| `run <expert> <task> [--answers <json>]` | Delegates and prints the outcome: the report on `completed`, the questions on `needs-input`, the approval notice on `needs-approval`, raw JSON otherwise |
| `tasks` | Pending tasks by expert |
| `agent` | Fleet summary: `Installs: N   Online: M` + one line per agent |

`--host` defaults to `https://aclade.com`. Exit codes: `0` success, `1` request/HTTP error, `2` usage/config error (bad token source, malformed `--answers` JSON).

```bash
aclade whoami
aclade experts
aclade run "Sarah" "Triage this morning's inbox and list what needs a human"
aclade run "Sarah" "Draft the report" --answers '{"audience": "exec"}'
aclade tasks
aclade agent
```

## Example scripts

- [quickstart.py](../examples/python/quickstart.py) — list experts, delegate, print the report
- [delegate_with_answers.py](../examples/python/delegate_with_answers.py) — handle the `needs-input` round trip
- [watch_tasks.py](../examples/python/watch_tasks.py) — poll pending work

## What the SDK deliberately is not

No AI logic, no model keys, no billing state, no tenant data storage — it's a thin, inspectable API client (like `stripe` to Stripe). If a method can't be explained as "call this endpoint, parse that JSON," it doesn't belong here.
