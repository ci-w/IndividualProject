from django.contrib import admin
from making.models import Category, Project, UserProfile

# Register your models here by importing it and calling it below
admin.site.register(Category)
admin.site.register(Project)
admin.site.register(UserProfile)
