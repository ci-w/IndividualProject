from django.db import models
from django.contrib.auth.models import User
# when you create a new model, need to add it to admin.py to see it in admin interface
# should probably do isinstance checks with equality functions

class UserProfile(models.Model):
    # links the User instance its associated with, Users can have multiple UserProfiles
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=100)
    requirements = models.OneToOneField("Requirements", on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.profile_name
    
    # this will throw out ALL the concrete fields
    def to_dict(self):
        opts = UserProfile._meta
        data = {}
        for f in opts.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data 
    
    def syl_dict(self):
        data = {'requirements_id': self.requirements.id}
        data.update(Requirements.syl_dict(self.requirements))
        return data
    
    # returns true if the REQUIREMENTS are equal
    def equality(self, other): 
        return Requirements.equality(self.requirements, other.requirements)

# custom manager for Projects
class ProjectManager(models.Manager):
    def get_choices(self):
        return super().values_list('pk','title')

class Project(models.Model):
    title = models.CharField(max_length=50)
    requirements = models.OneToOneField("Requirements", on_delete=models.DO_NOTHING)
    instructions = models.TextField()
    description = models.TextField(max_length=100)

    # default manager
    objects = models.Manager()
    # custom manager
    choices_objects = ProjectManager()
    
    def __str__(self):
        return self.title 
    
    def syl_dict(self):
        data = {'p_id': self.id, 'requirements_id': self.requirements.id}
        data.update(Requirements.syl_dict(self.requirements))
        return data
    
    # returns true if the REQUIREMENTS are equal
    def equality(self, other): 
        return Requirements.equality(self.requirements, other.requirements)

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

    def syl_dict(self):
        data = {'vision': self.vision, 'dexterity': self.dexterity, 'language': self.language, 'memory': self.memory}
        return data
    
    def equality(self, other):
        return self.vision == other.vision and self.dexterity == other.dexterity and self.language == other.language and self.memory == other.memory 
   # maybe something here that drags in its related Tool objects? 
   
class Tool(models.Model):
    name = models.CharField(max_length=30)
    skill_level = models.IntegerField()
    requirements = models.ForeignKey(Requirements, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def syl_dict(self):
        data = {'name': self.name, 'skill_level': self.skill_level}
        return data
    
    def equality(self, other):
        return self.name == other.name and self.skill_level == other.skill_level
    
    def greater(self, other):
        return self.name == other.name and self.skill_level > other.skill_level 
    
    def satf(self, other):
        return self.name == other.name and self.skill_level <= other.skill_level