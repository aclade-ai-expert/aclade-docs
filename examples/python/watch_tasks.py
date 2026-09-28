#!/usr/bin/env python3
"""Watch what's queued across your team, and how the local-agent fleet looks.

Run:  python watch_tasks.py [seconds-between-polls]
"""
import sys
import time
import aclade

team = aclade.Aclade()
interval = float(sys.argv[1]) if len(sys.argv) > 1 else 30.0
by_name = {m.get("id"): m.get("name", m.get("id")) for m in team.members()}

try:
    while True:
        pending = team.pending_tasks().get("pendingByExpert") or {}
        if pending:
            for expert_id, count in sorted(pending.items(), key=lambda kv: -kv[1]):
                print(f"  {by_name.get(expert_id, expert_id):<24} {count} queued")
        else:
            print("  (nothing queued)")
        fleet = team.connector_status()
        print(f"  fleet: {fleet.get('installs', 0)} install(s), {fleet.get('connected', 0)} online")
        time.sleep(interval)
except KeyboardInterrupt:
    pass
