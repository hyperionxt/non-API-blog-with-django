from django.db import models
from home_app.models import Post
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    
    post = models.ForeignKey(Post, related_name='comments', null=True, blank=True, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.CASCADE)
    parent= TreeForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField(blank=False, default="", max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Comment id {self.id} created by {self.author} in {self.post}'
    
    class MMPTMeta:
        order_insertion_by = ['-created']
        
    