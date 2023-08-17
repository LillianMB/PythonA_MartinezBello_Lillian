from django.shortcuts import get_object_or_404
from .forms import *
from .models import *


def obtenerUsuarioLogueado(request):
    if request.user.is_authenticated:
        usuario = get_object_or_404(Usuario, username=request.user.username)
        return usuario
    else:
        return None