from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class product(models.Model):
    name=models.CharField(max_length=100,default='null')
    price=models.IntegerField(default=0)
class file(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    File_id=models.AutoField(unique=True,primary_key=True)
    Title=models.CharField(max_length=300,default='file')
    File=models.FileField(upload_to='media',default='')
    def __str__(self):
        return self.Title


    