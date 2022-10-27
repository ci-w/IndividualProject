from django.urls import path
from making import views

app_name = 'making'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about' ),
    path('project/<slug:project_name_slug>/',
        views.show_project, name='show_project'),
]