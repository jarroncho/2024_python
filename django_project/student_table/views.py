from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Student

# Create your views here.
def home_hello(request):
    return HttpResponse("Welcome!")

def student(request):
    my_students = Student.objects.all().values()
    template = loader.get_template('student.html')
    context = {
        'Students': my_students,
    }
    return HttpResponse(template.render(context, request))