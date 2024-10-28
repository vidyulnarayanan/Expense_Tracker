from django.shortcuts import render
from expenses.models import Expense
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
import matplotlib.pyplot as plt
from django.contrib import messages
import io
from datetime import datetime
import base64

@login_required
def dashboard(request):
    user = request.user
    current_date = timezone.now().date()
    start_of_month = current_date.replace(day=1)
    current_month_name = datetime.now().strftime('%B')
    monthly_expenses = Expense.objects.filter(user=user, date__gte=start_of_month, date__lte=current_date)
    total_expense = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    expenses_by_category = monthly_expenses.values('category').annotate(total=Sum('amount'))
    recent_transactions = monthly_expenses.order_by('-date')[:5]
    categories = [item['category'] for item in expenses_by_category]
    category_totals = [item['total'] for item in expenses_by_category]

    pie_chart = None
    if category_totals:
        plt.figure(figsize=(8, 8))
        plt.pie(category_totals, labels=categories, autopct='%1.1f%%', startangle=140,
                textprops={'fontsize': 14, 'fontweight': 'bold'})
        plt.title(f'PIE CHART',fontsize=20, fontdict={'fontweight': 'bold', 'fontfamily': 'serif'})
        
        pie_chart_image = io.BytesIO()
        plt.savefig(pie_chart_image, format='png')
        pie_chart_image.seek(0)
        
        pie_chart = base64.b64encode(pie_chart_image.getvalue()).decode()
    context = {
        'total_expense': total_expense,
        'expenses_by_category': expenses_by_category,
        'recent_transactions': recent_transactions,
        'current_date': current_date,
        'pie_chart': pie_chart,
        'messages': messages.get_messages(request),
        'current_month_name': current_month_name,
    }
    return render(request, 'dashboard.html', context)

