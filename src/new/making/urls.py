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
    path('profile/', views.profile, name='profile'),
]