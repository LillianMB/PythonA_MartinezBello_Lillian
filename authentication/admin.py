from django.contrib import admin
from .models import *

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'nombres', 'apellidos', 'correo_electronico', "tipo_usuario")
    list_filter = ()
    search_fields = ('username', 'nombres', 'apellidos', 'correo_electronico')

admin.site.register(Usuario, UsuarioAdmin)


# class ImagenInline(admin.TabularInline):
#     model = Imagen
#     extra = 1

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id_de_reporte', 'nombre_corto_problema','descripcion_problema', 'status','ubicacion', 'fecha_creacion')
    list_filter = ('status', 'fecha_creacion')
    search_fields = ('nombre_corto_problema','status')
    # inlines = [ImagenInline]
admin.site.register(Solicitud, SolicitudAdmin)

# @admin.register(Imagen)
# class ImagenAdmin(admin.ModelAdmin):
#     pass