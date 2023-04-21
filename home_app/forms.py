from .models import Post, Community, Sub_Category
from django import forms


class CreateCommunity(forms.ModelForm):
    
    
    class Meta:
        model= Community
        fields = [
            
            "title",
            "about",
            "adult_content",
            "image",
        ]
          
class CreatePost(forms.ModelForm):
    
    class Meta:
        model= Post
        
        fields = [
            
            "title",
            "content",

        ]

        

class EditCommunity(forms.ModelForm):
    
    class Meta:
        model= Community
        
        fields = [
            
            "title",
            "about",
            "image",
        ]
        
class EditPost(forms.ModelForm):
    
    class Meta:
        model= Post
        
        fields = [
            
            "title",
            "content",
            "community",
        ]