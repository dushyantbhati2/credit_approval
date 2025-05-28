import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_register_customer():
    client = APIClient()
    data = {
        "first_name": "New",
        "last_name": "User",
        "age": 25,
        "monthly_income": 40000,
        "phone_number": 9988776655
    }
    response = client.post("/register", data, format="json")
    assert response.status_code == 201
    assert "customer_id" in response.data


@pytest.mark.django_db
def test_check_eligibility(customer):
    client = APIClient()
    data = {
        "customer_id": customer.customer_id,
        "loan_amount": 100000,
        "interest_rate": 14,
        "tenure": 12
    }
    response = client.post("/check-eligibility", data, format="json")
    assert response.status_code == 200
    assert "approval" in response.data


@pytest.mark.django_db
def test_create_loan(customer):
    client = APIClient()
    data = {
        "customer_id": customer.customer_id,
        "loan_amount": 100000,
        "interest_rate": 14,
        "tenure": 12
    }
    response = client.post("/create-loan", data, format="json")
    assert response.status_code == 201
    assert response.data["loan_approved"] is True


@pytest.mark.django_db
def test_view_loan(loan):
    client = APIClient()
    response = client.get(f"/view-loan/{loan.loan_id}")
    assert response.status_code == 200
    assert response.data["loan_id"] == loan.loan_id


@pytest.mark.django_db
def test_view_loans_by_customer(customer, loan):
    client = APIClient()
    response = client.get(f"/view-loans/{customer.customer_id}")
    assert response.status_code == 200
    assert isinstance(response.data, list)
