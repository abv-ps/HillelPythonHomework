"""
This module provides a function to remove HTML tags from a given text.
"""

import re


def remove_html_tags(text: str) -> str:
    """
    Removes all HTML tags from a given text using regular expressions.

    Args:
        text (str): The input text containing HTML tags.

    Returns:
        str: The text without any HTML tags.

    Example:
        >>> remove_html_tags('<p>Welcome to <b>my <i>website</i></b>! <i>This is a '
        ...                 '<a href="https://example.com">sample link</a>.</i></p> '
        ...                 '<p>Here is an <b><i>important</i> image link</b>: '
        ...                 '<a href="https://example.com/image.jpg">'
        ...                 '<img src="image.jpg" alt="An image" /></a></p>')
        'Welcome to my website! This is a sample link. Here is an important image link: '
    """
    return re.sub(r"</?[^>]+>", "", text) if text else ""


s = ('<p>Welcome to <b>my <i>website</i></b>! <i>This is a '
        '<a href="https://example.com">sample link</a>.</i></p> '
        '<p>Here is an <b><i>important</i> image link</b>: '
        '<a href="https://example.com/image.jpg">'
        '<img src="image.jpg" alt="An image" /></a></p>')

clean_text = remove_html_tags(s)
print(f"Cleaned text: {clean_text}" if clean_text else "Empty input or invalid text.")
