from django.shortcuts import render
from ReadBook.models import Book
from django.db.models import Q

# This function get the book objects and render the object in search.html templates
def search(request):
	query =""
	book = ''
	if request.GET:
		query = request.GET.get('q','').strip()		
		if query != '':
			book = get_data_queryset(query)
	return render(request, 'ReadBook/Book.html',context={"books": book})

#This function will return data and set() will remove repetition of output data and list() is for typecasting
def get_data_queryset(query= None):
	queryset = [] 
	queries = query.split(" ") 
	for q in queries:
		books = Book.objects.filter(
			Q(book_name__icontains= q)
			).distinct()
		for book in books:
			queryset.append(book)
	return list(set(queryset))

