import datetime
import io
import csv
import xlsxwriter
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import *
from .models import *
from .util import *
from .decorators import *


# Create your views here.

def home(request):
    return render(request, "authentication/index.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            usuario_logueado = obtenerUsuarioLogueado(request)

            if usuario_logueado.tipo_usuario == "Ciudadano" :
                return redirect(reverse("mi_pagina"))
            if usuario_logueado.tipo_usuario == "Servidor" :
                return redirect(reverse("servidor_publico"))
            
            return redirect(reverse("mi_pagina"))
        else:
            return render(request, "authentication/signin.html", {"loginerror" : True })
    
    return render(request, "authentication/signin.html", {"loginerror" : False })

def signout(request):
    logout(request)
    return redirect('home')

def signup2(request):
    form = UsuarioForm()
    return render(request, "authentication/signup2.html", {"form": form})

def usuario(request):
    
    if request.method == "POST":
        usrdata = UsuarioForm(data = request.POST)

        if usrdata.is_valid():

            username = request.POST['username']
            correo_electronico = request.POST['correo_electronico']
            contrasena = request.POST['contrasena']
            
            UserDjango = User.objects.create_user(username, correo_electronico, contrasena)

            #guardamos la solicitud con commit=False para poder editar los datos antes de almacenarlo en la db
            usr = usrdata.save(commit=False)
            usr.id_user = UserDjango.id
            usrdata.save()
            
            user = authenticate(username=username, password=contrasena)
            login(request, user)

            if usr.tipo_usuario == "Ciudadano" :
                return redirect(reverse("mi_pagina") + "?usuario_nuevo")
            if usr.tipo_usuario == "Servidor" :
                return redirect(reverse("servidor_publico") + "?usuario_nuevo")
            
        else:
            return redirect(reverse("signup2") + "?error")
        
def creasolicitud(request):
    if request.method == "POST":
        soldata = SolicitudForm(data = request.POST)

        if soldata.is_valid():
            #obtenemos la info del usuario guardada en la base de datos
            usuario_logueado = obtenerUsuarioLogueado(request)
            
            #guardamos la solicitud con commit=False para poder editar los datos antes de almacenarlo en la db
            solicitud = soldata.save(commit=False)

            solicitud.id_de_usuario = usuario_logueado.id_de_usuario
            soldata.save()

            return redirect(reverse("mi_pagina") + "?solicitud_guardada")
        else:
            return redirect(reverse("mi_pagina") + "?error_solicitud")
      
@check_authenticated 
def mi_pagina(request):
    solicitud_form = SolicitudForm()

    if request.user.is_authenticated:
        usuario_logueado = obtenerUsuarioLogueado(request)
        solicitudes = Solicitud.objects.filter(id_de_usuario=usuario_logueado.id_de_usuario)
    return render(request, "authentication/mi_pagina.html", {"solicitud_form__" : solicitud_form, "solicitudes" : solicitudes})

@check_authenticated
def servidor_publico(request):
    solicitudes = Solicitud.objects.all()
    return render(request, "authentication/servidor_publico.html", {"solicitudes" : solicitudes})

def export_excel(request):
    usuario_logueado = obtenerUsuarioLogueado(request)

    if usuario_logueado is None:
        return render(request, "authentication/index.html")

    if usuario_logueado.tipo_usuario == "Servidor":
        rows = Solicitud.objects.all().values_list('id_de_reporte', 'id_de_usuario', 'nombre_corto_problema', 'descripcion_problema', 'status', 'ubicacion', 'fecha_creacion', 'fecha_modificacion')

    if usuario_logueado.tipo_usuario == "Ciudadano":
        rows = Solicitud.objects.filter(id_de_usuario=usuario_logueado.id_de_usuario).values_list('id_de_reporte', 'id_de_usuario', 'nombre_corto_problema', 'descripcion_problema', 'status', 'ubicacion', 'fecha_creacion', 'fecha_modificacion')

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="solicitudes.xlsx"'

    wb = xlsxwriter.Workbook(response, {'in_memory': True, 'remove_timezone': True})
    ws = wb.add_worksheet()

    # Obtener los campos de la clase Solicitud
    solicitud_fields = Solicitud._meta.fields

    # Agregar los nombres de columna usando verbose_name
    for col_num, field in enumerate(solicitud_fields):
        ws.write(0, col_num, field.verbose_name)

    
    
    row_num = 1  # Comenzar en la siguiente fila después de los nombres de columna
    for row in rows:
        for col_num, value in enumerate(row):
            # Formatear campos fecha_creacion y fecha_modificacion
            if col_num in (6 , 7):  # Índices de fecha_creacion y fecha_modificacion
                ws.write_datetime(row_num, col_num, value, wb.add_format({'num_format': 'yyyy-mm-dd HH:mm:ss'}))
            else:
                ws.write(row_num, col_num, value)
        row_num += 1

    wb.close()
    return response

def detalle_solicitud(request, solicitud_id):
    try:
        solicitud = Solicitud.objects.get(id_de_reporte=solicitud_id)
        solicitud_data = {}

        for field in Solicitud._meta.fields:
            field_long_name = field.verbose_name
            field_value = getattr(solicitud, field.name)

            if isinstance(field_value, (datetime.datetime, datetime.date)):
                field_value = field_value.strftime("%Y-%m-%d %H:%M:%S")
            
            if field.name == "status":
                solicitud_data[field.name] = {"long_name" : field_long_name, "value": field_value, "status_choices" : Solicitud.STATUS_CHOICES}
            else:
                solicitud_data[field.name] = {"long_name" : field_long_name, "value": field_value}

        return JsonResponse(solicitud_data)
    except Solicitud.DoesNotExist:
        return JsonResponse({"error": "Solicitud no encontrada"}, status=404)

def actualizar_solicitud(request, solicitud_id):
    if request.method == 'PATCH':
        solicitud = get_object_or_404(Solicitud, id_de_reporte=solicitud_id)
        
        # Actualiza los campos según los datos recibidos en el cuerpo de la solicitud
        solicitud.status = request.POST.get('status', solicitud.status)
        solicitud.save()

        return JsonResponse({'message': 'Solicitud actualizada exitosamente'})

    return JsonResponse({'error': 'Método no permitido'}, status=405)  # Método no permitido


def pruebitas(request):
    print("---------------------------------------------")
    print(1)
    usuario = obtenerUsuarioLogueado(request)
    print(2)
    print(usuario.username)
    print("---------------------------------------------")