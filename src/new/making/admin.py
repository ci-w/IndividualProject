from django.contrib import admin
from making.models import UserProfile, Project, Requirements, Tool

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Requirements)
admin.site.register(Tool)