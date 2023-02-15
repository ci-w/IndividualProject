from django.shortcuts import render, redirect
from making.forms import RequirementsForm, ToolForm, UserForm, ProfileForm
from making.models import Requirements, Tool, UserProfile
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.

def index(request):
    try:
        user_profile = UserProfile.objects.filter(user=request.user)[0]
    except UserProfile.DoesNotExist:
        user_profile = None
    return render(request, 'making/index.html', context = {'user_profile': user_profile})

def about(request):
    return render(request, 'making/about.html')

def project(request):
    pass

def projects(request):
    pass

def register(request):
# tells the template if registration was successful 
    registered = False 
    # if its a HTTP post, we want to process form data
    if request.method == 'POST':
        # try to get info from the raw form info 
        form = UserForm(request.POST)
        # if the forms are valid
        if form.is_valid(): 
            # save users form data to the db 
            user = form.save() 
            # hash password, update user object
            user.set_password(user.password)
            user.save() 
            registered = True
        else: 
            print(form.errors)
    else: 
        # not a http POST, so render form using modelForm instance - blank ready for user input
        form = UserForm()

    # render template depending on context 
    return render(request, 'making/register.html', context = {'form': form, 'registered': registered})

def user_login(request):
    worked = False
    if request.method == 'POST':
        form = UserForm(request.POST)
        username = form['username'].value()
        password = form['password'].value()
        # are details valid?
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            worked = True
            #return redirect(reverse('making:index'))            
    else:
        form = UserForm()
    return render(request, 'making/login.html', context={'form': form, 'worked': worked})
 
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('making:index'))

# assuming this is creating new profile
@login_required
def create_profile(request):
    # tells the template if registration was successful 
    registered = False 
    # if its a HTTP post, we want to process form data
    if request.method == 'POST':
        # try to get info from the raw form info 
        profile_form = ProfileForm(request.POST)
        requirements_form = RequirementsForm(request.POST)
        # if the forms are valid
        if profile_form.is_valid() and requirements_form.is_valid(): 
            user = request.user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()         
            requirements = requirements_form.save()
            profile.requirements = requirements
            profile.save()           
            registered = True
        else: 
            print(profile_form.errors)
    else: 
        # not a http POST, so render form using blank form instances for user input
        profile_form = ProfileForm()
        requirements_form = RequirementsForm()
    # render template depending on context 
    return render(request, 'making/create_profile.html', context = {'profile_form': profile_form, 'requirements_form': requirements_form,'registered': registered})

@login_required
def view_user(request):
    user = request.user
    return render(request, 'making/view_user.html', context = {'user': user})

@login_required
def view_profile(request):
    user = request.user
    # this automatically just picks the first user profile, need to change this
    try:
        user_profile = UserProfile.objects.filter(user=user)[0]
    except UserProfile.DoesNotExist:
        user_profile = None
    try:
        tools = Tool.objects.filter(requirements=user_profile.requirements)
    except Tool.DoesNotExist:
        tools = None
    return render(request, 'making/view_profile.html', context = {'user':user, 'user_profile': user_profile, 'tools':tools})

@login_required 
# also UP required.. how to enforce?
# this also just picks the first UP
def update_profile(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.filter(user=user)[0]
    except UserProfile.DoesNotExist:
        user_profile = None
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user_profile)
        requirements_form = RequirementsForm(request.POST, instance=user_profile.requirements)
        if profile_form.is_valid() and requirements_form.is_valid():
            profile_form.save()
            requirements_form.save()
        else:
            print(profile_form.errors, requirements_form.errors)
    else:
        profile_form = ProfileForm(instance=user_profile)
        requirements_form = RequirementsForm(instance=user_profile.requirements)
    return render(request, 'making/update_profile.html', context={'profile_form':profile_form, 'requirements_form':requirements_form})

@login_required
def add_tool(request):
    user = request.user 
    try:
        user_profile = UserProfile.objects.filter(user=user)[0]
    except UserProfile.DoesNotExist:
        user_profile = None
    # tells the template if registration was successful 
    registered = False 
    # if its a HTTP post, we want to process form data
    if request.method == 'POST':
        # try to get info from the raw form info 
        tool_form = ToolForm(request.POST)
        # if the forms are valid
        if tool_form.is_valid(): 
            tool = tool_form.save(commit=False)
            tool.requirements = user_profile.requirements
            tool.save()                 
            registered = True
        else: 
            print(tool_form.errors)
    else: 
        # not a http POST, so render form using blank form instances for user input
        tool_form = ToolForm()

    # render template depending on context 
    return render(request, 'making/add_tool.html', context = {'tool_form': tool_form, 'registered': registered})