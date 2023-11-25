from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_choice = [
        ('Learner', 'Learner'),
        ('Leader', 'Leader'),
        ('Admin', 'Admin')
    ]
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    user_type = models.CharField(choices=user_choice, default='Leader', max_length=10)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField('users.User', related_name="user_profile", on_delete=models.CASCADE, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_image/", null=True, blank=True)


class UserSkill(models.Model):
    user = models.ForeignKey('users.User', related_name="user_skill", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    experience = models.FloatField(null=True, blank=True)


class Message(models.Model):
    sender = models.ForeignKey('users.User', related_name="sender_user", on_delete=models.CASCADE, null=True, blank=True)
    reciver = models.ForeignKey('users.User', related_name='reciver_user', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
