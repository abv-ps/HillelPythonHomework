"""
This module provides a function to extract all URLs from a given text.

A URL is defined as a string that starts with 'http://', 'https://', or 'www.' followed by any characters
that form a valid URL structure (e.g., domain name, path, query parameters).

The function uses a regular expression to identify and extract URLs from the input text.

Functions:
    extract_urls(text: str) -> List[str]:
        Extracts all URLs from the input text.
"""
import re
from typing import List


def extract_urls(text: str) -> List[str]:
    """
    Extracts all URLs from the given text.

    A URL is defined as a string that starts with 'http://', 'https://', or 'www.' followed by any
    characters that form a valid URL structure (e.g., domain name, path, query parameters).

    Args:
        text (str): The input text from which URLs will be extracted.

    Returns:
        List[str]: A list of URLs found in the text.

    Example:
        >>> extract_urls("Visit our website at https://www.example.com "
        ...              "and our support page at http://support.example.com.")
        ['https://www.example.com', 'http://support.example.com']
    """
    pattern = r'(https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9&%_/.-]*)?)|(www\.[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9&%_/.-]*)?)'

    urls = re.findall(pattern, text)

    return [url[0] or url[1] for url in urls]


text = "Visit our website at https://www.example.com and our support page at http://support.example.com."
urls = extract_urls(text)
print(urls)
