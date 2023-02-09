from django.shortcuts import render, redirect
from making.forms import RequirementsForm, ToolForm, UserForm, ProfileForm
from making.models import Requirements, Tool
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.

def index(request):
    #form = inlineformset_factory(Requirements, Tool, fields='__all__')
    form = UserForm()
    return render(request, 'making/index.html', {'form':form})

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
        #user_form = LoginForm(request.POST)
        #email = user_form.email
        #password = user_form.password
        #username = request.POST.get('username')
        #password = request.POST.get('password')
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
def profile(request):
    # tells the template if registration was successful 
    registered = False 
    # if its a HTTP post, we want to process form data
    if request.method == 'POST':
        # try to get info from the raw form info 
        profile_form = ProfileForm(request.POST)
        requirements_form = RequirementsForm(request.POST)
        tool_form = ToolForm(request.POST)
        # if the forms are valid
        if profile_form.is_valid(): 
            user = request.user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            if requirements_form.is_valid():
                # this crashes
                requirements = requirements_form.save()
                profile.requirements = requirements
                profile.save()
                if tool_form.is_valid():
                    tool = tool_form.save(commit=False)
                    tool.requirements = requirements
                    tool.save()
           
            registered = True
        else: 
            print(profile_form.errors)
    else: 
        # not a http POST, so render form using modelForm instance - blank ready for user input
        profile_form = ProfileForm()
        requirements_form = RequirementsForm()
        tool_form = ToolForm()

    # render template depending on context 
    return render(request, 'making/profile.html', context = {'profile_form': profile_form, 'requirements_form': requirements_form, 'tool_form': tool_form, 'registered': registered})

@login_required
def view_user(request):
    user = request.user
    return render(request, 'making/view_user.html', context = {'user': user})
