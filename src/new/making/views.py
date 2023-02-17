from django.shortcuts import render, redirect
from making.forms import RequirementsForm, ToolForm, UserForm, ProfileForm, SyllabusForm
from making.models import Requirements, Tool, UserProfile, Project
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.

def index(request):
    try:
        # need to change this to filter when default profile is implemented
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    return render(request, 'making/index.html', context = {'user_profile': user_profile})

def about(request):
    return render(request, 'making/about.html')

#todo: have the tab (i forget word) for this page display the projects title
def projects(request, project_id):
    try:
        #is there a project with that id?
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        project = None 
    return render(request, 'making/projects.html', context={'project': project})


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

# todo: fancy way of turning model instance into dict
def create_syllabus(request):
    if request.method == 'POST':
        syllabus_form = SyllabusForm(request.POST)
        if syllabus_form.is_valid():
            user = request.user 
            user_profile = UserProfile.objects.filter(user=user)[0]
            test = user_profile.__dict__
            up_copy = {'UP_id': test['id'], 'requirements_id': test['requirements_id']}
            up_req = Requirements.objects.get(id=up_copy['requirements_id'])
            up_req = up_req.__dict__
            up_copy['vision'] = up_req['vision']
            up_copy['dexterity'] = up_req['dexterity']
            up_copy['language'] = up_req['language']
            up_copy['memory'] = up_req['memory']   

            tools = Tool.objects.filter(requirements=up_copy['requirements_id'])
            tools = tools.values()
            list =  [entry for entry in tools]
            up_copy['tools'] = list

            end_proj_id = syllabus_form.cleaned_data['end_project']
            end_project = Project.objects.get(id=end_proj_id)
            end_project = end_project.__dict__
            end_req = Requirements.objects.get(id=end_project['requirements_id'])
            end_req = end_req.__dict__
            end_project['vision'] = end_req['vision']
            end_project['dexterity'] = end_req['dexterity']
            end_project['language'] = end_req['language']
            end_project['memory'] = end_req['memory']  
            proj_tools = Tool.objects.filter(requirements=end_project['requirements_id'])
            proj_tools = proj_tools.values()
            proj_list =  [entry for entry in proj_tools]
            end_project['tools'] = proj_list
            end_project.pop('_state')
            end_project.pop('title')
            end_project.pop('instructions')
            end_project.pop('description')

            # i start doing things with end_proj here
            end_project.pop('id')
            end_project.pop('requirements_id')
            end_project['tools'][0].pop('requirements_id')
            end_project['tools'][0].pop('id')            
            end_project['tools'][1].pop('requirements_id')
            end_project['tools'][1].pop('id')

            # things with UP
            up_copy.pop('UP_id')
            up_copy.pop('requirements_id')
            up_copy['tools'][0].pop('requirements_id')
            up_copy['tools'][0].pop('id')            
            up_copy['tools'][1].pop('requirements_id')
            up_copy['tools'][1].pop('id')

            # ??
            for tool in end_project['tools']:
                # tool is a dictionary :)
                help = tool
                # does the UP have this tool
                for up_tool in up_copy['tools']:
                    if up_tool['name'] == tool['name']:
                        #is the tool at the correct level?
                        if up_tool['skill_level'] < tool['skill_level']:
                            #try find a project 
                            present = up_tool
                #help = up_copy['tools'][1]['name'] == tool['name']
            

            
        else:
            print(syllabus_form.errors)
    else:
        end_proj_id = None
        end_project = None
        test = None
        up_copy = None
        syllabus_form = SyllabusForm()
        up_req = None
        tools = None
        list = None
        end_req = None
        help = None
        present = None


    return render(request, 'making/create_syllabus.html', context = {'syllabus_form': syllabus_form, 'end_proj_id': end_proj_id, 'end_project':end_project, 'up_copy':up_copy, 'tools':tools, 'list':list, 'end_req':end_req, 'help':help, 'present':present})