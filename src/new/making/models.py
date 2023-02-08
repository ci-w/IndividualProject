from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# when you create a new model, need to add it to admin.py to see it in admin interface

class UserProfile(models.Model):
    # links the User instance its associated with, Users can have multiple UserProfiles
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    requirements = models.OneToOneField("Requirements", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user_name

class Project(models.Model):
    title = models.CharField(max_length=50)
    requirements = models.OneToOneField("Requirements", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title 

class Requirements(models.Model):
    VISION_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High')
    ]
    vision = models.IntegerField(choices=VISION_CHOICES)
    dexterity = models.IntegerField(choices=VISION_CHOICES)
    language = models.IntegerField(choices=VISION_CHOICES)
    memory = models.IntegerField(choices=VISION_CHOICES)
    

class Tool(models.Model):
    name = models.CharField(max_length=30)
    skill_level = models.IntegerField()
    requirements = models.ForeignKey(Requirements, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name