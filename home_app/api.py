from .models import *
from rest_framework import viewsets, permissions
from .serializers import *

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer
    
class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset=Sub_Category.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SubCategorySerializer

class CommunityViewSet(viewsets.ModelViewSet):
    queryset=Community.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CommunitySerializer
    
class PostViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PostSerializer