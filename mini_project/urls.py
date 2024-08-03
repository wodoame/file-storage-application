"""
URL configuration for mini_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views
from components.testButton.testButton import testButton

urlpatterns = [
    path('admin/', admin.site.urls),
    path('components/', include('components.urls')),
    path('', views.Index.as_view(), name='index'), # * For testing might be removed soon
    path('test/', views.Test.as_view(), name='test'),
    path('test-login/', views.TestLogin.as_view(), name='test-login'),
    path('test-signup/', views.TestSignup.as_view(), name='test-signup'),
    path('get-icon/', views.getIcon.as_view()),
    path('search/', views.Search.as_view()),
    path('delete/', views.DeleteFileOrFolder.as_view(), name='delete'),
    path('upload-file/<uuid:id>/', views.UploadFile.as_view(), name='upload-file'),
    path('download/<uuid:id>/', views.DownloadFile.as_view(), name='download'),
    path('<str:username>/', views.Home.as_view(), name='home'),
    path('<str:username>/<uuid:id>/', views.Files.as_view(), name='files'), # * For testing
    path('render-files/<str:username>/<uuid:id>/', views.RenderFiles.as_view()),
    path('render-path/<str:username>/<uuid:id>/', views.RenderPath.as_view()),
    path('components/testButton/', testButton.as_view()),
]
