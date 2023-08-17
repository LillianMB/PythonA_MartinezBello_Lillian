from django import forms
from .models import *

class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('username', 'nombres', 'apellidos', 'correo_electronico', 'contrasena', 'confirma_tu_contrasena', 'tipo_usuario')
        labels = {
            'username': 'Nombre de usuario',
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'correo_electronico': 'Correo electrónico',
            'contrasena': 'Contraseña',
            'confirma_tu_contrasena': 'Confirma tu contraseña',
            'tipo_usuario': 'Tipo de usuario',
            # 'fecha_creacion': 'Fecha de creación',
        }
        widgets = {
            'contrasena': forms.PasswordInput(),
            'confirma_tu_contrasena': forms.PasswordInput(),
        #     'fecha_creacion': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            # 'correo_usuario',
            # 'nombre_usuario',
            'nombre_corto_problema',
            'descripcion_problema',
            # 'status',
            'ubicacion',
            # 'imagenes',
        ]
        widgets = {
            'descripcion_problema': forms.Textarea(attrs={'rows': 6}),
        }