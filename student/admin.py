from django.contrib import admin

from .models import (
    Students,
    Parents,
)

# Register your models here.

class StudentsAdmin(admin.ModelAdmin):
    list_display = ["id","first_name", "last_name", "student_id","slug", "joining_date"]
    
class ParentsAdmin(admin.ModelAdmin):
    list_display = ["id", "father_name", "father_email", "mother_name", "mother_email"]
    
admin.site.register(Students, StudentsAdmin)
admin.site.register(Parents,ParentsAdmin)