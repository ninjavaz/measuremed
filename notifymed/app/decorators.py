from django.http import HttpResponse
from django.shortcuts import redirect



def unauthenticated_user(view_func):
    """
    returns back a login page for user whose authentication was a failure

    Args:
        view_func 
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else :
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    """
    give the informations for a given group when one belongs to the group

    Args:
        allowed_roles
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page.')
        
        return wrapper_func
    return decorator