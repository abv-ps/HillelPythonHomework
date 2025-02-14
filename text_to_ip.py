import re


def text_to_ip(text: str) -> str | None:
    r: str = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    match = re.match(r, text)

    if match:
        return text
    return None


t = '1.2.34.56'
print(text_to_ip(t))
