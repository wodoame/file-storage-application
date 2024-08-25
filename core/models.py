from typing import Iterable
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

class AbstractModel(models.Model): 
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    class Meta:
        abstract = True 

class Folder(AbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders', blank=True)
    folder = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_folders', null=True, blank=True)
    name = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def isFolder(self): 
        return True
    
    def __str__(self) -> str:
        return self.user.username + ' ' + self.name


class File(AbstractModel):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    name = models.CharField(max_length=125, null=True, blank=True)
    file = models.FileField(upload_to='files/')
    extension = models.CharField(max_length=10, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def isFolder(self): 
        return False

# * This model extends the user model through a one-to-one relationship by including other properties that cannot be directly added to the built-in user model
class Profile(AbstractModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpeg')
    
    def __str__(self) -> str:
        return self.user.username + ' profile'