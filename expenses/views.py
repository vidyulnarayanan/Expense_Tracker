from django.shortcuts import render,get_object_or_404,redirect,redirect
from django.contrib.auth.decorators import login_required
from .models import Expense
from django.contrib import messages  
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
import matplotlib.pyplot as plt
from django.db.models import Sum
import base64
import csv
from django.http import HttpResponse
import io

@login_required
def add_expense(request):
    if request.method == 'GET':
        return render(request, 'add_expense.html', {
            'today': datetime.today().strftime('%Y-%m-%d')
        })
    elif request.method == 'POST':
        description = request.POST.get('description').strip()
        amount = request.POST.get('amount').strip()
        date = request.POST.get('date').strip()
        category = request.POST.get('category').strip()

        if not description or not amount or not category or not date:
            messages.error(request, 'All fields are required!')
            return render(request, 'add_expense.html', {'today': datetime.today().strftime('%Y-%m-%d')})

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, 'Amount must be greater than zero!')
                return render(request, 'add_expense.html', {'today': datetime.today().strftime('%Y-%m-%d')})
            
            transaction_date = datetime.strptime(date, '%Y-%m-%d').date()
            if transaction_date > datetime.today().date():
                messages.error(request, 'Date cannot be in the future!')
                return render(request, 'add_expense.html', {'today': datetime.today().strftime('%Y-%m-%d')})

            Expense.objects.create(
                user=request.user, 
                description=description,
                amount=amount,
                date=date,
                category=category
            )

            messages.success(request,'Expense added successfully!')
            return redirect('dashboard')

        except ValueError:
            messages.error(request, 'Invalid input format!')
            return render(request, 'add_expense.html', {'today': datetime.today().strftime('%Y-%m-%d')})
        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'add_expense.html', {'today': datetime.today().strftime('%Y-%m-%d')})

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'GET':
        return render(request, 'edit_expense.html', {
            'expense': expense,
        })

    elif request.method == 'POST':
        description = request.POST.get('description').strip()
        amount = request.POST.get('amount').strip()
        date = request.POST.get('date').strip()
        category = request.POST.get('category').strip()

        if not description or not amount or not category or not date:
            messages.error(request, 'All fields are required!')
            return render(request, 'edit_expense.html', {'expense': expense})

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, 'Amount must be greater than zero!')
                return render(request, 'edit_expense.html', {'expense': expense})
            
            transaction_date = datetime.strptime(date, '%Y-%m-%d').date()
            if transaction_date > datetime.today().date():
                messages.error(request, 'Date cannot be in the future!')
                return render(request, 'add_expense.html', {'today': datetime.today().strftime('%Y-%m-%d')})

            expense.description = description
            expense.amount = amount
            expense.date = date
            expense.category = category
            expense.save()

            messages.success(request, 'Expense updated successfully!')
            return redirect('dashboard')  

        except ValueError:
            messages.error(request, 'Invalid input format for amount!')
            return render(request, 'edit_expense.html', {'expense': expense})
        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'edit_expense.html', {'expense': expense})


@login_required
def expense_history(request):
    search_term = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    expenses = Expense.objects.filter(user=request.user)

    if search_term:
        expenses = expenses.filter(Q(description__icontains=search_term))

    if category_filter:
        expenses = expenses.filter(category=category_filter)

    if start_date and end_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            expenses = expenses.filter(date__range=(start_date_obj, end_date_obj))
        except ValueError:
            messages.error(request, "Invalid date range!")

    paginator = Paginator(expenses, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'expense_history.html', {
        'page_obj': page_obj,
        'search_term': search_term,
        'category_filter': category_filter,
        'start_date': start_date,
        'end_date': end_date,
        'category_choices': Expense.CATEGORY_CHOICES
    })

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expense_history')
    return redirect('expense_history')

@login_required
def reports(request):
    user = request.user
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_month_name = datetime.now().strftime('%B')  
    monthly_expenses = (
        Expense.objects.filter(user=user, date__year=current_year)
        .values('date__month')
        .annotate(total=Sum('amount'))
        .order_by('date__month')
    )
    category_expenses = (
        Expense.objects.filter(user=user, date__year=current_year)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    daily_expenses = (
        Expense.objects.filter(user=user, date__year=current_year, date__month=current_month)
        .values('date__day')
        .annotate(total=Sum('amount'))
        .order_by('date__day')
    )
    months = [item['date__month'] for item in monthly_expenses]
    monthly_totals = [item['total'] for item in monthly_expenses]

    plt.figure(figsize=(10, 6))
    plt.bar(months, monthly_totals, color='#4BC0C0')
    plt.title(f'Monthly Expenses for {current_year}')  
    plt.xlabel('Month')
    plt.ylabel('Total Expenses')
    plt.xticks(months, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct'])
    
    monthly_image = io.BytesIO()
    plt.savefig(monthly_image, format='png')
    monthly_image.seek(0)
    monthly_chart = base64.b64encode(monthly_image.getvalue()).decode()
    plt.clf()

    days = list(range(1, 32))  
    daily_totals = [0] * 31 

    for item in daily_expenses:
        day_index = item['date__day'] - 1
        daily_totals[day_index] = item['total']

    plt.figure(figsize=(10, 6))
    plt.bar(days, daily_totals, color='#FF6384')
    plt.title(f'Daily Expenses for {current_month_name}') 
    plt.xlabel('Day')
    plt.ylabel('Total Expenses')
    plt.xticks(days)  

    daily_image = io.BytesIO()
    plt.savefig(daily_image, format='png')
    daily_image.seek(0)
    daily_chart = base64.b64encode(daily_image.getvalue()).decode()
    plt.clf()  

    categories = [item['category'] for item in category_expenses]
    category_totals = [item['total'] for item in category_expenses]  

    plt.figure(figsize=(10, 6))
    plt.bar(categories, category_totals, color='#FF6384')
    plt.title(f'Expenses by Category for {current_month_name}')
    plt.xlabel('Category')
    plt.ylabel('Total Expenses')
    plt.xticks(ha='right')  

    category_image = io.BytesIO()
    plt.savefig(category_image, format='png')
    category_image.seek(0)
    category_chart = base64.b64encode(category_image.getvalue()).decode()

    context = {
        'monthly_chart': monthly_chart,
        'daily_chart': daily_chart,
        'category_chart': category_chart,
        'monthly_expenses': list(monthly_expenses),
        'category_expenses': list(category_expenses),
        'current_month_name': current_month_name,

    }
    return render(request, 'reports.html', context)

@login_required
def download_report(request):
    user = request.user
    report_type = request.GET.get('type', 'all') 
    current_month_name = datetime.now().strftime('%B')

    if report_type == 'current_month':
        expenses = Expense.objects.filter(
            user=user,
            date__year=datetime.now().year,
            date__month=datetime.now().month
        ).values('date', 'category', 'amount', 'description').order_by('-date')
        filename = f"{current_month_name}_report.csv"
    else:
        expenses = Expense.objects.filter(
            user=user,
        ).values('date', 'category', 'amount', 'description').order_by('-date')
        filename = f"{user.username}_report.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Amount', 'Description'])

    for expense in expenses:
        writer.writerow([expense['date'].strftime('%Y-%m-%d'), expense['category'], expense['amount'], expense['description']])

    return response
