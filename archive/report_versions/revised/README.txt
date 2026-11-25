HS455 — Food Inflation and Unemployment: Evidence from Urban India
Revised report, 21 November 2026

OPEN
HS455_Report.pdf is the report. report.tex is the editable LaTeX source.

STRUCTURE AND LENGTH
The five exact required section headings appear in order:
1. Background and motivation
2. Research questions and hypotheses
3. Data and methodology
4. Discussion of results
5. Conclusion and policy implications

Main text: 3,753 words; 10 pages (printed pages 1--10, PDF pages 2--11).
Word count includes narrative, headings, captions, source lines and table text.
Decimals count as one token. Formulas, inline mathematical expressions and plot
axis labels are excluded, as are the cover, references and appendices.
Total PDF: 14 pages — cover, 10 main pages, 1 reference page, 2 appendix pages.
There are 10 figures with 18 panels and 9 tables across main text/appendices.
Nine figures and seven tables are in the main text.

COVER
The cover uses the supplied 10pt A4 class, 0.75-inch side margins, 0.65-inch
vertical margins, 20/26-point title and logo at 44% of the text width.
Student names, entry numbers and instructors follow the supplied details.
The logo comes from the sample supplied by the user. No department or email
address was inferred. The exact course title was unavailable, so HS455 is used.

COMPILE THE INCLUDED SOURCE
Upload this folder to Overleaf, selecting report.tex as the main document.
It uses standard packages compatible with pdfLaTeX. The verified local build
uses Tectonic 0.17.0:
    tectonic --keep-logs --keep-intermediates report.tex
    cp report.pdf HS455_Report.pdf
Tectonic handles reference passes. With pdfLaTeX, run it twice.
Saved vector figures and tables are included; Python is not required to compile.

OPTIONAL REGENERATION AND NUMERICAL VERIFICATION
Install the packages in requirements.txt, then:
    python3 make_figures.py
    python3 make_tables.py
Compile as above, then:
    python3 verify_report.py
The verifier expects report.log from compilation and HS455_Report.pdf.
report_verification.json contains the 123 passing checks and word/page counts.
Checks independently recalculate descriptive moments, correlations, primary OLS
slopes/fit, HC3 difference intervals, leave-one-out estimates and variance shares.

RESEARCH DATA
research_data is the portable subset needed for report figures, tables and checks.
It contains source and claim registers. The separate, previously delivered
hs455-research-pre-report-checkpoint.zip contains the full retrieval, estimation,
simulation code, raw sources and research audit. This compact report archive does
not duplicate that entire checkpoint.

INTERPRETATION
All unemployment comparisons use matched Urban observations. Positive estimated
core slopes do not establish a positive causal effect. Food allocations are
covariance accounting shares, not shares caused by identified food shocks.
The imputation-exclusion monthly food allocation is 88.614713%, correctly rounded
to 88.61%. Seasonal reconciliation and the historical 90.59% target are explained
in Appendix B. Weak detection power is retained in the spillover interpretation.
