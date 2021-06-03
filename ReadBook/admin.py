from django.contrib import admin
from .models import Book,Transaction,Review,UserInfo
# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Book)
admin.site.register(Transaction)
admin.site.register(Review)