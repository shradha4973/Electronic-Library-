from django.http import JsonResponse

def check_method(method="GET"):
  '''
  Decorator to validate request method
  '''
  def decor(func):
    def wrapper(request,*args, **kwargs):
      if request.method == method.upper():
        return func(request,*args, **kwargs)
      else:
        return JsonResponse({"Error":{"Message":"Request Method is not {}".format(method.upper())}})
    return wrapper
  return decor