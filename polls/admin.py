from django.contrib import admin
from .models import Question, Choice, Student, Attendance, Mark, Fee

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Mark)
admin.site.register(Fee)