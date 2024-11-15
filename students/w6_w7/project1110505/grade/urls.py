from django.urls import path
from . import views

urlpatterns = [    
    path('', views.grade_hello, name='grade_hello'),    
    path('student/', views.student, name='student_v2'),     
    path('student_course/', views.student_course, name='student_v2_course'), 
    path('student/new', views.student_new, name='student_v2_new'),   
    path('student/delete/<int:record_id>/', views.student_delete, name='student_v2_delete'),
    path('student/update/<int:record_id>/', views.student_update, name='student_v2_update'),
]