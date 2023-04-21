from django.contrib import admin
from .models import CustomUser

class UserView(admin.ModelAdmin):
    
    list_display=("username","id","email","status")
    search_fields=("username","id","email",)
    list_filter=("status",)

admin.site.register(CustomUser, UserView)
