"""
Reads queries from stdin, only print if they contain `match_id`

"""

import sys
import re
from urllib.parse import unquote_plus
from tqdm import tqdm

match_id = sys.argv[1]


if "|" not in match_id:
    re_compile = re.compile("<http://www.wikidata.org/[^>]*?({}.*?)>".format(match_id))

    for line in tqdm(sys.stdin):
        query, sourceCategory, user_agents, count = line.strip().split("\t")
        query = unquote_plus(query).replace("\n", "\t")
        p = re_compile.findall(query)
        if p:
            print(query, sourceCategory, user_agents, count)
else:
    match_ids = match_id.split("|")
    for line in tqdm(sys.stdin):
        query, sourceCategory, user_agents, count = line.strip().split("\t")
        query = unquote_plus(query).replace("\n", "\t")

        p = re.findall("<http://www.wikidata.org/[^>]*?({}.*?)>".format(match_id[0]), query)
        if p and all(pp in p for pp in match_ids):
            print(query, sourceCategory, user_agents, count)