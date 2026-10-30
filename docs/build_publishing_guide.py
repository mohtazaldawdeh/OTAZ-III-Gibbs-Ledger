"""Render the step-by-step Arabic publishing guide to PDF.

Usage:  python docs/build_publishing_guide.py
Output: docs/OTAZ_III_Publishing_Guide_AR.pdf

SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""
from pathlib import Path

from weasyprint import HTML

HERE = Path(__file__).resolve().parent


def main():
    source = HERE / "OTAZ_III_Publishing_Guide_AR.html"
    target = HERE / "OTAZ_III_Publishing_Guide_AR.pdf"
    HTML(str(source)).write_pdf(str(target))
    pages = "unknown"
    try:
        import pypdf
        pages = len(pypdf.PdfReader(str(target)).pages)
    except Exception:                      # pragma: no cover
        pass
    print(f"written: {target}  pages: {pages}")


if __name__ == "__main__":
    main()
