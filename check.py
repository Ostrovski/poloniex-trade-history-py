#!/usr/bin/env python

import json
import heapq
import sys


def check(filename):
    gaps = []
    lookahead = []
    lookahead_capacity = 100
    min_trade_id = None
    with file(filename) as f:
        for line in f:
            record = json.loads(line)
            trade_id = record['tradeID']

            if len(lookahead) < lookahead_capacity:
                heapq.heappush(lookahead, -trade_id)

            if len(lookahead) == lookahead_capacity:
                while (lookahead and min_trade_id == -lookahead[0] + 1) or min_trade_id is None:
                    min_trade_id = -heapq.heappop(lookahead)

                if len(lookahead) == lookahead_capacity:
                    gaps.append((min_trade_id, -lookahead[0]))
                    min_trade_id = -heapq.heappop(lookahead)

            assert len(lookahead) < lookahead_capacity

    while lookahead:
        if min_trade_id == -lookahead[0] + 1:
            min_trade_id = -heapq.heappop(lookahead)
        else:
            gaps.append((min_trade_id, -lookahead[0]))
            min_trade_id = -heapq.heappop(lookahead)

    return gaps


def main(filename):
    gaps = check(filename)
    if gaps:
        print('Found %s gaps:' % len(gaps))
        print([' -> '.join(map(str, g)) for g in gaps])
    else:
        print('Looks good!')


if __name__ == '__main__':
    main(sys.argv[1])
