from django.urls import path
from making import views 

app_name = 'making'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('projects/<int:project_id>/', views.project, name='project'),
    path('projects/', views.projects, name='projects'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('view_profile/', views.view_profile, name="view_profile",),
    path('update_profile/',views.update_profile, name="update_profile"),
    path('select_profile/', views.select_profile, name="select_profile"),
    path('add_tool/', views.add_tool, name="add_tool"),
    path('create_syllabus/', views.create_syllabus, name="create_syllabus"),
]