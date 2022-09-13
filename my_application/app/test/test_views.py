from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from app.models import Profile, Report
import uuid, os


class TestViews(TestCase):

    def test_home(self):
        response = self.client.get(reverse("home"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_register(self):
        response = self.client.get(reverse("register"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_login(self):
        response = self.client.get(reverse("login"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_show_profile(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse("show_profile"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_show_report(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        file_path = os.path.join('app\\test\\test_files', 'output_sample.xlsx')
        self.report = Report.objects.create(id=uuid.uuid4(), output_data=file_path)
        response = self.client.get(reverse("show_report", args=[self.report.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Report.html')

    def test_create_report(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse("create_report"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Report_form.html')
