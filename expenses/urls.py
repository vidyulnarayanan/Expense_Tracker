# expenses/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('add_expense/', views.add_expense, name='add_expense'),
    path('edit_expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('expense-history/', views.expense_history, name='expense_history'),
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('reports/', views.reports, name='reports'),
    path('download-report/', views.download_report, name='download_report')

]
