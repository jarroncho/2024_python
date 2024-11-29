from django.db import models

# Create your models here.
from django.core.validators import MaxValueValidator

# Create your models here.

class Student_V2(models.Model):     
    name = models.CharField(max_length=255)
    student_ID = models.CharField(max_length=10,default='ST_0000')
  
  

    def __str__(self):
        return self.name

class Course(models.Model):      
    student = models.OneToOneField(Student_V2, on_delete=models.CASCADE, related_name='course')
    chinese_score = models.IntegerField(validators=[MaxValueValidator(limit_value=100)], default=0)  
    english_score = models.IntegerField(validators=[MaxValueValidator(limit_value=100)], default=0)
    math_score = models.IntegerField(validators=[MaxValueValidator(limit_value=100)], default=0)
    physics_score = models.IntegerField(validators=[MaxValueValidator(limit_value=100)], default=0)
   
  
    def __str__(self):
        return self.student.name 