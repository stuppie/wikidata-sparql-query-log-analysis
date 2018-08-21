#!/usr/bin/env bash

./download.sh

# sort all queries (208 million)
# requires a lot of tmp space
sort -k1,1 -s <(zcat data/2017-06-12_2017-07-09_all.tsv.gz) <(zcat data/2017-07-10_2017-08-06_all.tsv.gz) <(zcat data/2017-08-07_2017_09_03_all.tsv.gz) |
    gzip > data/2017-678_sort.tsv.gz

# groupby query, concatenate other columns, keep count
zcat data/2017-678_sort.tsv.gz | python3 groupby.py | gzip > data/2017-678_uniq.tsv.gz
# end up with 35 million unique queries

# top user-agents
zcat data/2017-06-12_2017-07-09_all.tsv.gz data/2017-07-10_2017-08-06_all.tsv.gz data/2017-08-07_2017_09_03_all.tsv.gz |
tail -n +2 | cut -f4 | sort | uniq -c | sort -nr > top_ua.txt

# unquote (change from url-encoded to plain text), and toss the header and other columns
zcat data/2017-678_uniq.tsv.gz | tail -n +2 | cut -f1 | python3 unquote.py | gzip > data/2017-678_uniq_query.tsv.gz

# get counts of most used entities
zcat data/2017-678_uniq_query.tsv.gz | python3 count_entities.py P > prop_count.txt
zcat data/2017-678_uniq_query.tsv.gz | python3 count_entities.py Q > item_count.txt

# calculate co-occurence of items (appearing in the same sparql query)
zcat data/2017-678_uniq_query.tsv.gz | python3 calculate_cooccurence.py P > cooccurence_P.txt
zcat data/2017-678_uniq_query.tsv.gz | python3 calculate_cooccurence.py Q > cooccurence_Q.txt