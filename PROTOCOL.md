# What Does Better Photography Sell?

Parsa Ara · Protocol v0.1 · October 29, 2026

**Stage: literature collection and public mechanics demo. No participant collection has begun. This is a dated protocol draft, not a registered preregistration.**

## Question and estimand

For adults who have booked a hotel online in the previous 12 months, does greater room-information clarity improve factual understanding of one room, independently of photographic atmosphere? The primary estimand is the effect of assignment to high versus low clarity on a six-item room-attribute accuracy score, averaged equally over the two atmosphere conditions. Generalization is initially limited to this room, stimulus set, English-language instrument and sample.

Clarity means coverage and legibility of decision-relevant room features. Atmosphere means aesthetic warmth and experiential appeal. Neither is a synonym for resolution, price, service quality or luxury. We expect clarity to improve accuracy; atmosphere may affect appeal and confidence without improving accuracy. A null result or a failed manipulation remains informative.

## Design and controls

Use a 2 × 2 between-person factorial: lower/higher clarity × neutral/atmospheric treatment. Assign eligible, consented participants once, in concealed randomly permuted blocks of 8 (two assignments per cell). Keep the allocation list server-side in a future collection system. The public demo uses independent browser randomization solely to demonstrate mechanics and cannot enroll participants.

All cells depict the **same verified room at the same property** with the same six image slots, pixel dimensions, ordering, exposure duration rules, room availability, price, taxes, cancellation rules, source label, factual copy, page layout and device requirements. Use six actual photographs per cell, no people, no virtual staging, no added/removed amenities, no simulated window views, no misleading perspective expansion. Keep file quality and loading performance equivalent.

Manipulate clarity through preplanned coverage/cropping: coherent wide views plus legible functional details versus narrower decorative views that leave features ambiguous. Manipulate atmosphere using restrained lighting/color treatment without altering objects, image geometry or feature visibility. This separation is a design goal, not an achieved fact. Reject a set that cannot independently vary these dimensions. In particular, a crop that also changes appeal is a confound unless pretesting resolves it. Hold alt-text descriptions fact-equivalent across atmosphere within clarity; audit that they do not disclose facts absent from a visual condition.

Before confirmatory collection, freeze file hashes, displayed copy, question order, scoring key, allocation algorithm and analysis code in a new version. The SVG in this repository is an interface wireframe and is **not an experimental stimulus**. Public readers can explore all cells; a future participant sees only one and cannot inspect other conditions or the answer key.

## Stimulus and instrument validation (not yet authorized to recruit)

Prepare at least two candidate same-room sets. An independent usability/pretest sample, excluded from the main study, should assess clarity and atmosphere separately after a neutral task. Proposed 40–60-person pretest is a feasibility check, not evidence of treatment efficacy. Evaluate confidence intervals rather than treating a nonsignificant cross-effect as equivalence. Initial practical criterion: intended dimension difference ≥1 point on a 7-point scale; unintended dimension difference contained within ±0.5 points with a 90% interval. If imprecise, extend the pretest under a revised, frozen plan or revise stimuli. Do not tune against the main accuracy outcome. These criteria need review before pretesting.

Have two reviewers independently verify each photographed attribute in the room or against an authoritative property record. Resolve disagreements before freezing the scoring key. Check that each question has one unambiguous correct answer and plausible distractors. Test keyboard and screen-reader task use, loading, mobile/desktop rendering, item ceilings and floors. For the first confirmatory study, standardize to desktop/laptop ≥1024 CSS pixels with successful image loading; audit exclusions this creates. Prepare a separate accessible text-description study if visual presentation cannot be made equivalent for assistive technology users. Never infer disability from telemetry or silently combine different treatments.

## Procedure and outcomes

1. Present neutral consent and eligibility questions (18+, prior online hotel booking in 12 months). No names, email addresses, precise location or account identifiers. Ethics/privacy review and a retention plan precede actual collection.
2. Assign one cell. Show a neutral brief about evaluating room information for a hypothetical two-night stay. Do not tell participants the directional hypotheses. Permit self-paced viewing; log rendered exposure and failures, not screen recordings.
3. Collect all six primary items without correctness feedback, with the gallery still available. Freeze order; do not show manipulation checks first. Items target bed configuration, work surface, separate seating, shower/tub configuration, luggage-storage provision, and balcony presence. Final wordings and keys depend on the actual room. Include “Cannot tell from the information shown.” Score 1 for the correct attribute and 0 for a wrong or “cannot tell” response. Require an explicit answer to each; withdrawal remains available. An unanswered item is missing, never zero.
4. Collect confidence in the overall accuracy of the six answers (0–100), booking intention (1–7), and aesthetic appeal (1–7). Confidence calibration is exploratory: compare mean confidence with percentage accuracy; it is not a validated individual calibration measure. A separate decision-suitability item is exploratory. Do not ask willingness to pay in this first study; a priced hypothetical judgment cannot establish revenue.
5. Ask clarity and atmosphere manipulation checks (1–7), then device/render checks and optional task-difficulty feedback using fixed choices. Debrief. Never exclude participants because a manipulation-check rating disagrees with the intended treatment.

Primary outcome: number of correctly identified attributes, 0–6. Primary test: two-sided clarity main effect, α=.05. Secondary: confidence, appeal and booking intention. Atmosphere main effect and clarity × atmosphere interaction are exploratory unless a later revision powers and preregisters them. Report secondary estimates with intervals and treat multiplicity explicitly; do not promote a favorable secondary result into the primary result. There is no actual booking or revenue endpoint.

## Sample-size plan

Planning assumption: standardized clarity effect d=0.30, two-sided α=.05, 80% power, independent observations. Normal approximation:

`n_per_clarity_level = ceil(2 × (1.959964 + 0.841621)^2 / d²)`.

Round total upward to a multiple of four: **352 complete outcomes, 88 per cell**. This corresponds to 0.45 more correct items if the score SD is 1.5, an unverified planning SD. Sensitivity: d=.20 requires 788 complete outcomes; d=.40 requires 200. With 15% incomplete outcomes, the recruitment planning ceiling is **416 assignments**, rounded to a block of eight. No effect size is estimated from the six literature rows. Run `python3 analysis/power.py` to reproduce this calculation.

Use a fixed assignment ceiling; do not extend after looking at treatment effects. Missingness may leave the study below planned power. Report that limitation rather than asserting 80% achieved power. This plan is not powered for a small interaction or revenue. A 12–20-person usability pilot would check execution only; it would not satisfy this sample target. No pilot or main recruitment has been authorized or started.

## Analysis and missingness

Unit = one eligible, consented randomized participant. Publish only deidentified aggregates. Keep the assignment roster, including dropouts, in a restricted future data store; participant exports never enter this public repository. Preserve original assignment even after display failures. Mark objective technical failure, withdrawal and missing outcomes; report counts by cell. Deduplicate by a nonidentifying study ID; conflicting repeated IDs fail validation rather than being arbitrarily chosen. Do not exclude short viewing times, “cannot tell” answers or unfavorable manipulation checks post hoc.

For each of four cells, report assigned N, complete N, missing N and mean score. The primary contrast gives equal weight to both atmosphere levels: `(mean_C1A0 + mean_C1A1 − mean_C0A0 − mean_C0A1)/2`. Report a heteroskedastic cell-mean standard error, `sqrt(sum(s²_cell/n_cell)/4)`, and an asymptotic 95% interval. This equals the clarity coefficient and HC2 uncertainty from a saturated, centered factorial model. The supplied pipeline labels inference diagnostic if any cell has fewer than 50 complete outcomes; use the prespecified model regardless of significance. No covariate adjustment is primary.

The full-randomized target is intention to treat. A complete-outcome estimate alone requires a missingness assumption and is labeled accordingly. The pipeline also gives conservative full-roster bounds by filling missing scores with 0 or 6 in the directions that minimize/maximize the clarity contrast. Report the bounds and attrition by arm; missing is never assumed to be zero. Technical failures remain in the roster and in those bounds. Consider multiple imputation only in a reviewed future amendment, not as an unannounced rescue analysis.

Current release status is `demo_only`. The analysis loader rejects demo/test/synthetic records, unknown keys, invalid ranges, duplicate IDs and unapproved releases. It requires a reviewed scoring key and a frozen, non-demo stimulus identifier. It does not certify the provenance of manually supplied data; access controls and an audit trail remain necessary.

## Release conditions and exact next needs

- Written permission from the photographer/rightsholder **and** property for public experimental display and the intended research purpose, including derivative treatments. Do not assume a commission, personal possession or portfolio permission covers research reuse.
- Six matched actual room photographs per cell, RAW/edit records where available, factual room specification and two-reviewer scoring key, with file-level SHA-256 hashes and a capture/permission ledger. No third-party photos or private client work until cleared.
- Independent stimulus pretest and usability review; final six questions; a consent/debrief/privacy/retention plan; appropriate ethics determination; a recruitment source and compensation budget approved separately.
- A real collection backend with concealed assignment, consent/eligibility checks, immutable mode flags, withdrawal support and a complete assignment roster. The current Pages site has no response endpoint.
- Final preregistration before any main-study outcomes, followed by a versioned release manifest, sample ceiling and analysis freeze.

## Evidence basis and search limits

The six-row evidence table is a bounded, purposive literature pilot assembled October 29, 2026, not a systematic review or meta-analysis. Searches covered hotel photography, photo appeal, information value, booking intention and eye tracking; priority went to publishers and university repositories. Included primary empirical studies with direct relevance; excluded marketing multipliers, unsourced conversion claims, image-recognition-only datasets and literature-only articles. Access levels and missing sample sizes are explicit. No participant microdata, booking records or property revenue were acquired. See `data/evidence.csv`, `data/source_manifest.json` and `DATA_DICTIONARY.md`.
