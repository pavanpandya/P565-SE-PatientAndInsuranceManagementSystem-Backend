from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        mobile_number = request.POST['mobile_number']
        email = request.POST['email']
        gender = request.POST['gender']
        date_of_birth = request.POST['date_of_birth']

        # Check for uniqueness of email and mobile number
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        if User.objects.filter(mobile_number=mobile_number).exists():
            messages.error(request, 'Mobile number already exists')
            return redirect('signup')

        User.objects.create(
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile_number,
            email=email,
            gender=gender,
            date_of_birth=date_of_birth
        )
        messages.success(request, 'Account created successfully')
        return redirect('signup')

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('dashboard')  # Redirect to the dashboard page after login
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')
    
