from django.urls import path,include
from rest_framework import routers
from user.views import (
    home,
    UserRegistration,
    UserLogin,
    # activation_user
)

router = routers.DefaultRouter()

router.register(r"sign-up", UserRegistration, basename = "users")
# router.register(r"login", UserLogin, basename = "user-login")


urlpatterns = [
    path("", include(router.urls)),
    path("home/", home),
    path("login/", UserLogin.as_view()),
    # path("email-verification/<str:uidb64>/<str:token>/", activation_user, name="email_activation")
]