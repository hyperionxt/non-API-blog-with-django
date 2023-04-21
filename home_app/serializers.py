from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = ('id','title','author', 'created', 'updated')
        read_only_fields = ('created', 'updated',)
