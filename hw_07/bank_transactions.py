"""
Bank Account Module

This module provides functionality for managing a bank account, including deposit, withdrawal,
and balance retrieval operations. It also includes a custom exception for handling insufficient
funds scenarios.

Features:
- `BankAccount` class for handling basic banking transactions.
- `NoMoneyException` for handling insufficient funds errors.
- Unit tests using `pytest`:
  - Fixtures for setting up test accounts.
  - Parameterized tests for deposit and withdrawal.
  - Mock testing for external API interactions.
  - Conditional skipping of tests based on account balance.

Usage:
This module can be used to simulate bank account operations and test different scenarios related
to deposits, withdrawals, and account balance management.
"""

import pytest
from unittest.mock import MagicMock


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


class BankAccount:
    """
    Represents a bank account with basic transaction operations.
    """

    def __init__(self, owner: str, balance: float, currency: str = "UAH") -> None:
        """
        Initialize a bank account.

        Args:
            owner (str): The name of the account holder.
            balance (float): The initial balance of the account.
            currency (str, optional): The currency of the account (default is "UAH").
        """
        self.owner = owner
        self.balance = balance
        self.currency = currency

    def deposit(self, amount: float) -> None:
        """
        Deposit money into the account.

        Args:
            amount (float): The amount to deposit.
        """
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """
        Withdraw money from the account if there are sufficient funds.

        Args:
            amount (float): The amount to withdraw.

        Raises:
            NoMoneyException: If there are not enough funds in the account.
        """
        if self.balance < amount:
            raise NoMoneyException(amount, self.balance, self.currency, "withdrawal")
        self.balance -= amount

    def get_balance(self) -> float:
        """
        Get the current account balance.

        Returns:
            float: The current balance.
        """
        return self.balance


# Fixture for creating a bank account
@pytest.fixture
def bank_account():
    return BankAccount("John Doe", 1000.00)


# Test deposit functionality
@pytest.mark.parametrize("deposit_amount", [100, 200, 500])
def test_deposit(bank_account, deposit_amount):
    initial_balance = bank_account.get_balance()
    bank_account.deposit(deposit_amount)
    assert bank_account.get_balance() == initial_balance + deposit_amount


# Test withdraw functionality
@pytest.mark.parametrize("withdraw_amount", [50, 200, 500])
def test_withdraw(bank_account, withdraw_amount):
    initial_balance = bank_account.get_balance()
    bank_account.withdraw(withdraw_amount)
    assert bank_account.get_balance() == initial_balance - withdraw_amount


# Test withdrawal when insufficient funds
def test_withdraw_insufficient_funds(bank_account):
    with pytest.raises(NoMoneyException):
        bank_account.withdraw(2000)  # Exceeds balance


# Mock test for external API interaction
def test_mock_external_api():
    mock_api = MagicMock()
    mock_api.get_balance.return_value = 500.00
    assert mock_api.get_balance() == 500.00


# Skip test if balance is zero
@pytest.mark.skipif(lambda: bank_account().get_balance() == 0, reason="Skipping because balance is zero")
def test_skip_withdraw_on_empty_account(bank_account):
    bank_account.withdraw(bank_account.get_balance())
    with pytest.raises(NoMoneyException):
        bank_account.withdraw(10)  # Should fail due to zero balance
