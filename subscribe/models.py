from django.db import models
from auth_app.models import CustomUser
from home_app.models import Community

# Create your models here.



class Subscriptions(models.Model):

    username=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)


    

    class Meta:
        verbose_name='subscription'
        verbose_name_plural= 'subscriptions'
