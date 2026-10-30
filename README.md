# OTAZ III — The Gibbs Ledger

A standalone mathematical study of one operator: a temperature-scaled softmax over
scores, normalising a weighted mean of values, carried alongside the scaled
log-partition sum. The paper proves what that pair does algebraically, what a
distributed implementation must carry in order to merge exactly, what the merge
costs when it carries too little, and what can be certified when the weights are
estimated rather than known.

* Manuscript, single column, A4:
  `publication/OTAZ_III_Gibbs_Ledger_EN.pdf` (34 pages)
* Manuscript, IEEE-style two column:
  `publication/OTAZ_III_Gibbs_Ledger_EN_IEEE_layout.pdf` (20 pages)
* Cover card: `publication/OTAZ_III_Cover.png` / `.svg`
* Post card, black and white: `publication/OTAZ_III_Social_Card.png` (1200 × 1200)
  and the wide variant `OTAZ_III_Social_Card_wide.png` (1200 × 627)
* The English post text, with the link slot and the posting checklist:
  `publication/OTAZ_III_LinkedIn_Post.md`
* The step-by-step publishing guide, Arabic, with the file names to upload on each
  platform and the option to pick in every field: `docs/OTAZ_III_Publishing_Guide_AR.pdf`
* The whole deposit as one archive: **`OTAZ_III.zip`**, built by
  `python scripts/otaz_build_master_zip.py` (91 files under a single `OTAZ_III/`
  folder plus a `MANIFEST.txt`)
* Novelty assessment, one page, Arabic: `publication/OTAZ_III_Novelty_Assessment_AR.pdf`
  (source `publication/OTAZ_III_Novelty_Assessment_AR.html`)
* Author: **Al-Mu'taz Billah Salah Al-Dawoodiya** — software developer,
  artificial intelligence and computer science — `mohtazaldawdeh@gmail.com`
* Companion report (different object, cited where it applies):
  [10.5281/zenodo.23648070](https://doi.org/10.5281/zenodo.23648070)

> **Status.** Preprint. Not peer reviewed, not submitted, no acceptance claimed.
> No quantum-computational-advantage claim is made anywhere in this work.

## The title in full

*OTAZ III: The Gibbs Ledger — Exact Aggregation, a Sharp Impossibility Theorem,
and Certified Error Budgets for Scored-Record Fusion.*

## What the paper proves

| Result | Statement | Evidence |
|---|---|---|
| Thm 1 | the ledger is a commutative monoid; the merge is exact in any tree | `e13_binary_algebra.json`, `e16_tree_merge.json` |
| Thm 1(iii) | a duplicated record adds exactly `β⁻¹ ln 2` to the score | `e13_binary_algebra.json` |
| Lemma 1 | the operation is not bilinear; the defect is 2.1932 at `λ = 2` | `e13_binary_algebra.json` |
| Thm 3 | **with value-only summaries the reachable set is the convex hull** | `e12_impossibility.json` |
| Thm 4 | **the minimax merge rule is the midpoint; its worst case is half the range, and is attained** | `e12_impossibility.json` |
| Thm 5 | **a ledger quantised to relative precision `δ` merges to `Dδ/(1−δ)`, for any number of shards** | `e15_quantisation.json` |
| Thm 6 | temperature calculus: `dV/dβ = Cov_p(v,w)`, `d²lnZ/dβ² = Var_p(w)`, `d³lnZ/dβ³ = κ₃(w)` | `e2_temperature_calculus.json`, `e14_worked_example.json` |
| Thm 7 | coarse-graining gap `= β⁻¹ H(π) ≤ β⁻¹ ln k`, sharp at equal masses | `e3_coarse_graining.json` |
| Thm 8 | the gap obeys a Shannon chain rule across pipeline levels | `e4_hierarchy.json` |
| Thm 9 | the logit parametrisation does not amplify an `L1` error: `TV ≤ ε/(1−ε)` | `e9_nonamplification.json` |
| Thm 10 | sampling and truncation compose into `D·min(1, τ̂ + ε/(1−ε))` | `e10_pipeline.json` |
| Thm 11, Cor. 1 | dephasing contracts trace distance; a Helstrom floor follows | `e11_dephasing.json`, `e6_helstrom.json` |
| Thm 12 | no converse: two orthogonal states with identical diagonals | `e5_quantum_boundary.json` |

## What the paper does not claim

No priority over the classical results cited in the prior-art table (Section IX).
Theorem 3 with Theorem 4 is offered as new, explicitly, with the condition that a
reader who knows a source should say so. The quantisation bound of Theorem 5 is
proved but not attained in the experiments — the measured worst case was 0.31 of
the bound — and the constant is not claimed to be sharp.

Negative results are in the main text, not in footnotes: a bootstrap interval that
under-covers in two of eight cells (0.892 and 0.900 against a nominal 0.95), a
certificate that saturates at high `β` with few shots (1.63, larger than any
achievable error), and a Helstrom floor whose slack grows with `β`.

## Reproduce everything

```bash
pip install -r requirements-paper.txt

python experiments/otaz_run_quantum.py     # E1–E16 → 19 JSON files in results/
python otaz_make_figures.py                # figures/fig1..fig8 (svg + png, monochrome)
python otaz_make_cover.py                  # publication/OTAZ_III_Cover.*
python otaz_make_social_card.py            # publication/OTAZ_III_Social_Card*
python -m unittest discover -s tests       # 52 unit tests
python scripts/otaz_verify_quantum.py      # 56 independent checks (no library import)
python scripts/otaz_checksums.py           # SHA-256 manifest
python paper/build_manuscript.py           # both PDFs
python scripts/otaz_build_master_zip.py    # OTAZ_III.zip
```

State of this snapshot: **52/52 tests pass, 56/56 checks pass, sixteen experiments
stored in nineteen JSON files, eight figures, two PDFs.**

## Layout

```
otaz_quantum/core.py               library (primitives, algebra, temperature calculus,
                                   coarse graining, ledger, quantum interface, sampling)
experiments/otaz_run_quantum.py    sixteen experiments, writes results/*.json
tests/test_core.py                 52 unit tests, including seven for the ledger
scripts/otaz_verify_quantum.py     independent verifier (does not import the library)
scripts/otaz_checksums.py          SHA-256 manifest
scripts/otaz_build_master_zip.py   packs the whole deposit into OTAZ_III.zip
otaz_make_figures.py               monochrome figures (no colour anywhere)
otaz_make_cover.py                 cover card
otaz_make_social_card.py           black-and-white post cards (square and wide)
paper/                             manuscript modules, CSS, build script
results/                           nineteen JSON files, environment, verification
figures/                           fig1_reachable … fig8_helstrom, .svg and .png
publication/                       PDFs, cover, post cards, novelty assessment,
                                   metadata, archives
docs/                              reading, release, publishing and colour guides
```

## Determinism

Every experiment is seeded from a master seed (`2026110101`) with a fixed
per-experiment offset. No wall-clock timing is stored as a scientific result;
`results/environment.json` records versions and marks elapsed CPU time as
non-scientific. `results/source_hashes.json` is regenerated on every run and is
re-checked by the verifier, so an edit to the code without a fresh run fails
verification.

Determinism on one machine is **not** replication: the verifier is independent
code but runs on the same host against the same stored outputs.

## Licences

* Code, experiments, tests, verifier: **PolyForm Noncommercial 1.0.0** (`LICENSE`).
* Text, figures, documentation, results: **CC BY-NC 4.0**
  (`LICENSES/CC-BY-NC-4.0.txt`).

See `NOTICE` for the split and for third-party components.

## Citation

`CITATION.cff` in this repository, or:

```bibtex
@misc{otaz3_gibbs_ledger_2026,
  author       = {Al-Dawoodiya, Al-Mu'taz Billah Salah},
  title        = {{OTAZ III}: The {G}ibbs Ledger --- Exact Aggregation, a Sharp
                  Impossibility Theorem, and Certified Error Budgets for
                  Scored-Record Fusion},
  year         = {2026},
  month        = oct,
  howpublished = {Preprint, Zenodo (DOI to be reserved at deposit)},
  note         = {Not peer reviewed. Companion report:
                  \doi{10.5281/zenodo.23648070}}
}
```

The DOI is intentionally left as a placeholder: this repository does not invent
identifiers, and the real one only exists once the deposit is published.
