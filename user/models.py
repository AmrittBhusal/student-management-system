from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
# from student.managers import ActiveManager
# Create your models here.


class UserProfile(models.Model):
    ROLE_CHOICE = [
        ("IsSystemAdmin", "IsSystemAdmin"),
        ("General User", "General User"),
        ("Student", "Student"),
        ("Teacher", "Teacher")
    ]
    
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Profile", null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICE, blank=True, null=True)
    gender = models.CharField(max_length=15, default="Male", choices=GENDER_CHOICES)
    email = models.CharField(max_length=100, blank=True,null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_modified = models.DateField(auto_now_add=True, blank=True, null=True)
    # active = ActiveManager()
    
    
    def __str__(self):
        return self.user.username
    
    
class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_name", null=True,blank=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.email} - {self.code}"
    
    def is_expired(self):
        # code expire after 10 min
        time =(timezone.now()-self.created_at).total_seconds() > 600
        print(time, "TimeTimeTimeTimeTimeTimeTimeTimeTimeTimeTimeTime---------------------")
        return time
    