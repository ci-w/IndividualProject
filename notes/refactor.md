# All notes from Sem 2 refactor process 
## Notes
* User profile should somehow be separate from User, so that non-logged in users can still adapt projects
    * Is this viable? Or should I just have it that site access requirements are separate and work without an account?
* Idea of a User having multiple user profiles. Use case: one carer/instructor working with a group. 
* Idea of one Project having multiple potential difficulty levels 
* The granularity of different skill levels to improve may need to be adjusted, especially in relation to syllabus creation i.e. a jump from one level to the next may be too great
* Make language surrounding disability/requirements consistent and best practice
* Display difficulty of Project based on the users current profile
    * If the Project and the User Profile's requirements are equal, the difficulty is 100%
    * Have a "practice" button at the bottom of the project page to do more projects at the same level 
* Need to design it in such a way that it's easy to add new skills/tools
* Users should be able to view projects that they don't have the skills for, and the project should be adapted as much as possible. Project page should display this information. Projects like this shouldn't be put in the syllabus. 

## Whole website 
### Notes
* At one point I was going to have User Profiles able to be stored as session variables, so non-logged in users could have greater access. Changed this so that only Site Access Requirements were separate/session variables rather than the entire User Profile.
* Have project requirements separate from site accessibility requirements? i.e. large text, colour changes, screen reader friendly. Site requirements would interact with every view. 
* A way of recording if a User Profile has completed a project, or how far through they are.
### Modules/Models
* User:
    - Can: log in, register, update User details
    - Has: username, password 

User has (none, one, or many) User Profiles.
* User Profile:
    - Has: (project) requirements, ~~(site access) requirements~~
    - Can: update details
* Project:
    - Has: ID, title, categories, requirements
    - Can:  
* Syllabus (creation):
    - Takes: User Profile, Project (the "end goal")
    - Can: combine these and output a path of projects. (need to define "combine" further)
* Website page:
    - Takes: User Profile (if any) and modifies view based on the User Profile's project + site requirements
* Project view: takes a Project and a User Profile, outputs view of Project accordingly.

### Models (refined further)
Foreign key: field that is linked to another tables primary key. Has to be exactly the same value. 
* Requirements object can only be a FK in ONE User Profile xor Project 

**User**
* Attributes:
    - Username
    - Password
    - ID
* Methods:
    - log in
    - log out
    - register
    - change details 

User -> User Profile is a One to Many relationship

**User Profile**
* Attributes:
    - User ~~(optional)~~
        - UserId as FK
        - Should you be able to change what User?
    - Project requirements (FK to Requirements object)
    - Site requirements
    - ID
    - ~~user_name~~ profile name (renamed to avoid confusion)
* Methods:
    - Update requirements

**Site requirements** (this stored as session attribute?)
* Attributes 
    - Text size
    - Colour scheme
    - Screen reader friendly 

**Project**
* Attributes:
    - ID
    - Title
    - Categories
    - Requirements (FK to Requirements object)
    - Instructions
    - Description (short)
* Methods:
    - Should you be able to create new projects?

Project -> Requirements is a One to One relationship

**Syllabus**
* Attributes:
    - List/path of projects (stored as IDs?)
    - User Profile ID (FK)
* Methods:
    - Create syllabus:
        - Requires User Profile + Project (end goal)
        - [Does something]
        - Outputs a list of projects (a syllabus). Starting with user profiles current skill level and ending with end goal project. 

**Requirements**
* Attributes:
    - Vision level (1-5)
    - Dexterity level (1-3)
    - Language level (1-3)
    - Memory level
    - Tools
    - ID 
    - ~~p or u + ID number~~ 

Requirements -> Tool is a One to Many relationship. 

**Tool**
* Attributes:
    - Tool name (might have to have this as a list of choices)
        - Have name options be list of (current) tools -> no use in adding tool proficiency if no projects have them?
    - Skill level 
    - ~~project or user ID~~
    - Requirements ID 

Need to decide what attributes can be NULL. 

--- 
### Requirements 
* Realised that project and user requirements were actually very similar structures/the same thing. 
* Language level: have different sets of instructions. Need to interact with vision/dexterity adaptation?
    * "what level of language/modularity of instructions are you comfortable with?"
    * maybe do this with an example i.e. a bit of text giving instructions with increasing difficulty
* Project vision level: vision level needed, however this should be able to be changed/adapt the project for lower vision? 
* Image instructions: Boolean toggle, show images of each instruction step.
* Project materials needed? if it requires finicky objects, could these be swapped out?

* Challenges in:
    * short term memory
    * long term memory
    * manual dexterity
    * emotional regulation + patience 
    * literacy
    * speech
    * attention
    * reasoning 
    * retention
___
### Forms
* Log in
* Register
    - Should you be able to create a User Profile at the same time as creating a User?
    - Having a User creation separate from User Profile creation
* Create user profile
    - Form for user profile model:
        - User = autofill from request.user
        - Profile name = input
        - Requirements = auto link (don't .save() this until processed next form)
    - Form for requirements model:
        - Just for each skill level etc 
    - Form for tools?
        - Need to be able to do multiple of these?
        - Automatically set requirements ID
    - How to handle not all the forms being completed (i.e. profile having no tools etc)
        - If tool form is blank, don't add any tools
* Update user profile
    - This would also update requirements + tools?
* Switch user profile
    - Just list of User Profiles associated with current User?
___
### Views
Python function that takes a web request and returns a web response. Contains whatever logic is needed for that. 
Create views last, can use django.admin for testing.
* Home/index page
* About page
* Individual Project page
* Projects page (all projects)
* User page
* User profile page 
    - At top: flag "finish creating current profile"
    - Display current UP details
    - Update current UP details (redirect? or list?)
    - Create new UP?
    - Delete current UP
    - Change which UP: either a button/link, or list of UPs and you click which one to change to. Include add new UP?
* Update user profile 
    - Update skills
    - Add tool
    - Update current tools
* Register
* Log in
___
### Syllabus
* Some skills/attributes are fixed i.e. they cannot be changed/improved. Others can. 
* Increments in steps of 1 in each skill needing to be improved? If too long, can make bigger jumps towards end. 
* Syllabus create view function:
    - Form: pastes in (end) project object, can get UP object from request
    - Main body:
        - Take a copy of UP/reqs/Tools
        - Create Difference (between UP and end project)
            - Note: surely you want to recalculate difference each time UP updates 
        - For each non null value in difference:
            - look for a project with values equal to UP and +1 in difference
            - if found, add project to syllabus and update UP_copy 
        - Go through each value in end project (maybe starting with tools?)
        - When you find a value greater than UPs, look for a project
        - When EP == UP, add EP to syllabus and finish

* For each tool in end project, either
    - the user doesn't have that tool
    - the user does have that tool and
        - it's not at the correct skill level
        - its at the correct skill level  

* Need a table_level (manager) method for Tools which returns all tools with a certain req ID/ a to_dict of them?
* Question: when to increase vis/dex/etc levels?
    - after all tools?
    - at the same time as tools? (i.e. one pass of them all together)
    - interspersed with tools? (i.e. one pass of tools, one pass of skills)
* Need to do a full filter/check that next project fits current requirements
* Is there a project with that increased level (queryset), is that project less than or equal to current UP (taking into account increased level)? If not, go to next project in query set.
* Need to do something to add the end/goal project 
* When writing greater than (model) function, "other" doesn't have to be a model instance. Just write it as if its a dictionary. 
* Function takes in: (tool name, skill level), UP
    - checks if UP has tool
    - checks if skill level is sufficient 

Another bit of paper (16/2/23):
* find a list of projects fitting the requirements, each time incrementing a skill level to finally equal the end project
* at one point I was considering creating "Difference"/"Syllabus Req" as a requirements object/structure
    - Req levels:
        If end proj level > UP level: SY level = EP - UP
        Else: SY level = 0
    - Tools: If tool is in EP and not UP: SY tool = PJ tool Else if tool is in EP and UP AND (EP tool level > UP tool level): SY tool level: EP - UP
* Then use ^ this object to create the syllabus
* You dont actually want to change the UPs levels before they complete a project though
* What to do if a project isn't found?
* For a solid hour I considered if I should do it as a constraint program before I came to my senses:
    - there exists a directed edge between two projects if: all of the tools and levels in P2 are the same as P1 (this wont work because project doesn't have to equal UP)
    - apart from one - which is currently at a lower level than the end point - being +1 level
    - find a path from UP to end project

(16/2/23) redesign:
"I think this works. Only problem is search inefficiency/path finding i.e. what if you go in the wrong direction and then there's not a path. Is this mitigated by the "easier" option?"
* While not eq_func(UP_copy, end_proj)
    - UP_copy, found = find_func(UP_copy, end_proj)
    - syllabus_list.append(found)
    - (need to have a way of including end_proj in syllabus_list)
* eq_func: function that checks if an UP contains everything in a project (i.e. UP can have other tools/higher skill levels)
* find_func: takes UP_copy, looks for a project that is 1 step towards end_proj. Returns new UP_copy and found project?
    - the order in which the checks are in is important i.e. leaving vision upgrades until other upgrades are unavailable 
    - for i in difference:
        - try and find a project with reqs/tools equal to UP but with +1 in whatever i is
        - if this doesn't work look for one with requirements less than or equal to UP, but with +1 in i (should this be done if there's no equal ones among ALL difference)
        - if a project is found, return the project + updated UP 
* difference: calculates what needs to be improved for UP to reach end_proj and by how much
* eq_+1_func: function that takes 2 projects and returns true if they are equal but +1 skill increase 

Another redesign: 
* Logic flow:
    - While EndProject > UserProfile (<-dictionary):
        - check = False, ~~do all the tools (once?)~~, ~~do all the skills (once?)~~
        - pick one thing to improve, change UserProfile, move on (do While loop again)
        - if tools not equal and check == False:
                pick a tool and improve. (this means all tools will be done before skills) (need to do it so that it switches if no projects available)
        - if skills not equal and check == False:
                pick a skill and improve 
* End project: have it as an object so can use project methods. But maybe this is inefficient? 
* add func: takes a user profile (dict) and a skill/tool name. Returns a dictionary with that incremented. 
* "pick a skill/tool and improve" few potential strategies:
    - pick first unequal one
    - pick random unequal one
    - pick unequal one with lowest current skill level
* function that returns the unequal skills?
* function: try finding project with that skill/tool. return projects that equal add func(UP). or, if add_func returns not none, process it (check = True). Otherwise, next skill. 
* do i need skill and tool behaviour separate? 
* if i was being real fancy, the "while" function check would return true if UP is one-out from end project (i.e. making it easy to add end_project to syllabus)

second bit of paper from this:
```python
while end project > user profile:
    check = False
    if tools not equal: findTool
        if findTool != None: 
            add project, update user_profile, go to while loop 
    if skills not equal: same drill ^ 
```
I rewrote this while function about 20 times.
```python
while Eq(EndProj,UsP):
    EqFunc(EndProj, UsrP) #will return list of names(skills, tools) to be improved*
    arr = []
    #at one point i had 2 separate functions for getting the names of things to be improved, one for tools and one for skills
    append list of names to arr, pass arr into another function?
    for i in arr:
        FindProject(UsP, i)
    #i moved this ^ out into its own function
```
```python
Funny(UP, arr):
    for i in arr:
        if i in [skills]:
            look for proj
            if proj, return proj
        else:
            look for proj
            if proj, return proj 
```
```python
FindProject(UP, i):
    if i in [skills]:
        look for project equal to UP + 1 in skill
        if project exists, return it and the updated UP
```
```python
next_project = Funny(UP,arr)    #Funny will return project if possible
if next_project == None:
    relax constraints, search again
else:
    append next_project to syllabus (UP is already updated?)
```

```python
FindTool(UserProfile, ??):
    #needs a list of unequal tools
    For each unequal tool:
        try to find a project
        If one is found, return it
    If no tools are found at all, return None at the end of the entire function
```
```python
FindSkill( ):
    #either needs list of unequal skills, or UserProfile+EndProject
    For each unequal skill:
        try to find a project
        if one is found, return it
    return None
```
```python
def function:
    ToolsEqual( )
    if ToolsEqual != None/False:
        FindTool
        if FindTool != None:
            process FindTool
            return 
    if SkillsEqual != None/False:
        same as above
    #If you get this far, try it with less than equals
``` 
Refined functions from this ^ 
```python
while not unEq(EndProj, UP):
    arr = imp(EP, UP)
    UP, next_proj = FindProject(UP, arr)
    if next_proj != None:
        append next_proj to syllabus
    else:
        relax search constraints 
return syllabus 
```
```python
FindProject(UP, arr):
#UP is a dictionary, arr is a list of strings from Imp()
    for i in arr:
        new_up = UpdateUp(UP, i)
        next_proj = Search(new_up)
        if next_proj != None:
                UP = new_UP #need to check dict copy behaviour 
                return(UP, next_proj)
```
```python
ReqEq(EndProj, UP):
# both inputs as dictionaries?
    EndProj['dex'] <= UP['dex'] 
    AND ...
    AND ... (for all skills)    #instead of hardcoding this, do it a different way
    AND...
     for all { tool } in EndProj:
        ToolEq( tool, UP) == True
    all(ToolEq(j, UP['tools'] is True for j in EndProj['tools']))
``` 
```python
ToolEq(target: tool dict, tools: UP['tools'] list of dicts) -> Boolean
    has_tool = next(i for i in tools if i['name']==target['name'], False)
    return (has_tool AND target['skill_level']<= has_tool['skill_level'])
```
```python
Imp(EndProj, UP): #will look like UnEq
    arr = []
    for skill in EndProj:
        if EndProj[skill]>UP[skill]:
            append skill to arr
    for tool in EndProj:
        if tool not in UP or UP[tool][skill_level] < tool[skill_level]:
            append tool to arr
    return arr #list of strings 
```
```python
Search(UP):
    database search that fits UP parameters
    return project or None
```
```python
UpdateUp(UP, item: String):
    deepcopy UP
    if item in [skills]:
        UP_copy[item] += 1
    else:
        has_tool = ..... #get index
        if has_tool:
            UP_copy[i][skill_level] += 1
        else:
            append new tool with skill level 1
    return UP_copy
```



___
### User Profile 
* Selection of UP at login: if User has more than 1 UP, ask them to select which one (and include option to create a new one?). This would remove need for default UP. But what if they have no UP?
* Write fancier UP system but for now do:
    - Register -> log in -> create UP (all req) -> add tools page
    - Log in -> select profile or create new 
* I think I was flirting with the idea of users being able to partially create a User Profile (i.e. the process of creating a UP was too much to be done in one go), saving after each step. However 1.) is the UP actually too much and 2.) this made it all very complicated (i.e. how to handle UP's accessing pages when its not complete) (if a user hasn't completed their UP, are they really going to be trying to access the site?)
* Should a user with no UP be able to access the site? yes?
* However if a user does have UP, do they have to select one to access the site? No?

My 6 million redesigns of this:

* Create user -> 
* automatically logged in -> 
* "select UP" page, if User has no UP, show "create UP button"

* Create UP:
    - Enter profile name + submit 
    - Creates UP with blank reqs?
    - Takes you through each req form? (if UP.vis == NULL, show vis form etc)
    - Saves response, puts you through to the next one 

Another design
* Create user
    - Potentially ability to create profile at the same time? 
    - However, if this was enforced: it would be based on the assumption that its the intended user creating the account i.e. not an instructor. So I think it'd be better to not do this. 
* Automatically logged in
* Potentially redirect to "create profile" page 
* If user doesn't have a UP, display "create UP" button/pop up prominently? 
* Create UP:
    - Form for UP: profile name (required) 
    - Potentially allow for the rest of the form(s) to be blank? i.e. is the form too much to be completed in one go?
        - And if things are left blank, how to process that in the model?
    - Maybe have separate views(?) for each requirement, which can be saved/recorded after each one? 
    - But then how is that different than update UP?
        - So, this part is actually "update profile" but "create profile" would direct you there (after instantiating an empty req object?)

Third times the charm
* Create UP ->
* Enter profile name ->
* Creates UP with name and related req object with all other fields == NULL
    * Would need to have all pages/views that use UP make checks that req fields aren't NULL
* Or, keep throwing you through this loop until all req fields are done?
* Have a separate view/form for each req. Once one isn't NULL, display the next one.
* Save and record after each one
* Then redirect to 'add tools' page 
* If its done this way, would have to have create/update UP be separate, because new users will want to go through it step by step, but normal updates will want to go change a section 
* Should you be able to create a new UP if (current) one isn't finished? Logically yes. Probably should show 'finish user profile' on create new UP blurb. OR have a 'create new UP' button in the UP process. 
