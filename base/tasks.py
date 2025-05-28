import pandas as pd
from .models import Customer, Loan
from celery import shared_task
from datetime import datetime

@shared_task
def ingest_data():
    customer_df = pd.read_excel('/app/customer_data.xlsx')
    loan_df = pd.read_excel('/app/loan_data.xlsx')

    for _, row in customer_df.iterrows():
        Customer.objects.get_or_create(
            customer_id=row['Customer ID'],
            defaults={
                'first_name': row['First Name'],
                'last_name': row['Last Name'],
                'phone_number': row['Phone Number'],
                'monthly_income': row['Monthly Salary'],
                'approved_limit': row['Approved Limit'],
                'age':row['Age']
            }
        )

    for _, row in loan_df.iterrows():
        Loan.objects.get_or_create(
            loan_id=row['Loan ID'],
            defaults={
                'customer_id': row['Customer ID'],
                'loan_amount': row['Loan Amount'],
                'tenure': row['Tenure'],
                'interest_rate': row['Interest Rate'],
                'monthly_installment': row['Monthly payment'],
                'emis_paid_on_time': row['EMIs paid on Time'],
                'start_date': pd.to_datetime(row['Date of Approval']).date(),
                'end_date': pd.to_datetime(row['End Date']).date(),
            }
        )
