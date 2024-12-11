from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Space, Category
from django.db.models import Q
from .models import Space 
from .forms import EditSpaceForm, SpaceForm
from booking.models import Booking

def space_list(request):
    query = request.GET.get('query', '')
    category_name = request.GET.get('category', '')
    
    spaces = Space.objects.all()
    if query:
        spaces = spaces.filter(title__icontains=query)
    if category_name:
        spaces = spaces.filter(category__name=category_name)
    
    popular_spaces = spaces.order_by('book_count')[:6] 

    # Fetch all categories for the sidebar
    categories = Category.objects.all()
    
    context = {
        'query': query,
        'category_name': category_name,
        'popular_spaces': popular_spaces,
        'categories': categories,
    }
    
    return render(request, 'space/spaces.html', context)

@login_required
def detail(request, pk):
    space = get_object_or_404(Space, pk=pk)
    related_spaces = Space.objects.filter(
        category__in=space.category.all(),
        is_booked=False
    ).exclude(pk=space.pk).distinct()
    
    # Get bookings for the current space
    space_bookings = Booking.objects.filter(space=space)
    
    # Bookings managed by the user if they are a superuser
    if request.user.is_superuser:
        pending_bookings = space_bookings.filter(status='pending')
        approved_bookings = space_bookings.filter(status='approved')
    else:
        pending_bookings = None
        approved_bookings = None
    
    # Check if the user has booked this space
    user_booking = space_bookings.filter(user=request.user).first()
    
    return render(request, 'space/detail.html', {
        'space': space,
        'related_spaces': related_spaces,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'user_booking': user_booking,
    })


@login_required
def delete(request, pk):
    space = get_object_or_404(Space, pk=pk, managed_by=request.user)
    space.delete()

    return redirect('dashboard:index')

@login_required
def edit(request, pk):
    space = get_object_or_404(Space, pk=pk, managed_by=request.user)

    if request.method == 'POST':
        form = EditSpaceForm(request.POST, request.FILES, instance=space)

        if form.is_valid():
            form.save()

            return redirect('space:detail', pk=space.id)
    else:
        form = EditSpaceForm(instance=space)

    return render(request, 'space/form.html', {
        'form': form,
        'title': 'Edit',
        'space': space,
    })

@login_required
def edit_pop(request, pk):
    space = get_object_or_404(Space, pk=pk, managed_by=request.user)

    if request.method == 'POST':
        form = EditSpaceForm(request.POST, request.FILES, instance=space)

        if form.is_valid():
            form.save()

            return redirect('space:detail', pk=space.id)
    else:
        form = EditSpaceForm(instance=space)

    return render(request, 'space/detail.html', {
        'form': form,
        'title': 'Edit',
        'space': space,
    })

@login_required
def add_space(request):
    if request.method == 'POST':
        form = SpaceForm(request.POST, request.FILES)
        if form.is_valid():
            space = form.save(commit=False)
            space.managed_by = request.user  
            space.schedule = 'abcdefghijklmnop'
            space.book_count = 0
            space.save()
            form.save_m2m() 
            return redirect('space:detail', space.id)
        else:
            print(form.errors)
    else:
        form = SpaceForm()
    
    return render(request, 'space/add_space.html', {'form': form})
