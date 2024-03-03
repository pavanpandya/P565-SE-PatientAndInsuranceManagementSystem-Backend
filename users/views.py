from .models import Patient, Doctor, InsuranceProvider
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import json


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone = data.get('phone')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            user_type = data.get('user_type')

            # Validate request data
            if not all([first_name, last_name, email, phone, password, confirm_password]):
                return JsonResponse({'error': 'All fields are required'}, status=400)
            if password != confirm_password:
                return JsonResponse({'error': 'Password and confirm password do not match'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            if User.objects.filter(phone=phone).exists():
                return JsonResponse({'error': 'Mobile number already exists'}, status=400)

            # Create User and save
            user = User.objects.create_user(
                email=email, 
                password=password, 
                first_name=first_name, 
                last_name=last_name
            )

            # Return success message
            return JsonResponse({'message': 'Account created successfully. Please login to continue'}, status=201)
        except ValidationError as e:
            return JsonResponse({'error': e.message}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Authenticate user
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                logout(request)
                return JsonResponse({'message': 'Logout successful'}, status=200)
            else:
                return JsonResponse({'error': 'User is not authenticated'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def profile(request):
    if request.user.is_authenticated:
        user = request.user
        return JsonResponse({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone
        }, status=200)
    else:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)
    

@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                data = json.loads(request.body)
                user = request.user
                user.first_name = data.get('first_name', user.first_name)
                user.last_name = data.get('last_name', user.last_name)
                user.email = data.get('email', user.email)
                user.phone = data.get('phone', user.phone)
                user.save()
                return JsonResponse({'message': 'Profile updated successfully'}, status=200)
            else:
                return JsonResponse({'error': 'User is not authenticated'}, status=401)
        except ValidationError as e:
            return JsonResponse({'error': e.message}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    

@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                data = json.loads(request.body)
                user = request.user
                old_password = data.get('old_password')
                new_password = data.get('new_password')
                confirm_password = data.get('confirm_password')

                if not all([old_password, new_password, confirm_password]):
                    return JsonResponse({'error': 'All fields are required'}, status=400)
                if new_password != confirm_password:
                    return JsonResponse({'error': 'New password and confirm password do not match'}, status=400)
                if not user.check_password(old_password):
                    return JsonResponse({'error': 'Old password is incorrect'}, status=400)

                user.set_password(new_password)
                user.save()
                return JsonResponse({'message': 'Password changed successfully'}, status=200)
            else:
                return JsonResponse({'error': 'User is not authenticated'}, status=401)
        except ValidationError as e:
            return JsonResponse({'error': e.message}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    

@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'error': 'Email is required'}, status=400)
            if not User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email does not exist'}, status=400)

            return JsonResponse({'message': 'Reset password link sent to your email'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    

@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')

            if not all([email, new_password, confirm_password]):
                return JsonResponse({'error': 'All fields are required'}, status=400)
            if new_password != confirm_password:
                return JsonResponse({'error': 'New password and confirm password do not match'}, status=400)
            if not User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email does not exist'}, status=400)

            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return JsonResponse({'message': 'Password reset successful'}, status=200)
        except ValidationError as e:
            return JsonResponse({'error': e.message}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
