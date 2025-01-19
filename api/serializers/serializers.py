from rest_framework import serializers
from student.models import (
    Students,
    Parents
)

class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Students
        fields = "__all__"
        
class ParentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Parents
        fields = "__all__"