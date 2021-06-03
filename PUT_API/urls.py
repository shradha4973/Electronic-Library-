from django.urls import path, include
from . import views

app_name = "PUT_API"

urlpatterns = [
    path('updatebook/id=<int:bookid>/', views.updateBook, name='updatebook'),
]