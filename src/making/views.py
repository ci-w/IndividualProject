from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse
from making.models import Category, Project

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    
    project_list = Project.objects.order_by('title')[:6]
    context_dict = {}
    context_dict['projects'] = project_list
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'making/index.html', context=context_dict)

def about(request):
    return HttpResponse("Hiii")
