from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from todo.views import *


urlpatterns = [

    path('', home,name='home'),
    path('signup/', signup_view,name='signup'),
    path('logout/',logout_view,name='logout'),
    path('login/',login_view,name='login'),
    path('add-task/',add_task,name='add-task'),
    path('completed-tasks/',completed_tasks,name='completed-tasks'),
    path('view-task/<int:todo_pk>',view_task,name='view-task'),
    path('view-task/<int:todo_pk>/update',update_task,name='update-task'),
    path('view-task/<int:todo_pk>/complete',mark_complete,name='mark-complete'),
    path('view-task/<int:todo_pk>/delete',delete_task,name='delete-task'),

    
]