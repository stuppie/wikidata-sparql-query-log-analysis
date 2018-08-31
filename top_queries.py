import sys
from urllib.parse import unquote_plus
import heapq

from tqdm import tqdm

k = 10
heap = []
for line in tqdm(sys.stdin):
    query, sourceCategory, user_agents, count = line.split("\t")
    count = int(count)
    if len(heap) < k or count > heap[0][0]:
        # If the heap is full, remove the smallest element on the heap.
        if len(heap) == k:
            heapq.heappop(heap)
        # add the current element as the new smallest.
        query = unquote_plus(query).replace("\n", "\t")
        heapq.heappush(heap, (count, query))

heap = heapq.nlargest(k, heap, lambda x: x[0])
for n in heap:
    print(n[0])
    print(n[1])
