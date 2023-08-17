from django.urls import path, re_path

from api.views import LibroDetalleView, LibroListaView, LibroListaCustomView, LibroDetalleCustomView, TokenObtainView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('tokenDefault/', TokenObtainPairView.as_view(), name='token_pair'),
    path('tokenCustom/', TokenObtainView.as_view(), name='token_pair_custom'),
    path('test', LibroListaView.as_view(), name='libros_lista'),
    path('test/<int:pk>', LibroDetalleView.as_view(), name='libros_detalle'),   
    path('', LibroListaCustomView.as_view(), name='libros_lista_custom'),   
    path('<int:pk>', LibroDetalleCustomView.as_view(), name='libros_detalle_custom'),   
] 