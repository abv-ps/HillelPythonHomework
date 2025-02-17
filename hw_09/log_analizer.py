"""
This module processes a web server log file, extracting information about client requests.

It contains functions to:
1. Parse individual log lines to extract the IP address, HTTP method, and status code.
2. Analyze an entire log file and count occurrences of each unique combination
of IP address, HTTP method, and status code.
3. Print the statistics showing how many times each unique log entry appeared.

Functions:
- parse_log_line(line: str) -> Tuple[str, str, str] | None:
    Parses a single log line to extract the IP address, HTTP method, and status code.
- analyze_log(file_path: str) -> Dict[Tuple[str, str, str], int]:
    Analyzes the log file and counts occurrences of unique
    (IP, HTTP method, status code) combinations.
- print_statistics(stats: Dict[Tuple[str, str, str], int]) -> None:
    Prints the statistics of the log entries.

Usage:
    The user can provide a path to a web server log file, and the script will analyze it,
    printing the count of each unique log entry combination.
"""

import re
from collections import Counter
from typing import Tuple, List, Dict

# Regular expression to extract IPv4 addresses and HTTP request details
IP_PATTERN = r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})'
LOG_PATTERN = re.compile(rf'({IP_PATTERN}) .*? "(\w+) .*?" (\d+)')


def parse_log_line(line: str) -> Tuple[str, str, str] | None:
    """
    Parses a single log line and extracts the IP address, HTTP method, and status code.

    Args:
        line (str): A line from the log file.

    Returns:
        Tuple[str, str, str] | None: A tuple containing (IP, HTTP method, status code),
        or None if no match found.

    Examples:
        >>> parse_log_line('192.168.1.1 - - [10/Feb/2025:13:55:36 +0000] '
    ...                     '"GET /index.html HTTP/1.1" 200 1024')
        ('192.168.1.1', 'GET', '200')
    """
    match = LOG_PATTERN.search(line)
    return (match.group(1), match.group(6), match.group(7)) if match else None


def analyze_log(file_path: str) -> Dict[Tuple[str, str, str], int]:
    """
    Analyzes a web server log file and counts occurrences of (IP, HTTP method, status code) tuples.

    Args:
        file_path (str): Path to the log file.

    Returns:
        Dict[Tuple[str, str, str], int]: A dictionary mapping tuples
        (IP, HTTP method, status code) to their counts.
    """
    entries: List[Tuple[str, str, str]] = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parsed = parse_log_line(line)
            if parsed:
                entries.append(parsed)

    return Counter(entries)


def print_statistics(stats: Dict[Tuple[str, str, str], int]) -> None:
    """
    Prints the statistics of log entries.

    Args:
        stats (Dict[Tuple[str, str, str], int]): Dictionary with log entry counts.
    """
    for entry, count in stats.items():
        print(f"{entry}: {count} {'time' if count == 1 else 'times'}")


if __name__ == "__main__":
    LOG_FILE_PATH = "access_log_20240925_2.log"
    statistics = analyze_log(LOG_FILE_PATH)
    print_statistics(statistics)
