from django.urls import path
from making import views

app_name = 'making'
h
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about' ),
    path('project/<slug:project_name_slug>/',
        views.show_project, name='show_project'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('search/', views.search, name="search"),
    path('update/', views.update_requirements, name="update"),
    path('profile/', views.view_profile, name="profile"),
]