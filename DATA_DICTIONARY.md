# Data dictionary and collection log

## Literature evidence

One row per primary publication, not one row per experiment or participant. Collection date: October 29, 2026; exact UTC retrieval timestamp in each row. Search is a purposive pilot and may omit eligible studies. We did not pool effect sizes across incompatible outcomes.

| Field | Meaning |
|---|---|
| id | Stable project citation key |
| title, authors | Verified publication identity |
| issue_year, first_online_date | Issue year and online/in-press date, kept separate |
| doi | DOI; null means no DOI established, not a missing publication |
| url | Primary publisher or university repository link |
| access_depth | `full_text` or `abstract`; never infer full-text review from a metadata page |
| design | Design as described in accessed material |
| sample_n, sample_unit | Reported N with its unit; null = not stated in accessed material, not zero |
| outcome_type | `stated_wtp`, `booking_intention`, `booking_proxy`, or `visual_attention` |
| extraction, limitations | Concise interpretation and limits of that source |
| source_locator | Section/page supporting the extraction |
| retrieved_at_utc | ISO 8601 access timestamp |
| measurement_window | Publication-specific time scope; see extraction rather than assume comparable periods |
| missingness | Explicit limits of accessible sampling/missing-data information |
| capture | Local raw capture filename if available; copyrighted raw files stay outside the public repo |

`source_manifest.json` records hashes for locally captured HTML/PDF bytes. These are access-time fingerprints, not a claim that a changing publisher page will reproduce byte-for-byte. Some sources were readable through web extraction but blocked direct byte retrieval; their hash/capture fields are intentionally null. Cornell full text was fetched from the repository's bitstream API after the browser endpoint rate-limited. Shin remained restricted; Bufquin’s repository explicitly provides no downloadable document. Marder’s accepted manuscript was read through web PDF extraction, then captured from the University of Edinburgh alternate endpoint after the Southampton direct download returned 403; its exact capture URL is recorded. Feess metadata/abstract was fetched directly; no full paper or purchase was made.

## Image/rights inventory

`image_inventory.json`: `id`, `asset` (relative path or null), `kind`, `rights_status`, `use`, `same_room_verified`, `permission_evidence`, `research_ready`, `reviewed_at_utc`.

Real hotel photographs cleared for research: **0**. The original SVG is a fictional room drawing for interface demonstration. A focused filename/path search in existing Codex workspaces for hotel/hospitality/resort media found no qualifying matches. Other interior/client media are not presumed reusable. A later depth-two directory-name search across mounted external volumes identified two hospitality directory leads, with no still-image files discovered in those candidate trees. External disks were not exhaustively searched; Dropbox was not searched. The inventory records the scope of this limited search, not a claim that Parsa owns no hotel images. No client imagery or private file paths are published.

## Demo event envelope

Downloaded JSON contains `schema_version: 1`, `data_kind: "demo"`, `environment: "public_demo"`, `protocol_version: "0.1"`, `stimulus_version: "diagram-v1"`, random `session_id`, `condition` (clarity/atmosphere binary), and ordered `events`. Each event has `event`, `elapsed_ms`, and `payload`. Allowed event names: `assigned`, `completed`. Completion payload: six explicit answers, confidence 0–100, and the demo correctness count. The diagram’s key is public and irrelevant to a real experiment. No event is sent anywhere, persisted in browser storage, or counted as research. Ordinary GitHub hosting access logs are outside the demo’s control. Export is a local file initiated by the visitor.

## Future restricted analysis input

One JSON object per line, including assigned participants with no outcome. Exact keys:

| Field | Type / values |
|---|---|
| schema_version | integer 1 |
| data_kind | exactly `observed`; demo/synthetic/test always rejected |
| environment | exactly `approved_study` |
| protocol_version | matches release manifest |
| stimulus_version | matches non-demo frozen release |
| participant_id | nonidentifying study ID, 8–80 ASCII letters/digits/hyphen/underscore |
| consent, eligible | boolean true; assessed before randomization |
| clarity, atmosphere | integer 0 or 1 |
| answers | six strings from each release-keyed item’s allowed options, or null for an unanswered item |
| confidence | integer 0–100 or null |
| booking_intention, appeal | integer 1–7 or null |
| technical_failure | boolean; retained, not an exclusion |

Missing a required field is an error; explicit null is missing. Unknown fields are rejected to prevent accidental inclusion of names/emails/free text. Full-roster completeness still depends on collection-system audit. A manually edited `observed` flag is not proof of actual data. Keep these files outside Git, with a separately approved retention policy.

`data/release.json` currently disallows observed analysis. A future reviewed release must set `status: "approved_for_collection"`, replace the demo stimulus ID, include six item objects (`options`, `correct`) and freeze hashes in `stimulus_sha256`. Approval is an actual governance step, not achieved by changing a string in this file. Test fixtures are labeled synthetic and are only exercised through test-only functions.
