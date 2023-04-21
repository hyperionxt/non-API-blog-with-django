from django.contrib import admin
from .models import Comment
from mptt.admin import MPTTModelAdmin


admin.site.register(Comment, MPTTModelAdmin)

