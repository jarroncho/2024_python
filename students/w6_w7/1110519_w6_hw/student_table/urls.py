from django.urls import path
from . import views

urlpatterns = [    
    path('simple/', views.simple_view, name='simple'),
    path('template/', views.template_view, name='template'),
    path('students/', views.student_list_view, name='student_list'),
]