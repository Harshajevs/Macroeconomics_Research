HS455: Food Inflation and Unemployment — Evidence from Urban India
Clarity revision, 25 November 2026

OPEN
HS455_Report.pdf is the updated report. report.tex is the editable source.
The earlier formal report remains preserved in its separate output folder.

RESEARCH ANSWERS
Question 1: The matched Urban sample does not support a stronger negative
unemployment relationship after excluding food/fuel; food-only exclusion gives
the same qualitative answer. This does not rule out a structural Phillips curve.
Question 2: Food receives 88.71% of monthly and 80.96% of annual Combined
headline variance under covariance accounting. The historical allocation is
well supported by the reported data/sample checks. It is not a causal shock share.
Extension: No clear positive delayed predictability is detected under the monthly
specification. Limited power leaves small spillovers unresolved.

CLARITY CHANGES
The discussion connects each result to a question and explains what the sign,
spread, fit, variance share and uncertainty imply. Section 5 retains the required
common heading, with separate 5.1 Conclusion and 5.2 Policy implications.
The figures, underlying data, estimates and numerical tables are retained.
The spillover plot has more vertical space for readability. No new model or
preferred specification was selected for this revision.

LENGTH AND LAYOUT
Main text: 3,970 words on 12 pages, printed pages 1--12 / PDF pages 2--13.
The count includes narrative, headings, captions, source lines and table text;
a decimal number counts as one token. Equations, inline mathematics, plot-axis
labels, references and appendices are excluded.
The complete PDF has 14 pages. References share PDF page 13 with the final main
section and take less than half of the usable page height. Appendices A and B
share PDF page 14. There are 12 figures, 20 panels and 10 tables in total.
Headings remain bold black. Links, citations and cross-references remain dark blue.

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
The JSON record lists 147 passing numerical/document checks and the count scope.
research_data is the portable subset used for report figures/tables and checks.
The separately delivered earlier research checkpoint contains the full raw-source
retrieval and estimation/simulation code.
