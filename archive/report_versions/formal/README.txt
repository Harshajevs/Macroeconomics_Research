HS455: Food Inflation and Unemployment — Evidence from Urban India
Formal report revision, 23 November 2026

DELIVERABLE
HS455_Report.pdf is the report; report.tex is the editable LaTeX source.
The five main sections retain the exact required headings and order.
All report headings are bold black. Citations, cross-references and linked
reference titles are dark blue. The cover retains the supplied dimensions.
The report contains no reproducibility discussion.

LENGTH AND CONTENT
Main text: 3,978 words on 11 pages (printed pages 1--11; PDF pages 2--12).
The count includes narrative, headings, captions, source lines and table text;
decimal numbers count as one token. Equations, inline mathematics, plot-axis
labels, references and appendices are excluded.
Complete PDF: 14 pages, including cover and reference/appendix material.
References are on PDF page 13 and occupy less than half of the usable page.
They share that page with Appendix A; Appendix B is on PDF page 14.
There are 12 figures with 20 panels and 10 tables across the report.
Eleven figures and eight tables appear in the main text.

ADDED PROJECT CALCULATIONS
The new monthly contribution table compares sample means, medians, standard
deviations and ranges. Calendar-month means use 12 or 13 observations each.
The food covariance calculation separates its 88.71% headline-variance allocation
into an 82.58% own-variance term and a 6.13% covariance term. The pandemic OLS
leverage calculation uses the observed unemployment regressor.

BUILD
Upload this folder to Overleaf and set report.tex as the main document.
Standard pdfLaTeX packages are used. The verified local build uses Tectonic:
    tectonic --keep-logs --keep-intermediates report.tex
    cp report.pdf HS455_Report.pdf
Tectonic performs the reference passes. With pdfLaTeX, run twice.
Python is not needed to compile with the supplied assets and table files.

OPTIONAL CALCULATION / FIGURE REGENERATION
Use the packages in requirements.txt, then:
    python3 make_figures.py
    python3 make_tables.py
    python3 additional_analysis.py
Compile as above, followed by:
    python3 verify_report.py
The verifier expects report.log and HS455_Report.pdf from the build.
The JSON verification record contains all 141 passing checks and count definitions.
Those checks cover numerical values, data scope, document structure and layout.
They do not measure or certify an AI-content percentage or course-policy compliance.

SOURCE DATA
research_data contains the portable data subset, results, source register and
claim ledger needed for this report. The separate earlier research checkpoint
archive contains the complete raw-source retrieval and model-estimation code.
Older report versions are preserved separately. No results were selected anew
for this wording/layout revision.
