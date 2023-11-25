from rest_framework import serializers
from users.models import User, UserProfile, UserSkill, Message
from rest_auth.serializers import LoginSerializer

# class UserLoginSerializer(LoginSerializer):
#
#     class Meta:
#         fields


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']
        if new_password == confirm_password:
            return attrs
        else:
            raise serializers.ValidationError({'msg': "This password not equal"})


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"


class UserSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSkill
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', "username", 'user_type', 'phone_number']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = "__all__"
