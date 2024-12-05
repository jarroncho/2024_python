from django.shortcuts import render
from django.http import HttpResponse

def simple_hello(request):
    return HttpResponse("Simple Hello world")

from django.urls import path
from . import views

urlpatterns=[
    path('simple/', views.simple_hello,name='simple_world')
]

from django.contrib import admin
from django.urls import include, path

urlpatterns=[
    path('',views.home_hello,name='home'),
    path('hello_world/', include('hello_world.urls')),
    path('admin/', admin.site.urls),
]

