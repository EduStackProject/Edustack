from django.db import models
import uuid
class Student(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True,editable=False)
    name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=1)
    phno=models.CharField(max_length=10)
