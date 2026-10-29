# What Can Room Photos Tell Us?
Parsa Ara · Protocol v0.2 · October 29, 2026

**Draft coverage study. No participants enrolled; no hotel photographs cleared. Not preregistered or approved for collection.** This revision replaces the v0.1 clarity × atmosphere factorial. It is a design revision before participant outcomes, not a change prompted by results.

## Question, contribution and scope
Does broader coverage of decision-relevant features in a hotel-room gallery increase the number of room facts correctly identified, compared with a plausible narrower-coverage gallery of the same room?

The primary estimand is the intention-to-treat effect of assignment to broader versus narrower coverage on a six-item factual-identification count, in the recruited sample for this room and these galleries. It is not a test of photographic professionalism, general comprehension, confidence calibration, sales or revenue. Showing more relevant information may predictably help identification; the practical contribution depends on comparing credible gallery choices and establishing a worthwhile difference before collection. Novelty is not established by the initial literature review.

## Two-arm design
Randomize once, 1:1, to broader or narrower coverage. Hold atmosphere, edit treatment and technical quality constant as production controls; no independent atmosphere claim is planned. Use concealed server-side random blocks of size 4 or 6, chosen randomly with equal probability, and equal allocations within each block. Keep the allocation sequence inaccessible to participants and recruiters. Stop at the frozen assignment ceiling, even if the final block is incomplete. Analyze original assignment.

Both galleries depict the same verified room, with six image slots in the same layout. Match dimensions, compression, loading rules, source label, price, taxes, cancellation policy, factual copy and viewing instructions. Copy must not disclose tested attributes. No people, virtual staging, invented amenities, expanded perspective or altered views. Do not create a deliberately implausible or defective control. The narrower set should be a credible gallery a hotel might choose; the broader set adds views of useful features while retaining the same image count. Preserve capture/edit records and disclose unavoidable differences. The treatment is the gallery package, not an isolated aesthetic property.

Use at least two candidate gallery pairs in development, then freeze one pair before the main study. One room is a deliberate initial scope limitation, not replication across hotels. Additional rooms require a new sampling, analysis and power plan that models stimulus variation.

## Ground truth and visual answerability
Two reviewers independently verify room facts using an authoritative room record or inspection. Separately, they code each item in each gallery as established, contradicted or not established, citing the relevant image/region. Resolve disagreements and record the resolution before release. A fact being true in the room does not mean it is visible in the gallery.

Draft domains are bed configuration, work surface, separate seating, bathing facility, luggage provision and one further useful attribute selected from verified room facts. These are domains, not frozen questions. Do not infer absence of a balcony or amenity from an omitted view. Exclude items whose answers cannot be established unambiguously in the broader gallery. The public drawing uses a visible window as its sixth item, not balcony absence. Final wording must ask about the room fact and offer an explicit “Cannot tell from this gallery.”

## Development and pretest
1. Review candidate pairs with hospitality/photography expertise for realistic gallery choice, useful feature selection and unintended changes. Log reviewer identity privately, decision rationale publicly, and any commercial interest. This independent review has not occurred.
2. Run cognitive interviews/usability testing with a separately reviewed sample to check question interpretation, guessing, uncertainty, task burden and accessibility. This is instrument development, not an efficacy test.
3. Freeze the pretest protocol, sample source, stopping rule, rating items and acceptance criteria before a separate stimulus pretest. Use coverage and realism ratings; inspect appeal and legibility as possible unintended differences. Pretest observations never enter the main study.
4. Size the pretest for its actual precision criterion, not an arbitrary 40–60 people. Illustratively, a two-group 90% interval with SD 1.5 and total N=60 has half-width about 0.64 points. About 98 people only reaches half-width 0.5 at a zero estimated difference; adequate equivalence-test power can require more. These are calculations, not an approved target or acceptance rule. Margins and realism thresholds remain unresolved and block release.
5. Revise if the broader gallery does not establish the intended facts, the control is implausible, or item distributions show unusable floors/ceilings. Log iterations and do not repeatedly test until significance. Predeclare any staged continuation rule. Pilot performance is not a confirmatory effect estimate.

## Population and procedure
Proposed eligibility: adults 18+ who booked a hotel online in the prior 12 months and can use the English instrument. Recruitment geography, source, quotas, compensation and completion-time estimate are unresolved and must be frozen before enrollment. Initial desktop/laptop display ≥1024 CSS pixels is a control that limits mobile generalization. Agree accessible task arrangements before recruitment; do not infer disability from telemetry. The public demo provides equivalent descriptions. The actual experiment must review whether descriptions change the treatment, and use a separately specified accessible study if equivalent treatment cannot be delivered.

Consent and eligibility precede randomization. Present a neutral two-night-stay brief without directional hypotheses. Show the assigned gallery, self-paced, with the gallery available throughout the six questions. Log successful rendering and exposure, not recordings. Collect explicit responses without correctness feedback. Withdrawal is always available and must not be converted into a wrong response.

After the primary items, collect an optional overall confidence rating (0–100) and perceived coverage (1–7). Confidence is descriptive and is not a calibration endpoint. Booking intention, atmosphere, appeal and decision suitability are removed from the main instrument. They are not necessary for this first question. Debrief after all study items. Pretest appeal ratings remain separate from main-study data.

## Outcomes and interpretation
Primary: number of correctly identified room facts, 0–6. A wrong answer or “cannot tell” earns no identified fact, but these are distinct categories and must always be reported separately. This score is not a judgment-quality score: a correct guess can score, and justified uncertainty is not a factual error.

For each arm and each item report correct identification, incorrect assertion, cannot tell and missing counts. For complete records report mean counts of all three response categories. Preserve partial responses. Do not describe “cannot tell” as wrong in feedback, figures or prose. Interpretation must consider whether a gain in correct identification is accompanied by fewer incorrect assertions, fewer uncertain responses, or both. No separate confirmatory tests on those descriptive categories.

Secondary confidence and coverage ratings: descriptive N, mean and dispersion by arm. Never exclude people because their manipulation-check rating conflicts with assignment. No favorable secondary result substitutes for the primary test.

## Sample size and practical relevance
No final recruitment target is approved. First specify the smallest worthwhile difference in correctly identified facts and justify it with the planned use of the findings. Evaluate plausible score variance, ceilings/floors and attrition, then freeze the design calculation before collection.

`python3 analysis/power.py` provides illustrative independent-groups normal-approximation planning only: d=.20 → 786 complete outcomes; d=.30 → 350; d=.40 → 198. At d=.30, assuming SD=1.5 implies 0.45 facts, not an established benefit. A hypothetical 15% loss gives a ceiling of 412 assignments after rounding to an even number. These values are not registration or budget approval. Use a fixed ceiling, do not extend after inspecting effects, and do not claim achieved 80% power if missingness reduces N. The former 352/four-cell target is superseded.

## Analysis and missingness
One row per randomized participant in a restricted roster; no participant rows in this repository. Primary contrast: complete-outcome mean count in broader minus narrower coverage, with standard error sqrt(s²_b/n_b + s²_n/n_n), two-sided normal 95% interval and p value. This is an asymptotic unadjusted estimate; at fewer than 50 complete outcomes in either arm it is diagnostic only. The 50 threshold is a reporting guard, not proof of approximation quality. Review finite-sample operating characteristics for the final bounded instrument before freezing the analysis. No primary covariate adjustment.

The target is all randomized participants. The complete-outcome estimate requires a missingness assumption and is explicitly labeled. Report assigned/complete/missing/technical-failure counts by arm. Partial rows remain incomplete for the primary mean; their observed answers contribute to item summaries and tighten full-roster bounds. Each missing item is bounded by 0 and 1, preserving known correct answers. Assign missing items to minimize/maximize the arm contrast. These are identification bounds for the finite roster, not confidence intervals. No silent imputation or post hoc rescue model.

If either arm has fewer than two complete outcomes or all within-arm variance is zero, do not output a misleading inferential interval or p value; report the contrast descriptively and flag insufficient/degenerate variance. Final analysis review must specify whether a prescheduled randomization-based sensitivity analysis is warranted. The current pipeline does not implement one.

Deduplicate before enrollment through a separately approved provider mechanism; store its identifying linkage separately from the study ID. After randomization retain technical failures and short viewing times. Duplicate IDs fail validation for adjudication against the immutable allocation log. Do not exclude after seeing outcomes. Distinguish withdrawal, noncompletion and technical failure in the private audit log. Where consent requires deletion, remove response contents as specified and retain an allocation-only record only if permitted; otherwise disclose inability to reconstruct the complete roster. Retention duration, withdrawal deadline and access owners must be decided in the consent/privacy plan.

## Release and governance
The release stays `demo_only`. A future collection release must name real approval/review records and a preregistration, identify the frozen sample ceiling, include six keyed questions and twelve actual file-level stimulus hashes mapped to arm and slot, and document answerability. The loader checks the local files against that manifest. Hashes and flags cannot establish provenance, permission or ethics approval; a human review and controlled collection system remain necessary.

Before collection: confirm written rightsholder/property permissions for the intended research/display/edits; finalize independent stimulus and instrument validation; settle recruitment, compensation, consent/debrief, privacy, retention, withdrawal and appropriate ethics determination; audit allocation concealment and complete-roster reconciliation; dry-run the exact study with test-only data; review statistical operating characteristics; preregister and tag the frozen release. See DATA_DICTIONARY.md for the requirement-to-field mapping and READINESS.md for unresolved decisions.

## Evidence and reporting
The six-publication collection is an initial purposive review, not a systematic review, exhaustive search or proof of novelty. A study-level matrix separates experiments and marks unextracted fields. The amendment search log records actual searches from this revision; the original search history was not recorded and is not reconstructed. No pooled effect estimate is justified.

Report the participant flow, deviations, all prespecified outcomes, intervals, missingness bounds and limitations irrespective of direction or significance. Disclose the investigator’s photography-related commercial interest, funding and contributions before collection. Publish deidentified aggregates, protocol versions and analysis code; access to individual responses is a separate governance decision. Preregistration amendments must preserve dates, reasons and which data were already seen.

Method references: [COS preregistration](https://www.cos.io/initiatives/prereg), [stimulus sampling](https://journals.sagepub.com/doi/abs/10.1177/1745691614564879), [W3C image alternatives](https://www.w3.org/WAI/tutorials/images/).
