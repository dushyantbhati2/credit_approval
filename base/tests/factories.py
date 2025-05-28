import factory
from base.models import Customer, Loan
from datetime import date, timedelta

class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    customer_id = factory.Sequence(lambda n: 1000 + n)
    first_name = "Test"
    last_name = "User"
    age = 30
    monthly_income = 50000
    approved_limit = 1800000
    current_debt = 0
    phone_number = factory.Sequence(lambda n: 9000000000 + n)


class LoanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Loan

    customer = factory.SubFactory(CustomerFactory)
    loan_id = factory.Sequence(lambda n: 2000 + n)
    loan_amount = 200000
    interest_rate = 12
    monthly_installment = 17800.0
    tenure = 12
    emis_paid_on_time = 10
    start_date = date.today() - timedelta(days=30)
    end_date = date.today() + timedelta(days=365)
