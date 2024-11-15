from django.db import models
from django.contrib.auth.models import User
import shortuuid
# Create your models here.
class ChatGroup(models.Model):
    name = models.CharField(max_length=255,default=shortuuid.uuid)
    users_online=models.ManyToManyField(User,related_name='online_in_group',blank=True)
    groupchat_name=models.CharField(max_length=100,null=True,blank=True)
    admin=models.ForeignKey(User,related_name='groupchats',blank=True,null=True,on_delete=models.CASCADE)
    members=models.ManyToManyField(User,related_name='chat_groups',blank=True)
    is_private=models.BooleanField(default=False)
    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE,related_name='group_msgs')
    message = models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.author.username} : {self.message}'
    
    class Meta:
        ordering = ['-created_at']