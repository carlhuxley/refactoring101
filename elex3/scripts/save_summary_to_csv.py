#!/usr/bin/env python
"""
This script leverages re-usable bits of code in the lib/ directory to
generate a summary CSV of election results.

USAGE:

    python save_summary_results_to_csv.py


OUTPUT:

    summary_results.csv containing racewide totals for each race/candidate pair.


"""
from os.path import dirname, join
import csv

from elex3.lib.summary import summarize
from elex3.lib.parser import parse_and_clean
from elex3.lib.scraper import download_results


def main():
    fname = 'fake_va_elec_results.csv'
    path = join(dirname(dirname(__file__)), fname)
    download_results(path)
    results = parse_and_clean(path)
    summary = summarize(results)
    write_csv(summary)


def write_csv(summary):
    """Generates CSV from summary election results data

    CSV is written to 'summary_results.csv' file in elex3/ directory.

    """
    outfile = join(dirname(dirname(__file__)), 'summary_results.csv')
    with open(outfile, 'wb') as fh:
        # Limit output to cleanly parsed, standardized values
        fieldnames = [
            'date',
            'office',
            'district',
            'last_name',
            'first_name',
            'party',
            'all_votes',
            'votes',
            'winner',
        ]
        writer = csv.DictWriter(fh, fieldnames, extrasaction='ignore', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for race, results in summary.items():
            cands = results.pop('candidates')
            for cand in cands:
                results.update(cand)
                writer.writerow(results)



if __name__ == '__main__':
    main()
