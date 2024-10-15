from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import AdminSignUpForm  # Use this form consistently
from .models import Admin
from django.utils import timezone

from .forms import SpaceForm
from .models import Space

def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_login')  # if sakto tanan fields adto siya login or pwede rasad home na diritso 
    else:
        form = AdminSignUpForm()
    return render(request, 'admins/admin_signup.html', {'form': form})

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
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def index(request):
    return render(request, 'index.html')

def admin_profile(request):
    return render(request, 'admins/admin_profile.html')

@login_required
def edit_admin_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        return redirect('admin_profile')  # Redirect to the admin home after saving
    return render(request, 'signup/admin_profile.html')

@login_required
def admin_spaces(request):
    today = timezone.now()  
    return render(request, 'admins/admin_spaces.html', {'today': today})


@login_required
def admin_spaces(request):
    today = timezone.now()

    if request.method == 'POST':
        form = SpaceForm(request.POST)
        if form.is_valid():
            space = form.save(commit=False)  # Don't save to the database yet
            space.added_by = request.user  # Assign the current logged-in admin
            space.save()  # Now save to the database
            return redirect('admin_spaces')  # Redirect after saving
    else:
        form = SpaceForm()  # Create an empty form for GET requests

    return render(request, 'admins/admin_spaces.html', {'form': form, 'today': today})

@login_required
def admin_home(request):
    # Fetch all spaces from the Space model
    spaces = Space.objects.all()  # Fetch all spaces from the database
    return render(request, 'admins/admin_home.html', {'spaces': spaces})