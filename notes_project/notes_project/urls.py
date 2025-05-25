from django.contrib import admin
from django.urls import include,path
urlpatterns = [
    path('user_notes/',include("user_notes.urls")),
    path('admin/', admin.site.urls),
]
