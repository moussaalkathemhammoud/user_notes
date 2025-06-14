from django.urls import path
from .views import register,login,list_notes,add_note,delete_note

urlpatterns = [
    path("register/",register, name="register"),
    path("login/",login, name="login"),
    path("notes/list",list_notes, name="list-notes"),
    path("notes/add",add_note, name="add-note"),
    path("notes/delete/",delete_note, name="delete"),
]