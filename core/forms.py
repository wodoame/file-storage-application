from django import forms
from .models import File, Folder
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UploadFileForm(forms.ModelForm):
    class Meta: 
        model = File
        fields = '__all__'

class CreateFolderForm(forms.ModelForm):
    class Meta: 
        model = Folder
        fields = '__all__'
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']