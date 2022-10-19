from django.urls import path
from making import views

app_name = 'making'

urlpatterns = [
    path('', views.index, name='index'),
]