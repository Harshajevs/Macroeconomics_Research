from pathlib import Path
p=Path('report.tex');s=p.read_text()
additions=[
('Our approach joins an Urban unemployment comparison', '''A distinction between the price level and inflation is useful here. A household can still face expensive food after food inflation falls, because a slower rate of increase does not reverse earlier price rises. Likewise, a low average inflation rate can coexist with sharp monthly fluctuations. Our unemployment exercise concerns the rate of price change, while the variance exercise concerns fluctuations around its average. Neither calculation measures the complete burden on a household budget.

This also explains why we keep two outcomes in view. A large food allocation may help explain a noisy headline series, yet it need not reveal what drives unemployment. A clear answer requires checking that second link directly. The value of the exercise is the comparison between the hypotheses and the data, including cases where the expected relationship does not appear.

Our approach joins an Urban unemployment comparison'''),
('Quarterly levels average all three monthly indices.', '''Rescaling the retained weights prevents the core index from falling simply because two groups have been removed. It keeps the index on a comparable scale before growth rates are calculated. The construction is nevertheless selective: excluding the Fuel and Light group does not remove every item influenced by energy costs. We therefore report exactly what is retained, and use the food-only comparison to separate the assignment's question from our broader operational definition. A label alone would not make these baskets equivalent.

Quarterly levels average all three monthly indices.'''),
('Pearson correlation measures linear association.', '''The standard deviation uses the squared distance of each observation from the sample mean, divided by one less than the number of observations, before taking the square root. Squaring gives a large observation more influence than the median does. Skewness and kurtosis go further by using third and fourth powers of deviations. They are useful warning signals about unusual observations, but can themselves be unstable in a short sample. We therefore read them with the actual plotted observations rather than classify the data from a single cutoff. An extreme value is checked against its source before being treated as either a genuine event or an error; statistical influence alone is not grounds for correcting it.

Pearson correlation measures linear association.'''),
('For annual inflation, headline and core standard deviations are close:', '''The same arithmetic checks the reported spread: the unemployment squared deviations sum to 231.5667, giving $s_U=\\sqrt{231.5667/26}=2.9844$. The median is the fourteenth ordered observation, 8.3. These summaries agree with the concentration visible in the plot.

For annual inflation, headline and core standard deviations are close:'''),
('These correlations should be read within the observed period.', '''Correlation standardises the covariance by both series' standard deviations. A regression slope instead keeps the original units. In this simple model their link is $\\hat\\beta=r(s_\\pi/s_U)$. Thus a smaller inflation standard deviation can change the slope even when correlation is unchanged. Comparing both summaries helps distinguish the direction of association from the scale of the price movements.

These correlations should be read within the observed period.'''),
('The smaller Urban food weight helps explain the lower Urban allocation,', '''A component with a steady positive contribution can raise average headline inflation while explaining little of its variability. Conversely, a contribution that swings above and below its mean can receive a large variance share. The covariance formula captures those swings and their alignment with the total. For this reason, our shares should not be read as a breakdown of the average inflation rate, or as the percentage contribution to an individual month's price increase.

The smaller Urban food weight helps explain the lower Urban allocation,'''),
('An earlier 90.59\\% estimate uses a reconstructed', '''The checks serve different purposes. Complete dates establish coverage; published anchors establish source agreement; the residual establishes arithmetic reconciliation. Agreement across these checks is more persuasive than relying on a successful download or a single headline match.

An earlier 90.59\\% estimate uses a reconstructed''')]
for anchor,replacement in additions:
 assert anchor in s,anchor
 s=s.replace(anchor,replacement,1)
# Tighter captions retain the interpretation in the surrounding text.
replacements={
'Matched Urban series, 2018Q2--2024Q4. Inflation is the log change in quarterly-average CPI over the same quarter a year earlier. Shading marks 2020--2021.':'Matched Urban unemployment and YoY log inflation, 2018Q2--2024Q4. Shading marks 2020--2021.',
'Observed distributions. Boxes show the interquartile range and median; dots show every observation. H denotes headline and C denotes operational core. The q/q rates are seasonally adjusted and annualised.':'Observed distributions. Boxes show quartiles and medians; dots show all observations. H: headline; C: core; q/q: seasonally adjusted annualised inflation.',
'Pearson correlations for year-on-year inflation. Both panels use identical variable definitions; only the fixed pandemic exclusion changes. Diagonal entries equal one by construction.':'YoY Pearson correlations: full and fixed-exclusion samples. U denotes unemployment. All correlations use matched rows.',
'Inflation--unemployment scatter plots and OLS fits. Diamonds identify the three excluded pandemic quarters. Dashed exclusion fits are drawn only over unemployment values observed in that sample. Rows use different inflation transformations.':'Matched inflation--unemployment observations and OLS fits. Diamonds mark excluded quarters; dashed fits use only the exclusion sample\'s observed unemployment range.',
'Direct slope differences and nominal HC3 ranges. Negative values would favour a more negative core slope; all four point estimates are positive. The ranges are sensitivity summaries, not calibrated guarantees.':'Core-minus-headline slopes and nominal HC3 ranges. Negative values favour a more negative core slope. All four estimates are positive.',
'Influence checks. Panel A allocates centred unemployment variation across quarters. Panel B refits each regression after omitting one quarter; every positive core estimate remains above the dotted zero line.':'Influence checks: centred unemployment variation (A) and leave-one-quarter-out slopes (B). Every core slope remains positive.',
'Food allocations and descriptive 12-month moving-block ranges, using 4,999 draws. Bars use official raw headline inflation. The longer annual ranges reflect uncertainty in a sample with overlapping changes.':'Food allocations to official raw headline variance; descriptive 12-month moving-block ranges use 4,999 draws.',
'Monthly official headline inflation and additive contributions. The shaded area contains all contributions other than food, including the aggregation residual. Raw changes retain seasonality because they answer the official-headline accounting question.':'Official monthly headline inflation and food contributions. Shading combines all other contributions and the residual; raw changes retain seasonality.',
'Different spillover summaries. Blue estimates sum delayed lags 1--3; rust estimates also include the current-month coefficient. All bars show nominal HC3 ranges. The two quantities should not be treated as the same effect.':'Delayed and current-plus-delayed food coefficients with nominal HC3 ranges. Blue excludes the current month; rust includes it.'
}
for a,b in replacements.items():assert a in s,a;s=s.replace(a,b)
s=s.replace('\\setlength{\\tabcolsep}{5pt}','\\setlength{\\tabcolsep}{5pt}\n\\setlength{\\intextsep}{8pt plus 2pt minus 2pt}\n\\setlength{\\textfloatsep}{8pt plus 2pt minus 2pt}')
s=s.replace('log inflation, $100\\ln(\\bar I_q/\\bar I_{q-4})$. Urban headline means','log inflation, $100\\ln(\\bar I_q/\\bar I_{q-4})$.\nUrban headline means')
s=s.replace('an imputation-exposed monthly change','an imputation-exposed monthly change')
p.write_text(s)
p=Path('make_figures.py');f=p.read_text().replace("figsize=(6.8,2.0)","figsize=(6.8,1.75)").replace("figsize=(6.8,2.55),gridspec_kw={'width_ratios':[1.1,1]}","figsize=(6.8,2.25),gridspec_kw={'width_ratios':[1.1,1]}").replace("figsize=(6.8,2.3)","figsize=(6.8,1.8)")
f=f.replace("xticklabels=names,yticklabels=names", "xticklabels=['U','Headline','Core'],yticklabels=['U','Headline','Core']")
p.write_text(f)
p=Path('make_tables.py');t=p.read_text().replace("f'{r[k]:.2f}'", "f'{0 if abs(r[k])<.005 else r[k]:.2f}'").replace('Nine numerical table files','Eight numerical table files')
p.write_text(t)
