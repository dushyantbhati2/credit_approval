from django.urls import path
from . import views
urlpatterns = [
    path('register',views.CustomerView.as_view()),
    path('check-eligibility',views.CheckEligibilityView.as_view()),
    path('create-loan',views.LoanView.as_view()),
    path('view-loan/<int:pk>',views.LoanView.as_view()),
    path('view-loans/<int:pk>',views.AllLoanView.as_view())
]
