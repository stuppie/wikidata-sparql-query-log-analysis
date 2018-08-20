#!/usr/bin/env python3
"""
unquote.py
Reads from stdin
Input: url encoded string
Output: decoded string with newlines replaced with tabs
"""
import sys
from urllib.parse import unquote_plus
for line in sys.stdin:
    line = unquote_plus(line)
    line = line.replace("\n", "\t")
    print(line, file=sys.stdout)
