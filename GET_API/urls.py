from django.urls import path,include
from . import views

app_name = "GET_API"

urlpatterns = [
  path('book/id=<int:id>/',views.getBook,name="getBook"),
  path('book/',views.getAllBook,name="getAllBook"),
  path('book/page=<int:page>/size=<int:size>/',views.getBookOfPage,name="getBookOfPage"),
  #review
  path('review/book=<int:bookid>/',views.getAllReview,name="getAllReview"),
  path('review/book=<int:bookid>/page=<int:page>/size=<int:size>/',views.getReviewOfPage,name="getReviewOfPage"),
  #search
  path('book/search/',views.search,name="getReview"),
]