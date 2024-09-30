# signup/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import AdminSignUpForm  # Import the form you just created
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup_success')
    else:
        form = AdminSignUpForm()
    return render(request, 'signup/admin_signup.html', {'form': form})

def signup_success(request):
    return render(request, 'signup/signup_success.html')

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_home')  # Change to the actual admin homepage URL
    else:
        form = AuthenticationForm()
    return render(request, 'signup/admin_login.html', {'form': form})

@login_required  # This decorator ensures that only logged-in users can access this view
def admin_home(request):
    return render(request, 'signup/admin_home.html')  # Point to your admin home template


@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')  # Redirect to the login page after logout