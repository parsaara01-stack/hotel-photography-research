# Data dictionary — protocol v0.2

## Evidence files
`evidence.json` and `.csv`: one row per publication. `access_depth` refers to the original extraction: full text or abstract. Later publisher section snippets do not upgrade an extraction to full-text review. Null means unestablished/unextracted, never zero. `source_manifest.json` fingerprints retained source bytes where available; byte hashes do not certify an interpretation. Raw papers remain outside this public repository.

`study_matrix.csv`: one row per identifiable main study, plus explicitly labeled development pilots where extracted. Publication totals are not assigned to individual studies. `reported_finding` is the authors’ report; `appraisal` is this project’s interpretation. Null/unextracted effects are not evidence of null effects. No pooled effect estimate or formal risk-of-bias score is supplied. Independent extraction verification remains pending.

`search_log.json`: actual amendment search queries, platform, date, selected records screened and decisions. It is a targeted search, not an exhaustive database search. Original v0.1 query history is unavailable; no retrospective search counts are invented.

## Demo
Version 2 envelope: `data_kind: demo`, `environment: public_demo`, `protocol_version: 0.2`, `stimulus_version: diagram-v2`, random `session_id`, binary `coverage`, and assigned/completed `events` with elapsed milliseconds. Completion stores six answers and counts `correct`, `incorrect`, `cannot_tell`. No confidence or sales measure in this public mechanics demo. No response transport or persistent browser storage. Optional JSON download is local. Hosting access logs are separate.

## Restricted analysis row (JSONL)
Every row has exactly these fields. Never commit real rows.

| Field | Type / meaning |
|---|---|
| schema_version | Integer 2 |
| data_kind, environment | `observed`, `approved_study` |
| protocol_version, stimulus_version | Exact approved-release match |
| participant_id | Random study ID, 8–80 ASCII letters/digits/underscore/hyphen; never a name/provider ID |
| consent, eligible | True before assignment |
| coverage | Integer 0 = narrower; 1 = broader |
| answers | Six keyed strings or null; explicit `cannot_tell` remains distinct |
| confidence | Optional integer 0–100, represented by null if unanswered |
| coverage_rating | Optional integer 1–7, represented by null if unanswered |
| technical_failure | Boolean; does not exclude a row |

Unknown fields are rejected as a guard against accidental extra columns, not a guarantee of anonymity. There is no `atmosphere`, `booking_intention` or `appeal` main-study field. Six-item incomplete rows are missing for the primary total but contribute observed item categories and itemwise identification bounds.

## Requirement-to-data mapping
| Protocol requirement | Collection field / record | Storage and validation | Reporting |
|---|---|---|---|
| Consent/eligibility | Versioned consent receipt, eligibility outcome; booleans in analysis row | Restricted consent log; must precede assignment | Enrollment flow |
| Randomization | Study ID, coverage, block ID, sequence index, assignment timestamp | Restricted immutable allocation log; reconcile every ID with analysis roster | Assigned counts and deviations |
| Stimulus exposure | Assigned release/hash, render status, viewport, elapsed exposure | Restricted technical log; exact release mapping | Render failures by arm |
| Primary answers | answers[0:6] | Restricted response store; keyed options/null validation | Total and item/category counts |
| Secondary ratings | confidence, coverage_rating | Restricted response store; bounded integer/null | Descriptive N/mean/SD |
| Withdrawal/missingness | Status and permitted retention, completion state, reason code | Restricted audit log; do not collect unnecessary free text | Flow and missingness reasons |
| Duplicate prevention | Provider token/linkage | Separate restricted provider mapping; never analysis ID itself | Adjudication counts |
| Permissions/answerability | File/arm/slot hashes, rights and reviewer records | Restricted originals; publish cleared ledger summary | Stimulus provenance/limitations |

No backend or those private logs exists yet. The analysis loader cannot certify full-roster completeness. Withdrawn response data are retained only as allowed by reviewed consent; preservation of allocation metadata must be explicitly permitted.

## Future release manifest
Status `approved_for_collection`; schema version 2; protocol version 0.2; non-demo stimulus version; real review and preregistration references; frozen assignment ceiling ≥2; six items containing a stable `id`, string `options` (including `cannot_tell`) and factual `correct` key; twelve `stimuli` entries containing `coverage`, `slot` (1–6), relative `path` and SHA-256; six `answerability` entries with item ID and ratings for both arms; all broader-arm entries established. Answerability values: established / contradicted / not_established.

Run analysis with `--stimulus-root` pointing to the approved local files. Path traversal and missing/mismatched files fail validation. A repeated hash is allowed only if it refers to the same file path; repeated slots within an arm are rejected. Real shared images across arms are legitimate controls. These checks cannot substitute for independent review.
