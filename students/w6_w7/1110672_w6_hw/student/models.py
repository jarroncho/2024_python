from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=50)
    st_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
