# Release steps — OTAZ III

The full step-by-step procedure, in Arabic, with the exact file names to upload on
each platform and the option to choose in every field, is
`docs/OTAZ_III_Publishing_Guide_AR.pdf` (source `.html`, rebuilt by
`python docs/build_publishing_guide.py`). The short version is below.

Everything here is performed by the author; this repository does not create
accounts, reserve DOIs or claim deposits.

## 1. Local verification (10 minutes)

```bash
python experiments/otaz_run_quantum.py
python otaz_make_figures.py
python otaz_make_cover.py
python otaz_make_social_card.py
python -m unittest discover -s tests
python scripts/otaz_verify_quantum.py
python scripts/otaz_checksums.py
python paper/build_manuscript.py
python publication/build_packages.py
python scripts/otaz_build_master_zip.py
python docs/build_publishing_guide.py
```

Expected: 52/52 tests, 56/56 checks, sixteen experiments in nineteen JSON files,
eight figures, two PDFs, the cover, two post cards, the Arabic novelty assessment
PDF, a written manifest, and `OTAZ_III.zip` one level above the repository root.
Record any deviation in `CHANGELOG.md` before publishing.

## 2. Build the Arabic novelty assessment

```bash
python - <<'PY'
from weasyprint import HTML
HTML("publication/OTAZ_III_Novelty_Assessment_AR.html").write_pdf(
    "publication/OTAZ_III_Novelty_Assessment_AR.pdf")
PY
```

It must come out as exactly one A4 page. If it spills, shorten the table cells
rather than the falsification section: the falsification conditions are the part a
reader is entitled to.

## 3. The post

`publication/OTAZ_III_LinkedIn_Post.md` holds the English text and a checklist.
Attach `OTAZ_III_Social_Card.png`; replace `ZENODO-LINK` with the reserved record
URL; do not state a DOI before it exists. The Arabic counterpart is
`publication/OTAZ_III_LinkedIn_Post_AR.md`.

## 4. GitHub

1. Create an empty repository named `OTAZ-III-Gibbs-Ledger` (public, no README).
2. `git init && git add . && git commit -m "OTAZ III v3.0.0"`.
3. `git remote add origin <your-url>` and push.
4. Check the Actions tab: the `OTAZ-III tests` workflow runs the tests, the
   experiments, the figures, the verifier and the checksum verification.
5. Create a release `v3.0.0`, attach the ZIPs from `publication/`, and paste the
   abstract from `publication/OTAZ_III_Abstract.md`.

## 5. Zenodo

1. Log in with GitHub or e-mail; link the repository under *Settings → GitHub* if
   you want automatic archiving.
2. *New upload*; drag the files: the two manuscript PDFs, the novelty assessment
   PDF, the cover, the post cards, and **`OTAZ_III.zip`** as the master archive
   (or the two smaller ZIPs if the record has a size limit).
3. Fill the metadata from `publication/OTAZ_III_Zenodo_Metadata.json`:
   publication type **preprint**, language **eng**, licence **CC BY-NC 4.0**,
   related identifier `10.5281/zenodo.23648070` with relation *is supplement to*.
4. Add your ORCID iD in the creators field — **only your real one**. The metadata
   file carries the placeholder `TO-BE-ADDED-BY-AUTHOR` on purpose.
5. Reserve the DOI, put it into `CITATION.cff`, the README and the BibTeX entry,
   re-run `scripts/otaz_checksums.py`, commit, then publish.
6. After publishing, add the DOI to the LinkedIn post and to the GitHub release
   notes. Do not edit the files after publishing; use a new version.

## 6. ORCID

*Works → Add → Add work with DOI → Retrieve → confirm visibility → Add.* ORCID
hosts metadata, not the PDF. Use the published version DOI.

## 7. What not to write anywhere

* "peer reviewed", "accepted", "indexed";
* a DOI, ORCID iD or repository URL that does not exist yet;
* "quantum advantage", "speed-up", "solves";
* any claim of priority for the classical results named in the prior-art table;
* that the quantisation bound of Theorem 5 is attained, or that its constant is
  sharp.
