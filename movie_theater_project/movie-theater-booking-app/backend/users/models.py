from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Additional fields can be added here if needed
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional profile fields can be added here
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # Add more fields as necessary

    def __str__(self):
        return self.user.username