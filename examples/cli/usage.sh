#!/usr/bin/env bash
# Aclade CLI — common patterns (npm `aclade` and the PyPI `aclade` CLI).
#
# NOTE: both packages install an `aclade` command. `aclade --version` tells
# you which one you have:
#   aclade 1.0.0 (aclade-agent 1.2.1)   <- npm CLI
#   aclade 0.1.0                        <- Python SDK CLI
# Use `npx aclade …` or `python -m aclade.cli …` to remove the ambiguity.

set -euo pipefail

# ---------------------------------------------------------------- npm CLI ----

# Connect this machine to your workspace (token: portal -> Settings -> Local Agent).
# Starts the local connector in the background; safe to close the terminal.
npx aclade connect --token "$ACLADE_TOKEN"

# Where things stand: daemon, log tail, and the live fleet.
npx aclade status

# Rotate a 12-hour token — the previous daemon is replaced, not stranded.
npx aclade connect --token "$FRESH_TOKEN"

# Connect a machine without Node (the installer provisions a local runtime).
curl -fsSL https://aclade.com/install.sh | bash

# Stop the local connector cleanly.
npx aclade stop

# ------------------------------------------------------------ Python CLI ----

# (pip install aclade; token auto-loaded from $ACLADE_TOKEN or ~/.aclade-agent.json)

aclade whoami                    # identity carried by the token
aclade experts                   # who's on the roster

# Delegate and wait for the report.
aclade run "Sarah" "Triage this morning's inbox and list what needs a human"

# The expert asked clarifying questions? Answer and go again:
aclade run "Sarah" "Draft the Q3 status report" --answers '{"audience": "exec", "tone": "formal"}'

# What's queued, and is the fleet healthy?
aclade tasks
aclade agent

# ----------------------------------------------------------------- notes ----
# • The Python CLI and the SDK share one token file with the npm connector
#   (~/.aclade-agent.json) — connect once, `import aclade` just works.
# • Every command prints human-readable output; `aclade run` falls back to
#   raw JSON for statuses outside completed/needs-input/needs-approval.
