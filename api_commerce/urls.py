from django.urls import path

from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('view_note', views.view_note, name="view_note"),
    path('<slug>', views.specified_note, name="specified_note"),
    path('<slug>/update', views.specified_note_edit, name="update"),
    path('<slug>/delete', views.specified_note_delete, name="delete"),
    path('create/', views.specified_note_create, name="create")
]