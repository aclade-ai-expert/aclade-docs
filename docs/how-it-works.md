# How it works

Ten minutes, no fluff. What Aclade is architecturally, and why the clients (this repo's packages) are so small.

## The one-line version

Aclade experts are **persistent, autonomous workers** — not chat sessions. Each has an identity (name, avatar, voice), a schedule, long-term memory scoped to your tenant, and access only to the tools you approve. The intelligence runs on `aclade.com`; your machine and your scripts talk to it with a signed, short-lived token.

## The thin-client principle

Everything the client packages do fits in one sentence each:

- **npm `aclade` / `aclade-agent`** — a background process that *polls* the platform outbound over HTTPS and executes approved, workspace-scoped actions on your machine (files, git, local tools). It opens **no inbound ports**.
- **PyPI `aclade`** — an HTTP client that *delegates* work to the platform and reads results. It contains no model, no prompt, no key, no AI code at all.

That asymmetry is the security model: the interesting surface (reasoning, credentials, metering) is one server fleet you can harden, audit, and isolate — not N machines on the internet.

## Tenant isolation

- Every company gets a workspace at `yourcompany.aclade.com` with its own durable state (roster, memories, tasks, history).
- Tokens carry a `companyId`; endpoints enforce it. An expert rented by two companies keeps separate memories and can't cross-read.
- Integration credentials are stored server-side and granted **per credential, per human approval** — the expert requests, the owner decides, revocation is immediate.

## The local connector, step by step

1. You run `aclade connect --token <T>`. The agent stores `{token, host}` in `~/.aclade-agent.json` and daemonizes (`~/.aclade-agent.pid`, log in `~/.aclade-agent.log`).
2. It polls `aclade.com` on an outbound HTTPS connection. Nothing listens on your machine.
3. When your workspace has work that requires your machine, the platform queues it; the agent executes within the token's scope — and actions a token can't authorize simply don't exist for it.
4. High-risk steps don't execute at all: the task returns `needs-approval`, and a human in your workspace approves or denies by email.
5. `aclade status` shows the daemon, the log tail, and the whole fleet (installs/online per agent). `aclade stop` ends it cleanly. Since `aclade-agent` 1.2.1, re-running `connect` replaces the old daemon instead of stranding it — which matters because tokens rotate every 12 hours.

## Delegation lifecycle (what `delegate()` returns)

```
you ──task──▶ expert
                │
                ├─ completes the work ──────────────▶ status: "completed"   → run.report
                ├─ needs a decision from you ───────▶ status: "needs-input" → questions[] → re-call with answers
                └─ hits a high-risk action ─────────▶ status: "needs-approval" → human approves/denies by email
```

Nothing sensitive happens without either your input or an explicit human approval.

## Billing

Per second of actual work, no seat, no minimum. Launch offer: 1/10 of baseline rates — $1.80–$18/hr effective (baseline catalogue $18–$180/hr), USD/EUR/INR. Kill the job and the meter stops.

## Where the limits are (honestly)

The platform publishes its gaps alongside its wins at https://aclade.com/compare: talking-head avatar video, SOC 2/ISO certification, and enterprise SSO/SCIM are on the roadmap, not in the product. If your use case needs one of those today, that page says who to pick instead.
