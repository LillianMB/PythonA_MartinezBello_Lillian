from django.db import models

# Create your models here.
class Usuario(models.Model):
    id_de_usuario = models.AutoField(primary_key=True)
    id_user = models.IntegerField()
    username = models.CharField(max_length=50, verbose_name="Nombre de usuario")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    correo_electronico = models.EmailField(verbose_name="Correo electrónico")
    contrasena = models.CharField(max_length=128, verbose_name="Contraseña")
    confirma_tu_contrasena = models.CharField(max_length=128, verbose_name="Confirma tu contraseña")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    tipo_usuario = models.CharField(max_length=20, choices=[("Ciudadano", "Ciudadano"), ("Servidor", "Servidor")], default='Ciudadano', verbose_name="Tipo de usuario")

    
    def __str__(self):
        return self.username


class Solicitud(models.Model):
    id_de_reporte = models.AutoField(primary_key=True)
    id_de_usuario = models.IntegerField()
    nombre_corto_problema = models.CharField(max_length=150, verbose_name="Nombre corto del problema")
    descripcion_problema = models.CharField(max_length=1300, verbose_name="Descripción del problema")
    STATUS_CHOICES = [
        ('enviado', 'Enviado/Pendiente de revisión'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
        ('en_revision', 'En proceso de revisión'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enviado', verbose_name="Status")
    ubicacion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ubicación de coordenadas o descripción")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de modificación")
    # imagenes = models.ManyToManyField('Imagen', blank=True, verbose_name="Imágenes")

    def __str__(self):
        return f"Reporte #{self.id_de_reporte}: {self.nombre_corto_problema}"

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"


# class Imagen(models.Model):
#     Solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, verbose_name="Solicitud relacionada")
#     imagen = models.ImageField(upload_to='imagenes/', verbose_name="Imagen")

#     def __str__(self):
#         return f"Imagen #{self.id}"

#     class Meta:
#         verbose_name = "Imagen"
#         verbose_name_plural = "Imágenes"
