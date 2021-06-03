from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 
from GET_API.decorator import check_method
from django.http import JsonResponse
import json

from ReadBook.models import Book

# Create your views here.
@csrf_exempt
@check_method(method='PUT')
def updateBook(request,bookid):
    if request.body and Book.objects.filter(pk = bookid).exists():
        try:
            book = Book.objects.get(pk = bookid)
            decode_data = request.body.decode('UTF-8')
            data = json.loads(decode_data)
            price = 0
            
            if book.uploaded_by_id == data['userid']:
                #checking book type
                if data['booktype'] == 'Premium':
                    price = int(data['price'])
                elif data['booktype'] == 'Free':
                    price = 0
                else:
                    return JsonResponse({'Error':'Book type did not matched'})

                #checking for errors
                if (data['title'].strip() == '' or data['booktype'].strip() == '' or data['description'].strip() == '' or data['category'].strip() == ''):
                    return JsonResponse({'Error':'Empty Fields'})

                #updating Book
                book.book_name=data['title']
                book.book_price=price
                book.book_type=data['booktype']
                book.book_description=data['description']
                book.book_category=data['category']
                book.save()
                
                book = Book.objects.filter(pk = bookid)

                #success
                return JsonResponse({'Success':'Book Updated Successfully','Book':list(book.values())})
            else:
                return JsonResponse({'Error':'Unauthorized user'})
        
        except Exception as e:
            print("ERROR : "+str(e))
            return JsonResponse({'Error':'Internal Server Error'})
    else:
        return JsonResponse({'Error':'Book id or update data are missing'})