import sys
import re
from collections import defaultdict, Counter

match_char = sys.argv[1].strip()
assert match_char in {'Q', 'P'}

d = defaultdict(int)
for line in sys.stdin:
    # Matches PIDs or QIDs, outputing all matched IDs from the same line, in the same line
    p = re.findall("<http://www.wikidata.org/[^>]*?({}.*?)>".format(match_char), line)
    for pp in p:
        d[pp] += 1

mc = Counter(dict(d)).most_common()

for k, v in mc:
    print(k + "\t" + str(v))
