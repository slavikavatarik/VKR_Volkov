from django import views
from django.urls import path
from . import views

urlpatterns = [    
    path('ttests', views.ttests, name="ttests"), 
    path('starttest/<th_id>', views.starttest, name="starttest"),
    path('show_question', views.show_question, name="show_question"),
    path('show_result', views.show_result, name="show_result"),
    path('get_courses', views.get_courses, name="get_courses"),
    path('show_test_themes/<c_id>', views.show_test_themes, name="show_test_themes"),    
]