import re

def text_to_dict(text: str) -> dict[str, int]:
    s = re.split(r"\W+", text.lower())

    return {word: s.count(word) for word in set(s) if word}

# Тестуємо функцію
print(text_to_dict('Заявляється повна незалежність України, проте ця незалежність являє собою фікцію!'
                   'Отже можемо зробити висновок, що для досягнення незалежності потрібно правильно виховати молодь!'))
