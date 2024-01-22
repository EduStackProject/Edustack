from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=1)
    phno=models.CharField(max_length=10)
