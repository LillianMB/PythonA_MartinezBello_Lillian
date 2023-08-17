import datetime
from django.test import TestCase
from django.urls import reverse
from ..models import Solicitud, Usuario  # Importa tus modelos
from django.contrib.auth.models import User

# Create your tests here.
class HomeViewTest(TestCase):
    def setUp(self):
        # Crear un usuario para las pruebas
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Crear un usuario personalizado para las pruebas
        self.usuario = Usuario.objects.create(
            id_user=self.user.id,
            username='testuser',
            nombres='Test',
            apellidos='User',
            correo_electronico='test@example.com',
            contrasena='testpassword',
            confirma_tu_contrasena='testpassword',
            tipo_usuario='Ciudadano'
            # Agrega otros campos según tu modelo Usuario
        )

        self.user = User.objects.create_user(username='testservidor', password='testpassword')

        # Crear un usuario personalizado para las pruebas
        self.usuario = Usuario.objects.create(
            id_user=self.user.id,
            username='testservidor',
            nombres='Test',
            apellidos='User',
            correo_electronico='test@example.com',
            contrasena='testpassword',
            confirma_tu_contrasena='testpassword',
            tipo_usuario='Servidor'
            # Agrega otros campos según tu modelo Usuario
        )

        # Crear una solicitud para las pruebas
        self.solicitud = Solicitud.objects.create(
            id_de_usuario=self.usuario.id_de_usuario,
            nombre_corto_problema='Test Problem',
            descripcion_problema='This is a test problem',
            status='enviado',
            ubicacion="Ubicación 1",
            fecha_creacion=datetime.datetime(2023, 7, 1, 10, 0, 0),
            fecha_modificacion=datetime.datetime(2023, 7, 2, 12, 0, 0)
        )

        # Crear una solicitud para las pruebas
        self.solicitud2 = Solicitud.objects.create(
            id_de_usuario=self.usuario.id_de_usuario,
            nombre_corto_problema='Test Problem2',
            descripcion_problema='This is a test problem2',
            status='enviado',
            ubicacion="Ubicación 2",
            fecha_creacion=datetime.datetime(2023, 6, 15, 9, 0, 0),
            fecha_modificacion=datetime.datetime(2023, 6, 20, 11, 0, 0)
        )

############ probando home
    def test_home(self): 
        response = self.client.get(reverse('home'))# Simula una solicitud GET a la vista home
        self.assertEqual(response.status_code, 200)# Verifica que la respuesta tenga un estado HTTP 200 (OK)
        self.assertTemplateUsed(response, 'authentication/index.html')# Verifica que el template correcto sea utilizado para renderizar

############ probando signin
    def test_signin_successful(self):
        response = self.client.post(reverse('signin'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_signin_failed(self):
        error_por_contrasena = self.client.post(reverse('signin'), {'username': 'testuser', 'password': 'contraseñaerronea'})
        error_por_usuario = self.client.post(reverse('signin'), {'username': 'usuarioerrorneo', 'password': 'testpassword'})

        self.assertEqual(error_por_contrasena.status_code, 200)  # Login failed, page should still be accessible
        self.assertEqual(error_por_usuario.status_code, 200)  # Login failed, page should still be accessible

    def test_signin_template(self):
        response = self.client.get(reverse('signin'))
        self.assertTemplateUsed(response, 'authentication/signin.html')


############ probando signout
    def test_signin_successful(self):
        self.client.post(reverse('signin'), {'username': 'testuser', 'password': 'testpassword'})
        response = self.client.post(reverse('signout'))

############ probando signup2
    def test_signup2_render(self):
        response = self.client.get(reverse('signup2'))
        self.assertEqual(response.status_code, 200)  # Check if the page renders successfully
        self.assertTemplateUsed(response, 'authentication/signup2.html')  # Check if the correct template is used

############ probando usuario
    def test_usuario_signup_valid_data(self):
        data = {
            'username': 'testuser1',
            'nombres': 'John',
            'apellidos': 'Doe',
            'correo_electronico': 'test@example.com',
            'contrasena': 'testpassword',
            'confirma_tu_contrasena': 'testpassword',
            'tipo_usuario': 'Ciudadano'
        }

        response = self.client.post(reverse('usuario'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup

        # Check if the user and profile are created in the database
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Usuario.objects.filter(username='testuser').exists())

    def test_usuario_signup_invalid_data(self):
        data = {
            'username': 'testuser2',
            'nombres': 'John',
            'apellidos': 'Doe',
            'correo_electronico': 'invalidemail',  # Invalid email format
            'contrasena': 'testpassword',
            'confirma_tu_contrasena': 'testpassword',
            'tipo_usuario': 'Ciudadano'
        }

        response = self.client.post(reverse('usuario'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after form submission

        # Since the data is invalid, the user and profile should not be created
        self.assertFalse(User.objects.filter(username='testuser2').exists())
        self.assertFalse(Usuario.objects.filter(username='testuser2').exists())

############ probando creasolicitud
    def test_crearsolicitud_valid_data(self):
        response = self.client.post(reverse('signin'), {'username': 'testuser', 'password': 'testpassword'})
        data = {
            'nombre_corto_problema': 'Problema de prueba',
            'descripcion_problema': 'Descripción del problema de prueba',
        }

        response = self.client.post(reverse('creasolicitud'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission

        # Check if the solicitud is created in the database
        self.assertTrue(Solicitud.objects.filter(nombre_corto_problema='Problema de prueba').exists())

    def test_crearsolicitud_invalid_data(self):
        data = {
            'nombre_corto_problema': '',  # Missing required field
            'descripcion_problema': 'Descripción del problema de prueba',
        }

        response = self.client.post(reverse('creasolicitud'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after form submission

        # Since the data is invalid, the solicitud should not be created
        self.assertFalse(Solicitud.objects.filter(descripcion_problema='Descripción del problema de prueba').exists())

############ probando mi_pagina
    def test_mi_pagina_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mi_pagina'))
        self.assertEqual(response.status_code, 200)  # Successful response for authenticated user

    def test_mi_pagina_unauthenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        self.client.logout()  # Log out the user
        response = self.client.get(reverse('mi_pagina'))
        self.assertEqual(response.status_code, 302)


############ probando servidor_publico
    def test_servidor_publico(self):
        self.client.login(username='testservidor', password='testpassword')
        response = self.client.get(reverse('servidor_publico'))
        solicitudes = response.context['solicitudes']

        self.assertEqual(len(solicitudes), 2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/servidor_publico.html')

############ probando export_excel
    def test_export_excel(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('export_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/ms-excel')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="solicitudes.xlsx"')


############ probando detalle_solicitud
def test_detalle_solicitud(self):
        response = self.client.get(reverse('detalle_solicitud', args=[1]))
        self.assertEqual(response.status_code, 200)

        solicitud_data = response.json()
        self.assertEqual(solicitud_data['nombre_corto_problema']['value'], "Test Problem")

def test_detalle_solicitud_view_invalid_id(self):
    invalid_id = 9999  # Un ID que no existe en la base de datos
    response = self.client.get(reverse('detalle_solicitud', args=[invalid_id]))
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.json(), {"error": "Solicitud no encontrada"})
