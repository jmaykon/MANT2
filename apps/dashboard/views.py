from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# -------------------- DECORADORES DE ROL --------------------
def role_required(roles):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            return render(request, 'core/403.html', status=403)
        return _wrapped_view
    return decorator



@login_required
def home_dashboard(request):
    if request.user.role == 'admin':
        template = 'dashboard/admin.html'
    elif request.user.role == 'tecnico':
        template = 'dashboard/tecnico.html'
    else:
        template = 'dashboard/usuario.html'
    return render(request, template)
