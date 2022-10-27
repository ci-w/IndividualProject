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

def show_project(request, project_name_slug):
    context_dict = {}
    try:
        # is there a project with the given name?
        project = Project.objects.get(slug=project_name_slug)
        # add it to context dictionary
        context_dict['project'] = project
    except Project.DoesNotExist:
        context_dict['project'] = None;
    return render(request, 'making/project.html', context=context_dict)
