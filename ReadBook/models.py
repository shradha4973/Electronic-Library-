from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.


class UserInfo(models.Model):
    # linking to user model through one to one relation
    users = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional
    user_type = models.CharField(max_length=6)
    user_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.users.username
    
    #Test Case
    def validate_UserInfo(self):
        return self.user_amount > 0 and (self.user_type == "Author" or self.user_type == "Reader")

class Book(models.Model):
    book_name = models.CharField(max_length=50)
    uploaded_by = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    book_price = models.IntegerField(default=0)
    book_type = models.CharField(max_length=10)
    book_discount = models.IntegerField(default=0)
    book_cover = models.ImageField(upload_to='book_images/')
    book_description = models.TextField()
    book_category = models.CharField(max_length=30)
    book_file = models.FileField(upload_to='book/')
    book_rating = models.SmallIntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.book_name)

    #overriding delete method
    def delete(self, *args, **kwargs):
        self.book_file.delete()
        self.book_cover.delete()
        super().delete(*args, **kwargs)  # Call the "real" delete() method.
    
    #Test Case
    def check_uploaded_file(self):
        return os.path.exists(self.book_file.path) and os.path.exists(self.book_cover.path)
    
    #Test Case
    def validate_book_rating(self):
        return  self.book_rating >= 0 or self.book_rating <=5


class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(default=0)
    total = models.IntegerField()

    def __str__(self):
        return str(self.book) + " ==> " + str(self.user)

    #Test Case
    def validate_transaction_total(self):
        return self.price - self.discount

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)
    review = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.book) + " - " + str(self.user) + " - " + str(self.rating)
    
    #Test Case
    def validate_rewiew_count(self):
        count = Review.objects.filter(user = self.user).count()
        return count == 1

    #Test Case
    def validate_user_rating(self):
        return  self.rating >= 0 or self.rating <= 5
    