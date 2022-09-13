from django.test import SimpleTestCase
from app import views
from django.urls import reverse, resolve
import uuid


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home', args=[])
        self.assertEquals(resolve(url).func, views.home)

    def test_register_url_resolves(self):
        url = reverse('register', args=[])
        self.assertEquals(resolve(url).func, views.register)

    def test_show_profile_url_resolves(self):
        url = reverse('show_profile', args=[])
        self.assertEquals(resolve(url).func, views.show_profile)

    def test_create_report_url_resolves(self):
        url = reverse('create_report', args=[])
        self.assertEquals(resolve(url).func, views.create_report)

    def test_show_report_url_resolves(self):
        url = reverse('show_report', args=[uuid.uuid4()])
        self.assertEquals(resolve(url).func, views.show_report)