"""
count_entities.py
Parses sparql query log files to generate usage stats on items and properties
Reads from stdin. expects 4 columns: query, sourceCategory, user_agent, count

Usage: python3 count_entities.py entity_type r out_file_name.csv
where the first argument is Q or P, for items or properties
`r` is the r-length to use to generate combinations of elements.
    1 means single usage, 2 means co-occurance of 2 items within the same query, etc..

"""

"""
Note: to do the search with grep
grep -Po "<http://www.wikidata.org/[^>]*?(P.*?)>" | grep -oEi 'P[0-9]+'

# parallel
zcat data/2017-678_uniq.tsv.gz| parallel --pipe --block 10M python3 unquote.py | grep -P "<http://www.wikidata.org/[^>]*?P699>"
"""

import sys
import re
from collections import defaultdict
from itertools import combinations
from urllib.parse import unquote_plus
import pandas as pd
from tqdm import tqdm

MATCH_CHAR = sys.argv[1].strip()
assert MATCH_CHAR in {'Q', 'P'}
COMBS = int(sys.argv[2].strip())
OUT_FILE_NAME = sys.argv[3]
CUTOFF = 10

unique_count = defaultdict(int)
total_count = defaultdict(int)
user_agent_count = defaultdict(lambda: defaultdict(int))
user_agent_total_count = defaultdict(lambda: defaultdict(int))
sourceCategory_count = defaultdict(lambda: defaultdict(int))
sourceCategory_total_count = defaultdict(lambda: defaultdict(int))

re_compile = re.compile("<http://www.wikidata.org/[^>]*?({}[0-9]+?)>".format(MATCH_CHAR))

for line in tqdm(sys.stdin):
    query, sourceCategory, user_agents, count = line.split("\t")
    query = unquote_plus(query).replace("\n", "\t")
    count = int(count)
    user_agents = user_agents.split(",")

    # Matches PIDs or QIDs, outputing all matched IDs from the same line, in the same line
    p = re_compile.findall(query)
    # get all pairwise combinations of these IDs
    pairs = list(combinations(p, COMBS))
    for pair in pairs:
        pp = "|".join(sorted(pair))
        unique_count[pp] += 1
        total_count[pp] += count
        sourceCategory_count[sourceCategory][pp] += 1
        sourceCategory_total_count[sourceCategory][pp] += count
        for user_agent in user_agents:
            user_agent_count[user_agent][pp] += 1
            user_agent_total_count[user_agent][pp] += count

# this runs out of memory if we keep everything (for items, props are ok).
# toss items with count < CUTOFF
unique_count = {k: v for k, v in unique_count.items() if v >= CUTOFF or total_count[k] >= CUTOFF}
total_count = {k: v for k, v in total_count.items() if v >= CUTOFF or unique_count.get(k, 0) >= CUTOFF}
# filter these items out of sourceCategory and user_agent also
keep_items = set(total_count.keys())
do_filter = lambda d: {k: {kk: vv for kk, vv in v.items() if kk in keep_items} for k, v in d.items()}
sourceCategory_count = do_filter(sourceCategory_count)
sourceCategory_total_count = do_filter(sourceCategory_total_count)
user_agent_count = do_filter(user_agent_count)
user_agent_total_count = do_filter(user_agent_total_count)

# build df
unique_df = pd.DataFrame.from_dict(unique_count, columns=['unique'], orient="index")
total_df = pd.DataFrame.from_dict(total_count, columns=['total'], orient="index")

user_agent_count_df = pd.DataFrame(user_agent_count)
user_agent_total_count_df = pd.DataFrame(user_agent_total_count)
sourceCategory_count_df = pd.DataFrame(sourceCategory_count)
sourceCategory_total_count_df = pd.DataFrame(sourceCategory_total_count)

user_agent_total_count_df.rename(columns={c: c + "__total" for c in user_agent_total_count_df.columns}, inplace=True)
sourceCategory_total_count_df.rename(columns={c: c + "__total" for c in sourceCategory_total_count_df.columns},
                                     inplace=True)

df = unique_df.join(total_df)
df = df.join(sourceCategory_count_df)
df = df.join(sourceCategory_total_count_df)
df = df.join(user_agent_count_df)
df = df.join(user_agent_total_count_df)

df.sort_values(["unique", "total"], inplace=True, ascending=False)
df.to_csv(OUT_FILE_NAME)
