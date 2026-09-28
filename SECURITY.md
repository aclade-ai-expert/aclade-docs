# Security policy

Aclade takes the security of its platform and of customer workspaces seriously.

## Reporting a vulnerability

**Please do not open a public issue for a security concern.** Report it to **enterprise@aclade.com** with "Security" in the subject line, including:

- the affected package or endpoint (npm `aclade` / `aclade-agent`, PyPI `aclade`, or a platform URL)
- steps to reproduce
- any evidence (screenshots, request/response pairs — redact tokens)

We aim to acknowledge reports within 48 hours and will keep you informed while we investigate.

## Design notes relevant to security

- Connection tokens are **signed, workspace-scoped, and expire after 12 hours** — a leaked token is both limited in blast radius and short-lived. Reissue from the portal (Settings → Local Agent).
- The local connector opens **no inbound ports**: it polls outbound over HTTPS only, and every action is scoped to the token's workspace.
- **High-risk steps require human approval**: delegation returns `needs-approval` and the workspace admin gets an approve/deny email; nothing sensitive executes unattended.
- **Tenants are isolated**: each company's memory, tasks, and history live only under its own workspace (`yourcompany.aclade.com`).
