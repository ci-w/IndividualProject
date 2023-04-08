from django.db import models
from django.contrib.auth.models import User
from making_project.settings import BASE_DIR
import os
from django.utils.safestring import mark_safe   # for putting html in help text
# when you create a new model, need to add it to admin.py to see it in admin interface

# custom manager for Profiles
class ProfileManager(models.Manager):
    def get_profiles(self, id):
        return super().get_queryset().filter(user=id)

    def get_choices(self, id):
        profiles = UserProfile.choices_objects.get_profiles(id)
        return [(i.pk, i.profile_name) for i in profiles]

class UserProfile(models.Model):
    # links the User instance its associated with, Users can have multiple UserProfiles
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=100)
    requirements = models.OneToOneField("Requirements", on_delete=models.DO_NOTHING, null=True)

    # default manager
    objects = models.Manager()
    # custom manager
    choices_objects = ProfileManager()

    class Meta:
        verbose_name ="User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.profile_name

    def syl_dict(self):
        data = {'requirements_id': self.requirements.id}
        data.update(Requirements.syl_dict(self.requirements))
        return data

    def view_dict(self):
        data = {'profile_name': self.profile_name}
        data.update(Requirements.view_dict(self.requirements))
        return data

# custom manager for Projects
class ProjectManager(models.Manager):
    def get_choices(self):
        return super().values_list('pk','title')

class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    materials = models.TextField(max_length=300)
    instructions = models.TextField()

    requirements = models.OneToOneField("Requirements", on_delete=models.DO_NOTHING)

    # default manager
    objects = models.Manager()
    # custom manager
    choices_objects = ProjectManager()

    class Meta:
        verbose_name ="Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    # this is used in the create_syllabus view
    def syl_dict(self):
        data = {'p_id': self.id, 'requirements_id': self.requirements.id}
        data.update(Requirements.syl_dict(self.requirements))
        return data

    # this is used in the project view + project template
    def view_dict(self):
        # materials are split by comma, convert them into a list
        materials = self.materials.split(",")
        # instructions are split by [], convert them to list, strip whitespace and remove any empty strings
        instructions = (self.instructions).split("[]")
        instructions = [i.strip() for i in instructions if i]

        data = {'title': self.title, 'description': self.description, 'materials':materials, 'instructions':instructions }
        data.update(Requirements.view_dict(self.requirements))
        return data

    def get_img_path(self):
        # get the full path to wherever the images are stored
        dir_path = 'making\\static\\making\\images\\projects\\' + str(self.pk)
        full_path = os.path.join(BASE_DIR, dir_path)
        full_path = full_path.replace("\\", "/")
        # if the project actually has a dir/any images
        if os.path.isdir(full_path):
            dir_contents = os.listdir(full_path)
            # need to pass through the personalised URL that you add to {static } in template
            project_path = "making/images/projects/" + str(self.pk)+ "/"
            paths = [(project_path + i) for i in dir_contents]
            return paths

    # function to return data needed for previews of projects
    def preview_dict(self):
        # should probably have a folder for thumbnails, for now picking first image in the projects folder
        try: 
            thumbnail = self.get_img_path()[0]
        except: 
            thumbnail = None
        return {'pk':self.pk,'title':self.title,'description':self.description, 'thumbnail': thumbnail}

class Requirements(models.Model):
    CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High')
    ]
    vision = models.IntegerField(choices=CHOICES, help_text=mark_safe("<p>This is how much you can see.</p>  <ul class='list-unstyled'><li> Low: you can read off a road sign.</li><li>Medium: you can read large text.</li><li>High: you can read small text.</li> </ul>"),default=1)
    dexterity = models.IntegerField(choices=CHOICES, help_text=mark_safe("<p>This is how much you can use your hands to do things.</p><ul class='list-unstyled'><li> Low: you can stack wooden blocks. </li><li>Medium: you can put Duplo blocks together. </li><li>High: you can put Lego blocks together. </li> </ul>"),default=1)
    language = models.IntegerField(choices=CHOICES, help_text=mark_safe("<p>This is what sort of instructions you can understand.</p><ul class='list-unstyled'><li> Low: you can understand simple instructions with pictures. </li><li>Medium: you can understand simple instructions without pictures. </li><li>High: you can understand more difficult instructions. </li> </ul>"),default=1)
    memory = models.IntegerField(choices=CHOICES, help_text=mark_safe("<p>This is how much you can remember things.</p><ul class='list-unstyled'><li> Low: you need reminders. </li><li>Medium: you can remember some things you've learnt before. </li><li>High: you can remember a lot of things you've learnt before. </li> </ul>"),default=1)

    class Meta:
        verbose_name = "Requirements"
        verbose_name_plural = "Requirements"

    def __str__(self):
        return(str(self.id))

    def syl_dict(self):
        tools_qs = self.tool_set.all()
        tools = [Tool.syl_dict(i) for i in tools_qs]    
        return {'vision': self.vision, 'dexterity': self.dexterity, 'language': self.language, 'memory': self.memory, 'tools':tools}

    # returns the skill levels as the related choices word rather than a number
    def view_dict(self):
        tools_qs = self.tool_set.all()
        tools = [Tool.view_dict(i) for i in tools_qs]
        return {'vision': self.get_vision_display(), 'dexterity': self.get_dexterity_display(), 'language': self.get_language_display(), 'memory': self.get_memory_display(), 'tools': tools}

# custom manager for Tools
class ToolManager(models.Manager):
    # returns all unique tool names as [str]
    def get_names(self):
        return super().values_list('name', flat=True).distinct()

    # returns CHOICES version of all unique tool names [(str,str)]
    def get_choices(self):
        tool_names = Tool.choices_objects.get_names()
        return [(i, i) for i in tool_names]

    # gets all the tool object choices associated with a given requirements object
    def get_req_tools(self, requirements):
        tools = super().get_queryset().filter(requirements=requirements)
        tool_choices = tools.values_list('name','skill_level')
        return tool_choices

class Tool(models.Model):
    LEVEL_CHOICES = [
        (0, 'None'),
        (1, 'Beginner'),
        (2, 'Competent'),
        (3, 'Expert')
    ]
    name = models.CharField(max_length=30)
    skill_level = models.IntegerField(choices=LEVEL_CHOICES,default=0)
    requirements = models.ForeignKey(Requirements, on_delete=models.CASCADE)

    # default manager
    objects = models.Manager()
    # custom manager
    choices_objects = ToolManager()

    class Meta:
        verbose_name = "Tool"
        verbose_name_plural = "Tools"
        # each requirements object can only have 1 tool object per tool name
        constraints = [
            models.UniqueConstraint(fields=['name', 'requirements'], name='unique_tool')
        ]

    def __str__(self):
        return self.name

    def syl_dict(self):
        data = {'name': self.name, 'skill_level': self.skill_level}
        return data

    def view_dict(self):
        data = {'name': self.name, 'skill_level': self.get_skill_level_display()}
        return data