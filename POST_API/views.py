from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from GET_API.decorator import check_method 
from django.http import JsonResponse
from ReadBook.models import UserInfo,Book

# Create your views here.
@csrf_exempt
@check_method(method='POST')
def addBook(request):
    name = ''
    price = ''
    btype = ''
    cover = ''
    pdf = ''
    description=''
    category=''
    userid=''
    try:
        data = request.POST
        files = request.FILES
        name = data["Title"].strip()
        btype = data["Type"].strip()
        cover = files.get("Cover",None)
        pdf = files["PDF"]
        description= data["Description"].strip()
        category=data["Category"].strip()
        userid=int(data["UserID"])

        if btype == 'Free':
            price = 0
        elif btype == 'Premium':
            price = int(data['Price'])
        else:
            raise Exception('Invalid book type')

        #checking for errors
        if (name == '' or btype == '' or description == '' or category == ''):
            raise Exception('Empty Field')
        elif pdf.content_type != 'application/pdf':
            raise Exception('File Type Error')
        elif cover == None:
            cover = 'book_images\\no_cover.jpg'
        elif cover.content_type != 'image/jpeg' and cover.content_type != 'image/png':
            raise Exception('Image Type Error')

        #checking user if user is reader
        if not UserInfo.objects.filter(pk = userid,user_type = "Author"):
            raise Exception("Userid {} is not Author".format(userid))

        #If user is Author
        book = Book.objects.create(book_name=name,book_price=price ,book_type=btype,book_cover=cover,book_description=description,book_category=category,book_file=pdf,uploaded_by_id=userid)
        book = Book.objects.filter(pk = book.pk)
        return JsonResponse(
        {"Success": {"Message":"Book added Successfully."},
        "Book":list(book.values())}
        )

    except Exception as ex:
        print("Error:"+str(ex))
        return JsonResponse({"ERROR": "Missing or Miss matched field.","Required Fields":["Title","Price","Type[Free/Premium]","Cover","PDF","Description","Category","UserID"]})