HS455: Food Inflation and Unemployment — Evidence from Urban India
Cover and pagination update, 25 November 2026

OPEN
HS455_Report.pdf is the updated report. report.tex is the editable source.
The previous clarity revision remains preserved in its separate output folder.

CHANGES
The cover follows the supplied example: 26pt main title, 16pt subtitle,
centred course/instructor block, institute logo, affiliation and team table.
Both email addresses are clickable. All links, citations and cross-references
use the exact supplied xcolor shade blue!50!black. Headings remain bold black.
Kohith's email follows the supplied institute entry-number address pattern.
Pagination was adjusted to fill PDF page 3 and meet the 13-page total cap.
The body retains the 10pt font; line spacing is 1.10 and scientific figures
are displayed at 95% of text width. Float placement uses available page space.
No body wording, equation, table value, data or figure asset was changed.
Section 5 retains separate Conclusion and Policy implications subsections.

LENGTH AND LAYOUT
Main text: 3,970 words on 11 pages, printed pages 1--11 / PDF pages 2--12.
The count includes narrative, headings, captions, source lines and table text;
a decimal number counts as one token. Equations, inline mathematics, plot-axis
labels, references and appendices are excluded.
The complete PDF has 13 pages including the cover and appendices.
References share PDF page 12 with the final main section and occupy less than
half of the usable page height. Appendices A and B share PDF page 13.
There are 12 figures, 20 plot panels and 10 tables in total.

COMPILE
Upload the folder to Overleaf and choose report.tex as the main document.
The included packages support standard pdfLaTeX. The local verified build used:
    tectonic --keep-logs --keep-intermediates report.tex
    cp report.pdf HS455_Report.pdf
Tectonic performs the needed reference passes. With pdfLaTeX, run twice.
Python is unnecessary merely to compile the included LaTeX, tables and figures.

OPTIONAL REGENERATION / VERIFICATION
Install packages from requirements.txt, then:
    python3 make_figures.py
    python3 make_tables.py
    python3 additional_analysis.py
Compile as above, followed by:
    python3 verify_report.py
The verifier expects report.log, report.aux and HS455_Report.pdf from compilation.
The JSON record lists 213 passing numerical/document/preservation checks.
preservation_baseline.json records the approved text and unchanged-file hashes.
research_data is the portable subset used for report figures/tables and checks.
The separately delivered research checkpoint contains the full raw-source
retrieval and estimation/simulation code.
