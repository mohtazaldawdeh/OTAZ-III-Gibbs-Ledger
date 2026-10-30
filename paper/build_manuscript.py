"""Build the OTAZ-III manuscript PDF (black and white only) with WeasyPrint.

Usage:  python paper/build_manuscript.py
Output: publication/OTAZ_III_Gibbs_Ledger_EN.pdf

SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""
import re
import sys
from pathlib import Path

from weasyprint import HTML, CSS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "publication"
OUT.mkdir(exist_ok=True)

sys.path.insert(0, str(HERE))
from sec_1_front import TITLE, ABSTRACT, TOC, SEC_I, SEC_II          # noqa: E402
from sec_2_algebra import SEC_III                                      # noqa: E402
from sec_3_ledger import SEC_IV                                        # noqa: E402
from sec_4_accounting import SEC_V, SEC_VI, SEC_VII                    # noqa: E402
from sec_5_quantum import SEC_VIII                                     # noqa: E402
from sec_6_back import SEC_IX, SEC_X                                   # noqa: E402
from sec_7_tail import SEC_XI, SEC_XII, SEC_XIII, SEC_XIV              # noqa: E402
from sec_8_appendix import (APPENDIX_A, APPENDIX_B, APPENDIX_C,        # noqa: E402
                            REFERENCES)


def group_tables(html):
    """Wrap each table with its caption in one unbreakable block.

    WeasyPrint honours page-break-inside on the table box but can still place a
    caption at the foot of one page and the rows on the next; grouping them in a
    div with break-inside: avoid keeps them together.
    """
    out = []
    pos = 0
    while True:
        start = html.find("<table>", pos)
        if start == -1:
            out.append(html[pos:])
            break
        end = html.find("</table>", start) + len("</table>")
        block = html[start:end]
        cap_start = block.find("<caption>")
        cap_end = block.find("</caption>") + len("</caption>")
        caption = block[cap_start:cap_end]
        rest = (block[:cap_start] + block[cap_end:]).replace("<table>", "<table>", 1)
        out.append(html[pos:start])
        out.append('<div class="tblwrap">' + caption + rest + "</div>")
        pos = end
    return "".join(out)


def build_html(two_column=False):
    columns = [
        SEC_I, SEC_II, SEC_III, SEC_IV, SEC_V, SEC_VI, SEC_VII,
        SEC_VIII, SEC_IX, SEC_X, SEC_XI, SEC_XII, SEC_XIII, SEC_XIV,
        APPENDIX_A, APPENDIX_B, APPENDIX_C, REFERENCES,
    ]
    columns = [group_tables(c) for c in columns]
    if two_column:
        body = TITLE + ABSTRACT + "<div class='columns'>" + "".join(columns) + "</div>"
    else:
        body = TITLE + ABSTRACT + TOC + "".join(columns)
    return ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
            "<title>OTAZ III - Gibbs weights as a ledger</title></head>"
            f"<body>{body}</body></html>")


def word_count(html):
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&[a-zA-Z]+;|&#\d+;", " ", text)
    return len(text.split())


def render(html, css_name, out_name):
    target = OUT / out_name
    HTML(string=html, base_url=str(ROOT)).write_pdf(
        str(target), stylesheets=[CSS(filename=str(HERE / css_name))])
    print(f"written: {target}")
    try:
        import pypdf
        print("  pages:", len(pypdf.PdfReader(str(target)).pages))
    except Exception as exc:            # pragma: no cover
        print("  page count unavailable:", exc)
    return target


def main():
    single = build_html(two_column=False)
    (HERE / "manuscript.html").write_text(single, encoding="utf-8")
    print("words in source:", word_count(single))
    render(single, "style.css", "OTAZ_III_Gibbs_Ledger_EN.pdf")

    two = build_html(two_column=True)
    (HERE / "manuscript_ieee.html").write_text(two, encoding="utf-8")
    render(two, "style_ieee.css", "OTAZ_III_Gibbs_Ledger_EN_IEEE_layout.pdf")


if __name__ == "__main__":
    main()
