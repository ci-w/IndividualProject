from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login 
from django.urls import reverse

from making.models import Category, Project
from making.forms import UserForm, UserProfileForm

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
        
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

def register(request):
    # tells the template if registration was successful 
    registered = False 

    # if its a HTTP post, we want to process form data
    if request.method == 'POST':
        # try to get info from the raw form info 
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST) 

        # if the forms are valid
        if user_form.is_valid() and profile_form.is_valid(): 
            # save users form data to the db 
            user = user_form.save() 
            # hash password, update user object
            user.set_password(user.password)
            user.save() 

            profile = profile_form.save(commit=False)
            profile.user = user 

            profile.save()

            registered = True
        else: 
            print(user_form.errors, profile_form.errors)
    else: 
        # not a http POST, so render form using 2 modelForm instances - blank ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    # render template depending on context 
    return render(request, 'making/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # is the username/pass combo valid? 
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # logs user in and returns them to homepage
                login(request, user)
                return redirect(reverse('making:index'))
            else:
                # inactive account! 
                return HttpResponse("Your account is disabled.")
        else: 
            # log in details arent valid 
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details.")
    else: 
        return render(request, 'making/login.html')