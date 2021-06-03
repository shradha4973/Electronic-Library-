from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import BookPost
from GET_API.decorator import check_method

@csrf_exempt
@check_method(method='POST')
def postbook(request):
    if request.body:
        try:
            decoded_data = request.body.decode('utf-8')# utf-8 is used to decode data
            data=json.loads(decoded_data)# loads function will convert objects to dict
            book = BookPost.objects.create(book_name=data['Title'],book_price=data['Price'],book_description=data['Description'])
            book = BookPost.objects.filter(pk = book.pk)

            return JsonResponse({"message": "Completed Successfully.","PostBook":list(book.values())}) # dictionary is always accessed through key and value
        except Exception as ex:
            print("Error: "+str(ex))
            return JsonResponse({"message": "Error. Internal Server Error.","Required Fields":["Title","Price","Description"]})
    else:
        return JsonResponse({"message": "Error Missing Fields","Required Fields":["Title","Price","Description"]})