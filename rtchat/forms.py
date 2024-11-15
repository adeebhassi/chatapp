from django.forms import ModelForm
from django import forms
from .models import GroupMessage,ChatGroup

class chatMessageForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields=['message']
        widgets={
            'message': forms.TextInput(attrs={'placeholder': 'Add message...','class':'p-4 text-black','max-length:':'300', 'rows': 1,'auto-focus':True})
        }
        
        
class NewGroupForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields=['groupchat_name']
        widgets={
            'groupchat_name': forms.TextInput(attrs={'placeholder': 'Add group name...','class':'p-4 text-black','max-length':'300','autofocus':True})
        }