from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    # path('signup', views.singup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('signup2', views.signup2, name="signup2"),
    path('usuario', views.usuario, name="usuario"),
    path('mi_pagina', views.mi_pagina, name="mi_pagina"),
    path('solicitud', views.creasolicitud, name="creasolicitud"),
    path('solicitud/<int:solicitud_id>/', views.detalle_solicitud, name='detalle_solicitud'),
    path('servidor_publico', views.servidor_publico, name="servidor_publico"),
    path('export_excel/', views.export_excel, name='export_excel'),
    path('solicitud/<int:solicitud_id>/', views.actualizar_solicitud, name='actualizar_solicitud'),

    path('pruebitas', views.pruebitas, name="pruebitas"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)