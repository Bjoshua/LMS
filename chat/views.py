from django.shortcuts import render, redirect
from users.models import *
from .models import *
from django.contrib import messages
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
# Create your views here.

        

        
def display_room(request, room_id):
    room = Room.objects.get(id=room_id)
    messages = Messages.objects.filter(room=room)
    members = room.members.all
    if request.method == "POST":
        get_messages = request.POST.get('message')
        get_file = request.POST.get('message_file')
        get_image = request.POST.get('message_image')
        room = Room.objects.get(id=room_id)
        sender = request.user
        message = Messages.objects.create(message=get_messages, sender=sender, room=room, message_file=get_file, message_image=get_image)
        message.save()
    if messages.exists():
        context ={
            'room':room,
            'messages':messages,
            'members':members,
        }
        return render(request, 'chat_room.html', context)
    else:
        context ={
            'room':room,
            'messages':messages,
            'members':members,

        }
        return render(request, 'chat_room.html', context)
def delete_message(request, room_id, message_id):
    message = Messages.objects.get(id=message_id)
    message.delete()
    return redirect(display_room, room_id)
def delete_message_personal(request, message_id, receiver_pk):
    receiver = CustomUser.objects.get(id=receiver_pk)
    message = Personal_messages.objects.get(id=message_id)
    message.delete()
    return redirect(Sendpersonalmessage, receiver_pk=receiver_pk)
def edit_message(request, room_id, message_id):
    message_edit = Messages.objects.get(id=message_id)
    room = Room.objects.get(id=room_id)
    messages = Messages.objects.filter(room=room)
    members = room.members.all

    if request.method=="POST":
        get_message = request.POST.get("message")
        new_message = Messages.objects.get(id=message_id)
        new_message.message=get_message
        new_message.save()
        return redirect(display_room, room_id)
    context ={
            'room':room,
            'messages':messages,
            'message_edit':message_edit,
            'members':members,

        }
    return render(request, 'edit_message.html', context)
def edit_message_personal(request, receiver_pk, message_id):
    message_edit = Personal_messages.objects.get(id=message_id)
    receiver = CustomUser.objects.get(id=receiver_pk)
    users = CustomUser.objects.all()
    get_messages = Personal_messages.objects.filter(sender=request.user, receiver=receiver) | Personal_messages.objects.filter(sender=receiver, receiver=request.user) 
    messages = get_messages.order_by('created_at')
    if request.method=="POST":
        get_message = request.POST.get("message")
        new_message = Personal_messages.objects.get(id=message_id)
        new_message.message=get_message
        new_message.save()
        return redirect(Sendpersonalmessage, receiver_pk)
    context ={
            'messages':messages,
            'message_edit':message_edit,

        }
    return render(request, 'edit_form.html', context)
def Chatroom(request):
    users = CustomUser.objects.all()
    context = {
        'users' : users,
    }
    return render(request, 'p_chat_room.html', context)
@login_required(login_url='login')
def Sendpersonalmessage(request, receiver_pk):
    receiver = CustomUser.objects.get(id=receiver_pk)
    users = CustomUser.objects.all()
    get_messages = Personal_messages.objects.filter(sender=request.user, receiver=receiver) | Personal_messages.objects.filter(sender=receiver, receiver=request.user) 
    messages = get_messages.order_by('created_at')
    print('receiver: ', receiver)
    print('users: ', users)
    if request.method == "POST":
        get_messages = request.POST.get('message')
        get_file = request.POST.get('message_file')
        get_image = request.POST.get('message_image')
        sender = request.user
        message = Personal_messages.objects.create(message=get_messages, sender=sender, receiver=receiver, message_file=get_file, message_image=get_image)
        message.save()
        return redirect(Sendpersonalmessage, receiver_pk=receiver_pk)
    context = {
        'receiver' : receiver,
        'messages' : messages,
        'users' : users,
    }
    return render(request, 'personal_form.html', context)
        


def check_for_new_messages(request):
    last_check = request.session.get('last_check_for_new_messages', None)
    if last_check is None:
        request.session['last_check_for_new_messages'] = timezone.now().isoformat()
        return JsonResponse({'new_messages': False})

    new_messages = Message.objects.filter(datetime=last_check).exists()
    request.session['last_check_for_new_messages'] = timezone.now().isoformat()
    return JsonResponse({'new_messages': new_messages})
