"""Rebuild the two release archives (code package and publication kit).

SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "publication"

EXCLUDE_DIRS = {"__pycache__", ".git", "qa", ".github", "node_modules"}
EXCLUDE_NAMES = {"OTAZ_III_Research_Package.zip", "OTAZ_III_Publication_Kit.zip"}

CODE_DIRS = ["otaz_quantum", "experiments", "tests", "scripts", "figures",
             "results", "paper", "docs", "LICENSES"]
CODE_FILES = ["README.md", "NOTICE", "LICENSE", "LICENSING.md", "CITATION.cff",
              "CHANGELOG.md", "requirements.txt", "requirements-paper.txt",
              "otaz_make_figures.py", "otaz_make_cover.py", "OTAZ_SHA256SUMS.txt"]

KIT_FILES = ["OTAZ_III_Gibbs_Ledger_EN.pdf", "OTAZ_III_Gibbs_Ledger_EN_IEEE_layout.pdf",
             "OTAZ_III_Cover.png", "OTAZ_III_Cover.svg",
             "OTAZ_III_Novelty_Assessment_AR.pdf", "OTAZ_III_Novelty_Assessment_AR.html",
             "otaz_build_novelty_ar.py",
             "OTAZ_III_Social_Card.png", "OTAZ_III_Social_Card.svg",
             "OTAZ_III_Social_Card_wide.png", "OTAZ_III_Social_Card_wide.svg",
             "OTAZ_III_Abstract.md",
             "OTAZ_III_Citation.bib", "OTAZ_III_Zenodo_Metadata.json",
             "OTAZ_III_Release_Checks.json", "OTAZ_III_LinkedIn_Post.md",
             "OTAZ_III_LinkedIn_Post_AR.md", "README.md"]


def add(zf, path, root):
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return 0
    if path.name in EXCLUDE_NAMES:
        return 0
    zf.write(path, path.relative_to(root).as_posix())
    return 1


def build(name, dirs, files, base):
    target = PUB / name
    n = 0
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for d in dirs:
            for path in sorted((base / d).rglob("*")):
                if path.is_file():
                    n += add(zf, path, base)
        for f in files:
            path = base / f
            if path.exists() and path.is_file():
                n += add(zf, path, base)
    with zipfile.ZipFile(target) as zf:
        bad = zf.testzip()
    print(f"{target.name}: {n} entries, test={'ok' if bad is None else bad}")
    return target


if __name__ == "__main__":
    build("OTAZ_III_Research_Package.zip", CODE_DIRS, CODE_FILES, ROOT)
    build("OTAZ_III_Publication_Kit.zip", [], KIT_FILES, PUB)
