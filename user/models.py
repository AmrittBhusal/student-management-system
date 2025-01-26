from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.


class UserProfile(models.Model):
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
    role = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=15, default="Male", choices=GENDER_CHOICES)
    email = models.CharField(max_length=100, blank=True,null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_modified = models.DateField(auto_now_add=True, blank=True, null=True)
    