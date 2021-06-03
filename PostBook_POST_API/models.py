from django.db import models

class BookPost(models.Model):
  book_name = models.CharField(max_length=50)
  book_price = models.IntegerField(default=0)
  book_description = models.TextField()
  
  def __str__(self):
    return str(self.book_name)
