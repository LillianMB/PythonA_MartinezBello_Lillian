from django.db import models

# Create your models here.


class Libro(models.Model):
    nombre_libro = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    editorial = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return str(self.nombre_libro)