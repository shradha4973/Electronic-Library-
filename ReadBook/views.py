from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponse
from .models import Book,Review,Transaction,UserInfo
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages

from .decorator import author_only

# Create your views here.
def loadBook(request):
  '''
    This view function will load all the books.
  '''
  books = Book.objects.all()
  amount = UserInfo.objects.get(pk = request.user.id).user_amount if request.user.is_authenticated else None 
  return render(request,'ReadBook/Book.html',context={'books':books,'amount':amount})

def bookDescription(request,bid):
  '''
    This view function will handle a book description page.
  '''
  book = None
  reviews = None
  bought = False
  hadreview = None
  owner = False
  amount = None
  loggedin = True if request.user.is_authenticated else False 
  
  if Book.objects.filter(id=bid).exists():
    try:
      book = Book.objects.get(id=bid)
      reviews = Review.objects.filter(book_id = bid).order_by('date').all()[:5]
      if loggedin:
        #get user amount
        amount = UserInfo.objects.get(pk = request.user.id).user_amount
        #check owner
        owner = True if Book.objects.get(pk = bid).uploaded_by_id == request.user.id else False
        if not owner:
          #check if user have bought this book 
          bought = True if Transaction.objects.filter(user_id=request.user.id,book_id=bid).exists() else Book.objects.filter(id = bid , book_type = "Free").exists()
        else:
          #not bought
          bought = True

        if bought :
          #check if user have review this book
          hadreview = Review.objects.filter(user_id=request.user.id,book_id=bid).all()
          hadreview = '' if len(hadreview) == 0 else hadreview[0]
    except Exception as e:
      print("Error in bookDescription :"+str(e))
      messages.error(request,"Internal Servre Error.")
  else:
    #no book found of that id
    messages.error(request,"Book Not Found.")
    return redirect('ReadBook:premiumbook')
  
  return render(request,'ReadBook/BookDescription.html',context={
    'book':book,
    'reviews':reviews,
    "loggedin":loggedin,
    "bought":bought,
    "hadreview":hadreview,
    "owner":owner,
    "amount":amount
    })

@login_required(login_url='/login/')
def review(request,bid):
  '''
    This view function will accept only post request and handle review of a particular book
  '''
  review = None
  user = None
  if request.method == "POST":
    #METHOD POST
    if Book.objects.filter(id = bid).exists():
      try:
        review = request.POST.get('review','').strip()
        user = request.user
        #checking if book has been bought or not or Free or Owned by user
        if (Transaction.objects.filter(user_id=user.id,book_id=bid).exists()) or (Book.objects.filter(id = bid , book_type = "Free").exists()) or (Book.objects.get(pk = bid).uploaded_by_id == request.user.id):

          if review == '' :
            raise Exception('Review is Null')
          elif Review.objects.filter(user_id = user.id , book_id = bid).exists():
            #update existing Review
            update_row = Review.objects.filter(user_id = user.id , book_id = bid).get()
            update_row.review = review
            update_row.save()
          else:
            #create new Review
            Review.objects.create(book_id = bid , user_id = user.id, review = review)

          messages.success(request,"Review added successfully")
          return redirect("ReadBook:description", bid=bid)

        else:
          #book not bought
          messages.error(request,"You must buy this book to Review this book.")
          return redirect("ReadBook:description", bid=bid)
      except Exception as e:
        print("Error in review :"+str(e))
        messages.error(request, 'Error while adding review')
        return redirect("ReadBook:description", bid=bid)
    else:
      # if No Book
      messages.error(request,"Internal Server Error")
      return redirect("ReadBook:premiumbook")
  else:
    #METHOD GET
    #No page for get method
    messages.error(request,"Page Not Found")
    return redirect("ReadBook:premiumbook")

@login_required(login_url='/login/')
def rating(request,bid):
  '''
    This view function will accept only post request and handle Rating of a particular book
  '''
  rating = None
  user = None
  if request.method == "POST":
    #METHOD POST
    if Book.objects.filter(id = bid).exists():
      try:
        rating = int(request.POST.get('star',None))
        user = request.user
        #checking if book has been bought or not or Free or own by Author itself
        if (Transaction.objects.filter(user_id=user.id,book_id=bid).exists()) or (Book.objects.filter(id = bid , book_type = "Free").exists()) or (Book.objects.get(pk = bid).uploaded_by_id == request.user.id): 

          if rating > 5 or rating < 1 :
            raise Exception('Rating Not valid')
          elif Review.objects.filter(user_id = user.id , book_id = bid).exists():
            #update existing rating
            update_row = Review.objects.filter(user_id = user.id , book_id = bid).get()
            update_row.rating = rating
            update_row.save()
            #calling function that make change in book_rating cell
            calculateRating(bid)
          else:
            #create new one
            Review.objects.create(book_id = bid , user_id = user.id, rating = rating)
            calculateRating(bid)
          messages.success(request,"Rating added successfully")
          return redirect("ReadBook:description", bid=bid)

        else:
          #book not bought
          messages.error(request,"You must buy this book to Rate this book.")
          return redirect("ReadBook:description", bid=bid)
      except Exception as e:
        print("Error in rating :"+str(e))
        messages.error(request, 'Error while adding your rating')
        return redirect("ReadBook:description", bid=bid)
    else:
      # If No Book
      messages.error(request,"Internal Server Error")
      return redirect("ReadBook:premiumbook")
  else:
    #METHOD GET
    #No page for get method
    messages.error(request,"Page Not Found")
    return redirect("ReadBook:premiumbook")

@login_required(login_url='/login/')
@author_only
def addBook(request):
  '''
    This view function will handle both post and get method for adding book.
    This function is only allowed to access if user type is author and user is logged in 
  '''
  name = ''
  price = ''
  btype = ''
  cover = ''
  pdf = ''
  description=''
  category=''
  userid=''
  if request.method == 'POST':
    #Method POST
    try:
      name = request.POST['name'].strip()
      btype = request.POST['type'].strip()
      description = request.POST['description'].strip()
      category = request.POST['category'].strip()
      cover = request.FILES.get('image',None)
      pdf = request.FILES['file']
      userid = request.user.id

      #checking book type
      if btype != 'Free':
        price = int(request.POST['price'])
      else:
        price = 0

      #checking for errors
      if (name == '' or btype == '' or description == '' or category == ''):
        raise Exception('Empty Field')
      elif pdf.content_type != 'application/pdf':
        raise Exception('File Type Error')
      elif cover == None:
        cover = 'book_images\\no_cover.jpg'
      elif cover.content_type != 'image/jpeg' and cover.content_type != 'image/png':
        raise Exception('Image Type Error')
      
      Book.objects.create(book_name=name,book_price=price ,book_type=btype,book_cover=cover,book_description=description,book_category=category,book_file=pdf,uploaded_by_id=userid)

      #success 
      messages.success(request,"Book Added Successfully.")
      return redirect('ReadBook:premiumbook')
    except Exception as e:
      print("ERROR : "+str(e))
      messages.error(request,"Error while processing the data. This might be because data is incorrect.")

  return render(request,'ReadBook/AddBook.html',context={
    'bookname':name,
    'bookprice':price,
    'description':description,
    'category':category
    })

@login_required(login_url='/login/')
@author_only
def updateBook(request,bid):
  '''
    This view function will handle both post and get method for updating book.
    This function is only allowed to access if user type is author and user is logged in 
  '''
  if Book.objects.filter(id = bid):
    book = Book.objects.get(id = bid)
    if request.method == 'POST':
      #METHOD POST
      try:
        name = request.POST['name'].strip()
        btype = request.POST['type'].strip()
        description = request.POST['description'].strip()
        category = request.POST['category'].strip()
        userid = request.user.id

        if book.uploaded_by_id == userid:
          #checking book type
          if btype != 'Free':
            price = int(request.POST['price'])
          else:
            price = 0

          #checking for errors
          if (name == '' or btype == '' or description == '' or category == ''):
            raise Exception('Empty Field')

          #updating Book
          book.book_name=name
          book.book_price=price
          book.book_type=btype
          book.book_description=description
          book.book_category=category
          book.save()

          #success
          messages.success(request,"Book updated Successfully")
          return redirect('ReadBook:description',bid=book.pk)
        else:
          # not the same user
          messages.error(request,"You do not have permission to Update book.")
          return redirect("ReadBook:description", bid=book.pk)
      except Exception as e:
        print("ERROR : "+str(e))
        messages.error(request,"Error while processing the data. This might be because data is incorrect.")
        return redirect("ReadBook:description", bid=book.pk)
    else:
      #METHOD GET
      return render(request,'ReadBook/UpdateBook.html',context={"book":book})
  else:
    messages.error(request,"Didn't found the book you are trying to update.")
    return redirect('ReadBook:premiumbook')

@login_required(login_url='/login/')
@author_only
def deleteBook(request,bid):
  '''
    This view function will handle post method only for deleting book.
    This function is only allowed to access if user type is author and user is logged in 
  '''
  book = None
  if Book.objects.filter(id = bid).exists():
    book = Book.objects.get(id = bid)
    if book.uploaded_by_id == request.user.id:
      if request.method == 'POST':
        #METHOD POST
        book.delete()
        messages.success(request,"Book Deleted Successfuly")
        return redirect('ReadBook:premiumbook')
      else:
        #METHOD GET
        messages.error(request,"Error while deleting Book")
        return redirect('ReadBook:description',bid=bid)
    else:
      messages.error(request,"You do not have permission. Permission Denied.")
      return redirect('ReadBook:description',bid=bid)
  else:
    messages.error(request,"Internal Server Error")
    return redirect('ReadBook:premiumbook')

#helper
def calculateRating(bid):
  '''
    TO calculate average rating of the book
  '''
  total = Review.objects.filter(book_id = bid).aggregate(Sum('rating'))
  review_no = Review.objects.filter(book_id = bid).all().count()
  update_row = Book.objects.get(id = bid)
  update_row.book_rating = int(total['rating__sum'])/int(review_no)
  update_row.save()

@login_required(login_url='/login/')
def download(request,bid):
  '''
    TO check if the user owns the book or not 
    and if he owns then sends response with book attached and ready for download.
  '''
  if Book.objects.filter(pk= bid).exists():
    book = Book.objects.get(pk = bid)
    owner = True if Book.objects.get(pk = bid).uploaded_by_id == request.user.id else False
    bought = True if Transaction.objects.filter(user_id=request.user.id,book_id=bid).exists() else False
    if owner or bought :
      file = book.book_file
      response = HttpResponse(file, content_type='application/pdf')
      response['Content-Disposition'] = 'attachment; filename="' + book.book_file.name + '"'
      return response
    else:
      messages.error(request,"Problem while Converting to Pdf.")
      return redirect("ReadBook:description",bid=bid)
  else:
    messages.error(request,"Internal Server Error.")
    return redirect("ReadBook:premiumbook")

@login_required(login_url='/login/')
def booksOwn(request):
  '''
    TO view own or bought book
  '''
  transactions = Transaction.objects.filter(user_id=request.user.id)
  ownbooks = Book.objects.filter(uploaded_by_id = request.user.id)
  return render(request,"ReadBook/MyBooks.html",context={"transactions":transactions,"ownbooks":ownbooks})
