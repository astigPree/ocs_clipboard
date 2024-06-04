from django.urls import path
from . import views

urlpatterns = [
    path('' , view=views.clipboard_list_page , name="home" ),
    path('writes/', view=views.write_notes , name="write"),
    path('suggestions/', view=views.suggestion_page, name="suggestion"),
    path('sticky notes/', view=views.sticky_notes_view, name='sticky_notes_view')
]
