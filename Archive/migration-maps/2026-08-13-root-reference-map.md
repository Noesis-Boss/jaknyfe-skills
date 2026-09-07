# Root migration reference map — 2026-08-13

Scope: loose files at `/home/workspace` root. No files moved by this map.

## Safe to map next

| Cluster | Root entries | Proposed destination | Gate |
|---|---|---|---|
| Scholarship pipeline | `batch_*.json`, `*_candidates*.json`, `*_scholarships*.json`, `discover*.py`, `discovery*.py`, `build_*.py`, `compile_candidates.py`, `gather_scholarships.py`, `gen_*.py`, `insert_*.py`, `quick_discover.py`, `run_discovery.py`, `verify_batch.py`, related cleanup files | `Research/scholarships/` | Confirm no cron/automation invokes root paths; preserve active database inputs and logs until the automation is tested from the new path. |
| Novel/research documents | `Chapter12-Know-Where-the-Brain-Stops-Research.md`, `49 Psychological Mind Tricks Breakdown.rtf`, `memorization-*.md`, `manuscript.md`, `story-arcs.json` | Relevant book/research folders | Match each file to a project before moving; do not infer from filename alone. |
| Email exports | `gmail-*` groups | `Documents/email-exports/` | Move complete basename groups together (`.eml`, `.html`, `.md`, `.txt`); check no scripts reference root paths. |
| Generated logs | `HealthCheck.log`, `cron_test.log`, `heartbeat*.log`, `moltbook*.log`, `status_logs.log`, `system-health.log`, `*.tmp`, `nohup.out` | `Archive/logs/` | Confirm no live process expects the root filename; exclude large active logs from the first move. |

## Hold — requires individual project maps

- Deployment and service scripts: `deploy_*.sh`, `fix_paperclip.sh`, `get-docker.sh`, `start-pg-restored.sh`, `heartbeat.sh`, `void_daily.sh`, `run_*.sh`, `kilo_hermes.sh`, `maximize_points.sh`.
- Databases and data stores: `*.db`, `memory.json`, `scholars`, `scholarsearch-noesis`, and unnamed files that may be process inputs.
- Certificates, environment files, tokens, and runtime state: `.env*`, `cert.pem`, `token.txt`, `supervisord.pid`, marker files.
- HTML/JS and images: inspect ownership and live references before moving; some are source/reference assets.
- Duplicate or truncated-looking project directories/files: `Bound-by-Ash-*`, `scottish*`, `scholar`, and similar names.

## Verification protocol before each move

1. `git ls-files --error-unmatch <path>` — tracked status.
2. `rg -n --hidden -g '!Trash/**' -g '!.git/**' '<exact basename>|<root path>' /home/workspace` — references.
3. Inspect cron, service, automation, and script invocations for root-path dependencies.
4. Move only a complete, homogeneous cluster to its destination.
5. Re-run the reference search, verify old paths are absent, and run the affected smoke test.
6. Record the result here and in the relevant project `AGENTS.md`.

## Current decision

The scholarship pipeline is **not safe to move as a root batch**. `run_discovery.py`, `quick_candidates.json`, and several root scripts are referenced by one another, while the canonical skill and project scripts use fixed paths under `scholarsearch/`, `scholarsearch-site/`, and `Skills/scholarship-discovery/`. The project has an active automation and a documented verification issue, so root scripts/data remain in place until each script is classified as obsolete, archival, or still runnable.

Evidence checked:

- `Skills/scholarship-discovery/AGENTS.md` identifies the canonical runner and live databases.
- Root `run_discovery.py` reads root `quick_candidates.json` and writes to live scholarship databases.
- Root `batch_insert.py`, `build_candidates.py`, `build_scholarship_batch.py`, `gather_scholarships.py`, `quick_discover.py`, and `verify_batch.py` reference live databases or root JSON inputs.
- No cron entry was found in the checked cron locations for these root filenames.

Next safe action: create a script-level classification table for the scholarship cluster; do not move it yet.

## Script-level classification — 2026-08-13 continuation

| Root entry | Classification | Evidence / migration decision |
|---|---|---|
| `run_discovery.py`, `quick_discover.py`, `gather_scholarships.py` | live/possibly live | Open the root `quick_candidates.json` and write to both live databases. Leave in place until the active automation is proven independent of them. |
| `batch_insert.py`, `build_candidates.py`, `build_scholarship_batch.py`, `build_scholarship_json.py`, `discover200.py`, `discover_batch2.py`, `gen_batch2.py`, `insert_batch.py`, `insert_scholarships.py`, `verify_batch.py` | operational/historical | Directly reference the live databases; some are batch builders or maintenance tools. Do not move as a group. Archive only after checking no unfinished batch or operator run depends on each file. |
| `discover_scholarships.py` | historical/possibly reusable | Uses root `scholarship_candidates.json`, but points at the canonical skill directory for support code. Preserve until its replacement status is documented. |
| `discover_web.py` | historical | Writes root `discovered_scholarships.json`; no canonical automation reference found. Keep until output is confirmed disposable, then move script and output together. |
| `compact_discover.py` | historical | Writes root `quick_candidates.json`, which is still consumed by root scripts. Keep with that input until the dependent scripts are retired or relocated together. |
| `compile_candidates.py`, `discovery.py`, `discovery_clean.py`, `gen_scholarships_json.py` | historical/unknown | No live-database marker or canonical automation reference found in the script scan. Inspect source/output provenance before archival; no move yet. |
| `moltbook_karma_bot.py` | unrelated active script | Tracked and unrelated to scholarship migration. Exclude. |

### Result

No scholarship script is independently safe to move in this batch. The smallest safe future batch is a fully retired producer plus every exact root input/output it owns, after a final reference scan and a no-active-run check. The canonical skill remains the only approved recurring runner.

### Root JSON reference results

- Referenced and held: `quick_candidates.json`, `scholarship_batch.json`, `scholarship_candidates.json`, `discovered_scholarships.json`.
- Unreferenced by local scripts, but not yet safe to move without content/mtime review: `batch_candidates.json`, `comprehensive_candidates.json`, `final_2.json`, `final_scholarships.json`, `scholarship_additional.json`, `scholarship_batch2.json`, `scholarship_candidates_200.json`, `scholarship_candidates_batch2.json`, `scholarship_input_final.json`, `today_candidates.json`.
- Decision: no JSON moved. “Unreferenced” proves only that the current local script scan found no consumer; it does not prove the files are disposable or not needed for a pending manual run.

## Scholarship cluster classification queue

| Root entry pattern | Initial classification | Required proof |
|---|---|---|
| `run_discovery.py`, `batch_insert.py`, `build_candidates.py`, `build_scholarship_batch.py`, `gather_scholarships.py`, `quick_discover.py`, `verify_batch.py` | live/possibly live | Run `--help` or inspect entrypoints; trace all inputs/outputs; preserve until replacement is confirmed. |
| `discover*.py`, `discovery*.py`, `gen_*.py`, `compile_candidates.py`, `insert_*.py`, `compact_discover.py` | historical or live unknown | Search references and timestamps; compare behavior with `Skills/scholarship-discovery/scripts/discover.py`. |
| `batch_*.json`, `*_candidates*.json`, `*_scholarships*.json`, `discovered_scholarships.json`, `final_*.json`, `quick_candidates.json`, `today_candidates.json` | generated data | Check whether any current script opens the exact basename; retain source inputs and archive only confirmed outputs. |
| `cleanup_*.txt`, `*_delete_ids.txt`, `nuke_ids.txt`, `missing_events.tsv` | operational data | Never move until confirming whether an unfinished cleanup depends on it. |
| `scholarship_verify.log` | active log | Leave in place while the recurring link checker runs; archive only after log destination is explicitly changed. |

## Unreferenced JSON review — 2026-08-13 continuation

Reviewed and archived as one homogeneous generated-data batch:

`batch_candidates.json`, `comprehensive_candidates.json`, `final_2.json`, `final_scholarships.json`, `scholarship_additional.json`, `scholarship_batch2.json`, `scholarship_candidates_200.json`, `scholarship_candidates_batch2.json`, `scholarship_input_final.json`, and `today_candidates.json`.

Evidence: all 10 files were untracked; their mtimes were 2026-07-24 through 2026-07-26; each contained generated scholarship candidate data (one was an empty array); and an exact-basename reference scan across `/home/workspace` excluding `.git`, `Trash`, `node_modules`, `Media`, and `Archive` returned no matches. The canonical recurring runner remains `Skills/scholarship-discovery/scripts/discover.py`, which does not reference these files.

Destination: `Archive/scholarship-candidates/2026-08-13/`.

Post-move verification: all 10 old root paths are absent; the archived files exist at the destination; no live script or canonical automation reference was introduced. Remaining scholarship files are still held: referenced JSON inputs/outputs, root scripts with live-database dependencies, cleanup inputs, and the active verification log.
