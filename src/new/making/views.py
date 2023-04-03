from django.shortcuts import render, redirect
from making.forms import RequirementsForm, ToolForm, UserForm, LoginForm, ProfileForm, SyllabusForm, SwitchProfileForm, BaseToolFormSet
from making.models import Requirements, Tool, UserProfile, Project
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from copy import deepcopy
from pathlib import Path
import os
from making_project.settings import BASE_DIR, STATIC_URL
from django.forms import formset_factory
from django.core.exceptions import ValidationError

# helper function that gets current user profile OBJECT
def getProfile(request):
    try:
        user_profile = UserProfile.objects.get(id=request.session['user_profile'])
    except:
        user_profile = None
    return user_profile

def index(request):
    user_profile = getProfile(request)
    return render(request, 'making/index.html', context = {'user_profile': user_profile})

def about(request):
    return render(request, 'making/about.html')

# view of multiple projects, just grabs the first 10
def projects(request):
    user_profile = getProfile(request)
    project_objs = Project.objects.all()[:10]
    # get all the preview dicts of the objects
    projects = [Project.preview_dict(i) for i in project_objs]
    return render(request, 'making/projects.html', context={'user_profile':user_profile,'projects': projects})

# specific project
def project(request, project_id):
    user_profile = getProfile(request)
    # turn profile into a dict 
    if user_profile:
        user_profile = UserProfile.view_dict(user_profile)
    # need to order profile tools in the same order as project (zip them together)
    paths = None
    try:
        #is there a project with that id?
        project_obj = Project.objects.get(id=project_id)
        # turn into dictionary, get the related requirements and tool objects (if any tools)
        project = Project.view_dict(project_obj)
        paths = Project.get_img_path(project_obj)
    except Project.DoesNotExist:
        project = None 
    return render(request, 'making/project.html', context={'user_profile':user_profile,'project': project,'paths':paths})

def register(request):
    # tells the template if there was an issue in registration
    error = None 
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid(): 
            # save users form data to the db 
            user = user_form.save() 
            # hash password, update user object
            user.set_password(user.password)
            user.save() 
            # logs the user in and takes them to create profile page
            login(request, user)  
            # they dont have any profiles yet          
            request.session['user_profile'] = None 
            return redirect(reverse('making:create_profile'))             
        else: 
            error = user_form.errors
            #print(user_form.errors)
    else: 
        user_form = UserForm()

    return render(request, 'making/register.html', context = {'user_form': user_form, 'error': error})

def user_login(request):
    error = False
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        username = user_form['username'].value()
        password = user_form['password'].value()
        # are details valid?
        user = authenticate(username=username, password=password)
        if user:
            login(request, user) 
            # initialise session variable  
            request.session['user_profile'] = None          
            profiles = UserProfile.objects.filter(user=user)
            # if the user just has 1 profile, set the session profile to that
            if len(profiles) == 1:
                request.session['user_profile'] = profiles[0].pk
                return redirect(reverse('making:index'))  
            # if the user doesn't have any profiles, redirect them to create profile
            elif len(profiles) == 0:
                return redirect(reverse('making:create_profile'))
            # otherwise redirect them to select profile
            else: 
                return redirect(reverse('making:select_profile'))   
        else:
            error = True         
    else:
        user_form = LoginForm()
    return render(request, 'making/login.html', context={'user_form': user_form, 'error': error})
 
@login_required
def user_logout(request):
    # also deletes session data 
    logout(request)
    return redirect(reverse('making:index'))

@login_required
def create_profile(request):
    # tells the template if creation was successful 
    registered = False 
    user_profile = getProfile(request)
    ToolFormSet = formset_factory(ToolForm, extra=0, max_num=6, formset=BaseToolFormSet)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        requirements_form = RequirementsForm(request.POST)
        toolFormSet = ToolFormSet(request.POST) 
        # if the forms are valid
        if profile_form.is_valid() and requirements_form.is_valid() and toolFormSet.is_valid(): 
            profile = profile_form.save(commit=False)
            profile.user = request.user       
            requirements = requirements_form.save()
            profile.requirements = requirements
            profile.save()           
            registered = True
            # change the session profile to this new one
            request.session['user_profile'] = profile.pk 
            user_profile = getProfile(request)
            # then try to add the tools 
            for form in toolFormSet: 
                tool = form.save(commit=False)
                tool.requirements = user_profile.requirements
                try:
                    tool.full_clean()
                    tool.save()
                except ValidationError as e: 
                    print(e)
        else: 
            print(profile_form.errors)
    else: 
        profile_form = ProfileForm()
        requirements_form = RequirementsForm()
        toolFormSet = ToolFormSet()
    return render(request, 'making/create_profile.html', context = {'user_profile':user_profile,'profile_form': profile_form, 'requirements_form': requirements_form,'toolFormSet':toolFormSet,'registered': registered})

@login_required
def view_user(request):
    user_profile = getProfile(request)
    return render(request, 'making/view_user.html', context = {'user_profile': user_profile})

@login_required
def view_profile(request):
    # get current profile object
    user_profile = getProfile(request)
    #if user doesn't have a profile selected, redirect to homepage
    if not user_profile: 
        return redirect(reverse('making:index'))
    # turn profile obj into dictionary, get the related requirements and tools (if any)
    profile = UserProfile.view_dict(user_profile)
    return render(request, 'making/view_profile.html', context = {'user_profile': user_profile,'profile':profile})

@login_required 
# need to process tool form submission
def update_profile(request):
    user_profile = getProfile(request)
    # if they dont have a profile selected, redirect to select_profile
    if not user_profile:
        return redirect(reverse('making:select_profile'))

    ToolFormSet = formset_factory(ToolForm,extra=0)
    # get all the profiles related tool objects
    tool_qs = user_profile.requirements.tool_set.all()    
    # dictionary version of the tool objects
    tools = tool_qs.values() 

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user_profile)
        requirements_form = RequirementsForm(request.POST, instance=user_profile.requirements)
        toolFormSet = ToolFormSet(request.POST,initial=tools)
        for form in toolFormSet.forms:
            form.fields['name'].choices = [(form.initial['name'],form.initial['name'])]

        if profile_form.is_valid() and requirements_form.is_valid() and toolFormSet.is_valid():
            profile_form.save()
            requirements_form.save()
            for i in range(len(toolFormSet)):
                # update the skill level because thats the only thing that could be changed
                tool_qs[i].skill_level = toolFormSet[i].fields['skill_level']       
        else:
            print(profile_form.errors, requirements_form.errors)
    else:
        profile_form = ProfileForm(instance=user_profile)
        requirements_form = RequirementsForm(instance=user_profile.requirements)

        toolFormSet = ToolFormSet(initial=tools)
        for form in toolFormSet.forms:
            form.fields['name'].choices = [(form.initial['name'],form.initial['name'])]
    return render(request, 'making/update_profile.html', context={'user_profile': user_profile, 'profile_form':profile_form, 'requirements_form':requirements_form, 'toolFormSet':toolFormSet})

# passes list of profiles to template
# cant run functions in template, pass through NUMBER of profiles
@login_required
def select_profile(request):
    user = request.user
    user_profile = getProfile(request)
    profile_choices = UserProfile.choices_objects.get_choices(user.pk)
    # if they dont have any profiles, redirect to create_profile
    if not profile_choices:
        return redirect(reverse('making:create_profile'))
    no_profiles = len(profile_choices)
    
    switch_form = SwitchProfileForm()
    switch_form.fields['profile'].choices = profile_choices

    if request.method == 'POST':
        switch_form = SwitchProfileForm(request.POST)
        # if i dont have line below, it will fail validation (because the form doesn't know the correct choices)
        switch_form.fields['profile'].choices = profile_choices
        if switch_form.is_valid():
            # ID of the chosen profile
            request.session['user_profile'] = switch_form['profile'].value()      
            # re-run this function to get the new user profile object
            user_profile = getProfile(request)     
        else:
            print(switch_form.errors)
    else:
        switch_form = SwitchProfileForm()
        switch_form.fields['profile'].choices = profile_choices

    return render(request, 'making/select_profile.html', context = {'user_profile':user_profile,'switch_form': switch_form, 'no_profiles':no_profiles})

# have to stop people adding a tool they already have - i.e. update it instead
@login_required
def add_tool(request):
    user_profile = getProfile(request)
    ToolFormSet = formset_factory(ToolForm, extra=1, max_num=6, formset=BaseToolFormSet)
    # tells the template if tool was added successfully
    error = None
    success = []
    # if its a HTTP post, we want to process form data
    if request.method == 'POST':
        # try to get info from the raw form info 
        tool_form = ToolForm(request.POST)
        toolFormSet = ToolFormSet(request.POST) 
        for form in toolFormSet:
        # have to do validation this way due to model form not containing all model fields 
            tool = form.save(commit=False)
            tool.requirements = user_profile.requirements
            try:
                tool.full_clean()
                tool.save()
                success.append(tool.name)
            except ValidationError as e:
                error = e
    else: 
        tool_form = ToolForm()
        toolFormSet = ToolFormSet() 
    return render(request, 'making/add_tool.html', context = {'user_profile': user_profile, 'tool_form': tool_form, 'error':error, 'success':success,'toolFormSet':toolFormSet})

@login_required
def create_syllabus(request):
    user_profile_obj = getProfile(request)
    end_project = None
    user_profile = None
    syllabus = None
    projects = None
    if request.method == 'POST':
        syllabus_form = SyllabusForm(request.POST)
        if syllabus_form.is_valid():
            user_profile = UserProfile.syl_dict(user_profile_obj)
            end_proj_id = syllabus_form.cleaned_data['end_project']
            end_project = Project.objects.get(id=end_proj_id)
            end_project = Project.syl_dict(end_project)
            syllabus = []

            while not req_eq(end_project, user_profile):
                arr = imp(end_project, user_profile)

                if find_project(user_profile, arr):
                    new_req, next_proj = find_project(user_profile, arr)
                    user_profile = deepcopy(new_req)
                    syllabus.append(next_proj)
                else: 
                    syllabus.append("i broke!")
                    break  
            # get the view_dicts for every project in the syllabus 
            if end_project not in syllabus:
                syllabus.append(end_project)
            project_objs = [Project.objects.get(id=i['p_id']) for i in syllabus]  
            projects = [Project.preview_dict(i) for i in project_objs]    
                                       
        else:
            print(syllabus_form.errors)
    else:
        syllabus_form = SyllabusForm()

    return render(request, 'making/create_syllabus.html', context = {'user_profile':user_profile_obj, 'syllabus_form': syllabus_form, 'end_project':end_project, 'user_profile_dict':user_profile, 'syllabus': syllabus,'projects':projects})

# target = 1 tool, userTools = list of tools
# returns true if userTools has target tool, and its skill level is greater than or equal to the targets
def tool_geq(target, userTools):
    # will either return false, or a dictionary
    has_tool = next((i for i in userTools if i['name']==target['name']), False)
    return has_tool and (target['skill_level'] <= has_tool['skill_level'])

# checks that target tool exists in userTools and has equal skill level
def tool_eq(target, userTools):
    # will either return false, or a dictionary
    has_tool = next((i for i in userTools if i['name']==target['name']), False)
    return has_tool and (target['skill_level'] == has_tool['skill_level'])

def tool_leq(target, userTools):
    # will either return false, or a dictionary
    has_tool = next((i for i in userTools if i['name']==target['name']), False)
    return has_tool and (target['skill_level'] >= has_tool['skill_level'])

# returns true if all user skills are <= targets, AND all target tools return true from tool_eq()  
def req_eq(endProj, usrProf):
    skills = (endProj['vision'] <= usrProf['vision']) and (endProj['dexterity'] <= usrProf['dexterity']) and (endProj['language'] <= usrProf['language']) and (endProj['memory'] <= usrProf['memory'])
    return skills and (all(tool_geq(j, usrProf['tools']) for j in endProj['tools'] ))

# this one returns an array of skills that need to be improved
# returns empty list if theres no skills :)
def imp(endProj, usrProf):
    arr = []
    skills = ['vision', 'dexterity', 'language', 'memory']
    for i in endProj:
        if (i in skills) and (endProj[i] > usrProf[i]):
            arr.append(i)
        elif i == 'tools':
            for j in endProj[i]:
                # should probably use tool_eq (non boolean ver) here 
                has_tool = next((x for x in usrProf['tools'] if x['name']==j['name']), False)
                if (not has_tool) or (j['skill_level'] > has_tool['skill_level']):
                    arr.append(j['name'])
    return arr

def update_up(usrProf, name):
    new_up = deepcopy(usrProf) 
    skills = ['vision', 'dexterity', 'language', 'memory']
    if name in skills: 
        new_up[name] += 1 
    else: 
        has_tool = next((idx for idx, i in enumerate(new_up['tools']) if i['name'] == name), False)
        if type(has_tool) is int:
            new_up['tools'][has_tool]['skill_level'] += 1
        else:
            new_up['tools'].append({'name':name, 'skill_level':1})
    return new_up

# tries to find a project that matches the user profiles skill levels
# this wont properly work until i implement constraint relaxing 
def search(usrProf, item):
    # find all projects matching users skills
    next_proj = Project.objects.filter(requirements__vision = usrProf['vision'], requirements__dexterity = usrProf['dexterity'], requirements__language = usrProf['language'], requirements__memory = usrProf['memory']) 

    # make list of users tool names, and a dict mapping tool names to skill values 
    user_tools = []
    user_dict = {}
    for tool in usrProf['tools']:
        user_tools.append(tool['name'])
        user_dict[tool['name']] = tool['skill_level']
        
    # for each potential project    
    # NEED TO COVER CASE THAT THE PROJECT HAS NO TOOLS 
    for i in next_proj:
        # turn project into dict
        proj_dict = Project.syl_dict(i)
        # get a queryset of the projects tools
        tools = Tool.objects.filter(requirements = i.requirements)
        # IF THE PROJECT HAS TOOLS
        if tools:    
            if item in skills:            
                tools_check = tools.exclude(name__in=user_tools)
                if not tools_check:
                    tool_list = [Tool.syl_dict(tool) for tool in tools]
                    # i dont think this does what i want it to do
                    # the tool levels need to be EQUAL, not just suitable 
                    tooly = all(tool_eq(j,usrProf['tools']) for j in tool_list )
                    if tooly:
                        #proj_dict['tools'] = tool_list
                        return proj_dict
            else: 
                tools_check = tools.exclude(name__in=user_tools)
                if not tools_check:
                    tool_list = [Tool.syl_dict(tool) for tool in tools]
                    # i dont think this does what i want it to do
                    # the tool levels need to be EQUAL, not just suitable 
                    # all existing tools in project are equal to user
                    tooly = all(tool_eq(j,usrProf['tools']) for j in tool_list )
                    # need to check that specified tool exists and is at right level
                    i_tool = next((t for t in tool_list if t['name']==item), False)
                    # get users tools skill level 
                    u_tool = next((s for s in usrProf['tools'] if s['name']==item), False)
              

                    if tooly and i_tool and (i_tool['skill_level'] == u_tool['skill_level']):
                       # proj_dict['tools'] = tool_list
                        return proj_dict

        # IF PROJECT DOESNT HAVE ANY TOOLS
        else: 
            # if you arent looking to improve a skill, thats fine
            if item in skills:
                return proj_dict

def find_project(usrProf, arr):
    for i in arr:
        new_prof = update_up(usrProf, i)
        next_proj = search(new_prof, i)
        if next_proj:
            return (new_prof, next_proj)
    # if it gets this far without returning, that means there's no suitable projects?
    for i in arr:
        new_prof = update_up(usrProf, i)
        next_proj = rel_search(new_prof, i)
        if next_proj:
            return (new_prof, next_proj)
    # if it gets this far without returning anything, relax those constraints babey!
    # ie allow projects that are equal to or lesser than user profile (apart from that one skill you are trying to improve???)
    # NEED to have it so its apart from the one skill you are improving, so that you can level up your profile correctly
    # search takes in i (a string)
    # checks if i is a skill (or otherwise its a tool name)
    # try and make a query filter
    # if its a skill:

def rel_search(usrProf, item):
    skills = ['vision', 'dexterity', 'language', 'memory']
    # find all projects matching users skills
    filter_dict = {}
    for j in skills:
        if j == item:
            filter = 'requirements__' + j 
            value = usrProf[j]
            filter_dict[filter] = value
        else: 
            filter = 'requirements__' + j + '__lte'
            value = usrProf[j]
            filter_dict[filter] = value

    next_projs = Project.objects.filter(**filter_dict)

    # make list of users tool names, and a dict mapping tool names to skill values 
    user_tools = []
    user_dict = {}
    for tool in usrProf['tools']:
        user_tools.append(tool['name'])
        user_dict[tool['name']] = tool['skill_level']
        
    # for each potential project    
    # NEED TO COVER CASE THAT THE PROJECT HAS NO TOOLS 
    # could probably turn this into a fancy query like with kwargs above 
    for i in next_projs:
        # turn project into a dict
        proj_dict = Project.syl_dict(i)
        # get the projects tools
        tools = Tool.objects.filter(requirements = i.requirements)

        # if "item" is a tool name, the proj HAS to have tools, otherwise its fine
        if item not in skills: 
             # check that toolz[i][skill_lvl] == up[i][skill_lvl]
            # check that the rest of the tools are gte
            
            # IF THE PROJECT HAS TOOLS
            if tools:    
                # see if the project has any tools that the user doesnt have            
                tools_check = tools.exclude(name__in=user_tools)
                # this doesnt mean it HAS the tool we are looking for though........
                # if it doesnt, check they are a suitable skill level
                
                if not tools_check:
                    tool_list = [Tool.syl_dict(tool) for tool in tools]
                    i_tool = next((t for t in tool_list if t['name']==item), False)
                    u_tool = next((s for s in usrProf['tools'] if s['name']==item), False)

                    tooly = all(tool_geq(j,usrProf['tools']) for j in tool_list )
                    if tooly and i_tool and (i_tool['skill_level'] == u_tool['skill_level']):
                       # proj_dict['tools'] = tool_list
                        return proj_dict
        else: 
            if tools:    
                # see if the project has any tools that the user doesnt have            
                tools_check = tools.exclude(name__in=user_tools)
                # if it doesnt, check they are a suitable skill level
                if not tools_check:
                    tool_list = [Tool.syl_dict(tool) for tool in tools]
                    tooly = all(tool_geq(j,usrProf['tools']) for j in tool_list )
                    if tooly:
                       # proj_dict['tools'] = tool_list
                        return proj_dict
        # IF PROJECT DOESNT HAVE ANY TOOLS
            else: return proj_dict

skills = ['vision', 'dexterity', 'language', 'memory']

def test_page(request):
    user_profile = getProfile(request)
    ToolFormSet = formset_factory(ToolForm, extra=0, max_num=6, formset=BaseToolFormSet)
    errors = []
    if request.method == 'POST': 
        toolFormSet = ToolFormSet(request.POST) 
        if toolFormSet.is_valid():
            for form in toolFormSet: 
                tool = form.save(commit=False)
                tool.requirements = user_profile.requirements
                try:
                    tool.full_clean()
                    tool.save()
                except ValidationError as e: 
                    errors.append(e)
        else:
            errors.append(toolFormSet.errors)
    else: 
        toolFormSet = ToolFormSet()

    return render(request, 'making/test.html', context = {'projects':projects,'toolFormSet':toolFormSet,'errors':errors })