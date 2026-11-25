"""Export the primary regression and food-variance result tables."""
from pathlib import Path
import pandas as pd

RESULTS = Path(__file__).resolve().parents[1] / 'results'


def main():
    estimates = pd.read_csv(RESULTS / 'phillips_all_specifications.csv')
    primary = estimates[
        (~estimates.trend)
        & estimates.inference_sensitivity.eq('HC3')
        & estimates['sample'].isin(['full27', 'exclude_three_pandemic'])
    ]
    rows = []
    for (frequency, sample), group in primary.groupby(['frequency', 'sample']):
        group = group.set_index('outcome')
        difference = group.loc['core_food_fuel_excluded_minus_headline']
        rows.append({
            'frequency': frequency,
            'sample': sample,
            'n': int(difference.n),
            'headline_slope': group.loc['headline', 'slope'],
            'core_slope': group.loc['core_food_fuel_excluded', 'slope'],
            'core_minus_headline_slope': difference.slope,
            'nominal_HC3_difference_low': difference.ci_low,
            'nominal_HC3_difference_high': difference.ci_high,
        })
    pd.DataFrame(rows).to_csv(RESULTS / 'primary_phillips_comparison.csv', index=False)

    allocations = pd.read_csv(RESULTS / 'official_headline_variance_allocations.csv')
    food = allocations[
        allocations.component.eq('food_bev')
        & allocations['sample'].eq('full_history')
        & ~allocations.frequency.eq('MoM_STL7')
    ]
    food.to_csv(RESULTS / 'primary_food_variance_summary.csv', index=False)
    print('Exported primary regression comparisons and food-variance summary.')


if __name__ == '__main__':
    main()
