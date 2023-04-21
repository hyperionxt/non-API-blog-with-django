from django.contrib import admin
from .models import Community, Post, Category, Sub_Category

# Aditional view in admin panel

class CategoryAdmin(admin.ModelAdmin):

    fields = [
        
        'title',
    ]
    
    readonly_fields=('created', 'updated','author','slug')
    
    search_fields=("title", "author")
    list_display=("title","author")
    date_hierarchy="created"
    

class SubCategoryAdmin(admin.ModelAdmin):

    fields = [
        
        'title',
        'category',
    ]
    
    readonly_fields=('created', 'updated','author','slug')
    
    search_fields=("title", "author")
    list_display=("title","category","author")
    date_hierarchy="created"



class CommunityAdmin(admin.ModelAdmin):

    fields = [
        
        'title',
        'about',
        'category',
        'subcategory',
        'image',
    ]
    
    readonly_fields=('published', 'updated','author', 'slug')
    
    search_fields=("title", "author")
    list_display=("title","category","subcategory","author")
    date_hierarchy='published'
    


class PostAdmin(admin.ModelAdmin):

    fieldsets = [
        
        ("Header", {"fields":['title','community', 'author','image']}),
        ("Content", {"fields":['content']}),
        ("Date", {"fields":['published','modified']}),

    ]
    
    list_filter=("community",)
    list_display=("title","author","community","post_category","post_subcategory")
    date_hierarchy="published"
    search_fields=("title","community", "author")
    readonly_fields=('published', 'modified')
    
    


admin.site.register(Community, CommunityAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Sub_Category, SubCategoryAdmin)