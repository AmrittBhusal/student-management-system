from django.urls import path,include
from rest_framework import routers
from user.views import (
    home,
    UserRegistration,
    UserLogin,
    Change_password,
    forget_password,
    reset_password,
    # UserProfileViewsets,
    # activation_user
)

router = routers.DefaultRouter()

router.register(r"sign-up", UserRegistration, basename = "users")
# router.register(r"user-profile", UserProfileViewsets, basename = "user-profile-viewset")
# router.register(r"login", UserLogin, basename = "user-login")


urlpatterns = [
    path("", include(router.urls)),
    path("home/", home),
    path("login/", UserLogin.as_view()),
    path("change-password/", Change_password, name="Change-user-password"),
    path("forget-password/", forget_password, name="forget-user-password"),
    path("reset-password/", reset_password, name="user-reset-password")
    # path("email-verification/<str:uidb64>/<str:token>/", activation_user, name="email_activation")
]