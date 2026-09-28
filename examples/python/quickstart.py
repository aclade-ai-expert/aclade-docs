#!/usr/bin/env python3
"""List your experts and delegate a task.

Requires a token, in order of preference:
  1. export ACLADE_TOKEN=<token from the portal>
  2. or run `aclade connect --token <token>` (npm) on this machine once —
     the SDK reads ~/.aclade-agent.json automatically.

Run:  python quickstart.py
"""
import aclade

team = aclade.Aclade()
print(f"Signed in as {team.name!r}  (workspace {team.company_id})")

experts = team.experts()
if not experts:
    raise SystemExit("No experts on the roster yet — rent one at https://aclade.com/rent")

print("Your team:")
for e in experts:
    print(f"  - {e['name']:<24} {e.get('title', '')}")

task = "Reply with a one-line status on your current work"
result = team.delegate(experts[0], task)

print(f"\nStatus: {result.get('status')}")
if result.get("status") == "completed":
    print(result["run"]["report"])
elif result.get("status") == "needs-input":
    print("The expert has questions — see delegate_with_answers.py:")
    for q in result.get("questions") or []:
        print("  -", q)
elif result.get("status") == "needs-approval":
    print("A high-risk step is awaiting human approval (admin email is on its way).")
