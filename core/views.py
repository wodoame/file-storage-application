from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from .forms import UploadFileForm, CreateFolderForm, CreateUserForm
from .models import File, Folder, Profile
from .utils import getExtension, getPath, getSVG, checkOwnership
from .components import renderFiles, renderPath, generateSearch

# load the intial page
class Home(View):
    def get(self, request, username):
        get_object_or_404(User, username=username)
        rootFolder = Folder.objects.get(name='root', user__username=username)
        context = {'page':'home', 'username': username, 'id':rootFolder.id}
        return render(request,'index.html', context)

# redirects a user to his home page if he is authenticated or to the login  page otherwise
class Index(View):
    def get(self, request):
        if request.user.is_authenticated: 
            return redirect(reverse('home', args=[request.user.username]))
        return redirect('test-login')


from components.alertButton.alertButton import alertButton
class Test(View):
    def get(self, request):
        # print(alertButton.render()) # * I'm trying to do server side rendering with the django-components library. 
        # * This is getting the rendered html
        # * The component itself can be made a view so this may not be necessary
        context = {}
        return render(request, 'test.html', context) 

# processes an uploaded file
class UploadFile(View):
    def get(self, request):
        context = {'page': 'upload-file'}
        return render(request, 'upload-file.html', context)
    
    def post(self, request, id):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid(): 
            folder = Folder.objects.get(id=id)
            file: InMemoryUploadedFile = request.FILES.get('file')
            instance: File = form.save(commit=False)
            instance.name = file.name
            instance.folder = folder
            instance.extension = getExtension(file.name)
            form.save()
        else:
            print(form.errors.as_data())
        return redirect(reverse('files', args=[request.user.username, id]))
    
    # * An uploaded file can be handled by some method
    def handleUploadedFile(self, f):
       pass

# handles file downloads
import os
class DownloadFile(View):
    def get(self, request, id): 
        file = File.objects.get(id=id).file
        response = HttpResponse(file, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file.name)}"'
        return response
    
# * This view displays the files page but it not directly responsible for rendering the file and folder icons on the page
class Files(View):
    template = 'files.html'
    
    def get(self, request, username, id): 
        context = {'page': 'my-files', 'username': username,  'id': id, 'isOwner': checkOwnership(request, username)}
        return render(request, 'files.html', context)
    
    def post(self, request, username, id):
        print(request.POST)
        form = CreateFolderForm(request.POST)
        if form.is_valid(): 
            folder = form.save(commit=False)
            folder.user = request.user
            folder.folder = Folder.objects.get(id=id) # assigning it a parent folder
            form.save() 
        else: 
            print(form.errors.as_data())
        return self.get(request, username, id)

# * This view renders the file and folder icons on the page
class RenderFiles(View):
    def get(self, request, username, id):
        html = renderFiles(request, username, id)
        return HttpResponse(html)

# This renders the path breadcrumb in the UI
from collections import deque
class RenderPath(View):
    def get(self, request, username, id):
        path, ids = getPath(Folder.objects.get(id=id), deque())
        html = renderPath(path.removesuffix('/'), ids, username) # remove the trailing / since renderPath function splits by that
        return HttpResponse(html)
    
# Helps you get an icon for a file
class getIcon(View): 
    def get(self, request):
        filename = request.GET.get('filename')
        extension = getExtension(filename)
        html = getSVG(extension)
        return HttpResponse(html)

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

# Handles the login page
class TestLogin(View):
    template = 'login.html'
    
    def get(self, request):
        return render(request, self.template)
    
    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        print(request.POST)
        context = {} 
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else: 
            username = request.POST.get('username')
            context = {'invalidCredentials': True, 'username': username}
        return render(request, self.template, context)

# Handles the signup page
class TestSignup(View):
    template = 'signup.html'
    def get(self, request):
        # use the UserCreationForm 
        # when a user is created make sure to create a root folder for the user
        return render(request, self.template)
    
    def post(self, request): 
        print(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        form = CreateUserForm(request.POST)
        if form.is_valid(): 
            user = form.save()
            Profile.objects.create(user=user)
            Folder.objects.create(name='root', user=user)
            return redirect('test-login')
        # print(form.errors.get_json_data().values())
        # print(form.errors.values())
        jsonData = form.errors.get_json_data().values()
        errors = []
        for errorType in jsonData: 
            for error in errorType: 
                errors.append(error.get('message'))
        return render(request, self.template, {'errors': errors, 'username': username, 'email': email})

from django.contrib.auth import logout
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('test-login')


# Handles the search
class Search(View):
    def get(self, request): 
        q = request.GET.get('q')
        id = request.GET.get('folder_id')
        html = generateSearch(q, id)
        return HttpResponse(html)    

class DeleteFileOrFolder(View):
    def get(self, request):
        id = request.GET.get('id')
        objectType = request.GET.get('type')
        if objectType == 'folder': 
            self.recursiveDelete(Folder.objects.get(id=id))
        else: 
            file = File.objects.get(id=id)
            os.remove(file.file.path) # delete the actual file
            file.delete() # delete the model instance
        return redirect(request.META.get('HTTP_REFERER'))
    
    # * recursively delete the folder as well as every file and folder inside it
    def recursiveDelete(self, folder):
        files = folder.files.all()
        subFolders = folder.sub_folders.all()
        for file in files:
            os.remove(file.file.path)
            file.delete() # delete the database record of the file

        for subFolder in subFolders:
            self.recursiveDelete(subFolder)
        
        folder.delete() # delete the database record of the parent folder

class UploadImage(View):
    def post(self, request): 
        userData, created = Profile.objects.get_or_create(user=request.user)
        userData.profile_pic = request.FILES.get('profile-image')
        userData.save()
        return redirect(request.META.get('HTTP_REFERER'))
    
    
        
    