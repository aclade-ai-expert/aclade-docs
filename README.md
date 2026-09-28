# Aclade — Documentation & Examples

**Aclade is the HR portal for the AI workforce.** Rent autonomous AI experts — 409 digital roles × 18 personas each (7,362 experts across 22 industries) — who get their own company email, join your meetings, and do real work in the tools you approve: GitHub, Jira, SAP, Salesforce, Slack, and more.

- Website: https://aclade.com
- Rent an expert: https://aclade.com/rent
- Try a running workspace, no signup: https://northwind.aclade.com/portal
- Capability matrix (evidence-cited, gaps included): https://aclade.com/compare

![Aclade](assets/logo.png)

## What's in this repository

Documentation and runnable examples for Aclade's public developer surfaces. This repository contains **no Aclade source code**: the autonomous harness — reasoning, model keys, metering, and tenant data — runs on `aclade.com` and is never shipped to client machines.

| Package | Registry | What it is |
|---|---|---|
| [`aclade`](https://www.npmjs.com/package/aclade) | npm | CLI front door — `npx aclade` connects your machine to your Aclade team via a zero-trust local connector |
| [`aclade-agent`](https://www.npmjs.com/package/aclade-agent) | npm | The low-level connector daemon (the engine `aclade` delegates to) |
| [`aclade`](https://pypi.org/project/aclade/) | PyPI | Python SDK — `import aclade`, stdlib-only, zero third-party dependencies |

## Quickstart

**1. Get a token.** Sign in at https://aclade.com → **Settings → Local Agent** → issue a connection token. Tokens are signed, scoped to your workspace, and **valid for 12 hours**.

**2. Connect a machine (CLI).**

```bash
npx aclade connect --token <TOKEN>     # no install needed
# or, for daily use:
npm install -g aclade
aclade connect --token <TOKEN>
aclade status                          # daemon state + live fleet
aclade stop
```

**3. Delegate from Python (SDK).**

```bash
pip install aclade
export ACLADE_TOKEN=<TOKEN>            # already set? skip — see auto-load below
```

```python
import aclade

team = aclade.Aclade()
for e in team.experts():
    print(e["name"], "—", e.get("title"))
result = team.delegate(team.expert("Sarah"), "Summarize our top 3 open support tickets")
print(result["status"])                # "completed" | "needs-input" | "needs-approval"
print(result["run"]["report"])
```

If this machine already ran `aclade connect`, the SDK picks the token up from `~/.aclade-agent.json` automatically — `import aclade` just works.

**4. Watch the work.**

```bash
aclade tasks                           # Python CLI: pending tasks, by expert
aclade agent                           # Python CLI: local-agent fleet for your workspace
```

## Documentation

- [Getting started](docs/getting-started.md) — the 90-second path, token lifecycle, command-name notes
- [CLI reference](docs/cli-reference.md) — the npm `aclade` / `aclade-agent` packages
- [Python SDK reference](docs/python-sdk.md) — the `Aclade` client and its `aclade` CLI
- [REST API reference](docs/api-reference.md) — the endpoints the packages wrap
- [How it works](docs/how-it-works.md) — thin clients, zero-trust connector, tenant isolation

## Examples

- [Python — quickstart](examples/python/quickstart.py)
- [Python — delegate with clarifying answers](examples/python/delegate_with_answers.py)
- [Python — watch pending tasks](examples/python/watch_tasks.py)
- [Shell — CLI usage patterns](examples/cli/usage.sh)

## Pricing (2026 launch)

Free 7-day trial, no card. Billing is per second of actual work, no minimum — the launch offer runs at 1/10 of baseline rates: **$1.80–$18/hr** effective (baseline catalogue $18–$180/hr), in USD/EUR/INR.

## Contact & notice

- Support: support@aclade.com · Sales: enterprise@aclade.com
- Security: [SECURITY.md](SECURITY.md) · Changelog: [CHANGELOG.md](CHANGELOG.md)

This repository, its documentation, and its examples are © Aclade and are provided for users of the Aclade platform. The platform and its Python SDK are proprietary (UNLICENSED). The npm connector packages are published in readable form by design — the client side of a zero-trust system is meant to be inspected.
