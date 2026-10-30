"""Write and verify a SHA-256 manifest of the repository's source and outputs.

Usage:
    python scripts/otaz_checksums.py            # write OTAZ_SHA256SUMS.txt
    python scripts/otaz_checksums.py --verify   # verify against the file

SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "OTAZ_SHA256SUMS.txt"

SKIP_DIRS = {"__pycache__", ".git", ".github", "qa", "node_modules", ".pytest_cache"}
SKIP_NAMES = {"OTAZ_SHA256SUMS.txt", "environment.json", "source_hashes.json",
              "verification.json", "manuscript.html", "manuscript_ieee.html",
              "OTAZ_III_Research_Package.zip", "OTAZ_III_Publication_Kit.zip"}
SUFFIXES = {".py", ".md", ".txt", ".cff", ".yml", ".json", ".svg", ".css", ".pdf",
            ".html", ".bib"}


def iter_files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.name in SKIP_NAMES or path.suffix not in SUFFIXES:
            continue
        yield path


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def main(argv):
    verify = "--verify" in argv
    if verify:
        if not MANIFEST.exists():
            print("no manifest to verify against")
            return 2
        bad, n = [], 0
        for line in MANIFEST.read_text().splitlines():
            if not line.strip():
                continue
            want, rel = line.split("  ", 1)
            path = ROOT / rel
            n += 1
            if not path.exists() or digest(path) != want:
                bad.append(rel)
        print(f"{n - len(bad)}/{n} entries verified")
        for rel in bad:
            print("  mismatch or missing:", rel)
        return 0 if not bad else 1
    lines = [f"{digest(p)}  {p.relative_to(ROOT).as_posix()}" for p in iter_files()]
    MANIFEST.write_text("\n".join(lines) + "\n")
    print(f"wrote {len(lines)} entries to {MANIFEST.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
