from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .models import UserInfo

def author_only(func):
  '''
  Decorator to validate author
  '''
  def wrapper(request,*args, **kwargs):
    if UserInfo.objects.filter(pk = request.user.id,user_type = "Author").exists():
      return func(request,*args, **kwargs)
    else:
      messages.error(request,"You do not have permission. Please sign up as Author.")
      return redirect('ReadBook:premiumbook')
  return wrapper