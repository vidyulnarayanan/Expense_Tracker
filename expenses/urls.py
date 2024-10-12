from django.urls import path
from .views import ExpenseListView  

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expense-list'),
]
