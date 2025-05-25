from django.urls import path
from .views import RegisterView, ListAddNotesView, DeleteNoteView,LoginView

urlpatterns = [
    path("register/",RegisterView.as_view(), name="register"),
    path("login/",LoginView.as_view(), name="login"),
    path("notes/",ListAddNotesView.as_view(), name="list-add-notes"),

    path("notes/<int:note_id>",DeleteNoteView.as_view(), name="delete"),
]