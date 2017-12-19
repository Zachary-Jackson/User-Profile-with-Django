from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    '''This is the profile model for a User.'''
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=1000, blank=True)
    avatar = models.ImageField(blank=True,
                               upload_to='accounts/media/images')
    hobby = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.user)
