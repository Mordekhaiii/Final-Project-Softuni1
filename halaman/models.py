from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, default="Default bio")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, default="Unknown")
    age = models.IntegerField(default=0)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

