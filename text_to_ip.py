import re

def text_to_ip(text: str) -> str:
    r: str = r'^(\d{1,3})\.{4}$'
    a: str | None = re.match(r, text)
    return a

t = '1.2.34.56'

print(text_to_ip(t))