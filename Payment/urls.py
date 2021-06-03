from django.contrib import admin
from django.urls import path
from . import views 

app_name = 'Payment'

urlpatterns = [
	path('getbook/<int:id>', views.getBook, name= 'getBook'),
	path('payment/<int:bid>', views.payment, name ='Payment'),
	path('updateamount/', views.update_amount, name ='updateamount'),
]