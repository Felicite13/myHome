from django.shortcuts import redirect
from functools import wraps

def profil_valide_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.est_valide:
                return view_func(request, *args, **kwargs)
        return redirect('en_attente_validation')
    return _wrapped_view

