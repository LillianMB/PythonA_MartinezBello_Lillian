from django.shortcuts import render
from rest_framework import generics
from api.models import Libro
from api.serializers import LibroSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class TokenObtainView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')


        if username is None or password is None:
            return Response({'error': 'Se requiere nombre de usuario y contraseña.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                if user.groups.filter(name__in=["api","administrador"]).exists():
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                    })
                else:
                    return Response({'error': 'Este usuario no tiene los permisos para acceder a la API'}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            pass


        return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)



class LibroListaView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer


class LibroDetalleView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer


class LibroListaCustomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        libros = Libro.objects.filter(activo=True)
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)

    def post(self, request):
        libro = Libro(nombre_libro=request.data['nombre_libro'],autor=request.data['autor'],
                    editorial=request.data['editorial'], activo=request.data['activo'])
        libro.save()
        serializer = LibroSerializer(libro)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LibroDetalleCustomView(APIView):
    def get_permissions(self):
        methods_protected = ['PUT', 'PATCH', 'DELETE']
        if self.request.method in methods_protected:
            return [IsAuthenticated()]
        return []

    def get_object(self, pk):
        try:
            return Libro.objects.get(pk=pk)
        except Libro.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        libro = self.get_object(pk)
        serializer = LibroSerializer(libro)
        return Response(serializer.data)
    
    def put(self, request, pk):
        libro = self.get_object(pk)
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        libro = self.get_object(pk)
        serializer = LibroSerializer(libro, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        libro = self.get_object(pk)
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
