#!/usr/bin/env bash

./download.sh

# unquote (change from url-encoded to plain text), and toss the header and other columns
zcat data/2017-06-12_2017-07-09_all.tsv.gz | tail -n +2 | cut -f1 | python3 unquote.py | gzip > data/2017-06-12_2017-07-09_all_uq.tsv.gz
zcat data/2017-07-10_2017-08-06_all.tsv.gz | tail -n +2 | cut -f1 | python3 unquote.py | gzip > data/2017-07-10_2017-08-06_all_uq.tsv.gz
zcat data/2017-08-07_2017_09_03_all.tsv.gz | tail -n +2 | cut -f1 | python3 unquote.py | gzip > data/2017-08-07_2017_09_03_all_uq.tsv.gz

# deduplicate queries
# this goes from ~60 million queries to ~8 million (first file)
zcat data/2017-06-12_2017-07-09_all_uq.tsv.gz | uniq | sort -u | gzip > data/2017-06-12_2017-07-09_uniq.tsv.gz
zcat data/2017-07-10_2017-08-06_all_uq.tsv.gz | uniq | sort -u | gzip > data/2017-07-10_2017-08-06_uniq.tsv.gz
zcat data/2017-08-07_2017_09_03_all_uq.tsv.gz | uniq | sort -u | gzip > data/2017-08-07_2017_09_03_uniq.tsv.gz

# get the counts of the most common queries
# not actually using this for anything, just to get a feel of the scope of the most duplicated queries
zcat data/2017-06-12_2017-07-09_all_uq.tsv.gz | sort -S 1000000 | uniq -cd | sort -nr | head -n100 > 2017-06-12_2017-07-09_top.tsv
# top query was performed 3.2 million times (identical, not counting anonymized strings) some sort of musicbrainz query

# merge uniq queries into one file
zcat data/*_uniq.tsv.gz | gzip > data/2017-678_uniq.tsv.gz

# get counts of the most common properties
zcat data/2017-678_uniq.tsv.gz | grep -Po "<http://www.wikidata.org/[^>]*?>" | grep -Po "P[^>]*" |
sort | uniq -c | sort -nr > prop_count_6.txt

# get counts of the most common items
zcat data/2017-678_uniq.tsv.gz | grep -Po "<http://www.wikidata.org/[^>]*?>" | grep -Po "Q[^>]*" |
sort | uniq -c | sort -nr > item_count.txt


# calculate co-occurence of items (appearing in the same sparql query)
zcat data/2017-678_uniq.tsv.gz | python3 calculate_cooccurence.py P > cooccurence_P.txt
zcat data/2017-678_uniq.tsv.gz | python3 calculate_cooccurence.py Q > cooccurence_Q.txt