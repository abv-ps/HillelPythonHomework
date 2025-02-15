"""
This module provides a function to extract all valid IPv4 addresses from a given text.

An IPv4 address consists of four numbers (from 0 to 255), separated by periods.

The function uses regular expressions to find potential IP addresses and then filters
out any invalid ones (where any number is outside the range of 0-255).

Functions:
    extract_ipv4_addresses(text: str) -> List[str]:
        Extracts all valid IPv4 addresses from the input text.
"""

import re
from typing import List


def extract_ipv4_addresses(text: str) -> List[str]:
    """
    Extracts all IPv4 addresses from a given text.

    An IPv4 address consists of four numbers (from 0 to 255), separated by periods.

    Args:
        text (str): The input text that may contain IPv4 addresses.

    Returns:
        List[str]: A list of IPv4 addresses found in the text.

    Example:
    >>> extract_ipv4_addresses("The most popular IP addresses in Ukraine: 91.192.0.1, "
    ...                        "89.184.13.25, 354.13.52.4, 2001:0db8:85a3:0000:0000:8a2e:0370:7334, 213.87.98.255.")
    ['91.192.0.1', '89.184.13.25', '213.87.98.255']
    """
    pattern = r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})'

    ipv4_addresses = re.findall(pattern, text)

    valid_ipv4_addresses = [
        f"{a}.{b}.{c}.{d}" for a, b, c, d in ipv4_addresses
        if all(0 <= int(part) <= 255 for part in (a, b, c, d))
    ]

    return valid_ipv4_addresses


text = ("The most popular IP addresses in Ukraine: 91.192.0.1, 89.184.13.25, 354.13.52.4, "
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334, 213.87.98.255.")
ipv4_addresses = extract_ipv4_addresses(text)
print(ipv4_addresses)
