from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserSkillView, UserProfileView, ChangePasswordView, LoginViewSet, MessageView, AllUser

router = DefaultRouter()
router.register("profile", UserProfileView, basename="profile")
router.register("skill", UserSkillView, basename="skill")
router.register("login", LoginViewSet, basename="login")
router.register("message", MessageView, basename="message")
router.register("all-user", AllUser, basename="all-user")

urlpatterns = [
    path("", include(router.urls)),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]

