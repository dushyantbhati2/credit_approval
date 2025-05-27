from base.models import Loan, Customer
from datetime import date
from math import pow

def evaluate_eligibility(customer: Customer, loan_amount: float, interest_rate: float, tenure: int):
    loans = Loan.objects.filter(customer=customer)

    if customer.current_debt > customer.approved_limit:
        return {
            "approved": False,
            "credit_score": 0,
            "corrected_interest_rate": interest_rate,
            "monthly_installment": 0,
            "reason": "Customer has exceeded credit limit"
        }

    emis_paid_on_time = sum(l.emis_paid_on_time for l in loans)
    emi_score = min(emis_paid_on_time, 30)

    num_loans = loans.count()
    loan_count_score = max(0, 20 - num_loans * 2)

    current_year_loans = loans.filter(start_date__year=date.today().year).count()
    current_year_score = min(current_year_loans * 3, 15)

    total_loan_volume = sum(l.loan_amount for l in loans)
    loan_volume_score = min(total_loan_volume // 100000, 20)

    credit_score = min(100, emi_score + loan_count_score + current_year_score + loan_volume_score)

    corrected_interest_rate = interest_rate
    approved = False

    if credit_score > 50:
        approved = True
    elif 30 < credit_score <= 50:
        corrected_interest_rate = max(interest_rate, 12)
        approved = corrected_interest_rate >= 12
    elif 10 < credit_score <= 30:
        corrected_interest_rate = max(interest_rate, 16)
        approved = corrected_interest_rate >= 16
    else:
        approved = False

    monthly_interest = corrected_interest_rate / 100 / 12
    emi = (loan_amount * monthly_interest * pow(1 + monthly_interest, tenure)) / (pow(1 + monthly_interest, tenure) - 1)

    current_emis = sum(l.monthly_installment for l in loans if l.end_date >= date.today())
    if current_emis + emi > 0.5 * customer.monthly_income:
        approved = False

    return {
        "approved": approved,
        "credit_score": credit_score,
        "corrected_interest_rate": corrected_interest_rate,
        "monthly_installment": round(emi, 2),
    }
