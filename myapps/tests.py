from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone
import datetime

from django.contrib.auth.models import User

from .views import index

from django.test import override_settings
from PIL import Image
from io import BytesIO
from django.core.files import File
import tempfile

class TechLlamaIndexViewTest(TestCase):
    def setUp(self):
        url = reverse('index')
        self.response = self.client.get(url)

    def test_index_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_index_url_resolves_index_view(self):
        view = resolve('/')
        self.assertEqual(view.func, index)
    
    def test_has_apps(self):
        self.assertContains(response, '<img', 9)


class TechLlamaNavbarTopbarTest(TestCase):
    def setUp(self):
        url = reverse('index')
        self.response = self.client.get(url)

    def test_topbar_navbar_links_exists(self):
        index_url = reverse('index')
        self.assertContains(self.response, 'href="{0}"'.format(index_url))

    def test_navbar_links_exists_not_authenticated_user(self):
        signup_url = reverse('signup')
        login_url = reverse('login')
        self.assertContains(self.response, 'href="{0}"'.format(signup_url))
        self.assertContains(self.response, 'href="{0}"'.format(login_url))

    def test_navbar_links_exists_authenticated_user(self):
        user = User.objects.create_user(username='susiesalmon', password='abc123', email='ss@gmail.com', first_name='Susie', last_name='Salmon')
        self.client.login(username='susiesalmon', password='abc123')
        logout_url = reverse('logout')
        url = reverse('index')
        response = self.client.get(url)
        self.assertTrue(User.objects.exists())
        self.assertTrue(user.is_authenticated)
        self.assertContains(response, 'href="{0}"'.format(logout_url))