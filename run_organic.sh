#!/usr/bin/env bash

# merge
zcat data/organic/* | gzip > data/organic/2017-678_organic.tsv.gz

# unquote (change from url-encoded to plain text), and toss the header and other columns
zcat data/organic/2017-678_organic.tsv.gz | tail -n +2 | cut -f1 | python3 unquote.py | gzip > data/organic/2017-678_organic_uq.tsv.gz

# deduplicate queries
# this goes from 637935 queries to 249846
zcat data/organic/2017-678_organic_uq.tsv.gz | uniq | sort -u -S 100000 | gzip > data/organic/2017-678_organic_uniq.tsv.gz

# get counts of most used entities
zcat data/organic/2017-678_organic_uniq.tsv.gz | python3 count_entities.py P > prop_count_organic.txt
zcat data/organic/2017-678_organic_uniq.tsv.gz | python3 count_entities.py Q > item_count_organic.txt

# calculate co-occurence of items (appearing in the same sparql query)
zcat data/organic/2017-678_organic_uniq.tsv.gz | python3 calculate_cooccurence.py P > cooccurence_P_organic.txt
zcat data/organic/2017-678_organic_uniq.tsv.gz | python3 calculate_cooccurence.py Q > cooccurence_Q_organic.txt