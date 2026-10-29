# What Can Room Photos Tell Us?
Parsa Ara · Protocol v0.2 · October 29, 2026

An initial literature review and proposed two-arm study of room-photo coverage and factual identification. **No participant study has been conducted. No hotel photographs are cleared.** The public site is an interface demonstration, not an enrollment portal.

Live site: https://parsaara01-stack.github.io/hotel-photography-research/

## Run and verify
Python 3.9+; no third-party dependencies required.
```sh
python3 scripts/serve.py
python3 scripts/verify.py
python3 analysis/power.py
```
Open http://127.0.0.1:8769 (or use `--port 8770`). Verification checks build consistency, local references, declared data structure and analysis edge cases. It is not scientific, privacy or accessibility certification.

## Research materials
- PROTOCOL.md: question, two-arm design, response categories, missingness and reporting.
- READINESS.md: unresolved decisions that block collection.
- DATA_DICTIONARY.md: evidence schema and protocol-to-data mapping.
- data/evidence.csv: six primary publications; original extractions include three full texts and three abstracts.
- data/study_matrix.csv: study-level extraction with explicit unextracted values and appraisal.
- data/search_log.json: actual targeted amendment searches; no invented reconstruction of the original search.
- data/source_manifest.json: source locators and access-time hashes where available.
- data/image_inventory.json: fictional drawing and unmet photograph/rights requirements.
- analysis/: draft two-arm pipeline; current release blocks observed analysis.

## What changed
The v0.2 audit revision narrows the title and estimand, removes the atmosphere factor and main-study intention/appeal items, separates wrong assertions from “cannot tell,” replaces balcony absence in the drawing task, and moves technical materials out of the main reading path. The 352/four-cell target is superseded by illustrative two-arm planning, not a finalized recruitment target. See CHANGELOG.md.

## Future analysis
```sh
python3 analysis/analyze.py /restricted/roster.jsonl --release /reviewed/release.json --stimulus-root /reviewed/stimuli
```
The current `demo_only` release refuses this. A future release must map twelve actual stimulus files to arm and slot, verify their bytes, freeze six items and answerability, and reference actual review and preregistration records. Flags/hashes do not prove consent, rights or provenance. No participant data belong in Git.

The initial literature review does not establish novelty, a pooled effect or sales impact. Third-party papers and images retain their rights. Source links are attribution, not permission to reuse images. Client media, participant responses and paper PDFs are not distributed. No recruitment, external outreach or purchase has occurred.
