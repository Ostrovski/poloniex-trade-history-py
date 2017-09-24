# Poloniex Trade History grabber

## Usage
```
python grab.py --help
usage: [--file </path/to/file.json>] <currency_pair> <start> [end]

grab trade history from poloniex.com

positional arguments:
  currency_pair         BTC_ETH, or ETH_XRP, or ...
  start_at              ISO time string
  end_at                ISO time string (optional)

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  the file where the history should be written
```

## Verify grabbed data
Trade history records are indexed by `tradeID`. Command `check.py` performs sequential analyze of
grabbed JSON file and detects gaps in the `tradeID`s.

```
python check.py </path/to/file.json>
```

## Examples
Grab BTC_XRP history since `2017-09-15 UTC` to `foobar.json`:
```
python grab.py btc_xrp 2017-09-15T00:00:00 -f foobar.json
python check.py foobar.json
```

## TODO
Poloniex provides trade history data in reverse order. Need script to revert grabbed data on disk.
Now you can do the trick via `tail -r foobar.json`.

## Author
Ivan Velichko <iximiuz@gmail.com>
