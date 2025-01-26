from django.contrib import admin
from django.urls import path, include
from api.views import (
    student_list,
    post_student,
    student_update,
    delete_student ,
    
)

urlpatterns = [
    path("student-list/", student_list, name="get-student-list"),
    path("post-student/", post_student, name = "post-student-data"),
    path("student-update/", student_update, name="student-update"),
    path("student-delete", delete_student, name = "delete-student")
]