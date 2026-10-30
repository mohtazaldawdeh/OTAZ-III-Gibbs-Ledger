# Colour policy (black and white only)

The document and every figure are monochrome. This is enforced by construction,
not by inspection:

* `otaz_make_figures.py` sets `axes.prop_cycle` to a single black entry, sets all
  text, tick and spine colours to black, and distinguishes curves by **line style
  and marker shape** only.
* No figure uses a colormap, a fill colour other than white, or a hatch colour.
* The cover (`otaz_make_cover.py`) draws black rules explicitly; the default
  patch colour is never used for a visible element.
* The stylesheets (`paper/style.css`, `paper/style_ieee.css`) declare no colour
  other than `#000` and `white`.
* The Arabic novelty assessment
  (`publication/OTAZ_III_Novelty_Assessment_AR.html`) is styled with `#000` and
  `#fff` only, and uses rules rather than shading in its tables.
* Tables use borders rather than shading.

To re-audit: `grep -n "color" otaz_make_figures.py otaz_make_cover.py` and check
that every occurrence is black or "white".
