from django.urls import path,include
from . import views

app_name = "DELETE_API"

urlpatterns = [
  path('delete/book=<int:id>/',views.deleteBook,name="deleteBook"),

]