from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = ('id','title','author', 'created', 'updated')
        read_only_fields = ('created', 'updated',)

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Sub_Category
        fields = ('id','title','author', 'created', 'updated')
        read_only_fields = ('created', 'updated',)

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model= Community
        fields = ('id','title','author', 'category','subcategory', 'published', 'updated','adult_content')
        read_only_fields = ('published', 'updated',)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields = ('id','title','author','post_category','post_subcategory', 'community', 'published', 'modified')
        read_only_fields = ('published','modifiend','post_category','post_subcategory')
        

