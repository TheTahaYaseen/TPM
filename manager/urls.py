from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
 
    path("projects/add", views.add_project_view, name="add_project"),
    path("project/alter/<str:project_id>", views.alter_project_view, name="alter_project"),
    path("project/delete/<str:project_id>", views.delete_project_view, name="delete_project"),
    path("projects/<str:project_id>", views.project_view, name="project"),
 
    path("states", views.states_view, name="states"),
]