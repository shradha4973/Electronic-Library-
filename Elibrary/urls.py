"""Elibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #add include to your apps url.py
    path('',include('ReadBook.urls')),
    path('',include('Payment.urls')),
    path('',include('Search.urls')),
    path('', include('Accounts.urls')),
    path('api/',include('GET_API.urls')),
    path('api/',include('DELETE_API.urls')),
    path('api/',include('PUT_API.urls')),
    path('api/',include('POST_API.urls')),
    path('api/',include('PostBook_POST_API.urls')),
]
