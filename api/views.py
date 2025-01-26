from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from student.models import (
    Students,

)
from api.serializers.serializers import (
    StudentSerializer
)

# Create your views here.
@swagger_auto_schema(
    name = "Get student list",
    operation_description = "Get student list",
    method = "get",
    manual_parameters = [
        openapi.Parameter(
            name = "id",
            in_ = openapi.IN_QUERY,
            type = openapi.TYPE_STRING,
            required = False,
            description = "Enter your id",
        ),
    ]
)
@api_view(['GET'])
def student_list(request):
    id = request.query_params.get("id")
    query = Q()
    if id:
        query &= Q(id=id)
        queryset = Students.objects.filter(query)
        if queryset.exists():
            queryset = queryset.values(
                "id",
                "first_name",
                "last_name",
            )
            return Response(data = list(queryset), status= status.HTTP_201_CREATED)
    else:
            queryset = Students.objects.values(
                "id",
                "first_name",
                "last_name",
                "student_id",
                "gender",
                "date_of_birth",
                "Student_class",
                "religion",
                "slug",
                "address",
                "section",
            )
            # serializer = StudentSerializer(obj, many=True)
            return Response(data=list(queryset), status= status.HTTP_201_CREATED )
    return Response({"err": "no data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def post_student(request):
    serializer = StudentSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "msg": "Student data posted successfully", 
            "student": serializer.data
            }, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    name = "Get student id",
    operation_description = "Get student id",
    method = "put",
    manual_parameters = [
        openapi.Parameter(
            name = "id",
            in_ = openapi.IN_QUERY,
            type = openapi.TYPE_STRING,
            required = False,
            description = "Enter your id",
        ),
    ]
)
@api_view(["PUT"])
def student_update(request, pk=None):
    id = request.query_params.get("id")
    try:
        insatnce = Students.objects.get(id=id)
        serializer = StudentSerializer(insatnce, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": " Student data is updated sucessfully",
                "student":serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
         return Response({"msg": "error", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["DELETE"])
def delete_student(request):
    id = request.data.get("id")
    if id is None:
        return Response({"msg": "Student id Required"})
    
    try:
        student = Students.objects.get(id=id)
        student.delete()
        print(student)
        return Response(f"msg: {student} deleted sucessfully", status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"msg": "student not found"}, status=status.HTTP_400_BAD_REQUEST)
    