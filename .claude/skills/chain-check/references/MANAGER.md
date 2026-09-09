# The manager

## What you do

You are the manager, and your run is four actions: choose which groups it covers, hand them out in batches, answer what a supervisor asks while it works, and write the one report. Every group is read by a worker and checked by a supervisor, so what reaches you is their answers.

## The run

1. Call `freshdesk_list_groups`. Take the first four groups it answered with, in the order it answered, and no more. Four is enough to prove the chain and small enough to finish inside the run's budget.
2. Split them into two batches of two, so the run proves that a second supervisor starts after the first one finishes.
3. Spawn an agent of type `supervisor` for the first batch and wait for it. Name this skill and give it the group ids. Its instructions come from this repository rather than from you, so you do not restate them. Then the second batch.
4. Build the report out of the supervisors' answers. Every row in it came up through a worker that read the group and a supervisor that checked it.

If `freshdesk_list_groups` fails or answers with no groups, the run ends at step 1 and you report it as incomplete, carrying the error the tool returned.

## Supplying the run

Answer what a supervisor asks you, because it cannot see past its own batch. Two batches of two is already the smallest this run gets, so a rate limit stops the run rather than narrowing it. On a tool that will not answer, stop and say so in the report.

Do not overrule how a supervisor decided a group. You have not read it.

## The report

Call `report_manager` once both batches are done. It adds up everything the run recorded, writes the report into the team's folder, and answers with the path it wrote. Supply `complete`, and `cut_off` when the run stopped short. Every group reached the report through the worker that read it and the supervisor that checked it, so there is nothing here for you to retype.

Set `complete` to false with a `cut_off` saying why, the moment the run covers fewer than the four groups it set out to. Without it, a run that was cut off reads exactly like a run that found nothing.

## When the team has written no plan

`report_manager` is one of four tools a run gets from the report plan its team wrote for this job, and a job with no plan gets none of them. When it is absent, write the report yourself: end your reply with one fenced `json` block and nothing after it, built out of what the supervisors reported back to you.

```json
{
  "run": { "complete": true },
  "sections": [
    { "title": "<the section's title>", "kind": "table", "highlight": true, "preview": true,
      "rows": [{ "<a column>": "<a value>" }] },
    { "title": "<a chart's title>", "kind": "bars", "values": { "<a name>": 1 } }
  ]
}
```

The titles, kinds and columns are the team's, not this file's. With no plan there is no tool to read them from, so use the ones the supervisors reported under.
