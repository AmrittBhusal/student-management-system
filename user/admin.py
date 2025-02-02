from django.contrib import admin
from user.models import (
    UserProfile,
    PasswordResetCode,
)

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["id","user", "first_name", "middle_name", "last_name", "full_name", "username", "role","email"]
    
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display =["id","user", "code", "is_used","created_at"]
    
    
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(PasswordResetCode,PasswordResetCodeAdmin)