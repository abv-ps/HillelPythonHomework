class Price:
    def __init__(self, amount: float):
        self.amount = round(amount, 2)

    def __add__(self, other: "Price") -> "Price":
        if not isinstance(other, Price):
            return NotImplemented
        return Price(self.amount + other.amount)

    def __sub__(self, other: "Price") -> "Price":
        if not isinstance(other, Price):
            return NotImplemented
        return Price(self.amount - other.amount)

    def __eq__(self, other: "Price") -> bool:
        if not isinstance(other, Price):
            return NotImplemented
        return self.amount == other.amount

    def __lt__(self, other: "Price") -> bool:
        if not isinstance(other, Price):
            return NotImplemented
        return self.amount < other.amount

    def __le__(self, other: "Price") -> bool:
        return self.amount < other.amount or self.amount == other.amount

    def __gt__(self, other: "Price") -> bool:
        return not self.amount <= other.amount

    def __ge__(self, other: "Price") -> bool:
        return not self.amount < other.amount


