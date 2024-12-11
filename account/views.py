from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser

# Create your views here.

@login_required
def user_profile(request):
    user = request.user  
    return render(request, 'user_profile.html', {'user': user})
