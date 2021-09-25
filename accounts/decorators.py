from django.shortcuts import redirect
from django.http import HttpResponse

def admin_or_logged_out_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser or not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to view this page.')
    return wrapper_func
