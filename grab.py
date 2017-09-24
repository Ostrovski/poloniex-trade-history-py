#!/usr/bin/env python

import argparse
import json
import sys
import time
import urllib
from datetime import datetime, timedelta, tzinfo


def grab_history(currency_pair, start_at, end_at, fil, api_url='https://poloniex.com/public'):
    min_global_trade_id = None
    while start_at < end_at:
        chunk_start_at, chunk_end_at = create_chunk_period(start_at, end_at)
        print(chunk_start_at, chunk_end_at)
        req = create_request(api_url, currency_pair, chunk_start_at, chunk_end_at)

        # chuck is sorted by time desc
        chunk = http_get_json(req)
        print('chunk: %s record(s)' % len(chunk))
        if len(chunk) > 0:
            print(chunk[0])
        if len(chunk) > 1:
            print(chunk[-1])

        if chunk and min_global_trade_id is not None:
            chunk = [x for x in chunk if x['globalTradeID'] < min_global_trade_id]

        if chunk:
            lines = [json.dumps(x) + u'\n' for x in chunk]
            fil.writelines(lines)
            min_global_trade_id = chunk[-1]['globalTradeID']
            end_at = parse_dt(chunk[-1]['date'])
        else:
            end_at = chunk_start_at


def create_chunk_period(start_at, end_at):
    return max(start_at, end_at - timedelta(30)), end_at


def create_request(api_url, currency_pair, start_at, end_at):
    return api_url + '?command=returnTradeHistory&currencyPair=%s&start=%s&end=%s' \
                     % (currency_pair, int(timestamp(start_at)), int(timestamp(end_at)))


def http_get_json(url):
    return json.loads(fetch(url))


def fetch(url):
    print('HTTP GET ' + url)
    try:
        response = urllib.urlopen(url)
        return response.read()
    finally:
        print('got!')


def parse_dt(dt):
    dt = dt.replace('T', ' ')
    return datetime(*(time.strptime(dt, '%Y-%m-%d %H:%M:%S')[0:6]), tzinfo=UTC())


def timestamp(dt):
    return (dt - EPOCH).total_seconds()


class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0) + self.dst(dt)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return 'UTC+00'


EPOCH = datetime(1970, 1, 1, tzinfo=UTC())


def main(currency_pair, start_at, end_at=None, filename=None):
    currency_pair = currency_pair.upper()
    start_at = parse_dt(start_at)
    end_at = parse_dt(end_at) if end_at else datetime.now(UTC())
    out = file(filename, 'w') if filename else sys.stdout

    try:
        grab_history(currency_pair, start_at, end_at, out)
    finally:
        if out != sys.stdout:
            out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='poloniex-trade-history',
        usage='[--file </path/to/file.json>] <currency_pair> <start> [end]',
        description='grab trade history from poloniex.com')
    parser.add_argument('currency_pair', help='BTC_ETH, or ETH_XRP, or ...')
    parser.add_argument('start_at', help='ISO time string')
    parser.add_argument('end_at', help='ISO time string (optional)', nargs='?', default=None)
    parser.add_argument('-f', '--file', help='the file where the history should be written',
                        default=None)
    args = parser.parse_args()
    main(args.currency_pair, args.start_at, end_at=args.end_at, filename=args.file)
