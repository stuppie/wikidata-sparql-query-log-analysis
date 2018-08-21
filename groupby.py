"""
Input: original sparql query log file (e.g. 2017-06-12_2017-07-09_all.tsv.gz), SORTED by query
groupby query, distinct values other columns, add a column at the end with the count
"""

from itertools import groupby
import sys

i = map(lambda x: x.split("\t"), sys.stdin)
f = lambda s: s.strip().replace(",", ";")
for key, gb in groupby(i, lambda x: x[0]):
    gb = [[f(xx) for xx in x[1:]] for x in gb]
    cols = list(zip(*gb))
    cols.pop(0)  # get rid of the times
    cols_str = "\t".join([",".join(set(col)) for col in cols]) + "\t" + str(len(gb))
    print("{}\t{}".format(key, cols_str))
