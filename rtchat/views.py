from django.contrib import messages
from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import chatMessageForm,NewGroupForm
from django.http import Http404

# Create your views here.
@login_required
def chat_view(request,chatroom_name='public-group'):
    chat_group=get_object_or_404(ChatGroup,name=chatroom_name)
    group_msg=chat_group.group_msgs.all()
    form=chatMessageForm()
    other_user=None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user=member
                break
    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
            if request.user.emailaddress_set.filter(verified=True).exists():
                chat_group.members.add(request.user)
            else:
                print("here id is",chat_group.id)
                request.session['chat_group_id'] = chat_group.id
                print("id is",request.session['chat_group_id'])
                messages.warning(request,"First you need to verify your email")
                return redirect('profile-settings')
            
    if request.htmx:
        form=chatMessageForm(request.POST)
        if form.is_valid:
            message=form.save(commit=False)
            message.author=request.user
            message.group=chat_group
            message.save()
            form=chatMessageForm()
            context={
                'message':message,
                'user':request.user
            }
            return render(request,'rtchat/partials/chat_message_p.html',context)
    context={
        'group_msg':group_msg,
        'chat_group':chat_group,
        'form':form,
        'other_user':other_user,
        'chatroom_name':chatroom_name
    }
    return render(request, 'rtchat/chat.html',context)


@login_required
def get_or_create_chat(request,username):
    if request.user.username==username:
        print("this is")
        return redirect('home')
    other_user=User.objects.get(username=username)
    my_chatrooms=request.user.chat_groups.filter(is_private=True)
    
    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom=chatroom
                break
            else:
                chatroom=ChatGroup.objects.create(is_private=True)
                chatroom.members.add(other_user,request.user)
    else:
        chatroom=ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user,request.user)
        
    return redirect('chatroom',chatroom.name)

@login_required
def new_chatgroup(request):

    groupForm=NewGroupForm()
    if request.method=='POST':
        groupForm=NewGroupForm(request.POST)
  
        if groupForm.is_valid():
        
            group=groupForm.save(commit=False)
            group.admin=request.user
            group.save()
            group.members.add(request.user)
     
            return redirect('chatroom',group.name)
    context={
        'form':groupForm
    }
    return render(request,'rtchat/chatgroup.html',context)

