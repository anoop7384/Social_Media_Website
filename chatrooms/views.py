from django.shortcuts import render, redirect
from .models import ChatRoom, Message
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.


def chatroom(request, pk):
    obj = User.objects.get(pk=pk)
    sender_room, screated = ChatRoom.objects.get_or_create(
        sender=request.user, receiver=obj)
    if (request.method == 'POST'):
        text = request.POST.get('textfield')
        print(text)
        receiver_room, rcreated = ChatRoom.objects.get_or_create(
            receiver=request.user, sender=obj)
        sender_room.last_text=text
        receiver_room.last_text=text
        sender_room.last_time = timezone.now()
        receiver_room.last_time = timezone.now()
        sender_room.save()
        receiver_room.save()
        sender_message = Message.objects.create(
            sender=request.user, receiver=obj, chatroom=sender_room, content=text, timestamp=timezone.now())
        receiver_message = Message.objects.create(
            sender=request.user, receiver=obj, chatroom=receiver_room, content=text, timestamp=timezone.now())
        sender_message.save()
        receiver_message.save()

    messages = Message.objects.filter(chatroom=sender_room)
    context = {
        'title': 'Chat',
        'account': obj,
        'user': request.user,
        'messages': messages
    }
    return render(request, 'chatrooms/chat.html', context)
