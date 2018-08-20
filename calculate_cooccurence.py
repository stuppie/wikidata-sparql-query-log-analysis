#!/usr/bin/env python3
"""
calculate_cooccurence.py
Usage: cat "xxx" | calculate_cooccurence.py {Q,P}
Input: each line is a unquoted query
"""

import sys
import re
from collections import defaultdict, Counter
from itertools import combinations

from tqdm import tqdm

match_char = sys.argv[1].strip()
assert match_char in {'Q', 'P'}

# store count of cooccurence of terms
# key is a tuple of sorted IDs, value is count of co-occurrance in the same query
d = defaultdict(int)

for line in tqdm(sys.stdin):
    # Matches PIDs or QIDs, outputing all matched IDs from the same line, in the same line
    p = re.findall("<http://www.wikidata.org/[^>]*?({}.*?)>".format(match_char), line)
    # get all pairwise combinations of these IDs
    pairs = list(combinations(p, 2))
    for pair in pairs:
        d[tuple(sorted(pair))] += 1

mc = Counter(dict(d)).most_common()

for k, v in mc:
    print(",".join(k) + "\t" + str(v))
