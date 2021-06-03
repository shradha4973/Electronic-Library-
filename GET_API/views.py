from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from ReadBook.models import Book,Review
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .decorator import check_method

# Create your views here.

#Default No. of recored a page holds
size = 10

#book
@csrf_exempt
@check_method(method="GET")
def getBook(request,id):
  '''
  Return Book that match given book id
  '''
  if Book.objects.filter(id = id).exists():
    fetch_book = Book.objects.filter(id = id)
    data = {"Book":list(fetch_book.values())}
    return JsonResponse(data)
  else:
    return JsonResponse({"Error":{"Message":"Book Not found of id {}".format(id)}})

@csrf_exempt
@check_method(method="GET")
def getAllBook(request):
  '''
  Return first 10 Books
  '''
  if Book.objects.all().exists():
    fetch_book = Book.objects.all()
    total_page = totalPage(fetch_book.count(),size)
    fetch_book = fetch_book[:size]
    data = list(fetch_book.values())
    data.append({"Current Page":1,"Total Page":total_page})
    return JsonResponse({"Book":data})
  else:
    return JsonResponse({"Error":{"Message":"No Book in database."}})


@csrf_exempt
@check_method(method="GET")
def getBookOfPage(request,page,size):
  '''
  Return Book of selected page and selected size
  '''
  skip = size*(page - 1)
  limit = size*page
  fetch_book = Book.objects.all()[skip:limit]
  if fetch_book.exists():
    data = {"Book":list(fetch_book.values())}
    return JsonResponse(data)
  else:
    return JsonResponse({"Error":{"Message":"You are in a page {} that has no data.".format(page)}})

#review
@csrf_exempt
@check_method(method="GET") 
def getAllReview(request,bookid):
  '''
  Return first 10 reviews
  '''
  if Book.objects.filter(id = bookid).exists():
    if Review.objects.filter(book_id = bookid).exists():
      fetch_review = Review.objects.filter(book_id = bookid)
      total_page = totalPage(fetch_review.count(),size)
      fetch_review = fetch_review[:size]
      data = list(fetch_review.values())
      data.append({"Current Page":1,"Total Page":total_page})
      return JsonResponse({"Review":data})
    else:
      return JsonResponse({"Error":{"Message":"No Review in this book(id={}) yet.".format(bookid)}})
  else:
    return JsonResponse({"Error":{"Message":"Book of this id {} not found.".format(bookid)}})


@csrf_exempt
@check_method(method="GET")
def getReviewOfPage(request,bookid,page,size):
  '''
  Return review of selected page and selected size
  '''
  skip = size*(page - 1)
  limit = size*page
  if Book.objects.filter(id = bookid).exists():
    if Review.objects.filter(book_id = bookid)[skip:limit].exists():
      fetch_review = Review.objects.filter(book_id = bookid)[skip:limit]
      data = list(fetch_review.values())
      return JsonResponse({"Review":data})
    else:
      return JsonResponse({"Error":{"Message":"You are in a page {} that has no data.".format(page)}})
  else:
    return JsonResponse({"Error":{"Message":"Book of this id {} not found.".format(bookid)}})


#search
@csrf_exempt
@check_method(method="GET")
def search(request):
  '''
  Search Book Through Keyword
  '''
  try:
    keyword = request.GET.get('q','')
    page = int(request.GET.get('page',0))
    size = 5
    skip = 0
    limit = size

    if page:
      skip = size * (page - 1)
      limit = size * page

    queries = keyword.split(" ") 
    for q in queries:
      books = Book.objects.filter(
        Q(book_name__icontains= q)
      ).distinct()

    total_page = totalPage(books.count(),size)
    books = books[skip : limit]

    if books.exists():
      data = list(books.values())
      data.append({"Current Page":page+1,"Total Page":total_page})
      return JsonResponse({"book":data})
    elif total_page != 0:
      return JsonResponse({"Error":[
        {"Message":"You are in a page that has no data."},
        {"Current Page":page,"Total Page":total_page}
        ]})
    else:
      return JsonResponse({"Error":{"Message":"Your search keyword - {} - did not match any Books.".format(keyword)}})
  except Exception as e:
    print("Error: "+str(e))
    return JsonResponse({"Error":{"Message":"Error while Processing"}})

#helper
def totalPage(total,size):
  '''
  Return Total page number 
  '''
  page = total//size
  page = page+1 if total%size else page
  return page