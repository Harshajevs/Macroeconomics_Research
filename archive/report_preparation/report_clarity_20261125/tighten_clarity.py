from pathlib import Path
p=Path('report.tex');s=p.read_text()
def paragraph(start,new):
 global s
 a=s.index(start);b=s.index('\n\n',a);s=s[:a]+new.strip()+s[b:]
paragraph('We first compare Urban headline and core inflation', '')
a=s.index('We begin with means, medians, sample standard deviations')
b=s.index('Pearson correlation measures linear association.',a)
s=s[:a]+r'''We report means, medians, sample SDs, skewness and excess kurtosis. The mean averages observations; the median is the middle ordered value. SD measures spread using $n-1$ in the variance denominator. Positive skewness indicates a longer upper tail; excess kurtosis describes tail weight relative to a normal distribution. We use bias-corrected moments. Since unusual observations strongly affect these measures, we inspect plots and check original sources rather than classify the data from a cutoff.

'''+s[b:]
paragraph('An earlier 90.59',r'''
An earlier 90.59\% uses a reconstructed seasonally adjusted aggregate. We use official raw headline throughout; Appendix~\ref{app:validation} explains the difference.
''')
paragraph('The calculation assigns food its own',r'''
Food's covariance with headline includes its own fluctuation and shared movement with other groups. The explicit residual keeps group contributions adding to the official rate. This is an accounting answer, rather than an identified causal food-shock effect.
''')
paragraph('Every group uses the same headline-variance',r'''
The common headline-variance denominator makes group shares comparable. Other groups and the residual receive 11.29\% jointly. Their smaller variance share does not measure their welfare importance or contribution to average inflation.
''')
# Condense optional technical details without removing any qualification of the findings.
a=s.index('The earlier 90.5899',s.index('\\section{Accounting and source checks}'))
s=s[:a]+r'''The earlier 90.5899\% uses a reconstructed seasonally adjusted aggregate. Independently adjusting General and each group assigns reconciliation residuals of 24.2410\% (Combined) and 25.0889\% (Urban), with food shares of 69.7544\% and 61.3913\%. These differ from our raw official-headline target.

PLFS corrections use Statement 5, printed p.~6 (PDF p.~9), in the two 2019 bulletins. Urban pan/tobacco is marked macro-imputed in April 2020, but not May; housing and fuel/light are unmarked in both months. Elementary imputation remains possible. Annual exclusions include April--May 2021 denominator exposure.

Calendar HAC respects quarter gaps; monthly simulations regenerate lagged outcomes. Block-wild null rejection ranges from 4.0--6.1\% for non-food and 4.3--7.1\% for core. A reverse relative-price sensitivity changes a joint tail from 0.0965 to 0.0341, confirming specification sensitivity rather than a causal direction.
\end{document}
'''
p.write_text(s)
