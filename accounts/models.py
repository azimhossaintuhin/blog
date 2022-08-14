from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.manager import UserManager

class User(AbstractUser):
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    profile_image = models.ImageField(upload_to = 'profile_image',blank = True , null= True) 

    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return self.username
    
    def get_profile_image(self):
        url = "/static/assets/images/def.jpg"
        try:
            url = self.profile_image.url
        except :
            url = "/static/assets/images/def.jpg"

        return url    