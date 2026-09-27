"""Reproduce every table, figure, and reported value from the de-identified data.

    python analysis/run_all.py
"""
import quantitative
import qualitative
import figures

if __name__ == "__main__":
    quantitative.main()
    qualitative.main()
    figures.main()
    print("Done. Tables and numbers are in results/, figures in figures/.")
