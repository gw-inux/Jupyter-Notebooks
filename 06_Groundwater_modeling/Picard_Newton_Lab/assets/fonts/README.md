# Figure fonts

Noto Sans Arabic, Noto Sans Devanagari and Noto Sans CJK SC are distributed with
their accompanying SIL Open Font License notices. The Simplified Chinese face
has been extracted from the Noto CJK collection without changing its glyphs.

The application uses these local files for figure layout. It embeds only the
glyphs used in each SVG, together with their shaping tables. Latin text and
mathematical notation use the DejaVu Sans font already distributed by
Matplotlib; its license is also included here. Browser text rendering joins
Arabic and Devanagari characters correctly. No external font service is used.

Keep this entire folder when deploying the app. Font subsetting is display-only
and cached; it does not participate in model calculations.
