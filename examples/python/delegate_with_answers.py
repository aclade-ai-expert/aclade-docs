#!/usr/bin/env python3
"""Delegate a task and answer the expert's clarifying questions when asked.

`delegate()` blocks until the platform returns one of:
  completed      -> run.report has the work
  needs-input    -> questions[] needs your answers; re-call with answers={...}
  needs-approval -> a human approves/denies by email; nothing runs unattended

Run:  python delegate_with_answers.py
"""
import sys
import aclade

team = aclade.Aclade()
expert = "Sarah"  # any name substring from `aclade experts`, or an expert dict
task = "Draft the weekly status report for the exec team"

ANSWERS = {  # pre-filled answers for questions we know the shape of
    "audience": "executive leadership",
    "tone": "formal, concise",
    "length": "one page",
}


def ask_questions(questions) -> dict:
    """Prompt interactively for anything we don't already have an answer to."""
    answers = dict(ANSWERS)
    for q in questions:
        prompt = q if isinstance(q, str) else str(q.get("question", q))
        key = q.get("key") if isinstance(q, dict) else prompt
        if key in answers:
            print(f"  {prompt}  ->  {answers[key]}  (pre-filled)")
            continue
        answers[key] = input(f"  {prompt}  ->  ").strip()
    return answers


result = team.delegate(expert, task)
for _ in range(3):  # a few rounds of clarification is normal
    if result.get("status") == "completed":
        print("\n=== REPORT ===")
        print(result["run"]["report"])
        break
    if result.get("status") == "needs-input":
        print("The expert needs input:")
        answers = ask_questions(result.get("questions") or [])
        result = team.delegate(expert, task, answers=answers)
        continue
    if result.get("status") == "needs-approval":
        print("A high-risk step requires approval — the admin email link is on its way.")
    print(result, file=sys.stderr)
    break
else:
    print("Still needs input after 3 rounds — answer it from the portal.", file=sys.stderr)
    sys.exit(1)
