from django.contrib import admin
from django.urls import path, include
from api.views import student_list

urlpatterns = [
    path("student-list/", student_list, name="get-student-list")
]