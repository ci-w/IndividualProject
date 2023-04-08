from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from making.models import UserProfile, Project, Requirements, Tool
from django.utils.html import format_html
from django.urls import reverse

class ToolInline(admin.TabularInline):
    model = Tool

class UserProfileInline(admin.TabularInline):
    model = UserProfile

# show a user's profiles in the user model section
class UserAdminCustom(UserAdmin):
    inlines = [ 
        UserProfileInline,
    ]
admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)

class UserProfileAdmin(admin.ModelAdmin):
    def req_link(self, obj):
        url = reverse('admin:making_requirements_change', args=(obj.requirements.id,))
        return format_html("<a href='{}'>{}</a>", url, obj.requirements.id)
    req_link.admin_order_field = 'requirements'
    req_link.short_description = 'requirements'
    list_display = ('profile_name', 'user', 'req_link')
admin.site.register(UserProfile, UserProfileAdmin)

class RequirementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'vision', 'dexterity', 'language', 'memory')
    inlines = [
        ToolInline,
    ]
admin.site.register(Requirements, RequirementsAdmin)

class ProjectAdmin(admin.ModelAdmin):
    def req_link(self, obj):
        url = reverse('admin:making_requirements_change', args=(obj.requirements.id,))
        return format_html("<a href='{}'>{}</a>", url, obj.requirements.id)
    req_link.admin_order_field = 'requirements'
    req_link.short_description = 'requirements'
    list_display = ('id', 'title', 'description','materials', 'instructions', 'req_link')
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