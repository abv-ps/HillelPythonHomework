def text_to_dict(text: str) -> dict[str, int]:
    s = ''.join(char if char not in ".,!?;:()[]{}\"'-" else ' ' for char in text).lower().split()

    return {word: s.count(word) for word in set(s) if word}


print(text_to_dict('Заявляється повна незалежність України, проте ця незалежність являє собою фікцію!'
                   'Отже можемо зробити висновок, що для досягнення незалежності потрібно правильно виховати молодь!'))

