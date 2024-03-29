# python-fit-downloader

## Dependencies

### mtpy

https://github.com/ldo/mtpy

Got the file `mtpy.py` from there, changed the lines for macOS:

```
29    mtp = ct.cdll.LoadLibrary("libmtp.so.9")
29    mtp = ct.cdll.LoadLibrary("libmtp.dylib")

54    libc = ct.cdll.LoadLibrary("libc.so.6")
54    libc = ct.cdll.LoadLibrary("libSystem.dylib")
```

Note: I also tried https://github.com/emdete/python-mtp and couldnt't get it to run.

### libmtp

Installed `libmtp` via brew:

```bash
brew install libmtp
```

Copied the dylib into the script directory, I suppose linking it to an expected place would also work:

```bash
cp /opt/homebrew/Cellar/libmtp/1.1.20/lib/libmtp.dylib .
```

## Usage

Running it to list and download activitiy `*.fit` files:

```bash
cd python-fit-downloader
python download.py

# Device 0 (VID=091e and PID=4cd8) is a Garmin Fenix 6S Pro/Sapphire.
# Downloading 2023-03-13-18-23-31.fit 86.9 KiB
```

Target file path: `python-fit-downloader/activities/2023/2023-03-13-18-23-31.fit`

## Alias

Put the following into your `.zshrc`:

```
alias fitdl='cd "/Users/guenther/Development/private/python-fit-downloader/" && python download.py && cd -'
```
