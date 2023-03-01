from django.shortcuts import render, redirect
from making.forms import RequirementsForm, ToolForm, UserForm, ProfileForm, SyllabusForm
from making.models import Requirements, Tool, UserProfile, Project
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from copy import deepcopy
from django.db.models import Q, F

def index(request):
    if request.user.is_authenticated:
        # need to change this to filter when default profile is implemented
        user_profile = UserProfile.objects.get(user=request.user)
    else:
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
# todo: make a function that compares two requirements
# todo: make a function that updates tool level
# todo: make a function that checks if a user has a specified tool
# todo: make a function that grabs a project and all its related fields   
def create_syllabus(request):
    if request.method == 'POST':
        syllabus_form = SyllabusForm(request.POST)
        if syllabus_form.is_valid():
            # just using this as testing to see what original profile values are
            og_profile = UserProfile.objects.filter(user=request.user)[0]
            og_profile = UserProfile.syl_dict(og_profile)
            og_tools = Tool.objects.filter(requirements=og_profile['requirements_id'])
            og_profile['tools'] = [Tool.syl_dict(tool) for tool in og_tools]

            user_profile = UserProfile.objects.filter(user=request.user)[0]
            user_profile = UserProfile.syl_dict(user_profile)
            up_tools = Tool.objects.filter(requirements=user_profile['requirements_id'])
            user_profile['tools'] = [Tool.syl_dict(tool) for tool in up_tools]

            end_proj_id = syllabus_form.cleaned_data['end_project']
            end_project = Project.objects.get(id=end_proj_id)
            end_project = Project.syl_dict(end_project)
            proj_tools = Tool.objects.filter(requirements=end_project['requirements_id'])
            end_project['tools'] = [Tool.syl_dict(tool) for tool in proj_tools]
            
            og_test_req = {'vision': 1, 'dexterity': 1, 'language': 1, 'memory': 1, 'tools': [{'name': '3d printer', 'skill_level': 1}]}
            test_req = {'vision': 1, 'dexterity': 1, 'language': 1, 'memory': 1, 'tools': [{'name': '3d printer', 'skill_level': 1}]}
            test_2_req = {'vision': 2, 'dexterity': 2, 'language': 2, 'memory': 2, 'tools': [{'name': '3d printer', 'skill_level': 2},{'name': 'circuits', 'skill_level': 1} ]}


            syllabus = []
            all_prof = []
            all_arr = []

            all_prof.append(user_profile)
            while not req_eq(end_project, user_profile):
                arr = imp(end_project, user_profile)
                all_arr.append(arr)
                # im getting weird debugging cos im running this function twice lol 
                if find_project(user_profile, arr):
                    new_req, next_proj = find_project(user_profile, arr)
                    user_profile = deepcopy(new_req)

                    all_prof.append(user_profile)
                    syllabus.append(next_proj)
                else: 
                    syllabus.append("i broke!")
                    break
                    # either have to break after getting 1 project or this runs forever :)
                    # i think its an issue with the dictionaries not/being overwritten correctly
                    # make a debug trace of their values at all points. good luck. 
                   
                #test = "it is not equal"           
        else:
            print(syllabus_form.errors)
    else:
        syllabus_form = SyllabusForm()
        end_project = None
        user_profile = None
        og_profile = None
        next_tool = None
        next_proj = None
        syllabus = None
        test = None
        all_prof = None
        test_req = None 

        all_arr = None 

        og_test_req = None
        test_2_req = None


    return render(request, 'making/create_syllabus.html', context = {'syllabus_form': syllabus_form, 'end_project':end_project, 'user_profile':user_profile, 'syllabus': syllabus, 'og_profile': og_profile, 'all_prof': all_prof, 'all_arr': all_arr})

# target = 1 tool, userTools = list of tools
# i think this works
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
# i think this also works
def req_eq(endProj, usrProf):
    skills = (endProj['vision'] <= usrProf['vision']) and (endProj['dexterity'] <= usrProf['dexterity']) and (endProj['language'] <= usrProf['language']) and (endProj['memory'] <= usrProf['memory'])
    return skills and (all(tool_geq(j, usrProf['tools']) for j in endProj['tools'] ))

# this one returns an array of skills that need to be improved
# returns empty list if theres no skills :)
# seems to work
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

# i dont trust this one
# but it SEEMS to work
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
                        proj_dict['tools'] = tool_list
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
                        proj_dict['tools'] = tool_list
                        return proj_dict

        # IF PROJECT DOESNT HAVE ANY TOOLS
        else: 
            # if you arent looking to improve a skill, thats fine
            if item in skills:
                return proj_dict

def find_project(usrProf, arr):
    for i in arr:
        print("normal search looking for "+i)
        new_prof = update_up(usrProf, i)

        next_proj = search(new_prof, i)
        if next_proj:
            print("normal search FOUND "+ i)

            return (new_prof, next_proj)
    # if it gets this far without returning, that means there's no suitable projects?
    print("HELLO CAN U HEAR ME")
    for i in arr:
        print("REL search looking for "+i)
        new_prof = update_up(usrProf, i)
        next_proj = rel_search(new_prof, i)
        if next_proj:
            print("REL search FOUND "+i)
            return (new_prof, next_proj)
    # if it gets this far without returning anything, relax those constraints babey!
    # ie allow projects that are equal to or lesser than user profile (apart from that one skill you are trying to improve???)
    # NEED to have it so its apart from the one skill you are improving, so that you can level up your profile correctly
    # search takes in i (a string)
    # checks if i is a skill (or otherwise its a tool name)
    # try and make a fucked up query filter
    # if its a skill:
    # 

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
                        proj_dict['tools'] = tool_list
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
                        proj_dict['tools'] = tool_list
                        return proj_dict
        # IF PROJECT DOESNT HAVE ANY TOOLS
            else: return proj_dict

skills = ['vision', 'dexterity', 'language', 'memory']
def test_page(request):

    syllabus_form = SyllabusForm()

    test_req = {'vision': 1, 'dexterity': 1, 'language': 1, 'memory': 1, 'tools': [{'name': '3d printer', 'skill_level': 1}]}
    test_2_req = {'vision': 2, 'dexterity': 2, 'language': 2, 'memory': 2, 'tools': [{'name': '3d printer', 'skill_level': 2},{'name': 'circuits', 'skill_level': 1} ]}
    test_3_req = {'vision': 1, 'dexterity': 2, 'language': 1, 'memory': 1, 'tools':[]}
    all_arr = []
    syllabus = []
    all_prof = []

    all_prof.append(test_req)
    # this line doesnt overwrite test_req
    array = imp(test_2_req, test_req)
    all_arr.append(array)

    test_prof, test_proj = find_project(test_req, array)
    syllabus.append(test_proj)
    all_prof.append(test_prof)

    array = imp(test_2_req, test_prof)
    all_arr.append(array)

    test_prof, test_proj = find_project(test_prof, array)
    syllabus.append(test_proj)
    all_prof.append(test_prof)

    cir_test = {'vision': 1, 'dexterity': 1, 'language': 1, 'memory': 1, 'tools': []}
    girl = find_project(cir_test, ['circuits'])



    return render(request, 'making/create_syllabus.html', context = {'syllabus_form':syllabus_form, 'og_profile':test_req, 'all_prof':all_prof, 'all_arr': girl, 'syllabus': syllabus, })