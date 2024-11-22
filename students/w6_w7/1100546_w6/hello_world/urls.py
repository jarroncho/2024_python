from django.urls import path
from . import views

urlpatterns = [
    path('simple/', views.simple_hello, name='simple_world'),
    path('template/', views.template_hello, name='template_world'),
    path('student/', views.student, name='student')
]