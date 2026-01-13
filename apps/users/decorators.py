from django.shortcuts import redirect
from functools import wraps

def role_required(roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            return redirect('dashboard:home')  # si no tiene permiso
        return _wrapped_view
    return decorator
