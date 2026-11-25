HS455: Food Inflation and the Phillips Relationship in India
AI-assisted review draft | November 2026

WHAT TO OPEN
HS455_Report_Review_Draft.pdf is the report.
report.tex is the editable main source; cover_details.tex holds the cover details.
The assets and tables folders must remain beside report.tex.

CONTENT AND LENGTH
The five mandatory sections are included in the requested order.
The main text occupies printed pages 1--10 (PDF pages 2--11).
Cover: PDF page 1. References: PDF page 12. Appendices: PDF pages 13--16.
There are 3,048 paragraph-prose words, excluding headings, figure/table text,
and mathematical expressions. A deliberately inclusive count of ALL content
on main PDF pages, including running heads, equations and chart labels, is
3,844 whitespace-delimited tokens. Both checks exclude references/appendices.
Five vector figures and nine tables appear across the report and appendices.

READINESS AND COURSE RULE
This is a complete review draft, not a certification of submission compliance.
AI assisted the research, code, calculations, figures and prose. The students
must verify the results, understand the calculations, revise in their own words
where required, and follow the course's below-30% AI-use rule. No detector score
or AI percentage is claimed. Detailed disclosure is in Appendix C.
The exact course title was not supplied, so the cover uses HS455 only.
The original named Assignment_HS455.pdf was unavailable; the report follows
the requirements quoted by the user (3,000--4,000 words and five sections).
The supplied CQF sample informed the cover, and its embedded institute logo
was reused. Its subject matter, department and course title were not copied.

COMPILE
Upload this folder's contents to an Overleaf project and select report.tex as
the main document. Standard pdfLaTeX should support the included packages.
Locally, the verified build used Tectonic 0.17.0:
    tectonic --keep-logs --keep-intermediates report.tex
    cp report.pdf HS455_Report_Review_Draft.pdf
Tectonic performs the needed reference passes. With pdfLaTeX, run it twice.
Python is not needed merely to compile the supplied LaTeX and saved assets.

OPTIONAL: REGENERATE FIGURES/TABLES AND CHECK NUMBERS
Python packages: numpy, pandas, matplotlib, scipy and pypdf.
    python3 make_figures.py
    python3 make_tables.py
Then compile as above, followed by:
    python3 verify_report.py
The verifier expects report.log from the compile and the named review PDF.
report_verification.json records the 65 passing checks and word/page counts.
numerical_audit.json links the main comparison/variance numbers to the included
CSV results. The verifier independently refits the four primary regressions,
recalculates their HC3 intervals, verifies the worked index examples and
recalculates complete covariance allocations from component contributions.

DATA AND RESEARCH SCOPE
research_data contains the saved inputs/results needed for figure/table
regeneration and report verification. It is a compact report subset, not the
full source-retrieval/model-estimation package. Source register and claim ledger
are included under research_data/documentation.
The full prior research package is separately available as:
    hs455-research-pre-report-checkpoint.zip
It contains the raw sources, extraction decisions, estimation/simulation scripts,
validation outputs and older project stages. No model or specification was
reselected during report writing to obtain a preferred finding.

INTERPRETATION
Food's main shares are 88.71% monthly and 80.96% annual for Combined CPI;
Urban shares are 79.85% and 64.69%. These are covariance accounting allocations,
not causal estimates. The older 90.59% applies to a reconstructed seasonally
adjusted target and is explicitly distinguished in the report.
The Urban unemployment comparison does not support a stronger negative
relationship after excluding food/fuel. Positive estimated core slopes do not
establish a positive structural effect. The monthly spillover extension has
limited power and does not prove that spillovers are zero.
