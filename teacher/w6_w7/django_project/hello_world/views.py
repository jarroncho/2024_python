from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Student

# Create your views here.
def home_hello(request):
    return HttpResponse("Home Hello world!")


def simple_hello(request):
    return HttpResponse("Simple Hello world!")


def template_hello(request):
  template = loader.get_template('first_page.html')
  return HttpResponse(template.render())


def student(request):
    my_students = Student.objects.all().values()
    template = loader.get_template('student.html')
    context = {
        'Students': my_students,
    }
    return HttpResponse(template.render(context, request))
