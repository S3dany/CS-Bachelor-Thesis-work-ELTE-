from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('profile', views.show_profile, name='show_profile'),
    path('report/<uuid:id>', views.show_report, name='show_report'),
    path('new_report', views.create_report, name='create_report'),
 ]