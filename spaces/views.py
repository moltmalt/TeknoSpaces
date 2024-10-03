from django.shortcuts import render
from .models import Space

def spaces_list(request):
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    spaces = Space.objects.all()

    if query:
        spaces = spaces.filter(title__icontains=query)  # for title
    
    if category:
        spaces = spaces.filter(tag__icontains=category)  # for category based on tag

    context = {
        'spaces': spaces,
        'search_query': query,
        'category': category,
    }
    
    return render(request, 'spaces.html', context)