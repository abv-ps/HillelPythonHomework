class Product(type):
    """
    Metaclass for creating product classes with predefined attributes.
    """
    def __new__(cls, name, bases, dct):
        dct.setdefault('name', None)
        dct.setdefault('price', None)
        return super().__new__(cls, name, bases, dct)


class ProductWithGetSet(metaclass=Product):
    def __init__(self, name: str, price: float):
        self.name = name
        self.set_price(price)

    def get_price(self) -> float:
        return self._price

    def set_price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value


class ProductWithProperty(metaclass=Product):
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value


class PriceDescriptor:
    """Descriptor for validating and managing the price attribute."""
    def __get__(self, instance, owner):
        return instance._price

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        instance._price = round(value, 2)


class CurrencyDescriptor:
    """Descriptor for converting price based on currency exchange rates."""
    def __init__(self, base_currency: str, exchange_rate: float):
        self.base_currency = base_currency
        self.exchange_rate = exchange_rate

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return round(instance.price * self.exchange_rate, 2)


class ProductWithDescriptor(metaclass=Product):
    """Product class using descriptors for price and currency conversion."""
    price = PriceDescriptor()
    price_usd = CurrencyDescriptor("USD", 1.0)
    price_eur = CurrencyDescriptor("EUR", 1.0)

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    @classmethod
    def update_exchange_rates(cls, usd_rate: float, eur_rate: float):
        """Updates exchange rates for all instances."""
        cls.price_usd.exchange_rate = usd_rate
        cls.price_eur.exchange_rate = eur_rate


def test_product_with_currency():
    # Create a product with base price
    product = ProductWithDescriptor(name="Some product", price=77.7)

    # Asking user for exchange rates
    usd_rate = float(input("Enter USD exchange rate: "))
    eur_rate = float(input("Enter EUR exchange rate: "))

    # Update exchange rates
    ProductWithDescriptor.update_exchange_rates(usd_rate, eur_rate)

    # Display product details
    print(f"Product name: {product.name}")
    print(f"Price in base currency: {product.price} units")
    print(f"Price in USD: {product.price_usd} dollars")
    print(f"Price in EUR: {product.price_eur} euros")


if __name__ == "__main__":
    p1 = ProductWithGetSet("Some_get", 11.2)
    print(f"ProductWithGetSet: {p1.name}, Price: {p1.get_price()}")
    p1.set_price(12.5)
    print(f"Updated Price: {p1.get_price()}")
    print()
    try:
        p1.set_price(-7)
    except ValueError as e:
        print(f"Error: {e}")
        print()

    p2 = ProductWithProperty("Some_prop", 12.1)
    print(f"ProductWithProperty: {p2.name}, Price: {p2.price}")
    p2.price = 27.3
    print(f"Updated Price: {p2.price}")
    print()
    try:
        p2.price = -2
    except ValueError as e:
        print(f"Error: {e}")
        print()

    test_product_with_currency()
