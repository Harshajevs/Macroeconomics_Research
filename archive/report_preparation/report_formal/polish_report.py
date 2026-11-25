from pathlib import Path
p=Path('report.tex');s=p.read_text()
s=s.replace('\\definecolor{ink}{HTML}{203743}','\\definecolor{ink}{HTML}{000000}')
s=s.replace('\\definecolor{accent}{HTML}{12647A}','\\definecolor{accent}{HTML}{153E6F}')
s=s.replace('linkcolor=ink,citecolor=accent,urlcolor=accent','linkcolor=accent,citecolor=accent,urlcolor=accent')
changes={
'Food prices are often the most visible part of inflation. A rise in grocery bills affects everyday spending, but it need not signal the same economic conditions as a rise in prices driven by strong demand. Demand can raise both prices and employment. A poor harvest can raise food prices while employment remains weak. This difference makes the composition of inflation relevant when studying its relationship with unemployment.':
'This report studies the relationship between inflation and unemployment in India and measures food\'s contribution to headline-inflation variability. Demand growth can increase prices and employment together. A food-supply disruption can instead raise prices during weak employment conditions. Separating food from the remaining CPI groups helps us examine whether these different sources of price change affect the estimated unemployment relationship.',
'We examine that possibility rather than assume that a measure called ``core\'\' must behave in this way.':
'We test this possibility using the same observations for headline and core inflation.',
'The literature provides useful reference points.':'Three studies inform the analysis.',
'We use these studies to motivate the questions, while keeping our simpler estimates and their limitations clear.':
'Our estimates use simpler models and a different sample, so they are compared with these studies rather than treated as replications.',
'This also explains why we keep two outcomes in view. A large food allocation may help explain a noisy headline series, yet it need not reveal what drives unemployment. A clear answer requires checking that second link directly. The value of the exercise is the comparison between the hypotheses and the data, including cases where the expected relationship does not appear.':
'We estimate the unemployment relationship separately from the variance allocation. A large food share in headline variability does not, by itself, establish that excluding food improves the Phillips-curve relationship. Each question therefore has its own measure, sample and hypothesis. The conclusions depend on those calculations rather than on whether the estimated signs match the expected pattern.',
'The time paths immediately identify an unusual observation: unemployment reaches':'Unemployment reaches',
'Headline and core inflation do not move in a simple mirror image of unemployment. Their shared trends and differing responses suggest that a fitted line will need to be interpreted alongside the distribution and influence checks.':
'Neither inflation series shows a stable inverse movement with unemployment over the full period. We therefore examine sample moments, fitted slopes and the influence of individual quarters before interpreting the relationship.',
'These summaries agree with the concentration visible in the plot.':
'The mean, median and standard deviation describe different features of the same observations.',
'Figure~\\ref{fig:distribution} makes the contrast visible.':'Figure~\\ref{fig:distribution} shows the observed distributions.',
'The estimation can be traced to basic arithmetic.':'The OLS calculation uses centred cross-products.',
'This sensitivity reinforces the need to assess the complete pattern rather than select one favourable coefficient.':
'The trend-adjusted result therefore does not provide evidence of a negative core relationship.',
'Question 2 therefore has a clear accounting answer: food contributes more to measured variability than its expenditure weight alone would suggest.':
'Food\'s variance allocation therefore exceeds its expenditure weight in both baskets and at both horizons.',
'The contribution paths show why food receives a large share.':'The monthly contribution paths are consistent with the variance results.',
'The graph still allows exceptions: an allocation over the whole sample does not require food to dominate in every month.':
'Food need not be the largest contribution in every month for its full-sample variance share to be high.',
'The checks serve different purposes. Complete dates establish coverage; published anchors establish source agreement; the residual establishes arithmetic reconciliation. Agreement across these checks is more persuasive than relying on a successful download or a single headline match.':
'Coverage, source agreement and accounting reconciliation are checked separately. None is used as a substitute for the other two.',
'The extension therefore adds a cautious result: large headline accounting exposure to food can coexist with weak evidence of delayed predictability in other prices.':
'These results show large direct food contributions to headline variability, with limited evidence of delayed predictability in the other price groups.',
'The practical lesson is to examine headline and core together.':'The results support examining headline and core together.'
}
for a,b in changes.items():
 assert a in s,a
 s=s.replace(a,b,1)
# A numerical influence calculation, using the actual design matrix.
a='The 2020Q2 observation accounts for 61.38\\% of centred unemployment variation; the three excluded quarters account for 75.43\\%.'
b=a+' Its OLS leverage is 0.6509, calculated as $1/27+0.6138$, compared with average leverage $2/27=0.0741$. This measures how strongly its unemployment value can influence the fitted line; it does not establish that the observation is erroneous.'
s=s.replace(a,b)
# One full page of additional empirical work, keeping the original research questions.
new=r'''
\clearpage
\subsection{Further calculations from monthly contributions}

We calculate the mean, median and standard deviation of food's contribution and the sum of the other contributions. These are percentage-point contributions to headline inflation, not inflation rates within the separate baskets. The other series includes the residual so that the two series add to official headline inflation in every month.

\input{tables/contribution_statistics}

\fig{11_calendar_contributions.pdf}{Combined CPI: calendar-month mean contributions. Each mean uses 12 or 13 observations from February 2013--December 2025.}{fig:calendar}{Calculations from the raw monthly contribution series.}

The mean food contribution is 0.941 percentage points in July and $-0.527$ in December. Its calendar pattern is larger than that of the other contributions. This describes the raw sample and does not identify weather or supply effects. Keeping seasonality in the main variance calculation is appropriate because the question concerns variation in the official unadjusted headline rate.

\fig{12_covariance_calculation.pdf}{Food allocation split into its own-variance and covariance terms. Both use official headline variance as the denominator.}{fig:covsplit}{Calculations from the same 155 monthly observations.}

Food's contribution variance is 0.366607 and its covariance with the other contributions is 0.027200. Their sum, 0.393807, is the covariance with headline inflation. Dividing each term by headline variance gives $82.58+6.13=88.71\%$. The positive covariance term shows that movements in the other contributions reinforce food's variance allocation on average. It is an accounting relationship, not evidence that one group causes price changes in another.
'''
a='\\clearpage\n\\subsection{Extension: food--non-food predictability}'
assert a in s;s=s.replace(a,new+'\n'+a,1)
# Replace the report's bibliography and appendices together, removing software/reproduction commentary.
s=s.split('% MAIN_TEXT_END')[0]+'% MAIN_TEXT_END\n'
refs=r'''
\par\medskip
\begin{minipage}{\linewidth}
\begingroup\setstretch{1.0}
\begin{thebibliography}{99}\fontsize{9}{10.8}\selectfont
\setlength{\itemsep}{2pt}\setlength{\parskip}{0pt}
\bibitem{cpiapi} MoSPI. \href{https://esankhyiki.mospi.gov.in/macroindicators?product=cpi&tab=api}{Consumer Price Index API, v2.0.0: historical 2012-base Urban series}. Accessed 21 November 2026.
\bibitem{cpirelease} NSO (2025). \href{https://www.mospi.gov.in/sites/default/files/press_release/CPI_PR_12Feb25.pdf}{Consumer Price Index Numbers, January 2025}. 12 February, Annexure I.
\bibitem{plfs2024} NSO. \href{https://mospi.gov.in/sites/default/files/publication_reports/PLFS_Quarterly_Bulletin_Oct-Dec24.pdf}{PLFS Quarterly Bulletin, October--December 2024}. Statement 5, Urban persons aged 15+.
\bibitem{plfs2019a} NSO. \href{https://www.mospi.gov.in/sites/default/files/publication_reports/Quarterly_Bulletin_PLFS_April_June_2019_M_0.pdf}{PLFS Quarterly Bulletin, April--June 2019}. Statement 5, p.~6 (PDF p.~9).
\bibitem{plfs2019b} NSO. \href{https://mospi.gov.in/sites/default/files/publication_reports/Quarterly_Bulletin_July_September_2019_M.pdf}{PLFS Quarterly Bulletin, July--September 2019}. Statement 5, p.~6 (PDF p.~9).
\bibitem{plfschange} MoSPI (2025). \href{https://www.mospi.gov.in/sites/default/files/publication_reports/PLFS_Changes-in-2025_rev.pdf}{PLFS: Changes in 2025}. Survey-design and comparability note.
\bibitem{imputation} NSO (2020). \href{https://www.mospi.gov.in/sites/default/files/press_release/CPI%20Technical%20Note%20on%20Imputation.pdf}{Compilation of Consumer Price Index: A Technical Note}. Table 1.
\bibitem{behera2017} Behera, H., Wahi, G. and Kapur, M. (2017). \href{https://rbi.org.in/Scripts/PublicationsView.aspx?id=17752}{Phillips Curve Relationship in India: Evidence from State-Level Analysis}. RBI Working Paper 08/2017.
\bibitem{patra2024} Patra, M.~D., John, J. and George, A.~T. (2024). \href{https://rbi.org.in/Scripts/BS_ViewBulletin.aspx?Id=22323}{Are Food Prices the `True' Core of India's Inflation?} RBI Bulletin, 18 January.
\bibitem{mohan2026} Mohan, R., Hasan, S., Sarkar, S. and John, J. (2026). \href{https://www.rbi.org.in/Scripts/BS_ViewBulletin.aspx?Id=23980}{Retail Inflation Volatility in India: Sources, Determinants, and Implications}. RBI Bulletin, 20 February.
\end{thebibliography}
\endgroup
\end{minipage}

\par\medskip
\appendix
\section{Regression details and inference checks}
\input{tables/regression_details}
\input{tables/calibration}
\fig{10_power.pdf}{Power for the non-food equation under AR/GARCH errors. Each point uses 1,000 recursive datasets and 999 bootstrap draws. Rejection is 5.4\% at a delayed sum of 0.048, 31.6\% at 0.100 and 93.8\% at 0.200. Higher null rejection can inflate apparent power.}{fig:power}{Recursive simulation; true effects allocated equally over three food lags.}

\Needspace{6\baselineskip}
\section{Accounting and source checks}
\label{app:validation}

The earlier 90.5899\% share uses a reconstructed aggregate of separately seasonally adjusted groups. It differs from the raw official-headline target. Adjusting General and every group independently with STL assigns 24.2410\% of Combined variance and 25.0889\% of Urban variance to the reconciliation residual. Corresponding food shares are 69.7544\% and 61.3913\%. This residual includes seasonal-adjustment inconsistencies and is not an economic category.

PLFS corrections use Statement 5, printed p.~6 (PDF p.~9), in the two 2019 bulletins. CPI imputation flags follow the technical note: Urban pan/tobacco is macro-imputed in April 2020 but is not marked in May; Urban housing and fuel/light are not marked in either month. Elementary-level imputation may still occur. Annual exclusions remove changes using April--May 2020 in either period, including April--May 2021.

Calendar HAC respects actual quarter distances after exclusions. The monthly simulations regenerate lagged outcomes recursively. Block-wild null rejection ranges from 4.0--6.1\% for non-food and 4.3--7.1\% for core across the simulated error processes. These checks do not guarantee correct inference under every process. Reverse predictability remains exploratory: adding a lagged relative-price term changes one joint bootstrap tail from 0.0965 to 0.0341, demonstrating specification sensitivity.
\end{document}
'''
p.write_text(s+refs)
