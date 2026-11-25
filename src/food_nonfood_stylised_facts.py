"""Compatibility wrapper for the corrected descriptive analysis.

The original Stage-1 version generated iid-style inference on overlapping YoY
series and a circular YoY bootstrap. Those outputs are archived and deprecated.
Run the corrected script instead; this wrapper delegates to it.
"""
from corrected_descriptive_analysis import main

if __name__ == "__main__":
    main()
