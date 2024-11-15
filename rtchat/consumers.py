from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import *
from django.template.loader import render_to_string
import json
from asgiref.sync import async_to_sync
class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user=self.scope['user']
        self.chatroom_name=self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom=get_object_or_404(ChatGroup,name=self.chatroom_name)
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,self.channel_name
        )
        
        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()
        self.accept()
        
    def receive(self, text_data):
        text_data_json=json.loads(text_data)
        message_body=text_data_json['message']
        message=GroupMessage.objects.create(
            group=self.chatroom,
            author=self.user,
            message=message_body 
        )
        event={
            'type':'message_handler',
            'message_id':message.id
        }
        
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,event
        )
    
    def message_handler(self,event):
        message_id=event['message_id']
        message=GroupMessage.objects.get(id=message_id)
        context={
            'message':message,
            'user':self.user
        }
        html=render_to_string('rtchat/partials/chat_message_p.html',context=context)
        self.send(text_data=html)
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,self.channel_name
        )
        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()
            
    def update_online_count(self):
        online_count=self.chatroom.users_online.count()
        event={
            'type':'online_count_handler',
            'online_count':online_count
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,event
        )
    def online_count_handler(self,event):
        context={
            'online_count':event['online_count'],
            'chat_group':self.chatroom
        }
        html=render_to_string('rtchat/partials/online_count.html',context=context)
        self.send(text_data=html)