from django.contrib import admin
from django.urls import path
from . import views
app_name= 'Search'
urlpatterns = [
	path('search/', views.search, name='search'),
]

