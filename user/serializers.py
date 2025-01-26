from rest_framework import serializers

from user.models import (
    UserProfile,
    User,
)

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "username", "password"]

class UserProfileSerializers(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    
        
        
    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_is_active(self, obj):
        status = obj.user.is_active
        return status

    def get_username(self, obj):
        username = obj.user.username
        return username

    def get_group(self, obj):
        if obj.user:
            group = obj.user.groups.all()
            return group.first().id if group else None
        else:
            return None

    def get_group_name(self, obj):
        if obj.user:
            group = obj.user.groups.all()
            return group.first().name if group else None
        else:
            return None