from django.contrib import admin
from making.models import UserProfile, Project, Requirements, Tool
from django.utils.html import format_html
from django.urls import reverse

# Register your models here

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_name', 'user', 'requirements')
admin.site.register(UserProfile, UserProfileAdmin)

class RequirementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'vision', 'dexterity', 'language', 'memory')
admin.site.register(Requirements, RequirementsAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description','materials', 'instructions', 'requirements')
    list_display_links = ('id','title')
admin.site.register(Project, ProjectAdmin)

class ToolAdmin(admin.ModelAdmin):
    def req_link(self, obj):
        url = reverse('admin:making_requirements_change', args=(obj.requirements.id,))
        return format_html("<a href='{}'>{}</a>", url, obj.requirements.id)
    req_link.admin_order_field = 'requirements'
    req_link.short_description = 'requirements'
    list_display = ['id', 'name', 'skill_level', 'req_link',]
admin.site.register(Tool, ToolAdmin)