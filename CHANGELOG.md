# Changelog

## 3.0.0 — 2026-10-28

First release of **OTAZ III: The Gibbs Ledger**, a standalone study of scored-record
fusion: a Gibbs-weighted mean of values carried together with the scaled
log-partition sum.

Added
* `otaz_quantum/core.py`: Gibbs primitives and the binary/n-ary algebra; the
  temperature calculus; coarse-graining and hierarchy accounting; the ledger
  functions (impossibility, minimax, quantisation, tree merging); the commuting and
  coherent quantum interface; finite-shot estimation.
* Experiments E1–E16 writing nineteen JSON result files, all seeded from
  `2026110101`.
* Twelve theorems, two lemmas and one corollary, with Appendix A carrying the
  proofs A.1–A.10.
* The central negative result: with value-only summaries the reachable set is the
  convex hull of the reported values (Theorem 3), the minimax rule is the midpoint
  with worst-case error equal to half the range and attained (Theorem 4), and a
  ledger quantised to relative precision δ merges to `Dδ/(1−δ)` for any number of
  shards (Theorem 5).
* Eight monochrome figures (SVG + PNG), a monochrome A4 cover card, fifty-two unit
  tests, a fifty-six-check independent verifier that does not import the library,
  and a SHA-256 manifest script.
* Two black-and-white post cards (`OTAZ_III_Social_Card*`, square 1200 × 1200 and
  wide 1200 × 627) built by `otaz_make_social_card.py`, and the English post text
  with a posting checklist in `publication/OTAZ_III_LinkedIn_Post.md`.
* `docs/OTAZ_III_Publishing_Guide_AR.pdf`: a step-by-step publishing guide in
  Arabic covering GitHub, Zenodo, ORCID and LinkedIn, with the exact file names and
  field choices, plus the rebuild order that keeps the SHA-256 manifest valid.
* `scripts/otaz_build_master_zip.py`, which packs the whole deposit into a single
  `OTAZ_III.zip` with a `MANIFEST.txt` inside.
* Manuscript in two layouts (single column, 34 pp; IEEE-style two column, 20 pp),
  abstract, BibTeX, Zenodo metadata, release checks, LinkedIn drafts (EN/AR),
  a one-page Arabic novelty assessment (`تقييم الجدة`), and deposit guides.

Changed from the earlier architecture of this repository
* The manuscript is no longer organised around an external source section: the
  object, the notation and the scope are defined inside the paper, and Sections
  I–XIV are written as a self-contained study.
* Figures are numbered in order of appearance in the text
  (`fig1_reachable` … `fig8_helstrom`); results files are named by experiment.
* Section IV (the impossibility theorem) is now the longest section of the paper
  and the one the abstract leads with.

Notes
* No DOI is reserved by this release. The BibTeX, README and Zenodo metadata carry
  an explicit placeholder until the author deposits the record.
* Negative results are reported in the main text: the bootstrap interval
  under-covers in two of eight cells, the certificate saturates at high β with few
  shots, and the quantisation bound is proved but not attained (worst measured
  ratio 0.31).
