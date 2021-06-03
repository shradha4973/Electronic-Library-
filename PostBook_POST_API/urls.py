from django.urls import path, include
from . import views

app_name = "POST_BOOK"

urlpatterns = [
    path('postbook/',views.postbook,name='postbook')
]