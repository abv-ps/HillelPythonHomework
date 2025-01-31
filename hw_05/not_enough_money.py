class NoMoneyException(Exception):
    """
    Exception raised when a user attempts to complete a transaction without sufficient funds.
    """

    def __init__(
            self,
            required_amount: float,
            current_balance: float,
            currency: str = "UAH",
            transaction_type: str = "unknown",
    ) -> None:
        """
        Initialize the exception.

        Args:
            required_amount (float): The amount required to complete the transaction.
            current_balance (float): The current balance in the account.
            currency (str, optional): The currency of the account (default is "UAH").
            transaction_type (str, optional): The type of transaction (default is "unknown").
        """
        super().__init__(
            f"Insufficient funds for {transaction_type}. "
            f"Required: {required_amount:.2f} {currency}, but available: {current_balance:.2f} {currency}."
        )
        self.required_amount = required_amount
        self.current_balance = current_balance
        self.currency = currency
        self.transaction_type = transaction_type


class DigitalAccount:
    """
    Represents a digital account with basic transaction operations.
    """

    VALID_TRANSACTIONS = {"withdrawal", "send_money"}

    def __init__(self, owner: str, balance: float, currency: str = "UAH") -> None:
        """
        Initialize a digital account.

        Args:
            owner (str): The name of the account holder.
            balance (float): The initial balance of the account.
            currency (str, optional): The currency of the account (default is "UAH").
        """
        self.owner = owner
        self.balance = balance
        self.currency = currency

    def execute_transfer(self, amount: float, transfer_type: str) -> None:
        """
        Perform a transaction (withdrawal or sending money), checking for sufficient funds.

        Args:
            amount (float): The amount required for the transaction.
            transfer_type (str): The type of transaction (must be "withdrawal" or "send_money").

        Raises:
            NoMoneyException: If there are not enough funds in the account.
            ValueError: If the transaction type is invalid.
        """
        if transfer_type not in self.VALID_TRANSACTIONS:
            raise ValueError(f"Invalid transaction type: {transfer_type}. Allowed: {self.VALID_TRANSACTIONS}")

        if self.balance < amount:
            raise NoMoneyException(amount, self.balance, self.currency, transfer_type)

        self.balance -= amount
        print(
            f"{transfer_type.capitalize()} successful! {amount:.2f} {self.currency} deducted. "
            f"New balance: {self.balance:.2f} {self.currency}."
        )


if __name__ == "__main__":
    acc = DigitalAccount("Oleg Kadenyuk", 10000.00)

    try:
        acc.execute_transfer(200, "send_money")
    except NoMoneyException as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")

    try:
        acc.execute_transfer(200, "withdrawal")
    except NoMoneyException as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")

    # Перевірка некоректного типу транзакції
    try:
        acc.execute_transfer(100, "invalid_type")
    except NoMoneyException as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
