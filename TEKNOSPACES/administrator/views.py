from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import User, Space
from .forms import UserSignUpForm  
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import SpaceForm
from .models import Reservation
from django.contrib import messages
from django.db.models import Q

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'admin':
                return redirect('admin_home')  
            elif user.is_active == 1 and user.user_type == 'regular':
                return redirect('user_home')  
            else:
                return redirect('login.html') #add if user.is_active = 1; can't login; else, user_home
    return render(request, 'users/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('user_home')  
    else:
        form = UserSignUpForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def user_home(request):
    if request.user.user_type != 'regular':
        return redirect('admin_home') 
    spaces = Space.objects.all()
    return render(request, 'users/user_home.html', {'spaces': spaces})

@login_required
def user_profile(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user)  
    return render(request, 'users/user_profile.html', {'user': user, 'reservations': reservations})

def user_spaces(request):
    today = timezone.now()

    if request.method == 'POST':
        form = SpaceForm(request.POST)
        if form.is_valid():
            space = form.save(commit=False)  
            space.added_by = request.user  
            space.save()  
            return redirect('user_spaces')  
    else:
        form = SpaceForm()  

    return render(request, 'users/user_spaces.html', {'form': form, 'today': today})


@login_required
def edit_user_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        return redirect('user_profile')  
    return render(request, 'users/user_profile.html')


@login_required
def admin_home(request):
    if request.user.user_type != 'admin':
        return redirect('user_home')  
    
    spaces = Space.objects.all()    
    return render(request, 'admins/admin_home.html', {
        'spaces': spaces,
    })

def approve_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.status = 'approved'
    reservation.notified = False  
    reservation.save()

    messages.success(request, f'Reservation for {reservation.space.space_title} has been approved!')

    if not reservation.notified:
        reservation.notified = True  
        reservation.save()

    return redirect('admin_profile')

def decline_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.status = 'declined'
    reservation.notified = False  
    reservation.save()

    messages.error(request, f'Reservation for {reservation.space.space_title} has been declined.')

    if not reservation.notified:
        reservation.notified = True  
        reservation.save()

    return redirect('admin_profile')

#modify this dapat naay notifications nga sa users affected... not just in the tab 
def cancel_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.status = 'cancelled'
    reservation.notified = False  
    reservation.save()

    messages.error(request, f'Reservation for {reservation.space.space_title} has been cancelled.')

    if not reservation.notified:
        reservation.notified = True  
        reservation.save()

    return redirect('admin_reservations')




@login_required
def admin_profile(request):
    if request.user.user_type != 'admin':
        return redirect('user_profile')  
    
    pending_reservations = Reservation.objects.filter(status='pending')

    return render(request, 'admins/admin_profile.html', {
        'pending_reservations': pending_reservations,
    })


@login_required
def edit_admin_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        return redirect('admin_profile')  
    return render(request, 'signup/admin_profile.html')

@login_required
def admin_spaces(request):
    today = timezone.now()

    if request.method == 'POST':
        form = SpaceForm(request.POST)
        if form.is_valid():
            space = form.save(commit=False)  
            space.added_by = request.user  
            space.save()  
            return redirect('admin_spaces')  
    else:
        form = SpaceForm()  

    return render(request, 'admins/admin_spaces.html', {'form': form, 'today': today})
@login_required
def admin_reservations(request):
    if request.user.user_type != 'admin':
        return redirect('user_reservation')  
    
    pending_reservations = Reservation.objects.filter(status='pending')
    approved_reservations = Reservation.objects.filter(status='approved')
    declined_reservations = Reservation.objects.filter(status='declined')
    cancelled_reservations = Reservation.objects.filter(status='cancelled')

    return render(request, 'admins/admin_reservations.html', {
        'pending_reservations': pending_reservations,
        'approved_reservations': approved_reservations,
        'declined_reservations': declined_reservations,
        'cancelled_reservations': cancelled_reservations,
    })

from django.http import JsonResponse
from .models import Space

def get_space(request, space_id):
    space = Space.objects.get(id=space_id)
    data = {
        'id': space.id,
        'space_title': space.space_title,
        'description': space.description,
        'location': space.location,
        'from_date': space.from_date.strftime('%Y-%m-%d'),
        'to_date': space.to_date.strftime('%Y-%m-%d'),
    }
    return JsonResponse(data)

@login_required
def edit_space(request):
    if request.method == 'POST':
        space_id = request.POST.get('space_id')
        space = Space.objects.get(id=space_id)
        
        # Update space details
        space.space_title = request.POST.get('space_title')
        space.description = request.POST.get('description')
        space.location = request.POST.get('location')
        space.from_date = request.POST.get('from_date')
        space.to_date = request.POST.get('to_date')
        space.save()

        return redirect('admin_home')
    

@login_required
def reserve_space(request):
    if request.method == 'POST':
        space_id = request.POST['space_id']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        
        space = Space.objects.get(id=space_id)
        reservation = Reservation.objects.create(
            user=request.user,
            space=space,
            start_time=start_time,
            end_time=end_time,
            status='pending'
        )
        reservation.save()
        messages.success(request, 'Reservation request submitted successfully!')
        return redirect('user_reservation')
    return redirect('user_reservation')

@login_required
def user_reservation(request):
    pending_reservations = Reservation.objects.filter(user=request.user, status='pending')
    approved_reservations = Reservation.objects.filter(user=request.user, status='approved')
    declined_reservations = Reservation.objects.filter(user=request.user, status='declined')
    cancelled_reservations = Reservation.objects.filter(user=request.user, status='cancelled')
    
    context = {
        'pending_reservations': pending_reservations,
        'approved_reservations': approved_reservations,
        'declined_reservations': declined_reservations,
        'cancelled_reservations': cancelled_reservations,
    }
    return render(request, 'users/user_spaces.html', context)


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
@login_required
def delete_space(request, space_id):
    """
    Deletes the space from the administrator_space table if the admin created it.
    """
    if request.method == 'POST':
        space = get_object_or_404(Space, id=space_id, added_by=request.user)
        space_title = space.space_title
        space.delete()
        return JsonResponse({'success': True, 'message': f'Space "{space_title}" deleted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
#gana
@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        return redirect('user_home')  
    
    users = User.objects.filter(user_type='regular')
    return render(request, 'admins/admin_dashboard.html', {
        'users': users,
    })

#ambot
@login_required
def edit_user_from_admin_dashboard(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        return redirect('admin_dashboard')  
    return render(request, 'admins/admin_dashboard.html')

#ambot
@login_required
def edit_user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User details updated successfully.')
            return redirect('admin_dashboard')
    else:
        form = UserSignUpForm(instance=user)
    return render(request, 'admins/admin_dashboard.html', {'form': form, 'user': user})

@login_required
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()

    if user.is_active:
        messages.success(request, f'{user.username} has been activated.')
    else:
        messages.success(request, f'{user.username} has been deactivated.')

    return redirect('admin_dashboard')
