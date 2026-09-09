"""One deterministic step, as a tool the skill can call instead of judging it itself.

A tool answers what IS, never what it means. This one reports which of the team's known
phrases a piece of text contains, and where. What a match means stays in the skill, because
that is the part a list cannot hold.
"""

import json
import sys


def example_step(text, phrases):
    """Which phrases the text contains, and the character each one starts at."""
    low = (text or "").lower()
    found = []
    for phrase in phrases or []:
        at = low.find(phrase.lower())
        if at >= 0:
            found.append({"phrase": phrase, "at": at})
    return {"found": found, "count": len(found)}


def _run(args):
    return example_step(args.get("text", ""), args.get("phrases", []))


if __name__ == "__main__":
    print(json.dumps(_run(json.load(sys.stdin) if not sys.stdin.isatty() else {})))
