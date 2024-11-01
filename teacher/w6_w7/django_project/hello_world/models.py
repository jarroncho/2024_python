from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

class Student(models.Model):  
  id = models.IntegerField(primary_key=True)  
  name = models.CharField(max_length=255)
  
  #give a default value for models.charfield

  
 

  def __str__(self):
    return self.name
