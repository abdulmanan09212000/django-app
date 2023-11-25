from django.db.models import Q
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.models import UserProfile, UserSkill, User, Message
from users.serializers import UserSkillSerializer, UserProfileSerializer, ChangePasswordSerializer, UserSerializer, MessageSerializer


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user_serializer = UserSerializer(user).data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": user_serializer})


class UserProfileView(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserSkillView(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            self.object.set_password(serializer.data.get("new_password"))
            self.object.change_password_status = True
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)


class MessageView(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user, reciver=self.kwargs.get['pk'])

    def get_queryset(self):
        return self.queryset.filter(Q(sender=self.request.user, reciver=self.kwargs.get['pk']) | Q(sender=self.kwargs.get('pk'), reciver=self.request.user))


class AllUser(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get"]
