# todo: fancy way of turning model instance into dict
# todo: make a function that compares two requirements
# todo: make a function that updates tool level
# todo: make a function that checks if a user has a specified tool
# todo: make a function that grabs a project and all its related fields   
def create_syllabus(request):
    # horrible helper functions i should move 
    def tools_eq(endTools, userTools): 
        check = False
        for i in endTools:
            girl = next((item for item in userTools if item['name'] == i['name']), False)
            if girl and (i['skill_level']<=girl['skill_level']):
                check = True
            else: 
                check = False 
        return check

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

            next_tool = None
            next_proj = None
            syllabus = []
            while not tools_eq(end_project['tools'], user_profile['tools']):
                for tool in end_project['tools']:
                    # does the UP have this tool
                    exists = next((item for item in user_profile['tools'] if item['name'] == tool['name']), False)
                    index = next((i for i, item in enumerate(user_profile['tools']) if item['name'] == tool['name']), False)
                    if exists: 
                        # does the user have needed skill level in that tool 
                        if exists['skill_level'] < tool['skill_level']:
                                # need to include a check if a project actually exists
                                # need to have all other things in the project be do-able too !!!!
                                # oh god this is going to search through profile tool objects too 
                                # i need to be filtering through PROJECT objects 
                                next_tool = Tool.objects.filter(name=tool['name'], skill_level=exists['skill_level']+1)[0]
                                next_proj = Project.objects.filter(requirements=next_tool.requirements)[0]
                                next_proj = Project.syl_dict(next_proj)
                                next_tools = Tool.objects.filter(requirements=next_proj['requirements_id'])
                                next_proj['tools'] = [Tool.syl_dict(tool) for tool in next_tools]
                                syllabus.append(next_proj)
                                # increment usr profile here
                                user_profile['tools'][index]['skill_level'] += 1
                    else: 
                        next_tool = Tool.objects.filter(name=tool['name'], skill_level=1)[0]
                        next_proj = Project.objects.filter(requirements=next_tool.requirements)[0]
                        next_proj = Project.syl_dict(next_proj)
                        next_tools = Tool.objects.filter(requirements=next_proj['requirements_id'])
                        next_proj['tools'] = [Tool.syl_dict(tool) for tool in next_tools]
                        syllabus.append(next_proj)
                        user_profile['tools'].append({'name':tool['name'], 'skill_level':1})

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

    return render(request, 'making/create_syllabus.html', context = {'syllabus_form': syllabus_form, 'end_project':end_project, 'user_profile':user_profile, 'next_proj': next_proj, 'syllabus': syllabus, 'og_profile': og_profile})


{% extends 'making/index.html' %}
{% block body_block %}
<br>
<form method="post" action="{% url 'making:create_syllabus' %}">
    {% csrf_token %}
    {{ syllabus_form }}
    <input type="submit" name="submit" value="Submit" /> 
</form>
User's original profile: {{ og_profile }} <br>
User's end profile: {{ user_profile }} <br>
End project: {{ end_project }} <br>
Next project: {{ next_proj }} <br>
Syllabus: <br>
{% for i in syllabus %}
    {{ i }} <br>
{% endfor %}
{% endblock %}