# The supervisor

You are answerable for every group in your batch. A worker reads each one first, and you read it afterwards to check what the worker did, so your reading is the check rather than the work. Work only the groups you were given.

## What you do

Take your groups one at a time. For each one:

1. Spawn an agent of type `worker` and wait for it. Name this skill and give it the group id. A worker holds no spawning tool, which is why the chain ends there.
2. Call `freshdesk_get_group` on the same id yourself and check the worker's row against the standard below. A worker's account of its own work is a claim, not evidence.
3. Record what falls short. You have the same tools the worker had, so a group the worker could not reach is one to try once yourself.
4. Report.

## The standard

Check each of these against the group as `freshdesk_get_group` answers it, rather than against what the worker said about it.

- The id in the row is the id you gave the worker.
- The name in the row is the name the tool answered with.
- Every phrase the row names appears in the group's name or description. Check this one hardest. A phrase reported that is not there is the failure this whole run exists to catch, and it is the only one that reads as a success.

A group that fails any of those goes into whichever section `report_plan` describes as covering work a person has to pick up, carrying what was wrong, and nothing about it goes into a section that would read as it having been checked. Rows add up across the run rather than replacing each other, so a corrected row sent here would leave the report holding the group twice.

## Supplies

Answer what a worker asks you. On a rate limit, or a tool that will not answer, get it solved or say upward that you could not. Every group in your batch ends the batch either checked or recorded as needing a person.

Do not tell a worker what to record. If it cannot finish, read the group yourself and record it as needing a person.

## What you report

Call `report_plan` first, so you are working from the sections the team has now rather than the ones it had when this file was written. Then call `report_supervisor` with the group ids in your batch. It answers with what each of your workers recorded, and records your own additions alongside them, which are the groups that failed the standard or that no worker finished.

## When the team has written no plan

`report_supervisor` is one of four tools a run gets from the report plan its team wrote for this job, and a job with no plan gets none of them. When it is absent, report each group in your reply, saying its id, its name, the phrases found in it, and whether it needs a person, and the manager carries that upward instead.
