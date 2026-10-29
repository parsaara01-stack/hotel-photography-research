# What Does Better Photography Sell?

Research by **Parsa Ara** · Protocol v0.1 · October 29, 2026

A static research website, six-publication literature evidence pilot, image/rights inventory, randomized task wireframe and reproducible future analysis. **No participant experiment has been conducted.** The public site has no response-submission endpoint.

## Run locally

Python 3.9+; no pip install, Node build, account, tracking service or API key required.

```sh
python3 scripts/serve.py
```

Open `http://127.0.0.1:8769`. If that port is in use, `python3 scripts/serve.py --port 8770`. The server builds and verifies the static files before serving them. The finished `docs/` folder is deployed by the GitHub Actions workflow from `main`, using only `docs/` as the public artifact.

```sh
python3 scripts/verify.py
python3 analysis/power.py
```

The first command builds the evidence bundle, checks integrity/links/privacy gates, and runs nine analysis tests. The second reproduces planning assumptions for sample size; it does not analyze participant results.

## Contents and actual collection

- `data/evidence.csv` / `.json`: six source-linked primary publications, three full text and three abstract only. Null sample sizes mean not stated in accessed material, never zero.
- `data/source_manifest.json`: exact retrieval timestamps, access depth, locators and access-time byte hashes when direct capture succeeded. Raw copyrighted source files are not redistributed.
- `data/image_inventory.json`: original fictional SVG, plus the unmet real-photo requirement. Zero hotel photographs are cleared for experimental use.
- `PROTOCOL.md`: factorial design, primary outcome, sample-size assumptions, stimulus controls, missingness, exclusions and release conditions.
- `DATA_DICTIONARY.md`: data fields, limited search scope, local demo event schema and future restricted input schema.
- `docs/`: accessible static site using local assets and system fonts. Filter evidence, inspect conditions, answer six fictional-room questions and optionally export demo JSON locally.
- `analysis/`: Python code for planning and a future local-only analysis with scoring validation, equal-weight cell contrasts, uncertainty, missingness counts and full-roster bounds.
- `tests/`: fabricated, in-memory unit-test structures. They are test execution artifacts, never research records.
- `.github/workflows/pages.yml`: deterministic build and analysis checks on `main` and pull requests.

## Evidence limits

The new Feess/Rosato/Schilling lead is verified against the publisher’s October 27, 2026 metadata and abstract (DOI 10.1628/jite-2026-0030); its full text has not been obtained. Do not interpret its willingness-to-pay contrast as a nightly rate or revenue return. Other reviewed sources distinguish visual attention, stated booking intention, and a hotel-level booking-badge proxy. They do not establish this project’s accuracy effect. This is a purposive literature pilot, not a systematic review or pooled causal estimate.

No private client photographs, participant records, identifiable responses or source-paper PDFs are in the public repository. Original room illustrations are explicitly fictional. No AI-generated evidence photos are used. Public visibility of a photograph elsewhere is not evidence of research reuse rights.

## Future analysis is deliberately gated

```sh
python3 analysis/analyze.py /restricted/assignment-roster.jsonl --release /reviewed/release.json
```

This refuses to run with the committed `data/release.json`, whose status is `demo_only`. A future reviewed release needs 24 frozen photograph hashes, six item keys and a non-demo stimulus version. The loader separately rejects `demo`, `synthetic` and `test` records, unknown fields, out-of-range scores, duplicate IDs and release mismatches. Demo exports cannot be converted into research by renaming the file. Provenance and collection-system access controls still need independent review.

Report one roster row per randomized participant, including dropouts and technical failures. An unanswered item is null. A selected “cannot tell” scores zero against the room fact. Missing outcomes receive sensitivity bounds, not assumed zeros. The primary estimator averages the clarity contrast equally across atmosphere; secondary means are descriptive. No revenue model is provided.

## Publishing and next data

Repository: `parsaara01-stack/hotel-photography-research`. See `PROGRESS.md` and `DEPLOYMENT.json` for observed remote/CI/Pages status rather than inferred URLs. Remote repository creation and Pages configuration require authenticated access; all published content is suitable for this requested public deliverable.

The next inputs are written rightsholder/property permission, same-room photographs and verified room facts, a stimulus pretest, reviewed consent/privacy/ethics/recruitment arrangements, a real collection backend and preregistration. No recruitment, client contact, purchase or change to Adobe Portfolio has been made.

Third-party studies and their images retain their original rights. Source links provide attribution; the repository distributes our concise evidence extraction, code and original diagram only. No general license to client imagery is implied.
