from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    CATEGORY_CHOICES = (
        ('Food', 'Food'),
        ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'),
        ('Utilities', 'Utilities'),
        ('Other', 'Other'),  
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    description = models.CharField(max_length=255, default='Unnamed Expense')  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()  
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.category})"
