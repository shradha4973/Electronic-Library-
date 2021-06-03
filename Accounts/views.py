from django.shortcuts import render, redirect
from ReadBook.models import UserInfo
from django.contrib import messages
from django.contrib.auth.models import User, auth
# Create your views here.
  
def register_user(request): #This method is used for registering users.
	if not request.user.is_authenticated:
		if request.method == 'POST': #Checking if request method is POST.
			first_name= request.POST['first_name']
			last_name= request.POST['last_name']
			username= request.POST['username']
			email= request.POST['email']
			user_type= request.POST['user_type']
			password1= request.POST['password1']
			password2= request.POST['password2']
			if password1==password2: #Validating the form and if error occurs show throw these messages
				if User.objects.filter(username=username).exists():
					messages.info(request,'username is taken')
					return redirect('Accounts:register_user')
				elif User.objects.filter(email=email).exists(): 
					messages.info(request,'Email is taken')
					return redirect('Accounts:register_user')
				else: #If form is validates, then addning in database
					user= User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
					user.save()
					UserInfo.objects.create(id = user.id,user_type=user_type, users_id=user.id)
					return redirect('Accounts:login_user')
			else: #If request method is not POST then throwing these messages.
				messages.info(request,'Password didn\'t match')
				return redirect('Accounts:register_user')
		return render(request, 'Accounts/register.html')
	else:
		return redirect('/')
		

def login_user(request): #This method is used to login the user
	if not request.user.is_authenticated: #Checking if user is logged in or not
		if request.method == 'POST':
			username= request.POST['username']
			password= request.POST['password']

			user = auth.authenticate(username=username, password=password)
			if user is not None:
				auth.login(request,user)
				return redirect('/')
			else:
				messages.info(request,'invalid credentials')
				return redirect("Accounts:login_user")
		else:
			return render(request, 'Accounts/login.html')
	else:
		return redirect('/')
		

def logout_user(request): #This method is used to logout the user
	auth.logout(request)
	return redirect('Accounts:login_user')
