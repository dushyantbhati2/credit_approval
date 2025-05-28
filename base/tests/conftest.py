import pytest
from .factories import CustomerFactory, LoanFactory

@pytest.fixture
def customer():
    return CustomerFactory()

@pytest.fixture
def loan(customer):
    return LoanFactory(customer=customer)
