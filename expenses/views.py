from django.shortcuts import render
from django.http import JsonResponse
from .models import Expense
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

@csrf_exempt  # Only include this if you're not using CSRF tokens; remove if CSRF protection is applied correctly.
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
