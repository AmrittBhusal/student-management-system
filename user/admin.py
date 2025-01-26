from django.contrib import admin
from user.models import (
    UserProfile,
)

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "middle_name", "last_name", "full_name", "username", "role","email"]
    
    
    
admin.site.register(UserProfile,UserProfileAdmin)