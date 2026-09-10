# Test repo

The repository a team machine runs a scheduled job against, to see the whole path work end to end. Every call a run makes is a read, so it can be pointed at a live Freshdesk and run as often as it takes.

Its layout is the one `team-repo-template` sets out, so a part that works here behaves the same way in a team's own repository.

## The skill

A repository holds one skill, and a job is named for it. `group-phrases` covers the first four groups Freshdesk lists. A worker reads one of them and records which of four phrases its name or description contains. A supervisor checks each group in its batch against Freshdesk and signs it off. The manager opens the run, hands it out in two batches, and signs off the report the tool writes.

Run it by hand from the `cloud-db/teams` folder of the checkout on the machine, and read the log, before giving it a schedule:

```bash
./run-team-job.sh <team> test-repo group-phrases
```

The runner passes `.claude/agents/manager.md` as the prompt, so a run starts as the manager. The log ends with a table naming every agent the run started, how long each ran, how many times each called the model, and which tools each reached.

## Where everything lives

| File | Holds |
|---|---|
| `.claude/agents/manager.md` | the manager's whole instructions, and the prompt a run starts from |
| `.claude/agents/supervisor.md` | the supervisor's |
| `.claude/agents/worker.md` | the worker's |
| `.claude/skills/group-phrases/SKILL.md` | the terms all three share |
| `polly-tools.json` | the steps this repository declares, each reaching a run as `team_<name>` |

Nothing in a run can read `.claude/agents`, so each role arrives holding its own file and reads none of the others.

## What a run needs before it can report

Its report tools come from the report plan the team wrote for this skill, and a run with no plan gets none of them. The plan is `report-plans.json` at the root of the team's folder, beside `cron.json`, and the Build Report tab in the app writes it. This skill's plan holds three sections:

| Section | Kind | Columns |
|---|---|---|
| Needs a person | table, leading the report and listed in the app | `group`, `why` |
| Groups read | table, listed in the app | `group`, `name`, `phrases` |
| Phrases seen | bars | |

The agent definitions say what each role puts in them.

## The chain of command

A run refuses any spawn outside the chain, and any read of `.claude/agents`, and writes each refusal to `chain-violations.log` in the team's folder. A clean run leaves that file absent.

## Before scheduling it

```bash
python3 tools/run_tests.py
```
