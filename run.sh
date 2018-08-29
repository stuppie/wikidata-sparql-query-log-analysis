#!/usr/bin/env bash

./download.sh

# sort all queries (208 million)
# requires a lot of tmp space (~120gb), and ~3 hours
sort -k1,1 -s <(zcat data/2017-06-12_2017-07-09_all.tsv.gz) <(zcat data/2017-07-10_2017-08-06_all.tsv.gz) <(zcat data/2017-08-07_2017_09_03_all.tsv.gz) |
    gzip > data/2017-678_sort.tsv.gz

# groupby query, concatenate other columns, keep count
zcat data/2017-678_sort.tsv.gz | python3 groupby.py | gzip > data/2017-678_uniq.tsv.gz
# end up with 35 million unique queries

# top user-agents
zcat data/2017-06-12_2017-07-09_all.tsv.gz data/2017-07-10_2017-08-06_all.tsv.gz data/2017-08-07_2017_09_03_all.tsv.gz |
tail -n +2 | cut -f4 | sort | uniq -c | sort -nr > top_ua.txt

# get counts of most used entities
zcat data/2017-678_uniq.tsv.gz | python3 count_entities.py P 1 prop_count.csv
zcat data/2017-678_uniq.tsv.gz | python3 count_entities.py Q 1 item_count.csv

# calculate co-occurence of items (appearing in the same sparql query)
zcat data/2017-678_uniq.tsv.gz | python3 count_entities.py P 2 prop_2_count.csv
zcat data/2017-678_uniq.tsv.gz | python3 count_entities.py Q 2 item_2_count.csv
