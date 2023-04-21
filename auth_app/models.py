from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    

    
    user_type = (
        
        ('regular', 'regular'),
        ('moderator', 'moderator'),
    )
    
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=user_type , default='regular')
    description = models.TextField('Description', max_length=500, default='', blank=True)
    image = models.ImageField(default='default/profile-icon.png', upload_to='users')
    
    def __str__(self):
        return self.username
    
