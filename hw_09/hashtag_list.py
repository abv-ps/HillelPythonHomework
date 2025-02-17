"""
This module provides a function to extract hashtags from a given text.
It uses regular expressions to find words that start with '#'
and contain only letters and numbers.
"""

import re
from typing import List


def extract_hashtags(text: str) -> List[str]:
    """
    Extracts hashtags from a given text. Hashtags are words that start with '#'
    and contain only letters and numbers (no special characters except letters and digits).

    Args:
        text (str): The input text from which hashtags will be extracted.

    Returns:
        List[str]: A list of hashtags without the '#' symbol.

    Example:
        >>> extract_hashtags("The most popular hashtags in Ukraine are: "
        ...                  "#Україна #Єдність #УкраїнськаМова #_ЗСУ")
        ['Україна', 'Єдність', 'УкраїнськаМова']
    """
    # Regular expression to find words that start with # and contain only letters and numbers
    hashtags = re.findall(r'(?<=#)(?!_)([A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ0-9]+)(?=\s|$|#)', text)
    return hashtags


if __name__ == "__main__":
    s = "The most popular hashtags in Ukraine are: #Україна #Єдність #УкраїнськаМова #_ЗСУ"
    tags = extract_hashtags(s)
    print(tags)
