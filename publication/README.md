# publication/

| File | What it is |
|---|---|
| `OTAZ_III_Gibbs_Ledger_EN.pdf` | manuscript, single column, A4, 34 pp, black and white |
| `OTAZ_III_Gibbs_Ledger_EN_IEEE_layout.pdf` | same content in an IEEE-style two-column layout, 20 pp |
| `OTAZ_III_Novelty_Assessment_AR.pdf` / `.html` | one-page novelty assessment in Arabic (`تقييم الجدة`), item by item, with falsification conditions |
| `OTAZ_III_Cover.png` / `.svg` | cover card: the object, the formula, eight of the twelve theorems, the size of the evidence base |
| `OTAZ_III_Social_Card.png` / `.svg` | square 1200 × 1200 black-and-white card for the post; the theorems, the sharp constant, the evidence strip |
| `OTAZ_III_Social_Card_wide.png` / `.svg` | the same content in 1200 × 627, for link previews and slides |
| `OTAZ_III_Abstract.md` | abstract as plain text for deposit forms |
| `OTAZ_III_Citation.bib` | BibTeX entries (this paper and the companion report) |
| `OTAZ_III_Zenodo_Metadata.json` | field-by-field metadata for the deposit form |
| `OTAZ_III_Release_Checks.json` | what was run and what came out, plus what is *not* claimed |
| `OTAZ_III_LinkedIn_Post.md` / `_AR.md` | the English post (with the card and the Zenodo link slot) and its Arabic counterpart |
| `OTAZ_III_Research_Package.zip` | code, results, figures, tests, verifier, manuscript sources |
| `OTAZ_III_Publication_Kit.zip` | PDFs, novelty assessment, cover, abstract, BibTeX, metadata, checks |
| `build_packages.py` | rebuilds both ZIPs |

For the order of operations, the files to upload on each platform and the option to
choose in every field, follow `../docs/OTAZ_III_Publishing_Guide_AR.pdf`.

The DOI fields are placeholders, and the post carries `ZENODO-LINK` until the record
is reserved. Nothing in this folder claims peer review.

The whole deposit, including code, results, figures and manuscript sources, is
packed into a single archive by `python scripts/otaz_build_master_zip.py`, which
writes `OTAZ_III.zip` one level above the repository root; its `MANIFEST.txt` lists
every file inside.
