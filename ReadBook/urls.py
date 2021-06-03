from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "ReadBook"

urlpatterns = [
    path('', views.loadBook, name='premiumbook'),
    path('description/<int:bid>/', views.bookDescription, name='description'),
    path('addbook/', views.addBook, name='addbook'),
    path('review/<int:bid>/', views.review, name="review"),
    path('rating/<int:bid>/', views.rating, name='rating'),
    path('delete/<int:bid>/',views.deleteBook, name='deletebook'),
    path('update/<int:bid>/',views.updateBook, name='updateBook'),
    path('download/<int:bid>/',views.download, name='download'),
    path('mybooks/',views.booksOwn, name='mybooks'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
