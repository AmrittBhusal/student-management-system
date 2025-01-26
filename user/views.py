from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status  
from django.db.models import Q 
from rest_framework.authtoken.models import Token
# from django.contrib.auth  import get_user_model
# from django.utils.encoding import force_str
# from django.utils.http import urlsafe_base64_decode
# from .utils import account_activation_token
# from django.http import HttpResponse
from user.models import (
    User,
    UserProfile,
)
from user.serializers import (
    UserProfileSerializers,
    UserSerializer
)

def home(request):
    pass
# Create your views here.

class UserRegistration(GenericViewSet, CreateModelMixin):
    serializer_class = UserSerializer
    
    def create(self,request):
        if UserProfile.objects.filter(user__email=request.data.get("email")).exists():
            return Response({"msg": "email is already exists"}, status = 400)
        if UserProfile.objects.filter(user__username=request.data.get("usrname")).exists():
            return Response({"msg": "username is already exists"}, status=400)
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save(is_active=True)
                user.set_password(serializer.validated_data["password"])
                user.save()
            profile,created= UserProfile.objects.get_or_create(user=user)
            if profile:
                username = request.data.get("username", None)
                first_name = request.data.get("first_name",None)
                last_name = request.data.get("last_name",None)
                email = request.data.get("email",None)
                middle_name = request.data.get("middle_name", None)
                full_name = request.data.get("full_name", None)
                gender = request.data.get("gender", None)
                phone = request.data.get("phone", None)
                if username:
                    profile.username = username
                if first_name:
                    profile.first_name = first_name
                if last_name:
                    profile.last_name = last_name
                if email:
                    profile.email = email
                if middle_name:
                    profile.middle_name = middle_name
                if full_name:
                    profile.full_name = full_name
                if gender:
                    profile.gender = gender  
                if phone:
                    profile.phone = phone
                user.save()
                profile.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status = 400)
    
    
        
class UserLogin(APIView):
    
    def post(self,request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if User.objects.filter(Q(username = username)|Q(email=username)).exists():
            user = User.objects.filter(Q(username=username)|Q(email=username))[0]

            if user.check_password(password):
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        "token": token.key,
                        "user_id":user.pk,
                        "username": user.username,
                        "email":user.email
                       
                    })
                
                return Response({"msg":"please check your email and password"},status=403)
            
            
            return Response({"msg": "invalid password"}, status=400)
        return Response({"msg":"user does not exit"})
    
# def activation_user(request, uidb64,token):
#     User = get_user_model()
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError,OverflowError,User.DoesNotExist):
#         user = None
        
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
        
#         response = """
#         <Script type="text/javascript">
#             alert('Your account has been activated. you can noe login.');
#             window.location.href = '{}';
#             </Script>
#         """
#         return HttpResponse(response)
#     else:
#         return HttpResponse("Activation link is invalid")
    
    
    
