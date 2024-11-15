from django.urls import path
from .consumers import *
websockets_urlpatterns=[
    path('ws/chatroom/<chatroom_name>',ChatroomConsumer.as_asgi())
]