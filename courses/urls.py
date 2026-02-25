from django import views
from django.urls import path
from . import views

urlpatterns = [     
    path('', views.home, name="home"),    
    path('courses/', views.courses, name="courses"),   
    path('show_themes/<c_id>', views.show_themes, name="show_themes") ,
    path('show_lections/<t_id>', views.show_lections, name="show_lections"),
    path('open_lection/<l_id>', views.open_lection, name="open_lection"),
]