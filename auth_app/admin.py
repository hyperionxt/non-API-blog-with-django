from django.contrib import admin
from .models import CustomUser

class UserView(admin.ModelAdmin):
    
    list_display=("username","id","email","is_superuser")
    search_fields=("username","id","email",)

admin.site.register(CustomUser, UserView)
