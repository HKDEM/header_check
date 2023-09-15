# HTTP Header Checker

HTTP Header Checker is a Python script designed to check the HTTP response headers of a target URL or IP address. It helps you identify security vulnerabilities and misconfigurations in the HTTP response headers of a web server. The script checks various headers, such as Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Public-Key-Pins, and Content-Security-Policy (CSP), and provides insights into their configurations.

## Features

- Shows all avaliable response headers of the given target.
- Checks various HTTP headers for security misconfigurations when searched spesificly.
- Provides detailed information about security risks and solutions.
- Supports checking specific headers or all headers.
- Offers color-coded output for easy interpretation.

## Prerequisites

Before running the script, ensure that you have the required Python libraries installed:

- `argparse`: For parsing command-line arguments.
- `requests`: For making HTTP requests to the target.
- `termcolor`: For coloring the output.

You can install these libraries using `pip`:

```bash
pip install argparse requests termcolor
```

## Usage

You can run the script by executing the following command:

```bash
python header_checker.py [target] [-header HEADER [HEADER ...]]
```

- 'target': The URL or IP address of the target server you want to analyze.

- '-header HEADER [HEADER ...]': (Optional) Specify which response headers to check. You can provide one or more header names separated by spaces. For example,
-header X-Frame-Options X-XSS-Protection checks only the specified headers, while not using this option checks all available headers.

## Example Usage

1. Check all available headers for a target:

```bash
python header_checker.py example.com
```

2. Check specific headers for a target:   

```bash
python header_checker.py example.com -header X-Frame-Options X-XSS-Protection
```
## Output

- Red: High severity (security risk).
- Yellow: Medium severity (potential risk).
- Green: Low severity (recommendation).
- Blue: No security risks identified (properly configured).
