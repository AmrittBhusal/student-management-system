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