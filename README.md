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

## What `.claude/settings.json` decides

Four environment settings and one hook, all per repository, so a team changes its own runs without anyone touching the machine.

The prompt cache is an hour because these jobs repeat inside one and the cached prefix is the same every run, so the next run reads what the last one wrote. The concurrency cap is 2, and it counts the agents a run starts rather than the session that starts them, so it is one supervisor with its worker while the manager waits.

`CLAUDE_CODE_EXTRA_BODY` is the one that will not be obvious to whoever finds it. Its value is JSON merged into every API request, spread last, which is how it overrides `tool_choice`, and what it sets there is `disable_parallel_tool_use`. That holds every agent to one tool call per turn.

It is there because the tool calls in one turn all run at once. A manager that writes two spawn calls into one message starts two supervisors, which fills the concurrency cap, and the next spawn is refused with an error that tells the model not to retry. A supervisor refused its worker ends having done nothing, and the run comes back a batch short. No instruction reaches this, because the turn is already written by the time the calls are made, and nothing else in Claude Code does: a definition's `background` field only forces background on, having no meaning when false, and there is no per-turn setting. `CLAUDE_CODE_EXTRA_BODY` is the only way in, and `disable_parallel_tool_use` is an Anthropic API field rather than a Claude Code one, so it is reached through that door rather than a supported switch.

To see whether it still works, group a run's `Agent` calls by the `id` of the assistant message that holds them, in the session transcript under `~/.claude/projects`. One call per id is it working. Two under one id is it gone.

The hook beside it, `.claude/hooks/foreground-spawns.py`, refuses any spawn that does not carry `run_in_background` set to false, for the same reason: an agent whose spawn does not wait replies and ends before its own worker comes back.

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
