from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def validate_password_strength(password):
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char in '!@#$%^&*()_+' for char in password):
        return False
    return True

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return redirect('register')

        if not validate_password_strength(password):
            messages.error(request, 'Password must be at least 8 characters long, contain an uppercase letter, and a special character.')
            return redirect('register')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request,'login.html')
    
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html', {'email': email}) 
        
def logout_view(request):
    logout(request)
    return redirect('login')
