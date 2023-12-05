from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProjectState(models.Model):
    state = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Project(models.Model):
    name =  models.CharField(max_length=255) 
    abbreviation =  models.CharField(max_length=255) 
    description =  models.TextField() 
    purpose =  models.TextField() 
    state =  models.ForeignKey(ProjectState, on_delete=models.SET_NULL, null=True)
    pseudocode =  models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)