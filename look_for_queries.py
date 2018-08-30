"""
Reads queries from stdin, only print if they contain `match_id`

"""

import sys
import re
from urllib.parse import unquote_plus
from tqdm import tqdm

match_id = sys.argv[1]

re_compile = re.compile("<http://www.wikidata.org/[^>]*?({}.*?)>".format(match_id))

for line in tqdm(sys.stdin):
    query, sourceCategory, user_agents, count = line.strip().split("\t")
    query = unquote_plus(query).replace("\n", "\t")
    p = re_compile.findall(query)
    if p:
        print(query, sourceCategory, user_agents, count)
