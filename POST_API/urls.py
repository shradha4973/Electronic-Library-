from django.urls import path, include
from . import views

app_name = "POST_API"

urlpatterns = [
    path('addbook/',views.addBook,name='addbook')
]