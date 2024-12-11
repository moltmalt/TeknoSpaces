from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from space.models import Category, Type, Space
from account.models import CustomUser

def index(request):
    spaces = Space.objects.filter(is_booked=False)[0:6]
    categories = Category.objects.all()
    types = Type.objects.all()
    latest_spaces = Space.objects.filter(is_booked=False).order_by('-date_created')[:4]
    popular_spaces = Space.objects.filter(is_booked=False).order_by('book_count')[:8]

    slider_images = [
        'slider-image-1.svg',
        'slider-image-2.svg',
        'slider-image-3.svg',
    ]

    return render(request, 'core/index.html',{
        'categories': categories,
        'types': types,
        'spaces': spaces,
        'latest_spaces': latest_spaces,
        'popular_spaces': popular_spaces,
        'slider_images': slider_images,
    })

def contact_us(request):
    return render(request, 'core/contact_us.html')

def about_us(request):
    return render(request, 'core/about_us.html')

@login_required
def log_out(request):
    logout(request)
    return redirect('core:index')

from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'core/log_in.html'
