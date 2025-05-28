from django.shortcuts import render
from . import serializers,models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from math import pow
from datetime import date,timedelta
from .utils import evaluate_eligibility
# Create your views here.

class CustomerView(APIView):
    def post(self,request):
        try:
            serial=serializers.CustomerSerializer(data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data,status=201)
            return Response({'error':serial.errors},status=400)
        except Exception as e:
            return Response({'error':str(e)},status=500)

class CheckEligibilityView(APIView):
    def post(self, request):
        try:
            customer = models.Customer.objects.get(customer_id=request.data['customer_id'])
            result = evaluate_eligibility(
                customer=customer,
                loan_amount=float(request.data['loan_amount']),
                interest_rate=float(request.data['interest_rate']),
                tenure=int(request.data['tenure']),
            )

            return Response({
                "customer_id": customer.customer_id,
                "approval": result['approved'],
                "interest_rate": float(request.data['interest_rate']),
                "corrected_interest_rate": result['corrected_interest_rate'],
                "tenure": int(request.data['tenure']),
                "monthly_installment": result['monthly_installment'],
            },status=200)

        except models.Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class LoanView(APIView):
    def get(self,request,pk):
        try:
            loan=models.Loan.objects.get(loan_id=pk)
            serial=serializers.LoanViewSerializer(loan)
            return Response(serial.data,status=200)
        except models.Loan.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    def post(self, request):
        try:
            customer = models.Customer.objects.get(customer_id=request.data['customer_id'])

            result = evaluate_eligibility(
                customer=customer,
                loan_amount=float(request.data['loan_amount']),
                interest_rate=float(request.data['interest_rate']),
                tenure=int(request.data['tenure'])
            )

            if not result['approved']:
                return Response({
                    "loan_id": None,
                    "customer_id": customer.customer_id,
                    "loan_approved": False,
                    "message": "Loan not approved",
                    "monthly_installment": result['monthly_installment']
                },status=200)

            loan = models.Loan.objects.create(
                customer=customer,
                loan_amount=float(request.data['loan_amount']),
                interest_rate=result['corrected_interest_rate'],
                tenure=int(request.data['tenure']),
                monthly_installment=result['monthly_installment'],
                emis_paid_on_time=0,
                start_date=date.today(),
                end_date=date.today() + timedelta(weeks=4 * int(request.data['tenure']))
            )

            customer.current_debt += loan.loan_amount
            customer.save()

            return Response(serializers.LoanSerializer(loan).data, status=201)

        except models.Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class AllLoanView(APIView):
    def get(self,request,pk):
        try:
            loans=models.Loan.objects.filter(customer__customer_id=pk)
            serial=serializers.AllLoanViewSerializer(loans,many=True)
            return Response(serial.data,status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)