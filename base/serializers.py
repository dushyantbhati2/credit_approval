from rest_framework.serializers import ModelSerializer
from . import models

class CustomerSerializer(ModelSerializer):
    class Meta:
        model=models.Customer
        fields='__all__'
        read_only_fields = ('approved_limit','customer_id')
    
    def create(self,validated_data):
        monthly_income = validated_data.get('monthly_income')
        approved_limit = round((36 * monthly_income) / 100000) * 100000
        last_customer = models.Customer.objects.order_by('-customer_id').first()
        next_customer_id = last_customer.customer_id + 1 if last_customer else 1
        return models.Customer.objects.create(approved_limit=approved_limit,customer_id=next_customer_id,**validated_data)
    
    def to_representation(self, instance):
        return {
            'customer_id': instance.customer_id,
            'name': f"{instance.first_name} {instance.last_name}",
            'age': instance.age,
            'monthly_income': int(instance.monthly_income),
            'approved_limit': int(instance.approved_limit),
            'phone_number': int(instance.phone_number)
        }
    
class LoanSerializer(ModelSerializer):
    class Meta:
        model = models.Loan
        fields = '__all__'
        read_only_fields = ('loan_id',)

    def create(self,validated_data):
        last_loan = models.Loan.objects.order_by('-loan_id').first()
        next_loan_id = last_loan.loan_id + 1 if last_loan else 1
        return models.Loan.objects.create(loan_id=next_loan_id,**validated_data)
    
    def to_representation(self, instance):
        return {
            "loan_id": instance.loan_id,
            "customer_id": instance.customer.customer_id,
            "loan_approved": True,
            "message": "Loan approved",
            "monthly_installment": round(instance.monthly_installment, 2)
        }

class LoanViewSerializer(ModelSerializer):
    customer=CustomerSerializer()
    class Meta:
        model = models.Loan
        fields = ['loan_id','customer','loan_amount','interest_rate','monthly_installment','tenure']

class AllLoanViewSerializer(ModelSerializer):
    class Meta:
        model = models.Loan
        fields = ['loan_id', 'loan_amount', 'interest_rate', 'monthly_installment', 'tenure', 'emis_paid_on_time']

    def to_representation(self, instance):
        repayments_left = max(instance.tenure - instance.emis_paid_on_time, 0)
        return {
            "loan_id": instance.loan_id,
            "loan_amount": instance.loan_amount,
            "interest_rate": instance.interest_rate,
            "monthly_installment": round(instance.monthly_installment, 2),
            "repayments_left": repayments_left
        }
    
    