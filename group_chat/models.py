
from django.db import models
from admin_module.views import User
class Group(models.Model):
    name = models.CharField(max_length=255)
    group_members = models.ManyToManyField(User, related_name='group_memberships')
    is_active = models.BooleanField(default=True) 
    creator=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    
class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_messages', blank=True)

    def __str__(self):
        return self.group.name