from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from .models import Project, ProjectState

# Create your views here.
@login_required(login_url="login")
def home_view(request):

    all_projects = Project.objects.all()
    all_projects_count = len(all_projects) 
    states_with_count = ProjectState.objects.annotate(count_of_projects=Count("project"))[:3]

    state_filter = request.GET.get("state") if request.GET.get("state") else "" 

    if state_filter:
        projects = Project.objects.filter(
            Q(state__state__exact=state_filter)
        )
    else:
        projects = Project.objects.all()

    for project in projects:
        project.description = project.description[:225] + "...." 

    context = {"all_projects_count": all_projects_count, "states_with_count": states_with_count, "projects": projects}
    return render(request, "home.html", context)

def states_view(request):

    all_projects = Project.objects.all()
    all_projects_count = len(all_projects) 
    states_with_count = ProjectState.objects.annotate(count_of_projects=Count("project"))[:5]

    context = {"all_projects_count": all_projects_count, "states_with_count": states_with_count}
    return render(request, "states.html", context)

@login_required(login_url="login")
def project_view(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.user != project.created_by:
        return redirect("home")
    context = {"project": project}
    return render(request, "project.html", context)

def register_view(request):
    form_action = "Register"
    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == None and password == None:
            error = "You Can Leave Neither Username Or Password Empty!"
        elif len(password) < 8:
            error = "Your Password Must Atleast Be 8 Characters Long!"
        else:
            try:
                user = User.objects.get(username = username)
                error = "User With Username Alrady Exists!"
            except User.DoesNotExist:
                user = User.objects.create(
                    username=username,
                    password=password
                )
                login(request, user)
                return redirect("home")

    context = {"form_action": form_action, "error": error}
    return render(request, "auth_form.html", context)

def login_view(request):
    form_action = "Login"
    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == None and password == None:
            error = "You Can Leave Neither Username Or Password Empty!"
        else:
            try:
                user = User.objects.get(username=username, password=password)
                login(request, user)
                return redirect("home")
            except User.DoesNotExist:
                error = "An Error Occured During Login! Maybe Invalid Credentials!"            

            try:
                user = User.objects.get(username = username)
            except User.DoesNotExist:
                error = "User With Username Does Not Exist!"

    context = {"form_action": form_action, "error": error}
    return render(request, "auth_form.html", context)

@login_required(login_url="login")
def add_project_view(request):
    form_action = "Add Project" 
    error = ""

    if request.method == "POST":
        name = request.POST.get("name")
        abbreviation = request.POST.get("abbreviation")
        description = request.POST.get("description")
        purpose = request.POST.get("purpose")
        state = request.POST.get("state")
        pseudocode = request.POST.get("pseudocode")

        fields = [name, abbreviation, description, purpose, state, pseudocode]
        if None in fields:
            error = "Please Do Not Leave Any Field Empty!"
        else:
            project_state, created = ProjectState.objects.get_or_create(state=state, created_by=request.user)    
            Project.objects.create(
                name = name,
                abbreviation = abbreviation,
                description = description,
                purpose = purpose,
                state = project_state,
                pseudocode = pseudocode,
                created_by=request.user
            )
            return redirect("home")

    context = {"form_action": form_action, "error": error}
    return render(request, "project_form.html", context)

@login_required(login_url="login")
def alter_project_view(request, project_id):

    project = Project.objects.get(id=project_id)
    form_action = "Alter Project"

    error = ""

    if request.user != project.created_by:
        return redirect("home")

    name = project.name
    abbreviation = project.abbreviation
    description = project.description
    purpose = project.purpose
    state = project.state.state
    pseudocode = project.pseudocode

    if request.method == "POST":
        name = request.POST.get("name")
        abbreviation = request.POST.get("abbreviation")
        description = request.POST.get("description")
        purpose = request.POST.get("purpose")
        state = request.POST.get("state")
        pseudocode = request.POST.get("pseudocode")

        fields = [name, abbreviation, description, purpose, state, pseudocode]
        if None in fields:
            error = "Please Do Not Leave Any Field Empty!"
        else:
            project_state, created = ProjectState.objects.get_or_create(state=state, created_by=request.user)    
            project.name = name 
            project.abbreviation = abbreviation 
            project.description = description 
            project.purpose = purpose 
            project.state = project_state 
            project.pseudocode = pseudocode 

            project.save()

            return redirect("home")
    
    context = {"form_action": form_action, "error": error,
               "name": name, "abbreviation": abbreviation, "description": description, "purpose": purpose, "state": state, "pseudocode": pseudocode}
    return render(request, "project_form.html", context)

@login_required(login_url="login")
def delete_project_view(request, project_id):

    project = Project.objects.get(id=project_id)

    if request.user != project.created_by:
        return redirect("home")

    item_category = "Project"
    item = project.name

    if request.method == "POST":
        project.delete()
        return redirect("home")
    
    context = {"item_category": item_category, "item": item}
    return render(request, "delete.html", context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("home")