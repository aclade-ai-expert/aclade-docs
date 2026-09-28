# REST API reference

The endpoints below are the **stable client surface** the npm CLI and the Python SDK wrap. The platform exposes more to its own portal application; treat everything not documented here as internal.

- **Base URL:** `https://aclade.com`
- **Format:** JSON in, JSON out
- **Auth:** `Authorization: Bearer <token>`

## Authentication

Portal-issued connection tokens (Settings → Local Agent) are **signed base64url JSON** — `payload.signature`. The payload carries:

```json
{ "companyId": "co_…", "memberId": "m_…", "superAdmin": false, "name": "…", "exp": 1790000000 }
```

- Scoped to one workspace; requests for other tenants are rejected.
- **Valid 12 hours** (`exp`). Reissue in the portal on expiry.
- A client may decode its own payload to display identity (the SDK's `whoami` does exactly this, offline).

Error shape is uniform: `{"error": "…"}` with an HTTP status — `400` validation, `401` unauthenticated/expired, `403` outside your workspace, `500` platform error.

## Endpoints

### `GET /api/workspace?companyId=<id>`

The durable company workspace.

```json
{ "workspace": { "companyId": "co_…", "company": { "id", "name", "slug", "domain", … }, "members": [ … ] } }
```

Each member: `id`, `companyId`, `name`, `email`, `role`, `title`, `reportsTo`, `kind` (`human`/`ai`), `origin` (`seed`/`rented`), `status`, `joinedAt`, and for rented experts an `expert` block (`catalogRole`, `budget`, `schedule`, `activities`, `integrations`, `provisioning`).

### `PUT /api/workspace`

Replace the workspace roster. Body: `{ "companyId", "company": {…}, "members": [ … ] }` (members must carry the token's `companyId`).

```json
{ "ok": true, "updatedAt": "2026-09-28T06:13:28.220Z" }
```

### `POST /api/experts/run`

Delegate a task to an expert and wait for the outcome.

Request body:

```json
{
  "expert": {
    "id": "m_…", "companyId": "co_…", "name": "Sarah",
    "role": "Customer Success Lead", "roleId": "customer-success",
    "personaId": "sarah-…", "companyDomain": "yourco.com", "email": "sarah@yourco.com",
    "activities": ["…"], "integrations": ["email", "jira"],
    "replacingName": null, "replacingContext": null
  },
  "task": "Summarize our top 3 open support tickets",
  "answers": { "audience": "exec" },
  "attachments": [ ]
}
```

`answers` is supplied on a follow-up call after a `needs-input` response; the Python SDK builds the `expert` block for you from your roster.

Response:

```json
{
  "status": "completed",
  "run": { "report": "…the work, as the expert reports it…" },
  "brain": "…",
  "recognizedFromMemory": false
}
```

| `status` | Follow-up |
|---|---|
| `completed` | read `run.report` |
| `needs-input` | read `questions[]`, re-POST the same task with `answers` |
| `needs-approval` | a high-risk step is gated; the workspace admin receives an approve/deny email |

### `GET /api/tenant/pending-tasks`

Work currently queued, per expert:

```json
{ "pendingByExpert": { "m_…": 2 } }
```

### `GET /api/connector/token`

The local-agent fleet for the token's workspace, as seen by the platform:

```json
{
  "installs": 2,
  "connected": 1,
  "agents": [
    { "hostname": "laptop", "platform": "darwin", "version": "1.2.1",
      "online": true, "tasksExecuted": 14, "lastSeenAt": 1790000000000 }
  ]
}
```

### `GET /api/security/status`

Public (no auth): platform and shield status — a useful liveness probe.

## curl walkthrough

```bash
TOK="<token from the portal>"

curl -s https://aclade.com/api/workspace?companyId="co_…" -H "Authorization: Bearer $TOK" | python3 -m json.tool

curl -s https://aclade.com/api/tenant/pending-tasks -H "Authorization: Bearer $TOK"

curl -s https://aclade.com/api/experts/run -H "Authorization: Bearer $TOK" \
  -H "Content-Type: application/json" -d '{
    "expert": { "id": "m_…", "companyId": "co_…", "name": "Sarah",
                "role": "Customer Success Lead", "roleId": "customer-success",
                "companyDomain": "yourco.com", "email": "sarah@yourco.com",
                "activities": [], "integrations": [] },
    "task": "Summarize our top 3 open support tickets"
  }'
```

## Billing note

Work delegated through the API is metered per second, exactly like portal work — the launch offer (1/10 of baseline rates, $1.80–$18/hr effective) and the free 7-day trial apply.
