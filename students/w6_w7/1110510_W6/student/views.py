from django.shortcuts import render
from django.http import HttpResponse
from .models import Student

def simple_view(request):
    return HttpResponse("Hello, World!")

def template_view(request):
    return render(request, 'master.html')

def student_list_view(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

