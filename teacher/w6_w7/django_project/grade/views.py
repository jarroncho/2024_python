from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Student_V2, Course
from django import forms

# Define local class
class StudentForm(forms.Form):
    # Define your form fields here    
    student_ID= forms.CharField(label='Student ID', max_length=10)
    name = forms.CharField(label='Name', max_length=255)
    chinese_score = forms.IntegerField(label='Chinese_Score')

 

class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student_V2
        fields = '__all__'


# Create your views here.
def grade_hello(request):
    return HttpResponse("Grade Hello world!")

# show student
def student(request):
    my_students = Student_V2.objects.all().values()
    template = loader.get_template('student_v2.html')
    context = {
        'Students': my_students,
    }
    return HttpResponse(template.render(context, request))



# show student_course
def student_course(request):
    my_students = Student_V2.objects.all()    
    template = loader.get_template('student_v2_course.html')    
    context = {
        'Students': my_students,
    }
    return HttpResponse(template.render(context, request))



# Create a new student
def student_new(request):
    # Handle form submission
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            # Process the form data (you can save it to the database or perform other actions)
            # For now, just print the form data            
            student_instance = Student_V2.objects.create(name=request.POST.get('name',''),student_ID=request.POST.get('student_ID',''))            
            course_instance = Course.objects.create(student=student_instance) 
            course_instance.chinese_score = request.POST.get('chinese_score', '')    
            course_instance.save()          
            student_instance.save()
            print(form.cleaned_data)
            # Redirect to a new URL:
            return redirect('student_v2_course')
        
    else:
        # Display the form for the first time
        form = StudentForm()

    # Render the HTML template with the form
    return render(request, 'student_v2_new.html', {'form': form})

# Delete a student
def student_delete(request,record_id):
    # Get the record from the database
    record = get_object_or_404(Student_V2, id=record_id)
    # Delete the record
    record.delete()    
    return redirect('student_v2_course')

# Update a student
def student_update(request,record_id):
    # Get the record from the database
    record = get_object_or_404(Student_V2, id=record_id)

    if request.method == 'POST':
        # Update the record from post data
        form = StudentModelForm(request.POST, instance=record)
        if form.is_valid():            
            #update the record to the database
            form.save()
            return redirect('student_v2_course')  # Redirect to another URL after updating
    else:
        form = StudentModelForm(instance=record)

    return render(request, 'student_v2_update.html', {'form': form, 'record': record})