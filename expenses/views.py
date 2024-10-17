from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import Expense
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

@csrf_exempt  
def add_expense(request):
    if request.method == 'GET':
        # Render the HTML form
        return render(request, 'add_expense.html', {
            'today': datetime.today().strftime('%Y-%m-%d')
        })
    
    elif request.method == 'POST':
        try:
            # Retrieve data from the form
            description = request.POST.get('description').strip()
            amount = request.POST.get('amount').strip()
            date = request.POST.get('date').strip()
            category = request.POST.get('category').strip()

            # Validate the inputs
            if not description or not amount or not category or not date:
                return JsonResponse({'success': False, 'error': 'All fields are required!'})

            # Convert amount to a float and validate
            amount = float(amount)
            if amount <= 0:
                return JsonResponse({'success': False, 'error': 'Amount must be greater than zero!'})

            # Create the Expense entry
            Expense.objects.create(
                description=description,
                amount=amount,
                date=date,
                category=category
            )

            return JsonResponse({'success': True})

        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid input format!'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == 'GET':
        return render(request, 'edit_expense.html', {
            'expense': expense,
        })

    elif request.method == 'POST':
        try:
            # Retrieve updated data from the form
            description = request.POST.get('description').strip()
            amount = request.POST.get('amount').strip()
            date = request.POST.get('date').strip()
            category = request.POST.get('category').strip()

            # Validate the inputs
            if not description or not amount or not category or not date:
                return JsonResponse({'success': False, 'error': 'All fields are required!'})

            # Convert amount to a float and validate
            amount = float(amount)
            if amount <= 0:
                return JsonResponse({'success': False, 'error': 'Amount must be greater than zero!'})

            # Update the existing expense
            expense.description = description
            expense.amount = amount
            expense.date = date
            expense.category = category
            expense.save()

            return JsonResponse({'success': True})

        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid input format!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})