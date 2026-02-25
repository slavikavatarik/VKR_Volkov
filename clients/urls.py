from django import views
from django.urls import path
from . import views

urlpatterns = [    
    path('profile', views.profile, name="profile"), 
    path('show_info/<a_id>', views.show_info, name="show_info"),    
    path('reports', views.reports, name="reports"),
    path('about/', views.about, name="about"),
    path('my_projects/', views.my_projects, name="my_projects"),
    path('show_user_tasks/<p_id>', views.show_user_tasks, name="show_user_tasks"),
    path('show_project_tasks/<p_id>', views.show_project_tasks, name="show_project_tasks"),
    path('add_user_task/<p_id>', views.add_user_task, name="add_user_task"),
    path('edit_user_task/<t_id>/<p_id>', views.edit_user_task, name="edit_user_task"),
    path('del_user_task/<t_id>', views.del_user_task, name='del_user_task'),
    path('edit_task_status/<t_id>/<p_id>', views.edit_task_status, name="edit_task_status"),
    path('show_chat', views.show_chat, name="show_chat"), 
    path('open_contacts/<g_id>', views.open_contacts, name="open_contacts"),
    path('open_chat/<s_id>', views.open_chat, name="open_chat"), 
]