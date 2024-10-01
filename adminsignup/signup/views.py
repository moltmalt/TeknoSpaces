from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import AdminSignUpForm  # Use this form consistently

def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup_success')  # Redirect to sign-up success page
    else:
        form = AdminSignUpForm()
    return render(request, 'admins/admin_signup.html', {'form': form})


def signup_success(request):
    return render(request, 'admins/signup_success.html')

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_home')
    else:
        form = AuthenticationForm()
    return render(request, 'admins/admin_login.html', {'form': form})

@login_required
def admin_home(request):
    return render(request, 'admins/admin_home.html')

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def index(request):
    return render(request, 'index.html')
