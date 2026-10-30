"""Build the single master archive OTAZ_III.zip containing the whole deposit.

Usage:
    python scripts/otaz_build_master_zip.py            # writes ../OTAZ_III.zip
    python scripts/otaz_build_master_zip.py --out PATH

Everything ships under one top-level folder, OTAZ_III/, with a MANIFEST.txt at its
root listing what is inside and how many files of each kind there are. Caches,
byte-code, git metadata and previously built archives are excluded.

SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""
import hashlib
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT.parent / "OTAZ_III.zip"
PREFIX = "OTAZ_III"

INCLUDE_DIRS = ["otaz_quantum", "experiments", "tests", "scripts", "paper",
                "figures", "results", "docs", "publication", "LICENSES"]
INCLUDE_FILES = ["README.md", "CHANGELOG.md", "CITATION.cff", "LICENSE",
                 "LICENSING.md", "NOTICE", "requirements.txt",
                 "requirements-paper.txt", "OTAZ_SHA256SUMS.txt",
                 "otaz_make_figures.py", "otaz_make_cover.py",
                 "otaz_make_social_card.py"]
EXCLUDE_DIRS = {"__pycache__", ".git", ".github", ".pytest_cache", "node_modules",
                "qa"}
EXCLUDE_SUFFIXES = {".pyc", ".zip"}


def collect():
    files = []
    for name in INCLUDE_DIRS:
        for path in sorted((ROOT / name).rglob("*")):
            if path.is_file() and not _skip(path):
                files.append(path)
    for name in INCLUDE_FILES:
        path = ROOT / name
        if path.exists() and path.is_file() and not _skip(path):
            files.append(path)
    return files


def _skip(path):
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDE_DIRS for part in rel.parts):
        return True
    return path.suffix in EXCLUDE_SUFFIXES


def manifest(files):
    counts = {}
    for path in files:
        key = path.suffix or "no extension"
        counts[key] = counts.get(key, 0) + 1
    lines = ["OTAZ III - The Gibbs Ledger",
             "Master archive of the deposit.",
             "",
             "Title: OTAZ III: The Gibbs Ledger - Exact Aggregation, a Sharp "
             "Impossibility Theorem,",
             "       and Certified Error Budgets for Scored-Record Fusion",
             "Author: Al-Mu'taz Billah Salah Al-Dawoodiya",
             "Version 3.0.0, 2026-10-28. Preprint; not peer reviewed.",
             "",
             f"Files in this archive: {len(files)}",
             "",
             "By kind:"]
    for key in sorted(counts):
        lines.append(f"  {key:>14}: {counts[key]}")
    lines += ["",
              "Start here:",
              "  publication/OTAZ_III_Gibbs_Ledger_EN.pdf            manuscript, 34 pp",
              "  publication/OTAZ_III_Gibbs_Ledger_EN_IEEE_layout.pdf manuscript, two column, 20 pp",
              "  publication/OTAZ_III_Novelty_Assessment_AR.pdf      one-page Arabic novelty assessment",
              "  publication/OTAZ_III_Social_Card.png                black-and-white card for the post",
              "  publication/OTAZ_III_LinkedIn_Post.md               the English post text",
              "  README.md                                           orientation and how to run",
              "",
              "Reproduce: python experiments/otaz_run_quantum.py, then "
              "otaz_make_figures.py,",
              "python -m unittest discover -s tests, "
              "python scripts/otaz_verify_quantum.py.",
              "",
              "Licences: text and results CC BY-NC 4.0; code PolyForm Noncommercial "
              "1.0.0.",
              "No DOI, ORCID iD or repository URL is asserted inside this archive.",
              ""]
    return "\n".join(lines)


def main(argv):
    out = DEFAULT_OUT
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1]).resolve()
    files = collect()
    digest = hashlib.sha256(manifest(files).encode()).hexdigest()[:16]
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.writestr(f"{PREFIX}/MANIFEST.txt",
                    manifest(files).replace("Files in this archive:",
                                            f"Manifest digest: {digest}\n"
                                            f"Files in this archive:"))
        for path in files:
            zf.write(path, f"{PREFIX}/{path.relative_to(ROOT).as_posix()}")
    with zipfile.ZipFile(out) as zf:
        bad = zf.testzip()
        n = len(zf.namelist())
    size = out.stat().st_size / 1024 ** 2
    print(f"written: {out}  ({size:.1f} MB, {n} entries, "
          f"test={'ok' if bad is None else bad})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
