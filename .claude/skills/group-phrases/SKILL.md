---
name: group-phrases
description: Reads the first four groups Freshdesk lists and records which of four phrases appear in each group's name or description. One run produces one report.
---

This skill might sound very basic. But this is a test skill to determine if the an agent can follow the section specific to the name of its role.

# Group phrases

This skill reads the first four groups that Freshdesk lists. It records which of four phrases appear in each group's name or description. It produces one report.Three roles share that work.

## Shared information

### Terms

- *Group*: Freshdesk's term for an a group of agents a ticket can be assigned to.

### Phrases

`escalation`, `support`, `billing`, `tier`. Those four, spelled that way.

### The roles

- Only 2 total subagents can exist at once.
- Only 1 subagent can be spawned at one time.

| Role | Answerable for |
|---|---|
| manager | opening the run, handing it out, and closing it |
| supervisor | every group in one batch |
| worker | one group |

## Manager instructions
If you are a manger this section is for you. If you are not a manager, ignore this section.

You hand four groups out in two batches, manage batch progress, and close. Closing is where you sign off the full report, and the forms are filled in by the roles below you.

### Your Tools for this skill

`freshdesk_list_groups` takes no arguments and responds with the groups in the workspace.

### Create Batches (Not loop)

1. Call `freshdesk_list_groups`. It takes no arguments and responds with all of the groups in the workspace.
2. Select the first four groups in the response.
3. Call `standalone_report_manager`. Create two batches, each batch with two items. Each item is one group id.

### Spawn Supervisor (loop)

- You can only spawn one supervisor at a time.
- There can only be a total of one supervisor at once.
- This section loops, and here are the conditions to end the loop. To exit the loop and proceed to `close` section, the following must be met.
  - All batches have been taken. All items have `"signed_off":true`.

### Close (Not loop)

After you complete and add your note to the report, *Reply with your own account of the run.*

## Supervisor instructions
If you are a supervisor this section is for you. If you are not a supervisor, ignore this section.

You are responsible for one batch of groups. A worker reads each group, and you check what it recorded against the group itself before you sign it off.

### Your Tools for this skill

`freshdesk_get_group` takes `group_id` and responds with that group's name and description.

### Take Your Batch (Not loop)

Your items are Freshdesk group ids, so the groups your batch names are yours.

### Spawn Worker (loop)

- You can only spawn one worker at a time.
- There can only be a total of one worker at once.
- This section loops, and here are the conditions to end the loop. To exit the loop and proceed to `Check And Sign Off`, the following must be met.
  - Every item in your batch has been taken.

### Check And Sign Off (loop)

The standard an item has to meet:

- No form fields are blank. "none" is not blank.
- Check every form field for a worker's excuse rather than an appropriate value. IF there's an excuse then follow it up.
- Every phrase the form names is one of the four above.

To revise an item that misses the standard:

- Check the item against what `freshdesk_get_group` responds with, rather than against what its worker said about it. Call `freshdesk_get_group` with that same group's id and read its name and description yourself.

This section loops, and here are the conditions to end the loop. To exit the loop and proceed to `Close`, the following must be met.
  - All items have `"signed_off":true`.

### Close (Not loop)

*Reply with your own account of the batch.*

## Worker instructions
If you are a worker this section is for you. If you are not a worker, ignore this section.

You report on one group. You take it yourself with the `batch_id` in the message that started you, so nobody hands you a group.

### Your Tools for this skill

`freshdesk_get_group` takes `group_id` and responds with that group's name and description.

`team_example_step` takes `text` and `phrases`. It responds with which of those phrases the text contains and the character each one starts at.

### Take Your Item (Not loop)

Your item is a Freshdesk group id, so that group is yours.

### Do The Work (Not loop)

1. Call `freshdesk_get_group`, with `group_id` set to your group's id.
2. Call `team_example_step`, with `text` set to the group's name and description run together, and `phrases` set to the four above. If none match, then report "none".

When a tool fails: one of the sections `standalone_report_plan` describes covers work a person has to pick up. Fill in that section, carrying the error the tool gave you.

### Fill In The Form (Not loop)

What belongs in each blank: you have your group's id from the take, and from `freshdesk_get_group` its name and description, and from `team_example_step` which phrases it found and where each one starts.

### Close (Not loop)

*Reply with your `item_id`, the group it stands for, and anything that went wrong while you were filling it in.*

