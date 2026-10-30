"""Render the one-page Arabic novelty assessment (تقييم الجدة) to PDF.

Usage:  python publication/otaz_build_novelty_ar.py
Output: publication/OTAZ_III_Novelty_Assessment_AR.pdf  (must be exactly one A4 page)

SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""
from pathlib import Path

from weasyprint import HTML

HERE = Path(__file__).resolve().parent


def main():
    source = HERE / "OTAZ_III_Novelty_Assessment_AR.html"
    target = HERE / "OTAZ_III_Novelty_Assessment_AR.pdf"
    HTML(str(source)).write_pdf(str(target))
    pages = "unknown"
    try:
        import pypdf
        pages = len(pypdf.PdfReader(str(target)).pages)
    except Exception:                      # pragma: no cover
        pass
    print(f"written: {target}  pages: {pages}")
    if pages != 1 and pages != "unknown":
        raise SystemExit("the novelty assessment must fit on one page")


if __name__ == "__main__":
    main()
