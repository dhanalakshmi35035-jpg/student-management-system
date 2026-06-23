from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('<int:question_id>/', views.detail, name='detail'),
path('<int:question_id>/results/', views.results, name='results'),
path('<int:question_id>/vote/', views.vote, name='vote'),
    path('about/', views.about, name='about'),
    path('students/', views.student_list, name='student_list'),

    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('add_student/', views.add_student, name='add_student'),
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    path('add_marks/', views.add_marks, name='add_marks'),
path('marks_list/', views.marks_list, name='marks_list'),
path('add_fee/', views.add_fee, name='add_fee'),
path('fee_list/', views.fee_list, name='fee_list'),
path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
path('student_pdf/<int:id>/', views.student_pdf, name='student_pdf'),
]
