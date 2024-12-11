from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from space.models import Space
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Conversation
from .forms import ConversationMessageForm
from django.contrib import messages
from notifications.models import Notification

from django.http import JsonResponse

def new_conversation(request, space_pk):
    space = get_object_or_404(Space, pk=space_pk)

    if space.managed_by == request.user:
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(space=space).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(space=space)
            conversation.members.add(request.user)
            conversation.members.add(space.managed_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            target_user = request.user
            admin_user = space.managed_by

            notification = Notification.objects.create(
                notification_type='message',
                sender=target_user,
                receiver=admin_user,
                message=f'New message from {request.user.username}.',
                link = f'/inbox/{conversation.id}/'
            )

            return redirect('space:detail', pk=space_pk)
    else:
        form = ConversationMessageForm() 
        
    return render(request, 'conversation/new.html', {
        'form': form,

    })

@login_required
def inbox(request):
    # Get query parameters
    search_query = request.GET.get('search', '')
    filter_type = request.GET.get('filter', '')
    
    # Base queryset
    conversations = Conversation.objects.filter(
        members=request.user
    ).order_by('-modified_at')
    
    # Apply search
    if search_query:
        conversations = conversations.filter(
            Q(members__username__icontains=search_query) |
            Q(space__title__icontains=search_query) |
            Q(messages__content__icontains=search_query)
        ).distinct()
    
    # Apply filters
    if filter_type == 'unread':
        conversations = conversations.filter(is_read=False)
    elif filter_type == 'read':
        conversations = conversations.filter(is_read=True)
    elif filter_type == 'latest':
        conversations = conversations.order_by('-modified_at')
    
    # Pagination
    paginator = Paginator(conversations, 10)  # 10 conversations per page
    page_number = request.GET.get('page', 1)
    conversations = paginator.get_page(page_number)
    
    context = {
        'conversations': conversations,
        'today': timezone.now(),
        'search_query': search_query,
        'filter_type': filter_type,
    }
    
    return render(request, 'conversation/inbox.html', context)

@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form,
    })

@csrf_exempt 
def mark_as_read(request):
    if request.method == "POST":
        conversation_id = request.POST.get('conversation_id')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            conversation.is_read = True
            conversation.save()
            return JsonResponse({'status': 'success'})
        except Conversation.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Conversation not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def conversation(request, space_id):
    space = get_object_or_404(Space, id=space_id)
    conversation = get_object_or_404(Conversation, space=space)

    context = {
        'space': space,
        'conversation': conversation,
    }
    return render(request, 'conversation/detail.html', context)

@login_required
def delete_conversation(request, conversation_id):
    # Get the conversation object or return a 404 if not found
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Check if the logged-in user is a member of the conversation
    if request.user not in conversation.members.all():
        messages.error(request, "You do not have permission to delete this conversation.")
        return redirect('conversation:inbox') 
    
    conversation.delete()

    # Show a success message
    messages.success(request, "Conversation deleted successfully.")
    return redirect('conversation:inbox')  # Redirect to the inbox after deletion