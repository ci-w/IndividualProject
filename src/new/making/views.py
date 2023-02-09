from django.shortcuts import render, redirect
from making.forms import RequirementsForm, ToolForm, UserForm
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
    pass 

def project(request):
    pass

def projects(request):
    pass

def register(request):
# tells the template if registration was successful 
    registered = False 
    passwordy = "none"
    # if its a HTTP post, we want to process form data
    if request.method == 'POST':
        # try to get info from the raw form info 
        user_form = UserForm(request.POST)
        passwordy = user_form['password'].value()
        # if the forms are valid
        if user_form.is_valid(): 
            # save users form data to the db 
            user = user_form.save() 
            # hash password, update user object
            user.set_password(user.password)
            user.save() 

            registered = True
        else: 
            print(user_form.errors)
    else: 
        # not a http POST, so render form using 2 modelForm instances - blank ready for user input
        form = UserForm()

    # render template depending on context 
    return render(request, 'making/register.html', context = {'form': form, 'registered': registered, 'password': passwordy})



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

def profile(request):
    pass