from django.shortcuts import get_object_or_404, redirect
from .forms import BookingForm
from .models import Booking, Space
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json
from django.shortcuts import render
from datetime import datetime, timedelta
import json, re
from django.contrib import messages
from notifications.models import Notification
from django.contrib.auth import get_user_model


User = get_user_model()

@login_required
def calendar_view(request, space_id):
    space = get_object_or_404(Space, id=space_id)
    bookings = Booking.objects.filter(space=space)
    bookings_json = json.dumps([{
        'title': booking.id,
        'start': f"{booking.date}T{booking.start_time}",
        'end': f"{booking.date}T{booking.end_time}",
    } for booking in bookings])
    
    selected_date = request.POST.get('selected_date')
    selected_slots = request.POST.get('selected_slots', '')
    
    time_slots = [
        '08:00-09:00', '09:00-10:00', '10:00-11:00', '11:00-12:00',
        '12:00-13:00', '13:00-14:00', '14:00-15:00', '15:00-16:00', '16:00-17:00'
    ]

    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        selected_date = request.POST.get('selected_date')  # Get the selected date
        selected_slots = request.POST.get('selected_slots')  # Get the string of selected slots, e.g. '9:00-10:00,10:00-11:00'

        print(f'1. SELECTED DATE: {selected_date}')
        print(f'1. SELECTED SLOTS: {selected_slots}')

        if form.is_valid():
            # Split the selected slots by commas to get each time range individually
            selected_slots_list = selected_slots.split(',')
            
            # Step 1: Sort the slots to ensure they are in chronological order
            selected_slots_list.sort()

            # Step 2: Merge consecutive slots
            merged_slots = []
            current_start_time = None
            current_end_time = None

            for selected_slot in selected_slots_list:
                try:
                    # Validate the slot format using regex (e.g., '8:00-9:00' or '08:00-09:00')
                    if not re.match(r'^[0-9]{1,2}:[0-9]{2}-[0-9]{1,2}:[0-9]{2}$', selected_slot):
                        print(f"Skipping invalid format: {selected_slot}")
                        continue  # Skip invalid format slots

                    # Split the time range (e.g., '8:00-9:00') into start and end times
                    start_time_str, end_time_str = selected_slot.split('-')

                    # Ensure the times are formatted correctly (e.g., '8' becomes '08:00')
                    start_time_str = f"{int(start_time_str.split(':')[0]):02}:{start_time_str.split(':')[1]}"
                    end_time_str = f"{int(end_time_str.split(':')[0]):02}:{end_time_str.split(':')[1]}"

                    # Parse the time strings into datetime objects
                    start_time = datetime.strptime(start_time_str, "%H:%M").time()
                    end_time = datetime.strptime(end_time_str, "%H:%M").time()

                    # Check if this slot is consecutive with the previous one
                    if current_end_time and start_time == current_end_time:
                        # Extend the end time to the new slot's end time
                        current_end_time = end_time
                    else:
                        # Add the previous slot to the merged slots
                        if current_start_time:
                            merged_slots.append(f"{current_start_time.strftime('%H:%M')}-{current_end_time.strftime('%H:%M')}")
                        
                        # Start a new slot
                        current_start_time = start_time
                        current_end_time = end_time

                except ValueError as e:
                    print(f"ValueError: {e} for selected slot: {selected_slot}")
                    continue  # Skip invalid slot formats

            # Add the last merged slot
            if current_start_time:
                merged_slots.append(f"{current_start_time.strftime('%H:%M')}-{current_end_time.strftime('%H:%M')}")

            print(f"Merged Slots: {merged_slots}")

            # Step 3: Create bookings for the merged slots
            for merged_slot in merged_slots:
                try:
                    start_time_str, end_time_str = merged_slot.split('-')

                    # Parse the time strings into datetime objects
                    start_time = datetime.strptime(start_time_str, "%H:%M").time()
                    end_time = datetime.strptime(end_time_str, "%H:%M").time()

                    # Create the booking entry
                    Booking.objects.create(
                        user=request.user,
                        space=space,
                        date=selected_date,
                        start_time=start_time,
                        end_time=end_time,
                        request_letter=form.cleaned_data['request_letter']
                    )

                    notification = Notification.objects.create(
                        notification_type='booking_sent',
                        sender=request.user,
                        receiver=space.managed_by,
                        message = f'A new booking request has been sent from {request.user.username} for {space.title}.',
                        link = f'/spaces/{space.id}/'
                    )

                except ValueError as e:
                    print(f"ValueError: {e} for merged slot: {merged_slot}")
                    continue  # Skip invalid slot formats

            messages.success(request, 'Your booking has been successfully created.')
            return redirect('dashboard:index') 
        else:
            pass
    
    booked_slots = []

    if selected_date:
        print(f"Space: {space} (Type: {type(space)})")
        print(f"Selected Date: {selected_date} (Type: {type(selected_date)})")

        # Filter bookings for the specific date and for the pending status
        bookings = Booking.objects.filter(
            space=space,
            date=datetime.strptime(selected_date, '%Y-%m-%d').date(),
            status="pending"  # Ensure this checks for pending status
        ).values_list('start_time', 'end_time')

        # Debugging: Print the actual query
        print(f"Query: {bookings.query}")

        # Debugging: Print retrieved bookings
        print(f'Retrieved Bookings: {list(bookings)}')

        # Split each booking into hourly intervals and format them
        for start_time, end_time in bookings:
            booked_slots.extend(split_into_hourly_intervals(start_time, end_time))

    print(f'Booked Slots: {booked_slots}')

    approved_slots = []

    if selected_date:
        # Filter bookings for the specific date and for the approved status
        approved_slots_query = Booking.objects.filter(
            space=space,
            date=datetime.strptime(selected_date, '%Y-%m-%d').date(),
            status='approved'  # Ensure this checks for approved status
        ).values_list('start_time', 'end_time')

        print(f"Query 2: {approved_slots_query.query}")
        print(f'Retrieved Bookings: {list(approved_slots_query)}')

        # Loop through each booking and split into hourly intervals
        for start_time, end_time in approved_slots_query:
            approved_slots.extend(split_into_hourly_intervals(start_time, end_time))

    print(f'Approved Slots: {approved_slots}')
    
    context = {
        'space': space,
        'bookings': bookings,
        'bookings_json': bookings_json,
        'selected_date': selected_date,
        'selected_slots': selected_slots,
        'time_slots': time_slots,
        'booked_slots': booked_slots,
        'approved_slots': approved_slots,
    }
    return render(request, 'calendar.html', context)

def space_booking(request, space_id):
    space = Space.objects.get(id=space_id)
    today = datetime.now()
    min_booking_date = today + timedelta(days=3)
    
    # Fetch all bookings for this space
    bookings = Booking.objects.filter(space=space, date__gte=today).values('date', 'start_time', 'end_time')
    
    # Convert bookings to JSON format
    bookings_json = json.dumps(list(bookings))
    
    return render(request, 'calendar.html', {
        'space': space,
        'bookings_json': bookings_json,
        'min_booking_date': min_booking_date.strftime('%Y-%m-%d')
    })

@login_required
def booking_view(request, space_id):
    # Get the space or return a 404 error if not found
    space = get_object_or_404(Space, id=space_id)

    
    # Render the template with the form
    context = {
        'space': space,
    }
    return render(request, 'calendar.html', context)

def merge_consecutive_slots(selected_slots_list):
    # Sort slots to ensure they are in chronological order
    selected_slots_list.sort()

    merged_slots = []
    current_start_time = None
    current_end_time = None

    for selected_slot in selected_slots_list:
        try:
            # Validate the slot format using regex (e.g., '8:00-9:00' or '08:00-09:00')
            if not re.match(r'^[0-9]{1,2}:[0-9]{2}-[0-9]{1,2}:[0-9]{2}$', selected_slot):
                print(f"Skipping invalid format: {selected_slot}")
                continue  # Skip invalid format slots

            # Split the time range (e.g., '8:00-9:00') into start and end times
            start_time_str, end_time_str = selected_slot.split('-')

            # Ensure the times are formatted correctly (e.g., '8' becomes '08:00')
            start_time_str = f"{int(start_time_str.split(':')[0]):02}:{start_time_str.split(':')[1]}"
            end_time_str = f"{int(end_time_str.split(':')[0]):02}:{end_time_str.split(':')[1]}"

            # Parse the time strings into datetime objects
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()

            # Check if this slot is consecutive with the previous one
            if current_end_time and start_time == current_end_time:
                # Extend the end time to the new slot's end time
                current_end_time = end_time
            else:
                # Add the previous slot to the merged slots
                if current_start_time:
                    merged_slots.append(f"{current_start_time.strftime('%H:%M')}-{current_end_time.strftime('%H:%M')}")
                
                # Start a new slot
                current_start_time = start_time
                current_end_time = end_time

        except ValueError as e:
            print(f"ValueError: {e} for selected slot: {selected_slot}")
            continue  # Skip invalid slot formats

    # Add the last merged slot
    if current_start_time:
        merged_slots.append(f"{current_start_time.strftime('%H:%M')}-{current_end_time.strftime('%H:%M')}")

    return merged_slots

def split_into_hourly_intervals(start_time, end_time):
    # Convert time objects to datetime objects for manipulation
    start_datetime = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)
    
    # Initialize a list to store the hourly intervals
    intervals = []
    
    # Loop and add hourly intervals
    while start_datetime < end_datetime:
        next_hour = start_datetime + timedelta(hours=1)
        
        # Ensure the end of the interval is within the requested range
        if next_hour > end_datetime:
            next_hour = end_datetime

        # Convert back to time objects for the interval
        intervals.append(f"{start_datetime.strftime('%H:%M')}-{next_hour.strftime('%H:%M')}")
        
        # Move to the next hour
        start_datetime = next_hour
    
    return intervals
