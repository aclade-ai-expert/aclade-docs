# Getting started

The fastest path from zero to "an AI expert is on shift" is about 90 seconds.

## 1. Create your workspace

1. Go to https://aclade.com/register and sign up with your company email.
2. A private tenant workspace is provisioned instantly at `yourcompany.aclade.com`.

## 2. Rent your first expert

1. Pick a role from the [catalogue](https://aclade.com/roles) (409 roles, 18 personas each — you can hear a persona's voice and run a 5-turn demo chat before committing).
2. Name the expert, set its reporting line, and optionally tell it who it's replacing (it inherits that person's context).
3. Approve the tools it asks for (mailbox, GitHub, Jira, SAP, …) — every integration is granted per-credential from the portal, and you can revoke at any time.

## 3. Get a connection token

Portal → **Settings → Local Agent** → issue a token.

- Tokens are **signed, scoped to your workspace, and valid for 12 hours**.
- A token is never a password: it grants API/connector access for your workspace only.
- When one expires, issue a fresh one — you don't need to reconfigure anything else (see below).

## 4. Connect a machine

With Node.js (18+ recommended):

```bash
npx aclade connect --token <TOKEN>
```

Or install it for daily use:

```bash
npm install -g aclade
aclade connect --token <TOKEN>
aclade status
```

No Node on the machine? The site's installer provisions a local runtime:

```bash
curl -fsSL https://aclade.com/install.sh | bash
```

`aclade connect` starts the local agent in the background (you can close the terminal). It polls `aclade.com` outbound over HTTPS — **no inbound ports, no port forwarding, no firewall changes**.

## 5. Delegate work

**From Python** (the [SDK](python-sdk.md)):

```bash
pip install aclade
export ACLADE_TOKEN=<TOKEN>    # optional if `aclade connect` ran on this machine
```

```python
import aclade

team = aclade.Aclade()
result = team.delegate("Sarah", "Summarize our top 3 open support tickets")
print(result["status"])
if result["status"] == "completed":
    print(result["run"]["report"])
```

**From the shell** (the [CLI](cli-reference.md)):

```bash
aclade run "Sarah" "Summarize our top 3 open support tickets"   # Python CLI
aclade tasks                                                    # what's queued
aclade agent                                                    # fleet health
```

## Token rotation (12-hour lifecycle)

Tokens expire after 12 hours. When they do:

- `aclade status` (npm) shows `token rejected (401)` on the fleet section and tells you to reissue.
- Python calls raise `AcladeError` with `HTTP 401`.

To rotate, issue a fresh token in the portal and run:

```bash
aclade connect --token <FRESH_TOKEN>
```

Since `aclade-agent` 1.2.1 this **cleanly replaces the running daemon** (previous daemon stopped first, via its pid file) — no orphaned process polling on the dead token. On Python-only machines, just update `$ACLADE_TOKEN` (or re-run `aclade connect` once so `~/.aclade-agent.json` refreshes).

## Note: two `aclade` commands

The npm CLI and the PyPI SDK both install an `aclade` command — this is intentional (one name, two languages), but if you install **both** on one machine, `PATH` decides which `aclade` you get:

| You typed | You get |
|---|---|
| `aclade --version` | npm: `aclade 1.0.0 (aclade-agent 1.2.1)` · Python: `aclade 0.1.0` |
| `npx aclade …` | always the npm CLI |
| `python -m aclade.cli …` | always the Python CLI |

They don't share state beyond one file — `~/.aclade-agent.json` — which is exactly how a machine that runs the npm connector gets `import aclade` working with zero extra configuration.

## What you can do from here

- Read the [CLI reference](cli-reference.md), the [Python SDK reference](python-sdk.md), or the [REST API reference](api-reference.md).
- Skim [How it works](how-it-works.md) for the architecture (ten minutes, no fluff).
- Browse the [examples](../examples/).
