from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    
    username = models.CharField(max_length=15, unique = True, validators=[RegexValidator(r'^[a-zA-Z0-9]+$')])
    email = models.EmailField(unique=True)
    description = models.TextField('Description', max_length=500, default='', blank=True)
    is_superuser = models.BooleanField(default=False)
    image = models.ImageField(default='default/profile-icon.png', upload_to='users')
    
    def __str__(self):
        return self.username
    
