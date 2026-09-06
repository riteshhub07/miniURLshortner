# Mini URL Shortener (CLI)

A simple command-line tool that shortens long URLs into short codes and resolves them back to the original URL — built entirely with Python's standard library, with data persisted locally in a JSON file.

## Features

- Shorten a URL into a randomly generated short code
- Optional custom alias support (`--alias`)
- Resolve a short code back to its original URL
- Tracks the number of times each code has been resolved (click count)
- List all shortened URLs created so far
- Data persists across runs (stored in `data.json`)
- Handles invalid URLs, duplicate aliases, and missing codes gracefully

## Requirements

- Python 3.x
- No external packages needed — standard library only (`json`, `os`, `random`, `string`, `argparse`, `urllib.parse`)

## How to Run

Clone this repo and run commands from the project folder using:

```
python main.py <command> [arguments]
```

### Shorten a URL

```
python main.py shorten https://google.com
```
Output:
```
Shortened URL: https://google.com -> WDxU8M
```

### Shorten with a custom alias

```
python main.py shorten https://youtube.com --alias yt
```
Output:
```
Shortened URL: https://youtube.com -> yt
```

### Resolve a short code

```
python main.py resolve yt
```
Output:
```
Original URL: https://youtube.com
(resolved 1 times)
```

### List all shortened URLs

```
python main.py list
```
Output:
```
WDxU8M -> https://google.com (clicks: 0)
yt -> https://youtube.com (clicks: 1)
```

## Error Handling Examples

Invalid URL:
```
python main.py shorten hello
Error: The url 'https://hello' is not valid!
```

Duplicate alias:
```
python main.py shorten https://youtube.com --alias yt
Error: alias 'yt' is already taken!
```

Missing/unknown code:
```
python main.py resolve doesnotexist
Error: code 'doesnotexist' not found.
```

## Design Notes

- If a URL is entered without `http://` or `https://` (e.g. `google.com`), the tool automatically assumes `https://` before validating and storing it.
- A URL is only accepted if it has both a scheme (e.g. `https`) and a domain that contains a dot (e.g. `google.com`). This rejects obviously invalid input like `hello`, though it is a basic check and not a guarantee that the domain actually exists or is reachable.
- Data is stored locally in `data.json` in the same directory as `main.py` — delete this file to reset all stored data.
- Duplicate aliases are rejected rather than overwritten, to avoid accidentally destroying an existing mapping.
- Short codes are generated randomly (6 characters, letters + digits) and checked against existing codes to avoid collisions.

## Author

Ritesh Kumar
NSUT, CSAI-1, 1st Year
