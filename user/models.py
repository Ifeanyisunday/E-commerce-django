from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Customer(AbstractUser):
    MEMBERSHIP_CHOICES = [
        ('B', 'Brass'),
        ('S', 'Silver'),
        ('G', 'Gold'),
    ]
    email = models.EmailField(unique=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default='B')