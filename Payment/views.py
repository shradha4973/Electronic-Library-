from django.shortcuts import render,redirect
from ReadBook.models import UserInfo, Book, Transaction
from django.contrib.auth.decorators import login_required

# Get book information from Book app and calculate total book price by giving or not giving discount
@login_required(login_url = '/login/')
def getBook(request,id):
	if Book.objects.filter(id=id).exists():
		book = Book.objects.get(id=id)
		dis = (int (book.book_discount) * int(book.book_price))/100
		total = book.book_price - dis
		return render(request,'Payment/transaction.html', context={'book':book, 'total': total})
	else:
		return redirect('ReadBook:premiumbook')

# This function payment() is for making transaction by the reader for premiun books.
@login_required(login_url = '/login/')  
def payment(request,bid):
	reader = request.user
	userinfo = UserInfo.objects.filter(id = reader.id).get()
	if request.method == 'POST':
		if Book.objects.filter(id = bid).exists():
			book=Book.objects.get(id = bid) 
			author=book.uploaded_by
			dis = (int (book.book_discount) * int(book.book_price))/100
			total = book.book_price - dis
			# This condition is for checking the user amount with the total amount of book.
			if userinfo.user_amount>=total:   
				pay=(int(userinfo.user_amount))-(int(total))	
				userinfo.user_amount=pay
				userinfo.save()

				# If the user amount is greate or equal to books price then 60% of total book price will be added in book uploader account.
				amou = (int(total) * 60)/100
				author.user_amount = int(author.user_amount) + amou
				author.save()

				# This query creates transaction by deducting amount from reader and adding amount in book uploader.
				Transaction.objects.create(user_id=userinfo.id, price=book.book_price, discount=book.book_discount, book_id=bid,total = total)
				# After successful transaction, user is redirect to homepage
				return redirect('ReadBook:description', bid = bid)

				#If the user amount is less than total book price then error message is displayed to the user.
			elif userinfo.user_amount<total:
				#add django message
				return redirect('Payment:updateamount')
		else:
			#if no book
			return redirect('ReadBook:premiumbook')
	else:
		return redirect('Payment:getBook',id=bid)

# This function is for updating the user amount incase of not sufficient amount available for purchasing book 
@login_required(login_url = '/login/')
def update_amount(request):
	if request.method == 'POST':
		user = request.user
		userinfo = UserInfo.objects.filter(users_id =user.id).get()
		amount = request.POST.get('amount',0)
		userinfo.user_amount = int(userinfo.user_amount)+int(amount)
		userinfo.save()
		return redirect('ReadBook:premiumbook')

	return render(request, 'Payment/updateprice.html')
	


	



