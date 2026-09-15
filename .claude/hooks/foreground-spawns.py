#!/usr/bin/env python3
"""Every spawn in this repo waits for what it starts, enforced outside the model.

A spawn that is not held to the foreground responds the moment it is made, so the agent that
made it replies and ends before its own worker comes back, and what that worker left is never
read or signed off. The agent type's `background` field does not reach this decision: the
definition is only consulted when the harness builds the call, never when an agent writes one.

This runs as a PreToolUse hook on the Agent tool and refuses any spawn that does not carry
`run_in_background` set to false. It lives in this repository, so it binds this team's runs
and no other.
"""

import json
import sys

#: The argument that decides whether a spawn waits, and the only value this repo allows.
ARGUMENT = "run_in_background"

REFUSED = f"This repository's runs spawn in the foreground. Make the call again with {ARGUMENT} set to false."


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        # A hook that cannot read its own input refuses, because the alternative is a hole
        # that opens exactly when something has already gone wrong.
        payload = {}
    if payload.get("tool_name") != "Agent":
        return
    if (payload.get("tool_input") or {}).get(ARGUMENT) is False:
        return
    json.dump({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": REFUSED,
        }
    }, sys.stdout)


if __name__ == "__main__":
    main()
