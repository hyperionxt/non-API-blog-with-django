from django.contrib import admin
from .models import Subscriptions

# Register your models here.


class SubscribeInfo(admin.ModelAdmin):
    
    fields =[
        'username',
        'community',
        
    ]
    
    search_fields=("username", "community")
    list_display=('id','username','community','created')
    

admin.site.register(Subscriptions, SubscribeInfo)
