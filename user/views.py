from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status  
from django.db.models import Q 
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
# from django.contrib.auth  import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
import string
import random

from django.utils import timezone
# from .utils import account_activation_token
# from django.http import HttpResponse
from user.models import (
    User,
    UserProfile,
    PasswordResetCode,
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
                role = request.data.get("role", None)
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
                    
                if role in [
                    "IsSystemAdmin",
                    "General User"
                    "Student",
                    "Teacher"
                ]:
                    profile.role = role
                    
                else:
                    profile.role = "General User"
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


# class UserProfileViewsets(ModelViewSet):
#     queryset = UserProfile.active.order_by("id")
#     print(queryset,"**************************************************************")
    
#     serializer = UserProfileSerializers
#     print(serializer,"--------------------------------------")
#     http_method_names = ["get", "post", "patch", "delete"]
    
    
#     def get_queryset(self):
#         queryset = UserProfile.objects.order_by("-id")
#         print(queryset, "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#         id = self.request.query_params.get("id", None)
#         if id:
#             queryset = UserProfile.objects.filter(user=self.request.user)
#         return queryset


@api_view(["POST"])
def Change_password(request):
    old_password = request.data.get("old_password", None)
    new_password = request.data.get("new_password", None)
    confirm_password = request.data.get("confirm_password", None)
    user = authenticate(username = request.user.username, password = old_password)
    
    if user is not None:
        if  new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            return Response(data={"msg": "password succesfully updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "New Password and Old password is not match"})
        
    else:
        return Response ({"Error": "Incorrect Old password"}, status=status.HTTP_400_BAD_REQUEST)
    
def generate_random_code(length=6):
    char = string.ascii_letters + string.digits
    code = "".join(random.choice(char) for _ in range(length))
    return code

@api_view(["POST"])
def forget_password(request):
    email = request.data.get("email")
    if not email:
        return Response({"msg":"Email is not found"}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(email=email).first()
    if not user:
        return Response({"msg":"User is not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    reset_code = generate_random_code()
    
    PasswordResetCode.objects.update_or_create(
        user=user,
        defaults= {"code":reset_code, "is_used": False, "created_at": timezone.now()}
    )
    
    email_sent = send_mail(
        subject= "password reset code",
        message= f"your reset code is: {reset_code}",
        from_email = settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
        
    )
    return Response(
        {"message": "Password reset code sent"} if email_sent else {"message": "code sending failed"},
        status=status.HTTP_200_OK
    )
    
@api_view(["POST"])
def reset_password(request):
    email = request.data.get("email", None)
    code = request.data.get("code", None)
    new_password = request.data.get("new_password", None)
    confirm_password = request.data.get("confirm_password",None)
    
    if not email or not code or not new_password or not confirm_password:
        return Response (
            {"msg:email,code,new_password and confirm_password is required "},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.filter(email=email).first()
    if not user:
        return Response(
            {"msg": "user is not found"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    if new_password!=confirm_password:
        return Response(
            {"msg":"password doesnot match"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    reset_code = PasswordResetCode.objects.filter(user=user, code=code).first()
    if reset_code.is_used:
        return Response(
            {"msg":"code has been alreasy used"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if reset_code.is_expired():
        return Response(
            {"msg":"code has been expired"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    user.password=make_password(new_password)
    user.save()
    
    reset_code.is_used =True
    reset_code.save()
    
    return Response(
        {"msg": "Password reset sucessfully"},
        status=status.HTTP_400_BAD_REQUEST
    )
    
    