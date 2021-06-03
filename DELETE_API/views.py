from django.shortcuts import render
from django.http import JsonResponse
from ReadBook.models import Book
from django.views.decorators.csrf import csrf_exempt
from GET_API.decorator import check_method

# Create your views here.
@csrf_exempt
@check_method(method="DELETE")
def deleteBook(request,id):
  '''
    Delete book by id
  '''
  if Book.objects.filter(id = id).exists():
    fetchBook = Book.objects.get(id = id)
    fetchBook.delete()
    return JsonResponse({"Success":{"Message":"Book id {} is deleted sucessfully.".format(id)}})
  else:
    return JsonResponse({"Error":{"Message":"Failed. Book Not found of id {}".format(id)}})
