from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]): # @allowed_users(allowed_roles=[ 'e.g. admin'])
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.users.group.exists():
                group = request.users.group.all([0]).Name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page.')
        return wrapper_func
    return decorator