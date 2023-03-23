from django.db import models
from django.contrib.auth.models import User
from making_project.settings import BASE_DIR
import os
from django.utils.safestring import mark_safe   # for putting html in help text
# when you create a new model, need to add it to admin.py to see it in admin interface
# should probably do isinstance checks with equality functions

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
    
    def view_dict(self):
        data = {'profile_name': self.profile_name}
        data.update(Requirements.view_dict(self.requirements))
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
    
    #try and get the projects image(s). SAY how many images there are ? or just punt the filenames of them all to the view
    # I WILL HAVE TO CHANGE THIS PATH WHEN I HOST IT, MAYBE USE DJANGO STATIC URL NAMESPACES
    # get the names and relative paths (i.e. the path after STATIC_URL) of all projects images, punt them through  
    # NEED to handle it having no images     
    def get_img_path(self):
        # get the full path to wherever the images are stored
        # first get the bit after BASE_DIR (on local, base_dir = "new" dir, using backslashes)
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
        # should probably have a folder for thumbnails
        # for now, just picking the first image in a projects image folder as its thumbnail
       # thumbnail = self.get_img_path()[0]
        check = self.get_img_path() 
        if check:
            thumbnail = check[0]
        else:
            thumbnail = None
        data = {'pk':self.pk,'title':self.title,'description':self.description, 'thumbnail': thumbnail}
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
    vision = models.IntegerField(choices=VISION_CHOICES, help_text=mark_safe("This is how much you can see. <ul class='list-unstyled'><li> Low: you can read off a road sign.</li><li>Medium: you can read large text.</li><li>High: you can read small text.</li> </ul>"),default=1)
    dexterity = models.IntegerField(choices=VISION_CHOICES, help_text=mark_safe("This is how much you can use your hands to do things.<ul class='list-unstyled'><li> Low: you can put Duplo blocks together. </li><li>Medium: you can </li><li>High: you can put Lego blocks together. </li> </ul>"),default=1)
    language = models.IntegerField(choices=VISION_CHOICES, help_text=mark_safe("This is what sort of instructions you can understand.<ul class='list-unstyled'><li> Low: you can </li><li>Medium: you can </li><li>High: you can </li> </ul>"),default=1)
    memory = models.IntegerField(choices=VISION_CHOICES, help_text=mark_safe("This is what your memory is like.<ul class='list-unstyled'><li> Low: you can </li><li>Medium: you can </li><li>High: you can </li> </ul>"),default=1)

    class Meta:
        verbose_name = "Requirements"
        verbose_name_plural = "Requirements"

    def __str__(self):
        return(str(self.id))

    def syl_dict(self):
        tools_qs = self.tool_set.all() 
        tools = [Tool.syl_dict(i) for i in tools_qs]
        data = {'vision': self.vision, 'dexterity': self.dexterity, 'language': self.language, 'memory': self.memory, 'tools':tools}
        return data

    # returns the skill levels as the related choices word rather than a number
    def view_dict(self):
        tools_qs = self.tool_set.all() 
        tools = [Tool.view_dict(i) for i in tools_qs]
        data = {'vision': self.get_vision_display(), 'dexterity': self.get_dexterity_display(), 'language': self.get_language_display(), 'memory': self.get_memory_display(), 'tools': tools}
        return data
    
    def equality(self, other):
        return self.vision == other.vision and self.dexterity == other.dexterity and self.language == other.language and self.memory == other.memory 
   # maybe something here that drags in its related Tool objects? 

# custom manager for Tools
class ToolManager(models.Manager):
    # returns all unique tool names as [str]
    def get_names(self):
        return super().values_list('name', flat=True).distinct()
    # returns CHOICES version of tool names [(str,str)]
    def get_choices(self):
        tool_names = Tool.choices_objects.get_names() 
        return [(i, i) for i in tool_names] 
   # def get_computer(self, name):
        #return super().get_queryset().filter(name=name)
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
    def equality(self, other):
        return self.name == other.name and self.skill_level == other.skill_level
    
    def greater(self, other):
        return self.name == other.name and self.skill_level > other.skill_level 
    
    def satf(self, other):
        return self.name == other.name and self.skill_level <= other.skill_level