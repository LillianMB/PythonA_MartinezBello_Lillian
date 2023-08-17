from rest_framework import serializers
from api.models import Libro


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['nombre_libro', 'autor', 'editorial']