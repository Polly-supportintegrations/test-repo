# Test repo

The repository a team machine runs against to prove a scheduled job works end to end. Nothing in it changes anything: every call either job makes is a read, so it can be pointed at a live Freshdesk and run again as often as it takes.

Its layout is the one `team-repo-template` sets out, so a part proven here behaves the same way in a team's own repository.

## The two jobs

| Job | What one run proves |
|---|---|
| `freshdesk-check` | The schedule fires, the tool server answers, the Freshdesk credential works, and the output reaches the team log. One agent, one line of output, and no report. |
| `chain-check` | A run spawns a supervisor, a supervisor spawns a worker, a worker reaches both an MCP tool and a repository tool, and all three record into one report the manager writes without reading a single group. |

Run either by hand from the `cloud-db/teams` folder of the checkout on the machine, and read the log, before giving it a schedule:

```bash
./run-team-job.sh <team> test-repo chain-check
```

## What chain-check needs before it can report

The four report tools come from the report plan the team wrote for that job, and a job with no plan gets none of them. The plan is `report-plans.json` at the root of the team's folder, beside `cron.json`, and the Build Report tab in the app writes it. For this job it holds three sections, and the role files under `.claude/skills/chain-check/references/` say what goes in each:

| Section | Kind | Columns |
|---|---|---|
| Needs a person | table, leading the report and listed in the app | `group`, `why` |
| Groups read | table, listed in the app | `group`, `name`, `phrases` |
| Phrases seen | bars | |

Without a plan the run still finishes. The manager writes the report as a fenced `json` block at the end of its reply instead, and the app reads it out of the log, which is the other half of the pipeline worth proving.

## Proving the chain refuses what it should

A run writes every refused spawn to `chain-violations.log` in the team's folder, so a clean run leaves that file untouched or absent. To see the hook refuse something, ask a worker in `prompts/chain-check.txt` to spawn a supervisor: the worker holds no spawning tool at all, and a supervisor asked to spawn another supervisor is refused by the hook and named in that file.

## Before scheduling either one

```bash
python3 tools/run_tests.py
```
