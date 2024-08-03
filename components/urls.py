from django.urls import path
from .files.files import Files

urlpatterns = [
    path('files/<str:username>/<uuid:id>/', Files.as_view()),
]