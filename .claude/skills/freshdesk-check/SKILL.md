---
name: freshdesk-check
description: Read one item out of Freshdesk and print a single line saying what came back. Use to confirm that a scheduled run reaches Freshdesk and that its output lands in the team log.
---

# Freshdesk check

Proves the whole path in one run: the schedule fires, the tool server answers, the
Freshdesk credential works, and the output reaches the team log.

## Steps

1. Call `freshdesk_list_groups`.
2. Take the first group it returned and call `freshdesk_get_group` with that group's id.
3. Print one line and nothing else:

```
freshdesk-check ok: N groups, first is <id> <name>
```

If either call fails, print one line instead, carrying the error the tool returned:

```
freshdesk-check failed: <error>
```

## Rules

- Read only. Neither call writes anything.
- Report the tool's own error rather than a description of it. A failure that reads as a
  success is the one outcome this check must never produce.
- One line, and no Training Block. Whoever opens the log is reading for the word ok.
