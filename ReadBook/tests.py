from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserInfo,Book,Transaction,Review

# Create your tests here.

class ModelTestCase(TestCase):

  #setting Up variables
  def setUp(self):
    self.user = User.objects.create_user(username = "Sora99",password = "12345678",email = "sora99@gmail.com")
    self.user1 = UserInfo.objects.create(users = self.user,user_amount = 100,user_type = "Author")
    self.book1 = Book.objects.create(book_name="test",book_price=0 ,book_type="Free",book_cover='testing\\testing.jpg',book_description="test description",book_category="category1",book_file="testing\\testing.pdf",uploaded_by_id=self.user1.pk)

  #Test code For UserInfo 
  def test_validate_UserInfo(self):
    self.assertTrue(self.user1.validate_UserInfo())
  
  #Test code For Book Model 
  def test_uploaded_file(self):
    self.assertTrue(self.book1.check_uploaded_file())
  
  #Test code For Book Model 
  def test_validate_BookRating(self):
    self.assertTrue(self.book1.validate_book_rating())
  
  #Test code For Transaction Model
  def test_validate_transaction_total(self):
    transaction1 = Transaction.objects.create(book = self.book1,user = self.user1,price= 200 ,discount = 57,total = 143)
    self.assertEqual(transaction1.validate_transaction_total(),transaction1.total)
  
  #Test code For Review Model 
  def test_count_review_of_user(self):
    review1 = Review.objects.create(book = self.book1,rating = 4,review = "TestReview",user=self.user1)
    self.assertTrue(review1.validate_rewiew_count())
  
  #Test code For Review Model
  def test_validate_user_rating(self):
    review1 = Review.objects.create(book = self.book1,rating = 4,review = "TestReview",user=self.user1)
    self.assertTrue(review1.validate_user_rating())

