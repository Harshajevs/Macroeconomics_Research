from pathlib import Path
p=Path('report.tex');s=p.read_text()
def paragraph(start,new):
 global s
 a=s.index(start);b=s.index('\n\n',a)
 s=s[:a]+new.strip()+s[b:]
paragraph('A distinction between the price level and inflation is useful here.',r'''
Inflation measures how quickly prices change, rather than how high they are. Food can remain expensive after its inflation rate falls because earlier price increases remain in the price level. Our unemployment analysis concerns inflation rates. The variance analysis concerns how much those rates fluctuate across months; it does not measure the full effect on household budgets.
''')
paragraph('We estimate the unemployment relationship separately from the variance allocation.',r'''
The two questions require separate calculations. Food may account for large headline fluctuations even if removing it fails to reveal a negative unemployment relationship. We therefore test each hypothesis against its own outcome, while keeping definitions and samples consistent within each comparison.
''')
paragraph('Our approach joins an Urban unemployment comparison',r'''
We first compare Urban headline and core inflation against the same unemployment observations. We then allocate headline variance across CPI groups, using both Combined and Urban baskets. A monthly food--non-food predictability exercise provides an extension. The conclusions distinguish observed association, accounting contributions and causal effects.
''')
paragraph('The standard deviation uses the squared distance',r'''
We calculate standard deviation from squared deviations around the mean, using $n-1$ in the denominator. Skewness and kurtosis use third and fourth powers of deviations, so unusual observations can strongly affect them. We read these measures alongside the plots. An extreme observation is checked against its source before deciding whether it represents an actual event or a data error.
''')
paragraph('Rescaling the retained weights prevents',r'''
Rescaling makes the retained weights add to one, so removing groups does not mechanically lower the index. The construction still retains energy-sensitive items within miscellaneous. Food-only exclusion therefore checks the assignment's exact question, while removing housing checks whether that large retained group drives the result.
''')
s=s.replace('\\subsection{A first look at the matched Urban series}','\\subsection{What the descriptive statistics tell us}')
s=s.replace('\\subsection{Distribution and correlation evidence}','\\subsection{What correlations say about Question 1}')
s=s.replace('\\subsection{Regression estimates and a worked calculation}','\\subsection{The regression answer to Question 1}')
s=s.replace('\\subsection{Uncertainty, influence and robustness}','\\subsection{How far the unemployment result can be trusted}')
s=s.replace('\\subsection{How much headline variability is allocated to food?}','\\subsection{The answer to Question 2: food dominates variability}')
s=s.replace('\\subsection{Monthly contributions and validation of the allocation}','\\subsection{Whether the food result survives data checks}')
s=s.replace('\\subsection{Further calculations from monthly contributions}','\\subsection{Why food receives a large variance allocation}')
s=s.replace('\\subsection{Extension: food--non-food predictability}','\\subsection{The extension: what we can conclude about spillovers}')
paragraph('The unemployment mean is 8.88',r'''
Average unemployment is 8.88\%, above the median of 8.30\%. The mean is pulled upward by unusually high pandemic observations, which also produce positive skewness and high excess kurtosis. Excluding the three fixed quarters lowers the mean to 8.05\%, the median to 8.00\%, and SD from 2.98 to 1.32 percentage points. This matters for Question 1 because the estimated slope depends heavily on a few quarters, rather than on many observations spread evenly across unemployment rates.
''')
paragraph('For annual inflation, headline and core standard deviations are close:',r'''
Annual headline and core inflation have similar SDs, 1.02 and 0.99. At the shorter q/q SAAR horizon, they are 2.14 and 1.23. Core's SD is about 42.4\% lower, from $100(1-1.2328/2.1388)$. Exclusion therefore removes considerable short-run price fluctuation. To support Question 1, however, core would also need to move downward as unemployment rises. Lower volatility alone cannot establish that relationship.
''')
paragraph('The full-sample unemployment correlation is',r'''
In the full sample, unemployment and annual headline inflation have correlation $+0.276$; for core it is $+0.370$. Positive signs mean that higher unemployment tends to occur alongside higher inflation across these observations. After exclusion, headline's correlation becomes $-0.080$, while core remains positive at $+0.537$. The core relationship is therefore not the expected negative one. A larger positive correlation cannot count as evidence supporting the hypothesis.
''')
paragraph('Correlation standardises the covariance',r'''
Correlation compares direction and closeness after adjusting for each series' spread. The regression slope keeps percentage-point units, with $\hat\beta=r(s_\pi/s_U)$. Both are useful because removing volatile components changes inflation's spread as well as its relationship with unemployment. Their signs give the same answer here.
''')
paragraph('These correlations should be read within',r'''
These results describe joint movement during the sample, not the reason for that movement. Recovery, supply conditions and policy responses may affect both series. We have not separately identified their effects. The positive correlations therefore do not show that unemployment causes inflation to increase. The regressions next express the same comparison in interpretable units.
''')
paragraph('The fitted annual lines are',r'''
The fitted annual lines are $\hat\pi_H=4.3747+0.0943U$ and $\hat\pi_C=3.7507+0.1228U$. Reading along these lines, unemployment of 9\% rather than 8\% is associated with about 0.094 percentage points higher headline inflation and 0.123 points higher core inflation. The expected negative relationship would require inflation to fall along the line. The intercept at zero unemployment lies outside the observed range and has no practical interpretation here.
''')
paragraph('The full annual slope difference is',r'''
The full annual difference is $0.1228-0.0943=+0.0285$, and the q/q difference is also positive, $+0.162$. Under exclusion, headline becomes slightly negative but core remains positive. \textbf{Question 1 is therefore not supported by these four primary comparisons.} Annual $R^2$ is 0.076 for headline and 0.137 for core: the lines account for about 8\% and 14\% of their respective variation, with positive slopes. A closer positive fit does not support a stronger negative relationship. The identity $R^2=r^2$, so $0.276^2\approx0.076$, checks this calculation.
''')
paragraph('Figure~\\ref{fig:delta} displays',r'''
Figure~\ref{fig:delta} shows how uncertain the slope comparison is. Most nominal 95\% HC3 ranges include zero, meaning the data do not sharply distinguish the difference from zero under that calculation. The annual exclusion range is positive. However, the short sample, overlapping annual inflation and dependent errors weaken nominal coverage. We can describe the observed signs confidently; we cannot claim a well-identified, stable relationship for India from these estimates.
''')
paragraph('The 2020Q2 observation accounts for',r'''
The 2020Q2 observation accounts for 61.38\% of centred unemployment variation; all three excluded quarters account for 75.43\%. Its OLS leverage is 0.6509, from $1/27+0.613816$, versus average leverage $2/27=0.0741$. This confirms its strong influence on the fitted line, rather than a source error. Exclusion reduces that influence but also removes much of the information available for a slope. Food-only exclusion answers the assignment directly and still leaves positive core slopes. Removing housing does too. A calendar trend changes the annual slope difference's sign, but both inflation slopes remain positive. Thus, the checks preserve the sample-level answer without proving that a structural Phillips curve is absent.
''')
paragraph('Food receives 88.71',r'''
\textbf{For Question 2, food accounts for most measured headline variability under our accounting definition.} Its allocations are 88.71\% for monthly Combined changes and 80.96\% for annual changes. Urban shares are 79.85\% and 64.69\%. All exceed the respective food basket weights, 45.86\% and 36.29\%. Food's prices fluctuate enough, and move sufficiently with the whole basket, to receive a larger variance allocation than its spending weight alone would imply.
''')
paragraph('This calculation includes food',r'''
The calculation assigns food its own contribution variance and its covariance with the remaining contributions. The residual closes the published headline/group aggregation gap, keeping the complete allocation exact. Because shared movements enter the calculation, this is an accounting answer rather than a causal estimate of independent food shocks.
''')
paragraph('A component with a steady positive contribution',r'''
In plain terms, the question concerns the headline rate's ups and downs across months. A group can add steadily to inflation yet explain little of those changes. Food's contribution varies much more, so it receives a high share. The 88.71\% does not mean food causes 88.71\% of every month's inflation or that removing food would reduce average inflation by that percentage.
''')
paragraph('The denominator measures how much headline',r'''
Every group uses the same headline-variance denominator, allowing a consistent comparison. The remaining groups and residual jointly receive 11.29\% of monthly Combined variance. Their smaller share concerns fluctuations around average inflation, not their importance to household welfare or their contribution to the average rate.
''')
# Remove the now-duplicated explanation, replacing it with the geographic interpretation.
paragraph('The smaller Urban food weight helps',r'''
The lower Urban share is consistent with its smaller food weight, although different group volatility and co-movement also matter. Reporting both baskets answers the broader price-composition question without treating Urban employment evidence as evidence about rural labour markets.
''')
paragraph('The annual Combined descriptive range',r'''
The Combined descriptive ranges are 85.94--93.14\% monthly and 70.48--98.98\% annually. They support food dominance across the resamples used here, with more uncertainty at the annual horizon. They are sensitivity checks, not guaranteed population confidence intervals. The historical calculation is precise for its inputs; its percentage need not apply unchanged to another period or CPI basket.
''')
paragraph('The 89.07',r'''
The monthly share is 89.07\% over the matched unemployment period, close to the full-history 88.71\%. Removing imputation-exposed changes gives 88.61\%, while pre-2020 and post-2021 shares remain high. This strengthens the answer to Question 2: food dominance survives the specified sample and data-quality checks. It is not driven solely by using a longer price series or retaining the exceptional collection period.
''')
paragraph('Source validation supports this interpretation.',r'''
The Urban CPI input contains 156 consecutive months and 1,092 group/general observations, without missing levels. Fifty-six independent anchor comparisons cover eight published months. Weighted groups reproduce Urban headline within 0.08034 index points. These checks support the data construction; they do not identify causal shocks or remove uncertainty about other samples.
''')
paragraph('Coverage, source agreement',r'''
Together, the checks establish what the data cover, whether published sources agree, and whether contributions reconcile with headline. Agreement makes the historical accounting result more credible, while leaving its economic scope unchanged.
''')
paragraph('Food\'s contribution has a slightly lower mean',r'''
The contribution table explains the large share economically: food has a slightly lower mean contribution than all other contributions combined, but about four times their SD. Its influence on variability therefore comes from larger month-to-month movements, rather than from a larger average contribution. These are percentage-point contributions to headline inflation. The remaining series includes the residual so the two add to official headline each month.
''')
paragraph('The mean food contribution is',r'''
Food's mean contribution is 0.941 percentage points in July and $-0.527$ in December. The larger calendar pattern helps explain why food contributes strongly to raw headline fluctuations. This descriptive pattern does not identify weather or supply effects. We retain seasonality because Question 2 concerns variation in the official unadjusted rate; removing it would change the question being answered.
''')
paragraph('Food\'s contribution variance is',r'''
Food's contribution variance is 0.366607 and its covariance with other contributions is 0.027200. Their sum, 0.393807, is the covariance with headline. Dividing each by headline variance gives $82.58+6.13=88.71\%$. Thus most of food's allocation comes from its own fluctuation, with a smaller addition from moving with other contributions. This supplies the arithmetic reason for the result while leaving the source of those shared movements unidentified.
''')
paragraph('The delayed sums,',r'''
The delayed sums are $-0.0035$ for non-food and $-0.0188$ for core. Their ranges permit negative, zero and small positive associations, so these estimates do not establish positive delayed transmission. Current-plus-lag sums are positive, 0.0342 and 0.0180, but their ranges also include zero. Same-month co-movement can reflect common costs or simultaneous adjustment, which our model cannot separate from transmission.
''')
paragraph('Non-rejection does not establish zero spillover.',r'''
\textbf{The extension gives no clear evidence of positive delayed predictability under this model, but small effects remain unresolved.} In a recursive non-food simulation, a delayed sum of 0.048 is detected only 5.4\% of the time under the specified persistent-error design. This is a scale comparison; the RBI's 0.048 is a different short-run ARDL quantity~\cite{patra2024}. Low detection power means a small effect can go unnoticed. Reverse predictability is also specification-dependent. We therefore cannot turn non-rejection into a claim that spillovers are zero. Food can dominate headline accounting even when later responses in other price groups are difficult to detect.
''')
a=s.index('\\section{Conclusion and policy implications}')
b=s.index('\\label{main:last}',a)
new=r'''\clearpage
\section{Conclusion and policy implications}
\subsection{Conclusion}

For Question 1, the matched Urban data do not support a stronger negative unemployment relationship after excluding food and fuel. Core slopes remain positive in both primary transformations and after the fixed pandemic exclusion. Food-only exclusion gives the same qualitative answer. Core's lower short-run volatility therefore does not establish the proposed unemployment relationship. With only 27 quarters and substantial pandemic influence, this result cannot rule out a structural Phillips curve in India.

For Question 2, food receives 88.71\% of monthly and 80.96\% of annual Combined headline variance, including its co-movement with other contributions. Its dominance survives the reported sample and imputation checks. This is our strongest descriptive finding. The percentage applies to the historical basket and period, rather than every month's inflation or the causal effect of a food shock.

The extension does not detect clear positive delayed food--non-food predictability, but limited power prevents a conclusion of zero spillover. Together, the results distinguish food's direct role in headline fluctuations from the less certain employment and transmission relationships.

\subsection{Policy implications}

Headline and core should be monitored together. Headline includes food prices faced by households, while core helps describe price movement outside selected groups. A smoother core measure should not automatically be assumed to offer a clearer inflation--employment trade-off.

Food's large variance allocation supports attention to weather, arrivals, storage and distribution in inflation monitoring, consistent with RBI research~\cite{mohan2026,patra2024}. Our accounting does not estimate the benefits of particular interventions. Nor should the unemployment slopes be used to choose an interest rate or calculate job losses required to reduce inflation. Expectations, common costs and policy responses need further evidence. A validated state panel and comparable longer series would help assess whether the sample findings extend more widely.
'''
s=s[:a]+new+s[b:]
p.write_text(s)
