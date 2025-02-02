from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from user.models import UserProfile

class IsGeneralUser(BasePermission):
    message = "you must be a general user"
    def has_permission(self,request,view):
        if request.user and request.user.is_authenticated:
            try:
                userprofile = UserProfile.objects.get(user=request.user)
                return userprofile.role == "General User"
            except UserProfile.DoesNotExist:
                raise ObjectDoesNotExist("Unaunthenticate User")
        return False  
    
    
class IsSystemAdmin(BasePermission):
    message = "you must be a system admin"
    def has_permission(self,request,view):
        if request.user and request.user.is_authenticated:
            try:
                userprofile = UserProfile.Objects.get(user = request.user)
                return userprofile.role == "IsSystemAdmin"
            except UserProfile.DoesNotExist:
                raise ObjectDoesNotExist("Unauthenticated User")
        return False
                